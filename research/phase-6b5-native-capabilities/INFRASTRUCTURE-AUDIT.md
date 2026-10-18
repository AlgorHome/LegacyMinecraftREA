# Diagnostic infrastructure audit — accepted553c655

Static review of diagnostics/RuntimeDiagnostics, not a new runtime test. Paths
below are relative to the immutable accepted checkout
C:/Users/arinze/Desktop/ReverseLegacyCraft/phase6b1-diagnostics. Phase6B planning
documents and the final D00 report were also reviewed. D00's hardware success
validates its narrow observed path; other compiled branches are unvalidated.

| Component / source locator | Classification | Evidence, limitation and proposed treatment |
|---|---|---|
| src/app.cpp:486-496 wWinMain | reusable pattern | MTA initialization then CoreApplication::Run(DiagnosticSource). Retain apartment/API sequence; use new project/identity. Early catch returns an HRESULT without a durable startup record: add new-project startup checkpoint before case dispatch where storage is available. |
| DiagnosticSource::CreateView, DiagnosticView::Initialize/SetWindow | reusable with modification | IFrameworkViewSource/IFrameworkView with activation/window callbacks. Guard callback failures and keep receipt creation independent of renderer startup; existing Initialize/SetWindow can throw before receipt worker. |
| include/build_config.h and D00 preprocessor guards | reusable safety principle | LFD_D00_ONLY defaults1. Do not toggle off: old keyboard/pointer/gamepad paths request Java. New native-only gate and case allowlist required. |
| StartNativeControl, nativeControlStarted atomic | requires modification | one D00 worker/process prevents repeated D00 requests; not a case dispatcher or cancellation state machine. New build has one immutable case with atomic start-once and first-terminal ownership. |
| src/jni_smoke.cpp rejection stub | reusable fail-closed idea, omit TU | inspectable E_ACCESSDENIED in D00 build. Stronger native project excludes the entire TU and all JNI inputs instead of retaining dormant runtime code. |
| report.cpp Text/Number/Flag, Sha256File | reusable with review | fixed fields/numeric errors and package hashing; no exception text/path dumps. Preserve bounded buffers and resource cleanup; return explicit hashing HRESULT/Win32 error. |
| report.cpp WriteAtomic:54 onward | reusable strategy, requires failure design | 128KiB limit, tmp write, FlushFileBuffers, close, MoveFileExW WRITE_THROUGH. No power-loss guarantee; synchronous I/O can block and mutex serializes writes. Cannot promise a watchdog can persist while another write holds the lock. |
| Receipt::Checkpoint/Finish/Status/PersistenceError | requires modification | first terminal wins; write failure reports RECEIPT_ERROR to UI. No serialized independent persistence-error field; terminal flag set before persistence. New evidence must separate in-memory result from saved result; prohibit late PASS after every case deadline, not only S21. |
| report.cpp Bindings:83 onward | requires modification | hardcodes diagnostic identity, production source_baseline and five role paths; every non-D00 case hashes the S21 profile. Unsafe to reuse for D06 unmodified. New schema binds case manifest, native project source commit and new identity; production comparison stays a separate field. |
| contracts/receipt.schema.json | unsuitable unchanged | only D00/S21 enum; no NOT EXECUTED status, no new hardware observation fields. New native receipt schema/version, validator and independent evidence index needed; never change accepted v1 schema. |
| UiState/ShowNativeResult/Render | reusable UI pattern, requires decoupling | shows persistence errors instead of success; mutex shared state. DiagnosticView::Run initializes/render-presents before starting D00; wrong dependency for a graphics-creation probe. Case must start and persist independently before best-effort UI. UI device is not test device. |
| PollGamepad:443 onward; KeyDown/PointerPressed guards | unsuitable as native input implementation | compiled out of D00; surviving alternative triggers RequestJavaSmoke. Replace with original WGI enumeration/edge logic, B cancel and focus handling in new project. No reuse by disabling safety gate. |
| RequestJavaSmoke watchdog:163-187 | unsuitable unchanged | S21-only, detached workers, no native-call cancellation. D00 has NO watchdog. Reuse only first-result concept; new monotonic per-case observer and owner external deadline. No process kills. |
| CreateRenderer/Render/Resize:319-440 | reusable example, not D06 certification | D3D11 hardware request, D2D/DWrite, CoreWindow swapchain and Present. Render catches suppress HRESULT; no pixel oracle or bounded frame budget/device-loss recovery. Isolate UI graphics from case result; later render test needs original oracle and exact error capture. |
| Closed/Activated/SizeChanged callbacks | requires modification | close flag/revoke subscriptions, but no Suspending/Resuming, VisibilityChanged or focus-loss state checkpoint. New lifecycle observer/deferral handling needs explicit design and validation. |
| report.cpp ResourceSnapshot:178 onward | reusable read-only observations | MemoryManager/current-process report, unavailable/error fields; CPU/GPU false. Snapshot is not allocation limit proof, leak/CPU benchmark or universal Series X budget. Add monotonic sample stages; no cross-process inventory. |
| build.ps1, tools/verify_artifacts.py, audit_d00.py | reusable workflow, requires new project rules | exact allowlist/x64/AppContainer/provenance/preprocessed/JNI exclusions valuable. Existing tools pin old identity/version/D00 payload, reject any native loader and native input handler; do not weaken accepted audits. New native-case audit must keep JNI prohibition separate from allowlisted sentinel loading/input APIs. |

## Existing native APIs and new requirements

Accepted imports include D3D11, D2D, DWrite, bcrypt, COM/WinRT, file/time/thread
contracts and UWP CRT. Generic C++/WinRT LoadLibraryExW/GetProcAddress support is
not evidence that arbitrary native loading is permitted. Old direct import audit
is not a transitive/runtime/API-policy closure proof. UI success alone does not
authorize testing every imported API or adding capabilities.

Current ordinary view-provider model agrees with Microsoft's
[DirectX app-object guidance](https://learn.microsoft.com/en-us/windows/uwp/gaming/about-the-uwp-user-interface-and-directx).
Use the runtime's UI ASTA and initialize new worker threads as MTA; do not migrate
CoreWindow objects onto a worker. Graphics-test COM objects/context stay owned by
their designated thread. Input callback collections need locking/revocation.

## Main infrastructure changes before any new case can be trusted

New immutable case policy, new native-only compile gates, new identity/bindings,
new receipt schema, independent early receipt path and global late-result guard
are prerequisite work. Add source/static checks for these contracts and a schema
validator; no assertion of correctness follows merely from compilation. Safety
tests should target wrong-case rejection, late worker/terminal races, write failure
and missing/hash-mismatched payloads when their execution is separately approved.
During source/build authorization only, checks remain static; do not execute the
new harness on Windows to exercise them implicitly.

Lifecycle/current-process observations are based on public UWP APIs:
[app lifecycle](https://learn.microsoft.com/en-us/windows/uwp/launch-resume/app-lifecycle),
[MemoryManager](https://learn.microsoft.com/en-us/uwp/api/windows.system.memorymanager?view=winrt-28000).
API metadata is not proof every candidate behaves identically on Xbox OS10.26100.9445.
