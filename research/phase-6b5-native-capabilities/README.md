# Phase 6B.5a — Xbox native capability validation design

2026-10-17, America/Chicago. **Documentation/static source review only.** Every
new case is NOT EXECUTED. No implementation, compilation, signing, installation,
console access or diagnostic execution is authorized by this dossier.

## Frozen reference

| Reference | Exact value |
|---|---|
| Production comparison | d1453434ceefe73bef5aff497194e09f39dde7e1 |
| Accepted diagnostic source | 553c6554f40f1372b0ea09f6badbbb98e133a9ab |
| Diagnostic version | 0.1.3.0 |
| Signed APPX SHA256 | ca93ec2f10b75a7e9e87df679a2cbf5cdf84630fc94820df731e2f3759661848 |
| Receipt SHA256 | 1d247637c6551e2da289eecd3b343e0728b57aa4385a852590f61444fe888b7f |
| Original photo SHA256 | 74f383324231a453d88474ebc8a83a4ffb7c178f720c0384cbe6b8b7be8bf6fa |

All original artifact hashes were rechecked; BASELINE-PRESERVATION.json binds
their exact local paths, acceptance-report hash and diagnostic source-file hashes.
No original is altered, rebuilt in place, re-signed or replaced. The accepted
console registration/data remain untouched; their live state was not queried.

[Accepted hardware report](../../../analysis-local/phase6b4h-hardware-receipts/FINAL-ACCEPTANCE-REVIEW.md),
[original receipt](../../../analysis-local/phase6b4h-hardware-receipts/originals/D00-0799F3FD-1056-4709-9302-202AA86C4C5D.json),
[original photograph](../../../analysis-local/phase6b4h-hardware-receipts/originals/Xbox-D00-PASS.png).
These private local originals are retained outside Git. The photograph supports
D00 UI PASS; its run association is owner-attested, not a visible UUID/time match.
Accepted D00 does not certify D06 graphics, audio, input, JNI or gameplay.

## Architecture recommendation

Use a **new standalone package**, proposed Name
AlgorHome.LegacyForge.NativeDiagnostics, Publisher CN=LegacyForgeDiagnostics,
initial Version0.2.0.0, x64, Application Id App, proposed ordinary UWP EntryPoint
LegacyForgeNativeDiagnostics.App. This is a proposal, not a registered identity or
new certificate. Keep App classification and initially zero capabilities. A new
Name creates an independent package family/LocalState, preserving installed D00.
A versioned update of RuntimeDiagnostics would replace the reference registration
and retain its data; reject that option for this phase.

Future source belongs in a new diagnostics/NativeCapabilities project on a new
research branch derived from accepted553c655, never the frozen project's output
folder. Reuse reviewed source selectively with provenance/license attribution.
One allowlisted native case per build/process, no automatic sweep or queue.
Case policy is embedded and hashed; unknown dispatch is rejected before any
worker/API/test fixture is selected. No arbitrary command-line paths or profiles.

Do not set LFD_D00_ONLY=0 to obtain controller handlers. Retain LFD_D00_ONLY=1
where inherited JNI stubs depend on it; add an independent LFN_NATIVE_ONLY=1,
LFN_JNI_ENABLED=0 and exactly one LFN_CASE selection enforced with compile-time
errors. Omit jni_smoke.cpp, JNI headers, Java fixture and runtime copying entirely
from the new project. New native case code must not sit inside old S21 guards.
Preprocessed-source/import/payload audits must prove the exclusions. These controls
are proposed changes, not implemented guarantees.

## Deliverable map and scope

- [Infrastructure audit](INFRASTRUCTURE-AUDIT.md): reuse/modification/unsuitable decisions.
- [Capability matrix](CAPABILITY-MATRIX.md): individual contracts and explicit outcomes.
- [First graphics experiment](GRAPHICS-FIRST-EXPERIMENT.md): D06-HW01 device creation only.
- [Safety and acceptance](SAFETY-AND-ACCEPTANCE.md): provenance, receipts, bounds, evidence.
- [Roadmap](PHASE-6B5-ROADMAP.md): ordered independent approvals and ranked risks.

The existing Phase6B matrix D06 encompasses rendering/readback/presentation. New
D06-* cases refine it; D06-HW01 alone must never be reported as all of D06 PASS.
Native-only ND-* cases refine the old D01 loading uncertainty without Java.

All new case outcomes must distinguish PASS, FAILED, BLOCKED, INCONCLUSIVE and
NOT EXECUTED as defined in SAFETY-AND-ACCEPTANCE.md. No new hardware result exists.
No runtime downloads, proprietary launcher code, Minecraft assets, credentials,
authentication, entitlement changes or Java/JNI execution are included. No GDK/
private SDK access is assumed; public Windows UWP contracts are candidates whose
availability on this specific Series X build still requires controlled validation.

STOP after design. Suggested next authorization: source/build/static review of
new-package D06-HW01 only; signing, deployment, one execution and evidence retrieval
remain separate explicit gates.
