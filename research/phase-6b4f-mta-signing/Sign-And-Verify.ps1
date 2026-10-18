# One authorized fresh-copy signing attempt; no installation, trust changes or target execution.
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$researchRoot = 'C:\Users\arinze\Desktop\ReverseLegacyCraft'
$repoRoot = Join-Path $researchRoot 'phase6b1-diagnostics'
$buildRoot = Join-Path $repoRoot 'diagnostics\RuntimeDiagnostics\out\20261017-142300-e07d5ee8'
$unsigned = Join-Path $buildRoot 'RuntimeDiagnostics.unsigned.appx'
$expected = '0595e9936aa4091ebdcce3e23b4e43fdba014d88267b4aaa0656fbd9cddb307e'
$approvedCommit = '553c6554f40f1372b0ea09f6badbbb98e133a9ab'
$thumb = 'D6245FB640D520EDED8F8A987B364BCADE01D01D'
$signTool = 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe'
function Hash-File([string]$path) { (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
if ((Hash-File $unsigned) -ne $expected) { throw 'Unsigned hash mismatch' }
$commit = (& git -C $repoRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $commit -ne $approvedCommit) { throw 'Source commit mismatch' }
$changes = & git -C $repoRoot status --porcelain
if ($LASTEXITCODE -ne 0 -or $changes) { throw 'Source checkout not clean' }
$buildReceipt = Get-Content -LiteralPath (Join-Path $buildRoot 'build-receipt.json') -Raw | ConvertFrom-Json
if ($buildReceipt.sourceCommit -ne $approvedCommit -or !$buildReceipt.d00Only -or $buildReceipt.status -ne 'BUILD_STATIC_CHECK_PASS_NOT_EXECUTED') { throw 'Build provenance mismatch' }
$staticAudit = Get-Content -LiteralPath (Join-Path $buildRoot 'd00-safety-audit.json') -Raw | ConvertFrom-Json
if ($staticAudit.verdict -ne 'PASS' -or $staticAudit.capabilities.Count -ne 0 -or $staticAudit.identity.Version -ne '0.1.3.0') { throw 'D00 safety audit mismatch' }
$preflightArchive = [IO.Compression.ZipFile]::OpenRead($unsigned)
try {
    $preflightReader = [IO.StreamReader]::new($preflightArchive.GetEntry('AppxManifest.xml').Open())
    try { $preflightManifest = [xml]$preflightReader.ReadToEnd() } finally { $preflightReader.Dispose() }
    if ($preflightManifest.Package.Identity.Name -ne 'AlgorHome.LegacyForge.RuntimeDiagnostics' -or $preflightManifest.Package.Identity.Publisher -ne 'CN=LegacyForgeDiagnostics' -or $preflightManifest.Package.Identity.Version -ne '0.1.3.0' -or $preflightManifest.Package.Identity.ProcessorArchitecture -ne 'x64' -or $preflightManifest.Package.Applications.Application.EntryPoint -ne 'LegacyForgeDiagnostics.App') { throw 'Manifest identity/activation mismatch' }
} finally { $preflightArchive.Dispose() }
$cert = Get-Item -LiteralPath ('Cert:\CurrentUser\My\'+$thumb)
if ($cert.Thumbprint -ne $thumb -or $cert.Subject -ne 'CN=LegacyForgeDiagnostics' -or !$cert.HasPrivateKey) { throw 'Nominated certificate mismatch' }
if ((Get-Date) -lt $cert.NotBefore -or (Get-Date) -gt $cert.NotAfter) { throw 'Certificate not currently valid' }
$ekuExtension = $cert.Extensions | Where-Object {$_.Oid.Value -eq '2.5.29.37'}
$eku = @($ekuExtension.EnhancedKeyUsages | ForEach-Object {$_.Value})
if ('1.3.6.1.5.5.7.3.3' -notin $eku) { throw 'Code Signing EKU missing' }
$usage = $cert.Extensions | Where-Object {$_.Oid.Value -eq '2.5.29.15'}
if (!$usage -or $usage.KeyUsages -ne [Security.Cryptography.X509Certificates.X509KeyUsageFlags]::DigitalSignature) { throw 'Unexpected key usage' }
$basic = $cert.Extensions | Where-Object {$_.Oid.Value -eq '2.5.29.19'}
if (!$basic -or $basic.CertificateAuthority) { throw 'Not an end-entity certificate' }
$rsa = [Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
try {
    if ($rsa.KeySize -ne 2048 -or $rsa -isnot [Security.Cryptography.RSACng] -or $rsa.Key.ExportPolicy -ne [Security.Cryptography.CngExportPolicies]::None) { throw 'Unexpected key properties/nonexportable policy' }
    $keyMetadata = @{keySize=$rsa.KeySize;exportPolicy=$rsa.Key.ExportPolicy.ToString();provider=$rsa.Key.Provider.Provider}
} finally { if ($rsa) { $rsa.Dispose() } }
$preserved = @(
    (Join-Path $researchRoot 'analysis-local\phase6b3d-signing\20261017-132111-5ff08807\RuntimeDiagnostics.D00.signed.appx'),
    (Join-Path $repoRoot 'diagnostics\RuntimeDiagnostics\out\20261017-122521-8ece767b\RuntimeDiagnostics.unsigned.appx'),
    (Join-Path $researchRoot 'docs\research\phase-6b3c-certificate\CERTIFICATE-PUBLIC-METADATA.json'),
    (Join-Path $researchRoot 'docs\research\phase-6b4a-activation-investigation\OWNER-OBSERVATIONS.json'),
    (Join-Path $researchRoot 'analysis-local\phase6b4c-signing\20261017-140847-c38e9c14\RuntimeDiagnostics.D00.ActivationExperiment.0.1.2.0.signed.appx'),
    (Join-Path $repoRoot 'diagnostics\RuntimeDiagnostics\out\20261017-140332-19d39263\RuntimeDiagnostics.unsigned.appx'),
    (Join-Path $researchRoot 'docs\research\phase-6b4d-activation-triage\OBSERVATIONS.json'),
    (Join-Path $researchRoot 'analysis-local\phase6b4e-evidence-retrieval\OWNER-INVENTORY.json'),
    $unsigned
)
$before = @($preserved | ForEach-Object { @{path=$_;sha256=(Hash-File $_)} })
function Trust-Snapshot {
    $items = foreach ($store in @('Cert:\CurrentUser\Root','Cert:\CurrentUser\TrustedPeople','Cert:\LocalMachine\Root','Cert:\LocalMachine\TrustedPeople')) {
        @{store=$store;thumbprints=@(Get-ChildItem -LiteralPath $store | ForEach-Object Thumbprint | Sort-Object)}
    }
    $items | ConvertTo-Json -Depth 4 -Compress
}
$trustBefore = Trust-Snapshot
$runName = (Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,8)
$runDir = Join-Path $researchRoot ('analysis-local\phase6b4f-signing\'+$runName)
New-Item -ItemType Directory -Path $runDir | Out-Null
$signed = Join-Path $runDir 'RuntimeDiagnostics.D00.MTAExperiment.0.1.3.0.signed.appx'
Copy-Item -LiteralPath $unsigned -Destination $signed
if ((Hash-File $signed) -ne $expected) { throw 'Fresh copy hash mismatch' }
$record = [ordered]@{sourceCommit=$commit;unsignedPath=$unsigned;unsignedSha256=$expected;signedPath=$signed;signAttempts=1;signerThumbprint=$thumb;certificate=@{subject=$cert.Subject;issuer=$cert.Issuer;thumbprint=$cert.Thumbprint;notBeforeUtc=$cert.NotBefore.ToUniversalTime().ToString('o');notAfterUtc=$cert.NotAfter.ToUniversalTime().ToString('o');eku=$eku;keyUsage=$usage.KeyUsages.ToString();endEntity=(!$basic.CertificateAuthority);signatureAlgorithm=$cert.SignatureAlgorithm.Value;key=$keyMetadata};signCommand='signtool sign /fd SHA256 /s My /sha1 <approved-thumbprint> <fresh-copy>';verifyCommand='signtool verify /pa /v <signed-copy>';targetExecuted=$false;consoleAccess=$false;trustChanged=$false}
function Save-Record { $record | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath (Join-Path $runDir 'SIGNING-VERIFICATION.json') -Encoding utf8 }
Save-Record
& $signTool sign /fd SHA256 /s My /sha1 $thumb $signed *> (Join-Path $runDir 'signtool-sign.log')
$record.signExitCode=$LASTEXITCODE
Save-Record
if ($record.signExitCode -ne 0) { throw 'Signing failed; do not retry' }
$record.signedSha256=Hash-File $signed
& $signTool verify /pa /v $signed *> (Join-Path $runDir 'signtool-verify.log')
$record.standardVerifyExitCode=$LASTEXITCODE
Save-Record
Add-Type -AssemblyName System.Security.Cryptography.Pkcs
Add-Type -Path (Join-Path $researchRoot 'docs\research\phase-6b3e-trust-investigation\ReadOnlySignatureChecks.cs')
$archive = [IO.Compression.ZipFile]::OpenRead($signed)
try {
    $signature = $archive.GetEntry('AppxSignature.p7x')
    $stream=$signature.Open(); $memory=[IO.MemoryStream]::new()
    try { $stream.CopyTo($memory); $bytes=$memory.ToArray() } finally { $stream.Dispose();$memory.Dispose() }
    if ([Text.Encoding]::ASCII.GetString($bytes,0,4) -ne 'PKCX') { throw 'APPX signature header mismatch' }
    $cms=[Security.Cryptography.Pkcs.SignedCms]::new()
    $cms.Decode([byte[]]$bytes[4..($bytes.Length-1)])
    $cms.CheckSignature($true)
    if ($cms.SignerInfos.Count -ne 1 -or $cms.SignerInfos[0].Certificate.Thumbprint -ne $thumb) { throw 'Embedded signer mismatch' }
    if ($cms.SignerInfos[0].DigestAlgorithm.Value -ne '2.16.840.1.101.3.4.2.1') { throw 'CMS digest is not SHA256' }
    $record.cmsIntegrity='PASS'
    $record.cmsDigestAlgorithm=$cms.SignerInfos[0].DigestAlgorithm.Value
    $record.packageDigest=[ReadOnlySignatureChecks]::VerifyPackageDigest($signed,$cms.ContentInfo.Content)
    if (!$record.packageDigest.FileDigestMatches -or !$record.packageDigest.MutatedExpectedDigestRejected) { throw 'APPX content digest verification failed' }
    $record.normalTrustCacheOnly=[ReadOnlySignatureChecks]::VerifyNormalTrustCacheOnly($signed)
    $manifestStream=$archive.GetEntry('AppxManifest.xml').Open();$reader=[IO.StreamReader]::new($manifestStream)
    try {$xml=[xml]$reader.ReadToEnd()} finally {$reader.Dispose()}
    $record.identity=@{name=$xml.Package.Identity.Name;publisher=$xml.Package.Identity.Publisher;version=$xml.Package.Identity.Version;architecture=$xml.Package.Identity.ProcessorArchitecture;applicationId=$xml.Package.Applications.Application.Id;entryPoint=$xml.Package.Applications.Application.EntryPoint}
} finally { $archive.Dispose(); Save-Record }
$record.preservedFiles=@($before | ForEach-Object { $current=Hash-File $_.path; if ($current -ne $_.sha256) { throw 'Original evidence mutated' }; @{path=$_.path;sha256=$current;unchanged=$true} })
$record.trustStoreInventoriesUnchanged=($trustBefore -ceq (Trust-Snapshot))
if (!$record.trustStoreInventoriesUnchanged) { throw 'Trust store inventory changed' }
$record.status='SIGNED_AND_CRYPTOGRAPHICALLY_VERIFIED_CHAIN_TRUST_REPORTED_SEPARATELY'
Save-Record
Write-Output ($record | ConvertTo-Json -Depth 9)

