# Phase 6B.4 — Xbox D00 hardware execution preparation

Prepared 2026-10-17. PREPARATION ONLY. No activation, receipt retrieval, repair,
termination, deployment or console configuration action was performed by Codex.
Execution and receipt collection require explicit owner authorization. Prior
installation permission does not authorize either step.

## Installation evidence and immutable inputs

Phase 6B.3h owner report: Series X installation PASS, no installation error;
registered name, publisher, version, architecture and App classification MATCHED.
No deliberate diagnostic launch reported. This is owner testimony, not a Codex
console observation; it does not establish that no incidental activation occurred.

| Identity field | Owner-confirmed value |
|---|---|
| Name | AlgorHome.LegacyForge.RuntimeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Version | 0.1.1.0 |
| Architecture | x64 |
| Classification | App |
| PackageFullName | NOT DISPLAYED; unresolved |
| OS build | 10.26100.9445, prior owner report |

Signed APPX rehashed during this preparation:
`51e5c74462e79a296335beab4830f479e861e7132e0f660c680f6974d3b27530`.
Artifact: `C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b3d-signing/20261017-132111-5ff08807/RuntimeDiagnostics.D00.signed.appx`.
Original unsigned hash remains the approved reference
`ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558`.
Built source 4101f7ee07d1c74911ffbf5cd2a44aff608c401d;
review df23adb6dbe948079510cf12eb64d5fd23542256.

Preserved Phase 6B.3e findings: independent CMS and APPX signed-content digest
verification PASS; normal Windows SignTool /pa verification FAIL, exit 1,
CERT_E_UNTRUSTEDROOT (0x800B0109). These checks were not rerun here.
Signer thumbprint D6245FB640D520EDED8F8A987B364BCADE01D01D.
Xbox installation acceptance does not change Windows certificate-chain trust.
No trust changes are required by this preparation.

## Read-only entry identification before execution

In the existing authenticated owner Portal, inspect the installed app's details
without pressing Launch or any modifying action. Match every identity field above,
not merely its display name. Record the actual PackageFullName and application
entry/relative ID if exposed; packaged Application Id is App. Do not construct a
publisher suffix or fabricate a package full name.

If UI details omit it, the owner can inspect the read-only
`GET /api/app/packagemanager/packages` response on the same authenticated Portal
origin. Find the exact matching Name/Publisher/Version record and retain only its
package identifiers. Architecture can be derived from the returned full name if
necessary, explicitly labeled derived. Do not share RegisteredUsers, SIDs,
credentials, cookies or full inventory captures. No Codex Portal access occurred.
If multiple entries, identity mismatch, or no reliable app-data mapping exists,
stop and record BLOCKED; do not launch by guessing.

