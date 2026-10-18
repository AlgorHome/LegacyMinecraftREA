# Phase 6B.5 roadmap — ordered, independent approval boundaries

**Current Phase6B.5a: design/static review complete; implementation NOT STARTED.**
No code, package or console changes are part of this roadmap. Dates below are not
scheduled tasks; stages occur only after their explicit scope is approved.

| Order / proposed stage | Reviewable output | Gate before any later action |
|---|---|---|
| 1 / 6B.5b | isolated NativeCapabilities project, zero-capability native-only controls, case schema/provenance, D06-HW01 only, unsigned0.2.0.0 x64 package and static/source/import audit | source/build/static approval; do not build in frozen D00 project; no diagnostic execution on Windows |
| 2 / 6B.5c | one freshly signed reviewed HW01 APPX, CMS/content/payload proof, exact signed hash and separate trust finding | exact-input signing approval; no trust-store changes or deployment |
| 3 / 6B.5d | owner installation/registration of new package identity, existing framework, no launch | one installation-only approval; preserve accepted D00 registration |
| 4 / 6B.5e | one HW01 launch and durable stage outcome within reviewed bounds | exact case/hash single-run approval, timeout/owner action plan |
| 5 / 6B.5f | scoped receipt collection and independent HW01 hardware-path assessment | read-only retrieval approval; no retry on missing evidence |
| 6 / native follow-ups | D06-A01 then FL01, RES01, P01, ERR01 in small separate builds/runs | each case source/build review, signing, installation, one-run/retrieval scopes separately approved; no batch sweep |
| 7 / input | IN-ENUM01 -> IN-READ01 -> optional IN-HOT01 | original native controller dispatch/focus policy review; owner interactive/disconnect consent |
| 8 / audio | AU-INIT01 then optional AU-TONE01 | API/native dependency review, then explicit low-volume playback consent; initialization success does not grant tone permission |
| 9 / lifecycle | LC-FOCUS01 -> LC-SUSP01 -> LC-REC01 | establish supported owner stimulus first; termination and later launch are explicitly separate actions, not automatic recovery |
| 10 / dependencies/resources | ND-STATIC01 can precede each build; RS-OBS01 then RS-ALLOC01 and ND-LOAD01 in independent cases | original sentinel code/static closure approval before any loading; no third-party executable acquisition |
| deferred | D06-SW01 optional separate control; broader renderer/GL/Java/JNI research | no software fallback substituted for Xbox hardware PASS; entirely separate future scopes |

Do not interpret order as authorization to proceed. Stop after each acceptance/
failure report. An observed failure may justify another one-variable proposal;
never silently patch, re-sign, reinstall or re-run. Missing API/device/receipts
can keep a case BLOCKED/INCONCLUSIVE without invalidating accepted native D00.

## Ranked risks and concrete decisions

| Rank | Risk / evidence | Design response / remaining uncertainty |
|---|---|---|
| 1 | Native driver or I/O call blocks observer's orderly completion; accepted Receipt uses synchronous writes | pre-call durable checkpoint, atomic first-result/late-PASS guard, bounded case and external owner window; cancellation/durable timeout not guaranteed. No kills or automatic retry. |
| 2 | Renderer startup masks the case or reuses its outcome | case worker/checkpoint before optional UI, own test device, distinct UI status/result fields; preserve code ownership/thread rules; HW01 is not render/present certification. |
| 3 | Incorrect new-case identity/profile/source binding | new schema and bindings, independent package bytes/role oracle plus external signed evidence index; old non-D00->S21 profile mapping must not survive. |
| 4 | Re-enabling old compile branches exposes Java dispatch | separate native-only gates and omit JNI TU/fixtures; do not disable LFD_D00_ONLY to add controller APIs; exact case allowlist and static audits. |
| 5 | Mistaking Windows UWP docs or Xbox One guidance for current Series X guarantees | public API requirements reviewed; record support failures individually and measure current memory limits; no GDK/private-API substitute or guessed budget. |
| 6 | Existing D00 reference overwritten by update or shared output | new package Name, new source/output project; frozen baseline hash inventory before/after; accepted source/version/signature/LocalState remain untouched. |
| 7 | Owner stimulus, screenshot or receipt attribution ambiguous | future UI shows case/version/run identifier; keep source/receipt/photo hashes and owner actions; account-free device observations; no fabricated run/time link. |
| 8 | Controller focus, consent/volume or lifecycle behavior changes state unexpectedly | small separate cases, B cancellation, focus gating, no microphone/vibration/pairing; explicit tone/termination approvals; no broad stress workload. |

## Recommended initial implementation scope

Approve only new-package0.2.0.0 D06-HW01 source/build/static review as described
in GRAPHICS-FIRST-EXPERIMENT.md. Freeze receipt-first optional post-case status UI
policy at implementation review. Permit no other capability case in that build.
This adds one measured hardware creation path with adapter classification and
chosen feature level, not a renderer rewrite, broad adapter sweep or runtime port.

No implementation is performed now. Any later budget/identity/capability/API
change must be disclosed and reviewed. Reusing the existing owner development
certificate in a later signing gate does not permit creating keys or changing
trust as part of source work. Installation acceptance remains separate from
activation and hardware-case acceptance.

Java21 JNI feasibility is a future independently gated research phase after native
evidence, reviewed runtime provenance/license/import closure and explicit owner
permission. Native phase PASS does not authorize Java, JIT/security probes,
Minecraft/gameplay/assets, production entitlement/authentication changes or the
56-target sweep. Do not expand this roadmap into those tasks automatically.
