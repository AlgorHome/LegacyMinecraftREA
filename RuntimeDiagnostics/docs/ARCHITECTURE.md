> **Phase 6B.1a:** The default configuration is now **D00Only**. See
> [D00-only build and safety contract](D00-ONLY.md).
> Earlier Java21 instructions describe the retained Java21Smoke configuration;
> they do not authorize JNI execution and do not apply to the D00-only package.
> Historical build/status evidence below refers to f77bd4c, not the new artifact.

# Initial implementation contract

The app is an independent native x64 UWP/CoreWindow process with its own package
identity and `ApplicationData.Current.LocalFolder` storage. It has no service,
general shell, remote command channel, arbitrary DLL/JAR/classpath picker, login,
game or production profile migration. Original status rendering is UI only;
there is no D06 graphics-acceptance claim in Phase6B.1.

## Native and Java isolation

D00 creates its own run/receipt and records package/executable identities and
resource observations without touching a JVM. It must finish durably before the
Java action is enabled. S21 gets a separate receipt, dedicated worker and
watchdog. Each process permits at most one VM creation attempt. There is no
fallback JNI version, JVM unload/reload, child process or speculative production
fix. The owner must actually terminate the app before another attempt.

Checkpoint before every potentially blocking load/query/create/call. A terminal
receipt is immutable: once the deadline wins, a late worker cannot replace it
with PASS. Check terminal state between stages; a blocked call itself cannot be
cancelled safely. No `DestroyJavaVM` wait or worker join may block UI shutdown.
Durable D00 evidence survives independently where storage/process behavior permits.
Catastrophic process/OS/storage failure can still prevent a final smoke receipt;
the last checkpoint is evidence of interruption, never a pass.

Receipt I/O is synchronous under its state lock; slow/stuck storage can also delay
the watchdog's final write. This is an observation deadline, not a hard cancellation
guarantee. Independently, terminal finalization refuses S21 PASS when worker
finalization starts at or after30s even if scheduling delayed the watchdog;
receipt I/O itself can take additional time. A terminal receipt retains the
last durable checkpoint stage/details, including completed module-load results,
rather than losing that context when the deadline wins. D00 and S21 share a random
process-instance marker so ordinary reactivation cannot be mistaken for a new
process from receipt IDs alone.

## JNI oracle

Use only package-relative, hash-listed Java21 modules. Record individual load
roles and numeric Win32 results, distinguishing absent inventory/dependencies,
hash drift, policy/load failure and missing JNI exports. Win32 error126 cannot
identify a specific transitive missing DLL by itself; do not invent one.

`JNI_GetDefaultJavaVMInitArgs` and `JNI_CreateJavaVM` are separate stages. Preserve
their exact requested version and return codes. One successful query does not
establish VM creation; one non-null VM does not establish Java execution. Require
the actual synthetic fixture's expected result, observed Java major21 and the
defined JNI/native result. Exceptions are classified and cleared using fixed
codes, never `ExceptionDescribe` or raw Java stack dumps. This is a synthetic
invocation test, not JIT evidence or complete JNI ABI/native-library coverage.

The production comparison block is
`MC.Xbox/launch/minecraft_launch.cpp:1352–1363`, approved commit
`d1453434ceefe73bef5aff497194e09f39dde7e1`. It assigns `JNI_VERSION_21` and calls
the resolved `JNI_CreateJavaVM` export. This independent smoke deliberately tests
that request rather than modifying production code or claiming an older-runtime
failure. Java17/8/25 comparisons are deferred.

## Reporting

Receipts retain source baseline, diagnostic identity, unique diagnostic run marker,
case/status/stage, technical artifact hashes, numeric errors, measurements and
monotonic elapsed time. Missing observations stay absent/null or explicitly
unavailable, not invented zeros. Resource observation failures remain separate
from measured zero. Temporary checkpoint writes are flushed and promoted within
the same owned result directory; persistence failure prevents claiming a durable
PASS. This is not a promise of power-loss durability under every storage failure.

Only fixed technical enum strings, package identities, role names, numeric results
and hashes enter public-facing JSON. Do not add exception text, environment maps,
user paths, command lines, tokens, device identifiers or arbitrary Java properties.
JSON receipts and owner-reviewed attachments still need manual privacy review.
Build/source/package hashes bind content; they do not prove observer truth.

The structural contract is [receipt.schema.json](../contracts/receipt.schema.json).
It documents actual serializer keys but does not replace owner evidence review or
constitute a tested receipt validator. No runtime receipts were produced during
implementation. Private JVM fatal-error logs, if any future runtime creates them,
stay in this diagnostic app's owned directory and are not included in exports.

Package activation, native-control result, runtime-availability decision and
Java21 result are distinct. A missing approved runtime is BLOCKED. A rejected
required JNI request or wrong synthetic result is FAILED. A deadline or incomplete
observation is INCONCLUSIVE. PASS is limited to the exact observed scenario.

Primary contracts: [LoadPackagedLibrary](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-loadpackagedlibrary)
and [Java21 JNI Invocation API](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/invocation.html).
Actual Series X behavior remains untested until separately approved execution.
