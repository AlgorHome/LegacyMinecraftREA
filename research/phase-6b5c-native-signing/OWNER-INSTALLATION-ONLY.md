# Owner NEW-package installation-only procedure — separate approval required

This is preparation, not an installation instruction to execute before approval.
NativeDiagnostics0.2.0.0 is a NEW identity; do not update/reinstall/remove the
accepted RuntimeDiagnostics0.1.3.0 or production LegacyForge.

1. Obtain explicit approval for ONE owner-operated installation-only attempt naming
   signed SHA256d4629d1f494f73db7dcb6290bee8c5c9f28375c8630c531e58b3ee95a6f05908.
   Confirm existing authenticated Portal access without configuration/trust changes.
2. Read-only inventory: if AlgorHome.LegacyForge.NativeDiagnostics is already
   installed or running, stop for review instead of overwriting/updating/terminating.
   Do not confuse it with AlgorHome.LegacyForge.RuntimeDiagnostics.
3. Immediately before submission, hash this exact file:
   C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b5c-signing/20261017-173712-e540416b/NativeDiagnostics.D06-HW01.0.2.0.0.signed.appx.
   Any mismatch means STOP.
4. Select only that signed APPX. Leave dependency uploads empty and use the existing
   Microsoft.VCLibs.140.00 x64 UWP framework first. Do not upload the UWPDesktop
   framework, Microsoft fallback, signing certificate/PFX or other package.
5. Disable automatic launch-after-install. If the flow cannot ensure no activation,
   stop BEFORE submission. Do not change App/Game classification or other console
   settings to force acceptance; expected classification is App.
6. Submit exactly once and wait for final installation/registration result. Upload
   accepted/pending is not PASS. Record time, final status and exact HRESULT/message.
7. Verify Name AlgorHome.LegacyForge.NativeDiagnostics, Publisher
   CN=LegacyForgeDiagnostics, Version0.2.0.0, x64, App classification, application
   entry App if exposed and actual full package name. Do not fabricate a publisher
   suffix/full name from the old RuntimeDiagnostics identity.
8. STOP after registration evidence. Do not press Launch, retrieve app files,
   collect broad logs, dismiss a dialog by launching the app, or clean anything up.
   Installation authorization does not grant D06-HW01 execution or retrieval.

Stop conditions: certificate rejection, dependency resolution failure, wrong
identity/version/classification, failed/ambiguous registration, pre-existing identity
collision or UI forcing activation. Preserve error evidence; no automatic retry,
repair, trust import, re-sign, capability change, framework install or uninstall.
If dependency failure occurs, assess the exact missing Name/version/publisher first;
it is not authorization to upload the fallback unnecessarily.

The new package has separate LocalState/NativeCapabilityReceipts; accepted D00
LocalState remains untouched. A future authorized run should account for startup
I/O and dialog limitations in MESSAGE-DIALOG-REVIEW.md. Hardware status is NOT
EXECUTED. Future gates: one exact-case launch, scoped original receipt/photo
collection/validation, then separately approved cleanup. No Java/JNI/Minecraft.
