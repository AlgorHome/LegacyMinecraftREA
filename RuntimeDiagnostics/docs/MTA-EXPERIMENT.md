# Phase 6B.4e — isolated entry-thread MTA experiment

Parent c70a17ecd4022452a963697196f362c8f286ed57 remains on
research/phase6b4b-uwp-activation. Earlier diagnostic branches, builds and signed
copies are preserved. This experiment supersedes only that parent's STA startup
and package version, not its corrected LegacyForgeDiagnostics.App activation.

Only runtime source edit: wWinMain in src/app.cpp initializes
winrt::apartment_type::multi_threaded instead of single_threaded. Existing
CoreApplication::Run(winrt::make<DiagnosticSource>()) and all worker initialization
remain unchanged. The SDK helper still calls CoInitializeEx; it is not replaced
with RoInitialize. No graphics, native-control, receipt/schema, dependency,
capability, D00 lock or Java/JNI code is changed.

The MTA initial thread matches Microsoft's native CoreApplication startup model
and the working launcher's multithreaded initialization. CoreApplication creates
its own UI ASTA; this edit does not convert DiagnosticView or its renderer to run
on a manually created MTA UI thread.

Reference: https://learn.microsoft.com/en-us/windows/uwp/gaming/about-the-uwp-user-interface-and-directx

Manifest version alone advances 0.1.2.0 -> 0.1.3.0 for distinguishable future
update evidence; the static verifier pins it. Name, publisher, architecture and
Application Id remain unchanged. This is not side-by-side installation; a later
approved update may retain diagnostic LocalState and old receipts. Full package
name changes with version, while family remains diagnostic-only. Do not update,
reset, uninstall or collect console receipts as part of this source/build step.

Build from the checkout with the existing toolchain:

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration D00Only -Package
```

No JDK or runtime input is needed/allowed for D00Only. The output is unsigned.
Compiler/static/preprocessor/packaging tools run; the produced program never does.
Exact comparison and preservation hashes are recorded in the external research
dossier docs/research/phase-6b4e-mta-experiment under ReverseLegacyCraft.

This isolates one startup property, not all possible causes of 0x8027025B. Existing
early exception reporting gaps, graphics/device failure and native dependency/API
compatibility remain untested. Version attribution of the split-second apparent
crash is owner-reported; triggering action and exact attempt count remain unknown.
Do not infer activation success, receipt persistence or causality from compilation.
Signing, installation/update, receipt collection and launch require later approval.
