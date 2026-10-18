# Phase 6B.5i — D06-RES01a implementation

**PASS_STATIC_ONLY. x64 compilation, unsigned packaging and static checks passed.**
Hardware status: **NOT EXECUTED**. No diagnostic binary was run.

- Research branch: research/phase6b5i-d06-res01a.
- Exact source commit: `4457142ff1fd9e01371eb446612c70162ce93357`.
- Parent accepted FMT01 source: bbe3a42c422e4328d5f98c07a9370fa948d0cbbf.
- Build ID: 20261017-183031-15ba7835.
- Unsigned APPX: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-183031-15ba7835\NativeCapabilities.unsigned.appx`.
- SHA256: **526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8**.

## Preserved baselines

Before source changes,107 pinned original artifact/evidence/source files and4 Git
source references were checked. The same107 files were rehashed after building and
remain unchanged. BASELINE-PRESERVATION.json supplies exact paths/SHA256s, including
accepted D00/HW01/FMT01 signed packages, receipts, original photographs and acceptance
reports. The original FMT01 research branch remains at the accepted commit. Prior
ignored build outputs are preserved; no accepted package was rebuilt or overwritten.

Production reference d1453434ceefe73bef5aff497194e09f39dde7e1;
D00 source553c6554f40f1372b0ea09f6badbbb98e133a9ab;
HW01 source a3f72874241914f6048d4ca9ec4fc0edc978625d;
FMT01 source bbe3a42c422e4328d5f98c07a9370fa948d0cbbf.
Accepted FMT01 signed SHA256 ae19e5ff93438bcf8a3c9e0d42ad0323908ee83d95231cba9dcd9a319fd5d8ef
and hardware receipt453d84192d19a698513513742468dae8509c74973ecd9645fe08266cb1184893
are preserved. No console/installed application/LocalState was accessed or changed.

## Identity/version and startup

Same diagnostic-only identity AlgorHome.LegacyForge.NativeDiagnostics,
publisher CN=LegacyForgeDiagnostics; version **0.2.2.0**, x64, application Id App,
entry point LegacyForgeNativeDiagnostics.App. MTA/CoreApplication startup retained;
zero capabilities, original Windows.Universal and Microsoft.VCLibs.140.00 dependencies.
App classification is required at later owner inventory; a host manifest cannot verify
that console configuration field. No framework is bundled or installed.

A future installation would **replace registered0.2.1.0 NativeDiagnostics**, potentially
retaining stale FMT01/HW01 LocalState. It is not side-by-side. No replacement occurs now.
If installed FMT01 must remain independently runnable, stop before signing/installation
and separately approve a distinct package identity and corresponding receipt bindings.
Accepted RuntimeDiagnostics D00 and production LegacyForge remain separate identities.

Only RES01a may dispatch: one-shot activation flag, Launch only, empty or exact
D06-RES01a argument. Other case arguments reject before worker/GPU dispatch. No Java
handlers, sweep or interactive test selection. LFN_NATIVE_ONLY1, LFN_JNI_ENABLED0,
LFD_D00_ONLY1 and LFN_CASE_D06_RES01A1 are compiler-checked; old HW01/FMT01 macros
are rejected. The inherited D00-named macro is a Java exclusion lock, not a D00 dispatch.

## One texture operation

Use accepted one-attempt hardware D3D11 device creation: HARDWARE,11_0,
BGRA_SUPPORT, no alternate driver/fallback. Establish adapter SOFTWARE flag clear.
CreateOneTexture checkpoints BEFORE_CREATE_TEXTURE and checks deadline/terminal state.
Then **one** `device->CreateTexture2D(&requested,nullptr,texture.put())` call.
Nonnull output storage is supplied; no initial data, content writes or reads.

| Descriptor field | Fixed requested value |
|---|---|
| Width /Height |1 /1 |
| MipLevels /ArraySize |1 /1 |
| Format | DXGI_FORMAT_R8G8B8A8_UNORM /28 |
| SampleDesc.Count /Quality |1 /0 |
| Usage | D3D11_USAGE_DEFAULT /0 |
| BindFlags | D3D11_BIND_SHADER_RESOURCE /8 |
| CPUAccessFlags /MiscFlags |0 /0 |

S_OK and nonnull texture are required. GetDesc is called once only after that success
and within deadline. It returns void, so no GetDesc HRESULT is invented. All11 scalar
fields (including sample count/quality) are compared explicitly, not via padded-memory
comparison. JSON records requested/returned descriptors and comparison boolean.
S_FALSE or another non-S_OK success is FAILED/TEXTURE_ALLOCATION_NOT_CONFIRMED,
including any unexpected nonnull output; it never proves allocation.

Scoped texture reference releases before scoped context/device references; any texture
returned unexpectedly on failure is also released. Resource flags are emitted after scopes
complete. No texture pointer/address is disclosed, only nonnull validity. No initialization,
SRV/RTV, render target, shader/compiler, buffer, draw/clear/copy/map/readback, swapchain,
presentation, WARP, second format query, repeated GPU work or stress loop is included.
SHADER_RESOURCE is an allocation bind flag only, not an actual shader-view creation.
Nominal texture data4bytes; actual driver allocation overhead is not bounded to4bytes.

## Receipt and outcome contract

Schema **legacyforge-native-capability-receipt-v3**, scoped to D06-RES01a0.2.2.0.
LocalState/NativeCapabilityReceipts/D06-RES01a-<run UUID>.json; same-name .json.tmp
is partial evidence only. Receipt binds source/build, frozen reference commits, expected
package identity, separate process/run UUIDs, device/adapter observations, texture HRESULT
and signed value, pointer validity, requested/returned descriptors, release/memory,
terminal result and six payload-role hashes. Normal sequence STARTED1 ->
BEFORE_CREATE_DEVICE2 -> BEFORE_CREATE_TEXTURE3 -> FINAL4.

| Outcome | Defined rule |
|---|---|
| PASS | Correct identity/build/six independent hashes; hardware S_OK/device/context/11_0/non-software adapter; texture S_OK+nonnull; GetDesc all11 fields exactly match fixed descriptor; releases complete; before headroom>=256MiB, observed growth<=64MiB, elapsed<10s; original terminal receipt subsequently retrieved and independently verified. Reason RGBA8_TEXTURE_CREATED_DESCRIPTOR_MATCH. |
| FAILED | Normal negative creation HRESULT, unexpected device outputs/software adapter, texture S_OK+null, non-S_OK success/S_FALSE, descriptor mismatch, native exception or observed growth>64MiB. No unsupported content/readback claim. |
| BLOCKED | Missing API/policy/classification/memory/receipt prerequisites; headroom insufficient. Device/texture E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED map to BLOCKED; exact returned HRESULT retained. |
| INCONCLUSIVE | Deadline/late return/owner close/observer failure; missing/nonterminal/partial/unbound original evidence or unresolved identity/hash mismatch. Watchdog can win without driver return/cleanup evidence. |
| NOT EXECUTED | No authorized target run/evidence. Distinct schema enum (with space) and current hardware status; compilation/synthetic fixtures never satisfy PASS. Runtime checkpoints use RUNNING until terminal. |

Requested descriptor is recorded before device creation; texture-specific HRESULT and
returned descriptor are absent if no call/result/GetDesc exists. Missing output is never
fabricated as a zero-filled successful descriptor. Exception receipts may contain only
sanitized HRESULT/reason, with partial observations unavailable; never infer cleanup.

## Bounded reporting and remaining risks

Inherited10s deadline,30s owner observation, first terminal wins/late PASS denied.
No watchdog cancellation or process/thread termination. A blocked GPU, GetDesc, COM
release, package hash read or storage call cannot be forcibly bounded/cancelled here.
Startup hashing/initial receipt precede deadline arming.128KiB writer byte limit,
100ms I/O-lock acquisition, finite byte-progress writes, same-directory temporary file,
flush/close then atomic replace; no retry. These are work/byte/lock bounds, not a hard
OS-call wall-clock guarantee. VERIFY_BY_RETRIEVAL avoids self-predicting durable flush.
Formal PASS requires downloaded final original; UI saved/PASS text alone is insufficient.

Memory observation is bounded to before/after samples; it is not peak memory, leak or
strict GPU allocation proof. C++ scoped cleanup is reviewed, not executed; process crash
or blocked call may prevent reporting. MessageDialog behavior/async error visibility are
inherited; dialog is platform UI, not app rendering. Target loader closure, graphics behavior,
receipt persistence and signing/trust for0.2.2.0 remain untested. No texture content use,
rendering, presentation, OpenGL, LWJGL, Java/JNI or Minecraft compatibility established.

## Build/static evidence

Existing Windows x64 MSVC14.44.35207 UWP store libraries, SDK10.0.26100.0/C++WinRT,
PowerShell7, Python3 standard library. Tool paths/hashes and command exit codes in
BUILD-RECEIPT.json; no download, certificate, framework install or console needed.
Reproduce from the clean committed checkout:

```powershell
Set-Location -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics'
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Fresh ignored out directory; app/report/probe compiled/preprocessed with /W4 /MD /O2,
UWP API family and AppContainer x64 link. Final compile/link/import/header/MakeAppx/
static-safety steps exit0. Six unsafe compiler-only configurations reject with #error.
Eight valid synthetic receipt forms pass;30 malformed cases reject, including every
returned descriptor field, S_FALSE-as-PASS, missing release, stale identity, late PASS,
forged payload bindings and duplicate JSON. No native target code was executed.

