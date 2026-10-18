# Owner D06-RES01a installation-only update checklist

**PREPARED ONLY. Requires separate explicit installation approval.**
No Portal access, installation or launch has occurred as part of signing verification.

1. Obtain approval for exactly one update of NativeDiagnostics0.2.1.0 ->0.2.2.0 using:
   `C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5j-signing\20261017-183700-68e8cd8f\NativeDiagnostics.D06-RES01a.0.2.2.0.signed.appx`
   SHA256 **ead7016c94e551fac43e2b622b323354bfa4506fe507f44bf5e98f112b8f0c3f**.
2. This replaces the installed FMT01 diagnostic executable/registration; it may retain
   LocalState and previous HW01/FMT01 receipts. Preserve original evidence. If side-by-side
   installed FMT01 must remain runnable, stop for a separate identity/build proposal first.
3. Immediately before submission, locally verify the exact signed file:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5j-signing\20261017-183700-68e8cd8f\NativeDiagnostics.D06-RES01a.0.2.2.0.signed.appx'
```

   Hash mismatch means STOP. Do not re-sign, rebuild or select another package.
4. Through the owner's existing authenticated Portal, inspect only intended registration:
   NativeDiagnostics0.2.1.0 must be Not running. Stop on unexpected identity/version or
   inability to confirm; do not terminate/repair apps or change console settings.
5. Select only the approved signed APPX. Leave dependency uploads empty if existing
   Microsoft.VCLibs.140.00 x64 UWP satisfies unchanged manifest. No UWPDesktop/fallback,
   framework/certificate/PFX/credential upload. Missing/unknown dependency means stop for review.
6. Disable automatic launch-after-install. If no-launch cannot be guaranteed, STOP before
   submission. No classification/security/trust/network configuration changes to force success.
7. Submit exactly once; await final status, record HRESULT/message and exact registered
   Name AlgorHome.LegacyForge.NativeDiagnostics, Publisher CN=LegacyForgeDiagnostics,
   Version0.2.2.0, x64, App classification and PackageFullName if actually displayed.
   Do not fabricate missing UI fields or infer classification from application Id App.
8. Stop on certificate rejection, dependency failure, identity/version mismatch, registration
   error or ambiguous outcome. No retries/repair/uninstall/data clear/trust import/framework install.
9. Preserve previous NativeDiagnostics LocalState unchanged; do not retrieve or delete receipts
   under installation-only approval. Leave accepted RuntimeDiagnostics D00/production untouched.
10. STOP after registration verification and report final status/identity. Do not click Launch
    or trigger another activation. Execution, scoped receipt retrieval and cleanup remain separate.

Known host trust result: integrity PASS, normal SignTool /pa CERT_E_UNTRUSTEDROOT0x800B0109.
No trust bypass is authorized. An Xbox rejection requires investigation, not automatic trust repair.
Future approved retrieval must identify a fresh D06-RES01a run/version/build, not stale FMT01/HW01
files retained by update. No additional test, dependency change or Java/JNI/Minecraft action.
