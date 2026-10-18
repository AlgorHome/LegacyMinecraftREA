# Phase6B.5o — D06-SRV01 local signing and integrity verification

**Signing PASS. CMS/APPX content/payload/blockmap integrity PASS.**
**Normal Windows chain trust FAIL: CERT_E_UNTRUSTEDROOT (0x800B0109), exit1.**
No trust settings/certificate stores changed; no source modification/rebuild, installation,
launch, console access or data retrieval. Hardware0.2.3.0 remains NOT EXECUTED.

Research branch `research/phase6b5n-d06-srv01`, clean at `e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8`.
Unsigned original `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-185632-1c4c5a9c\NativeCapabilities.unsigned.appx`;
SHA256 **e70fd6c9ef76ff17a06a9ad605c6c88e5eb412240446b6bbfcf17d1b8897c693**, independently recomputed before/after and unchanged.
Signed fresh copy **`C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5o-signing\20261017-190225-a21c9a46\NativeDiagnostics.D06-SRV01.0.2.3.0.signed.appx`**;
SHA256 **da28a5c22cb27b913b2bf296155c9d9bc5745e37ff3b2af88832f7661e042724**.
Exactly one signing invocation and one signed copy. No accepted earlier artifact re-signed.

## Pre-sign source, manifest and payload

Source/build/branch and fresh static audit matched the pinned research dossier. No build
command was run. Current source hashes/compiled-input metadata, entire payload allowlist,
native imports, case policy and receipt v4 were checked. Seven unsafe preprocessor rejection
results remain original build evidence;11 valid/37 invalid offline JSON-contract fixtures
passed the fresh audit, without native diagnostic execution.

| Property | Verified |
|---|---|
| Package | AlgorHome.LegacyForge.NativeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Manifest version/architecture |0.2.3.0 /x64 |
| Application Id/entry point | App /LegacyForgeNativeDiagnostics.App |
| Capabilities | None declared |
| Startup | MTA/CoreApplication retained |
| Intended case | D06-SRV01 only; old dispatch/macros and Java/JNI excluded |
| Operation | One hardware11_0/BGRA device, one accepted1x1 RGBA8 texture, one explicit Texture2D SRV; metadata checks and scoped SRV-before-texture release |
| Exclusions | No texel reads/writes, pipeline binding, shader/compiler/draw/clear/copy/map/readback/swapchain/present/fallback/extra cases/Java/Minecraft |
| Dependencies | Unchanged Windows.Universal min10.0.17763.0/max-tested10.0.26100.0; Microsoft.VCLibs.140.00 min14.0.0.0/Microsoft publisher; no bundled framework or extra executable |
| Xbox classification | App intended/required; Application Id App is not independent confirmation of that console inventory field. No Xbox access performed; no observed mismatch. |

UNSIGNED-PREFLIGHT.json records actual fresh payload/import/schema/policy findings.
No unrelated executable, runtime/dependency or fixture introduced by signing.
All141 frozen baseline pins match before/after;152 total prior files including unsigned
artifact and approved SRV01 dossier reverified. Accepted D00/HW01/FMT01/RES01a packages,
source/evidence/photo/receipt/report files remain unchanged.

## Certificate and exact signing workflow

Existing certificate Cert:\CurrentUser\My\D6245FB640D520EDED8F8A987B364BCADE01D01D;
subject/issuer CN=LegacyForgeDiagnostics. Thumbprint matches nominated certificate.
Validity checked:2026-10-17T17:58:48Z to2027-10-17T18:08:48Z;
RSA2048, sha256RSA, DigitalSignature only, Code Signing EKU1.3.6.1.5.5.7.3.3,
end-entity; private key available, CNG export policy None/nonexportable. Only public metadata
and availability/policy checks recorded; no PFX/private-key/password export or creation.
Production signing identity not used.

Existing SDK10.0.26100.0 x64 SignTool, exit0:
`signtool sign /fd SHA256 /s My /sha1 D6245FB640D520EDED8F8A987B364BCADE01D01D "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5o-signing\20261017-190225-a21c9a46\NativeDiagnostics.D06-SRV01.0.2.3.0.signed.appx"`.
SHA1 selects the certificate by its approved thumbprint; signing digest is SHA256.
No timestamp request/server. Exclusive local SIGN-ATTEMPT.lock prevents accidental helper
rerun signing again; do not remove it to retry. No accepted diagnostic was rebuilt or re-signed.

## Independent post-sign checks

| Verification | Result |
|---|---|
| CMS mathematics | PASS, SignedCms.CheckSignature(true), one nominated signer, SHA256 digest OID2.16.840.1.101.3.4.2.1 |
| APPX content digest | PASS, public Windows SIP CryptSIPVerifyIndirectData checks signed indirect content against exact package |
| Negative control | In-memory expected digest mutation rejected0x80096010; package bytes never changed |
| Payload preservation | All12 original members other than Content_Types byte-identical, including blockmap; no original member removed |
| Added metadata | Only AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat, plus matching two Content_Types declarations |
| Blockmap | All11 payload files checked:64KiB SHA256 blocks, whole-file hashes when present, sizes and local header sizes |
| Independent build pins | All6 role hashes match approved unsigned build; native imports, v4 schema, explicit SRV policy and native-only inventory unchanged |
| Trust stores | CurrentUser/LocalMachine Root/TrustedPeople inventories unchanged; no import/repair/security-setting operation |

CMS signature-only mode tests integrity independently of chain trust; it is not a certificate
import, trust-setting bypass or deployment acceptance. Read-only verification helper uses
platform cryptographic APIs, never loads the diagnostic executable or a target graphics DLL.
The structured APPX SIP digest blob is not the ordinary full-file SHA256 above.

Separate normal command: `signtool verify /pa /v "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5o-signing\20261017-190225-a21c9a46\NativeDiagnostics.D06-SRV01.0.2.3.0.signed.appx"`.
Exit1; one error, zero warnings; log says chain terminated at an untrusted root.
Read-only cache-only WinVerifyTrust independently returns0x800B0109/CERT_E_UNTRUSTEDROOT.
This is **failed chain verification**, retained without changing trust. Integrity checks found
no package corruption. Host trust failure neither proves nor guarantees Xbox package acceptance.
File is not timestamped; no timestamp-based post-expiry validation is claimed.

## Evidence and remaining risks/gates

SIGNING-VERIFICATION.json, VERIFICATION-SUMMARY.json, SIGNED-PAYLOAD-VERIFICATION.json,
SIGNED-MANIFEST.xml, UNSIGNED-PREFLIGHT.json and both SignTool logs provide exact outputs.
Source checkout remains clean. Original unsigned artifact and all preserved baseline hashes
remain unchanged after documentation.

Next separate approval: **one owner-operated installation-only0.2.2.0 ->0.2.3.0 update**,
using exact signed path/hash and no auto-launch. It replaces registered RES01a diagnostic
version and may retain stale LocalState/receipts. If side-by-side installed RES01a must remain,
approve a separate package identity/build first; do not change identity at deployment.
OWNER-INSTALLATION-ONLY.md supplies staged owner procedure/stop conditions.

Unresolved: normal desktop chain trust failed; console classification/installation/API/loader
behavior for0.2.3.0 not observed; no hardware SRV result or persistence proof. GPU/GetDesc/
release/file calls cannot be cancelled by observational watchdog; memory samples are not peak/
leak guarantees and platform MessageDialog has inherited async limits. No rendering, sampling,
presentation, OpenGL, LWJGL, Java/JNI or Minecraft compatibility established. Execution,
read-only receipt retrieval and cleanup each require separate approval after installation.
