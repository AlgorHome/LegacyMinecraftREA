# Native diagnostics safety, evidence and acceptance contracts

All controls below are proposed requirements for a NEW project; they are not
implemented or hardware-tested by this documentation phase. Accepted D00 source,
schema, package, receipt and photograph remain immutable reference evidence.

## Outcomes for every matrix case

| Status | Required interpretation |
|---|---|
| NOT EXECUTED | no approved case attempt; current state of every Phase6B.5 case |
| BLOCKED | declared entry condition, consent, supported API, device or evidence prerequisite unavailable; record precise missing input |
| FAILED | an exercised operation on the required supported path violated its stated oracle; retain original numeric HRESULT/Win32 code |
| INCONCLUSIVE | native call/I/O timeout, owner cancellation, interruption, lost observations or evidence insufficient to decide |
| PASS | case-specific oracle, time/resource policy, provenance and durable validated terminal evidence all satisfied; scope never expands to other cases |

RUNNING is an intermediate receipt state only, not acceptance. A detached process
or missing receipt has UNKNOWN completion and an INCONCLUSIVE review, not PASS.
OS-scheduled suspend/termination is a stimulus for lifecycle cases only; in an
unrelated case it interrupts the run. An expected negative API rejection can PASS
only that explicitly named negative contract; it does not mean a capability works.

## New native receipt design, no mutation of v1

Propose schema legacyforge-native-capability-receipt-v1, separate namespace and
directory LocalState/NativeCapabilityReceipts. Cases follow the matrix allowlist;
native-only schema has no S21 case and no Java fields that enable dispatch.
Retain explicit java_jni_enabled=false and minecraft_or_gameplay_tested=false.

Required typed fields: schema, case_id, policy_sha256, source_commit, source tree/
input digest, production_comparison_commit, frozen_d00_reference_commit, actual
package Name/Publisher/Version/architecture/ApplicationId, expected_identity_match,
run_id/process_instance_id, monotonic elapsed/deadline/start source, UTC event time,
sequence, stage, status/reason, terminal, fixed role hashes, native-only safety
flags and stage-specific result. Do not overload the old source_baseline field
to claim the production commit built a new diagnostic. Record actual source commit.

Role hashes: native executable, packaged manifest, source/build input inventory,
immutable case policy/profile, native payload inventory, plus each original fixture
or sentinel if that case includes it. Independent reviewer recomputes expected
hashes from the pinned package and compares receipt values. Hashing fields repeated
inside one receipt is not independent verification.

The signed APPX hash is bound by an EXTERNAL immutable evidence index: source
commit -> build ID/unsigned SHA256/member inventory -> fresh signed copy SHA256,
signer thumbprint/signature and chain results -> installation identity observation
-> run/process IDs -> retrieved original receipt SHA256 -> photo/hash/owner log.
Do not embed the final signed APPX's own hash in its payload: that is circular.
Installed extraction alone cannot reproduce the signed archive hash. Runtime
receipt references the prepackaging build ID/input digest; the external index
performs the archive-to-run join. No final signed hash is invented at design time.

Validate the new schema and all implementation-specific oracles independently.
Persist original downloaded JSON untouched; parse/redact copies. UUIDs are random
technical run identifiers, never hardware/account identities. Record only fixed
enums/numerics/HRESULTs and package-relative roles. No exception text, absolute
user paths, environment, user-association/device IDs, network addresses, keys,
tokens, microphone or unrelated process/file data in receipts.

## Durable observations and timeout behavior

Create run/binding and commit BEFORE_CASE checkpoint before the first risky call.
Each stage appends a bounded evidence item or replaces the case file atomically
with increasing sequence; no unbounded logging. First terminal outcome is immutable.
Late completion cannot change INCONCLUSIVE/timeout to PASS for ANY native case.
Before UI claims saved PASS, terminal persistence must succeed and be readable;
an in-memory status alone is insufficient. A separate persistence failure indicator
is visible in UI/observer output when possible; it cannot be trusted solely because
it is serialized to the same storage that is failing.

