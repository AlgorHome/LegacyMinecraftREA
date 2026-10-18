// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Runtime Diagnostics contributors.
//
// Original diagnostic implementation. The fixed initialization request is a
// baseline comparison with LegacyForge d1453434, minecraft_launch.cpp:1335-1363.
// This is not a production fix. A used/attempted JVM is never unloaded/restarted.
#include "diagnostics.h"
#if LFD_D00_ONLY
namespace lfd {
// Defense in depth: an accidental direct S21 call is rejected synchronously.
// No S21 worker, inventory access, module loading or receipt is started here.
void RunJava21Smoke(std::shared_ptr<Receipt> const&) {
    winrt::throw_hresult(E_ACCESSDENIED);
}
}
#else
#include <jni.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cwctype>
#include <map>
#include <new>
#include <set>
#include <string>
#include <vector>

namespace lfd {
namespace {
using CreateVm = jint(JNICALL*)(JavaVM**, void**, void*);
using QueryVmArgs = jint(JNICALL*)(void*);
constexpr wchar_t kInventoryName[] = L"runtime-inventory.json";
constexpr wchar_t kFixture[] = L"Fixtures/classes/diagnostic/JniSmoke.class";
constexpr wchar_t kRuntimePrefix[] = L"Runtime\\";
constexpr size_t kMaxInventoryBytes = 2 * 1024 * 1024;
constexpr uint32_t kExpectedNativeFold = 0x10203040u ^ 0x0f0f0f0fu;
std::atomic<bool> g_smokeClaimed{false};
std::atomic<bool> g_vmAttempted{false};

// Intentional process-lifetime handles: never FreeLibrary a JVM or dependency.
std::vector<HMODULE> g_processModules;

struct InventoryFile {
    std::wstring path;
    std::wstring hash;
};

std::wstring Lower(std::wstring value) {
    std::transform(value.begin(), value.end(), value.begin(),
                   [](wchar_t c) { return static_cast<wchar_t>(std::towlower(c)); });
    return value;
}

bool IsHash(std::wstring const& value) {
    return value.size() == 64 && std::all_of(value.begin(), value.end(), [](wchar_t c) {
        return (c >= L'0' && c <= L'9') || (c >= L'a' && c <= L'f') ||
               (c >= L'A' && c <= L'F');
    });
}

// Restrict inventory paths before filesystem access. No caller-supplied absolute,
// drive-relative, ADS, empty, dot, backslash or alternate-separator components.
bool SafeRelative(std::wstring const& path) {
    if (path.empty() || path.size() > 512 || path.front() == L'/' || path.back() == L'/') return false;
    size_t begin = 0;
    while (begin < path.size()) {
        size_t end = path.find(L'/', begin);
        if (end == std::wstring::npos) end = path.size();
        std::wstring const part = path.substr(begin, end - begin);
        if (part.empty() || part == L"." || part == L".." || part.back() == L'.') return false;
        for (wchar_t c : part) {
            if (!((c >= L'a' && c <= L'z') || (c >= L'A' && c <= L'Z') ||
                  (c >= L'0' && c <= L'9') || c == L'_' || c == L'-' || c == L'.' || c == L'+')) return false;
        }
        begin = end + 1;
    }
    return true;
}

std::wstring NativePath(std::wstring path) {
    std::replace(path.begin(), path.end(), L'/', L'\\');
    return path;
}

bool IsConfinedRegular(std::wstring const& base, std::wstring const& relative, DWORD& error) {
    if (!SafeRelative(relative)) { error = ERROR_INVALID_NAME; return false; }
    const DWORD baseAttributes = GetFileAttributesW(base.c_str());
    if (baseAttributes == INVALID_FILE_ATTRIBUTES) { error = GetLastError(); return false; }
    if (!(baseAttributes & FILE_ATTRIBUTE_DIRECTORY) || (baseAttributes & FILE_ATTRIBUTE_REPARSE_POINT)) {
        error = ERROR_DIRECTORY; return false;
    }
    std::wstring current = base;
    size_t begin = 0;
    while (begin < relative.size()) {
        size_t end = relative.find(L'/', begin);
        if (end == std::wstring::npos) end = relative.size();
        current += L"\\" + relative.substr(begin, end - begin);
        DWORD attributes = GetFileAttributesW(current.c_str());
        if (attributes == INVALID_FILE_ATTRIBUTES) { error = GetLastError(); return false; }
        if (attributes & FILE_ATTRIBUTE_REPARSE_POINT) { error = ERROR_REPARSE_TAG_INVALID; return false; }
        const bool final = end == relative.size();
        if (final ? (attributes & FILE_ATTRIBUTE_DIRECTORY) != 0 : (attributes & FILE_ATTRIBUTE_DIRECTORY) == 0) {
            error = ERROR_DIRECTORY;
            return false;
        }
        begin = end + 1;
    }
    error = ERROR_SUCCESS;
    return true;
}

bool ReadInventory(std::wstring const& path, std::wstring& text, DWORD& error) {
    CREATEFILE2_EXTENDED_PARAMETERS parameters{};
    parameters.dwSize = sizeof(parameters);
    parameters.dwFileAttributes = FILE_ATTRIBUTE_NORMAL;
    HANDLE file = CreateFile2(path.c_str(), GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING, &parameters);
    if (file == INVALID_HANDLE_VALUE) { error = GetLastError(); return false; }
    LARGE_INTEGER size{};
    if (!GetFileSizeEx(file, &size)) { error = GetLastError(); CloseHandle(file); return false; }
    if (size.QuadPart <= 0 || size.QuadPart > static_cast<LONGLONG>(kMaxInventoryBytes)) {
        error = ERROR_FILE_TOO_LARGE; CloseHandle(file); return false;
    }
    std::string bytes(static_cast<size_t>(size.QuadPart), '\0');
    DWORD read = 0;
    const BOOL ok = ReadFile(file, &bytes[0], static_cast<DWORD>(bytes.size()), &read, nullptr);
    error = ok ? ERROR_SUCCESS : GetLastError();
    CloseHandle(file);
    if (!ok || read != bytes.size()) { if (ok) error = ERROR_HANDLE_EOF; return false; }
    size_t skip = bytes.size() >= 3 && static_cast<unsigned char>(bytes[0]) == 0xef &&
        static_cast<unsigned char>(bytes[1]) == 0xbb && static_cast<unsigned char>(bytes[2]) == 0xbf ? 3 : 0;
    const char* input = bytes.data() + skip;
    const int count = static_cast<int>(bytes.size() - skip);
    int chars = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, input, count, nullptr, 0);
    if (!chars) { error = GetLastError(); return false; }
    text.resize(static_cast<size_t>(chars));
    if (!MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, input, count, &text[0], chars)) {
        error = GetLastError(); return false;
    }
    return true;
}

