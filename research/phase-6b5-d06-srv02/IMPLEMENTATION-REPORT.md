# Phase6B.5s — D06-SRV02 backing-resource identity implementation

**PASS_STATIC_ONLY**: unsigned x64 compilation, packaging and static verification passed.
Hardware **NOT EXECUTED**. No signing, installation, target launch, console/data access,
certificate/trust or production change occurred.

- Branch research/phase6b5s-d06-srv02.
- Exact source commit `c81d0f48286513f7a7579a1d2d786cca4f5e60e2`; accepted parent e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8.
- Build ID 20261017-192156-1c3f66cf.
- Unsigned APPX `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-192156-1c3f66cf\NativeCapabilities.unsigned.appx`.
- SHA256 **88cde899358b6eaade1658802831c5a914b8e637cf1466321b233fa8a2788c31**.

## Baseline preservation and identity

175 pinned local artifact/evidence/source files and6 source references checked before
source edits and after build; all unchanged. Includes accepted SRV01 signed package
da28a5c22cb27b913b2bf296155c9d9bc5745e37ff3b2af88832f7661e042724,
unsigned e70fd6c9ef76ff17a06a9ad605c6c88e5eb412240446b6bbfcf17d1b8897c693,
receipt5a989a129e49658d42dcc61abc364b8a614feb7a7006ed897394a4c178f51d9b
and original photo9dec20778c9add96fb54d18ea84fa4bb2d316b89435ae588fe37ae92eddac8e1.
BASELINE-PRESERVATION.json lists all earlier D00/HW01/FMT01/RES01a/SRV01 pins/ref commits.
Accepted SRV01 branch remains at its original commit. Prior packages/evidence not rebuilt,
overwritten or changed. Production reference d1453434ceefe73bef5aff497194e09f39dde7e1
remains untouched; all source changes confined to diagnostics/NativeCapabilities.

Manifest validated: AlgorHome.LegacyForge.NativeDiagnostics /CN=LegacyForgeDiagnostics,
version **0.2.4.0**, x64, Application Id App, entry point LegacyForgeNativeDiagnostics.App.
MTA/CoreApplication retained; zero capabilities, unchanged Windows.Universal and
Microsoft.VCLibs.140.00 dependencies. Console App classification requires later owner
inventory and is not inferred from Application Id App. No framework bundled/installed.

Future installation updates/replaces registered0.2.3.0 and may retain stale LocalState.
It is not side-by-side; no installed app is changed now. If independently runnable installed
SRV01 must remain, stop before installation for a distinct identity/build approval.
Accepted RuntimeDiagnostics D00 and production remain separate identities.

## One case and minimal new API use

Existing one-shot/Launch-only empty-or-exact-case dispatch now permits D06-SRV02 only.
Previous case macros rejected before compilation; native-only1/JNI0/inherited-D00-lock1/
SRV02-case1 fixed. The D00-named macro excludes Java, not a D00 dispatch route.

One accepted HARDWARE/11_0/BGRA device and non-software adapter classification;
one accepted1x1 RGBA8 DEFAULT/SHADER_RESOURCE texture; one accepted explicit Texture2D
SRV. Texture11-field and SRV4-active-field descriptor checks must pass first. No extra
format query, resource variation, retry, pipeline state or content access.

InspectBackingResource:

1. Persist BEFORE_GET_RESOURCE checkpoint; reject expired/terminal dispatch.
2. Exactly one `srv->GetResource(resource.put())` call, nonnull output storage.
   It returns void and adds one owned resource reference; no HRESULT is invented.
3. Require nonnull ID3D11Resource before querying identity.
4. Exactly one explicit QueryInterface for original texture, then (only after first
   S_OK+nonnull and deadline check) one for returned resource. Both use
   `__uuidof(IUnknown)`, precisely IID_IUnknown, without a new GUID library dependency.
5. Require both actual HRESULTs **S_OK**, both canonical IUnknown outputs nonnull, then
   compare `originalIdentity.get()==backingIdentity.get()`. Record boolean equality only.
   Failed/null queries never compare two nulls as PASS and omit unavailable result fields.
