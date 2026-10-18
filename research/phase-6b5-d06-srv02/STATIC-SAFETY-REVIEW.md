# D06-SRV02 static safety review

**PASS_STATIC_ONLY**, `c81d0f48286513f7a7579a1d2d786cca4f5e60e2`; unsigned SHA256 `88cde899358b6eaade1658802831c5a914b8e637cf1466321b233fa8a2788c31`.
Hardware **NOT EXECUTED**. Static result is not experimental backing-identity proof.

| Area | Result | Evidence |
|---|---|---|
| Baselines | PASS |175 frozen file hashes before/after,6 source refs; accepted SRV01 branch and all earlier artifacts/evidence intact |
| Scope/identity | PASS static | NativeDiagnostics0.2.4.0/x64, zero capabilities, MTA/entry point retained; one native case, no previous-case/Java dispatch |
| Compile safety | PASS |3 preprocessed units,8 unsafe configurations explicitly rejected; no JNI/Java calls/imports |
| Prerequisite graphics | PASS static | Exactly1 hardware device,1 accepted texture,1 accepted SRV, descriptors checked before backing query; no fallback/retry |
| Getter | PASS static | Exactly1 GetResource(resource.put()) with nonnull output, require nonnull ID3D11Resource; void/no fabricated HRESULT |
| Canonical identity | PASS static |2 explicit QueryInterface(__uuidof(IUnknown)) callsites, one per object; each S_OK+nonnull guarded before comparison; second query skipped after first failure/deadline |
| Pointer telemetry | PASS | Only nonnull/equality booleans; closed schema rejects raw pointer property; no arbitrary interface-pointer equality |
| Reference order | PASS static | Inner IUnknown scopes -> returned resource -> SRV -> texture/context/device; markers after scope progression; failure outputs remain scoped |
| Exclusions | PASS | No pipeline binding, shader/compiler, texel init/read, buffer/RTV/draw/clear/copy/map/readback/swapchain/presentation/software/loops/Java/Minecraft |
| Reporting | PASS with limits | v5/6 roles/UUIDs/FINAL6, 128KiB/100ms lock/temp-flush-atomic write; not hard OS-call timeout or power-loss guarantee |
| Timing/memory | PASS static |10s first-terminal/late-PASS guard;256MiB headroom/64MiB observed growth; no cancellation/driver cap/leak proof |
| Contracts | PASS offline |15 valid/53 invalid receipts; absent/failed/null identities never become equal-as-PASS, cleanup errors and fabricated HRESULT/address rejected |
| Package/dependencies | PASS |11 files plus unsigned metadata, ZIP/blockmap/stage checks; original modules/imports/libraries/dependencies retained; target loader closure pending |
| Signing/device use | NOT EXECUTED | No certificate/trust/device operation, deployment or target launch |

Failure-path review:

- Identity/hash/initial write can fail before observer; no original final means no acceptance.
- Device/classification/memory/checkpoint/texture/SRV descriptor failures stop before getter;
  no software fallback or repair. Getter checkpoint/deadline guards prevent late dispatch.
- GetResource null: FAILED, no QI/comparison. Temporary empty owning scopes may complete;
  release markers alone do not claim a resource existed. No invented getter HRESULT.
- First QI error/non-S_OK/null output: FAILED, second skipped. Second QI error/non-S_OK/null:
  FAILED, no comparison. Unexpected nonnull error outputs still released by com_ptr.
- Both S_OK+nonnull: only then compare canonical IUnknowns; unequal -> FAILED. Do not compare
  two null outputs, texture-vs-resource interface pointers or expose raw addresses.
- Temporary QI refs always scope before returned resource while SRV/texture still held.
  Successful QI/GetResource add references; each com_ptr releases its own reference even
  when canonical identity is the same. No double-release/manual Release mixed with com_ptr.
- Observer can win during Getter/QI/Release; late worker cannot overwrite terminal with PASS.
  A blocked call/crash/SEH may prevent cleanup/final telemetry. No cancellation/termination.
- Receipt I/O pending/error: in-memory/UI PASS insufficient; later original receipt needed.
  Exceptions unwind C++ scopes where possible, but partial data may be lost. No relaunch repair.

Inherited risks: startup hashing/write before timer, native/file calls may block; no strict
allocation cap, peak/leak proof, full loader/API closure or MessageDialog async-error coverage.
System helper LoadLibraryExW/GetProcAddress imports retained, no Java/third-party module route
or binary bundled. Platform dialog is not renderer/presentation validation. All runtime/driver
and persistence conclusions await separately authorized hardware evidence.

BUILD-EVIDENCE.json, STATIC-VERIFICATION.json, BUILD-RECEIPT.json, SOURCE-DIFF.patch and
`C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-192156-1c3f66cf\logs` hold exact supporting records.
