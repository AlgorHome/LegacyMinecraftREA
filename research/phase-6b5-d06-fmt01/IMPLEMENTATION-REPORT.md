# Phase 6B.5e — D06-FMT01 implementation

**PASS_STATIC_ONLY. x64 compilation and unsigned APPX packaging passed. No target execution.**
Source commit: `bbe3a42c422e4328d5f98c07a9370fa948d0cbbf` on `research/phase6b5e-d06-fmt01`.
Accepted parent experiment: `a3f72874241914f6048d4ca9ec4fc0edc978625d`.
Build: `20261017-180047-9ad3700d`.
Unsigned APPX: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-180047-9ad3700d\NativeCapabilities.unsigned.appx`.
SHA-256: **24dc6835408f9a5d38d1ab56ec82dfd550cf0dc183e495defa836299d77dd03d**.

## Scope and preserved evidence

Before any diagnostic source edit, 35 pinned local files were rehashed, including
accepted D00 signed APPX `ca93ec2f10b75a7e9e87df679a2cbf5cdf84630fc94820df731e2f3759661848`,
accepted HW01 signed APPX `d4629d1f494f73db7dcb6290bee8c5c9f28375c8630c531e58b3ee95a6f05908`,
and HW01 receipt `14d609bddfe39019ed4808a23190319895a4b9d4d7117eb072c6f74014a49bc7`.
The same files match after the build. BASELINE-REVALIDATION.json records paths/hashes.
Production reference `d1453434ceefe73bef5aff497194e09f39dde7e1` and accepted D00 source
`553c6554f40f1372b0ea09f6badbbb98e133a9ab` remain available as Git objects.
All source differences are confined to diagnostics/NativeCapabilities. Accepted
HW01 branch/commit and ignored earlier outputs are retained; no prior artifact was overwritten.
No installed application, LocalState, dependency, certificate or console was accessed/changed.

## Identity and future replacement consequence

Name `AlgorHome.LegacyForge.NativeDiagnostics`; publisher `CN=LegacyForgeDiagnostics`;
version **0.2.1.0**, x64; application Id `App`; entry point
`LegacyForgeNativeDiagnostics.App`; MTA preserved; zero declared capabilities.
Xbox classification **App is required at future owner inventory**; this host build
cannot observe or set that console field. Windows.Universal and Microsoft.VCLibs.140.00
requirements are unchanged, with no bundled framework.

This identity/version intentionally proposes an **update** of accepted NativeDiagnostics
0.2.0.0, not side-by-side installation. A later update may retain LocalState and would
replace the installed HW01 executable. Old HW01 receipts must not count as FMT01 results.
If retaining the installed 0.2.0.0 binary for independent reproducibility is necessary,
the alternative is a separately approved package name such as
`AlgorHome.LegacyForge.NativeFormatDiagnostics`, with fresh identity bindings and separate
LocalState/signing/deployment evidence. That alternative is not built or installed here.
Resolve this choice before installation; the current authorization requires no console change.
RuntimeDiagnostics 0.1.3.0 remains a separate, untouched package baseline.

## Experiment and outcome rules

One hardware D3D11CreateDevice attempt: level11_0, BGRA_SUPPORT, no alternate driver,
flags or feature retries. Query the adapter SOFTWARE flag as before. Only after a
non-software adapter is established and a BEFORE_FORMAT_QUERY checkpoint is durable,
call `ID3D11Device::CheckFormatSupport(DXGI_FORMAT_R8G8B8A8_UNORM, &formatSupport)` once.
No textures, buffers, shader/view factories, swapchain, draw, map/readback or presentation.
The device/context themselves may cause driver allocations; those cannot be strictly capped.

| Outcome | Strict rule |
|---|---|
| PASS | Identity/source/build/payload checks; S_OK hardware creation, device+context, level11_0, non-software classification; query S_OK and valid mask; TEXTURE2D + SHADER_SAMPLE + RENDER_TARGET bits all present; references released; memory/deadline policy met; original terminal receipt later retrieved and independently bound. Runtime reason RGBA8_REQUIRED_FORMAT_SUPPORT_CONFIRMED. |
| FAILED | Query S_OK with valid mask missing any required bit; unexpected device outputs/software adapter; ordinary negative creation/query HRESULT; native exception; observed memory growth >64MiB. This is failure of this case, not a conclusion about Minecraft. |
| BLOCKED | Observed memory unavailable/<256MiB headroom; receipt prerequisite/checkpoint failure; creation E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED; query E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE; unavailable DXGI classification. Preserve exact HRESULT where returned. |
| INCONCLUSIVE | Timeout/late completion/owner close/observer unavailability; query non-S_OK success code; reserved bit31/sentinel output on S_OK; missing/unreadable terminal receipt or unresolved source/payload/provenance discrepancy. Do not accept in-memory/UI PASS alone. |

Required flags: TEXTURE2D=0x20, SHADER_SAMPLE=0x200, RENDER_TARGET=0x4000;
required mask **0x4220**. MIP=0x1000 is optional, decoded whether true or false.
These are *reported support bits*, not exercised resource creation or shader sampling.
A valid S_OK zero mask records four false flags and FAILED. A failed HRESULT or invalid
mask records format_support_valid=false and **omits** raw/hex/decoded output; absence
is not zero. Sentinel0xffffffff/reserved bit31 yields INCONCLUSIVE; future flags in
reserved space require a schema/oracle review. Optional extra documented bits are retained.
Late returned data cannot override the first terminal decision.

## Exact changes from HW01

SOURCE-DIFF.patch is the complete diff against the accepted HW01 commit.

| File | Runtime-relevant change |
|---|---|
| src/probe.cpp | Format identity, required mask, attempted/valid markers; one query after classification; BEFORE_FORMAT_QUERY receipt gate; raw/hex/four decoded fields only on valid S_OK; query HRESULT and signed value; query result classification/late guard. Existing hardware creation, classification, memory observation and scoped cleanup retained. |
| src/report.cpp | Version guard0.2.1.0; receipt schema v2; frozen HW01 source field; FMT01 policy hash/path and per-run filename. Atomic writer/locking/first-terminal/deadline implementation unchanged. |
| src/app.cpp | Dialog title/case/version and scope text only. Activation dispatch, MTA, one-shot state, observer/worker scheduling unchanged. |
| include/native.h | Single allowed case constant changed to D06-FMT01. |
| include/build_config.h | FMT01-only compile macro; unsafe configurations and old HW01 macro rejected. Java/JNI remain excluded, inherited D00 lock remains1. |
| package/Package.appxmanifest | Version0.2.1.0, case display text and description; identity/publisher/entry point/platform/dependencies/capabilities unchanged. |
| profiles/D06-FMT01.json | Replaces packaged HW01 profile; adds exact format, one query, required/optional masks, invalid-output policy, no resources/shaders. Existing deadline/memory/device limits retained. |
| contracts/native-receipt.schema.json | Version2, FMT01/version/source binding, query checkpoint and typed query outputs; formatting expanded. Schema structure is supplemented by independent semantic oracle. |
| native-inventory.json | Single-case label only; empty fixtures/runtimes/extra modules remain. |
| build.ps1 | FMT01 profile/macro; five compiler-only unsafe-macro rejection checks; same three native translation units/libraries. |
| tools/static_verify.py | FMT01 identity/query/mask/no-resource checks and offline contract tests; package/import checks retained. |
| tools/receipt_contract.py | Original offline structural/semantic validator and synthetic contract checks; never packaged or executed on Xbox. |
| README.md | Scope, build, outcome, schema and update consequences. |

Generated source/build IDs, EXE bytes/hashes, native-inputs metadata, manifest/profile/schema/
inventory hashes and APPX blockmap naturally differ. Asset and license bytes are unchanged.
Native import module/symbol set is **identical** to accepted HW01. CheckFormatSupport
is a COM vtable call, so no new named DLL import is expected; source/preprocessed inspection
confirms the call, not import presence alone. No additional runtime source/production file changed.

## Reproducible build and results

Use existing Windows x64 MSVC14.44.35207 Build Tools with UWP store libraries,
Windows SDK10.0.26100.0 including C++/WinRT, PowerShell7 and Python3 standard library.
Exact tool paths and SHA256s are in BUILD-RECEIPT.json / BUILD-EVIDENCE.json.
No certificate, Java runtime, Xbox access, downloads or third-party Python package is required.
From a clean checkout at the source commit, run:

```powershell
Set-Location -LiteralPath 'C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics'
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Build insists on clean committed source and writes a fresh unique ignored out directory.
It compiles/preprocesses app/report/probe with /W4 /MD /O2 and UWP API family,
links /APPCONTAINER /DYNAMICBASE /NXCOMPAT x64, generates original PNG assets and
packages through MakeAppx. Rebuilding creates new timestamps/build IDs and need not
reproduce the identical APPX digest; verify the precise artifact above for later gates.

