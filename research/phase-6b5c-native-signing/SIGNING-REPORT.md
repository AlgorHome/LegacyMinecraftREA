# Phase 6B.5c — NativeDiagnostics D06-HW01 signing/static verification

2026-10-17, America/Chicago. **One fresh copy signed successfully. Integrity and
payload checks PASS; normal Windows chain trust FAIL as separately reported.**
No diagnostic/Java/JNI/Minecraft execution, installation, console access, source
modification, trust-store/dependency change or accepted-baseline replacement.

## Approved input and signed output

Source a3f72874241914f6048d4ca9ec4fc0edc978625d, clean
research/phase6b5b-d06-hw01 checkout; build/source/compiled identity reverified.
Unsigned approved hash79722c961dd677a2c89610599aec2e9537727dead6d66e2e3e8ff522da8b2501
matched immediately before copy/signing and remained unchanged afterward.

Signed APPX:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b5c-signing/20261017-173712-e540416b/NativeDiagnostics.D06-HW01.0.2.0.0.signed.appx`

SHA256: **d4629d1f494f73db7dcb6290bee8c5c9f28375c8630c531e58b3ee95a6f05908**.

| Manifest/signing field | Verified value |
|---|---|
| Package Name | AlgorHome.LegacyForge.NativeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Version/architecture | 0.2.0.0 / x64 |
| Application Id / entry point | App / LegacyForgeNativeDiagnostics.App |
| Capabilities | zero declared |
| Classification | App intended; actual console setting NOT OBSERVED because nothing installed/accessed |
| Case/build isolation | D06-HW01 only; native-only1, JNI0, inherited D001; exact three native TUs |
| Framework | Microsoft.VCLibs.140.00 >=14.0.0.0, Microsoft publisher; no bundled framework |
| Signer thumbprint | D6245FB640D520EDED8F8A987B364BCADE01D01D |
| Certificate validity UTC | 2026-10-17T17:58:48Z to2027-10-17T18:08:48Z, valid at signing |
| Certificate properties | RSA2048, DigitalSignature, Code Signing EKU, end-entity, ExportPolicy None |
| SignTool sign /fd SHA256 /s My /sha1 nominated-thumbprint fresh-copy | exit0; exactly one signing attempt; no timestamp |
| CMS CheckSignature(true) | PASS, SHA256, exact nominated embedded signer |
| APPX signed content digest via Windows SIP | PASS |
| In-memory negative expected digest | rejected with TRUST_E_BAD_DIGEST 0x80096010; APPX not changed |
| Standard signtool verify /pa /v signed-copy | exit1, chain terminates at untrusted root |
| Cache-only WinVerifyTrust | CERT_E_UNTRUSTEDROOT 0x800B0109 |
| Root/TrustedPeople stores | unchanged CurrentUser and LocalMachine inventories |

No private key/PFX/password export, new certificate or key modification. Signature
integrity is independent from certificate-chain trust. The known trust failure was
retained without importing a certificate, bypassing policy or re-signing. Xbox
installation/activation acceptance is NOT EXECUTED and is not inferred from either.

## Payload, block map and source safety

UNSIGNED-PREFLIGHT.json rechecks the exact unsigned bytes, manifest, input/source
hashes, preprocessed JNI exclusion, one hardware call site, no swapchain/presentation
code, unknown-case/start-once guards and payload allowlist. No compiler or native
capability test was run in this phase. The static audit is data/source inspection.

SIGNED-PAYLOAD-VERIFICATION.json proves 12 original non-content-type members,
including all11 payload files and AppxBlockMap.xml, remain byte-identical. Only
AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat were added. The content-type
document retains every original declaration and adds only exact signature/catalog
overrides. No executable, policy, native input, schema, inventory, asset, manifest,
license or block-map payload was rewritten.

All11 block-map file sizes/local-header lengths and every64KiB block SHA256 were
checked against uncompressed signed-package bytes. The existing2021 FileHash
extension for the executable was also checked as a whole-file SHA256. The reviewer
initially counted that extension as another block; inspection corrected the
verification parser to handle and validate it. No APPX change/re-sign occurred.
The independent SIP verification additionally validates the signed package digest.

Only the original single D06-HW01 path remains; no WARP/reference fallback, Java
fixtures/headers/runtime, proprietary assets, authentication modules or additional
native tests were added. This is hardware-device creation only, never all D06 PASS.

## Baseline preservation and UI risks

SIGNING-VERIFICATION.json records before/after hashes for prior artifacts/evidence,
including accepted signed RuntimeDiagnostics0.1.3.0, its unsigned file, original
receipt/photo/report and frozen RuntimeDiagnostics source. All match. Git source
remains clean at the approved commit, changes versus accepted553c655 confined to
NativeCapabilities; no production path or accepted D00 source changed.

See MESSAGE-DIALOG-REVIEW.md: normal dialog is queued after the case decision,
not a driver/persistence prerequisite. Initial synchronous receipt I/O can delay
activation; asynchronous dispatcher/dialog errors are unobserved; exact Xbox UI
support/dismissal/text constraints remain unknown. A stored terminal result can
exist without visible UI. A visible in-memory status with pending storage cannot
substitute for the original validated receipt. No source fixes were authorized.

Evidence files: SIGNING-VERIFICATION.json, signed manifest copy, unsigned preflight,
signed payload/block-map comparison, SignTool sign/verify logs and reviewed helper
scripts. Original signed copy/receipt remain in the unique analysis-local folder.

## Completion and next gate

No blocker prevented signing or static verification. Remaining uncertainty is
future Xbox registration, UI/API/loader behavior, blocked driver/storage calls
and actual runtime result. Standard Windows trust remains FAIL as documented.
Owner must separately authorize installation of this NEW package/hash, with
auto-launch off and no dependency upload. No unnecessary Microsoft VCLibs fallback
installation is proposed. OWNER-INSTALLATION-ONLY.md is prepared, not executed.
One D06-HW01 launch and scoped receipt retrieval require their own later approvals.
