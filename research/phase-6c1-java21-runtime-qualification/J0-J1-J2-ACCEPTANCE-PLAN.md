# Three separately gated experiments - preparation only

No source, fixture class, manifest, package or executable was created. Proposed new identity: AlgorHome.LegacyForge.Java21Diagnostics, publisher CN=LegacyForgeDiagnostics, x64, App Id App, own isolated LocalState. Final identity/version/manifest needs separate source approval. Accepted D00 remains native-only and unchanged; NativeDiagnostics/SRV03 are not repurposed.

## Gates applicable independently to every executable stage

1. Qualification: approve exact official runtime/member inputs and a per-case module/CRT policy after missing provenance is resolved. No Bandit code or module patch. A dependency's existence in the reference JDK does not approve packaging it.
2. Source/build: explicit diagnostic-only source and unsigned compilation approval. One case per build and one dispatch per activation. Reject incompatible case/compiler routes. Package allowlist, imports, schema, fixture oracle, all member hashes and failure paths reviewed before signing.
3. Signing: separate approval for one fresh pinned copy, integrity/payload verification; report Windows chain trust separately without changing stores.
4. Installation-only: separate owner approval, one attempt, auto launch disabled, no unapproved dependency upload. Verify exact identity; preserve old LocalState and baseline evidence.
5. One launch: separate approval with predeclared observation window; no retry. Record native control independently before unsafe runtime stage so its result survives JVM failure.
6. Retrieval: separate read-only approval, this package's existing receipt/photo only. Keep originals and independent hashes, sanitized analysis as needed.
7. Acceptance: separate offline evidence review, independent payload pins, stage statuses and run association. Cleanup/uninstall/system close actions require separate approval; no automatic termination or repairs.

## Common evidence and controls

Source/build/policy/manifest/runtime/native/module/fixture hashes, identity/version, distinct run/process UUIDs, architecture/OS context, sanitized numeric errors, per-module load/export status, monotonic elapsed, memory before/after and native-control receipt. Atomically write bounded current-run checkpoints and terminal data to own LocalState; cap receipt size and observed memory growth during source review. Persist bytecode/VM status separately from shutdown. Missing final retrieval never becomes PASS because UI showed success.

Use a worker thread with reviewed stack; preserve UWP UI startup independently. Proposed observation caps: J0/J1 each10s, J2 execution30s with a separately reported shutdown observation window. These are design budgets, not hard OS-call cancellation guarantees. Proposed J2 heap initial16MiB/max64MiB, direct-memory cap16MiB, no large arrays; tune only before approval and bind options hash. Total VM/native memory can exceed heap, so measure actual budget/headroom rather than assuming those numbers guarantee fit.

No harness/fixture network calls, account access, child-process spawning, JVM agents, arbitrary native plugins, game files, loaders, UI rendering or unnecessary filesystem mutations. No Xbox network/config changes implied. Runtime imports may include unused facilities; that risk must be reviewed explicitly. Logs contain no tokens, environment dumps or user account identifiers.

## J0 - package-native loading only

Question: can the exact reviewed runtime subset load and resolve its exported invocation entry points under package policy?

- Freeze an explicit module allowlist first. Candidate JVM imports prove CRT needs; JLI/java/net are not automatically preloads. Review app-local CRT versus framework and required forwarders/system APIs. A43-node static overapproximation is not an allowlist.
- Proposed route: one package-relative reviewed LoadPackagedLibrary path sequence, no absolute/PATH/cwd fallback. Exactly one attempt per approved module; load DLL initialization is execution and requires launch approval.
- Observe return handles/errors and three export addresses as present/absent booleans, not raw addresses in exported receipt. No JNI function invocation, VM creation, java.exe or game main.
- Release owned module handles in reverse reviewed order only with no VM created. Record cleanup; loader DLL teardown can also block.

PASS: all mandatory approved loads/exports, identity, memory/time and terminal persistence satisfy policy. FAILED: attempted mandatory load/export or observed policy violation negative. BLOCKED: missing input/license/allowlist/framework/approval. INCONCLUSIVE: crash/hang/partial attribution or missing final receipt. Native control can PASS independently when J0 fails. No JVM-execution claim.

## J1 - invocation query only

Question: does one explicit version request succeed for this runtime?

- Inherit accepted exact J0 modules. One query profile per cold activation; call JNI_GetDefaultJavaVMInitArgs once with JNI21. Portable JNI1_8 control is a distinct approved build/profile/activation; no fallback loop.
- Bind request constant/args schema, numeric result and returned fields to runtime/profile. No CreateJavaVM, Java execution, enumerating unrelated processes or account access.
- JNI_GetCreatedJavaVMs exists but is not needed for the first default-args query; don't add it merely because exported.

PASS: intended positive query returns JNI_OK and valid documented output. FAILED: positive request explicitly rejected or inconsistent output. BLOCKED: J0/input/approval missing. INCONCLUSIVE: hung call or incomplete evidence. An expected negative profile has its own oracle and cannot satisfy the positive VM gate.

## J2 - original Java execution, interpreter first

Question: can one actual VM execute a small original deterministic method?

- New cold process, one JNI_CreateJavaVM call and no recreate/fallback. JNI21 request and frozen minimal options including -Xint, reviewed class path and memory caps. No Bandit module/filesystem/AWT/security patches copied.
- Original fixture specification for later source approval: a fixed bounded loop over constant integer inputs, defined arithmetic/checksum and fixed expected result independently computed by the verifier; return an integer/short string to native caller. No class/source or compiled fixture exists from this phase.
- Require JNI_OK, nonnull VM/JNIEnv, actual runtime Java major/vendor and JNI version, correct class/method signature and return, no unexpected pending exception. Check exceptions after lookup/call; do not clear unknown exceptions to manufacture success.
- Release JNI local refs and record teardown separately. If DestroyJavaVM is part of approved cleanup policy, checkpoint before it, require actual returned JNI status for cleanup PASS. If it blocks, preserve earlier bytecode PASS as a subresult but overall cleanup/acceptance INCONCLUSIVE. Never FreeLibrary while VM/threads remain alive; no forced unrelated-process kill.

PASS: native control, VM creation/runtime identity, fixture oracle, exception and declared cleanup/time/memory/persistence all pass independently pinned inputs. FAILED: completed wrong result/runtime, VM error/null output or unexpected exception. BLOCKED: mandatory runtime/input/preceding approval missing. INCONCLUSIVE: crash/hang/unfinished cleanup or missing attributable terminal bytes. NOT EXECUTED for unrun stages. Interpreted bytecode success proves neither JIT nor Minecraft.

## Current status

J0/J1/J2 all NOT EXECUTED and execution preparation BLOCKED at missing full provenance/exact packaging policy; no source/build approval exists. Unknown Xbox API compatibility is the question for a future controlled J0, not a circular requirement to prove runtime success before designing that test. Each later negative result must remain visible, without security-policy workarounds.
