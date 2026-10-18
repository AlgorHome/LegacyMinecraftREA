# First proposal — D06-HW01: one classified hardware D3D11 device

**DESIGN ONLY / NOT EXECUTED.** This is not implementation approval or complete
D06 graphics certification. Objective: can the independent native package create
one feature-level11_0 hardware D3D11 device and record its classification durably?
No textures, test buffers, draw/readback, test swapchain, shaders, controller input,
audio, lifecycle sweep, third-party fixture or Java/JNI is needed for this question.

## Why first

Accepted D00 already requests a hardware device as part of its UI but does not
bind chosen feature level/adapter classification as a D06 oracle. It also starts
its receipt worker after renderer initialization. A new standalone case must
record the tested operation explicitly and survive an unavailable UI. Do not
retroactively label the accepted D00 photo a complete graphics test.

## Proposed package/source change

New project diagnostics/NativeCapabilities, new package Name
AlgorHome.LegacyForge.NativeDiagnostics, Version0.2.0.0, x64, App classification,
Publisher CN=LegacyForgeDiagnostics, Application Id App, proposed EntryPoint
LegacyForgeNativeDiagnostics.App. Same owner certificate may be nominated later;
no key/certificate operation is performed or required for this design.

Use a new research branch based on553c655. Never modify/rebuild the accepted
RuntimeDiagnostics project in place. Smallest case implementation is an original
RunHardwareDeviceProbe worker plus its fixed policy/receipt oracle; required
supporting changes are new identity/bindings, native-only build gates, case receipt
schema, static audit and early/start-once dispatch. These are real prerequisite
plumbing, not a one-line change to the accepted harness. Only this case is linked.

Retain MTA entry -> CoreApplication::Run -> runtime-created UI ASTA. Initialize
the case worker as MTA. Start case receipt/checkpoint before CreateRenderer is
ever attempted. Worker owns all test COM objects and releases them on that same
worker. UI failure cannot turn a saved case result into a graphics failure or
cause a second attempt.

The test path does not call CreateRenderer/Present. A best-effort inherited status
UI may be retained only as a separately labeled channel, after the test device is
released and final receipt persisted; no concurrent test/UI swapchain ownership.
That UI's own device creation is explicitly not another test attempt, is accounted
as support activity, and cannot rescue a failed/blocked test. If minimizing all
graphics activity is necessary, disable the status renderer and retrieve only
the receipt; report UI observation unavailable, not a test PASS surrogate. The
implementation review must choose and freeze one of these UI policies. Recommended
initial policy: receipt-first, optional existing status renderer after completion.

## Fixed operation sequence

1. Reject unknown or second case dispatch. Read immutable D06-HW01 policy from
   hashed package inputs; verify package/source roles. Record STARTED and
   BEFORE_CREATE_DEVICE with policy deadline and memory snapshot. Receipt failure
   before the call -> BLOCKED/RECEIPT_PREREQUISITE, do not call the driver.
2. Establish 10-second monotonic deadline immediately before the tested call;
   start an independent outcome observer. No native thread/process termination.
3. Call D3D11CreateDevice once with default adapter nullptr, requested
   D3D_DRIVER_TYPE_HARDWARE, Software nullptr, D3D11_CREATE_DEVICE_BGRA_SUPPORT,
   one allowed level D3D_FEATURE_LEVEL_11_0, SDKVersion D3D11_SDK_VERSION and output
   device/context/feature pointers. No DEBUG layer, WARP, alternate level list,
   hidden retry or optional debug-runtime dependency.
4. Record HRESULT verbatim (signed numeric and hexadecimal), nonnull outputs and
   selected level. From device QI IDXGIDevice -> GetAdapter -> QI IDXGIAdapter1 ->
   GetDesc1. Retain only enum/ordinal and numeric Flags; do not serialize adapter
   LUID, hardware serial, description, user/device/network identifiers. Compare
   DXGI_ADAPTER_FLAG_SOFTWARE. Query GetDeviceRemovedReason if a real device error
   occurs, not as a claim of tested recovery.
