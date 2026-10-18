# Phase 6B.4b — diagnostic UWP activation experiment: static review

2026-10-17. BUILD/STATIC REVIEW PASS. NO SIGNING, INSTALLATION OR EXECUTION.

Branch: research/phase6b4b-uwp-activation.
Source commit: c70a17ecd4022452a963697196f362c8f286ed57.
Checkout: C:/Users/arinze/Desktop/ReverseLegacyCraft/phase6b1-diagnostics.
Baseline branch research/phase6b1-runtime-diagnostics remains at
df23adb6dbe948079510cf12eb64d5fd23542256; original built source remains
4101f7ee07d1c74911ffbf5cd2a44aff608c401d.

## Artifact and reproduction

Unsigned APPX:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/out/20261017-140332-19d39263/RuntimeDiagnostics.unsigned.appx`

SHA256: **5fd3462dcce83faea10617b19d18000f437e19d70d04b0e2a5bc98411b9a44fd**.

From the checkout, using the existing Windows x64 MSVC/UWP store toolchain,
Windows SDK 10.0.26100.0, PowerShell 7 and Python:

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration D00Only -Package
```

All build commands returned exit 0. Compiler/linker/preprocessor/import inspection,
MakeAppx packaging validation, inventory/payload validation and compile-time D00
audit completed. The build script never invokes the produced executable. No Java
runtime was supplied or needed; its generic inventory field BLOCKED_RUNTIME_NOT_SUPPLIED
does not mean the D00 build failed. Runtime/Java execution remains untested/disabled.
Build receipt, tool hashes, source hashes and command exit codes are recorded in
build-receipt.json; static-verification.json and d00-safety-audit.json are copied
unchanged from this build. Outputs are ignored, with no binaries added to Git.

## Activation-model rationale

Pinned working LegacyForge d1453434ceefe73bef5aff497194e09f39dde7e1 uses MC.App in
the manifest and supplies AppSource to coreApp->Run from native wWinMain. The
diagnostic supplies DiagnosticSource to CoreApplication::Run. MC.App is suitable
as a reference for that ordinary UWP activation pattern, but is not a required
shared identifier or an appropriate diagnostic namespace to copy verbatim.

Use **LegacyForgeDiagnostics.App** as the diagnostic-specific ordinary UWP entry
identifier. No extra WinMD/factory is added: this native path supplies its
IFrameworkViewSource instance directly. This is supported by comparison and the
documented Run signature; it does not prove Xbox resolves/accepts the new metadata.
The source's DiagnosticSource type need not be renamed solely to match the
metadata string in this supplied-view-provider design.

Microsoft [Application schema](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-application)
distinguishes the partial-trust packagedClassicApp marker from windowsApp
activation; [CoreApplication.Run](https://learn.microsoft.com/en-us/uwp/api/windows.applicationmodel.core.coreapplication.run)
accepts the supplied view factory. Case handling of the old upper-case marker was
not tested; no claim is made that its capitalization alone caused the failure.

## Exact changes and checks

| Item | Result/evidence |
|---|---|
| Manifest activation | Windows.PartialTrustApplication -> LegacyForgeDiagnostics.App |
| Package version | 0.1.1.0 -> 0.1.2.0, deliberate future-update/evidence increment |
| Other manifest attributes/elements | Identical after normalizing only those two values, asserted by comparison helper |
| Name/publisher/architecture | AlgorHome.LegacyForge.RuntimeDiagnostics / CN=LegacyForgeDiagnostics / x64 unchanged |
| Application Id / EXE | App / RuntimeDiagnostics.exe unchanged |
| Capabilities | zero, enforced by verifier and static audit |
| Device family/dependency | Windows.Universal min10.0.17763.0 max tested10.0.26100.0; Microsoft.VCLibs.140.00 >=14.0.0.0 unchanged |
| COM initialization | STA remains byte-identical source at src/app.cpp:488 |
| Native source/headers/build script/receipt schema | unchanged relative to df23adb |
| LFD_D00_ONLY | 1 in every TU, preprocessed code and rejection stub audited PASS |
| S21 routes | handlers/UI/worker/watchdog/JNI implementation absent; fail-closed direct-call stub retained |
| Third-party/runtime/game/auth payload | none added; exact D00 allowlist PASS |
| PE code/imports | EXE identical except COFF and debug-directory timestamps; .text identical |
| PE protections | original GUI/x64/AppContainer configuration retained by unchanged build and byte comparison |
| Static verifier change | pins new exact entry point, Application Id and version; no runtime effect |
| Git change scope | diagnostic manifest, static verifier, experiment documentation only |

EXPERIMENT-COMPARISON.json enumerates every changed package member. Only these
five members differ: AppxManifest.xml, RuntimeDiagnostics.exe, diagnostic-inputs.json,
profiles/native-control.json, AppxBlockMap.xml. Native profile JSON is semantically
equal (key order changed). EXE is the same 119296 bytes; four changed bytes lie
within the two parsed timestamp fields at file offsets 248 and 85604. There is no
native code, import table or behavior change masked by this review. Generated
diagnostic-inputs bind the new source commit/build/input hashes; APPX block map
changes follow those payload bytes. Other original members are byte-identical.
No signature member exists in this new APPX.

## Preservation and evidence policy

BASELINE-PRESERVATION.json records freshly checked originals:

- unsigned ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558;
- signed 51e5c74462e79a296335beab4830f479e861e7132e0f660c680f6974d3b27530.

Original files were not overwritten. Public certificate metadata is copied as
BASELINE-CERTIFICATE-PUBLIC-METADATA.json, with file hash recorded, not reissued
or privately accessed. Signer thumbprint remains
D6245FB640D520EDED8F8A987B364BCADE01D01D. Prior CMS/content verification PASS and
Windows default trust CERT_E_UNTRUSTEDROOT remain historical evidence; neither
implies a signature on this unsigned experiment. No certificate-store operation
or dependency operation was performed.

BASELINE-XBOX-OBSERVATIONS.json preserves the one failed launch, code 0x87E10006,
registration PASS, UI not observed and receipt state UNKNOWN. Original screenshot
remains unavailable; it is not invented or represented as preserved image evidence.

## Existing registration and compatibility risks

Keep installed 0.1.1.0 unchanged for read-only failure/receipt troubleshooting now.
Only after separately approved signing and replacement should future experiment
evidence use **0.1.2.0**. Same name/publisher/architecture means an update, not
side-by-side isolation. Full package name changes; diagnostic family/LocalState
can persist. Preserve old receipts; bind later evidence to exact version, run and
process UUIDs, approved hashes and observation times. Do not label historical
receipts as experiment results. No rollback/update/uninstall is approved here.

STA remains an independent potential startup defect. A failure after a future
approved launch would not rule out the activation correction: the untouched STA
or unresolved native loader/API compatibility may still fail later. Static tools
cannot establish Xbox activation, hardware rendering, receipt durability or the
root cause of 0x87E10006. The diagnostic identifier's Xbox handling is untested.

STOP: new unsigned artifact is ready for review only. No signing, deployment,
console access, launch, certificate changes, dependency changes or production
LegacyForge modifications occurred. Further actions require separate approval.
