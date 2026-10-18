import subprocess, pathlib, json, re, zipfile, importlib.util, contextlib, io
P=pathlib.Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):
    spec=importlib.util.spec_from_file_location('jars',P/'inspect_jars.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
javap=r'C:\Users\arinze\AppData\Local\Programs\Ghidra\jdk-21.0.12.1+1\bin\javap.exe'
print('JAVAP_VERSION',subprocess.run([javap,'-version'],capture_output=True,text=True).stdout.strip())
selected=['net.legacylauncher.minecraft.launcher.MinecraftLauncher','net.legacylauncher.managers.AssetsManager','net.legacylauncher.managers.VersionManager','net.legacylauncher.managers.ProfileManager','net.legacylauncher.configuration.Configuration','net.legacylauncher.jre.JavaRuntimeRemoteListFetcher','net.legacylauncher.jre.JavaRuntimeInstallerDirect','net.legacylauncher.managers.JavaManager','net.legacylauncher.downloader.Sha1Downloadable','net.legacylauncher.downloader.DownloaderTask','net.legacylauncher.user.minecraft.MinecraftUser','net.legacylauncher.user.minecraft.strategy.MinecraftAuthenticationStrategy','net.legacylauncher.minecraft.auth.Authenticator','net.legacylauncher.ui.LegacyLauncherFrame','net.legacylauncher.LegacyLauncherBridged']
selected += ['net.minecraft.launcher.updater.RemoteVersionList','net.minecraft.launcher.updater.LocalVersionList','net.minecraft.launcher.versions.CompleteVersion','net.minecraft.launcher.versions.Library','net.minecraft.launcher.versions.Rule','net.minecraft.launcher.updater.AssetIndex','net.minecraft.launcher.process.JavaProcessLauncher','net.legacylauncher.user.MinecraftUser','net.legacylauncher.user.MinecraftUserJsonizer','net.legacylauncher.user.LoginCredentials','net.legacylauncher.user.PlainUser','net.legacylauncher.user.minecraft.MinecraftOAuthAuthenticate','net.legacylauncher.user.minecraft.MinecraftOAuthRefresh','net.legacylauncher.user.minecraft.strategy.gos.GameOwnershipValidator','net.legacylauncher.user.minecraft.strategy.gos.MinecraftUserGameOwnershipResponse','net.legacylauncher.configuration.AbstractConfiguration','net.legacylauncher.configuration.Static','net.legacylauncher.jre.JavaRuntimeLocal','net.legacylauncher.jre.JavaPlatform']
selected += ['net.minecraft.launcher.updater.OfficialVersionList','net.minecraft.launcher.updater.ExtraVersionList','net.minecraft.launcher.updater.RepositoryBasedVersionList','net.minecraft.launcher.updater.AssetDownloadable','net.legacylauncher.configuration.SimpleConfiguration','net.legacylauncher.user.MinecraftUserJsonizer$Payload','net.legacylauncher.user.MinecraftUserJsonizer$MinecraftTokenPayload','net.legacylauncher.user.MinecraftUserJsonizer$MicrosoftTokenPayload']
data={}
for name in selected:
    r=subprocess.run([javap,'-p','-c','-classpath',str(mod.ROOT/'launcher.jar'),name],capture_output=True,text=True,encoding='utf-8',errors='replace')
    methods={}; current=None
    for line in r.stdout.splitlines():
        if re.match(r'^  (?:public|private|protected|static)',line):
            current=line.strip();methods[current]={'calls':[],'constants':[]}
        elif current:
            call=re.search(r'// (?:InterfaceMethod|Method) (.+)',line)
            const=re.search(r'// String (.+)',line)
            if call: methods[current]['calls'].append(call[1])
            if const and (re.search(r'https?://|^-|\.json$|^\$\{|natives|classpath|runtime|auth_|access_token|product_minecraft|game_minecraft|^bin/|^SHA|^objects|^indexes|microsoftToken|minecraftToken',const[1])): methods[current]['constants'].append(const[1])
    data[name]={'returncode':r.returncode,'error':r.stderr[:200],'methods':methods}
(P/'focused-method-evidence.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
for k,v in mod.records.items():
    strings=[s for s in v['strings'] if re.search(r'^https?://',s)]
    if strings and any(w in k.lower() for w in ['minecraft','version','assets','jre','repository','bootstrap','user/']):
        print('ENDPOINT',k,strings)
for name in selected:
    print('CLASS',name)
    d=data[name]
    if d['error']: print('ERROR',d['error'])
    for method,m in d['methods'].items():
        if any(w in method for w in ['collectInfo(','downloadResources(','constructProcess(','unpackNatives(','constructClassPath(','createJvmArgs(','launchMinecraft(','createArgumentsSubstitutor(','checkFile(','checkResource(','collectAssets(','loadProfiles(','saveProfiles(','doFetch(','checkIntegrity(','pass(','refresh(','loadVersions(']):
            calls=[c for c in m['calls'] if re.search(r'legacylauncher|ProcessBuilder|java/io|nio/file|MessageDigest|gson|Files\.',c)]
            print('METHOD',method,'CALL_COUNT',len(calls),'CONSTANTS',m['constants'])
