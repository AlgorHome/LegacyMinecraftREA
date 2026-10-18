# D06-SRV03 static safety review

Verdict: PASS_STATIC_ONLY. Native diagnostic/hardware execution: NOT EXECUTED.

| Requirement | Static result and support |
| --- | --- |
| Isolated research scope | New research branch from accepted c81d0f4; diff restricted to NativeCapabilities; accepted artifacts/evidence preserved |
| Correct one-case dispatch | app.cpp launch-kind/arguments guard, atomic started exchange; build_config.h native-only/JNI-disabled/D00 lock and SRV03-only guard; all earlier case macros rejected |
| Hardware only | probe.cpp one D3D11CreateDevice HARDWARE/11_0/BGRA; nonsoftware adapter classification; no WARP/reference/retry |
| Fixed allocation | One1x1 RGBA8 DEFAULT SHADER_RESOURCE texture; one explicit Texture2D SRV; S_OK/nonnull outputs and independent GetDesc field comparison |
| GetDevice | probe.cpp InspectOwningDevice contains exactly one srv->GetDevice(returnedDevice.put()); nonnull storage and output required; void API, no HRESULT recorded |
| Canonical identities | Original ID3D11Device and returned ID3D11Device each QueryInterface(__uuidof(IUnknown)) once; both HRESULTs exactly S_OK, nonnull outputs and deadline checks before comparing canonical pointers |
| Reference ownership | Inner com_ptr<IUnknown> scopes release before owned returned device; then SRV, texture, context and original device; failure and exception unwinding scoped; no manual AddRef/Release arithmetic |
| Exclusions | No GetResource, binding/sampling, shaders, texel content initialization/read, render target, draw/clear/copy/map/readback, swapchain/presentation, runtime download or Java/JNI/Minecraft code/payload |
| Package | NativeDiagnostics0.2.5.0 x64, App Id App, corrected entry point/MTA; zero capabilities; dependencies/imports unchanged from SRV02 |
| Payload | Eleven allowlisted members; only NativeCapabilities.exe executable, original license/assets/schema/policy/inventory/build metadata; no runtime/extra modules/fixtures bundled |
| Receipt | Closed v6 schema, exact package/case, source/build/frozen pins, distinct UUIDs, six payload roles, no raw addresses; schema plus semantic validator and current-run retrieval required |
| Write policy | LocalState/NativeCapabilityReceipts, new run UUID, 128KiB serialized cap, 100ms lock attempt, temp-write/FlushFileBuffers/close/write-through rename; no cross-package path |
| Deadline |10s first-terminal ownership, guard against late PASS, separate observer; no cancellation or process termination APIs |
| Memory | Available before/after app samples required; >=256MiB initial headroom, <=64MiB observed growth; no GPU stress loop |
| Preservation |175 original frozen files and208 total accepted evidence/artifact files rehashed unchanged |

## Failure paths

- Device HRESULT failure: BLOCKED for unsupported/denied API or policy, otherwise FAILED; null device/context or wrong feature cannot continue.
- Adapter query/description unavailable: BLOCKED; software adapter: FAILED; no fallback.
- Texture/SRV HRESULT not S_OK, including S_FALSE: no allocation PASS; no getter on missing output. S_OK/null: FAILED. Wrong descriptors: FAILED; wrong view dimension does not read inactive union members.
- Checkpoint failure before a native call prevents that call (BLOCKED). Time expiry or an already terminal result prevents further probes; late returns produce INCONCLUSIVE and cannot overwrite prior terminal ownership.
- GetDevice null: FAILED, no QI. First QI not S_OK/null: FAILED, no second query/comparison. Second QI not S_OK/null: FAILED, no comparison. Valid unequal canonical identity: FAILED. All outputs remain scoped even on failures.
- Exception unwinds owned references and records FAILED exception HRESULT where available; it does not synthesize success/cleanup details. Unknown activation/case does not dispatch a worker.
- Unavailable memory: BLOCKED; insufficient initial headroom: BLOCKED; final sampled growth breach: FAILED.
- Persistence failure: UI cannot claim saved PASS; absent/inaccessible final retrieval blocks formal acceptance even if visible status says PASS.

PASS reason SRV_OWNING_DEVICE_IDENTITY_CONFIRMED requires all successful prerequisites, identity equality, release markers, deadline/memory policy. BLOCKED denotes unavailable prerequisite, FAILED a completed negative check, INCONCLUSIVE timeout/incomplete attribution, NOT EXECUTED no run. Formal acceptance additionally verifies original retrieved final JSON, all six independent pins and exact photo/run association.

Normal checkpoint sequence: STARTED1, BEFORE_CREATE_DEVICE2, BEFORE_CREATE_TEXTURE3, BEFORE_CREATE_SRV4, BEFORE_GET_DEVICE5, FINAL6. Prior stages replaced in one run file; final stage alone does not independently establish earlier bytes.

## Limits requiring later execution evidence

Native/driver/COM/file calls can block beyond observer deadline; no watchdog cancellation claimed. Observer/worker threads remain detached as in accepted source, with shared ownership and first-terminal guard; this is not forcible worker termination. GetDevice and QueryInterface calls use COM vtables, so absence of named PE imports does not mean absence of those calls. Static API cardinality and native import comparison are not runtime trace evidence. Release markers do not prove driver allocation reclamation, sampled memory does not prove peaks/leak freedom, atomic flush does not prove power-loss behavior. Actual Xbox activation, MessageDialog, APIs and persistence are all NOT EXECUTED for SRV03.

No signing, device access, console changes, installation, certificate/trust changes or production LegacyForge modification performed.
