# Phase 6B.4c — signing/static verification and future update gate

2026-10-17. One fresh-copy signing attempt succeeded. No Xbox access, package
registration/update, app execution, trust change or dependency change occurred.

## Approved input and source provenance

Clean experiment checkout HEAD remains
c70a17ecd4022452a963697196f362c8f286ed57 on research/phase6b4b-uwp-activation.
Build receipt binds that source, D00Only=true, and successful compilation/static
checks. Approved unsigned APPX was rehashed immediately before copying/signing:
`5fd3462dcce83faea10617b19d18000f437e19d70d04b0e2a5bc98411b9a44fd`.

The prior comparison proves only Application EntryPoint and reviewed Version
changed in manifest semantics; all native source/headers/receipt schema are
baseline-identical. Rebuilt PE differs only in COFF/debug timestamps; .text is
identical. Inventory/blockmap and profile JSON ordering changes are recorded in
../phase-6b4b-activation-experiment/EXPERIMENT-COMPARISON.json.

## Exact activation contract and remaining limit

Signed manifest: Application Id App, Executable RuntimeDiagnostics.exe,
EntryPoint LegacyForgeDiagnostics.App; Windows.Universal targeting, x64 GUI
AppContainer PE, separate diagnostic identity, no capabilities. Native wWinMain
still initializes STA and supplies winrt::make<DiagnosticSource>() to
CoreApplication::Run. DiagnosticSource implements IFrameworkViewSource and returns
DiagnosticView. This is the native supplied-view-provider contract, analogous to
the working launcher's MC.App and coreApp->Run(AppSource).

