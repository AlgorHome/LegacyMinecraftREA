[CmdletBinding()]
param(
    [ValidateSet('D00Only','Java21Smoke')][string]$Configuration = 'D00Only',
    [string]$JavaHome21,
    [string]$MsvcRoot = 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.44.35207',
    [string]$SdkRoot = 'C:\Program Files (x86)\Windows Kits\10',
    [string]$SdkVersion = '10.0.26100.0',
    [string]$Python = 'python',
    [string]$RuntimeRoot,
    [string]$RuntimeInventory,
    [switch]$Package
)
# Original diagnostic-only build: never runs resulting EXE, JVM or class files.
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$root=$PSScriptRoot
$d00Only=$Configuration -eq 'D00Only'
# Reject before creating outputs or invoking any tools.
if($d00Only -and ($RuntimeRoot -or $RuntimeInventory -or $JavaHome21)){throw 'D00Only rejects all Java/runtime input parameters'}
if(-not $d00Only -and -not $JavaHome21){throw 'Java21Smoke requires explicit JavaHome21'}
$sourceCommit=(& git -C $root rev-parse HEAD).Trim()
if($LASTEXITCODE -ne 0){throw 'Cannot record source commit'}
$runName=(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,8)
$out=Join-Path $root ('out\'+$runName)
$stage=Join-Path $out 'package'
$obj=Join-Path $out 'objects'
$logs=Join-Path $out 'logs'
foreach($dir in @($stage,$obj,$logs,(Join-Path $stage 'profiles'))){New-Item -ItemType Directory -Path $dir -Force | Out-Null}
$receipt=[ordered]@{schema='legacyforge-diagnostic-build-v1';mode='COMPILE_AND_STATIC_PACKAGE_ONLY';targetExecuted=$false;baseline='d1453434ceefe73bef5aff497194e09f39dde7e1';buildId=$runName;configuration=$Configuration;sourceCommit=$sourceCommit;d00Only=$d00Only;status='STARTED';runtimeStatus='BLOCKED_RUNTIME_NOT_SUPPLIED';commands=@();tools=@();sourceFiles=@();artifacts=@();licenseFiles=@()}
function Hash([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Save-Receipt { $receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $out 'build-receipt.json') -Encoding utf8 }
function Tool([string]$name,[string]$path){
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "Required tool missing: $name"}
 $file=Get-Item -LiteralPath $path
 $safe=$file.FullName.Replace([Environment]::GetFolderPath('UserProfile'),'<USERPROFILE>')
 $receipt.tools+=@{role=$name;path=$safe;fileVersion=$file.VersionInfo.FileVersion;sha256=(Hash $path)}
}
function Invoke-Compile([string]$role,[string]$exe,[string[]]$argv){
 $log=Join-Path $logs ($role+'.log')
 & $exe @argv *> $log
 $exitCode=$LASTEXITCODE
 $receipt.commands+=@{role=$role;exitCode=$exitCode;log=('logs/'+$role+'.log');logSha256=(Hash $log)}
 Save-Receipt
 if($exitCode -ne 0){throw "Compilation/static tool failed: $role exit=$exitCode; inspect local build log"}
}
$oldInclude=$env:INCLUDE;$oldLib=$env:LIB;$oldPath=$env:PATH
try {
 if(-not $d00Only){
 $javac=Join-Path $JavaHome21 'bin\javac.exe'
 $jni=Join-Path $JavaHome21 'include'
 $release=Join-Path $JavaHome21 'release'
 $releaseText=Get-Content -LiteralPath $release -Raw
 if($releaseText -notmatch '(?m)^JAVA_VERSION="21\.' -or $releaseText -notmatch '(?m)^OS_ARCH="(amd64|x86_64)"'){throw 'Explicit JavaHome21 must identify Java21 x64 in release metadata'}
 }
 $cl=Join-Path $MsvcRoot 'bin\Hostx64\x64\cl.exe'
 $link=Join-Path $MsvcRoot 'bin\Hostx64\x64\link.exe'
 $dump=Join-Path $MsvcRoot 'bin\Hostx64\x64\dumpbin.exe'
 $makeappx=Join-Path $SdkRoot ('bin\'+$SdkVersion+'\x64\makeappx.exe')
 $pythonExe=(Get-Command $Python -CommandType Application | Select-Object -First 1).Source
 foreach($entry in @(@('cl',$cl),@('link',$link),@('dumpbin',$dump),@('python',$pythonExe))){Tool $entry[0] $entry[1]}
 if($Package){Tool 'makeappx' $makeappx}
 if(-not $d00Only){Tool 'javac' $javac
 foreach($header in @((Join-Path $jni 'jni.h'),(Join-Path $jni 'win32\jni_md.h'))){if(-not(Test-Path -LiteralPath $header)){throw 'JNI header prerequisite missing'}}
 }
 $incBase=Join-Path $SdkRoot ('Include\'+$SdkVersion)
 $libBase=Join-Path $SdkRoot ('Lib\'+$SdkVersion)
 $receipt.tools+=@{role='cppwinrt-base-header';path=('WINDOWS_SDK/Include/'+$SdkVersion+'/cppwinrt/winrt/base.h');sha256=(Hash (Join-Path $incBase 'cppwinrt\winrt\base.h'))}
 $storeLib=Join-Path $MsvcRoot 'lib\x64\store'
 if(-not(Test-Path -LiteralPath $storeLib)){throw 'MSVC UWP store libraries missing'}
 $env:INCLUDE=@((Join-Path $MsvcRoot 'include'),(Join-Path $incBase 'ucrt'),(Join-Path $incBase 'shared'),(Join-Path $incBase 'um'),(Join-Path $incBase 'winrt'),(Join-Path $incBase 'cppwinrt')) -join ';'
 $env:LIB=@($storeLib,(Join-Path $MsvcRoot 'lib\x64'),(Join-Path $libBase 'ucrt\x64'),(Join-Path $libBase 'um\x64')) -join ';'
 $env:PATH=(Join-Path $MsvcRoot 'bin\Hostx64\x64')+';'+$oldPath
 $sourcePaths=@('build.ps1','package/Package.appxmanifest','runtime-inventory.template.json','tools/verify_artifacts.py','tools/audit_d00.py','include/diagnostics.h','include/build_config.h','src/app.cpp','src/report.cpp','src/native_control.cpp','src/jni_smoke.cpp','java/diagnostic/JniSmoke.java')
 foreach($rel in $sourcePaths){$p=Join-Path $root $rel;if(-not(Test-Path -LiteralPath $p)){throw "Diagnostic source not ready: $rel"};$receipt.sourceFiles+=@{path=$rel;sha256=(Hash $p)}}
 $sourceLicense=Join-Path (Split-Path (Split-Path $root -Parent) -Parent) 'LICENSE'
 if(-not(Test-Path -LiteralPath $sourceLicense -PathType Leaf)){throw 'Repository Apache-2.0 license missing'}
 $receipt.licenseFiles+=@{path='LICENSE.txt';sha256=(Hash $sourceLicense)}
 Copy-Item -LiteralPath $sourceLicense -Destination (Join-Path $stage 'LICENSE.txt')
 if(-not $d00Only){
 $receipt.tools+=@{role='jni-header';path='EXPLICIT_JAVA21/include/jni.h';sha256=(Hash (Join-Path $jni 'jni.h'))}
 $receipt.tools+=@{role='jdk-release';path='EXPLICIT_JAVA21/release';sha256=(Hash $release)}
 Invoke-Compile 'java-fixture' $javac @('--release','21','-encoding','UTF-8','-d',(Join-Path $stage 'Fixtures\classes'),(Join-Path $root 'java\diagnostic\JniSmoke.java'))
 }
 $objects=@()
 foreach($name in @('app','report','native_control','jni_smoke')){
  $outputObj=Join-Path $obj ($name+'.obj');$objects+=$outputObj
  $defines=@('/DLFD_D00_ONLY='+[int]$d00Only)
  $jniIncludes=@();if(-not $d00Only){$jniIncludes=@(('/I'+$jni),('/I'+(Join-Path $jni 'win32')))}
  $compileArgs=@('/nologo','/c','/std:c++17','/EHsc','/utf-8','/MD','/W4','/O2','/DUNICODE','/D_UNICODE','/DWINAPI_FAMILY=WINAPI_FAMILY_APP','/D_WIN32_WINNT=0x0A00',('/I'+(Join-Path $root 'include')),('/Fo'+$outputObj),(Join-Path $root ('src\'+$name+'.cpp')))+$defines+$jniIncludes
  Invoke-Compile ('cpp-'+$name) $cl $compileArgs
  if($d00Only -and $name -in @('app','jni_smoke')){
   Invoke-Compile ('preprocess-'+$name) $cl ($compileArgs+@('/P',('/Fi'+(Join-Path $obj ($name+'.i')))))
  }
 }
 $exe=Join-Path $stage 'RuntimeDiagnostics.exe'
 Invoke-Compile 'link' $link (@('/NOLOGO','/SUBSYSTEM:WINDOWS','/MACHINE:X64','/APPCONTAINER','/DYNAMICBASE','/NXCOMPAT',('/OUT:'+$exe))+ $objects + @('windowsapp.lib','runtimeobject.lib','d3d11.lib','dxgi.lib','d2d1.lib','dwrite.lib','ole32.lib','bcrypt.lib'))
 Invoke-Compile 'static-imports' $dump @('/nologo','/imports',$exe)
 $manifest=Get-Content -LiteralPath (Join-Path $root 'package\Package.appxmanifest') -Raw
 if(-not $d00Only){$manifest=$manifest.Replace('Runtime Diagnostics  -  D00 ONLY','Runtime Diagnostics  -  Java21Smoke').Replace('Phase 6B.1a native D00 control only; Java/JNI disabled','Independent native and synthetic Java21 diagnostics')}
 $manifest | Set-Content -LiteralPath (Join-Path $stage 'AppxManifest.xml') -Encoding utf8
 Invoke-Compile 'generate-original-assets' $pythonExe @((Join-Path $root 'tools\verify_artifacts.py'),'--assets',(Join-Path $stage 'Assets'))
 $inventory=Get-Content -LiteralPath (Join-Path $root 'runtime-inventory.template.json') -Raw | ConvertFrom-Json
 if([bool]$RuntimeRoot -ne [bool]$RuntimeInventory){throw 'RuntimeRoot and RuntimeInventory must be supplied together; neither is selected automatically'}
 if($RuntimeRoot){
  Invoke-Compile 'verify-approved-runtime-inputs' $pythonExe @((Join-Path $root 'tools\verify_artifacts.py'),'--runtime-root',$RuntimeRoot,'--runtime-inventory',$RuntimeInventory)
  $inventory=Get-Content -LiteralPath $RuntimeInventory -Raw | ConvertFrom-Json
  foreach($entry in $inventory.files){$dest=Join-Path (Join-Path $stage 'Runtime') $entry.path;New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null;Copy-Item -LiteralPath (Join-Path $RuntimeRoot $entry.path) -Destination $dest}
  $receipt.runtimeStatus='APPROVED_INPUTS_HASH_VERIFIED_NOT_EXECUTED'
  $receipt.licenseFiles+=@($inventory.files | ForEach-Object {@{path=('Runtime/'+$_.licensePath);sha256=$_.licenseSha256}})
 }
 if(-not $d00Only){
 $fixture=Join-Path $stage 'Fixtures\classes\diagnostic\JniSmoke.class'
 $inventory.fixtureFiles=@(@{path='Fixtures/classes/diagnostic/JniSmoke.class';sha256=(Hash $fixture)})
 }else{$inventory.fixtureFiles=@();$inventory.loadOrder=@();$receipt.runtimeStatus='DISABLED_COMPILE_TIME_D00_ONLY'}
 $inventory | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $stage 'runtime-inventory.json') -Encoding utf8
 $profiles=,@('native-control','NATIVE-CONTROL',0);if(-not $d00Only){$profiles+=,@('java21-smoke','S21',21)}
 foreach($profile in $profiles){@{schema='legacyforge-diagnostic-profile-v1';id=$profile[1];javaMajor=$profile[2];execution='NOT_EXECUTED';network=$false} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $stage ('profiles\'+$profile[0]+'.json')) -Encoding utf8}
 $inputs=[ordered]@{schema='legacyforge-diagnostic-inputs-v1';baseline=$receipt.baseline;buildId=$runName;configuration=$Configuration;sourceCommit=$sourceCommit;sourceFiles=$receipt.sourceFiles;runtimeInventorySha256=(Hash (Join-Path $stage 'runtime-inventory.json'));packageFiles=@()}
 foreach($p in @(Get-ChildItem -LiteralPath $stage -Recurse -File)){$inputs.packageFiles+=@{path=$p.FullName.Substring($stage.Length+1).Replace('\','/');sha256=(Hash $p.FullName)}}
 $inputs | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $stage 'diagnostic-inputs.json') -Encoding utf8
 Invoke-Compile 'static-package-check' $pythonExe @((Join-Path $root 'tools\verify_artifacts.py'),'--package',$stage,'--output',(Join-Path $out 'static-verification.json'))
 if($Package){Invoke-Compile 'makeappx-unsigned' $makeappx @('pack','/d',$stage,'/p',(Join-Path $out 'RuntimeDiagnostics.unsigned.appx'),'/o')}
 foreach($p in @(Get-ChildItem -LiteralPath $out -Recurse -File | Where-Object {$_.Name -ne 'build-receipt.json'})){$receipt.artifacts+=@{path=$p.FullName.Substring($out.Length+1).Replace('\','/');bytes=$p.Length;sha256=(Hash $p.FullName)}}
 if($d00Only){
  Invoke-Compile 'static-d00-audit' $pythonExe @((Join-Path $root 'tools\audit_d00.py'),'--build',$out,'--output',(Join-Path $out 'd00-safety-audit.json'))
 }
 $receipt.status='BUILD_STATIC_CHECK_PASS_NOT_EXECUTED';Save-Receipt
 Write-Output ('BUILD_STATIC_CHECK_PASS_NOT_EXECUTED '+$out)
} catch {
 $receipt.status='BUILD_FAILED_NOT_EXECUTED';Save-Receipt
 throw
} finally {$env:INCLUDE=$oldInclude;$env:LIB=$oldLib;$env:PATH=$oldPath}
