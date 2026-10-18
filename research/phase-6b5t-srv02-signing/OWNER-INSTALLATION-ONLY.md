# Owner checklist - pending separate installation authorization

Do not perform these steps under Phase 6B.5t. Installation, launch, receipt retrieval, final hardware acceptance and cleanup each require separate explicit approval.

1. After installation-only approval, use the owner's existing authenticated Xbox Device Portal. Verify current NativeDiagnostics is not running; stop on unexpected existing identity. Do not launch it to check.
2. Immediately before upload, hash exactly this signed file in PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5t-signing\20261017-193135-107a9142\NativeDiagnostics.D06-SRV02.0.2.4.0.signed.appx'
```

Expected: `a77e31a5922bca35a09084dbe885b5d13ed1207571f66458644d5ac7ee8738d5`. Stop on mismatch.

3. Select only that signed APPX. Expect Name AlgorHome.LegacyForge.NativeDiagnostics, Publisher CN=LegacyForgeDiagnostics, Version 0.2.4.0, Architecture x64, Application Id App; verify console classification App separately. Updating 0.2.3.0 replaces that registered diagnostic version and may retain stale LocalState. Preserve all existing receipts; do not clear, uninstall or overwrite evidence.
4. Leave dependencies empty if the existing Microsoft.VCLibs.140.00 resolves the manifest. Do not upload a fallback or UWPDesktop framework. Missing dependency requires stopping and separate review.
5. Disable automatic launch before submission. If it cannot be guaranteed, stop without submitting.
6. Submit exactly once; wait for final registration result. Record status, HRESULT if any, exact Name/Publisher/Version/Architecture/Application Id and PackageFullName if exposed. Do not retrieve unrelated inventory.
7. Stop on certificate rejection, missing dependency, registration failure or unexpected identity/version. No retry, repair, trust changes or framework installation.
8. Stop after registration verification. No launch, receipt retrieval, cleanup or production LegacyForge interaction. Local Windows untrusted-root status is retained; do not alter trust in response.