Final compilation, link, preprocessor, import/header analysis, MakeAppx and static-safety
commands all exit0. All five unsafe preprocessor variants exit nonzero with #error.
Seven valid synthetic receipt forms pass; eighteen malformed/unbound cases are rejected.
These are **offline oracle tests**, not native API execution. Eleven packaged payload
members match the exact allowlist; ZIP integrity and each block-map uncompressed hash/file
size pass. No signature present. Full payload/import inventory is in BUILD-EVIDENCE.json.
First build compiled/packaged but its audit rejected UWP CreateView via an overly broad
resource-view regex. Follow-up commit narrowed the audit to D3D resource view factories;
the fresh complete build passed. Earlier failed build is retained, not approved.

## Receipt persistence and remaining risks

Schema: legacyforge-native-capability-receipt-v2. Receipt:
LocalState/NativeCapabilityReceipts/D06-FMT01-<run UUID>.json; same-name .json.tmp
is a partial-file artifact. Source/build IDs, separate process/run UUIDs, expected identity,
format, returned HRESULTs/mask, six role hashes and terminal decision are bound in the file.
Normal sequence: STARTED1 -> BEFORE_CREATE_DEVICE2 -> BEFORE_FORMAT_QUERY3 -> FINAL4.
Initial checkpoint creation/hash gathering occurs before the inherited deadline is armed.