6. Inner temporary IUnknown scopes end first, then returned ID3D11Resource scope. Return
   while caller still owns SRV; SRV scope ends before texture/context/device scopes.
   Record release/order markers after the relevant scope boundaries.

No raw pointers, credentials, texel initialization/read, pipeline binding, shaders,
draw/clear/copy/map/readback, RTV, swapchain/presentation, software/WARP fallback,
GPU/identity retry loops or Java/JNI/Minecraft. Underlying driver allocations/release
behavior are not guaranteed merely by scoped owned-reference markers.

## Receipt contract and results

Schema **legacyforge-native-capability-receipt-v5**, case D06-SRV02/package0.2.4.0.
LocalState/NativeCapabilityReceipts/D06-SRV02-<run UUID>.json; .json.tmp partial only.
Source/build/frozen refs/expected identity/process/run UUIDs, original resource HRESULTs/
descriptors, GetResource call/non-null output, both QI HRESULTs/signed values/attempted/
nonnull outputs, comparison-performed/equality, reference release ordering, memory,
deadline/terminal and six payload hashes are bound. No invented get_resource_hresult
or raw-address property is allowed by the closed schema.

Normal sequence STARTED1 -> BEFORE_CREATE_DEVICE2 -> BEFORE_CREATE_TEXTURE3 ->
BEFORE_CREATE_SRV4 -> BEFORE_GET_RESOURCE5 -> FINAL6. No earlier overwritten checkpoint
history can be inferred solely from final metadata; original final retrieval remains required.

| Result | Rule |
|---|---|
| PASS | Accepted device/texture/SRV prerequisites; nonnull returned backing resource; both IID_IUnknown queries S_OK+nonnull; canonical equality true; all temporary/resource/SRV/texture cleanup/order markers true; memory/deadline policy, source/build/identity/six independent hashes and original final receipt/photo/run verification. Reason SRV_BACKING_RESOURCE_IDENTITY_CONFIRMED. |
| FAILED | Normal native failure/output/descriptor mismatch; GetResource null; either QI non-S_OK (including S_FALSE/E_NOINTERFACE), missing identity output or identity inequality; native exception or memory-growth breach. |
| BLOCKED | Missing API/policy/classification/memory/receipt prerequisite or checkpoint; before headroom<256MiB. Device/texture/SRV E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED retain blocking policy; identity-query failures are case FAILED, not assumed unsupported. |
| INCONCLUSIVE | Deadline/late return/owner close/observer failure, incomplete/unbound original evidence or unresolved attribution/persistence. No cancellation claim. |
| NOT EXECUTED | Current hardware status; build and JSON-contract tests are not native execution. RUNNING is intermediate only. |

Request descriptors unchanged: texture width/height/mips/array1, format28, sample1/quality0,
DEFAULT0, SHADER_RESOURCE8, CPU/misc0; SRV format28/TEXTURE2D4/most-detailed-mip0/mips1.
A comparison is only valid after two successful nonnull canonical queries; equality of
arbitrary interface pointers is not used. Separate queried references each own one release,
even when pointers identify the same COM object. No Release-count-to-zero assertion.

## Bounded observation and unresolved risks

Inherited10s decision deadline/30s owner window, first-terminal ownership and late-PASS guard.
No cancellation of GPU/GetResource/QueryInterface/Release/file calls and no process/thread
termination. Startup package hashing/initial write precedes timer arming. Writer128KiB,
100ms I/O lock, finite byte progress, temp/flush/close/atomic replace/no retry. These are
byte/work/lock bounds, not hard native/OS wall-time or power-loss guarantees.
VERIFY_BY_RETRIEVAL avoids predicting a successful flush within the bytes being written.

