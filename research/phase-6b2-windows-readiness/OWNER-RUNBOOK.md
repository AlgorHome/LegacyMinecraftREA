# Owner runbook: future isolated Windows D00 validation

**PREPARED ONLY. No signing, installation or activation is authorized yet.**
No guest has been selected. This is an exact parameterized procedure for an
owner-verified disposable Windows 11 x64 full VM, not a statement that such a VM
exists. Unresolved placeholders and failed checks are BLOCKED, never PASS.

## A. Select and verify the guest without starting the diagnostic

Owner/admin can first collect Hyper-V inventory read-only:

```powershell
Get-VM | Select-Object Name,State,Generation,Version,AutomaticStartAction
```

Choose only a disposable Windows 11 x64 VM with a locally controlled disposable
account and no personal credentials, production software/data, domain join,
Microsoft account, OneDrive or host filesystem shares. Do not repurpose a personal
VM. If none exists, creating/installing a VM requires an owner-approved setup and
licensed trusted Windows media; no VM or Windows download is performed here.

Set `$vmName` to the owner-confirmed exact name. All later host commands refer only
to that VM. Read these properties before changing anything:

```powershell
$vmName = '<OWNER-VERIFIED-DISPOSABLE-VM>'
if ($vmName -like '<*') { throw 'BLOCKED: no verified guest selected' }
$vm = Get-VM -Name $vmName -ErrorAction Stop
$vm | Select-Object Name,State,Generation,AutomaticStartAction
Get-VMNetworkAdapter -VMName $vmName | Select-Object Name,SwitchName,Status
Get-VMHardDiskDrive -VMName $vmName | Select-Object ControllerType,ControllerNumber,ControllerLocation,Path
Get-VMDvdDrive -VMName $vmName | Select-Object Path
Get-VMIntegrationService -VMName $vmName | Select-Object Name,Enabled
```

Use a basic VMConnect console; no Enhanced Session/RDP drive, clipboard, printer,
audio/video, USB or credential redirection. Do not paste host secrets. Inspect
session settings and guest file shares, and attest no personal credentials/data;
metadata alone cannot prove absence. Any GPU passthrough/GPU partitioning requires
its own owner-reviewed isolation configuration. Do not enable it implicitly.

Inside the selected guest, use guest-preflight.ps1 to collect read-only prerequisite
metadata. In the guest only, after confirming its context and allowing the reviewed
script under the owner's normal script policy:

```powershell
& C:\D00\Inputs\guest-preflight.ps1 -ConfirmedDisposableGuest
```

It never installs, signs, activates or executes the diagnostic. Review OS
x64/build, AppXSvc/policy and framework entries. Keep any local administrative
credentials inside the guest; do not send them through chat.

For graphics prerequisite evidence, the owner may use the guest's trusted system
DxDiag after approving guest inspection (not the diagnostic EXE):

```powershell
New-Item -ItemType Directory C:\D00\Prereq -Force | Out-Null
dxdiag.exe /whql:off /x C:\D00\Prereq\dxdiag.xml
```

Inspect D3D feature levels/driver/provider; redact machine/user/unique device IDs
before sharing. D00 requests D3D_DRIVER_TYPE_HARDWARE with 11_1/11_0/10_1/10_0.
Do not assume Microsoft Hyper-V Video, generic RDP or WARP supplies a suitable
hardware path. If unavailable, BLOCKED; do not alter the app or weaken isolation.
Driver/feature metadata supports preparation, not proof that device creation works.

## B. Plan signing locally — execute only after separate approval

Minimum inputs: pinned unsigned APPX; suitable owner-controlled code-signing
certificate/private-key access; subject exactly CN=LegacyForgeDiagnostics; valid
code-signing use/chain/time; SDK SignTool; owner-approved public certificate trust
in the guest; trusted x64 UWP Microsoft.VCLibs.140.00 >=14.0.0.0 if not installed.
The .UWPDesktop package and desktop VC redistributable EXE are not substitutes.
Record framework hash, signature, publisher, architecture and version.

