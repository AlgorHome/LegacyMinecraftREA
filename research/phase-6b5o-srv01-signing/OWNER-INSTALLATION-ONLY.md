# Owner D06-SRV01 installation-only checklist — separate gate

**PREPARED ONLY. Requires explicit installation-only approval.**
No Portal, installation, activation, console-data retrieval or cleanup authorization follows
from the completed local signing. Signed artifact:
`C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5o-signing\20261017-190225-a21c9a46\NativeDiagnostics.D06-SRV01.0.2.3.0.signed.appx`
SHA256 **da28a5c22cb27b913b2bf296155c9d9bc5745e37ff3b2af88832f7661e042724**.

1. Obtain explicit approval naming this artifact/hash for ONE0.2.2.0 ->0.2.3.0 update.
   It replaces installed NativeDiagnostics RES01a, may retain old LocalState/receipts.
   Preserve accepted artifacts and evidence. If installed RES01a must remain side-by-side,
   stop for a distinct identity/build approval; do not improvise a package rename or reinstall.
2. Immediately before submission, recompute exact signed file hash:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5o-signing\20261017-190225-a21c9a46\NativeDiagnostics.D06-SRV01.0.2.3.0.signed.appx'
```

   Any mismatch means STOP, no rebuild/re-sign/replacement selection.
3. Use only owner's existing authenticated Portal. Inspect intended package only: current
   NativeDiagnostics0.2.2.0 and Not running. Stop on unexpected identity/version/running state
   or inability to confirm; no termination, permission/security/network setting change.
4. Upload only approved signed APPX. Leave dependency uploads empty if existing
   Microsoft.VCLibs.140.00 x64 UWP satisfies unchanged manifest. No UWPDesktop/fallback,
   certificate/PFX/credentials or unrelated package upload. Unknown/missing dependency: STOP.
5. Disable automatic launch-after-install. If no activation cannot be guaranteed, STOP before
   submitting. Do not alter classification or console/trust settings to force success.
6. Submit exactly once and await final result. Record final status/HRESULT/message; pending
   upload is not successful registration. No automatic retry or repair.
7. Verify registered Name AlgorHome.LegacyForge.NativeDiagnostics, Publisher
   CN=LegacyForgeDiagnostics, Version0.2.3.0, x64, classification App. Record exact
   PackageFullName only if displayed; do not infer it or classification from Application Id App.
8. Stop on signature/certificate rejection, dependency failure, registration error, ambiguous
   outcome or identity/version/classification mismatch. No trust import, framework install,
   re-sign, uninstall, storage clear or configuration change.
9. Preserve existing NativeDiagnostics LocalState/prior receipts. Do not retrieve them under
   installation-only authorization. Leave D00/production LegacyForge and frozen evidence intact.
10. STOP after registration verification, report outcome. Do not press Launch or activate the
    diagnostic. One execution, scoped original receipt retrieval and cleanup are separate gates.

Known host finding: CMS/APPX/payload integrity PASS, normal SignTool /pa chain verification
FAIL/CERT_E_UNTRUSTEDROOT0x800B0109. No trust workaround authorized. A console rejection
needs review, not implicit certificate/trust repair or a dependency upload.
Future separately approved evidence must be fresh D06-SRV01/version0.2.3.0/current-build/run,
not stale RES01a/FMT01/HW01 LocalState. No Java/JNI/Minecraft or additional native test allowed.
