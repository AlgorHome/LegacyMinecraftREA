// SPDX-License-Identifier: Apache-2.0
#include "diagnostics.h"
#include <bcrypt.h>
#include <algorithm>
#include <cmath>
#include <iterator>
#include <mutex>
#include <winrt/Windows.ApplicationModel.h>
#include <winrt/Windows.Storage.h>
#include <winrt/Windows.System.h>
#include <winrt/Windows.System.Diagnostics.h>

namespace lfd {
namespace {
std::wstring Hex(unsigned char const* bytes, size_t count) {
    static constexpr wchar_t digits[] = L"0123456789abcdef";
    std::wstring result;
    result.reserve(count * 2);
    for (size_t i = 0; i < count; ++i) {
        result.push_back(digits[bytes[i] >> 4]);
        result.push_back(digits[bytes[i] & 15]);
    }
    return result;
}

std::wstring NewId() {
    GUID id{};
    winrt::check_hresult(CoCreateGuid(&id));
    wchar_t text[40]{};
    if (!StringFromGUID2(id, text, static_cast<int>(std::size(text)))) {
        winrt::throw_hresult(E_FAIL);
    }
    // This random run identifier contains no machine/account identity.
    return std::wstring(text + 1, 36);
}

bool SafeCase(std::wstring const& value) {
    if (value.empty() || value.size() > 64) return false;
    for (wchar_t ch : value) {
        if (!(ch >= L'A' && ch <= L'Z') && !(ch >= L'0' && ch <= L'9') &&
            ch != L'-' && ch != L'_') return false;
    }
    return true;
}

std::wstring UtcNow() {
    SYSTEMTIME time{};
    GetSystemTime(&time);
    wchar_t text[40]{};
    swprintf_s(text, L"%04u-%02u-%02uT%02u:%02u:%02u.%03uZ",
        time.wYear, time.wMonth, time.wDay, time.wHour, time.wMinute,
        time.wSecond, time.wMilliseconds);
    return text;
}

DWORD WriteAtomic(std::wstring const& path, std::string const& content) {
    if (content.size() > 128 * 1024) return ERROR_BUFFER_OVERFLOW;
    std::wstring temporary = path + L".tmp";
    HANDLE file = CreateFile2(temporary.c_str(), GENERIC_WRITE, 0, CREATE_ALWAYS, nullptr);
    if (file == INVALID_HANDLE_VALUE) return GetLastError();
    DWORD error = ERROR_SUCCESS;
    size_t offset = 0;
    while (offset < content.size()) {
        DWORD written = 0;
        DWORD length = static_cast<DWORD>(std::min<size_t>(content.size() - offset, 65536));
        if (!WriteFile(file, content.data() + offset, length, &written, nullptr)) {
            error = GetLastError();
            break;
        }
        if (!written) { error = ERROR_WRITE_FAULT; break; }
        offset += written;
    }
    if (!error && !FlushFileBuffers(file)) error = GetLastError();
    if (!CloseHandle(file) && !error) error = GetLastError();
    if (!error && !MoveFileExW(temporary.c_str(), path.c_str(),
            MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)) error = GetLastError();
    // Keep any failed temporary write for inspection. Flush + same-directory
    // replacement is a checkpointing strategy, not a power-loss guarantee.
    return error;
}

Json Bindings(std::wstring const& caseId) {
    Json result;
    // Shared across D00/S21 receipts in this process; unrelated to a device or
    // account identity. Ordinary UWP reactivation does not generate a new ID.
    static std::wstring const processInstance = NewId();
    Text(result, L"process_instance_id", processInstance);
    Text(result, L"source_baseline", kBaseline);
    Text(result, L"package_role", L"INDEPENDENT_RUNTIME_DIAGNOSTICS");
    auto package = winrt::Windows::ApplicationModel::Package::Current();
    auto identity = package.Id();
    Flag(result, L"expected_package_identity", identity.Name() == kDiagnosticIdentity);
    auto version = identity.Version();
    Text(result, L"package_version", std::to_wstring(version.Major) + L"." +
        std::to_wstring(version.Minor) + L"." + std::to_wstring(version.Build) + L"." +
        std::to_wstring(version.Revision));
    Json hashes;
    auto root = PackageRoot();
    auto roleHash = [&](wchar_t const* role, std::wstring const& relative) {
        DWORD error = 0;
        Text(hashes, role, Sha256File(root + L"\\" + relative, &error));
        if (error) Number(hashes, (std::wstring(role) + L"_error").c_str(), error);
    };
    roleHash(L"diagnostic_exe_sha256", L"RuntimeDiagnostics.exe");
    roleHash(L"package_manifest_sha256", L"AppxManifest.xml");
    roleHash(L"input_manifest_sha256", L"diagnostic-inputs.json");
    roleHash(L"runtime_inventory_sha256", L"runtime-inventory.json");
    roleHash(L"profile_sha256", caseId == L"D00" ?
        L"profiles\\native-control.json" : L"profiles\\java21-smoke.json");
    result.Insert(L"identities", hashes);
    return result;
}
}

void Text(Json const& object, wchar_t const* name, std::wstring const& value) {
    object.SetNamedValue(name, winrt::Windows::Data::Json::JsonValue::CreateStringValue(value));
}

void Number(Json const& object, wchar_t const* name, double value) {
    object.SetNamedValue(name, std::isfinite(value) ?
        winrt::Windows::Data::Json::JsonValue::CreateNumberValue(value) :
        winrt::Windows::Data::Json::JsonValue::CreateNullValue());
}

void Flag(Json const& object, wchar_t const* name, bool value) {
    object.SetNamedValue(name, winrt::Windows::Data::Json::JsonValue::CreateBooleanValue(value));
}

std::wstring Sha256File(std::wstring const& path, DWORD* outputError) {
    if (outputError) *outputError = ERROR_SUCCESS;
    HANDLE file = CreateFile2(path.c_str(), GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_DELETE, OPEN_EXISTING, nullptr);
    if (file == INVALID_HANDLE_VALUE) {
        if (outputError) *outputError = GetLastError();
        return {};
    }
    BCRYPT_ALG_HANDLE algorithm = nullptr;
    BCRYPT_HASH_HANDLE hash = nullptr;
    DWORD objectBytes = 0, returned = 0, error = ERROR_SUCCESS;
    std::vector<unsigned char> object;
    unsigned char digest[32]{};
    if (BCryptOpenAlgorithmProvider(&algorithm, BCRYPT_SHA256_ALGORITHM, nullptr, 0) < 0 ||
        BCryptGetProperty(algorithm, BCRYPT_OBJECT_LENGTH,
            reinterpret_cast<PUCHAR>(&objectBytes), sizeof(objectBytes), &returned, 0) < 0) {
        error = ERROR_GEN_FAILURE;
    }
    if (!error) {
        object.resize(objectBytes);
        if (BCryptCreateHash(algorithm, &hash, object.data(), objectBytes, nullptr, 0, 0) < 0)
            error = ERROR_GEN_FAILURE;
    }
    unsigned char buffer[65536];
    while (!error) {
        DWORD count = 0;
        if (!ReadFile(file, buffer, sizeof(buffer), &count, nullptr)) {
            error = GetLastError();
            break;
        }
        if (!count) break;
        if (BCryptHashData(hash, buffer, count, 0) < 0) error = ERROR_GEN_FAILURE;
    }
    if (!error && BCryptFinishHash(hash, digest, sizeof(digest), 0) < 0)
        error = ERROR_GEN_FAILURE;
    if (hash) BCryptDestroyHash(hash);
    if (algorithm) BCryptCloseAlgorithmProvider(algorithm, 0);
    CloseHandle(file);
    if (outputError) *outputError = error;
    return error ? std::wstring{} : Hex(digest, sizeof(digest));
}

std::wstring PackageRoot() {
    return winrt::Windows::ApplicationModel::Package::Current().InstalledLocation().Path().c_str();
}

std::wstring LocalRoot() {
    return winrt::Windows::Storage::ApplicationData::Current().LocalFolder().Path().c_str();
}

Json ResourceSnapshot() {
    Json result;
    try {
        using winrt::Windows::System::MemoryManager;
        Number(result, L"app_memory_usage_bytes", static_cast<double>(MemoryManager::AppMemoryUsage()));
        Number(result, L"app_memory_limit_bytes", static_cast<double>(MemoryManager::AppMemoryUsageLimit()));
        Flag(result, L"memory_manager_available", true);
    } catch (winrt::hresult_error const& error) {
        Flag(result, L"memory_manager_available", false);
        Number(result, L"memory_manager_hresult", static_cast<int32_t>(error.code()));
    } catch (...) {
        Flag(result, L"memory_manager_available", false);
    }
    try {
        auto process = winrt::Windows::System::Diagnostics::ProcessDiagnosticInfo::GetForCurrentProcess();
        auto memory = process.MemoryUsage().GetReport();
        Number(result, L"working_set_bytes", static_cast<double>(memory.WorkingSetSizeInBytes()));
        Number(result, L"peak_working_set_bytes", static_cast<double>(memory.PeakWorkingSetSizeInBytes()));
        Number(result, L"private_page_count_reported", static_cast<double>(memory.PrivatePageCount()));
        Flag(result, L"process_memory_available", true);
    } catch (winrt::hresult_error const& error) {
        Flag(result, L"process_memory_available", false);
        Number(result, L"process_memory_hresult", static_cast<int32_t>(error.code()));
    } catch (...) {
        Flag(result, L"process_memory_available", false);
    }
    Flag(result, L"cpu_measured", false);
    Flag(result, L"gpu_measured", false);
    return result;
}

struct Receipt::State {
    mutable std::mutex mutex;
    std::wstring caseId, id, path, bindingJson;
    std::wstring lastCheckpointStage, lastCheckpointDetails;
    std::wstring status = L"RUNNING";
    DWORD error = ERROR_SUCCESS;
    bool terminal = false;
    uint64_t sequence = 0;
    ULONGLONG started = GetTickCount64();