Use an existing suitable signer, or have the owner create a dedicated nonexportable
development signer locally after approval. No PFX/private-key export is required.
Only the public certificate may be transferred to the guest. The key/password never
enters chat, the repository or the guest. No certificate is created by this report.

Example future signing sequence on the owner-controlled signing machine using
an explicitly nominated CurrentUser/My certificate (do not automatically select
the first certificate or use a production key):

```powershell
$unsigned = '<PINNED-UNSIGNED-APPX-FULL-PATH>'
$signed = '<NEW-SIGNED-APPX-FULL-PATH>'
$thumbprint = '<OWNER-SELECTED-THUMBPRINT>'
$signTool = 'C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe'
if ($unsigned -like '<*' -or $signed -like '<*' -or $thumbprint -like '<*') { throw 'BLOCKED: unresolved signing inputs' }
if ((Get-FileHash -LiteralPath $unsigned -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558') { throw 'Unsigned hash mismatch' }
if ([IO.Path]::GetFullPath($unsigned) -eq [IO.Path]::GetFullPath($signed)) { throw 'Preserve unsigned artifact' }
if (Test-Path -LiteralPath $signed) { throw 'Choose a fresh signed output path' }
$cert = Get-Item ('Cert:\CurrentUser\My\' + $thumbprint) -ErrorAction Stop
if ($cert.Subject -ne 'CN=LegacyForgeDiagnostics' -or -not $cert.HasPrivateKey) { throw 'Wrong signer' }
# Owner also verifies validity, Code Signing EKU and intended trust chain.
Copy-Item -LiteralPath $unsigned -Destination $signed
& $signTool sign /fd SHA256 /s My /sha1 $thumbprint $signed
if ($LASTEXITCODE -ne 0) { throw 'Signing failed' }
& $signTool verify /pa /v $signed
if ($LASTEXITCODE -ne 0) { throw 'Signature/chain verification blocked; no implicit trust-store change' }
Get-FileHash -LiteralPath $signed -Algorithm SHA256
```

A self-signed development signer may require owner-approved chain trust for
verification; failure is BLOCKED, not permission to change host trust automatically.
Record signed SHA256 and signer public metadata, and compare all original payload
bytes to the approved unsigned ZIP (signature metadata is additional). Signing
changes the APPX hash. Do not reuse the unsigned hash for the signed artifact.

Prepare an immutable ISO containing only the signed APPX, approved public signer
certificate, trusted framework APPX if needed, approved payload-hash evidence and
the guest-preflight.ps1 collector and these procedures. No private keys, Minecraft, launcher installer or runtime files.
Attach this read-only medium to the guest, copy to C:\D00\Inputs and detach it
before activation. This is not a shared host filesystem drive. No media prepared now.

## C. Snapshot, disconnect and install — future approval required

Record an exact clean checkpoint name and guest identity after verifying graphics,
account and isolation, before installing certificates/framework/diagnostic. Preserve
the owner-selected baseline; do not change production VMs or use wildcard names.
For the eventual approved run, disconnect **all** NICs on the selected VM at the
hypervisor and verify no SwitchName remains. Guest firewall alone is insufficient.

```powershell
# Host, only after approval, with the exact $vmName established above:
Checkpoint-VM -Name $vmName -SnapshotName 'D00-BEFORE-INSTALL-20261017'
Disconnect-VMNetworkAdapter -VMName $vmName
Get-VMNetworkAdapter -VMName $vmName | Select-Object Name,SwitchName,Status
```

Keep disconnected through installation, activation, receipt inspection and shutdown.
Do not reconnect for Store downloads or missing dependencies; stop BLOCKED instead.

