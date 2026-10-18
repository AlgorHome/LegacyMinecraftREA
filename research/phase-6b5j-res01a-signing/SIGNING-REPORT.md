# Phase 6B.5j — D06-RES01a local signing and verification

**Signing PASS. CMS/APPX content/payload/blockmap integrity PASS.**
**Normal Windows chain trust FAIL: CERT_E_UNTRUSTEDROOT0x800B0109.**
No source, certificate, trust setting, dependency, installed application or console was changed.
No diagnostic binary was executed; hardware status remains NOT EXECUTED.

Source commit `4457142ff1fd9e01371eb446612c70162ce93357`, clean research/phase6b5i-d06-res01a checkout.
Unsigned path `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-183031-15ba7835\NativeCapabilities.unsigned.appx`.
Approved unsigned SHA256 **526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8**, matched before/after signing.
Signed path **`C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5j-signing\20261017-183700-68e8cd8f\NativeDiagnostics.D06-RES01a.0.2.2.0.signed.appx`**.
Signed SHA256 **ead7016c94e551fac43e2b622b323354bfa4506fe507f44bf5e98f112b8f0c3f**.
Exactly one fresh copy and one signing invocation; original unsigned package unchanged.
No timestamp server used, no timestamp claim after certificate expiry.

## Pre-sign confirmation

Fresh static audit UNSIGNED-PREFLIGHT.json matches the approved Phase6B.5i build evidence:
source/build identity, complete package allowlist, actual payload hashes, native imports,
case policy, receipt v3, three preprocessed native units/Java exclusion, one hardware
D3D11 device callsite and one texture callsite. No rebuild was performed. Eight valid and
thirty invalid synthetic receipt-contract checks remain offline validation, not hardware tests.

| Property | Verified |
|---|---|
| Identity | AlgorHome.LegacyForge.NativeDiagnostics |
| Publisher | CN=LegacyForgeDiagnostics |
| Version/architecture |0.2.2.0 /x64 |
| Application/entry point | App /LegacyForgeNativeDiagnostics.App |
| Capabilities | None declared |
| Startup | MTA/CoreApplication unchanged |
| Single case | D06-RES01a; previous case dispatches/macros excluded, Java/JNI compile locks retained |
| Xbox classification | App required at later owner inventory; not equivalent to manifest Application Id App, and not independently observable without console access |
| Dependencies | Unchanged Windows.Universal min10.0.17763.0/max-tested10.0.26100.0 and Microsoft.VCLibs.140.00 min14.0.0.0/Microsoft publisher; no bundled framework |

Intended operation remains exactly one hardware-only1x1 RGBA8 texture creation with
null initial data, nonnull output storage, DEFAULT usage/SHADER_RESOURCE bind flag,
one mip/array element, sample1/quality0, CPU/misc0. Only S_OK+nonnull leads to one
GetDesc; every11 defined scalar fields compared exactly. S_FALSE is not allocation success.
Scoped texture/device/context/adapter refs release; no texture initialization/content read,
shader view, render target, shader/compiler, draw/clear/copy/map/readback, swapchain,
presentation, fallback, operation sweep or Java/Minecraft content. Actual driver overhead
and blocked calls are not strictly capped/cancellable. Target behavior remains untested.

## Nominated certificate and signing

Cert:\CurrentUser\My\D6245FB640D520EDED8F8A987B364BCADE01D01D;
subject/issuer CN=LegacyForgeDiagnostics. Current validity checked:
2026-10-17T17:58:48Z through2027-10-17T18:08:48Z. RSA2048, sha256RSA,
DigitalSignature only, Code Signing EKU1.3.6.1.5.5.7.3.3, end-entity.
Private key availability verified; CNG export policy None/nonexportable. No key/PFX/password
export, certificate creation/replacement or production signing identity used.

Existing SDK10.0.26100.0 x64 SignTool, exit0:
`signtool sign /fd SHA256 /s My /sha1 D6245FB640D520EDED8F8A987B364BCADE01D01D "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5j-signing\20261017-183700-68e8cd8f\NativeDiagnostics.D06-RES01a.0.2.2.0.signed.appx"`.
SHA1 selects the certificate thumbprint; file/CMS digest is SHA256. Local exclusive
SIGN-ATTEMPT.lock prevents rerunning this helper to create a second signature attempt.

## Post-sign verification

| Check | Result |
|---|---|
| CMS signature | PASS, SignedCms.CheckSignature(true), one nominated signer, SHA256 digest |
| APPX content digest | PASS, Windows package SIP CryptSIPVerifyIndirectData against signed indirect content |
| Negative control | Altered expected digest only in allocated memory rejected0x80096010; no package bytes modified |
| Payload preservation | PASS, all12 original members other than Content_Types byte-identical, including blockmap; no removed member |
| Expected signing metadata | Only AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat added; two matching Content_Types declarations |
| Blockmap | PASS all11 payload files;64KiB block hashes, sizes/local headers and whole-file hash extensions when present |
| Independent pins | All6 role hashes match approved unsigned build; signed native imports identical; schema v3 and texture policy/descriptor unchanged |
| Frozen baselines | All107 required pins match before/after; total118 prior artifact/evidence files reverified, including unsigned package and Phase6B.5i dossier |
| Trust inventories | CurrentUser/LocalMachine Root/TrustedPeople inventories unchanged; no trust repair/import |

CMS signature-only verification establishes mathematics independently of trust; it is
not a certificate import, policy change or Xbox deployment guarantee. SIP digest blob
in logs is the APPX structured content digest; approved full-file SHA256 is the64-digit
value above. SIGNED-PAYLOAD-VERIFICATION.json lists every unchanged member/check.

Separate standard command: `signtool verify /pa /v "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5j-signing\20261017-183700-68e8cd8f\NativeDiagnostics.D06-RES01a.0.2.2.0.signed.appx"`.
Exit **1**, log reports chain terminates at an untrusted root. Read-only cache-only
WinVerifyTrust returns **0x800B0109 /CERT_E_UNTRUSTEDROOT**. Chain trust is FAIL,
not silently converted to PASS; integrity checks found no package corruption. Host policy
result alone neither proves nor guarantees Xbox acceptance. No security-setting change.

Evidence: SIGNING-VERIFICATION.json, VERIFICATION-SUMMARY.json,
SIGNED-PAYLOAD-VERIFICATION.json, SIGNED-MANIFEST.xml, UNSIGNED-PREFLIGHT.json,
signtool-sign.log, signtool-verify.log. Helpers document exact one-attempt signing and
read-only payload verification; no source checkout or accepted evidence file changed.

## Remaining approval gates

Next: owner-operated **installation-only update** naming this exact signed path/hash.
It would replace NativeDiagnostics0.2.1.0 registration, potentially retaining stale
HW01/FMT01 receipts and LocalState. Accepted artifacts/evidence remain archived; do not
clear storage. If side-by-side installed FMT01 is needed, approve a distinct package first.
See OWNER-INSTALLATION-ONLY.md. No Portal access made during this phase.

One launch, diagnostic-only receipt retrieval and cleanup each need separate approval.
No hardware texture allocation, rendering, presentation, OpenGL, LWJGL, Java/JNI or
Minecraft compatibility result is claimed by signing verification.