Microsoft's [Application activation schema](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-application)
distinguishes ordinary UWP entry identifiers from the packagedClassicApp
partial-trust marker. [CoreApplication.Run](https://learn.microsoft.com/en-us/uwp/api/windows.applicationmodel.core.coreapplication.run)
accepts the IFrameworkViewSource instance. MC.App is a comparison pattern, not a
production identifier the diagnostic must copy. The diagnostic-specific string
does not introduce a dependency on the production app or request a new capability.
This is a statically supported UWP experiment, not experimental verification that
Xbox accepts the exact identifier. No WinMD/XAML class factory is newly required
by the source's supplied-view-provider path. STA is deliberately unchanged and
remains a separate possible early-start failure; signing cannot resolve it.

## Signed artifact and public signer evidence

Artifact:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b4c-signing/20261017-140847-c38e9c14/RuntimeDiagnostics.D00.ActivationExperiment.0.1.2.0.signed.appx`

SHA256: **e4ffef8502405cd6bbc6d8e27b09a40c8f9119f6b424bfca53c5e08becf6ede7**.

| Field/check | Result |
|---|---|
| Name | AlgorHome.LegacyForge.RuntimeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Version / architecture | 0.1.2.0 / x64 |
| Signer subject/issuer | CN=LegacyForgeDiagnostics, self-signed |
| Thumbprint | D6245FB640D520EDED8F8A987B364BCADE01D01D |
| Validity UTC | 2026-10-17T17:58:48Z to 2027-10-17T18:08:48Z; valid at signing |
| Key / policy | RSA2048, Microsoft Software Key Storage Provider, ExportPolicy None |
| Usage / EKU / constraints | DigitalSignature / Code Signing 1.3.6.1.5.5.7.3.3 / end-entity |
| SignTool sign /fd SHA256 /s My /sha1 nominated-thumbprint | exit0, one actual signing attempt, no timestamp |
| CMS CheckSignature(true) | PASS, SHA256 digest, embedded signer matches nominated thumbprint |
| APPX signed-content digest | PASS via Windows APPX SIP |
| In-memory negative digest control | rejected with TRUST_E_BAD_DIGEST 0x80096010; package never mutated |
| Original payload/blockmap integrity | PASS, 11 original members byte-identical |
| Added signing metadata | AppxSignature.p7x, AppxMetadata/CodeIntegrity.cat |
| Content-type changes | only exact signature/catalog Override declarations; all originals retained |
| Standard signtool verify /pa /v | exit1, chain terminates at untrusted root |
| Cache-only WinVerifyTrust | CERT_E_UNTRUSTEDROOT 0x800B0109 |
| Root/TrustedPeople store inventories | unchanged, CurrentUser and LocalMachine |

CMS and APPX digest integrity PASS do not mean Windows default chain trust PASS
or Xbox activation PASS. No trust import, certificate replacement or re-sign was
performed. Public certificate evidence only is recorded; no PFX, key or password
was exported. Signed payload verification rechecks the exact identity/entry point,
zero capabilities, D00 input provenance and empty/unapproved runtime inventory.
The unchanged preprocessed source audit excludes S21 UI, dispatch, workers,
watchdog and JNI implementation and retains the E_ACCESSDENIED rejection stub.

The Sign-And-Verify.ps1 transcript represents one actual signing invocation.
An earlier preflight stopped before creating the copy because a PowerShell EKU
property projection was incorrect; reading the decoded certificate extension
confirmed the Code Signing EKU, and the preflight was corrected before signing.
The payload reviewer initially expected default content-type declarations; actual
SignTool Override declarations were inspected and precisely validated instead.
No signature retry or package rewrite was involved in either review correction.

## Preserved failed baseline

SIGNING-VERIFICATION.json records before/after SHA256 equality for the original
0.1.1.0 signed APPX (51e5c74462e79a296335beab4830f479e861e7132e0f660c680f6974d3b27530),
unsigned APPX (ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558),
public certificate metadata and original owner Xbox observation JSON. The approved
0.1.2.0 unsigned file also remains byte-identical. Failed launch 0x87E10006 and
unknown receipt state remain preserved; the unavailable original screenshot is
not invented. Production code and the baseline branch were not modified.

## Future OWNER UPDATE ONLY procedure — not currently authorized

1. Obtain explicit approval naming this signed hash/version for ONE owner-operated
   diagnostic update, with automatic launch disabled. Activation, receipt collection
   and cleanup require separate scope/approvals; no launch is implied by an update.
2. Preserve current failed-launch evidence before replacement. Read the existing
   diagnostic's untruncated PackageFullName if available and record installed
   version0.1.1.0. Preserve only diagnostic receipts if collection is separately
   approved. If old evidence cannot be retrieved, explicitly accept that limitation
   before replacement; do not delete/reset LocalState to hide it.
3. Immediately rehash the exact signed artifact above. Confirm same Name/Publisher/
   x64 and version0.1.2.0. Use the existing owner-authenticated Portal; no trust,
   configuration or certificate changes. Ensure diagnostic is not running; if it
   is running, stop rather than silently adding termination to the update scope.
4. Select only the approved experiment APPX, leave dependency uploads empty, use
   the already installed Microsoft.VCLibs.140.00, and disable automatic launch.
   If the UI cannot separate update from activation, stop before submitting.
5. Submit once. Wait for final registration result and record status/error. On
   certificate/dependency/registration rejection, stop without retry, repair,
   uninstall, downgrade, fallback upload or trust changes. Do not change App/Game
   classification. No writes are approved by this document alone.
6. Verify registered Name/Publisher/version0.1.2.0/x64, App classification and actual
   full package name. Unexpected identity/version means stop. Do not press Launch.

Same name/publisher/architecture retains the package family and may retain all
diagnostic LocalState. The full package name changes with version; this is not a
side-by-side package and not a clean-data run. Keep all old JSON/tmp files intact.

For a LATER separately approved single activation/receipt collection, establish a
read-only prelaunch diagnostic receipt listing, then attribute new evidence using
package_version0.1.2.0, case_id D00, new run_id/process_instance_id, observed time,
sequence and approved package-role hashes from PAYLOAD-VERIFICATION.json. Any old
0.1.1.0 receipt, unchanged timestamp or ambiguous run remains historical/ambiguous.
Do not substitute the outer signed APPX hash for the executable/manifest role
hashes inside receipts. Receipt schema and reason D00_ACTIVATED_HASHES_RECORDED are
unchanged; activation, rendering, native control, persistence and overall acceptance
remain separate observations. No S21/Java/JNI/Minecraft activity is authorized.

Current next gate: explicit owner approval for the diagnostic update ONLY, naming
the signed hash above. Standard Windows trust remains FAIL as reported; no bypass
or trust modification is included. Xbox acceptance and runtime execution remain
untested. STOP after signing/static verification.
