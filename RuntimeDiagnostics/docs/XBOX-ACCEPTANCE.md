> **Phase 6B.1a:** The default configuration is now **D00Only**. See
> [D00-only build and safety contract](D00-ONLY.md).
> Earlier Java21 instructions describe the retained Java21Smoke configuration;
> they do not authorize JNI execution and do not apply to the D00-only package.
> Historical build/status evidence below refers to f77bd4c, not the new artifact.

# Owner checklist — pending separate execution approval

No deployment, activation or binary execution was performed during implementation.
The checklist is a future procedure, not authorization.

1. Review source revision, unsigned-package/source/class hashes, manifest identity,
   dependencies and any separately approved Java21 runtime/license inventory.
   Approve signing/deployment/activation for this diagnostic package explicitly.
   Its identity must differ from `AlgorHome.LegacyForge`; retain the production
   package and data unchanged. No Device Portal credentials are requested.
2. Owner signs with a certificate matching the diagnostic manifest publisher,
   then uses the existing manual Developer Mode deployment route. Record exact
   signed APPX hash, framework dependencies, real Series X OS/build and package
   identity. Do not substitute another package's successful installation.
3. Cold-start the diagnostic app without a debugger. Confirm the original status
   UI appears, D00 finishes, and its app-local JSON receipt is present. Inspect
   package/executable identity, persistence result and resource values. A UI alone
   does not prove a durable receipt; persistence errors prevent a success claim.
4. Select the one Java21 smoke action only after durable D00 success. A default
   no-runtime package must give **BLOCKED**, not a passing JVM result. This is a
   native-control acceptance outcome only; it does not satisfy S21.
5. For a separately approved runtime-bearing package, inspect fixed-module hash
   and load results, exported JNI functions, query/creation return codes, observed
   JNI interface/Java major and expected synthetic result. A load or query success
   alone cannot pass the smoke. No second-VM retry or version fallback is allowed.
6. If the30s watchdog reports INCONCLUSIVE, preserve D00 and smoke checkpoints;
   close/terminate only the approved diagnostic app using the owner's system UI.
   A timeout is not proof the JVM was cancelled. A fresh cold process is required
   for another attempt; ordinary activation may merely reactivate a suspended app.
7. Export only reviewed diagnostic receipts via an owner-controlled local route.
   Keep free text, raw stderr, account/device identifiers, paths and credentials
   out of shared results. Record signing/package/input hashes alongside receipts.

Report D00 and S21 separately as PASS, FAILED, BLOCKED or INCONCLUSIVE, including
the declared subcase/oracle. Preserve failures and incomplete checkpoints. Never
call these results Minecraft support, gameplay, JIT feasibility, graphics/audio
validation, Store certification or readiness of another runtime/version.
