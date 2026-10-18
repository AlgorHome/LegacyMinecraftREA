# Dedicated diagnostic certificate workflow — future owner action only

**NOT EXECUTED. Current authorization permits preparation, not any write below.**
The private key belongs in the owner's Windows key store, nonexportable and outside
Git, Xbox, chat, transfer media and package payload. Never reuse production keys.
Subject must match the unchanged manifest publisher: CN=LegacyForgeDiagnostics.

After separate certificate-creation approval, owner creates locally:

```powershell
$cert = New-SelfSignedCertificate -Type Custom -Subject 'CN=LegacyForgeDiagnostics' `
 -FriendlyName 'LegacyForge D00 Diagnostic Development' `
 -CertStoreLocation 'Cert:\CurrentUser\My' `
 -Provider 'Microsoft Software Key Storage Provider' `
 -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 `
 -KeyExportPolicy NonExportable -KeyUsage DigitalSignature `
 -TextExtension @('2.5.29.37={text}1.3.6.1.5.5.7.3.3','2.5.29.19={text}')
$cert | Select-Object Subject,Thumbprint,NotBefore,NotAfter,HasPrivateKey
```

Confirm subject, valid dates, RSA2048/SHA256, DigitalSignature, Code Signing EKU,
end-entity Basic Constraints and HasPrivateKey locally. Key export policy can be
checked as provider metadata without exporting any private bytes:

```powershell
# Future inspection of the owner-created certificate only:
$rsa = [Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
try {
 if ($rsa -isnot [Security.Cryptography.RSACng]) { throw 'Unexpected key provider' }
 if ($rsa.Key.ExportPolicy -ne [Security.Cryptography.CngExportPolicies]::None) { throw 'Key is not strictly nonexportable' }
 'PASS: nonexportable provider policy'
} finally { if ($rsa) { $rsa.Dispose() } }
```

No export test, Export-PfxCertificate or password argument is needed. Share only
public subject/thumbprint/validity and inspection outcome if requested. No signer
has been created or nominated by this preparation run.

After **separate signing approval**, use an explicitly nominated store certificate
and fresh output copy. Preserve unsigned hash
`ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558`.
The SHA1 selector below is a certificate thumbprint, not the file digest algorithm:

```powershell
# Future only. First copy verified unsigned APPX to a fresh signed output path.
$thumbprint = '<APPROVED-DIAGNOSTIC-CERTIFICATE-THUMBPRINT>'
$signed = '<FRESH-APPX-COPY-FULL-PATH>'
if ($thumbprint -like '<*' -or $signed -like '<*') { throw 'BLOCKED: unresolved signing inputs' }
$tool = 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe'
& $tool sign /fd SHA256 /s My /sha1 $thumbprint $signed
if ($LASTEXITCODE -ne 0) { throw 'Signing failed' }
& $tool verify /pa /v $signed
if ($LASTEXITCODE -ne 0) { throw 'Verification blocked; no implicit trust change' }
Get-FileHash -LiteralPath $signed -Algorithm SHA256
```

Use the full pre-sign input/subject/validity guards in the existing
[signing checklist](../phase-6b3-xbox-readiness/SIGNING-AND-DEPENDENCIES.md).
Record new signed hash, certificate metadata and unchanged original ZIP payload
bytes. A self-signed key can require an owner-approved public-certificate trust
plan for local verification; failed verification is not permission to change trust
automatically. No PFX/key is transferred. Xbox's documented Portal install contract
does not require the separate signing-certificate upload used by Desktop/IoT;
do not invent a console TrustedPeople import step or bypass any console error.

References: [Microsoft certificate requirements](https://learn.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing),
[SignTool workflow](https://learn.microsoft.com/en-us/windows/msix/package/sign-app-package-using-signtool).
