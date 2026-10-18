# Phase 6B.1 read-only safety review

Reviewed 2026-10-17 (America/Chicago). Review only; no signing, registration,
activation, diagnostic execution, deployment or Device Portal access performed.

Exact source: `f77bd4cdabb4955a95eb6b9224159604731645c7`, local branch
`research/phase6b1-runtime-diagnostics`, clean working tree. Comparison baseline:
`d1453434ceefe73bef5aff497194e09f39dde7e1`. Diff contains only 20 new text
files under `diagnostics/RuntimeDiagnostics/`. Reviewed checkout:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/phase6b1-diagnostics`.

Evidence below uses paths relative to that project directory. PASS means the
stated source/metadata property was verified, not that runtime behavior passed.
Confidence is high for direct source/ZIP observations; execution remains untested.

| Requirement | Verdict | Supporting evidence and limits |
|---|---|---|
| 1. Review exact commit | PASS | HEAD and branch verified, working tree clean; exact commit above. |
| 2. D00 has no Java, unapproved runtime load, Minecraft access or authentication | PASS | `src/app.cpp:83` StartNativeControl calls `src/native_control.cpp:6` RunNativeControl. It reads fixed diagnostic package roles, identity and own-process resources; no JNI, external content, authentication or explicit DLL loader. UI needs Windows graphics APIs and trusted Microsoft UWP CRT/framework dependencies; actual dependency resolution is untested. |
| 3. Audit capabilities, signing, separation, receipts, watchdog and errors | PASS | `package/Package.appxmanifest:5` separate name/publisher; line 7 Windows.Universal/x64 VCLibs dependency; no capabilities element. `src/report.cpp:175,246` uses this package's LocalFolder/Phase6B1Receipts. `src/report.cpp:56,262,276` flush/replace checkpoints, sticky write errors and first terminal result. `src/app.cpp:83,125` numeric HRESULT/fixed reason reporting. Signing is absent, not validated. Limits below. |
| 4. Watchdog cannot terminate unrelated processes or alter production data | PASS | `src/app.cpp:148-174` observer only sleeps, writes its own receipt and updates UI. No process termination/spawn or production data path. `src/report.cpp:251` confines receipt writes to diagnostic LocalState. This is a source finding, not a claim that arbitrary failures can never occur. |
| 5. Prepare isolated Windows D00-only procedure | PASS | D00-ONLY-PROCEDURE.md accompanies this report. Actual run BLOCKED pending explicit execution approval and environment/signing inputs. |
| 6. Identify Windows/Xbox deployment steps | PASS | Procedure covers signing, trusted x64 framework, Windows registration and owner-controlled Xbox Dev Mode deployment. Console contact/deployment remains BLOCKED. |
| 7. Minimum signing inputs without chat secrets | PASS | Procedure lists local owner-controlled signer with matching publisher, target trust, SDK tools, framework and approved artifact. No private material requested. Signing itself BLOCKED. |
| 8. Java/JNI kept explicitly disabled pending approval | FAIL | No compiled D00-only switch exists: `src/app.cpp:125,222,231,409` permits S21 after durable D00 success via Enter/controller A/click. In the exact no-runtime APPX, `src/jni_smoke.cpp:261` blocks before `LoadPackagedLibrary` at line 356 or JNI exports at lines 377-378. This prevents JNI loading in this artifact, but does not disable the S21 worker/UI. A hard D00-only gate requires a separately authorized diagnostic-source change and reviewed rebuild. No change made during this read-only review. |
| 9. No Device Portal access or console deployment | PASS | Neither performed. Official documentation was read on Microsoft Learn only. |
| 10. No production code modification | PASS | Review produced only these separate research documents; reviewed checkout remains unchanged. |

## Artifact binding

Re-read unsigned APPX as a ZIP and computed SHA256 without executing its contents:

- File: `diagnostics/RuntimeDiagnostics/out/20261017-113425-45caeffd/RuntimeDiagnostics.unsigned.appx` relative to checkout.
- SHA256: `930f6844eea2777433886d1d347b6925206d2cfd51fccf4a36b1206ab8cf9f08`.
- Packaged inventory: `available:false`, `approvedForDiagnosticPackaging:false`,
  empty runtime file list; no Runtime directory or JVM/native runtime DLLs.
- Payload has original synthetic class, diagnostic EXE/profiles/assets/license,
  inventory and packaging metadata. No Minecraft or launcher payload.
- Prior compilation evidence, not rerun here: `docs/BUILD-STATUS.md:7` and
  `docs/COMPILATION-RECEIPT.json` record native compile/link, fixture compile and
  unsigned packaging. No D00/JNI execution is inferred from compilation.

## Material limits

D00 PASS means activation prerequisites, identity and readable hashed roles;
it does not compare those hashes against an external approved allowlist. The
operator must compare receipt hashes against the approved payload. The embedded
`jvm_loaded:false` is a source assertion, not a measured module enumeration.
Native dependency closure, graphics/input/audio capability, JIT and gameplay
remain untested (`src/native_control.cpp:17-22`). UI rendering is a prerequisite,
not D06 graphics acceptance; missing guest graphics support can prevent D00.

Receipt writes use a same-directory temporary file, flush and replacement with a
128 KiB bound (`src/report.cpp:56`). They reject a reparse receipt directory and
use generated run IDs. They are not a power-loss guarantee or protection against
an already privileged adversary. Persistence failure prevents Java enablement
and must not be reported as D00 success (`src/app.cpp:55-63`). A crash before receipt
creation can leave no receipt; preserve OS activation errors rather than infer PASS.

The 30-second watchdog is S21-only, starts after its first durable checkpoint,
and is an observation deadline, not cancellation. Synchronous receipt I/O and
mutex contention can delay its report. `src/report.cpp:276-290` prevents a late
S21 PASS. D00 has no automatic 30-second watchdog: its deadline in the procedure
is manual observation only. Preserve existing receipts on hang; close only the
identified diagnostic application. Do not run broad process-kill commands.

The existing `docs/XBOX-ACCEPTANCE.md` includes Java steps and must not be used
as this run's checklist. The accompanying D00-only procedure supersedes it for
this approval scope. **Not cleared for execution under an enforced Java-disabled
requirement until requirement 8 is resolved.** No runtime components are approved.
