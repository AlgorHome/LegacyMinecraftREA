# Phase 6B.3e — read-only signing trust investigation

2026-10-17, America/Chicago. **Package signature/content integrity PASS; Windows
default certificate-chain trust FAIL (expected untrusted self-signed certificate).
Xbox acceptance remains UNKNOWN and no deployment is authorized.**

## Exact artifacts and verification failure

- Signed APPX SHA256:
  `51e5c74462e79a296335beab4830f479e861e7132e0f660c680f6974d3b27530`.
- Original unsigned APPX SHA256:
  `ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558`.
- Nominated certificate: `D6245FB640D520EDED8F8A987B364BCADE01D01D`.
- Original command:
  `"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe" verify /pa /v "C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b3d-signing\20261017-132111-5ff08807\RuntimeDiagnostics.D00.signed.appx"`.
- Original exit code **1**, zero verified files, one error: chain terminates at an
  untrusted root. Its original log prints the message rather than a numeric HRESULT.
- Read-only reproduction adding `/debug`: exit **1**, same error. Normal Windows
  WinVerifyTrust Generic Verify V2, cache-only/no revocation network check, returns
  **0x800B0109 / CERT_E_UNTRUSTEDROOT**, establishing the exact chain error.
- No RFC3161 timestamp is present; the certificate is presently within validity.

