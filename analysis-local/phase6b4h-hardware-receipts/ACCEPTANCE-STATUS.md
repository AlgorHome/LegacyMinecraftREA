# Phase 6B.4h — hardware evidence intake status

2026-10-17. **Formal D00 hardware acceptance BLOCKED: receipt not supplied.**
This is an interim evidence status, not a completed receipt verification report.
No console access, new activation, package change or unrelated collection occurred.

Owner identifies installed target:
AlgorHome.LegacyForge.RuntimeDiagnostics_0.1.3.0_x64__x26zk9zqnnfrj,
and reports a successful visible D00 PASS. No receipt or photo was attached or
found in the prior intake originals folder at this step. Do not conclude the
receipt is absent on Xbox; local availability and console persistence differ.

| Field | Evidence state |
|---|---|
| Installation/registration0.1.3.0 | owner describes target as installed; full update result not independently inspected |
| Activation | successful visible run owner-reported; time/trigger/run binding not yet supplied |
| Rendering | visible D00 PASS owner-reported; photo not yet inspected |
| Native control | UI PASS owner-reported; receipt/hashes not yet verified |
| Durable persistence | UNKNOWN |
| Overall formal D00 acceptance | BLOCKED pending attributable validated receipt |

PINNED-ROLE-HASHES.json was derived directly from the approved unsigned0.1.3.0
APPX after rechecking hash0595e9936aa4091ebdcce3e23b4e43fdba014d88267b4aaa0656fbd9cddb307e.
It pins all five role hashes independently of any future receipt. Source553c655;
signed reference ca93ec2f10b75a7e9e87df679a2cbf5cdf84630fc94820df731e2f3759661848.
This file is build evidence, not proof of installed bytes or successful execution.

## Owner collection, no new launch

Use the existing authenticated Portal. In its already available read-only file
explorer select ONLY the exact diagnostic package above, its LocalAppData, then
LocalState/Phase6B1Receipts. Record remote filename, timestamp/timezone and size;
download the fresh D00 JSON and corresponding temporary file if present into
originals/. Do not delete, overwrite or rename console files. A prior-version
receipt retained by update is not evidence for the new PASS. If access is missing,
report unavailable/access denied/no directory/empty listing distinctly and stop
that path without settings, permissions or tool changes.

Retain the hardware photo locally and provide its local path. Preserve its original
privately; a separate sanitized evidence copy must remove unrelated personal
content without modifying the diagnostic display. Original photo not yet available,
so no visual verification/redaction or hash can presently be claimed.

## Verification after delivery

Hash original files before parsing; record source package/remote listing and local
retrieval time. Validate against the pinned receipt schema including required fields,
types, formats and additional-properties restrictions. Check case D00, version0.1.3.0,
expected_package_identity true, terminal true, stage FINAL, status PASS,
reason D00_ACTIVATED_HASHES_RECORDED, valid run/process UUIDs, sequence/elapsed time,
observed_at_utc, source_baseline d1453434ceefe73bef5aff497194e09f39dde7e1,
package_role INDEPENDENT_RUNTIME_DIAGNOSTICS and unchanged false gameplay/auth flags.
Compare all required role hashes against PINNED-ROLE-HASHES.json, not against the
receipt's own declarations. Check required_role_hashes_complete and JVM flags.
Correlate file/run/observation with actual reported success time; leave unresolved
attribution INCONCLUSIVE. Schema-valid JSON alone does not authenticate Xbox origin.

Keep originals unchanged and private. Hash sanitized derivatives separately and
remove personal account/device/network identifiers; retain package/version and
technical run fields needed for evidence. Final report must distinguish owner
testimony, visually inspected facts, receipt assertions and verified build matches.
Resource fields/graphics/input/audio claims are limited to actual D00 scope; no
Java/JNI/Minecraft or broader runtime acceptance follows from D00 success.

STOP awaiting existing receipt/photo delivery or an owner-reported inaccessible
collection path. No installation, signing, launch, console changes or production work.