5. Release test context/device/adapter references; capture after-resource snapshot.
   Coordinator attempts one terminal receipt. Observer may deny a late PASS even
   if the worker returns after deadline. Never overwrite a terminal timeout with
   success. Receipt persistence must succeed before UI claims saved PASS.

API requirements: d3d11.h/dxgi.h/dxgi1_2.h, Windows SDK10.0.26100.0, D3D11.lib,
DXGI.lib, WindowsApp/RuntimeObject and existing UWP CRT/static support as reviewed.
Use the existing MSVC x64 UWP toolchain; no new compiler/debug/runtime downloads.
The returned device methods add mostly COM vtable surface; the principal creation
API already exists in D00's imports. Exact new import closure still needs review.

Microsoft [D3D11CreateDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-d3d11createdevice)
documents parameter constraints and returned selected feature level. Default
adapter+HARDWARE is intentional: nonnull adapter+HARDWARE is invalid; a future
enumerated-adapter case must use the appropriate UNKNOWN driver type instead.
[GetDesc1](https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiadapter1-getdesc1)
provides descriptor metadata. Classify by Flags, not marketing strings.
[UWP Direct3D initialization](https://learn.microsoft.com/en-us/windows/uwp/gaming/simple-port-from-direct3d-9-to-11-1-part-1--initializing-direct3d)
supports the public UWP pattern; it is not a guarantee of this console's result.

## Budgets and explicit result contract

Fixed receipt <=128KiB, ordinary worker stack, one test device/context, no explicit
test GPU resources. Require readable usage/limit and >=256MiB observed headroom
before driver creation; otherwise BLOCKED/RESOURCE_PREREQUISITE. No total GPU/
driver-memory cap is enforceable with this API. Sample app memory before/after;
project tolerance is <=64MiB observed growth for the tested stage. If exceeded,
record FAILED/RESOURCE_POLICY_EXCEEDED and do not start optional UI. This is an
observation threshold, not a guaranteed allocation cap or claim of leak-free teardown.
Do not attempt OOM, classify as Game, request expandedResources or change limits.

| Outcome | Exact meaning for this case |
|---|---|
| NOT EXECUTED | current design; or no separately approved activation/attempt |
| BLOCKED | missing receipt precondition/headroom/API/adapter classification contract; HRESULT retained; no hardware certification inferred |
| FAILED | required creation returned a non-support-related error, outputs/level violate oracle, SOFTWARE flag set under hardware request, or resource policy exceeded |
| INCONCLUSIVE | deadline, cancelled/interrupted process, missing terminal file, uncorrelatable run or incomplete cleanup observation |
| PASS | timely S_OK, nonnull outputs, level11_0, readable adapter Flags with SOFTWARE clear, resource policy satisfied, test references released, and terminal receipt validates against the exact reviewed package |

A successful WARP/device fallback is never HW01 PASS. Hardware result means the
specified driver path and available adapter metadata on owner-attested Xbox; it
does not prove physical GPU identity, present/readback correctness, throughput,
maximum resource sizes, every feature level or device-loss recovery.

10-second observer +30-second owner observation window are separate. Driver calls
and storage cannot be forcibly cancelled safely; if a call/I/O hangs, the initial
durable checkpoint may be the only evidence. No final receipt means INCONCLUSIVE,
never fabricated failure persistence. At30s owner records current state and stops
observation; closing/termination requires the approved scope, never an automatic
kill or retry. This limitation must remain visible in implementation and runbook.

## Future build/acceptance artifacts and gates

Expected files: original probe source, new manifest, native-only build config,
fixed D06-HW01 profile, v2 native receipt schema, build/source hash receipt,
preprocessed exclusion audit, direct/delay import/dependency report, unsigned APPX
and immutable member-hash index. Later signing creates a separate copy and external
evidence index with signed SHA256. No binaries are produced by this design phase.

Before execution, review every source/build diff against the new-project policy;
prove no JNI/Java inputs/actions, exactly one case, zero capabilities, ordinary
UWP activation and unchanged frozen baseline. Windows compilation is not a hardware
test. Separate approvals: implementation/build/static review -> signing -> new
package installation only (no auto-launch) -> one D06-HW01 run -> scoped receipt
collection -> case acceptance -> next experiment. No source implementation now.
