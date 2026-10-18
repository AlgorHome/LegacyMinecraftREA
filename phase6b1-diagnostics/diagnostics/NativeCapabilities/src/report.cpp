// SPDX-License-Identifier: Apache-2.0
// Original diagnostic code; hash/atomic-write strategy adapted from accepted D00 report.cpp.
#include "native.h"
#include <bcrypt.h>
#include <chrono>
#include <vector>
#include <winrt/Windows.ApplicationModel.h>
#include <winrt/Windows.Storage.h>
#include <winrt/Windows.System.h>

namespace lfn {
void Text(Json const& j, wchar_t const* k, std::wstring const& v) { j.SetNamedValue(k, winrt::Windows::Data::Json::JsonValue::CreateStringValue(v)); }
void Number(Json const& j, wchar_t const* k, double v) { j.SetNamedValue(k, winrt::Windows::Data::Json::JsonValue::CreateNumberValue(v)); }
void Flag(Json const& j, wchar_t const* k, bool v) { j.SetNamedValue(k, winrt::Windows::Data::Json::JsonValue::CreateBooleanValue(v)); }
std::wstring Hex(HRESULT code) { wchar_t s[16]{}; swprintf_s(s, L"0x%08X", static_cast<unsigned>(code)); return s; }
namespace {
std::wstring NewId() { GUID id{}; winrt::check_hresult(CoCreateGuid(&id)); wchar_t s[40]{}; if (!StringFromGUID2(id,s,40)) winrt::throw_hresult(E_FAIL); return std::wstring(s+1,36); }
std::wstring Now() { SYSTEMTIME t{}; GetSystemTime(&t); wchar_t s[40]{}; swprintf_s(s,L"%04u-%02u-%02uT%02u:%02u:%02u.%03uZ",t.wYear,t.wMonth,t.wDay,t.wHour,t.wMinute,t.wSecond,t.wMilliseconds); return s; }
DWORD AtomicWrite(std::wstring const& path, std::string const& data) {
    if (data.size()>128*1024) return ERROR_BUFFER_OVERFLOW;
    HANDLE file=CreateFile2((path+L".tmp").c_str(),GENERIC_WRITE,0,CREATE_ALWAYS,nullptr);
    if(file==INVALID_HANDLE_VALUE) return GetLastError();
    DWORD error=0; size_t offset=0;
    while(offset<data.size()) { DWORD n=0; if(!WriteFile(file,data.data()+offset,static_cast<DWORD>(data.size()-offset),&n,nullptr)) {error=GetLastError(); break;} if(!n){error=ERROR_WRITE_FAULT;break;} offset+=n; }
    if(!error && !FlushFileBuffers(file)) error=GetLastError();
    if(!CloseHandle(file) && !error) error=GetLastError();
    if(!error && !MoveFileExW((path+L".tmp").c_str(),path.c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)) error=GetLastError();
    return error;
}
}
std::wstring HashFile(std::wstring const& path, DWORD* error) {
    *error=0; HANDLE file=CreateFile2(path.c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_DELETE,OPEN_EXISTING,nullptr);
    if(file==INVALID_HANDLE_VALUE){*error=GetLastError();return {};}
    BCRYPT_ALG_HANDLE algorithm=nullptr; BCRYPT_HASH_HANDLE hash=nullptr;
    DWORD size=0,returned=0; std::vector<unsigned char> object; unsigned char digest[32]{},buffer[16384]{};
    if(BCryptOpenAlgorithmProvider(&algorithm,BCRYPT_SHA256_ALGORITHM,nullptr,0)<0 || BCryptGetProperty(algorithm,BCRYPT_OBJECT_LENGTH,reinterpret_cast<PUCHAR>(&size),sizeof(size),&returned,0)<0) *error=ERROR_GEN_FAILURE;
    if(!*error){object.resize(size);if(BCryptCreateHash(algorithm,&hash,object.data(),size,nullptr,0,0)<0)*error=ERROR_GEN_FAILURE;}
    while(!*error){DWORD n=0;if(!ReadFile(file,buffer,sizeof(buffer),&n,nullptr)){*error=GetLastError();break;}if(!n)break;if(BCryptHashData(hash,buffer,n,0)<0)*error=ERROR_GEN_FAILURE;}
    if(!*error && BCryptFinishHash(hash,digest,32,0)<0)*error=ERROR_GEN_FAILURE;
    if(hash)BCryptDestroyHash(hash);if(algorithm)BCryptCloseAlgorithmProvider(algorithm,0);CloseHandle(file);
    if(*error)return {}; std::wstring value; constexpr wchar_t hex[]=L"0123456789abcdef";
    for(auto byte:digest){value+=hex[byte>>4];value+=hex[byte&15];} return value;
}
Json Memory() {
    Json j;
    try { Number(j,L"usage_bytes",static_cast<double>(winrt::Windows::System::MemoryManager::AppMemoryUsage())); Number(j,L"limit_bytes",static_cast<double>(winrt::Windows::System::MemoryManager::AppMemoryUsageLimit())); Flag(j,L"available",true); }
    catch(winrt::hresult_error const& e){Flag(j,L"available",false);Text(j,L"hresult",Hex(e.code()));}
    catch(...){Flag(j,L"available",false);Text(j,L"hresult",Hex(E_FAIL));} return j;
}
Receipt::Receipt() {
    static std::wstring const processId=NewId(); process_=processId;run_=NewId();
    auto package=winrt::Windows::ApplicationModel::Package::Current(); auto id=package.Id(); auto v=id.Version();
    if(id.Name()!=Identity || id.Publisher()!=L"CN=LegacyForgeDiagnostics" || v.Major!=0 || v.Minor!=2 || v.Build!=5 || v.Revision!=0 || id.Architecture()!=winrt::Windows::System::ProcessorArchitecture::X64) winrt::throw_hresult(E_ACCESSDENIED);
    Json binding;Text(binding,L"schema",L"legacyforge-native-capability-receipt-v6");Text(binding,L"case_id",Case);Text(binding,L"source_commit",SourceCommit);Text(binding,L"build_id",BuildId);
    Text(binding,L"production_comparison_commit",L"d1453434ceefe73bef5aff497194e09f39dde7e1");Text(binding,L"frozen_d00_reference_commit",L"553c6554f40f1372b0ea09f6badbbb98e133a9ab");
    Text(binding,L"frozen_hw01_reference_commit",L"a3f72874241914f6048d4ca9ec4fc0edc978625d");
    Text(binding,L"frozen_fmt01_reference_commit",L"bbe3a42c422e4328d5f98c07a9370fa948d0cbbf");
    Text(binding,L"frozen_res01a_reference_commit",L"4457142ff1fd9e01371eb446612c70162ce93357");
    Text(binding,L"frozen_srv01_reference_commit",L"e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8");
    Text(binding,L"frozen_srv02_reference_commit",L"c81d0f48286513f7a7579a1d2d786cca4f5e60e2");
    Text(binding,L"package_name",Identity);Text(binding,L"package_publisher",L"CN=LegacyForgeDiagnostics");Text(binding,L"package_version",L"0.2.5.0");Text(binding,L"architecture",L"x64");Text(binding,L"application_id",L"App");Flag(binding,L"expected_package_identity",true);
    Text(binding,L"run_id",run_);Text(binding,L"process_instance_id",process_);Flag(binding,L"java_jni_enabled",false);Flag(binding,L"minecraft_or_gameplay_tested",false);Flag(binding,L"all_d06_certified",false);Flag(binding,L"hardware_device_requested",true);Flag(binding,L"watchdog_cancels_native_calls",false);
    Json hashes;std::wstring root=package.InstalledLocation().Path().c_str();
    const struct{wchar_t const* role;wchar_t const* relative;} roles[]={{L"executable_sha256",L"NativeCapabilities.exe"},{L"manifest_sha256",L"AppxManifest.xml"},{L"build_inputs_sha256",L"native-inputs.json"},{L"policy_sha256",L"profiles\\D06-SRV03.json"},{L"schema_sha256",L"contracts\\native-receipt.schema.json"},{L"inventory_sha256",L"native-inventory.json"}};
    for(auto const& role:roles){DWORD error=0;auto digest=HashFile(root+L"\\"+role.relative,&error);if(error || digest.size()!=64)winrt::throw_hresult(HRESULT_FROM_WIN32(error?error:ERROR_INVALID_DATA));Text(hashes,role.role,digest);}
    binding.Insert(L"payload_hashes",hashes);binding_=binding.Stringify().c_str();
    std::wstring local=winrt::Windows::Storage::ApplicationData::Current().LocalFolder().Path().c_str();local+=L"\\NativeCapabilityReceipts";
    if(!CreateDirectoryW(local.c_str(),nullptr) && GetLastError()!=ERROR_ALREADY_EXISTS) winrt::throw_last_error();
    DWORD attr=GetFileAttributesW(local.c_str());if(attr==INVALID_FILE_ATTRIBUTES || !(attr&FILE_ATTRIBUTE_DIRECTORY) || (attr&FILE_ATTRIBUTE_REPARSE_POINT))winrt::throw_hresult(E_ACCESSDENIED);
    path_=local+L"\\D06-SRV03-"+run_+L".json";
}
void Receipt::ArmDeadline(){deadline_=GetTickCount64()+DeadlineMs;}
bool Receipt::Expired()const{auto d=deadline_.load();return d && GetTickCount64()>=d;}
Result Receipt::Snapshot()const{std::lock_guard<std::mutex> lock(resultMutex_);auto value=result_;if(Terminal() && !Settled())value.persistence=ERROR_IO_PENDING;return value;}
void Receipt::DeviceObservation(HRESULT hr,unsigned level){std::lock_guard<std::mutex> lock(resultMutex_);result_.creation=Hex(hr);if(SUCCEEDED(hr))result_.feature=Hex(static_cast<HRESULT>(level));}
bool Receipt::Persist(wchar_t const* stage,Json const& details,bool final){
    std::unique_lock<std::timed_mutex> io(ioMutex_,std::defer_lock);
    if(!io.try_lock_for(std::chrono::milliseconds(100))){std::lock_guard<std::mutex> lock(resultMutex_);result_.persistence=WAIT_TIMEOUT;return false;}
    if(!final && Terminal())return false;
    Json document=Json::Parse(binding_);Result snapshot=Snapshot();
    Text(document,L"status",snapshot.status);Text(document,L"reason",snapshot.reason);Text(document,L"stage",stage);Flag(document,L"terminal",final);Number(document,L"sequence",static_cast<double>(++sequence_));Number(document,L"elapsed_monotonic_ms",static_cast<double>(GetTickCount64()-started_));Number(document,L"deadline_ms",static_cast<double>(DeadlineMs));Text(document,L"observed_at_utc",Now());Text(document,L"last_durable_checkpoint_stage",lastCheckpoint_);
    // Only bytes successfully retrieved later prove persistence. Never claim future flush success.
    Text(document,L"receipt_persistence_result",L"VERIFY_BY_RETRIEVAL");document.Insert(L"details",details);
    DWORD error=AtomicWrite(path_,winrt::to_string(document.Stringify()));
    // A running checkpoint may finish after a timeout won but could not acquire
    // the I/O lock. Never let that older write erase the terminal persistence error.
    {std::lock_guard<std::mutex> lock(resultMutex_);if(final || !Terminal())result_.persistence=error;}
    if(!error && !final)lastCheckpoint_=stage;return !error;
}
bool Receipt::Checkpoint(wchar_t const* stage,Json const& details){return Persist(stage,details,false);}
bool Receipt::Finish(std::wstring status,std::wstring reason,Json const& details){
    if(status==L"PASS" && Expired()){status=L"INCONCLUSIVE";reason=L"DEADLINE_EXCEEDED";}
    if(terminal_.exchange(true))return false;
    {std::lock_guard<std::mutex> lock(resultMutex_);result_.status=std::move(status);result_.reason=std::move(reason);result_.persistence=ERROR_IO_PENDING;}
    try{bool saved=Persist(L"FINAL",details,true);settled_=true;return saved;}
    catch(...){std::lock_guard<std::mutex> lock(resultMutex_);result_.persistence=ERROR_WRITE_FAULT;settled_=true;return false;}
}
}
