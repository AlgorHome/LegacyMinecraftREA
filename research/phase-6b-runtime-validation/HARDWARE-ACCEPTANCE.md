# Minimal Series X acceptance — no Minecraft ownership or gameplay

This is an owner-run proposed procedure for a future reviewed diagnostic APPX. It uses only original synthetic fixtures and approved runtime/native dependencies. No Microsoft/Minecraft authentication flow, entitlement test, game/client JAR, asset pack, mod loader or network download is required. Series X Developer Mode/deployment access may require the owner's existing platform setup; that is separate from Minecraft ownership and is not performed by this plan.

## Inputs before any run

Owner explicitly approves the exact APPX/dependency hashes, separate diagnostic package identity, manifest capabilities, source revision, runtime/native provenance and intended console. Confirm real Series X, OS/build, display/controller/audio route, and permitted test actions. The owner retains signing/deployment/device credentials. No remote device discovery or automatic deployment is included. Use existing manual deployment only after approval; never update the installed production app with this package.

Start with NATIVE-CONTROL and S21 only. S21 pins one approved Java21 runtime, original Java/JNI fixture and intended GLFW/Mesa/OpenAL stack. Missing runtime/native artifacts make their cases BLOCKED; do not substitute the launcher's desktop DLLs or omit a failing backend. No all56-target run and no Java-family switching in one live process.

## Small acceptance sequence

| Step | Owner action / cases | Required result |
|---|---|---|
| 1 | Cold-start native control outside debugger: D00/D06/D10/D12 plus D01.native-sentinel, D14.native-storage and D17.native-budget subcases | Package/source/dependency identities recorded; visible known-color pattern; controller prompted transitions; generated audible PCM; owned storage hash valid; budget sampled. These native-only subcase receipts cannot pass full S21 D01/D14/D17 or imply JVM/shim loading, Java storage or VM resource evidence. |
| 2 | Cold-start S21 portable-control configuration, then close and start production-equivalent JNI21 configuration: D02/D03/D04 | Both configuration receipts show actual outcomes; required JNI21 case creates exactly one VM, reports Java21 and returns known synthetic Java/JNI values. No second-VM attempt inside the process. |
| 3 | Bounded intended execution-mode case: D05 | Runtime-native compiled-method evidence and correct checksum if claiming JIT. If observation unavailable, record JIT INCONCLUSIVE and block a full JIT-feasible claim. Interpreter success remains separate. |
| 4 | In separate clean render session, D07/D08/D09 |120presented frames with pixel oracle and owner-visible pattern; Java-to-native render returns expected result; actual GL/profile/extensions and shim discrepancies recorded. Release native-control swapchain first. |
| 5 | D10/D11/D12/D13/D14/D15 | Controller reconnect/reset; optional keyboard/pointer prompts if supplied; platform and OpenAL/JNI audio outcomes separated; synthetic storage and explicitly enumerated ZIPFS operations correct. Missing peripheral gets scoped BLOCKED, never fabricated. |
| 6 | Actual suspend/resume3times and cold relaunch3times: D16/D18; continue D17 | No stale input, stalled context/audio or lost committed fixture; valid resumed frames/audio/results; prior interrupted runs classified; no JVM reuse workaround. Actual callback/OS behavior recorded. |

Suggested owner session budget: about15–30minutes for prepared automated cases plus prompts, with explicit per-case bounds from the matrix. This is an estimate, not an observed runtime or platform limit. Do not test while production gameplay/downloads are active. Failure isolation/repeated runs require a new reviewed run record; do not erase failures.

## Acceptance decision

Return one case receipt for every D00–D18, even if BLOCKED/INCONCLUSIVE. The controller-only baseline may omit keyboard/pointer capability claims, but D11 must retain its actual status. Native-only controls do not establish S21 feasibility. The intended runtime path requires D01–D05 and D07–D09; audio requires D13 in addition to the native output control, storage requires the declared D14/D15 operations, and lifecycle/resource evidence requires D16–D18.

A discrepancy such as the known shim extension-query limitation must be recorded as a limitation or failed consumer contract. A triangle draw cannot erase it. If a required intended-path capability fails or is blocked/inconclusive, verdict is **PARTIAL / NOT YET DEMONSTRATED**, listing exact cases. **SYNTHETIC PROFILE DEMONSTRATED** is allowed only for the explicitly listed tested capability contract and exact package/runtime/native hashes. Never rename that result “Minecraft playable,” “all versions supported,” Store certification or production readiness.

Only after review of S21, propose one Java17 diagnostic followup, then Java8 if the separate legacy assessment justifies it. Runtime families and their native/options/capability changes get distinct profiles and fresh activations. Current/Java25 and real loader/gameplay work require later scope approval.

## Return package and stop conditions

Export sanitized JSON receipts, small bounded event/checkpoint data, input/hash manifest and optional owner-observed screenshot/audio confirmation. Use offline owner-controlled export; the baseline harness needs no networking permission. Export excludes account/device IDs, tokens, raw paths, raw stderr, personal typed text and signing secrets. File hashes and counts alone do not establish visible/audible behavior.

Stop on hash mismatch, unapproved capability/action, unexpected sign-in, non-diagnostic storage access, sustained unresponsive UI, uncontrolled audio volume, unexpected external process/network request or exhausted resource stop budget. Preserve the last checkpoint and classify the result. The owner decides whether to close the app or stop the overall run; no hidden worker retries or automatic console restart.

Current blockers: no approved diagnostic build/package, exact runtime/native artifacts/provenance, signing/deployment scope, new console observations or approved execution. This document records a plan, not permission or a test result.
