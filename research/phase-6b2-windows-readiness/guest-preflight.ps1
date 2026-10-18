[CmdletBinding()]
param(
    [switch]$ConfirmedDisposableGuest,
    [string]$OutputPath = 'C:\D00\Prereq\guest-preflight.json'
)
# Original metadata-only collector. Does not install, sign, trust, activate,
# launch DxDiag/diagnostics, change policy/network or inspect credentials.
# This switch is owner attestation, not proof that this is a disposable VM.
if (-not $ConfirmedDisposableGuest) { throw 'BLOCKED: owner must first confirm disposable guest context' }
$ErrorActionPreference = 'Stop'
$r = [ordered]@{
    schema='legacyforge-d00-guest-prerequisites-v1'
    diagnosticExecuted=$false
    packageInstalledByCollector=$false
    readiness='BLOCKED_PENDING_OWNER_AND_GRAPHICS_REVIEW'
    observations=[ordered]@{}
    blockers=@('OWNER_ATTESTATION_NO_PERSONAL_DATA_OR_CREDENTIALS',
               'HOST_CONFIRM_NO_SHARED_DRIVES_CLIPBOARD_OR_DEVICES',
               'HOST_CONFIRM_ALL_VM_NICS_DISCONNECTED',
               'REVIEW_D3D_HARDWARE_PREREQUISITES',
               'EXPLICIT_SIGN_INSTALL_ACTIVATION_APPROVAL')
}
try {
    $os=Get-CimInstance Win32_OperatingSystem
    $r.observations.os=@{caption=$os.Caption;version=$os.Version;build=$os.BuildNumber;architecture=$os.OSArchitecture;process64Bit=[Environment]::Is64BitProcess}
    if ([int]$os.BuildNumber -lt 22000 -or -not [Environment]::Is64BitOperatingSystem -or $os.ProductType -ne 1) { $r.blockers+='WINDOWS_11_X64_GUEST_REQUIRED' }
    $computer=Get-CimInstance Win32_ComputerSystem
    $r.observations.computer=@{manufacturer=$computer.Manufacturer;model=$computer.Model;domainJoined=$computer.PartOfDomain}
    if ($computer.PartOfDomain) { $r.blockers+='DOMAIN_JOINED_GUEST_NOT_APPROVED' }
} catch { $r.observations.osQueryHresult=$_.Exception.HResult; $r.blockers+='OS_QUERY_FAILED' }
try {
    $r.observations.appxService=Get-Service AppXSvc | Select-Object Name,@{n='Status';e={$_.Status.ToString()}},@{n='StartType';e={$_.StartType.ToString()}}
    if ($r.observations.appxService.StartType -eq 'Disabled') { $r.blockers+='APPX_SERVICE_DISABLED' }
    # Manual/trigger-start stopped is not automatically a failure.
} catch { $r.observations.appxServiceHresult=$_.Exception.HResult; $r.blockers+='APPX_SERVICE_QUERY_FAILED' }
try {
    $policy=Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' -ErrorAction SilentlyContinue
    $r.observations.sideloadPolicy=@{allowAllTrustedApps=$policy.AllowAllTrustedApps;allowDevelopmentWithoutDevLicense=$policy.AllowDevelopmentWithoutDevLicense;interpretation='OWNER_REVIEW_REQUIRED_MISSING_VALUES_NOT_ASSUMED_DISABLED'}
} catch { $r.observations.policyHresult=$_.Exception.HResult; $r.blockers+='SIDELOAD_POLICY_QUERY_FAILED' }
try {
    $framework=@(Get-AppxPackage -Name Microsoft.VCLibs.140.00 | Where-Object { $_.Architecture.ToString() -eq 'X64' -and $_.IsFramework -and $_.Version -ge [version]'14.0.0.0' -and $_.Publisher -eq 'CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US' })
    $r.observations.framework=@($framework | Select-Object Name,Version,@{n='Architecture';e={$_.Architecture.ToString()}},Publisher,IsFramework,Status)
    if (-not $framework.Count) { $r.blockers+='TRUSTED_X64_UWP_VCLIBS_NOT_CONFIRMED' }
    $existing=@(Get-AppxPackage -Name AlgorHome.LegacyForge.RuntimeDiagnostics)
    $r.observations.existingDiagnosticPackageCount=$existing.Count
    if ($existing.Count) { $r.blockers+='GUEST_NOT_CLEAN_DIAGNOSTIC_ALREADY_REGISTERED' }
} catch { $r.observations.frameworkHresult=$_.Exception.HResult; $r.blockers+='FRAMEWORK_QUERY_FAILED' }
try {
    $r.observations.video=@(Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion,Status)
    # Display metadata is not a D3D hardware device creation test.
} catch { $r.observations.videoHresult=$_.Exception.HResult; $r.blockers+='VIDEO_QUERY_FAILED' }
try {
    $r.observations.network=@(Get-NetAdapter | Select-Object Name,@{n='Status';e={$_.Status.ToString()}})
    if (@($r.observations.network | Where-Object Status -eq 'Up').Count) { $r.blockers+='GUEST_ADAPTER_UP_REQUIRES_HOST_DISCONNECT_CONFIRMATION' }
    $r.observations.visibleUncDriveCount=@(Get-PSDrive -PSProvider FileSystem | Where-Object {$_.DisplayRoot -like '\\*'}).Count
    if ($r.observations.visibleUncDriveCount) { $r.blockers+='VISIBLE_NETWORK_OR_REDIRECTED_DRIVE' }
} catch { $r.observations.networkHresult=$_.Exception.HResult; $r.blockers+='NETWORK_QUERY_FAILED' }
$parent=Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $parent -PathType Container)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
if (Test-Path -LiteralPath $OutputPath) { throw 'Choose a fresh metadata report path; do not overwrite evidence' }
$r | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding utf8
Write-Output ('Metadata collected only; ' + $r.readiness)