Writer caps JSON at128KiB, uses bounded-byte partial-write progress and one attempt per
checkpoint, same-directory temporary file, flush/close then atomic replacement,100ms I/O
mutex acquisition and no retry loop. Case deadline10s, owner observation30s.
These are byte/work/lock bounds, **not a hard wall-clock guarantee for OS I/O or driver calls**.
The observer cannot cancel a stuck GPU/storage call and cannot terminate other processes.
A terminal receipt can remain pending/unwritten after failure; do not accept PASS without
retrieval. VERIFY_BY_RETRIEVAL avoids predicting successful persistence from within the
bytes being written. A .tmp/checkpoint alone is not final PASS. No power-loss guarantee.

MessageDialog remains platform-rendered after the case; asynchronous UI errors are not
fully observed and do not invalidate a correct retrieved query receipt. New version has
not run; query support, startup behavior, signing/trust, loader closure and target persistence
remain **NOT EXECUTED / pending gates**. Memory observations do not prove absence of leaks.
No rendering, presentation, OpenGL, LWJGL, Java/JNI or Minecraft compatibility is established.

## Microsoft API basis

[CheckFormatSupport](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-checkformatsupport)
documents the HRESULT and ORed support mask.
[D3D11_FORMAT_SUPPORT](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ne-d3d11-d3d11_format_support)
defines the four decoded bits. Checked2026-10-17; no implication of successful drawing.

Next gate: explicit authorization for **one-copy local signing and static signature/payload
verification only**, retaining existing trust findings and no automatic device action.
