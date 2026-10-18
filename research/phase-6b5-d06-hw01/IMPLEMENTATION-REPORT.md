# Phase 6B.5b — isolated D06-HW01 implementation

2026-10-17, America/Chicago. Source/build/static review only. No diagnostic,
Java/JNI or Minecraft code was executed. No signing, installation, console access,
certificate/dependency operation or production modification occurred.

Branch: **research/phase6b5b-d06-hw01**, derived from accepted553c655.
Final source: **a3f72874241914f6048d4ca9ec4fc0edc978625d**.
All changed Git paths are under diagnostics/NativeCapabilities/. Accepted D00
source/branches, signed/unsigned packages, receipt, photograph and acceptance
report are preserved; additional static review compares their frozen hashes.

## Build artifact

Unsigned APPX:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/phase6b1-diagnostics/diagnostics/NativeCapabilities/out/20261017-173106-d79a3eae/NativeCapabilities.unsigned.appx`

SHA256: **79722c961dd677a2c89610599aec2e9537727dead6d66e2e3e8ff522da8b2501**.
Compilation/packaging/static verdict: **PASS_STATIC_ONLY; all recorded tool exit codes 0**.
BUILD-EVIDENCE.json binds the final clean source commit, generated compile-time
identity header, build ID, all input/tool/output hashes and command exit codes.
STATIC-ARTIFACT-EVIDENCE.json lists every member and direct import/export symbol.
ADDITIONAL-STATIC-REVIEW.json records baseline and reviewed CRT export comparisons.
RECEIPT-SCHEMA.json is the exact packaged original schema, not a hardware receipt.

Reproduce with existing Windows x64 MSVC14.44.35207 UWP/store libraries,
Windows SDK10.0.26100.0 (C++/WinRT/MakeAppx), PowerShell7 and Python:

```powershell
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Only a clean committed tree builds; outputs use new ignored directories. No
runtime, package signing or execution option exists. The build compiles,
preprocesses and statically inspects app.cpp/report.cpp/probe.cpp only. No accepted
D00 output is reused/overwritten. Earlier local failed/intermediate builds remain
separate and are not the review artifact. Initial compile needed an explicit
C++/WinRT collection-definition include; subsequent static review added the
checkpoint/timeout persistence race guard and exact S_OK oracle before final build.

## Package and implemented experiment

| Field | Value |
|---|---|
| Name | AlgorHome.LegacyForge.NativeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Version/architecture | 0.2.0.0 / x64 |
| Application Id / EntryPoint | App / LegacyForgeNativeDiagnostics.App |
| Classification | App required in future owner installation; not a manifest field proving console state |
| Capabilities | zero |
| Target | Windows.Universal min10.0.17763.0 / max tested10.0.26100.0 |
| Framework | Microsoft.VCLibs.140.00 >=14.0.0.0, unchanged Microsoft publisher |

MTA wWinMain -> CoreApplication::Run -> supplied IFrameworkViewSource. First valid
Launch activation, empty argument or exact D06-HW01, starts once; other arguments/
activation kinds reject before worker/device call. One case is linked, no queue.

Worker requests one D3D11CreateDevice(default adapter, HARDWARE, no Software module,
BGRA flag32, allowed11_0 only). Records returned HRESULT, pointers and feature
level. Obtains available IDXGIDevice/IDXGIAdapter1 Flags; retains no serial/LUID/
description or user/device identity. Requested driver type and observed SOFTWARE
flag are distinct fields. S_OK/nonnull outputs/11_0/clear SOFTWARE flag/resource
policy are required for PASS. There is no WARP/reference fallback or hidden retry.
Unsupported/policy APIs report BLOCKED; other oracle violations FAILED.

All scoped test COM references release on the owning MTA worker before terminal
success. No app-owned swapchain, render target, presentation loop, test textures,
buffers, shader or graphics stress workload exists. This is not all D06 PASS.

## Deliberate UI choice

The implementation authorization explicitly forbids swapchains/presentation,
overriding the planning dossier's optional inherited-renderer suggestion. Therefore
Windows.UI.Popups.MessageDialog supplies the status UI via the CoreWindow dispatcher.
Windows, not this project, renders the dialog. It shows case/title, status/reason,
hardware request, HRESULT, feature level, run ID and persistence result; dismissal
does not rerun or exit/kill another application. UI failure has a best-effort title
notice and does not change the hardware-device receipt. No D2D/DWrite/DXGI factory
renderer dependency is linked. MessageDialog and owner-visible text behavior on
this exact Xbox build are NOT EXECUTED, not certified by compilation.

[Microsoft MessageDialog non-XAML guidance](https://learn.microsoft.com/en-us/uwp/api/windows.ui.popups.messagedialog?view=winrt-26100),
[UWP CoreApplication/view model](https://learn.microsoft.com/en-us/windows/uwp/gaming/about-the-uwp-user-interface-and-directx),
[D3D11CreateDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-d3d11createdevice).

## Evidence, time and resource bounds

New schema/directory NativeCapabilityReceipts, exact new package identity/version,
random process/run IDs, actual compiled source/build identity, production comparison
and frozen D00 reference separately labeled, six payload-role hashes. Final signed
archive hash is bound later in an external index, never self-embedded circularly.

STARTED must persist before scheduling work; BEFORE_CREATE_DEVICE must persist
before entering D3D. 10s monotonic observer, atomic first terminal, late PASS denied;
30s external owner observation is a later separately approved step. Observer cannot
cancel a GPU/file call. Bounded100ms I/O-lock acquisition prevents observer waiting
forever for a worker checkpoint lock, but an acquired synchronous storage operation
can still block. Preserve checkpoint/tmp and report INCONCLUSIVE when no final
receipt can be obtained. No timeout process kill or automatic restart.

Require observed256MiB headroom before call; post-release observed growth over64MiB
fails policy. No explicit test GPU resources; receipt <=128KiB. API-created driver
allocations cannot be strictly capped; observed guard is not an OOM stress test.
Memory API unavailable is BLOCKED. UI status distinguishes decision from successful
write; serialized persistence result VERIFY_BY_RETRIEVAL is deliberately not a
prediction of a future successful flush. Actual downloaded original plus schema/
oracle/payload checks establishes persistence. First result and storage error remain
separate; an older checkpoint cannot clear a timeout's terminal persistence failure.

## Differences from accepted D00 and remaining gates

New project/name/LocalState/version/schema/case. Reuses reviewed hash/write strategy
and MTA view-provider pattern, not old Java branches or renderer. New immutable
case/native-only macros and exact package allowlist replace D00/S21-specific
bindings. No production, authentication, entitlement or third-party launcher code.

Remaining unknowns: Xbox activation/dialog/adapter interface behavior, system API-
set/transitive loader resolution, driver/COM cleanup timing, worker/storage race
behavior and actual headroom. Static audit is not a dynamic failure-injection test.
All hardware outcomes remain NOT EXECUTED. No extra capability is shown necessary;
no capability expansion is included. Stop at this unsigned review artifact.

Next gate is exact-hash fresh-copy signing approval. Owner installation of this
NEW identity, one launch, retrieval and cleanup each require separate approval;
see HARDWARE-ACCEPTANCE-PLAN.md. Accepted RuntimeDiagnostics is never updated.

