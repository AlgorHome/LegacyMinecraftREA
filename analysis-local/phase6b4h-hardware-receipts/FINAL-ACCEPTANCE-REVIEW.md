# Phase 6B.4 — Xbox D00 hardware acceptance review

2026-10-17, America/Chicago. **Xbox native D00 hardware acceptance PASS.**
The original receipt/build comparison passed and the owner-supplied hardware
photograph now supports the observed D00 UI PASS. Photo-to-receipt association
is contextual and owner-attested; the image does not display a run ID or timestamp.
No new hardware run was needed or performed by Codex.

This review supersedes ACCEPTANCE-STATUS.md's earlier missing-receipt status.

## Original receipt preservation

Located owner-provided file:
`C:/Users/arinze/Desktop/D00-0799F3FD-1056-4709-9302-202AA86C4C5D.json`.
Original left unchanged; byte-identical preserved copy in originals/ under the
same filename. SHA256 independently recomputed and matched owner reference:
**1d247637c6551e2da289eecd3b343e0728b57aa4385a852590f61444fe888b7f**.
Reviewed derivative in sanitized/ contains the same bytes: no personal account,
device/network identifier appears in this fixed technical receipt, so no invented
redaction was needed. Technical random run/process UUIDs are retained for binding.
File-size/download times on the PC are not substituted for missing remote listing
metadata. Xbox retrieval provenance is owner-attested; JSON is not itself signed.

## Receipt checks

| Check | Result |
|---|---|
| Schema | PASS, legacyforge-phase6b1-runtime-receipt-v1 |
| Case/version | D00 / 0.1.3.0 |
| Status/stage/terminal | PASS / FINAL / true |
| Reason | D00_ACTIVATED_HASHES_RECORDED |
| Package role | INDEPENDENT_RUNTIME_DIAGNOSTICS |
| Expected package identity | true in both binding and details |
| Source baseline | d1453434ceefe73bef5aff497194e09f39dde7e1 |
| Run UUID | 0799F3FD-1056-4709-9302-202AA86C4C5D, matches filename |
| Process UUID | 4ED596EB-3A90-4202-BEB3-3A18F8957218, valid UUID |
| Timestamp | 2026-10-17T19:33:43.607Z / 14:33:43.607 CDT |
| Sequence/elapsed | 2 / 31ms; consistent with one checkpoint then FINAL |
| Prior durable checkpoint | D00_ACTIVATION_STARTED |
| Required role completeness | true, all five hashes complete/matched |
| Java/JVM | jvm_loaded=false, including checkpoint |
| Gameplay/authentication modification | both false |

verify_receipt.py validates every assertion/type/format/pattern/additional-property
keyword used by the pinned schema with a local standard-library validator. No
dependency installation was performed. Pinned schema hash:
b73b2822e9b19799e1935bc9f6af12fc2a7b77598c87523e9c44aa44a12c3790.
Sequence2 and the embedded checkpoint are internally consistent; earlier physical
checkpoint file versions were not separately obtained. Console clock accuracy or
cross-device synchronization is not established by this timestamp.

## Independent payload comparison — all five PASS

The approved unsigned0.1.3.0 APPX was freshly rehashed as
0595e9936aa4091ebdcce3e23b4e43fdba014d88267b4aaa0656fbd9cddb307e.
Its members were independently hashed again, then compared with BOTH receipt
identities and details.role_hashes. No receipt-supplied value was used as the
expected build hash. Source build553c6554f40f1372b0ea09f6badbbb98e133a9ab.

| Role | Independently expected SHA256, matched |
|---|---|
| diagnostic_exe_sha256 | 89997350241657405fc38e596788c91b45c9e5978288d066ece51e3f42a4a6b9 |
| package_manifest_sha256 | 68e2b1a0a418593f6c768d5c4df044574e36b876276903c684eb18fe6a18065a |
| input_manifest_sha256 | b53990c9ef4c4211d7c88c33b547b043ec14bef8258b2089dd29e5ad0c102404 |
| runtime_inventory_sha256 | a847983740065493a4e5e106aada42b355f7d1b5955cedc39dd5bf36649915c1 |
| profile_sha256 | d27605ed090789a49f9f0e171b21a79470af27cae829c904c427f55bebe6f8e8 |

The signed outer package reference remains
ca93ec2f10b75a7e9e87df679a2cbf5cdf84630fc94820df731e2f3759661848;
it is not substituted for any member hash. Prior signing verification established
preservation of these payload bytes. Installed package attribution is supported
by owner retrieval context plus matching version/build hashes, not a new console
inventory connection by Codex.

## Persistence and separate hardware observations

The original retrieved terminal JSON is direct file evidence supporting D00
persistence for this run. Receipt::Finish writes terminal state through WriteAtomic;
the latter writes/flushed a tmp and replaces the destination with write-through.
No separate PersistenceError field is serialized. No role error is present.
This validates the retrieved terminal record, not absence of all later I/O failures
or power-loss durability. The supplied photo shows the saved-receipt success
message rather than a persistence warning.

| Acceptance dimension | Result and evidence authority |
|---|---|
| Installation/registration | owner-reported installed0.1.3.0; matching version/member hashes in retrieved receipt |
| Activation | PASS, supported by attributable native receipt and owner run report |
| D00 UI rendering | PASS, inspected photograph shows D00-only UI and D00: PASS |
| Native-control completion | PASS, validated final receipt and five build-bound role hashes |
| Receipt persistence | PASS for this retrieved terminal file; no broader lifecycle/power-loss claim |
| Photo/run correlation | supporting visual evidence matches receipt result and app UI; association with this run owner-attested, no visible run/time identifier |
| Overall requested formal hardware acceptance | PASS for native D00 scope, with evidence limits stated |

Preserved original photo: originals/Xbox-D00-PASS.png, copied byte-identically from
the supplied codex-clipboard-905f364c-0e6b-438b-9a8e-54b17ee37aa1.png.
SHA256: 74f383324231a453d88474ebc8a83a4ffb7c178f720c0384cbe6b8b7be8bf6fa.
Visual inspection confirms Runtime Diagnostics - D00 ONLY; D00: PASS;
Java/JNI disabled at compile time; activation receipt saved in diagnostic
LocalState; and the note that UI drawing is not a graphics capability test.
No legible personal account, device or network identifier is visible in this
diagnostic-screen photo; no synthetic editing/redaction was necessary. Preserve
the original without reconstructing or enhancing its diagnostic text. No visible
version/run/time identifier exists, so the image alone cannot authenticate a
specific run or identify Xbox hardware; those associations remain owner testimony.
The previous PowerShell screenshot supports receipt hashing only, not UI evidence.

## Scope and next independently gated phase

Native D00 scope is activation, package identities/hashes and resource observations.
Receipt explicitly marks graphics_capability_tested, input_capability_tested,
audio_capability_tested and native_dependency_closure_tested false. CPU/GPU
measurement flags are false. Visible basic UI does not certify the separate
graphics matrix, audio, input, lifecycle endurance or all native APIs. Java/JNI,
Minecraft and gameplay remain untested; no entitlement conclusions follow.

The source experiment supports testing MTA startup but this run alone does not
prove the prior 0x8027025B root cause. Prior failure observations remain preserved.

Next gate: recommend a separately approved native-capability diagnostic planning/review
phase covering representative graphics/input/audio/lifecycle tests. Java21 JNI
requires its own runtime provenance/dependency audit and explicit implementation,
packaging and execution approvals; D00 PASS grants none of those permissions.

No new launch, console connection, installation, signing, dependency/certificate
change or production modification occurred. STOP after this acceptance review.
