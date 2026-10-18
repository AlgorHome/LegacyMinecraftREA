from pathlib import Path
import json,subprocess,hashlib,re,zipfile
OUT=Path(__file__).parent
APP=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft')
JAVAP=Path(r'C:\Users\arinze\AppData\Local\Programs\Ghidra\jdk-21.0.12.1+1\bin\javap.exe')
OBJ=Path(r'C:\Users\arinze\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin\objdump.exe')
outer=APP/'launcher/bootstrap.jar'
with zipfile.ZipFile(outer) as z:
 member='BOOT-INF/lib/bootstrap-1.40.3-plain.jar';nested=OUT/'installer-extracted-local/installed-bootstrap-application.jar';nested.write_bytes(z.read(member))
cases=[(OUT/'installer-extracted-local/launcher.jar','ru.turikhay.tlauncher.minecraft.launcher.MinecraftLauncher',['321: invokevirtual','java/lang/ProcessBuilder.start']),
 (OUT/'installer-extracted-local/launcher.jar','net.minecraft.launcher.updater.OfficialVersionList',['version_manifest.json']),
 (OUT/'installer-extracted-local/bootstrap.jar','ru.turikhay.tlauncher.bootstrap.transport.SignedStream',['SHA1withRSA','/public.der']),
 (nested,'net.legacylauncher.bootstrap.transport.SignedStream',['SHA1withRSA','public.der']),
 (nested,'net.legacylauncher.bootstrap.meta.UpdateMeta',['.signed','validateSignature']),
 (nested,'net.legacylauncher.bootstrap.task.DownloadTask',['10000','5000','Files.copy']),
 (APP/'launcher/launcher.jar','net.legacylauncher.managers.ProfileManager',['Gson.toJson','Files.move']),
 (APP/'launcher/launcher.jar','net.legacylauncher.user.MinecraftUserJsonizer$MicrosoftTokenPayload',['getAccessToken','getRefreshToken'])]
results=[]
for jar,cls,patterns in cases:
 r=subprocess.run([str(JAVAP),'-p','-c','-classpath',str(jar),cls],capture_output=True,text=True,encoding='utf-8',errors='replace')
 results.append({'tool':'trusted-javap','artifact_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'class':cls,'exit_code':r.returncode,'pattern_checks':{p:p in r.stdout for p in patterns},'output_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
native=json.loads((OUT/'native-audit-local.json').read_text())
for rel in ['TL.exe','game/versions/1.21.11/natives/glfw.dll','game/versions/1.21.11/natives/OpenAL.dll','jre/bin/server/jvm.dll']:
 p=APP/rel;r=subprocess.run([str(OBJ),'-p',str(p)],capture_output=True,text=True,encoding='utf-8',errors='replace')
 found={x.lower() for x in re.findall(r'DLL Name:\s*(\S+)',r.stdout)}
 own=next(x for x in native['images'] if x['role']=='installed-target' and x['path']==rel)
 expected={x['module'].lower() for x in own['imports']+own['delay_imports']}
 results.append({'tool':'objdump','path':rel,'sha256':own['sha256'],'exit_code':r.returncode,'import_module_sets_equal':found==expected,'objdump_modules':sorted(found),'parser_modules':sorted(expected),'output_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
result={'meaning':'Analyzer cross-checks only, never behavioral target tests','checks':results,'javap_version':subprocess.run([str(JAVAP),'-version'],capture_output=True,text=True).stdout.strip(),'objdump_version':subprocess.run([str(OBJ),'--version'],capture_output=True,text=True).stdout.splitlines()[0]}
(OUT/'decoder-crosschecks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
