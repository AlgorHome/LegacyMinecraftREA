# D06-FMT01 owner installation-only update checklist

**PREPARED ONLY. Stop until explicit installation-only approval.**
This signing authorization permits no Portal access, installation or launch.

1. Resolve preservation choice: installing NativeDiagnostics0.2.1.0 replaces the accepted
   NativeDiagnostics0.2.0.0 registration; LocalState may retain old HW01 receipts.
   If side-by-side installed HW01 is required, stop for a separately approved identity/build.
   Do not uninstall/downgrade/clear storage or modify accepted RuntimeDiagnostics0.1.3.0.
2. Obtain approval for ONE owner-operated update using only:
   `C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5f-signing\20261017-180640-31684a3e\NativeDiagnostics.D06-FMT01.0.2.1.0.signed.appx`
   SHA256 **ae19e5ff93438bcf8a3c9e0d42ad0323908ee83d95231cba9dcd9a319fd5d8ef**.
3. Immediately before submission, run on the PC:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5f-signing\20261017-180640-31684a3e\NativeDiagnostics.D06-FMT01.0.2.1.0.signed.appx'
```

   Any mismatch means STOP. This command only reads bytes, not package execution.
4. Through the owner's existing authenticated Portal, read exact current NativeDiagnostics
   identity/version and confirm Not running. Expected starting version0.2.0.0; stop on
   unexpected registration. Do not terminate/reconfigure applications to force this check.
5. Select only the approved signed APPX. Leave dependencies empty using the installed
   Microsoft.VCLibs.140.00 x64 UWP framework if it satisfies the unchanged manifest.
   Do not upload UWPDesktop, fallback framework, certificates/PFX or unrelated packages.
   If dependency sufficiency is unknown, stop for review; no automatic upload/install.
6. Disable any automatic launch-after-install option. If this cannot be ensured, STOP before
   submitting. Do not change classification, certificates/trust, security or console settings.
7. Submit exactly ONE update and await final registration status. Record status, HRESULT,
   time and exact registered identity/full name if shown. Pending upload is not success.
8. Expected updated Name AlgorHome.LegacyForge.NativeDiagnostics; Publisher
   CN=LegacyForgeDiagnostics; Version0.2.1.0; x64; classification App. Application Id App
   and entry point LegacyForgeNativeDiagnostics.App where exposed. Do not guess suffixes
   or invent fields the UI does not expose.
9. Stop on certificate rejection, missing dependency, registration failure, identity/version/
   classification mismatch or ambiguous outcome. No retry, repair, fallback framework,
   certificate import, re-sign, uninstall, storage clearance or console configuration change.
10. STOP after registration evidence. No Launch button, diagnostic execution, receipt
    retrieval or cleanup. Preserve existing LocalState untouched. Report final result.

Known host trust finding: CMS/package integrity PASS; normal Windows SignTool /pa fails
CERT_E_UNTRUSTEDROOT0x800B0109. No trust change is included or implied. Installation failure
requires review; do not use this document to bypass verification or change console trust.

Future independently approved run: one D06-FMT01 activation. Future separately approved
retrieval: only NativeDiagnostics LocalState/NativeCapabilityReceipts, fresh
D06-FMT01-<run UUID>.json bound to0.2.1.0/build/source and independently pinned six hashes.
Older HW01 files retained by update are not FMT01 results. Cleanup remains a final separate gate.
No Java/JNI/Minecraft or production LegacyForge action is included in any step above.
