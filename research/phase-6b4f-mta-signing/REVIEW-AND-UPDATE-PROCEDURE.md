# Phase 6B.4f — MTA experiment signing and verification

2026-10-17. One fresh-copy signing attempt succeeded; no deployment/execution.

Signed APPX:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b4f-signing/20261017-143140-118313f1/RuntimeDiagnostics.D00.MTAExperiment.0.1.3.0.signed.appx`

SHA256: **ca93ec2f10b75a7e9e87df679a2cbf5cdf84630fc94820df731e2f3759661848**.

## Input provenance and unchanged safety boundaries

Approved source 553c6554f40f1372b0ea09f6badbbb98e133a9ab was reverified in the
clean research/phase6b4e-mta-startup checkout. Build receipt binds that commit,
D00Only configuration and successful build/static verification. Unsigned hash
rechecked immediately before copy/sign:
0595e9936aa4091ebdcce3e23b4e43fdba014d88267b4aaa0656fbd9cddb307e.

The phase-6b4e verification helper was rerun successfully before signing. Relative
to c70a17e/0.1.2.0, the only runtime source edit is wWinMain's init_apartment enum
single_threaded -> multi_threaded. Separate reviewed changes are manifest version
0.1.3.0, exact static verifier version pin and experiment documentation. Native
control, graphics, receipt/schema, all other initialization and build script are
unchanged. Direct/delay import sets are identical to the 0.1.2.0 build.

Manifest and signed payload checks confirm:

- Name AlgorHome.LegacyForge.RuntimeDiagnostics; Publisher CN=LegacyForgeDiagnostics;
  Version0.1.3.0; x64; Application Id App; EntryPoint LegacyForgeDiagnostics.App.
- Zero capabilities and unchanged Windows.Universal/Microsoft.VCLibs.140.00 dependency.
- D00-only compile-time audit PASS, with all native translation units built with
  LFD_D00_ONLY=1. JNI/S21 handlers, UI, worker, watchdog and runtime loader remain
  excluded; direct-call E_ACCESSDENIED stub remains fail-closed.
- Empty/unavailable/unapproved runtime and fixture inventory; no Java, Minecraft,
  authentication, framework or third-party runtime binary added.

## Signature results

| Check | Result |
|---|---|
| Certificate | CN=LegacyForgeDiagnostics / D6245FB640D520EDED8F8A987B364BCADE01D01D |
| Certificate validity | valid at signing; 2026-10-17T17:58:48Z through 2027-10-17T18:08:48Z |
| Key | RSA2048, nonexportable ExportPolicy None, Microsoft Software Key Storage Provider |
| Usage | DigitalSignature, Code Signing EKU, end-entity |
| SignTool sign /fd SHA256 /s My /sha1 nominated-thumbprint fresh-copy | exit0, one attempt, no timestamp |
| CMS CheckSignature(true) | PASS; embedded signer matches, SHA256 digest |
| Windows APPX SIP signed-content digest | PASS |
| Negative digest control (memory only) | rejected, TRUST_E_BAD_DIGEST 0x80096010 |
| Original payload and block map | all 11 original members except content-type document byte-identical |
| Added metadata | AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat only |
| Content types | existing declarations retained; only exact signature/catalog overrides added |
| Standard SignTool verify /pa /v | exit1: chain terminates in untrusted root |
| Cache-only WinVerifyTrust | CERT_E_UNTRUSTEDROOT 0x800B0109 |
| CurrentUser/LocalMachine Root and TrustedPeople inventories | unchanged |

SIGNING-VERIFICATION.json records exact input/output paths/hashes, public signer
metadata, cryptographic checks, trust result and preserved-file hashes.
PAYLOAD-VERIFICATION.json lists unchanged member hashes and identity checks.
signtool-sign.log and signtool-verify.log preserve tool results. Helpers operate
on bytes/public verification APIs; the target executable is never loaded/run.
Private keys, PFX and passwords were not exported; no signing-key/store changes.

Integrity PASS does not mean standard Windows chain trust PASS, Xbox update
acceptance PASS, or hardware activation PASS. Do not change trust or retry signing
to conceal the retained trust finding. Source checkout remains unchanged/clean.

## Preservation

Before/after hashes confirm unchanged original 0.1.1.0 and 0.1.2.0 signed/unsigned
APPX files, the approved unsigned0.1.3.0, public certificate evidence, separate
versioned failure observations and latest owner package inventory. No old build
or source commit was overwritten. No new receipt evidence was obtained; the
existing unknown receipt state remains unknown. Production LegacyForge is untouched.

## Prepared owner-operated UPDATE ONLY procedure — approval required

1. Obtain separate approval for ONE installation-only update from installed0.1.2.0
   to0.1.3.0 naming the signed hash above. This document does not authorize it.
2. Preserve existing diagnostic evidence first. If an approved read-only receipt
   route exists, retain old listing/files; if unavailable, record that limitation.
   Never clear LocalState, uninstall, reset or overwrite old receipt evidence.
3. In the existing owner-authenticated Portal confirm exact diagnostic identity,
   current version0.1.2.0/x64/App and Not running. Owner-reported existing full name:
   AlgorHome.LegacyForge.RuntimeDiagnostics_0.1.2.0_x64__x26zk9zqnnfrj;
   confirm from existing inventory, not a guessed suffix. Unexpected state means stop;
   no automatic termination is included.
4. Rehash the signed0.1.3.0 file immediately before submission. Select that APPX only;
   leave dependency uploads empty and use the existing Microsoft.VCLibs.140.00.
   Disable automatic launch. If auto-launch cannot be reliably disabled, stop.
5. Submit exactly once, only after update authorization. Record final registration
   result/error; an accepted upload alone is not success. On certificate/dependency/
   registration failure or ambiguity, stop without retry, trust/framework changes,
   repair or uninstall. Do not change App classification or console configuration.
6. Verify exact diagnostic Name/Publisher/version0.1.3.0/x64/App and record actual
   new PackageFullName. Unexpected identity/version means stop. Do not press Launch,
   collect receipts or clean up unless those actions have their own approval.

Same name/publisher/architecture means same diagnostic family and retained
LocalState may contain all prior receipts. It is not side-by-side isolation.
Full package name changes with version; do not fabricate it in advance. After a
LATER separately approved launch/collection, attribute new receipts through
package_version0.1.3.0, D00 case, new run/process UUIDs, observation time and role
hashes from this payload. The outer signed APPX hash is not the executable role
hash. Keep registration, activation, rendering, native control and persistence
separate. No existing receipt becomes current merely because the package updates.

STOP: signing/static verification complete. Xbox update and activation need
separate explicit authorization. No console access, installation, update, launch,
Java/JNI/Minecraft execution or production modification occurred.