Memory samples before/after: require>=256MiB headroom and<=64MiB growth. Not peak/leak/
repeated-run proof or driver allocation cap. Exceptions/timeouts may lose partial telemetry,
with no valid cleanup inference. Platform MessageDialog async errors remain incompletely
observed; dialog is not app-owned rendering. Actual0.2.4.0 identity-query, loader/startup,
cleanup and receipt behavior untested. Signing/trust and all hardware gates pending.
No shader, rendering, presentation, OpenGL, LWJGL, Java/JNI or Minecraft compatibility claim.

## Build, static and synthetic verification

Existing Windows MSVC14.44.35207 UWP store libraries, SDK10.0.26100.0/C++WinRT,
PowerShell7, Python3 standard library; tool paths/hashes/exit codes in BUILD-RECEIPT.json.
No downloads, certificate input, new dependencies or device access. Reproduce clean source:

```powershell
Set-Location -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics'
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Fresh ignored output;3 native units compiled/preprocessed, /W4 /MD /O2/UWP family,
x64 AppContainer/DYNAMICBASE/NXCOMPAT. All normal build/static commands exit0.
Eight unsafe preprocessor-only configurations fail with #error as expected.15 valid
synthetic receipts pass and53 invalid fixtures reject, including previous descriptor/S_FALSE/
cleanup/stale cases plus null resource, first/second failed QI, null identities, comparison
without success, unequal canonical identities, missing release/order, invented GetResource
HRESULT and raw pointer property. These are offline schema/oracle tests, not C++ execution.

11-member exact payload allowlist/stage bytes, unsigned signature absence, ZIP CRC,
all blockmap64KiB/optional whole-file hashes, sizes and local headers pass. Assets/license
unchanged, no extra runtime/executable/fixture. Native module/symbol set identical to SRV01;
new COM methods use vtables. Complete target loader/API closure remains untested.

## Exact source differences from accepted SRV01

SOURCE-DIFF.patch is the complete diff; digest stored in BUILD-EVIDENCE.json.

| File under diagnostics/NativeCapabilities | Change |
|---|---|
| src/probe.cpp | Add InspectBackingResource/getter/two canonical QIs/non-null/HR/equality/cleanup/deadline paths; called only after successful SRV descriptor match. Existing device, texture, SRV descriptors and policies unchanged. |
| src/report.cpp | Version guard0.2.4.0, schema v5, frozen SRV01 reference, new case profile hash path/per-run filename. Atomic writer/deadline mechanics unchanged. |
| src/app.cpp | Case/version/title/scope text only; MTA, activation guards and scheduling unchanged. |
| include/native.h | Single case constant SRV02. |
| include/build_config.h | SRV02 macro, prior SRV01 forbidden alongside earlier cases; native/JNI lock retained. |
| package/Package.appxmanifest | Version/display/description only; identity/entry point/capabilities/platform/dependencies retained. |
| profiles/D06-SRV02.json | New one-getter/two-one-per-object-QI/equality/reference-order policy, previous descriptors/limits retained. |
| contracts/native-receipt.schema.json | v5/reference/case/version/getter/QI/comparison/cleanup fields and new checkpoint. |
| native-inventory.json | Case label only; empty fixtures/runtimes/extra-modules retained. |
| build.ps1 | Case/profile/macro plus prior-SRV01 rejection test; same source/link libraries. |
| tools/receipt_contract.py | Canonical identity semantic checks and original positive/negative fixtures; structural validator retained. |
| tools/static_verify.py | Exact getter/QI API/count/output guards and scope/policy/contract checks. |
| README.md | Updated scope/build/limits/update semantics. |

Generated source/build identity, EXE/input/package hashes/blockmap naturally change. No other
source directory changed and no accepted artifact was rebuilt. Next separate gate: local
signing-only approval naming exact unsigned hash/source; no implicit future device approval.

Microsoft basis:
[GetResource](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11view-getresource)
(void and returned-reference ownership),
[QueryInterface](https://learn.microsoft.com/en-us/windows/win32/api/unknwn/nf-unknwn-iunknown-queryinterface%28refiid_void%29)
(canonical IUnknown identity and successful-query reference ownership).
