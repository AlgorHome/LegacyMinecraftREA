# Static safety review — D06-HW01 only

Review against accepted553c655 and Phase6B.5b authorization. No target program was
executed to test any path; source/control-flow and package bytes are the evidence.

| Requirement | Verdict | Supporting evidence |
|---|---|---|
| Frozen production/D00 unchanged | PASS static preservation | all Git diffs confined to new diagnostics/NativeCapabilities; original artifacts/source hashes compared with Phase6B.5a frozen index |
| Separate UWP identity / isolated data | PASS static | manifest exact NativeDiagnostics0.2.0.0/x64/App/new EntryPoint; report.cpp uses this package's ApplicationData.LocalFolder/NativeCapabilityReceipts |
| MTA startup | PASS static | src/app.cpp wWinMain and each worker use multi_threaded; view-provider uses CoreApplication::Run |
| Exactly one case/no unknown dispatch | PASS static | fixed compile macros, build ValidateSet, three exact native TUs; first valid activation only; invalid case/kind rejects before Start; no follow-on callback/test action |
| No Java/JNI/proprietary/auth payload | PASS static | no jni TU/header/fixtures/runtime inputs; input manifest and preprocessed outputs audited; imports and exact11-member payload allowlist checked |
| Compile-time rejection controls | PASS compiler-only | COMPILE-GATE-CHECKS.json: default config preprocesses successfully; JNI enabled, native-only disabled, inherited D00 disabled and case disabled each fail with the intended #error; no produced code executed |
| HW request vs adapter observation | PASS static | src/probe.cpp records driver enum/flags and creation HRESULT separately from adapter Flags; no device names/LUID; unavailable classification BLOCKED |
| No software fallback / broad sweep | PASS static | one D3D11CreateDevice call site, HW+11_0 only, no WARP/REFERENCE retries, no additional test code |
| No app-owned rendering | PASS static | no swapchain/render-target/texture/present calls, no presentation loop; platform MessageDialog status only |
| Resource release/budgets | PASS source contract | com_ptr lexical ownership; fixed memory pre/post guards; one device; no explicit GPU resources; driver/internal allocation cannot be hard-capped |
| Timeout | PASS static, runtime unknown | observer/first-terminal/late-PASS guard; no cancel-native/Terminate* imports;100ms lock bound; native/storage calls themselves not bounded/cancelled |
| Payload/source provenance | PASS static | clean commit, generated compile-time commit/build header, native-inputs records all package/source hashes; static ZIP bytes match verified stage |
| Manifest capabilities/dependencies | PASS static | zero capabilities; reviewed VCLibs declaration; no identity/capability sharing with production |
| Native imports/CRT exports | PASS for static coverage only | full modules/symbols in STATIC-ARTIFACT-EVIDENCE;19 direct CRT exports found in hash-pinned Microsoft x64 UWP reference package; installed console bytes/system API sets not resolved |
| Receipt schema/identity | PASS structural review | exact schema copy, local $refs/required fields checked; one case/version/native-only flags; no actual receipt generated |
| Signing/install/launch | NOT EXECUTED | no authorization or commands for any of these actions |

## Failure/race paths reviewed

- Unknown activation: Show fixed BLOCKED notice, no Start/worker/device. Repeated
  activation cannot run a second case because started is set first.
- Receipt constructor/binding/hash/identity/directory failure: startup catch displays
  INCONCLUSIVE without a saved-PASS claim. Failure before a receipt exists cannot
  manufacture durable evidence; no driver is called.
- Initial STARTED write failure: no workers/device. BEFORE_CREATE_DEVICE write failure:
  BLOCKED terminal attempt, no device. Synchronous writes may hang; observer/owner
  limit is honest about incomplete final evidence.
- Native call error: exact HRESULT retained, supported policy/API failure BLOCKED,
  unexpected supported-path error FAILED. S_OK alone is insufficient: require
  outputs11_0, adapter SOFTWARE clear, cleanup/memory oracle and saved final evidence.
- Device call hangs: observer can choose INCONCLUSIVE and write final if storage is
  available; no method kills the native thread. Device worker/context remain until
  call returns or owner closes the specific app under later approval.
- Device call returns late: terminal guard prevents overwrite; late PASS denied even
  if the observer was delayed. Returned HRESULT can become available in UI state
  but cannot replace an earlier terminal receipt.
- Checkpoint writer and timeout overlap: I/O mutex serializes bytes; timeout has
  bounded lock wait. A running checkpoint's later completion cannot overwrite the
  terminal persistence error. Snapshot reports IO_PENDING until terminal write
  attempt settles, preventing a prior checkpoint success from claiming FINAL saved.
- Final write failure: in-memory decision may exist, but UI reports not confirmed/
  numeric error. VERIFY_BY_RETRIEVAL inside candidate JSON does not self-certify it.
- Exception after acquired COM pointers: lexical RAII releases them; FAILED exception
  HRESULT (where caught) or fixed unknown-error reason. No arbitrary exception text.
- UI/dialog unavailable: best-effort title; does not force a renderer, case retry,
  capability addition or altered hardware receipt. UI support remains untested.
- Owner closes window: observer may mark interrupted INCONCLUSIVE; process exit may
  prevent final storage. No forced global process termination or automatic relaunch.

## Limits and decisions needing later evidence

Static review does not prove thread scheduling, native-API availability, disk
failure handling, modal UI/controller interaction, power-loss durability or
transitive Xbox import closure. No dynamic fault injection/test executable ran.
UI text may be constrained by the platform dialog; first hardware approval should
separate UI availability from device and receipt result. Hardware API behavior
and actual driver memory are unknown. No claim of full D06 graphics certification.

Existing Microsoft framework reference was read as ZIP/PE bytes only, not loaded
or installed. All direct required CRT exports are present there, but that does not
prove the exact console framework/system export graph. No extra DLL download or
dependency installation is proposed automatically. No capability addition blocker
was discovered; any future request for one needs separate source review.

Formal verdict: **PASS_STATIC_ONLY** for authorized build/package/source safety;
hardware compatibility and execution acceptance **NOT EXECUTED**.