bool Checkpoint(std::shared_ptr<Receipt> const& receipt, wchar_t const* stage, Json const& details) {
    if (receipt->Terminal() || receipt->PersistenceError()) return false;
    receipt->Checkpoint(stage, details);
    return !receipt->Terminal() && !receipt->PersistenceError();
}

void Fail(std::shared_ptr<Receipt> const& receipt, wchar_t const* reason, Json const& details,
          DWORD error = ERROR_SUCCESS) {
    Number(details, L"win32_error", error);
    if (!receipt->Terminal()) receipt->Finish(L"FAILED", reason, details);
}

bool HashMatches(std::wstring const& base, InventoryFile const& file, DWORD& error) {
    if (!IsConfinedRegular(base, file.path, error)) return false;
    std::wstring actual = Sha256File(base + L"\\" + NativePath(file.path), &error);
    if (actual.empty()) return false;
    if (Lower(actual) != Lower(file.hash)) { error = ERROR_CRC; return false; }
    return true;
}

bool CompleteRuntimeCoverage(std::wstring const& root, std::wstring const& relative,
                             std::map<std::wstring, InventoryFile> const& files,
                             std::shared_ptr<Receipt> const& receipt, size_t& entries,
                             unsigned depth, DWORD& error) {
    if (depth > 64 || entries > 40000) { error = ERROR_BUFFER_OVERFLOW; return false; }
    const std::wstring folder = relative.empty() ? root : root + L"\\" + NativePath(relative);
    WIN32_FIND_DATAW data{};
    HANDLE find = FindFirstFileExW((folder + L"\\*").c_str(), FindExInfoBasic, &data,
                                   FindExSearchNameMatch, nullptr, 0);
    if (find == INVALID_HANDLE_VALUE) {
        error = GetLastError();
        return error == ERROR_FILE_NOT_FOUND;
    }
    bool valid = true;
    do {
        if (receipt->Terminal()) { error = ERROR_CANCELLED; valid = false; break; }
        std::wstring name(data.cFileName);
        if (name == L"." || name == L"..") continue;
        ++entries;
        std::wstring path = relative.empty() ? name : relative + L"/" + name;
        if (entries > 40000 || !SafeRelative(path) || (data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT)) {
            error = ERROR_INVALID_DATA; valid = false; break;
        }
        if (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            if (!CompleteRuntimeCoverage(root, path, files, receipt, entries, depth + 1, error)) {
                valid = false; break;
            }
        } else if (files.find(Lower(path)) == files.end()) {
            error = ERROR_INVALID_DATA; valid = false; break;
        }
    } while (FindNextFileW(find, &data));
    if (valid) {
        error = GetLastError();
        valid = error == ERROR_NO_MORE_FILES;
    }
    FindClose(find);
    return valid;
}