    void Persist(std::wstring const& stage, std::wstring const& reason, Json const& details) {
        if (error) winrt::throw_hresult(HRESULT_FROM_WIN32(error));
        Json object = Json::Parse(bindingJson);
        Text(object, L"schema", L"legacyforge-phase6b1-runtime-receipt-v1");
        Text(object, L"case_id", caseId);
        Text(object, L"run_id", id);
        Text(object, L"status", status);
        Text(object, L"stage", stage);
        Text(object, L"reason", reason);
        Text(object, L"observed_at_utc", UtcNow());
        Number(object, L"sequence", static_cast<double>(++sequence));
        Number(object, L"elapsed_monotonic_ms", static_cast<double>(GetTickCount64() - started));
        Flag(object, L"terminal", terminal);
        Flag(object, L"minecraft_or_gameplay_tested", false);
        Flag(object, L"authentication_or_entitlements_modified", false);
        object.Insert(L"details", details);
        if (terminal && !lastCheckpointStage.empty()) {
            Text(object, L"last_durable_checkpoint_stage", lastCheckpointStage);
            object.Insert(L"last_durable_checkpoint_details", Json::Parse(lastCheckpointDetails));
        }
        auto encoded = winrt::to_string(object.Stringify());
        error = WriteAtomic(path, encoded);
        if (error) winrt::throw_hresult(HRESULT_FROM_WIN32(error));
    }
};

Receipt::Receipt(std::wstring caseId) : state_(std::make_shared<State>()) {
    if (!SafeCase(caseId)) winrt::throw_hresult(E_INVALIDARG);
    state_->caseId = std::move(caseId);
    state_->id = NewId();
    state_->bindingJson = Bindings(state_->caseId).Stringify().c_str();
    auto directory = LocalRoot() + L"\\Phase6B1Receipts";
    if (!CreateDirectoryW(directory.c_str(), nullptr)) {
        DWORD error = GetLastError();
        if (error != ERROR_ALREADY_EXISTS) state_->error = error;
    }
    DWORD attributes = GetFileAttributesW(directory.c_str());
    if (attributes == INVALID_FILE_ATTRIBUTES || !(attributes & FILE_ATTRIBUTE_DIRECTORY) ||
        (attributes & FILE_ATTRIBUTE_REPARSE_POINT)) state_->error = ERROR_ACCESS_DENIED;
    state_->path = directory + L"\\" + state_->caseId + L"-" + state_->id + L".json";
}

void Receipt::Checkpoint(std::wstring const& stage, Json const& details) {
    std::lock_guard<std::mutex> lock(state_->mutex);
    if (state_->terminal) return;
    try {
        state_->Persist(stage, L"CHECKPOINT", details);
        state_->lastCheckpointStage = stage;
        state_->lastCheckpointDetails = details.Stringify().c_str();
    }
    catch (...) {
        if (!state_->error) state_->error = ERROR_WRITE_FAULT;
        throw;
    }
}

bool Receipt::Finish(std::wstring const& status, std::wstring const& reason, Json const& details) {
    std::lock_guard<std::mutex> lock(state_->mutex);
    if (state_->terminal) return false;
    state_->terminal = true;
    bool valid = status == L"PASS" || status == L"FAILED" || status == L"BLOCKED" ||
        status == L"INCONCLUSIVE" || status == L"NOT_APPLICABLE";
    state_->status = valid ? status : L"FAILED";
    // Scheduling or slow checkpoint I/O can delay the watchdog itself. A late
    // worker must not win PASS merely because that observer could not run.
    bool latePass = state_->caseId == L"S21-JNI21" && status == L"PASS" &&
        GetTickCount64() - state_->started >= 30000;
    if (latePass) state_->status = L"INCONCLUSIVE";
    try {
        state_->Persist(L"FINAL", latePass ? L"SMOKE_DEADLINE_EXCEEDED" :
            (valid ? reason : L"INVALID_TERMINAL_STATUS"), details);
        return true;
    } catch (...) {
        if (!state_->error) state_->error = ERROR_WRITE_FAULT;
        return false;
    }
}

bool Receipt::Terminal() const {
    std::lock_guard<std::mutex> lock(state_->mutex);
    return state_->terminal;
}

std::wstring Receipt::RunId() const { return state_->id; }

DWORD Receipt::PersistenceError() const {
    std::lock_guard<std::mutex> lock(state_->mutex);
    return state_->error;
}

std::wstring Receipt::Status() const {
    std::lock_guard<std::mutex> lock(state_->mutex);
    return state_->error ? L"RECEIPT_ERROR" : state_->status;
}
}
