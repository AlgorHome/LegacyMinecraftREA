# D06-FMT01 static safety review

Verdict **PASS_STATIC_ONLY**, source `bbe3a42c422e4328d5f98c07a9370fa948d0cbbf`.
Unsigned APPX SHA256 `24dc6835408f9a5d38d1ab56ec82dfd550cf0dc183e495defa836299d77dd03d`. No diagnostic execution or hardware acceptance is claimed.

| Area | Verdict | Evidence |
|---|---|---|
| Accepted baselines preserved | PASS | BASELINE-REVALIDATION.json,35 exact files checked before and after; accepted HW01 Git branch retained; source diff confined to NativeCapabilities. |
| Isolated diagnostic scope | PASS | Separate production/D00 identity; NativeDiagnostics0.2.1.0 intentionally proposes replacing HW010.2.0.0 only at a later approved installation. |
| Startup/dispatch | PASS static | MTA, CoreApplication and LegacyForgeNativeDiagnostics.App unchanged; one-shot started flag, Launch only, empty or exact D06-FMT01 arguments; other case rejected before worker/device call. |
| Native-only compile lock | PASS | Three active translation units preprocessed; no Java symbols. Five unsafe configuration attempts rejected with compiler #error; LFN_CASE_D06_HW01 excluded. |
| Graphics scope | PASS static | One D3D11CreateDevice callsite; one CheckFormatSupport callsite for DXGI_FORMAT_R8G8B8A8_UNORM. No retry, WARP/reference fallback, resource/shader/view factory, draw, swapchain, readback or presentation. |
| Query validity | PASS static | UINT0xffffffff sentinel; only S_OK with bit31 clear publishes raw mask/four decoded flags. Invalid/failed output cannot become zero capabilities. |
| Oracle | PASS offline | Seven valid synthetic forms; eighteen malformed/unbound cases rejected. MIP optional; three required bits0x4220. Synthetic tests do not execute C++ or validate Xbox behavior. |
| Evidence binding | PASS static | Schema v2, source/build UUIDs and six package-member SHA256 roles; current-run FMT01 filename. Successful query adds BEFORE_FORMAT_QUERY checkpoint; expected normal terminal sequence4. |
| Receipt bounds/atomicity | PASS static with limits |128KiB byte bound,100ms mutex acquisition, partial-write progress, no retry; temp/flush/close/atomic replace. Underlying storage calls and constructor hashing have no enforced wall-time bound. No hard cancellation claim. |
| Watchdog scope | PASS static |10s decision deadline, first terminal wins, late PASS denied; no process/thread termination calls. Cannot cancel stuck native/driver/file call. |
| Cleanup/memory | PASS static | Scoped COM device/context/adapter refs; memory headroom>=256MiB, observed growth<=64MiB required for PASS. Not a proof of driver cleanup or strict allocation cap. |
| Manifest | PASS | Expected name/publisher/version/x64/App Id/entry point; zero capabilities; unchanged Windows.Universal and Microsoft.VCLibs.140.00 dependencies. Console App classification remains owner-verification gate. |
| Payload | PASS | Exact11-member allowlist plus blockmap/content-types metadata; ZIP CRC/content and64KiB block-map hashes validated. No signature, Java runtime, Minecraft content, credentials or extra DLL. |
| Native imports | PASS static with limits | Module/symbol set unchanged from HW01. PE AMD64/AppContainer/Windows GUI; no delay imports, Java/GL/compiler module. COM query does not have a named DLL import. Complete target loader closure not proven. |
| Signing/deployment/execution | NOT EXECUTED | No certificate/trust/console access. No target code or framework installed/loaded. |

Import helpers include inherited GetProcAddress/LoadLibraryExW/FreeLibrary through
system/runtime support; their presence is not falsely described as impossible dynamic
loading. No diagnostic source path selects an external Java/proprietary module, and the
package contains no extra executable module. Windows runtime/CRT imports remain external.

Risks requiring later evidence: a query may fail/hang on the target; OS I/O can block;
startup package hashing/initial write precede timer arming; observer may report a deadline
without final durable detail/cleanup; device/resource absence is not guaranteed by an
exception receipt. MessageDialog asynchronous errors are not fully observed. Platform UI
appearance is not app-render/presentation certification. Raw receipt origin and clocks are
not cryptographically attested; require independent pinned hashes and owner-correlated run.

An in-memory PASS with receipt I/O pending/failure is not formal acceptance. Missing evidence
is BLOCKED/INCONCLUSIVE as specified in HARDWARE-ACCEPTANCE-PLAN.md. Do not relaunch to repair it.

Detailed artifacts: STATIC-VERIFICATION.json, BUILD-RECEIPT.json, BUILD-EVIDENCE.json,
SOURCE-DIFF.patch; actual logs under `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-180047-9ad3700d\logs`.
The first build's false-positive audit and the corrected clean rebuild are recorded in
BUILD-EVIDENCE.json. No failed intermediate artifact is approved for later signing.