Microsoft identifies that HRESULT in its [signature troubleshooting guidance](https://learn.microsoft.com/en-us/windows/msix/msix-troubleshooting-guide#certificate-not-trusted-0x800b0109).
The very long value SignTool labels as the file hash is APPX's structured subject
digest, not the raw whole-file SHA256. The raw hashes above were measured separately.

## Independent cryptographic integrity — PASS

Two supported read-only checks were applied to the embedded signature and file:

1. .NET `SignedCms.Decode` followed by **CheckSignature(true)** verifies the CMS
   signature and signed attributes while deliberately not validating certificate
   trust. Exactly one embedded signer matches the owner-approved thumbprint and
   uses SHA256. This is an inspection result, not deployment trust approval.
2. Windows `CryptDecodeObjectEx` decodes that cryptographically verified signed
   indirect content; `CryptSIPRetrieveSubjectGuid` identifies the APPX SIP;
   **CryptSIPVerifyIndirectData** verifies the on-disk package against the signed
   subject digest. It returns true. This closes the gap between verifying only a
   CMS envelope and checking the package content to which that envelope refers.

As a negative control, one actual hash byte (offset8, after the APPX/AXPC headers)
was changed **only in the allocated expected-digest buffer**. The same Windows SIP
rejected it with **0x80096010 / TRUST_E_BAD_DIGEST**. The buffer was restored/freed;
no file, signature, certificate or store was modified. The initial exploratory
control changed a format byte and returned ERROR_BAD_FORMAT; the retained final
control preserves headers and tests a mismatched digest instead.

Supported contracts: [SignedCms signature-only mode](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.pkcs.signedcms.checksignature?view=windowsdesktop-9.0),
[CryptSIPVerifyIndirectData](https://learn.microsoft.com/en-us/windows/win32/api/mssip/nf-mssip-cryptsipverifyindirectdata),
[SIP subject information](https://learn.microsoft.com/en-us/windows/win32/api/mssip/ns-mssip-sip_subjectinfo).
These APIs inspect cryptographic data, not diagnostic executable code. No APPX
installation/registration or target module execution was used.

## Public certificate and chain observations

| Property | Observation |
|---|---|
| Subject / issuer | CN=LegacyForgeDiagnostics / CN=LegacyForgeDiagnostics |
| Thumbprint | D6245FB640D520EDED8F8A987B364BCADE01D01D |
| Validity UTC | 2026-10-17T17:58:48Z through 2027-10-17T18:08:48Z |
| EKU | Code Signing, 1.3.6.1.5.5.7.3.3 |
| Key usage | DigitalSignature |
| Basic Constraints | End entity, CA=false |
| Embedded signer digest | SHA256, 2.16.840.1.101.3.4.2.1 |
| Default X509Chain build | false; one element; UntrustedRoot |
| Chain policy used | NoFlag, Code Signing EKU; certificate downloads disabled; revocation not checked |
| CurrentUser Root / TrustedPeople | Nominated certificate absent; store thumbprint inventories unchanged |
| LocalMachine Root / TrustedPeople | Nominated certificate absent; store thumbprint inventories unchanged |

Public signer data came from the signed package; no private-key handle was opened
or exported during this investigation. The previously verified nonexportable
CurrentUser/My key was neither replaced nor modified. Certificate-chain trust,
revocation status and package integrity are separate properties; no fresh online
revocation guarantee is claimed.

## Four distinct decisions

| Decision | Meaning and current result |
|---|---|
| Signature integrity | The pinned signer's cryptographic signature authenticates the package digests and the file matches them: **PASS**. |
| Certificate-chain trust | The verifier's policy accepts the signing identity/chain: **FAIL** under this PC's unchanged default policy. A self-issued certificate is not automatically trusted. |
| Windows desktop trust configuration | My is key/certificate storage, not deployment trust. Desktop development package guidance uses **TrustedPeople** for a nominated test signer. No import occurred. |
| Xbox Developer Mode acceptance | A decision made by that console's deployment policy/build/dependencies and actual package installation: **UNKNOWN/NOT TESTED**. Windows /pa failure neither proves Xbox rejection nor establishes Xbox acceptance. |

Microsoft's [development signing guidance](https://learn.microsoft.com/en-us/windows/win32/appxpkg/how-to-sign-a-package-using-signtool)
recommends TrustedPeople for test package signers. Its current troubleshooting
guidance warns against putting a non-CA signing certificate in Trusted Root.
The [Device Portal install contract](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#install-an-app)
distinguishes Xbox from Desktop/IoT: Xbox does not require the separate signing
certificate upload described for those platforms. That request-body distinction
is **not** a promise to accept every self-signed package. The Portal HTTPS identity
is also separate from the APPX code-signing identity. No console was contacted.

## Least-privileged route and remaining gates

**No Trusted Root import is necessary for the remaining read-only Windows integrity
verification: it has already passed without any trust changes.** Do not promote
this end-entity diagnostic signer to a root merely to turn a host policy check green.

Keep normal SignTool /pa trust recorded as FAIL. Use the explicit approved signer
thumbprint, supported CMS/SIP integrity results, preserved payload comparison and
exact hashes as the local evidence. If Windows desktop installation/trust validation
is later required, obtain separate approval for Microsoft's appropriate scoped
test-signer trust procedure on the intended test machine, rather than changing the
production host now. This investigation does not prove what a future trust-store
configuration would return.

For Xbox, first obtain separately authorized owner-operated dependency inventory;
its framework state remains UNKNOWN. Confirm licensing conditions and exact verified
framework bytes if upload is actually needed. A later controlled installation of
the exact signed diagnostic is the way to observe console package acceptance, only
after separate console-access/installation approval. Launch, retrieval and overall
D00 acceptance remain separate subsequent gates. No re-signing, certificate
replacement, manifest change, desktop installation or new runtime is indicated
by the observed untrusted-root error alone.

## Preservation and evidence

Pinned source4101f7e/reviewdf23adb, D00-only executable/manifest/inventory and
separate identity remain unchanged. VCLibs SHA256 remains
`9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283`.
No certificates created, stores changed, packages signed/installed, dependencies
deployed, Xbox/Portal accessed, diagnostic launched, authentication/entitlements
altered or production code changed.

Evidence: [cryptographic checks](CRYPTOGRAPHIC-CHECKS.json),
[read-only helper source](ReadOnlySignatureChecks.cs),
[SignTool reproduction](signtool-debug.log),
[preservation results](PRESERVATION-EVIDENCE.json).
