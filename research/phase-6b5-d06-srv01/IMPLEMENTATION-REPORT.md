# Phase6B.5n — D06-SRV01 implementation

**PASS_STATIC_ONLY**: x64 compilation, unsigned APPX packaging and static checks passed.
Hardware **NOT EXECUTED**. Source/build approval does not authorize target execution.

- Branch: research/phase6b5n-d06-srv01.
- Exact source commit: `e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8`.
- Accepted parent:4457142ff1fd9e01371eb446612c70162ce93357 (D06-RES01a).
- Build ID: 20261017-185632-1c4c5a9c.
- Unsigned APPX: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-185632-1c4c5a9c\NativeCapabilities.unsigned.appx`.
- Unsigned SHA256: **e70fd6c9ef76ff17a06a9ad605c6c88e5eb412240446b6bbfcf17d1b8897c693**.

## Baseline preservation

141 pinned local artifact/evidence/source files and5 source references checked before
source changes and after build. All unchanged, including accepted RES01a signed SHA256
ead7016c94e551fac43e2b622b323354bfa4506fe507f44bf5e98f112b8f0c3f,
unsigned526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8,
receipt10081860917f805a82f366d0e2e9ddccb11a07deb330e16643bda68e55227fe9
and original photograph d62d1121b060179d27790454fc9165e26cc6fe4abfba7ab9c08c0723e740aee8.
BASELINE-PRESERVATION.json lists paths/pins for all earlier D00/HW01/FMT01/RES01a
artifacts, original receipts/photos/reports and source references. Original RES01a
branch remains at its accepted commit; no accepted build artifact was rebuilt/overwritten.
Production baseline d1453434ceefe73bef5aff497194e09f39dde7e1 is untouched.
No installed package, LocalState, certificate/trust store, dependency or console accessed.

## Identity/version and dispatch

AlgorHome.LegacyForge.NativeDiagnostics /CN=LegacyForgeDiagnostics /**0.2.3.0** /x64;
application Id App; entry point LegacyForgeNativeDiagnostics.App; MTA/CoreApplication
retained, zero declared capabilities. Windows.Universal and Microsoft.VCLibs.140.00
manifest dependencies unchanged, no framework bundled. Xbox classification App is required
at a later owner inventory; Application Id App does not itself verify that console field.

A future0.2.3.0 installation would replace registered0.2.2.0 NativeDiagnostics, potentially
retaining older RES01a/FMT01/HW01 LocalState. This is not side-by-side installation.
No replacement occurs now. If the installed accepted version must remain independently
runnable, separately approve a distinct package identity/build before installation.
Accepted RuntimeDiagnostics D00 and production remain separate identities.

One permitted case D06-SRV01; Launch with empty/exact-case argument only, one-shot
started flag. Old case/Java routes reject before worker/GPU dispatch. Compile gates
require native-only1/JNI0/inherited-D00-lock1/SRV01-case1; HW01/FMT01/RES01a macros
are rejected. The D00-named inherited macro is a Java-exclusion lock, not a D00 dispatch.

## Minimal operation and descriptor checks

Accepted hardware-only device path: one HARDWARE/11_0/BGRA_SUPPORT device request,
non-software adapter classification, no alternate driver/retry. One accepted1x1 RGBA8
texture: one mip, array1, sample1/quality0, DEFAULT usage, SHADER_RESOURCE bind flag,
CPU/misc0, null initial data and nonnull output. S_OK+nonnull and all11 texture descriptor
fields required before view creation. No texture initialization or reading undefined texels.

One explicit D3D11_SHADER_RESOURCE_VIEW_DESC:

| Field | Expected |
|---|---|
| Format | DXGI_FORMAT_R8G8B8A8_UNORM /28 |
| ViewDimension | D3D11_SRV_DIMENSION_TEXTURE2D /4 |
| Texture2D.MostDetailedMip |0 |
| Texture2D.MipLevels |1 |

After BEFORE_CREATE_SRV checkpoint/deadline gate, exactly one
`device->CreateShaderResourceView(texture,&requested,srv.put())` call. Only S_OK+nonnull
view leads to one view GetDesc; all4 active descriptor fields compared explicitly.
Both GetDesc methods return void; no resource-GetDesc HRESULT is invented. For a returned
non-TEXTURE2D dimension, comparison fails without reading the inactive Texture2D union;
JSON records only format/dimension in that mismatch case. SDK static_asserts bind numeric
format/dimension/bind/usage constants to the receipt contract.

View reference scope ends while caller still owns texture. Texture then leaves scope,
followed by context/device and adapter references; receipt marks per-resource release
and srv_released_before_texture. Those markers attest owned-reference scope progression,
not proof all driver allocations are freed. Unexpected nonnull error outputs still scoped.

No pipeline binding/VS-PS-CS resource setup, shader compile/execution/sampling, RTV/other
view, buffer, draw/clear/copy/map/readback, swapchain/presentation, WARP/software fallback,
format sweep, GPU loop, Java/JNI/Minecraft/runtime assets. Creating the view exposes only
metadata/allocation behavior; it does not establish sampling or rendering.

## Versioned receipt and result contract

Schema **legacyforge-native-capability-receipt-v4**, case D06-SRV01/package0.2.3.0.
Current-run path LocalState/NativeCapabilityReceipts/D06-SRV01-<run UUID>.json;
.json.tmp is partial evidence. Source/build, frozen reference commits, expected identity,
run/process UUIDs, device/texture/SRV HRESULTs and signed values, nonnull booleans,
requested/returned descriptors, cleanup order, memory, deadline, terminal result and
6 package-role hashes are recorded. Typical sequence STARTED1 -> BEFORE_CREATE_DEVICE2
-> BEFORE_CREATE_TEXTURE3 -> BEFORE_CREATE_SRV4 -> FINAL5. Returned fields omitted
when no result exists; no fabricated zero/empty successful descriptor.

| Result | Exact acceptance/classification |
|---|---|
| PASS | Hardware S_OK/device/context/11_0/non-software; texture S_OK+nonnull/exact11 fields; SRV S_OK+nonnull/exact4 active fields; releases/order true; memory/deadline within policy; exact identity/source/build/six independent hashes and original final receipt retrieval/photo-run association. Reason RGBA8_SRV_CREATED_DESCRIPTOR_MATCH. |
| FAILED | Normal negative API HRESULT; device/output mismatch/software adapter; S_OK+null texture/view; S_FALSE/non-S_OK success; descriptor mismatch; native exception or observed memory growth>64MiB. |
| BLOCKED | Required API/policy/classification/memory/receipt prerequisite unavailable; headroom<256MiB. Device/texture/SRV E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED map to BLOCKED, with exact returned HRESULT preserved. |
| INCONCLUSIVE | Deadline/late completion/owner close/observer failure; missing/partial/unbound final evidence or unresolved attribution. No claimed cancellation/cleanup for blocked call. |
| NOT EXECUTED | No authorized target run/evidence. Distinct from build/fixture success and runtime RUNNING checkpoints. Current hardware state. |

S_FALSE parameter-validation-only returns never count as allocation PASS, regardless of
unexpected nonnull output. Receipt structure is supplemented by independent semantic
validation; schema alone is not hardware truth. Six independently pinned role members
and hashes are in BUILD-EVIDENCE.json for future original-receipt verification.

## Observation bounds and remaining risks

Inherited10s decision deadline/30s owner window, first-terminal wins, late PASS denied.
No cancellation of blocked GPU/GetDesc/COM-release/file calls; no process/thread termination.
Startup package hashing/initial writer precedes timer arming. Writer caps128KiB and100ms
lock acquisition, finite byte-progress writes, temp/flush/close/atomic replace, no retry;
these are byte/work/lock bounds, not hard wall-time bounds on OS calls or power-loss proof.
VERIFY_BY_RETRIEVAL avoids predicting successful flush inside its own receipt bytes.

Only before/after memory samples: >=256MiB headroom, <=64MiB observed growth for PASS.
No peak/leak/repetition/resource-stress guarantee. Nominal texture data4bytes does not cap
actual driver/view allocation overhead. Inherited MessageDialog async errors are not fully
observed; platform UI is not app-owned rendering. Exception/crash/timeout can leave incomplete
telemetry; missing final receipt cannot become formal PASS. Target API/loader behavior,
startup and persistence for0.2.3.0 remain untested. No broader graphics/Minecraft conclusion.

## Build/static verification

Existing Windows MSVC14.44.35207 UWP libraries, SDK10.0.26100.0 C++/WinRT, PowerShell7,
Python3 standard library. Tool paths/hashes and all exit codes in BUILD-RECEIPT.json.
No downloads/new dependencies, certificates or console required. Clean committed checkout:

```powershell
Set-Location -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics'
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Fresh ignored output directory; app.cpp/report.cpp/probe.cpp compiled and preprocessed,
/W4 /MD /O2, UWP family, x64 AppContainer/DYNAMICBASE/NXCOMPAT. Compile/link/import/header/
MakeAppx/static audit all exit0. Seven unsafe preprocessor-only variants reject with #error.
Eleven valid synthetic contracts pass,37 malformed fixtures reject, including all texture/
SRV fields, wrong view dimension/inactive-union data, S_FALSE, null output, release order,
late/stale identity, forged payload and duplicate JSON. No native diagnostic/API executed.