In the guest's disposable user context, confirm no previous diagnostic package or
LocalState exists; stop and use a fresh baseline if there is one. After separately
approved trust/sideload changes, an elevated guest administrator may import only the
approved public signer certificate into LocalMachine/TrustedPeople. Confirm the
public certificate thumbprint first; do not create or import a private key in guest.

```powershell
# Future guest administration only; verify thumbprint before import:
Import-Certificate -FilePath C:\D00\Inputs\LegacyForgeDiagnostics.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople
```

Use the owner's approved Windows sideload/development policy. Do not enable Device
Portal, remote discovery or developer networking. With the signed hash already
verified, install only for the disposable user (not all-user provisioning):

```powershell
# Disposable guest user, not the host. Replace hash after signing approval.
$expectedSignedHash = '<APPROVED-SIGNED-SHA256>'
if ($expectedSignedHash -like '<*') { throw 'BLOCKED: signed artifact not approved' }
$appx = 'C:\D00\Inputs\RuntimeDiagnostics.signed.appx'
if ((Get-FileHash $appx -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedSignedHash.ToLowerInvariant()) { throw 'Signed artifact mismatch' }
if (Get-AppxPackage -Name AlgorHome.LegacyForge.RuntimeDiagnostics) { throw 'BLOCKED: use a clean guest' }
# Omit DependencyPath only if the verified matching x64 framework is installed:
Add-AppxPackage -Path $appx -DependencyPath C:\D00\Inputs\Microsoft.VCLibs.x64.14.00.appx -ErrorAction Stop
$pkg = @(Get-AppxPackage -Name AlgorHome.LegacyForge.RuntimeDiagnostics)
if ($pkg.Count -ne 1) { throw 'Package registration mismatch' }
$pkg = $pkg[0]
if ($pkg.Publisher -ne 'CN=LegacyForgeDiagnostics' -or $pkg.Version -ne [version]'0.1.1.0' -or $pkg.Architecture.ToString() -ne 'X64') { throw 'Wrong package' }
$pkg | Select-Object Name,Version,Architecture,Publisher,Status,PackageFamilyName
```

Registration is not an activation result. If registration fails, preserve its
sanitized HRESULT/ActivityId and record FAILED/BLOCKED; no retry with extra
capabilities, authentication, runtime payload or online dependency acquisition.

## D. Activate once and validate receipts — future run approval required

After independently confirming the hypervisor network remains disconnected and
input media detached, activate the exact registered diagnostic application:

```powershell
# Guest only, with $pkg from validated registration:
Start-Process explorer.exe -ArgumentList ('shell:AppsFolder\' + $pkg.PackageFamilyName + '!App')
```

D00 starts automatically. Use an external 30-second observation timer; D00 has no
automatic kill watchdog. Record the D00 ONLY display/status. Do not open another
EXE or test. On hang, close only that app via its window or shut down the disposable
guest; no wildcard/name-based process kill. Missing receipt means INCONCLUSIVE.

In the same guest user, inspect the following using the installed package root for
approved byte comparisons. No successful receipt has been generated yet.

