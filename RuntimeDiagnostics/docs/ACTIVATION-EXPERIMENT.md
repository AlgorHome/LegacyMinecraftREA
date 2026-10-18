# Phase 6B.4b — activation-model-only experiment

This branch supersedes the 0.1.1.0 activation metadata only for this experiment.
Baseline source 4101f7e/review df23adb remain reachable unchanged on
research/phase6b1-runtime-diagnostics. Failed Xbox launch observation is preserved
in the external research dossier phase-6b4a-activation-investigation.

Working pinned LegacyForge source d1453434ceefe73bef5aff497194e09f39dde7e1
MC.Xbox/Package.appxmanifest uses Application Id App, EntryPoint MC.App and
LegacyForge.exe; MC.Xbox/App.cpp passes an AppSource to coreApp->Run. The diagnostic
also supplies IFrameworkViewSource directly to CoreApplication::Run, through
DiagnosticSource::CreateView. It does not use XAML or require a new WinMD class
factory for this supplied-view-source path.

MC.App is the launcher's class identifier; it is not a library to load or a
production identity that the diagnostic must share. Its ordinary UWP activation
pattern is appropriate to compare. This experiment uses the diagnostic-specific
identifier LegacyForgeDiagnostics.App instead, retaining Application Id App and
RuntimeDiagnostics.exe. The source factory is supplied by native startup, not
looked up as a C++ type with that spelling by this code. Xbox acceptance remains
experimental; static packaging does not validate activation-class handling.

Microsoft's Application schema separates the partial-trust packagedClassicApp
marker from ordinary windowsApp activation:
https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-application
CoreApplication::Run accepts an IFrameworkViewSource instance:
https://learn.microsoft.com/en-us/uwp/api/windows.applicationmodel.core.coreapplication.run

Changes:

- EntryPoint Windows.PartialTrustApplication -> LegacyForgeDiagnostics.App.
- Version 0.1.1.0 -> 0.1.2.0, deliberately prepared for a future reviewed update.
- Static verifier requires the new exact Application Id/entry point/version.

No C++/header/build configuration change: STA initialization, renderer, native
control, receipts/schema, D00-only compile-time lock and JNI rejection remain
unchanged. No capabilities, dependencies, signing inputs or payload types added.
The initial STA remains a known independent compatibility risk. No correction of
it is included, so this experiment isolates activation metadata from COM changes.

Version is not needed merely to compile; it is incremented to distinguish evidence
and permit a future update of the same diagnostic registration without uninstalling.
Name, publisher, architecture and Application Id are unchanged: no side-by-side
registration is created. PackageFullName will change with version; package family
and LocalState remain shared with the diagnostic's earlier version. Existing data
must not be deleted and must not be mistaken for this experiment's new receipts.
No fresh-data isolation or rollback is implied. This does not touch production.

Preserve the currently installed 0.1.1.0 registration for read-only troubleshooting
now. Only after evidence preservation and separate signing/deployment approval,
use version 0.1.2.0 for this experiment. Snapshot receipt names/times if separately
authorized and bind any later run to package_version, run/process UUIDs, observed
time and exact approved payload hashes. There is no authorized second launch now.

Build: pwsh -NoProfile -File diagnostics/RuntimeDiagnostics/build.ps1
-Configuration D00Only -Package. Trusted compiler/static tools only; never invoke
the resulting EXE. New generated inventories bind this commit/build and hashes;
timestamps, native profile ordering and PE linker metadata may differ between
rebuilds. The evidence dossier must enumerate actual package byte differences.

Stop after unsigned packaging/static review. No signing, trust changes, install,
console access, activation or Java/Minecraft execution is authorized by this step.
