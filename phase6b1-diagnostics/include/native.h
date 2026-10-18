// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "build_config.h"
#include "build_identity.h"
#define NOMINMAX
#include <windows.h>
#include <atomic>
#include <memory>
#include <mutex>
#include <string>
#include <winrt/Windows.Data.Json.h>
#include <winrt/Windows.Foundation.Collections.h>

namespace lfn {
using Json = winrt::Windows::Data::Json::JsonObject;
inline constexpr wchar_t Case[] = L"D06-SRV03";
inline constexpr wchar_t Identity[] = L"AlgorHome.LegacyForge.NativeDiagnostics";
inline constexpr uint64_t DeadlineMs = 10000;
void Text(Json const&, wchar_t const*, std::wstring const&);
void Number(Json const&, wchar_t const*, double);
void Flag(Json const&, wchar_t const*, bool);
std::wstring Hex(HRESULT);
std::wstring HashFile(std::wstring const&, DWORD*);
Json Memory();
struct Result {
    std::wstring status = L"RUNNING", reason = L"STARTED";
    std::wstring creation = L"UNAVAILABLE (no returned HRESULT)", feature = L"UNAVAILABLE";
    DWORD persistence = ERROR_IO_PENDING;
};
class Receipt {
public:
    Receipt();
    bool Checkpoint(wchar_t const*, Json const& = Json{});
    bool Finish(std::wstring, std::wstring, Json const& = Json{});
    void ArmDeadline();
    bool Expired() const;
    bool Terminal() const { return terminal_.load(); }
    bool Settled() const { return settled_.load(); }
    Result Snapshot() const;
    void DeviceObservation(HRESULT, unsigned);
    std::wstring RunId() const { return run_; }
private:
    bool Persist(wchar_t const*, Json const&, bool);
    std::wstring binding_, run_, path_, process_;
    mutable std::mutex resultMutex_;
    std::timed_mutex ioMutex_;
    Result result_;
    std::atomic<bool> terminal_{false};
    std::atomic<bool> settled_{false};
    std::atomic<uint64_t> deadline_{0};
    uint64_t started_ = GetTickCount64(), sequence_ = 0;
    std::wstring lastCheckpoint_;
};
struct ProbeState {
    std::atomic<bool> started{false}, closed{false}, notified{false};
    std::shared_ptr<Receipt> receipt;
};
void Probe(std::shared_ptr<Receipt> const&);
}