bool LoadedModuleMatches(HMODULE module, std::wstring const& hash, DWORD& error) {
    std::vector<wchar_t> path(32768);
    DWORD length = GetModuleFileNameW(module, path.data(), static_cast<DWORD>(path.size()));
    if (!length || length >= path.size()) { error = length ? ERROR_INSUFFICIENT_BUFFER : GetLastError(); return false; }
    std::wstring actual = Sha256File(std::wstring(path.data(), length), &error);
    if (actual.empty()) return false;
    if (Lower(actual) != Lower(hash)) { error = ERROR_CRC; return false; }
    return true;
}

uint32_t ExpectedChecksum() {
    uint32_t value = 0x13579bdfu;
    for (uint32_t i = 0; i < 4096; ++i) {
        value ^= i * 0x045d9f3bu;
        value = (value << 5) | (value >> 27);
        value += 0x9e3779b9u;
    }
    return value;
}

jint JNICALL NativeFold(JNIEnv*, jclass, jint value) {
    return value ^ static_cast<jint>(0x0f0f0f0f);
}

bool UnexpectedJavaException(JNIEnv* env) {
    if (!env->ExceptionCheck()) return false;
    env->ExceptionClear(); // Never ExceptionDescribe, message/toString or raw stderr export.
    return true;
}

std::string Utf8(std::wstring const& value) {
    int size = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, value.data(),
                                  static_cast<int>(value.size()), nullptr, 0, nullptr, nullptr);
    if (!size) return {};
    std::string output(static_cast<size_t>(size), '\0');
    if (!WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, value.data(),
                            static_cast<int>(value.size()), &output[0], size, nullptr, nullptr)) return {};
    return output;
}