Microsoft documents package inventory and Xbox support in the
[core API reference](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/device-portal-api-core#get-installed-apps).
The [Xbox Portal guide](https://learn.microsoft.com/en-us/previous-versions/windows/uwp/xbox-apps/device-portal-xbox)
describes app actions and file exploration; availability of specific controls must
be checked on this console rather than assumed.

## Proposed owner-operated single-launch checklist — NOT YET AUTHORIZED

1. Obtain explicit approval for one D00 activation. Receipt listing/download should
   be included expressly or remain a separate later stage. No cleanup is implicit.
2. Verify the exact installed entry as above. If read-only process information
   shows it already running, stop: do not terminate or reactivate it automatically.
   If the file route is available and approved, record existing diagnostic receipt
   names/timestamps as a baseline; never delete old evidence. No baseline means
   attribution must retain that uncertainty.
3. Prepare a clock and a local evidence sheet. Record console build and local time
   with offset. Select only the matched diagnostic entry and issue Launch ONCE
   using the existing owner UI. Start the 30-second observation at that action.
   Do not press Launch again, invoke S21, navigate production data, or change App
   classification. D00 starts automatically on activation; no Java action is needed.
4. Observe the display for up to 30 seconds. Record appearance/absence of the D00-only
   UI, D00 status/reason, elapsed time, error codes, blank screen/crash/hang, and any
   persistence warning. A Portal launch request being accepted is not proof of
   activation. A visible UI is not proof of a durable receipt.
5. At 30 seconds, end observation and record the state. This is an OWNER observation
   window, not an app-enforced D00 watchdog. The S21 watchdog is compiled out in
   this package. Do not automatically kill, restart, repair or relaunch; termination
   is a distinct action requiring approval. If it finishes early, preserve the
   result and continue observing without additional test actions.
6. Stop after the authorized observations. If receipt collection is not separately
   approved, leave the package/data intact and report the observation only.

## Proposed diagnostic-only receipt collection — authorization required

Use the existing owner Portal file explorer, if it exposes app-local storage.
Select the actual diagnostic PackageFullName verified above, then only
`LocalState/Phase6B1Receipts`. Do not browse production LegacyForge, other app
containers, or arbitrary user data. If the Portal cannot map this exact package or
does not expose its LocalState, collection is BLOCKED; do not enable shares,
alter security, copy whole app stores, or reinstall anything as a workaround.

Download only the new/relevant `D00-<run UUID>.json` and any corresponding `.tmp`
artifact. Preserve original names/bytes; record source package, retrieval time,
size and local SHA-256 using Get-FileHash. Work from copies for parsing/redaction.
Do not upload/delete/edit console files. A partial tmp or old receipt is evidence,
not a successful terminal run. Preserve all candidate D00 receipts if attribution
is ambiguous; do not choose a historical PASS as the new run.

Validate against the existing `contracts/receipt.schema.json` and inspect:

- schema legacyforge-phase6b1-runtime-receipt-v1; case_id D00; a run/process ID
  consistent with this observation; package_version 0.1.1.0;
  expected_package_identity true; approved source_baseline d1453434ceefe73bef5aff497194e09f39dde7e1.
- terminal true, stage FINAL, status PASS, reason D00_ACTIVATED_HASHES_RECORDED.
- Complete details.role_hashes matching PAYLOAD-HASHES.json for the diagnostic
  executable, packaged manifest, input manifest, runtime inventory and native
  profile; required_role_hashes_complete true. The implementation records hashes;
  the reviewer must compare them with the approved payload.
- jvm_loaded false; Minecraft/gameplay and authentication/entitlement modification
  flags false. Any S21 receipt attributable to this attempt is unexpected: stop.
- Preserve resource observations and unavailable/error fields as emitted; do not
  turn missing metrics into zero or successful capability tests.

## Independent result fields

| Observation | Initial state | Acceptance evidence |
|---|---|---|
| Installation/registration | PASS, owner-reported | matched identity, no installation error |
| Activation | NOT TESTED | observed app/process or attributable activation receipt; launch request alone insufficient |
| Rendering | NOT TESTED | owner sees D00-only UI; hardware D3D11 requirement unchanged |
| Native control | NOT TESTED | matching final D00 receipt and approved role hashes |
| Receipt persistence | NOT TESTED | newly attributable, downloadable valid terminal receipt; UI PASS alone insufficient |
| Receipt retrieval | NOT AUTHORIZED/PERFORMED | approved diagnostic-only download and local hash |
| Overall D00 acceptance | NOT TESTED | activation + rendering + native control + validated durable receipt all supported |

Report FAILED for observed failure, BLOCKED for unavailable prerequisites/routes,
and INCONCLUSIVE for ambiguous attribution or a 30-second unresolved observation.
Do not overwrite the original emitted receipt status with the reviewer conclusion.
PackageFullName remains unresolved until an actual owner read-only observation.

## Failure evidence and stop conditions

Graphics failure may produce FAILED/DIAGNOSTIC_UI_UNAVAILABLE while still writing
a valid receipt: this supports activation and receipt persistence, but rendering
and overall acceptance fail; RunNativeControl is skipped. Record these separately.
No receipt does not establish that activation never occurred. A crash/hang may
leave only a checkpoint or tmp: preserve it and the owner's timing/error/display
evidence without retrying. Numeric error codes must be retained verbatim.

Stop on unexpected identity, unexpected S21/Java behavior, missing receipt,
RECEIPT_ERROR, crash, hang or failed/blocked result. No repairs, trust changes,
framework installs, production modifications or automatic restart. D00 does not
certify JNI, native dependency closure, input, audio, Minecraft or gameplay, and
UI rendering is not the separate D06 graphics capability test.

Source support: isolated harness src/app.cpp D00 activation path;
src/native_control.cpp RunNativeControl; src/report.cpp Receipt::Checkpoint,
Receipt::Finish, WriteAtomic and LocalRoot; contracts/receipt.schema.json;
docs/D00-ONLY.md. Prior evidence: ../phase-6b3e-trust-investigation/FINDINGS.md and
../phase-6b3g-final-predeployment/FINAL-REVIEW.md (historical pre-install state).

Execution approval and attributable hardware observations remain pending. STOP.
