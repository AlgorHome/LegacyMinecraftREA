# Phase 6B.5f — D06-FMT01 local signing

**Signing PASS; cryptographic signature/content/payload verification PASS.**
**Normal Windows chain trust FAIL: CERT_E_UNTRUSTEDROOT (0x800B0109).**
No trust change, installation, deployment, diagnostic execution or console access occurred.

Source: `bbe3a42c422e4328d5f98c07a9370fa948d0cbbf` on research/phase6b5e-d06-fmt01.
Unsigned original: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-180047-9ad3700d\NativeCapabilities.unsigned.appx`.
Unsigned SHA256: `24dc6835408f9a5d38d1ab56ec82dfd550cf0dc183e495defa836299d77dd03d` — reverified before and after, unchanged.
Signed copy: **`C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5f-signing\20261017-180640-31684a3e\NativeDiagnostics.D06-FMT01.0.2.1.0.signed.appx`**.
Signed SHA256: **`ae19e5ff93438bcf8a3c9e0d42ad0323908ee83d95231cba9dcd9a319fd5d8ef`**.
Exactly one fresh copy and one SignTool signing invocation. No timestamp server used.

## Pre-sign verification

Fresh source-provenance and static audit matched the pinned Phase6B.5e evidence:
clean source commit, exact APPX hash, build inputs/source hashes, eleven-member payload
allowlist, native imports, receipt schema v2, D06-FMT01 policy, compile-time safety,
and all six member-role hashes. UNSIGNED-PREFLIGHT.json preserves this fresh audit.
One hardware device callsite and one RGBA8 CheckFormatSupport callsite; no fallback,
resource creation, rendering, presentation or Java/JNI path. The retained offline oracle
checks accepted7 synthetic forms and rejected18 malformed cases, with no native execution.

| Manifest property | Verified value |
|---|---|
| Name | AlgorHome.LegacyForge.NativeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Version |0.2.1.0 |
| ProcessorArchitecture | x64 |
| Application Id / entry point | App / LegacyForgeNativeDiagnostics.App |
| Capabilities | None declared |
| Dependencies | Windows.Universal min10.0.17763.0/max-tested10.0.26100.0; Microsoft.VCLibs.140.00 min14.0.0.0, original Microsoft publisher |
| Xbox classification | App required; not independently observable from this manifest or host-only signing. Owner inventory remains a later gate. |

## Certificate and signing

Store Cert:\CurrentUser\My; subject/issuer CN=LegacyForgeDiagnostics;
thumbprint **D6245FB640D520EDED8F8A987B364BCADE01D01D**.
Validity checked locally:2026-10-17T17:58:48Z to2027-10-17T18:08:48Z.
RSA2048; sha256RSA certificate signature; DigitalSignature only; Code Signing EKU
1.3.6.1.5.5.7.3.3; end-entity. Private key available through CNG, export policy None.
Only public metadata/nonexportable-policy verification is recorded; no private key,
PFX, passwords or replacement certificate created/exported.

SDK10.0.26100.0 x64 SignTool command (exit0):
`signtool sign /fd SHA256 /s My /sha1 D6245FB640D520EDED8F8A987B364BCADE01D01D "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5f-signing\20261017-180640-31684a3e\NativeDiagnostics.D06-FMT01.0.2.1.0.signed.appx"`.
The SHA1 option selects the nominated certificate thumbprint; file/CMS digest is SHA256.
An exclusive local attempt marker prevents accidentally rerunning this helper to sign again.
No accepted HW01 artifact was rebuilt or re-signed.

## Independent post-sign checks

| Check | Outcome |
|---|---|
| CMS signature mathematics | PASS: SignedCms.CheckSignature(true), exactly one signer, nominated thumbprint, SHA256 digest OID2.16.840.1.101.3.4.2.1 |
| APPX content digest | PASS: Windows package SIP CryptSIPVerifyIndirectData validates signed indirect data against exact file |
| Negative control | PASS: mutate one in-memory expected hash byte, not the APPX; rejected with0x80096010 |
| Original payload and blockmap | PASS: all12 original members other than Content_Types byte-identical, no removals |
| Signing-only additions | AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat only |
| Content_Types | Only two expected signing metadata declarations added |
| Blockmap | All11 payload members checked: size,64KiB SHA256 blocks, local header size; whole-file hash extensions checked when present |
| Source/case/payload binding | All6 role hashes match independently pinned0.2.1.0 build; native imports identical; schema/policy/native-only inventory retained |
| Original evidence |84 prior artifact/evidence/source files rehashed before/after and unchanged, including accepted HW01/D00 artifacts and receipts/photos/reports |
| Trust-store inventories | CurrentUser and LocalMachine Root/TrustedPeople thumbprint inventories unchanged |

CMS verification with signature-only mode checks mathematical integrity independently;
it is not a certificate-trust import, security-setting change, or deployment acceptance.
The helper loads only platform cryptographic verification APIs, never the diagnostic EXE/DLL.
Public helper hash/method are pinned in VERIFICATION-SUMMARY.json.

Normal command: `signtool verify /pa /v "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5f-signing\20261017-180640-31684a3e\NativeDiagnostics.D06-FMT01.0.2.1.0.signed.appx"`.
Exit **1**; message: chain terminates in an untrusted root. Cache-only WinVerifyTrust
independently returned **0x800B0109 / CERT_E_UNTRUSTEDROOT**. No evidence of corruption;
chain trust is not reported as PASS. The file is not timestamped, so no timestamp-based
post-expiry claim is made. No trust repair/import attempted. Host policy failure neither
proves nor guarantees Xbox Developer Mode acceptance; that needs the separate owner gate.

SIGNING-VERIFICATION.json, SIGNED-PAYLOAD-VERIFICATION.json, SIGNED-MANIFEST.xml,
VERIFICATION-SUMMARY.json and both SignTool logs supply exact verification evidence.
Owner checklist: OWNER-INSTALLATION-ONLY.md.

## Remaining gates

Unsigned build/source remain unchanged. No Xbox observation was made this phase.
A later0.2.1.0 update replaces the accepted0.2.0.0 NativeDiagnostics registration and
may retain stale LocalState/NativeCapabilityReceipts. It cannot preserve side-by-side
HW01 execution. If that is needed, approve a distinct package implementation first;
do not change identity or registration during this signing phase. Accepted D00 and
production LegacyForge remain untouched.

Next approval: **one owner-operated installation-only update**, naming this exact signed
path/hash, with auto-launch disabled and no unnecessary dependency upload. Launch,
read-only receipt retrieval and cleanup are separate later approvals. No rendering,
presentation, OpenGL, LWJGL, Java/JNI or Minecraft compatibility is established here.