void RunImpl(std::shared_ptr<Receipt> const& receipt) {
    if (!receipt || receipt->Terminal()) return;
    bool unused = false;
    if (!g_smokeClaimed.compare_exchange_strong(unused, true)) {
        receipt->Finish(L"BLOCKED", L"FRESH_PROCESS_REQUIRED");
        return;
    }
    Json details{};
    Number(details, L"jni_requested", JNI_VERSION_21);
    Number(details, L"expected_java_major", 21);
    Flag(details, L"vm_creation_attempted", false);
    // Unreached observations are unknown, not synthetic rejection results.
    details.Insert(L"query_accepted", winrt::Windows::Data::Json::JsonValue::CreateNullValue());
    details.Insert(L"vm_created", winrt::Windows::Data::Json::JsonValue::CreateNullValue());
    details.Insert(L"java_body_verified", winrt::Windows::Data::Json::JsonValue::CreateNullValue());
    Flag(details, L"jit_validated", false);
    Flag(details, L"wx_validated", false);
    Text(details, L"runtime_role", L"PACKAGED_JAVA21");
    const std::wstring package = PackageRoot();
    if (package.empty()) { receipt->Finish(L"BLOCKED", L"PACKAGE_ROOT_UNAVAILABLE", details); return; }
    if (!Checkpoint(receipt, L"RUNTIME_INVENTORY_READ", details)) return;
    DWORD error = ERROR_SUCCESS;
    std::wstring input;
    if (!ReadInventory(package + L"\\" + kInventoryName, input, error)) {
        Number(details, L"win32_error", error);
        receipt->Finish(L"BLOCKED", L"RUNTIME_INVENTORY_UNAVAILABLE", details);
        return;
    }
    Json inventory = Json::Parse(input);
    if (!inventory.GetNamedBoolean(L"available", false)) {
        receipt->Finish(L"BLOCKED", L"APPROVED_RUNTIME_NOT_SUPPLIED", details); return;
    }
    if (!inventory.GetNamedBoolean(L"approvedForDiagnosticPackaging", false)) {
        receipt->Finish(L"BLOCKED", L"RUNTIME_APPROVAL_MISSING", details); return;
    }
    if (inventory.GetNamedString(L"schema") != L"legacyforge-runtime-inventory-v1" ||
        inventory.GetNamedNumber(L"expectedJavaMajor") != 21 ||
        inventory.GetNamedString(L"architecture") != L"x64") {
        Fail(receipt, L"RUNTIME_INVENTORY_CONTRACT_MISMATCH", details, ERROR_INVALID_DATA); return;
    }
    auto files = inventory.GetNamedArray(L"files");
    if (files.Size() == 0 || files.Size() > 20000) {
        Fail(receipt, L"RUNTIME_INVENTORY_FILE_COUNT_INVALID", details, ERROR_INVALID_DATA); return;
    }
    std::map<std::wstring, InventoryFile> indexed;
    std::vector<InventoryFile> licenses;
    for (auto const& value : files) {
        auto file = value.GetObject();
        InventoryFile entry{std::wstring(file.GetNamedString(L"path")), std::wstring(file.GetNamedString(L"sha256"))};
        std::wstring sourceId(file.GetNamedString(L"sourceId"));
        InventoryFile license{std::wstring(file.GetNamedString(L"licensePath")), std::wstring(file.GetNamedString(L"licenseSha256"))};
        if (!SafeRelative(entry.path) || !IsHash(entry.hash) || !SafeRelative(license.path) ||
            !IsHash(license.hash) || sourceId.empty() || sourceId.size() > 1024 ||
            !indexed.emplace(Lower(entry.path), entry).second) {
            Fail(receipt, L"RUNTIME_INVENTORY_ENTRY_INVALID", details, ERROR_INVALID_DATA); return;
        }
        licenses.push_back(license);
    }
    const std::array<wchar_t const*, 6> required{{
        L"bin/vcruntime140.dll", L"bin/vcruntime140_1.dll", L"bin/msvcp140.dll",
        L"bin/jli.dll", L"bin/server/jvm.dll", L"bin/java.dll"
    }};
    auto order = inventory.GetNamedArray(L"loadOrder");
    if (order.Size() != required.size()) {
        Fail(receipt, L"RUNTIME_LOAD_ORDER_INVALID", details, ERROR_INVALID_DATA); return;
    }
    for (uint32_t i = 0; i < required.size(); ++i) {
        if (std::wstring(order.GetStringAt(i)) != required[i] || indexed.find(Lower(required[i])) == indexed.end()) {
            Fail(receipt, L"RUNTIME_REQUIRED_MODULE_NOT_DECLARED", details, ERROR_INVALID_DATA); return;
        }
    }
    const std::wstring runtime = package + L"\\Runtime";
    Number(details, L"inventory_file_count", static_cast<double>(indexed.size()));
    if (!Checkpoint(receipt, L"RUNTIME_HASH_VERIFICATION", details)) return;
    size_t checked = 0;
    for (auto const& pair : indexed) {
        if (receipt->Terminal()) return;
        if (!HashMatches(runtime, pair.second, error)) {
            Number(details, L"inventory_file_index", static_cast<double>(checked));
            Fail(receipt, L"RUNTIME_ARTIFACT_MISSING_OR_HASH_MISMATCH", details, error); return;
        }
        ++checked;
    }
    for (auto const& license : licenses) {
        auto found = indexed.find(Lower(license.path));
        if (found == indexed.end() || Lower(found->second.hash) != Lower(license.hash)) {
            Fail(receipt, L"RUNTIME_LICENSE_NOT_HASH_BOUND", details, ERROR_INVALID_DATA); return;
        }
    }
    size_t enumerated = 0;
    if (!CompleteRuntimeCoverage(runtime, L"", indexed, receipt, enumerated, 0, error)) {
        if (!receipt->Terminal()) Fail(receipt, L"RUNTIME_INVENTORY_COVERAGE_MISMATCH", details, error);
        return;
    }
    Flag(details, L"runtime_inventory_complete", true);
    Number(details, L"verified_runtime_files", static_cast<double>(checked));
    Text(details, L"jvm_sha256", Lower(indexed.at(L"bin/server/jvm.dll").hash));
    auto fixtures = inventory.GetNamedArray(L"fixtureFiles");
    if (fixtures.Size() != 1) {
        Fail(receipt, L"FIXTURE_INVENTORY_INVALID", details, ERROR_INVALID_DATA); return;
    }
    auto fixture = fixtures.GetObjectAt(0);
    InventoryFile classFile{std::wstring(fixture.GetNamedString(L"path")), std::wstring(fixture.GetNamedString(L"sha256"))};
    if (classFile.path != kFixture || !IsHash(classFile.hash) || !HashMatches(package, classFile, error)) {
        Fail(receipt, L"FIXTURE_MISSING_OR_HASH_MISMATCH", details, error ? error : ERROR_INVALID_DATA); return;
    }
    Text(details, L"fixture_class_sha256", Lower(classFile.hash));
    // Do not permit inherited launcher/JDK options to change this fixed scenario.
    for (auto name : {L"JAVA_TOOL_OPTIONS", L"_JAVA_OPTIONS", L"JDK_JAVA_OPTIONS", L"CLASSPATH"}) {
        if (GetEnvironmentVariableW(name, nullptr, 0) != 0) {
            receipt->Finish(L"BLOCKED", L"UNREVIEWED_JAVA_ENVIRONMENT", details); return;
        }
    }
    details.Insert(L"resources_before_load", ResourceSnapshot());
    JsonArray moduleRows{};
    details.Insert(L"module_loads", moduleRows);
    if (!Checkpoint(receipt, L"PACKAGED_MODULE_LOAD", details)) return;
    HMODULE jvm = nullptr;
    for (size_t i = 0; i < required.size(); ++i) {
        if (receipt->Terminal()) return;
        Number(details, L"module_index", static_cast<double>(i));
        Text(details, L"fixed_module_role", required[i]);
        if (!Checkpoint(receipt, L"PACKAGED_MODULE_LOAD_ATTEMPT", details)) return;
        const std::wstring relative = std::wstring(kRuntimePrefix) + NativePath(required[i]);
        HMODULE loaded = LoadPackagedLibrary(relative.c_str(), 0);
        error = loaded ? ERROR_SUCCESS : GetLastError();
        if (receipt->Terminal()) return;
        Json row{};
        Number(row, L"index", static_cast<double>(i));
        Text(row, L"fixed_module_role", required[i]);
        Text(row, L"expected_sha256", Lower(indexed.at(Lower(required[i])).hash));
        Number(row, L"win32_error", error);
        Flag(row, L"load_succeeded", loaded != nullptr);
        Flag(row, L"transitive_dependency_identity_unresolved", !loaded && error == ERROR_MOD_NOT_FOUND);
        moduleRows.Append(row);
        if (!Checkpoint(receipt, L"PACKAGED_MODULE_LOAD_RESULT", details)) return;
        if (!loaded) { Fail(receipt, L"PACKAGED_MODULE_LOAD_FAILED", details, error); return; }
        g_processModules.push_back(loaded);
        if (!LoadedModuleMatches(loaded, indexed.at(Lower(required[i])).hash, error)) {
            Fail(receipt, L"LOADED_MODULE_IDENTITY_MISMATCH", details, error); return;
        }
        Flag(row, L"loaded_hash_matches", true);
        if (!Checkpoint(receipt, L"PACKAGED_MODULE_IDENTITY_VERIFIED", details)) return;
        if (i == 4) jvm = loaded;
    }
    auto query = reinterpret_cast<QueryVmArgs>(GetProcAddress(jvm, "JNI_GetDefaultJavaVMInitArgs"));
    auto create = reinterpret_cast<CreateVm>(GetProcAddress(jvm, "JNI_CreateJavaVM"));
    Flag(details, L"query_export_found", query != nullptr);
    Flag(details, L"create_export_found", create != nullptr);
    if (!query || !create) { Fail(receipt, L"JNI_EXPORT_MISSING", details, ERROR_PROC_NOT_FOUND); return; }
    JavaVMInitArgs defaults{};
    defaults.version = JNI_VERSION_21;
    if (!Checkpoint(receipt, L"JNI21_INITIALIZATION_QUERY", details)) return;
    jint queried = query(&defaults);
    if (receipt->Terminal()) return;
    Number(details, L"jni_query_result", queried);
    Number(details, L"jni_query_returned_version", defaults.version);
    Flag(details, L"query_accepted", queried == JNI_OK);
    if (queried != JNI_OK) { Fail(receipt, L"JNI21_QUERY_REJECTED", details); return; }
    std::string classPath = Utf8(package + L"\\Fixtures\\classes");
    if (classPath.empty()) { Fail(receipt, L"FIXTURE_CLASSPATH_ENCODING_FAILED", details, ERROR_NO_UNICODE_TRANSLATION); return; }
    std::wstring childName = L"java21-" + receipt->RunId();
    std::wstring local = LocalRoot();
    if (!SafeRelative(childName) || local.empty()) { Fail(receipt, L"PRIVATE_RUNTIME_ROOT_INVALID", details, ERROR_INVALID_NAME); return; }
    std::wstring privateRoot = local + L"\\" + childName;
    if (!CreateDirectoryW(privateRoot.c_str(), nullptr)) { Fail(receipt, L"PRIVATE_RUNTIME_ROOT_CREATE_FAILED", details, GetLastError()); return; }
    for (auto name : {L"home", L"tmp", L"logs"}) {
        if (!CreateDirectoryW((privateRoot + L"\\" + name).c_str(), nullptr)) {
            Fail(receipt, L"PRIVATE_RUNTIME_CHILD_CREATE_FAILED", details, GetLastError()); return;
        }
    }
    std::string home = Utf8(privateRoot + L"\\home");
    std::string temporary = Utf8(privateRoot + L"\\tmp");
    std::string privateErrorLog = Utf8(privateRoot + L"\\logs\\hs_err_pid%p.log");
    if (home.empty() || temporary.empty() || privateErrorLog.empty()) {
        Fail(receipt, L"PRIVATE_RUNTIME_PATH_ENCODING_FAILED", details, ERROR_NO_UNICODE_TRANSLATION); return;
    }
    Flag(details, L"app_local_home_and_tmp_options_set", true);
    Text(details, L"private_error_log_role", L"APP_LOCAL_NOT_EXPORTED");
    std::array<std::string, 7> optionStrings{{
        "-Xms16m", "-Xmx64m", "-XX:-UsePerfData", "-Djava.class.path=" + classPath,
        "-Duser.home=" + home, "-Djava.io.tmpdir=" + temporary, "-XX:ErrorFile=" + privateErrorLog
    }};
    std::array<JavaVMOption, 7> options{};
    for (size_t i = 0; i < options.size(); ++i) options[i].optionString = &optionStrings[i][0];
    JavaVMInitArgs arguments{};
    arguments.version = JNI_VERSION_21; // Exact fixed baseline request. No downgrade/fallback.
    arguments.nOptions = static_cast<jint>(options.size());
    arguments.options = options.data();
    arguments.ignoreUnrecognized = JNI_FALSE;
    bool neverAttempted = false;
    if (!g_vmAttempted.compare_exchange_strong(neverAttempted, true)) {
        receipt->Finish(L"BLOCKED", L"FRESH_PROCESS_REQUIRED", details); return;
    }
    Flag(details, L"vm_creation_attempted", true);
    Flag(details, L"vm_creation_call_returned", false);
    if (!Checkpoint(receipt, L"JNI21_VM_CREATION_ATTEMPT", details)) return;
    if (receipt->Terminal()) return;
    JavaVM* vm = nullptr;
    JNIEnv* env = nullptr;
    jint result = create(&vm, reinterpret_cast<void**>(&env), &arguments);
    // No FreeLibrary/DestroyJavaVM on any branch after this call, including failure.
    if (receipt->Terminal()) return;
    Flag(details, L"vm_creation_call_returned", true);
    Number(details, L"jni_create_result", result);
    Flag(details, L"vm_pointer_nonnull", vm != nullptr);
    Flag(details, L"env_pointer_nonnull", env != nullptr);
    Flag(details, L"vm_created", result == JNI_OK && vm && env);
    if (result != JNI_OK || !vm || !env) { Fail(receipt, L"JNI21_VM_CREATION_FAILED", details); return; }
    Flag(details, L"vm_created", true);
    details.Insert(L"resources_after_vm", ResourceSnapshot());
    if (!Checkpoint(receipt, L"JNI21_INTERFACE_OBSERVATION", details)) return;
    Number(details, L"env_interface_version", env->GetVersion());
    JNIEnv* requested = nullptr;
    jint getEnv = vm->GetEnv(reinterpret_cast<void**>(&requested), JNI_VERSION_21);
    if (receipt->Terminal()) return;
    Number(details, L"jni_get_env_result", getEnv);
    if (getEnv != JNI_OK || requested != env) { Fail(receipt, L"JNI21_INTERFACE_UNAVAILABLE", details); return; }
    if (!Checkpoint(receipt, L"SELF_AUTHORED_JAVA_BODY", details)) return;
    jclass body = env->FindClass("diagnostic/JniSmoke");
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !body) { Fail(receipt, L"FIXTURE_CLASS_LOOKUP_FAILED", details); return; }
    JNINativeMethod nativeMethod{};
    nativeMethod.name = const_cast<char*>("nativeFold");
    nativeMethod.signature = const_cast<char*>("(I)I");
    nativeMethod.fnPtr = reinterpret_cast<void*>(NativeFold);
    jint registered = env->RegisterNatives(body, &nativeMethod, 1);
    if (receipt->Terminal()) return;
    Number(details, L"jni_register_natives_result", registered);
    if (UnexpectedJavaException(env) || registered != JNI_OK) { Fail(receipt, L"SYNTHETIC_NATIVE_REGISTRATION_FAILED", details); return; }
    jmethodID run = env->GetStaticMethodID(body, "run", "()[J");
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !run) { Fail(receipt, L"FIXTURE_ENTRYPOINT_MISSING", details); return; }
    auto values = static_cast<jlongArray>(env->CallStaticObjectMethod(body, run));
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !values || env->GetArrayLength(values) != 4) {
        Fail(receipt, L"JAVA_BODY_RESULT_INVALID", details); return;
    }
    std::array<jlong, 4> actual{};
    env->GetLongArrayRegion(values, 0, static_cast<jsize>(actual.size()), actual.data());
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env)) { Fail(receipt, L"JAVA_BODY_RESULT_READ_FAILED", details); return; }
    Number(details, L"observed_java_major", static_cast<double>(actual[0]));
    Number(details, L"observed_architecture_code", static_cast<double>(actual[1]));
    Number(details, L"observed_checksum", static_cast<double>(actual[2]));
    Number(details, L"observed_native_callback", static_cast<double>(actual[3]));
    if (actual[0] != 21 || actual[1] != 1 || actual[2] != ExpectedChecksum() || actual[3] != kExpectedNativeFold) {
        Fail(receipt, L"JAVA21_SYNTHETIC_VALUE_MISMATCH", details); return;
    }
    if (!Checkpoint(receipt, L"JNI_ARRAY_ROUNDTRIP", details)) return;
    jmethodID roundTrip = env->GetStaticMethodID(body, "roundTrip", "([I)[I");
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !roundTrip) { Fail(receipt, L"ARRAY_ENTRYPOINT_MISSING", details); return; }
    const std::array<jint, 4> inputValues{{0, 1, -1, 0x12345678}};
    jintArray inputArray = env->NewIntArray(static_cast<jsize>(inputValues.size()));
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !inputArray) { Fail(receipt, L"ARRAY_ALLOCATION_FAILED", details); return; }
    env->SetIntArrayRegion(inputArray, 0, static_cast<jsize>(inputValues.size()), inputValues.data());
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env)) { Fail(receipt, L"ARRAY_INPUT_FAILED", details); return; }
    auto outputArray = static_cast<jintArray>(env->CallStaticObjectMethod(body, roundTrip, inputArray));
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !outputArray || env->GetArrayLength(outputArray) != inputValues.size()) {
        Fail(receipt, L"ARRAY_OUTPUT_INVALID", details); return;
    }
    std::array<jint, 4> outputValues{};
    env->GetIntArrayRegion(outputArray, 0, static_cast<jsize>(outputValues.size()), outputValues.data());
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env)) { Fail(receipt, L"ARRAY_OUTPUT_READ_FAILED", details); return; }
    for (size_t i = 0; i < inputValues.size(); ++i) {
        if (outputValues[i] != (inputValues[i] ^ static_cast<jint>(0x5a5a5a5a))) {
            Fail(receipt, L"ARRAY_ROUNDTRIP_MISMATCH", details); return;
        }
    }
    Flag(details, L"array_roundtrip_verified", true);
    if (!Checkpoint(receipt, L"CONTROLLED_JAVA_EXCEPTION", details)) return;
    jclass expectedException = env->FindClass("java/lang/IllegalStateException");
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !expectedException) {
        Fail(receipt, L"CONTROLLED_EXCEPTION_CLASS_MISSING", details); return;
    }
    jmethodID throwMethod = env->GetStaticMethodID(body, "controlledException", "()V");
    if (receipt->Terminal()) return;
    if (UnexpectedJavaException(env) || !throwMethod) {
        Fail(receipt, L"CONTROLLED_EXCEPTION_ENTRYPOINT_MISSING", details); return;
    }
    env->CallStaticVoidMethod(body, throwMethod);
    if (receipt->Terminal()) return;
    jthrowable exception = env->ExceptionOccurred();
    env->ExceptionClear();
    bool expectedThrown = exception && env->IsInstanceOf(exception, expectedException);
    if (UnexpectedJavaException(env) || !expectedThrown) { Fail(receipt, L"CONTROLLED_EXCEPTION_MISMATCH", details); return; }
    Flag(details, L"controlled_exception_verified", true);
    Flag(details, L"java_body_verified", true);
    details.Insert(L"resources_after_body", ResourceSnapshot());
    if (receipt->Terminal()) return;
    env->DeleteLocalRef(exception);
    env->DeleteLocalRef(expectedException);
    env->DeleteLocalRef(outputArray);
    env->DeleteLocalRef(inputArray);
    env->DeleteLocalRef(values);
    env->DeleteLocalRef(body);
    if (!Checkpoint(receipt, L"JNI_WORKER_DETACH", details)) return;
    jint detached = vm->DetachCurrentThread();
    if (receipt->Terminal()) return;
    Number(details, L"jni_detach_result", detached);
    if (detached != JNI_OK) { Fail(receipt, L"JNI_WORKER_DETACH_FAILED", details); return; }
    Flag(details, L"fresh_process_required", true);
    receipt->Finish(L"PASS", L"JAVA21_JNI21_SYNTHETIC_SMOKE_OBSERVED", details);
}
} // namespace

void RunJava21Smoke(std::shared_ptr<Receipt> const& receipt) {
    try {
        RunImpl(receipt);
    } catch (winrt::hresult_error const& failure) {
        if (receipt && !receipt->Terminal()) {
            Json details{};
            Number(details, L"hresult", static_cast<int32_t>(failure.code().value));
            receipt->Finish(L"FAILED", L"HARNESS_API_OR_INVENTORY_PARSE_FAILED", details);
        }
    } catch (std::bad_alloc const&) {
        if (receipt && !receipt->Terminal()) {
            Json details{};
            Number(details, L"win32_error", ERROR_NOT_ENOUGH_MEMORY);
            receipt->Finish(L"FAILED", L"HARNESS_ALLOCATION_FAILED", details);
        }
    } catch (...) {
        if (receipt && !receipt->Terminal()) {
            receipt->Finish(L"FAILED", L"HARNESS_UNEXPECTED_EXCEPTION");
        }
    }
}
} // namespace lfd

#endif // LFD_D00_ONLY