11-member payload allowlist, no signature, ZIP CRC and exact stage/member bytes pass;
all blockmap64KiB/optional whole-file hashes, sizes and local header sizes pass. Assets/license
unchanged. Native import module/symbol set identical to accepted RES01a; factory/GetDesc
methods use COM vtables, not new named DLL imports. Loader closure still needs target evidence.

## Exact source changes from RES01a

SOURCE-DIFF.patch contains the full comparison, digest in BUILD-EVIDENCE.json.

| File under diagnostics/NativeCapabilities | Runtime-relevant change |
|---|---|
| src/probe.cpp | Add explicit SRV factory/descriptor serializer/equality, safe active-union handling, checkpoint, HRESULT/pointer/output/cleanup markers and failure/late paths; call only after accepted texture check. Device/texture inputs and memory policy retained. |
| src/report.cpp | Version guard0.2.3.0, schema v4, frozen RES01a reference, SRV01 profile hash path/current-run filename. Writer/locking/deadline unchanged. |
| src/app.cpp | Case/version/title and scope text only; activation, one-shot dispatch, MTA and observer scheduling unchanged. |
| include/native.h | Single case constant SRV01. |
| include/build_config.h | SRV01 macro, old HW/FMT/RES macros forbidden; native/Java locks retained. |
| package/Package.appxmanifest | Version/display/description; no identity/entrypoint/capability/dependency/platform changes. |
| profiles/D06-SRV01.json | Replace RES01a profile, add exact SRV descriptor/one view/cleanup order/no-binding policy; texture/device/memory/deadline limits retained. |
| contracts/native-receipt.schema.json | v4/case/version/reference, SRV checkpoint/fields/active descriptor contract. |
| native-inventory.json | Case label only, empty runtime/fixture/module lists unchanged. |
| build.ps1 | Case/profile/macro and prior-RES rejection test; same3 source units and link libraries. |
| tools/receipt_contract.py | SRV semantic validation and new original positive/negative fixtures; base structure validator retained. |
| tools/static_verify.py | Permit exactly one reviewed SRV, ban pipeline/other work, validate descriptor/cleanup structure and v4 profile/tests. |
| README.md | Scope, build, bounds and update consequences. |

Generated source/build IDs, executable/package digests and blockmap naturally differ.
No other source directory changed and no accepted output was rebuilt.
Next gate: **separate local signing-only approval**, not hardware execution.

API basis:
[CreateShaderResourceView](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createshaderresourceview)
(explicit descriptor/output vs parameter validation),
[view GetDesc](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11shaderresourceview-getdesc)
(void metadata query). No pipeline resource binding is performed.
