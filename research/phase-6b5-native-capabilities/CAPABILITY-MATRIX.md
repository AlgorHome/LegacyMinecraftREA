# Native capability contracts — proposed, NOT EXECUTED

Every case below currently has status **NOT EXECUTED**. None is part of an
automatic sweep. Each future run records its own case/version/policy, precondition
check, stage/error, resource budget, cleanup and terminal receipt. Bounds are
project safety policies, not Windows/Xbox guarantees. Synchronous driver/I/O calls
may exceed them; see SAFETY-AND-ACCEPTANCE.md for observer limits.

For EVERY row: PASS requires its stated oracle and durable validated receipt;
FAILED means a documented supported operation violated that oracle; BLOCKED means
missing prerequisite/API/device/consent; INCONCLUSIVE means timeout, interruption,
ambiguous evidence or unverified capability. API E_NOTIMPL/E_NOINTERFACE or an
unsupported contract is BLOCKED when support was a prerequisite, not fabricated
success. Unexpected generic errors on an exercised required supported path are
FAILED with exact HRESULT. Missing receipts never become PASS. A specifically
designed negative case can PASS only by matching its declared expected rejection.
NOT EXECUTED means no approved attempt occurred, never a synonym for FAILED.

## Graphics — D06 subcases

| Case / uncertainty | Entry conditions and exact API stimulus | Expected observations / PASS oracle | Bound and resource policy | Cleanup / non-PASS distinction |
|---|---|---|---|---|
| D06-HW01 — hardware device creation | new package; fixed HW-only profile; MTA case worker; D3D11CreateDevice(nullptr,HARDWARE,nullptr,BGRA_SUPPORT,{11_0},1,D3D11_SDK_VERSION); IDXGIDevice::GetAdapter, QI IDXGIAdapter1, GetDesc1 | S_OK, nonnull device/context, chosen11_0, adapter SOFTWARE flag clear; record request/result enums, not device serial/LUID; durable result | 10s observer, 30s owner window; one device attempt; no test textures/buffers/frames; see first-experiment budget | release context/device/adapter on owning worker; no WARP/retry. Unsupported adapter classification -> BLOCKED hardware-certification field, not assumed hardware. |
| D06-A01 — adapter enumeration access | HW01 assessed; CreateDXGIFactory1 / IDXGIFactory1::EnumAdapters1, GetDesc1, where public API available | capped enumeration with DXGI_ERROR_NOT_FOUND normal terminator; ordinal/count, hardware/software flags; no adapter description/LUID retention | 5s, max4 adapters; require terminator within cap for enumeration-complete PASS | release all COM references; cap reached -> INCONCLUSIVE enumeration completeness; inaccessible factory -> BLOCKED. No display reconfiguration. |
| D06-FL01 — selected feature/format support | reviewed feature query allowlist; known hardware device; GetFeatureLevel, CheckFeatureSupport(THREADING), CheckFormatSupport(R8G8B8A8_UNORM) | chosen level and exact supported bitfields; assert only declared target requirements, e.g. TEXTURE2D/RENDER_TARGET for next case | 5s; no allocations seeking maximum support; report documented level-derived limits separately from measured behavior | release device; missing optional bit reported unsupported/BLOCKED dependent subcase, no false higher-level claim. No exhaustive feature sweep. |
| D06-RES01 — bounded textures/buffer work | HW01 and required format bits; CreateTexture2D 64x64 RGBA8 DEFAULT render target + STAGING readback; CreateBuffer 4096 bytes with known pattern; CopyResource, query EVENT/GetData, Map(DO_NOT_WAIT) only after ready | descriptor/HRESULT checks, byte-exact known clear/readback (per-channel tolerance1 for normalized color) and buffer checksum; no unbounded Map wait | 10s; <=1MiB declared test resource bytes, 5ms polling/backoff, bounded event query; driver overhead separately observed | Unmap/clear references/Release; not-ready deadline INCONCLUSIVE; device error FAILED + GetDeviceRemovedReason; no driver reset. |
| D06-P01 — bounded CoreWindow render/present | HW01/RES01; exclusive ownership of THIS new app's CoreWindow swapchain; UI status renderer paused for test; CreateSwapChainForCoreWindow, CreateRenderTargetView, ClearRenderTargetView, Present | known two-color pattern, <=3 presented frames, exact Present HRESULTs, owner sees ordered colors; GPU readback oracle from RES01 retained separately | 10s technical /30s owner; <=640x360 test surface where supported, two buffers, declared texture bytes <=8MiB incl readback; adapt only through reviewed policy | release swapchain/targets before restoring UI; S_OK Present is not proof of human display; occluded/hidden -> INCONCLUSIVE, unsupported size/API -> BLOCKED. No concurrent swapchains or production display access. |
| D06-ERR01 — unsupported feature/removal reporting | previously approved hardware path; one intentionally invalid local texture descriptor (zero width) as negative API contract; GetDeviceRemovedReason after real graphics errors | expected E_INVALIDARG/no object -> negative-case PASS; genuine removed reason captured numerically; normal S_OK removal query does NOT validate device-removal recovery | 5s; single invalid API call, no GPU hang/TDR injection or reset | release any unexpected object; accepted invalid desc FAILED oracle; natural removal handling remains NOT EXECUTED unless actually observed. |
| D06-SW01 — optional software control | separate explicit review/approval and platform support; D3D_DRIVER_TYPE_WARP only, never automatic HW fallback | separately labeled SOFTWARE_CONTROL result; even PASS cannot satisfy HW01 or Xbox hardware D06 | 10s, same bounded resources only after support review | release software device; unsupported Xbox path BLOCKED. No WARP DLL downloads; this case is deferred and optional. |

