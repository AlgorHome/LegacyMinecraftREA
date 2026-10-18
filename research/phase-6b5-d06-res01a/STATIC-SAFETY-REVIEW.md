# D06-RES01a static safety review

**PASS_STATIC_ONLY** at `4457142ff1fd9e01371eb446612c70162ce93357`. Unsigned SHA256 `526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8`.
Hardware **NOT EXECUTED**; this verdict is not texture-allocation success on Xbox.

| Requirement | Result | Supporting evidence |
|---|---|---|
| Preserve baselines | PASS |107 before/after hashes,4 Git refs in BASELINE-PRESERVATION.json; old FMT01 branch retained; prior builds/evidence untouched |
| Source isolation | PASS | SOURCE-DIFF.patch confined to diagnostics/NativeCapabilities; separate research branch |
| Identity/startup | PASS static |0.2.2.0/x64, MTA, corrected entry point, same separate diagnostic identity, zero capabilities; later update replaces0.2.1.0 |
| Single native case | PASS | Old arguments rejected pre-dispatch; one-shot activation; six bad compiler configurations rejected, no Java symbols in3 preprocessed units |
| Device path | PASS static | One HARDWARE/11_0/BGRA device call, original adapter classification; no retry/fallback |
| Texture scope | PASS static | One CreateTexture2D callsite, null initial data and nonnull output storage, fixed1x1 descriptor; no GPU work loops |
| Descriptor check | PASS static | S_OK+nonnull gate before one GetDesc; all11 fields serialized/compared explicitly, no padding comparison |
| S_FALSE | PASS oracle | Non-S_OK success maps FAILED/TEXTURE_ALLOCATION_NOT_CONFIRMED, even if unexpected nonnull output; fixture cannot become PASS |
| Strict exclusions | PASS | No initialization/content reads/SRV/RTV/buffer/shader/compiler/draw/clear/copy/map/readback/swapchain/present/old format query/Java/Minecraft |
| Cleanup | PASS static | Texture scope closes on all returned-result paths, including failure with nonnull output; device/context/adapter outer scopes retained; flags emitted after scopes, no guarantee after crash/hang |
| Reporting bounds | PASS with limits |128KiB,100ms I/O lock, finite byte progress, atomic temp/flush/rename; not a hard timeout for OS I/O or startup hash reads |
| Watchdog | PASS static |10s first-terminal/late-PASS guard; cannot cancel a native GPU/GetDesc/release/file call; no other process affected |
| Memory | PASS static | Before/after AppMemoryUsage/Limit; >=256MiB headroom and<=64MiB growth required; no peak/driver-overhead/leak guarantee |
| Receipt binding | PASS static | Schema v3, RES01a version, source/build/frozen refs/run/process IDs, six roles, BEFORE_CREATE_TEXTURE checkpoint |
| Synthetic contracts | PASS offline |8 valid/30 invalid; per-field mismatch, null result, S_FALSE, release, time/identity/binding errors covered; no C++ execution |
| Package | PASS |11 original payload files plus expected unsigned metadata; no third-party runtime/fixture or signature; all ZIP/member/blockmap/file/header checks |
| Imports/dependencies | PASS static | AMD64/AppContainer; same module/symbol set and manifest dependencies as FMT01, no delay/JVM/compiler/GL DLL; target closure remains untested |
| Signing/deployment/hardware | NOT EXECUTED | No certificate/trust/device access, installation, launch or target loading |

## Failure-path review

- Missing identity/package hashes/initial writer: constructor/startup may only produce a
  UI warning, not a receipt; no saved PASS claim. Missing original evidence remains inconclusive.
- Memory/classification/receipt prerequisite fails: stop before texture call; device refs
  release if already created. No WARP/retry or framework/trust repair.
- Before-create checkpoint fails/deadline wins: texture not attempted; absence of texture
  HRESULT/returned descriptor is intentional, not zero success.
- Creation S_OK/null: FAILED, no dereference/GetDesc. Negative policy/API HRESULT: BLOCKED;
  ordinary error: FAILED. S_FALSE: FAILED. Any unexpected nonnull output still scoped/released.
- Valid pointer: one void GetDesc; all-field mismatch FAILED. No content read. Returned
  descriptors and sanitized HRESULTs retained; pointer addresses never recorded.
- Deadline/owner-close observer can win during calls; late completion cannot overwrite
  terminal decision with PASS. Observer receipt may have empty details and no cleanup proof.
- Exceptions release C++ scopes where unwinding occurs but generic exception receipt may
  lack partial detail. A crash/SEH/blocked release is not guaranteed to produce final evidence.
- Final writer blocked/fails: in-memory/UI PASS is insufficient; preserve final/checkpoint/
  temporary bytes after a separately authorized retrieval, no relaunch to repair.

Inherited MessageDialog async failures are not fully observed. Startup hashing/write precede
10s arming. OS I/O/driver calls remain noncancellable, and no strict GPU memory cap is claimed.
Inherited runtime helper imports include LoadLibraryExW/GetProcAddress; no diagnostic path
selects an external Java/proprietary module and no such module is bundled. Import equality
is not a proof of complete Xbox loader closure. Native and UI behavior remain untested.

See BUILD-EVIDENCE.json, STATIC-VERIFICATION.json, BUILD-RECEIPT.json and full SOURCE-DIFF.patch.
Actual compiler/preprocessor/package logs: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-183031-15ba7835\logs`.
