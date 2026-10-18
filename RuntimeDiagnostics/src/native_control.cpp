// SPDX-License-Identifier: Apache-2.0
#include "diagnostics.h"
#include <winrt/Windows.ApplicationModel.h>

namespace lfd {
void RunNativeControl(std::shared_ptr<Receipt> const& receipt) {
    Json started;
    Flag(started, L"jvm_loaded", false);
    Flag(started, L"ui_render_is_d06_test", false);
    receipt->Checkpoint(L"D00_ACTIVATION_STARTED", started);

    Json details;
    auto package = winrt::Windows::ApplicationModel::Package::Current();
    bool identityMatches = package.Id().Name() == kDiagnosticIdentity;
    Flag(details, L"expected_package_identity", identityMatches);
    Text(details, L"source_baseline", kBaseline);
    Text(details, L"scope", L"D00_ACTIVATION_IDENTITIES_RESOURCES_ONLY");
    Flag(details, L"jvm_loaded", false);
    Flag(details, L"graphics_capability_tested", false);
    Flag(details, L"input_capability_tested", false);
    Flag(details, L"audio_capability_tested", false);
    Flag(details, L"native_dependency_closure_tested", false);
    details.Insert(L"resources", ResourceSnapshot());

    Json roleHashes;
    bool complete = true;
    const struct { wchar_t const* role; wchar_t const* relative; } roles[] = {
        {L"diagnostic_exe_sha256", L"RuntimeDiagnostics.exe"},
        {L"package_manifest_sha256", L"AppxManifest.xml"},
        {L"input_manifest_sha256", L"diagnostic-inputs.json"},
        {L"runtime_inventory_sha256", L"runtime-inventory.json"},
        {L"profile_sha256", L"profiles\\native-control.json"}
    };
    auto root = PackageRoot();
    for (auto const& role : roles) {
        DWORD error = 0;
        auto hash = Sha256File(root + L"\\" + role.relative, &error);
        Text(roleHashes, role.role, hash);
        if (error || hash.size() != 64) complete = false;
        if (error) Number(roleHashes, (std::wstring(role.role) + L"_error").c_str(), error);
    }
    details.Insert(L"role_hashes", roleHashes);
    Flag(details, L"required_role_hashes_complete", complete);
    if (!identityMatches) {
        receipt->Finish(L"FAILED", L"PACKAGE_IDENTITY_MISMATCH", details);
    } else if (!complete) {
        receipt->Finish(L"BLOCKED", L"REQUIRED_PACKAGE_EVIDENCE_MISSING", details);
    } else {
        // Finish returns success only if this first terminal receipt was written.
        // The caller must still inspect PersistenceError before enabling JNI.
        receipt->Finish(L"PASS", L"D00_ACTIVATED_HASHES_RECORDED", details);
    }
}
}