## Controller input — separate native dispatch, no old S21 handler reuse

| Case / uncertainty | Entry conditions and exact API stimulus | Expected observations / PASS oracle | Bound and resource policy | Cleanup / non-PASS distinction |
|---|---|---|---|---|
| IN-ENUM01 — WGI availability/enumeration | focused diagnostic view; Gamepad::Gamepads, GamepadAdded/Removed; callbacks registered before synchronized snapshot | count/synthetic per-run ordinal and consistent collection; at least one gamepad for device-present PASS; no User/nonroamable ID/account APIs | 5s enumeration; max4 in collection, no growing event log; controller unavailable -> BLOCKED reading case | revoke event tokens; no identity retention, vibration or headset probes. API exception on available path FAILED. |
| IN-READ01 — button/axis observations | ENUM01; explicit owner prompt; GetCurrentReading polling at <=60Hz; press/release A,X and D-pad; both sticks direction/neutral; both triggers | edge counts, timestamps/min/max only; sticks finite in[-1,1], triggers[0,1]; each specified action detected; reviewed threshold0.5 directional,0.8 trigger, neutral0.25; calibration limits disclosed | 30s total; fixed aggregate counters <=8KiB; B always cancels; no Guide/system-button interception | stop polling/revoke; focus loss pauses polling and records interruption but deadline continues; incomplete owner sequence INCONCLUSIVE, invalid numeric data FAILED, cancel INCONCLUSIVE/OWNER_CANCELLED. |
| IN-HOT01 — controlled disconnect/reconnect | owner explicitly agrees to disconnect same test controller; WGI add/remove + CoreWindow Activated/VisibilityChanged observations | one removal and one addition with correct prompt transitions; do not assert physical identity is same, no serial/account mapping | 45s wall observation, max8 events; alternate owner cancellation route if controller unavailable | revoke events; absent reconnect INCONCLUSIVE; never change pairing/security or force disconnect via code; cancel does not launch another app. |

## Audio — output only, no capture