Keep WriteAtomic's fixed-size/tmp/flush/replace strategy after review, not a claim
of power-loss guarantees. Design lock ordering so UI and result ownership never
wait on potentially blocked worker/API resources. Outcome observer uses a bounded
coordinator/atomic terminal decision and never calls native-thread cancellation.
A stuck storage write can still prevent a final timeout file; checkpoint plus
owner observation remains the honest evidence. Timeout observation cannot promise
safe cancellation of driver, loader, audio or file calls. No TerminateProcess,
TerminateThread, global process kill, repeated launch or console restart.

Case technical deadlines are in the matrix. A separate owner observation window
is explicitly recorded and does not run the app watchdog while suspended. For
lifecycle tests distinguish monotonic active deadlines, OS suspension deadline and
external wall window; do not label a system-suspended worker deadlocked. Revocation,
COM release and deferral completion belong to the correct owning thread; watchers
must not release a context while its native call is outstanding.

On cancellation/failure: stop scheduling work, revoke callbacks safely, stop/close
audio graphs, unmap/release owned resources on valid paths, and preserve checkpoint/
terminal/tmp evidence. If the call never returns, report incomplete cleanup. Do
not automatically unload live modules or terminate another process. User-requested
app closure/termination and cleanup are separately approved actions; reference
D00, shared VCLibs and production data never become cleanup targets.

## Resource and user-observation controls

Budgets are per-case safety thresholds, not stress targets or proven kernel/driver
caps. Use current MemoryManager limit/usage rather than Xbox One marketing figures
or available host RAM; do not change classification or memory limits. No allocation
to exhaustion, executable-memory/JIT permission probes, GPU hang/TDR fault injection,
unbounded query loops or automatic software fallback. Preflight failure is BLOCKED.
Natural device loss is recorded with GetDeviceRemovedReason; recovery is a separate
contract, never assumed from successful re-creation.

Hardware and SOFTWARE_CONTROL outcomes use different case IDs/build policies.
No WARP pass is promoted to hardware acceptance. Render/present tests own the
new package's swapchain exclusively; UI success is a separate support observation.
Controller validation needs owner prompts, bounded polling and focus cancellation;
no account association/device serial data or vibration. Audible tone requires
explicit per-run owner consent, owner-controlled comfortable system volume and
fixed low amplitude/duration. No capture or user media access.

## Hardware acceptance and provenance limits

Independently record registration, activation, case execution, UI/physical output,
resource/cleanup observation and durable receipt retrieval. Exact source/version/
hash changes require new evidence; accepted D00 is a reference, not an automatic
prerequisite PASS for every future package. API calls can succeed without audible
or visible output. A photo without run/version/time has owner/contextual correlation
only; a raw JSON file is not cryptographic proof of Xbox origin. State those limits
without discarding valid narrow receipt evidence or inventing visual correlation.

Acceptance package should include: original receipt/hash, exact independent member
comparison, schema/oracle validation output, owner action/time record, scoped
photo where the case requires physical observation, original numeric error/stage,
cleanup outcome and explicit missing metrics. A photo should display case/version
and short run ID in future native UI. Preserve raw original privately; derivative
redactions must not change test text. No blanket 'all capabilities PASS' summary.

## Separate approval gates and blockers

1. Design acceptance then original new-project source/build/static review only.
2. Fresh-copy signing of a named unsigned hash; signature integrity and chain trust
   results separate, no certificate-trust modification implied.
3. Owner new-package installation only with auto-launch off and existing framework.
4. Owner single named-case launch with per-case stimuli, consent, deadlines and
   exact approved signed hash; no background queue or implied repeat.
5. Scoped new-package receipt/photo collection and case acceptance.
6. Next case, owner termination/relaunch lifecycle test or cleanup requires scope
   appropriate to that action. No approval for production changes or Java follows.

Current blockers for execution: new native project/schema/controls do not exist;
no native case build/signature/deployment approval; public API availability and
resource behavior beyond accepted D00 untested; owner lifecycle stimulus and audio
consent not established. These are not reasons to broaden authority or download
workarounds. All new cases remain NOT EXECUTED.
