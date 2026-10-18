[CmdletBinding()]
param([ValidateSet('D06-SRV03')][string]$Case='D06-SRV03',
 [string]$MsvcRoot='C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.44.35207',
 [string]$SdkRoot='C:\Program Files (x86)\Windows Kits\10',[string]$SdkVersion='10.0.26100.0',[string]$Python='python')
# Compile/static tooling only; no diagnostic execution, signing, installation or downloads.
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$root=$PSScriptRoot
$commit=(& git -C $root rev-parse HEAD).Trim()
if($LASTEXITCODE -ne 0){throw 'Missing source identity'}
$dirty=@(& git -C $root status --porcelain)
if($LASTEXITCODE -ne 0 -or $dirty.Count -ne 0){throw 'Commit/review all source before building'}
$buildId=(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,8)
$out=Join-Path $root ('out\'+$buildId)
$stage=Join-Path $out 'package';$objects=Join-Path $out 'objects';$generated=Join-Path $out 'generated';$logs=Join-Path $out 'logs'
foreach($dir in @($stage,$objects,$generated,$logs,(Join-Path $stage 'profiles'),(Join-Path $stage 'contracts'))){New-Item -ItemType Directory -Path $dir -ErrorAction Stop | Out-Null}
function Hash([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$definitions=@('LFN_NATIVE_ONLY=1','LFN_JNI_ENABLED=0','LFD_D00_ONLY=1','LFN_CASE_D06_SRV03=1')
$sources=@('src/app.cpp','src/report.cpp','src/probe.cpp')
$record=[ordered]@{schema='legacyforge-native-build-v1';sourceCommit=$commit;buildId=$buildId;caseId=$Case;definitions=$definitions;compiledSources=$sources;nativeOnly=$true;jniEnabled=$false;status='STARTED';targetExecuted=$false;signed=$false;commands=@();tools=@();sourceFiles=@();artifacts=@()}
function Save { $record | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $out 'build-receipt.json') -Encoding utf8 }
function Invoke-Static([string]$name,[string]$exe,[string[]]$argv){
 $log=Join-Path $logs ($name+'.log'); & $exe @argv *> $log; $code=$LASTEXITCODE
 $record.commands+=@{role=$name;exitCode=$code;log=('logs/'+$name+'.log');sha256=(Hash $log)};Save
 if($code -ne 0){throw "Build/static tool failed: $name exit=$code"}
}
$oldInclude=$env:INCLUDE;$oldLib=$env:LIB;$oldPath=$env:PATH
try {
 $cl=Join-Path $MsvcRoot 'bin\Hostx64\x64\cl.exe';$link=Join-Path $MsvcRoot 'bin\Hostx64\x64\link.exe';$dump=Join-Path $MsvcRoot 'bin\Hostx64\x64\dumpbin.exe';$make=Join-Path $SdkRoot ('bin\'+$SdkVersion+'\x64\makeappx.exe');$py=(Get-Command $Python -CommandType Application | Select-Object -First 1).Source
 foreach($tool in @($cl,$link,$dump,$make,$py)){if(!(Test-Path -LiteralPath $tool)){throw 'Missing existing build tool'};$record.tools+=@{path=$tool;sha256=(Hash $tool)}}
 $inc=Join-Path $SdkRoot ('Include\'+$SdkVersion);$lib=Join-Path $SdkRoot ('Lib\'+$SdkVersion);$store=Join-Path $MsvcRoot 'lib\x64\store'
 if(!(Test-Path -LiteralPath $store)){throw 'Existing UWP store CRT missing'}
 $env:INCLUDE=@((Join-Path $MsvcRoot 'include'),(Join-Path $inc 'ucrt'),(Join-Path $inc 'shared'),(Join-Path $inc 'um'),(Join-Path $inc 'winrt'),(Join-Path $inc 'cppwinrt')) -join ';'
 $env:LIB=@($store,(Join-Path $MsvcRoot 'lib\x64'),(Join-Path $lib 'ucrt\x64'),(Join-Path $lib 'um\x64')) -join ';'
 $env:PATH=(Join-Path $MsvcRoot 'bin\Hostx64\x64')+';'+$oldPath
 foreach($file in @(Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {$_.FullName -notlike '*\out\*' -and $_.FullName -notlike '*\__pycache__\*'})){$record.sourceFiles+=@{path=$file.FullName.Substring($root.Length+1).Replace('\','/');sha256=(Hash $file.FullName)}}
 $identityHeader=Join-Path $generated 'build_identity.h'
 ('#pragma once'+[Environment]::NewLine+'namespace lfn { inline constexpr wchar_t SourceCommit[] = L"'+$commit+'"; inline constexpr wchar_t BuildId[] = L"'+$buildId+'"; }') | Set-Content -LiteralPath $identityHeader -Encoding utf8
 $record.generatedIdentitySha256=Hash $identityHeader
 # Preprocessor-only rejection tests: never link or execute an unsafe build.
 $gateSource=Join-Path $generated 'gate.cpp'
 '#include "build_config.h"' | Set-Content -LiteralPath $gateSource -Encoding utf8
 foreach($definition in @('LFN_NATIVE_ONLY=0','LFN_JNI_ENABLED=1','LFD_D00_ONLY=0','LFN_CASE_D06_SRV03=0','LFN_CASE_D06_HW01=1','LFN_CASE_D06_FMT01=1','LFN_CASE_D06_RES01A=1','LFN_CASE_D06_SRV01=1','LFN_CASE_D06_SRV02=1')) {
  $name='gate-'+$definition.Replace('=','-');$log=Join-Path $logs ($name+'.log')
  & $cl /nologo /P ('/I'+(Join-Path $root 'include')) ('/D'+$definition) ('/Fi'+(Join-Path $generated ($name+'.i'))) $gateSource *> $log
  $code=$LASTEXITCODE
  $record.commands+=@{role=$name;exitCode=$code;expected='nonzero preprocessor rejection';log=('logs/'+$name+'.log');sha256=(Hash $log)};Save
  if($code -eq 0 -or !(Select-String -LiteralPath $log -SimpleMatch '#error' -Quiet)){throw 'Unsafe compile configuration was not explicitly rejected'}
 }
 $objFiles=@()
 foreach($source in $sources){$name=[IO.Path]::GetFileNameWithoutExtension($source);$obj=Join-Path $objects ($name+'.obj');$objFiles+=$obj
  $args=@('/nologo','/c','/std:c++17','/EHsc','/utf-8','/MD','/W4','/O2','/DUNICODE','/D_UNICODE','/DWINAPI_FAMILY=WINAPI_FAMILY_APP','/D_WIN32_WINNT=0x0A00',('/I'+(Join-Path $root 'include')),('/I'+$generated),('/Fo'+$obj),(Join-Path $root $source))+@($definitions | ForEach-Object {'/D'+$_})
  Invoke-Static ('cpp-'+$name) $cl $args
  Invoke-Static ('preprocess-'+$name) $cl ($args+@('/P',('/Fi'+(Join-Path $objects ($name+'.i')))))
 }
 $exe=Join-Path $stage 'NativeCapabilities.exe'
 Invoke-Static 'link' $link (@('/NOLOGO','/SUBSYSTEM:WINDOWS','/MACHINE:X64','/APPCONTAINER','/DYNAMICBASE','/NXCOMPAT',('/OUT:'+$exe))+$objFiles+@('windowsapp.lib','runtimeobject.lib','d3d11.lib','ole32.lib','bcrypt.lib'))
 Invoke-Static 'imports' $dump @('/nologo','/imports',$exe)
 Invoke-Static 'headers' $dump @('/nologo','/headers',$exe)
 Copy-Item -LiteralPath (Join-Path $root 'package\Package.appxmanifest') -Destination (Join-Path $stage 'AppxManifest.xml')
 Copy-Item -LiteralPath (Join-Path $root 'profiles\D06-SRV03.json') -Destination (Join-Path $stage 'profiles\D06-SRV03.json')
 Copy-Item -LiteralPath (Join-Path $root 'contracts\native-receipt.schema.json') -Destination (Join-Path $stage 'contracts\native-receipt.schema.json')
 Copy-Item -LiteralPath (Join-Path $root 'native-inventory.json') -Destination (Join-Path $stage 'native-inventory.json')
 Copy-Item -LiteralPath (Join-Path (Split-Path (Split-Path $root -Parent) -Parent) 'LICENSE') -Destination (Join-Path $stage 'LICENSE.txt')
 Invoke-Static 'assets' $py @((Join-Path $root 'tools\static_verify.py'),'--assets',(Join-Path $stage 'Assets'))
 $inputs=[ordered]@{schema='legacyforge-native-inputs-v1';sourceCommit=$commit;compiledSourceCommit=$commit;buildId=$buildId;generatedIdentitySha256=$record.generatedIdentitySha256;caseId=$Case;nativeOnly=$true;jniEnabled=$false;definitions=$definitions;compiledSources=$sources;sourceFiles=$record.sourceFiles;packageFiles=@()}
 foreach($file in @(Get-ChildItem -LiteralPath $stage -Recurse -File)){$inputs.packageFiles+=@{path=$file.FullName.Substring($stage.Length+1).Replace('\','/');sha256=(Hash $file.FullName)}}
 $inputs | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $stage 'native-inputs.json') -Encoding utf8
 Invoke-Static 'makeappx' $make @('pack','/d',$stage,'/p',(Join-Path $out 'NativeCapabilities.unsigned.appx'),'/o')
 Invoke-Static 'static-safety' $py @((Join-Path $root 'tools\static_verify.py'),'--build',$out,'--output',(Join-Path $out 'static-safety.json'))
 foreach($file in @(Get-ChildItem -LiteralPath $out -Recurse -File | Where-Object Name -ne 'build-receipt.json')){$record.artifacts+=@{path=$file.FullName.Substring($out.Length+1).Replace('\','/');sha256=(Hash $file.FullName);bytes=$file.Length}}
 $record.status='BUILD_STATIC_PASS_NOT_EXECUTED';Save
 Write-Output ('BUILD_STATIC_PASS_NOT_EXECUTED '+$out)
}catch{$record.status='BUILD_FAILED_NOT_EXECUTED';Save;throw}finally{$env:INCLUDE=$oldInclude;$env:LIB=$oldLib;$env:PATH=$oldPath}