Exact11-member payload allowlist, unsigned signature absence, ZIP CRC, member bytes,
64KiB block hashes, optional whole-file hashes, local-header sizes and file sizes pass.
Native module/symbol imports **identical to FMT01**; texture/GetDesc use COM vtables.
Assets/license unchanged; no Java/Minecraft/runtime/proprietary fixture. Dependency
manifest unchanged; system/CRT loader closure still requires later platform evidence.

## Exact source comparison against accepted FMT01

SOURCE-DIFF.patch is the complete diff; SHA256 recorded in BUILD-EVIDENCE.json.

| Path under diagnostics/NativeCapabilities | Change |
|---|---|
| src/probe.cpp | Remove format-query operation; add fixed descriptor serialization/equality helpers and single CreateTexture2D/GetDesc path, checkpoint, pointer/HRESULT/descriptor/release fields and outcomes. Accepted device/classification/memory/scoped-device path retained. |
| src/report.cpp | Version guard0.2.2.0, schema v3, frozen FMT01 reference, RES01a policy-role path and per-run filename. Writer/deadline/terminal machinery unchanged. |
| src/app.cpp | Case/version/title and scope text; label device HRESULT explicitly. Scheduling, activation guards, MTA and dialog mechanics unchanged. |
| include/native.h | Single allowed case constant RES01a. |
| include/build_config.h | RES01a macro required; previous HW01/FMT01 macros forbidden; Java locks retained. |
| package/Package.appxmanifest | Version and display/description only. Identity/entry point/capabilities/dependencies/platform unchanged. |
| profiles/D06-RES01a.json | Replace FMT01 policy with fixed descriptor, one texture attempt and exclusions; previous device/memory/deadline limits retained. |
| contracts/native-receipt.schema.json | Version3, case/version/reference binding, new checkpoint/texture/descriptor fields; previous format-mask fields removed. |
| native-inventory.json | Case label only, empty runtime/fixture/module lists retained. |
| build.ps1 | Case/profile/macro and additional prior-FMT01 rejection check; no new runtime source or link library. |
| tools/receipt_contract.py | New texture/descriptor oracle and original synthetic fixtures; structure validator retained. |
| tools/static_verify.py | Permit exactly one reviewed texture factory; forbid other work and old query, verify descriptor comparisons and new policy/schema. |
| README.md | New case contract, build, limits and update semantics. |

New generated commit/build identity, EXE/package hashes and blockmap reflect these changes;
no other source path changed. No accepted artifact was rebuilt. Next gate: explicit
**local signing-only authorization** for one fresh copy, not installation or execution.

Microsoft sources checked for contract details:
[CreateTexture2D](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createtexture2d)
(S_OK vs parameter-validation-only S_FALSE; null initial data has undefined contents),
[GetDesc](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11texture2d-getdesc)
(void metadata query). No undefined texture contents are read.