| Case / uncertainty | Entry conditions and exact API stimulus | Expected observations / PASS oracle | Bound and resource policy | Cleanup / non-PASS distinction |
|---|---|---|---|---|
| AU-INIT01 — graph/default output setup | public Windows.Media.Audio availability reviewed; AudioGraphSettings(AudioRenderCategory::GameEffects), AudioGraph::CreateAsync, CreateDeviceOutputNodeAsync; do NOT Start | graph/device creation statuses success; inspect graph.EncodingProperties sample rate/channels/subtype and SamplesPerQuantum; no endpoint/user/device ID logs | 10s async observer; one graph and output node; no tone, file/capture inputs or microphone capability | close graph/nodes even on error; missing output device/API -> BLOCKED; successful setup does not establish audible output. |
| AU-TONE01 — bounded synthetic playback | INIT01; separate explicit low-volume playback consent immediately before run; owner controls comfortable system volume; approved original synthetic frame fixture | frame-input node feeds 440Hz,0.02 full-scale amplitude, <=0.5s stereo/mono matching reviewed format; bounded frame/quantum counts complete; owner confirms audibility separately | 10s including completion; max1MiB buffers; no boost/system-volume changes, repeat, microphone, user files or loopback | Stop graph, disconnect/close frame/output nodes; consent declined -> BLOCKED, unheard but API completion -> INCONCLUSIVE audible field, playback error FAILED; cancellation stops sound ASAP. |

## Lifecycle — owner actions are individually approved stimuli

| Case / uncertainty | Entry conditions and exact API stimulus | Expected observations / PASS oracle | Bound and resource policy | Cleanup / non-PASS distinction |
|---|---|---|---|---|
| LC-FOCUS01 — visibility/focus state | existing CoreWindow::Activated, VisibilityChanged, CoreApplication EnteredBackground/LeavingBackground if available; owner opens/closes Dev Home overlay without launching unrelated apps | ordered focus/visibility records with receipt checkpoints and input disarmed outside focus; do not equate background/focus loss with suspend | 45s external owner window; <=8 records then stop | revoke tokens; missing expected event -> INCONCLUSIVE/unsupported event API BLOCKED; no console setting changes or auto focus stealing. |
| LC-SUSP01 — actual suspend/resume | new lifecycle observers: CoreApplication::Suspending/Resuming, SuspendingOperation::GetDeferral/Deadline; owner-approved OS action capable of actual suspend must be identified first | pre-suspend checkpoint committed within OS deadline with safety margin, deferral completed on every path; resumed event preserves process/run relationship and resources revalidated | checkpoint target<=250ms, respect earlier OS Deadline; external window60s; no worker watchdog can run while app suspended | complete deferral/revoke; no real suspend stimulus available -> BLOCKED, background event alone insufficient; interrupted/missing resume INCONCLUSIVE. No synthetic API assertion or automatic resume/launch. |
| LC-REC01 — recovery after permitted termination | separate exact-app termination AND later one-launch approval; before termination an active-case checkpoint must exist; read old journal in new process | new process UUID/run, old incomplete run retained and classified INTERRUPTED/INCONCLUSIVE, no invented terminal completion; new run separately recorded | owner window30s each approved stage; no repeated launches or PID-wide kill | read/preserve old evidence, no clearing or overwriting; identity/old checksum mismatch FAILED binding; unavailable owner termination route BLOCKED. |

## Native dependencies and safe resources

