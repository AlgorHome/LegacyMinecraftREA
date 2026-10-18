# Phase 6B.5t - D06-SRV02 local signing

Result: signing and offline integrity verification PASS. Windows certificate-chain trust FAILED, separately recorded. No hardware acceptance claimed.

## Artifact and provenance

- Source: `c81d0f48286513f7a7579a1d2d786cca4f5e60e2`; branch `research/phase6b5s-d06-srv02`; checkout clean before and after. No source edit or rebuild.
- Unsigned original: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-192156-1c3f66cf\NativeCapabilities.unsigned.appx`
- Unsigned SHA-256: `88cde899358b6eaade1658802831c5a914b8e637cf1466321b233fa8a2788c31` (recomputed before signing and after verification).
- Signed fresh copy: `C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5t-signing\20261017-193135-107a9142\NativeDiagnostics.D06-SRV02.0.2.4.0.signed.appx`
- Signed SHA-256: `a77e31a5922bca35a09084dbe885b5d13ed1207571f66458644d5ac7ee8738d5`.
- Exactly one signing invocation; exit 0. SHA-256; no timestamp. Exclusive SIGN-ATTEMPT.lock prevents rerunning this helper.

## Manifest and policy

AlgorHome.LegacyForge.NativeDiagnostics; publisher CN=LegacyForgeDiagnostics; version 0.2.4.0; x64; Application Id App; entry point LegacyForgeNativeDiagnostics.App; zero declared capabilities. App console classification remains a later owner verification; the manifest Application Id alone cannot establish console classification.

Windows.Universal min 10.0.17763.0, MaxVersionTested 10.0.26100.0. Microsoft.VCLibs.140.00 min 14.0.0.0 with Microsoft publisher. No dependency bundled or installed. Native-only definitions and single D06-SRV02 policy match the approved build; Java/JNI/Minecraft payloads excluded. Fresh static audit matches pinned identity, capabilities, dependencies, payload, imports and receipt-contract test results.

Source review: src/probe.cpp:67 contains exactly one GetResource(resource.put()) call (void, no HRESULT). Lines 74 and 82 query IID_IUnknown, require S_OK and nonnull results before pointer equality at line 89. Nested com_ptr scopes release both identity references before returned resource, then SRV, texture, context and device. No extra operation or retry introduced. The query policy and schema v5 remain byte-identical.

## Signature and integrity

- Certificate: CN=LegacyForgeDiagnostics; thumbprint D6245FB640D520EDED8F8A987B364BCADE01D01D; self-issued end entity, RSA 2048, sha256RSA, DigitalSignature, Code Signing EKU 1.3.6.1.5.5.7.3.3.
- Valid UTC 2026-10-17T17:58:48.0000000Z through 2027-10-17T18:08:48.0000000Z; currently valid. Existing private key available, CNG ExportPolicy None; no key or certificate export and no certificate modification.
- CMS CheckSignature(signatureOnly=true): PASS with exactly the approved signer and SHA-256 digest.
- CryptSIPVerifyIndirectData: package digest PASS; deliberately altered expected digest in memory rejected with 0x80096010. Archive bytes were never altered for the negative control.
- All 12 original members except the expected content-types update are byte-identical, including original block map. Eleven block-mapped files checked for every block hash, whole-file hash extension, sizes and local header sizes. All six role hashes match independent pre-sign BUILD-EVIDENCE.json.
- ZIP CRC and unique entry names: PASS. Only AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat added; only their two expected content-type declarations added.
- Standard `signtool verify /pa /v <signed-copy>`: exit 1, untrusted-root chain error. Cache-only WinVerifyTrust confirms 0x800B0109 (CERT_E_UNTRUSTEDROOT). This is FAILED chain validation, not a successful normal verification. No trust changes or bypass.

## Preservation and limits

All 175 pinned frozen baseline files rehashed successfully before and after signing; all 186 total preserved files unchanged. Unsigned original, accepted D00/HW01/FMT01/RES01a/SRV01 packages, photos, receipts and dossiers untouched. Trust-store inventory snapshots unchanged. No application installed or executed, no Xbox connection, and no production changes.

No target execution means SRV02 hardware behavior, API/driver completion, resource-release telemetry and persistence remain untested. The observation deadline cannot cancel a GPU/native call blocked inside a driver. Signature integrity does not establish Xbox package acceptance. No timestamp was requested; certificate expiry remains relevant to future validation.

## Evidence and next gate

UNSIGNED-PREFLIGHT.json; SIGNING-VERIFICATION.json; SIGNED-PAYLOAD-VERIFICATION.json; SIGNED-MANIFEST.xml; signtool-sign.log; signtool-verify.log; VERIFICATION-SUMMARY.json. Read-only verification helpers are retained here. Prior approved dossiers were not edited.

Next gate: separate authorization for one owner-operated installation-only update, following OWNER-INSTALLATION-ONLY.md. Launch, receipt retrieval, final acceptance and cleanup each remain separately gated.
