# Original synthetic runtime probe

`RuntimeProbe.java` is an independently written, Java8-compatible source fixture for later execution **only inside an approved isolated guest or separately approved Xbox diagnostic package**. It contains no launcher/game code and does not use network, authentication, process creation, or explicit native loading. Do not execute it on the host or through a target-bundled desktop JRE.

## Status and compilation evidence

Prepared 2026-10-17. Trusted existing Ghidra JDK21 (Adoptium21.0.12.1+1-LTS, x86_64) compiled it with `javac --release 8`; exit0, two class files, both major version52. The compiler emitted only Java8 source/target obsolescence warnings. **The probe was not run. Compilation does not pass X03, X04, or any runtime family.** Local compiled classes/receipt remain under `analysis-local/final-audit/readiness/`, outside publication.

Source SHA256: `56a6250ddf494136c6214fab269966ec2c099b60642002a28becd543ec58ddfd`.

Compiler-only reproduction from the research root, after selecting a trusted installed JDK:

```powershell
# Compile original fixture only. This command does not run RuntimeProbe.
& '<trusted-jdk>\bin\javac.exe' --release 8 -d '<separate-analyst-class-output>' .\docs\research\legacy-launcher\tests\probes\RuntimeProbe.java
```

Use an explicit new analyst output directory. Never substitute execution of the archived launcher, game, or target JRE. Compilation is an analyst-tool action and is distinct from target execution.

## Future approved execution contract

The harness supplies exactly one argument: an existing, owner-approved, app-local test root inside the confirmed guest or diagnostic package's permitted storage. The fixture rejects a nonexistent/non-directory root or a root which is itself a symlink. **Java cannot prove that the supplied root is app-local or approved**; the owner/harness must enforce that boundary. Use a private root with no concurrent untrusted writer. No personal profile, cache, credential, or user-data directory is an acceptable substitute.

Each run creates one fresh `runtime-probe-<UUID>` child using create-directory semantics. It does not reuse an existing child. All writes are restricted to this new child; files use `CREATE_NEW`. It creates a fixed synthetic payload, reads/hashes it, renames it to a nonexistent destination without replacement flags, creates a fresh ZIP once, and mounts/reads the ZIP through ZIPFS. A daemon worker must complete within a five-second join. The probe makes no delete/cleanup calls and intentionally retains its own child and created files for owner inspection. Rename necessarily changes the fixture's own directory entry and is the only requested move operation.

To preserve the no-overwrite/no-delete boundary, **ZIP creation uses `ZipOutputStream`; ZIPFS is exercised for mount/readback only**. This is a ZIP-generation/ZIPFS-read roundtrip. It does not establish ZIPFS write/update/rename/delete, jar filesystem locking, provider-internal cleanup, crash consistency, full-volume behavior, or compatibility with each game's patched ZIPFS path. A failure leaves any partially created fixture files in its owned child.

The owner records exact probe source/class hashes, runtime/package hashes, Java family, OS/build, and argument-root class without publishing the root path. On Xbox, invoke its entrypoint only through an independently approved diagnostic package/harness with the intended packaged JVM, not by changing production launch/authentication code. No such package/harness exists in the current deliverable.

## Allowlisted output and interpretation

The source emits one JSON object with schema `legacyforge-phase6a-synthetic-runtime-v1`. Values are fixed enums, booleans/null, a numeric Java major, a normalized architecture label, and the SHA256 of the fixed synthetic payload. It never prints supplied paths, usernames, property blobs, raw exception text, stack traces, tokens, or command lines. Unreached checks remain `null`; `OBSERVED_OK` means only those narrow operations returned the expected synthetic result. `CONFIGURATION_REJECTED`/`OBSERVED_FAILURE` and fixed failure codes preserve failure without exposing exception details. VM/startup/provider failures before `main` need a separate sanitized harness receipt; do not publish raw stderr.

The JSON flags are `root_validated`, `fresh_child_created`, `thread_completed`, `file_read_write_sha256`, `rename_readback`, `zip_created_once`, and `zipfs_readback`. Runtime identity is self-reported through Java properties and must be bound to independently recorded JVM/module/package hashes. The source also explicitly emits false for cleanup, JNI, native loading, graphics, input, and audio testing.

Wrap observations in `tests/result.template.json` with actual environment/artifact/criteria evidence; do not automatically promote probe output into a phase or target PASS. It supplies only a subset of X04 and a basic Java/thread observation. Missing parts of X04 remain pending.

## Required diagnostic integration still absent

- X03: actual `LoadPackagedLibrary`, JNI API/requested/accepted version, JVM creation/exception observations for current/java21/java17/legacy. This Java entrypoint cannot establish native entrypoint or JNI compatibility.
- X04: broader permitted filesystem/ZIPFS operation and failure matrix, patch activation, thread behavior under lifecycle/resource pressure.
- X05-X08: actual module dependency/symbol/native loading; graphics context/extensions/shader/draw/present; controller/keyboard/pointer/focus/disconnect; audio/device loss. The fixture does not attempt these.
- X09-X13: suspend/resume/relaunch, resources, downloads/repair/account gates, legitimate gameplay and every56-row target/UI regression. No claim of compatibility follows from compilation or this fixture.

All Windows target, Xbox, and account executions remain **BLOCKED** until an approved environment/package exists and actual owner/harness receipts are returned.