| Case / uncertainty | Entry conditions and exact API stimulus | Expected observations / PASS oracle | Bound and resource policy | Cleanup / non-PASS distinction |
|---|---|---|---|---|
| ND-STATIC01 — import graph | static ZIP/PE/import/delay-import inspection of exact proposed package and reviewed SDK/framework sources; no module loading | complete packaged-module graph/hashes/architecture/export matches; system/API-set edges explicitly unresolved or justified from reviewed contracts, not fabricated DLL searches | offline analysis bounded to approved package and declared dependencies; no hardware attempt | no runtime cleanup; PASS only for declared static coverage, unresolved required edge -> BLOCKED closure, runtime closure remains untested. |
| ND-LOAD01 — packaged original sentinel | dedicated build only; self-authored minimal x64 UWP DLL with trivial DllMain and one pure fixed-checksum export; hash before load; LoadPackagedLibrary(fixed package-relative name,0), GetProcAddress | module handle, expected export return for fixed input; missing fixed nonexistent sentinel-name control returns failure/GetLastError without crash; distinguish positive/negative subresults | 10s; one module+one negative control; no path/PATH/network/runtime fallback; no arbitrary owner filename input | call FreeLibrary only after no outstanding work; sentinel starts no threads. Reject unsigned/unreviewed inventory before loading. Missing declared module FAILED, API/policy unavailable BLOCKED. |
| RS-OBS01 — resource accounting availability | MemoryManager::AppMemoryUsage/Limit/Level; ProcessDiagnosticInfo::GetForCurrentProcess().MemoryUsage().GetReport | before/after fixed snapshots with units and availability; positive sane usage/limit or explicit errors; no other-process/account inventory | 5s, <=4 snapshots, no allocation benchmark or limit changes | no active resources; missing optional metrics individually BLOCKED, not zero; this is not peak-capacity certification. |
| RS-ALLOC01 — small deterministic allocation | RS-OBS01 usable limit/headroom; one original byte-array checksum fixture, no executable memory | 4MiB allocation/touch/checksum/release, valid numeric before/during/after samples; do not require counters return exactly to baseline | 5s; allocation <=min(4MiB,5% observed headroom), require >=64MiB remaining margin; otherwise BLOCKED; no OOM/limit seeking | free allocation on every path; bad_alloc after prerequisites FAILED with code, pressure change cancels INCONCLUSIVE; no cap alteration, protection/JIT APIs. |

## API/platform references and review gates

Public UWP requirement pages describe contracts, not guaranteed availability or
all behavior on this Series X build. Runtime unavailability is an explicit outcome.
Do not substitute GDK-only interfaces, desktop-only APIs, debug-layer binaries or
private Xbox SDKs to force success.

- Graphics: [D3D11CreateDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-d3d11createdevice),
  [GetDesc1](https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiadapter1-getdesc1),
  [CheckFeatureSupport](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-checkfeaturesupport),
  [CreateTexture2D](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createtexture2d),
  [GetData](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-getdata),
  [CoreWindow swapchain](https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_2/nf-dxgi1_2-idxgifactory2-createswapchainforcorewindow),
  [GetDeviceRemovedReason](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-getdeviceremovedreason).
- Input: [Microsoft Xbox/UWP WGI guide](https://learn.microsoft.com/en-us/windows/uwp/gaming/gamepad-and-vibration).
  Use the state APIs, not user association or vibration APIs.
- Audio: [AudioGraph architecture and output/frame input](https://learn.microsoft.com/en-us/windows/apps/develop/media-authoring-processing/audio-graphs).
  Rendering only; no CreateDeviceInputNodeAsync or audio file APIs.
- Lifecycle: [UWP lifecycle](https://learn.microsoft.com/en-us/windows/uwp/launch-resume/app-lifecycle).
  System decides whether backgrounding actually suspends or terminates an app.
- Native loading: [LoadPackagedLibrary](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-loadpackagedlibrary).
  Declared dependency graph search is not arbitrary desktop DLL search; never call
  it in DllMain. Sentinel source/import/static review precedes execution approval.
- Resources: [MemoryManager](https://learn.microsoft.com/en-us/uwp/api/windows.system.memorymanager?view=winrt-28000),
  [AppMemoryUsageLimit](https://learn.microsoft.com/en-us/uwp/api/windows.system.memorymanager.appmemoryusagelimit?view=winrt-28000).
  Legacy [Xbox One resource guidance](https://learn.microsoft.com/en-us/previous-versions/windows/uwp/xbox-apps/system-resource-allocation)
  is historical context, not a promised Series X budget. Record observed current
  limits; do not change App classification or resource capabilities.
