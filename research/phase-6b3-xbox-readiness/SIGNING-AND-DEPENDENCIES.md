# Exact owner checklist: diagnostic signing and UWP dependencies

**Future owner procedure only. No commands in this document were executed.**
Stop at each missing input or failed check. No private material through chat.

## Signing inputs

- Approved unsigned APPX SHA256:
  `ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558`.
- Publisher/subject exactly `CN=LegacyForgeDiagnostics`; separate from production.
- Owner-controlled local certificate store key; validity at signing; DigitalSignature
  usage; Code Signing EKU1.3.6.1.5.5.7.3.3; end-entity certificate, not a CA.
- Explicit certificate thumbprint, not automatic /a selection; no PFX export,
  password argument, private key copy, repository certificate/key or production key.
- SDK10.0.26100.0 x64 SignTool exists locally; SHA256
  `431ee314c83988cacda86606356fd321b75ae0093481b97e3b738e99c412f2a0`.
- BlockMap algorithm is SHA256, so SignTool uses /fd SHA256. Certificate selector
  /sha1 denotes its thumbprint; it does not select SHA1 package signing.

Microsoft documents [subject/usage requirements](https://learn.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing)
and [hash matching/store-based signing](https://learn.microsoft.com/en-us/windows/msix/package/sign-app-package-using-signtool).
The following adapts the certificate recipe to a dedicated **nonexportable** key.
Use only after explicit certificate/signing approval, in the owner's local store:

```powershell
# FUTURE ONLY. Creates a new diagnostic key/certificate, never a production one.
$cert = New-SelfSignedCertificate -Type Custom -Subject 'CN=LegacyForgeDiagnostics' `
 -FriendlyName 'LegacyForge D00 Diagnostic Development' -KeyUsage DigitalSignature `
 -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -KeyExportPolicy NonExportable `
 -CertStoreLocation 'Cert:\CurrentUser\My' `
 -TextExtension @('2.5.29.37={text}1.3.6.1.5.5.7.3.3','2.5.29.19={text}')
$cert | Select-Object Subject,Thumbprint,NotBefore,NotAfter,HasPrivateKey
```

An existing dedicated suitable signer can be nominated instead. No matching signer
was found during preparation. Public subject/thumbprint/validity are review inputs;
private key files or credentials are neither needed nor requested.

```powershell
# FUTURE ONLY, after the owner explicitly approves signing this pinned input.
$unsigned = '<PINNED-UNSIGNED-APPX-FULL-PATH>'
$signed = '<FRESH-SIGNED-APPX-FULL-PATH>'
$thumbprint = '<APPROVED-DIAGNOSTIC-CERTIFICATE-THUMBPRINT>'
if ($unsigned -like '<*' -or $signed -like '<*' -or $thumbprint -like '<*') { throw 'BLOCKED: unresolved signing inputs' }
$tool = 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe'
if ((Get-FileHash -LiteralPath $unsigned -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558') { throw 'Unsigned input hash mismatch' }
if ([IO.Path]::GetFullPath($unsigned) -eq [IO.Path]::GetFullPath($signed) -or (Test-Path -LiteralPath $signed)) { throw 'Preserve original; choose a fresh signed path' }
$cert = Get-Item -LiteralPath ('Cert:\CurrentUser\My\' + $thumbprint) -ErrorAction Stop
if ($cert.Subject -ne 'CN=LegacyForgeDiagnostics' -or -not $cert.HasPrivateKey -or $cert.NotBefore -gt (Get-Date) -or $cert.NotAfter -le (Get-Date)) { throw 'Wrong/unusable signer' }
# Owner confirms EKU, DigitalSignature and end-entity status before continuing.
Copy-Item -LiteralPath $unsigned -Destination $signed
& $tool sign /fd SHA256 /s My /sha1 $thumbprint $signed
if ($LASTEXITCODE -ne 0) { throw 'Signing failed; no deployment' }
& $tool verify /pa /v $signed
if ($LASTEXITCODE -ne 0) { throw 'Signature/chain verification blocked; preserve output and stop' }
Get-FileHash -LiteralPath $signed -Algorithm SHA256
```

A development self-signed certificate may not be trusted by the signing PC.
Verification failure remains BLOCKED; do not ignore it, export keys or silently
import anything into host trust. Owner may separately approve public-certificate
trust on an appropriate verification machine or provide an already suitable signer.
That local verification policy is not an assertion that Xbox needs a certificate
upload. No timestamp service is selected implicitly; record certificate validity
and any separately approved timestamp policy.

After signing, compare every original ZIP payload file against the unsigned APPX
and record the new signed hash, signer metadata, verification results and added
signature metadata. Preserve name/publisher/version/x64/capabilities. Do not rebuild
or repack to change identity. The old unsigned hash does not identify the signed file.

Xbox Device Portal's [install contract](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#install-an-app)
does not require Xbox to receive the separate .cer payload specified for Desktop/
IoT. Never upload a PFX or private key. If current console behavior differs, stop
and record its error/build; do not invent a console certificate UI or bypass trust.

## Exact framework gate

| Field | Required verification |
|---|---|
| Name | Microsoft.VCLibs.140.00; **not** Microsoft.VCLibs.140.00.UWPDesktop |
| Architecture | x64 UWP retail framework for this x64 release app; not x86/ARM/debug DLLs |
| Version | >=14.0.0.0 manifest floor; additionally supplies all imported UWP CRT symbols |
| Publisher | CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US |
| Framework | Package Properties/Framework=true |
| Source/license | Original Microsoft Visual Studio UWP redistributable/authorized Microsoft channel; record acquisition and applicable redistribution terms |
| Byte identity | SHA256 of the actual unmodified APPX; no candidate file exists yet |
| Signature | Microsoft signature and valid verification chain; matching Publisher XML alone is insufficient |
| Content | Original MSVCP140_APP.dll, VCRUNTIME140_APP.dll, VCRUNTIME140_1_APP.dll and their required exports; inspect metadata/import closure without loading DLLs |
| Console state | Owner confirms exact installed framework or supplies verified candidate; host installation is not console proof |

Host inventory shows Store-signed Microsoft.VCLibs.140.00 14.0.33519.0 X64/X86,
but it is not a distributable APPX candidate. No extraction/repackaging from
WindowsApps is permitted by this plan. Never substitute a VC_redist.exe,
third-party mirror, emulator dependency ZIP or arbitrary DLL download.

For a future owner-supplied original APPX, inspect it as ZIP data, hash it, verify
manifest/architecture/framework/contents and run SDK SignTool **verification only**:

```powershell
# Future candidate verification only; does not install or execute its payload.
$dependency = '<ORIGINAL-MICROSOFT-X64-UWP-VCLIBS-APPX>'
if ($dependency -like '<*') { throw 'BLOCKED: framework artifact unavailable' }
Get-FileHash -LiteralPath $dependency -Algorithm SHA256
& 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe' verify /pa /v $dependency
if ($LASTEXITCODE -ne 0) { throw 'Dependency signature/provenance blocked' }
```

Record the actual Microsoft signer/chain and hash. Signature validation establishes
authenticity/integrity, not all licensing or Xbox runtime compatibility. OS graphics
and Windows API sets are console platform requirements; no extra runtime package
is invented for them. A dependency already installed with sufficient identity and
exports may remove the upload requirement, after owner verification.
