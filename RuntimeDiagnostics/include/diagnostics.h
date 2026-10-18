#pragma once
#include "build_config.h"
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <atomic>
#include <functional>
#include <memory>
#include <string>
#include <vector>
#include <winrt/Windows.Data.Json.h>
#include <winrt/Windows.Foundation.Collections.h>

namespace lfd {
inline constexpr wchar_t kBaseline[] = L"d1453434ceefe73bef5aff497194e09f39dde7e1";
inline constexpr wchar_t kDiagnosticIdentity[] = L"AlgorHome.LegacyForge.RuntimeDiagnostics";
using Json = winrt::Windows::Data::Json::JsonObject;
using JsonArray = winrt::Windows::Data::Json::JsonArray;

// All free-form values must be fixed enums/role names. Never pass exception text,
// environment dumps, Java properties, command lines, or absolute paths here.
void Text(Json const& object, wchar_t const* name, std::wstring const& value);
void Number(Json const& object, wchar_t const* name, double value);
void Flag(Json const& object, wchar_t const* name, bool value);
std::wstring Sha256File(std::wstring const& path, DWORD* error = nullptr);
std::wstring PackageRoot();
std::wstring LocalRoot();
Json ResourceSnapshot();

class Receipt {
public:
    explicit Receipt(std::wstring caseId);
    // Persist before entering a potentially blocking native/JNI call.
    void Checkpoint(std::wstring const& stage, Json const& details = Json{});
    // First terminal result wins. A timed-out worker cannot overwrite it.
    bool Finish(std::wstring const& status, std::wstring const& reason,
                Json const& details = Json{});
    bool Terminal() const;
    std::wstring RunId() const;
    DWORD PersistenceError() const;
    std::wstring Status() const;
private:
    struct State;
    std::shared_ptr<State> state_;
};

// Called only on a dedicated initialized worker; one VM creation attempt maximum
// for the entire app process. All paths are fixed package roles, never UI input.
void RunJava21Smoke(std::shared_ptr<Receipt> const& receipt);
// Pure package/activation/resource observation. It never creates or loads a JVM.
void RunNativeControl(std::shared_ptr<Receipt> const& receipt);
}