```powershell
$receiptDir = Join-Path $env:LOCALAPPDATA ('Packages\' + $pkg.PackageFamilyName + '\LocalState\Phase6B1Receipts')
$files = @(Get-ChildItem -LiteralPath $receiptDir -Filter 'D00-*.json' -File -ErrorAction Stop)
if ($files.Count -ne 1) { throw 'Unexpected D00 receipt count; not PASS' }
if (Get-ChildItem -LiteralPath $receiptDir -Filter 'S21*' -File) { throw 'Unexpected S21 receipt; stop' }
$receipt = Get-Content -LiteralPath $files[0].FullName -Raw | ConvertFrom-Json
if ($receipt.schema -ne 'legacyforge-phase6b1-runtime-receipt-v1' -or $receipt.case_id -ne 'D00' -or $receipt.terminal -ne $true -or $receipt.status -ne 'PASS' -or $receipt.reason -ne 'D00_ACTIVATED_HASHES_RECORDED') { throw 'D00 did not pass' }
if ($receipt.source_baseline -ne 'd1453434ceefe73bef5aff497194e09f39dde7e1' -or $receipt.expected_package_identity -ne $true -or $receipt.details.expected_package_identity -ne $true -or $receipt.details.required_role_hashes_complete -ne $true -or $receipt.details.jvm_loaded -ne $false) { throw 'Evidence binding mismatch' }
$roles = @{
 diagnostic_exe_sha256='RuntimeDiagnostics.exe'; package_manifest_sha256='AppxManifest.xml'
 input_manifest_sha256='diagnostic-inputs.json'; runtime_inventory_sha256='runtime-inventory.json'
 profile_sha256='profiles\native-control.json'
}
foreach ($role in $roles.Keys) {
 $actual = (Get-FileHash -LiteralPath (Join-Path $pkg.InstallLocation $roles[$role]) -Algorithm SHA256).Hash.ToLowerInvariant()
 if ($receipt.details.role_hashes.$role -ne $actual -or $receipt.identities.$role -ne $actual) { throw ('Role hash mismatch: ' + $role) }
}
$approvedRoleHashes = @{
 diagnostic_exe_sha256='418a77107f02f28dc8df882e4a31ea744d93f9c3d5470aa267ffc03a8eca4231'
 package_manifest_sha256='aeb26c76e9b53342fbff2ddded481df804a1a553ee2588f1c516fb9639c93400'
 input_manifest_sha256='4b98e676878900e44ffd92f9b7cec53145807bcf08dc31633c31bbf59be5c5b5'
 runtime_inventory_sha256='a847983740065493a4e5e106aada42b355f7d1b5955cedc39dd5bf36649915c1'
 profile_sha256='9b69198a132c651a2fdea1ddcaecefe20f1d30dac5ed764be05c8f1b4057e3ba'
}
foreach ($role in $approvedRoleHashes.Keys) {
 if ($receipt.details.role_hashes.$role -ne $approvedRoleHashes[$role]) { throw ('Approved payload mismatch: ' + $role) }
}
$receipt | Select-Object schema,case_id,status,reason,terminal,elapsed_monotonic_ms
Get-FileHash -LiteralPath $files[0].FullName -Algorithm SHA256
```

Require no RECEIPT_ERROR on UI; check resources/availability/numeric errors in
details. Missing metrics are not zeros and do not prove resource capability. The
jvm_loaded false flag is a source assertion; static disablement provides the
separate safety evidence. Any tmp-only/stale/partial receipt, role mismatch or
unexpected S21 evidence fails acceptance. Preserve error/checkpoint files unchanged.

## E. Preserve evidence and roll back

Keep original JSON/tmp, screenshot, OS/VM/driver metadata, unsigned/signed hashes,
signer/framework public metadata and sanitized numeric errors in the disposable
guest. Do not export raw DxDiag or host/account identifiers. Hash evidence files.
No shared host folder or clipboard is needed during execution. If no approved
offline evidence export route exists, preserve the stopped VM and mark export
BLOCKED rather than reconnect networking. Owner can approve a dedicated blank
evidence virtual disk and read-only offline retrieval after guest shutdown later.

After evidence preservation, shut down the exact disposable guest. Restore only
the previously recorded checkpoint (owner action, no production package uninstall):

```powershell
# Host, guest already shut down and evidence preserved:
$snap = @(Get-VMSnapshot -VMName $vmName -Name 'D00-BEFORE-INSTALL-20261017')
if ($snap.Count -ne 1) { throw 'BLOCKED: exact baseline snapshot not identified' }
Restore-VMSnapshot -VMSnapshot $snap[0] -Confirm
```

Restoration removes the run's guest-side trust/install/data changes by reverting
the VM. It may restore old NIC configuration: keep the guest stopped and verify
disconnection again before any later test. Do not delete VM disks, recurse through
host directories, uninstall production LegacyForge, or alter host trust as cleanup.
