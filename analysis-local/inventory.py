"""Read-only target inspection. Writes only derived metadata under analysis-local."""
from pathlib import Path
import hashlib, json, struct, zipfile, collections, sys, datetime

OUT=Path(__file__).parent
ROOT=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher')
APP=ROOT/'legacy/Minecraft'
INSTALLER=OUT.parent/'LegacyLauncher_Installer_legacy.exe'
def digest(p, alg='sha256'):
    h=hashlib.new(alg)
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
def pe(p):
    b=p.read_bytes()
    if b[:2]!=b'MZ': return None
    off=struct.unpack_from('<I',b,60)[0]
    if b[off:off+4]!=b'PE\0\0': return {'format':'DOS MZ'}
    machine,nsec,timestamp,_,_,optsize,flags=struct.unpack_from('<HHIIIHH',b,off+4)
    opt=off+24; magic=struct.unpack_from('<H',b,opt)[0]
    return {'format':'PE32+' if magic==0x20b else 'PE32','machine':hex(machine),'architecture':{0x14c:'x86',0x8664:'x86_64',0xaa64:'arm64'}.get(machine,'unknown'),'subsystem':struct.unpack_from('<H',b,opt+68)[0],'entry_rva':hex(struct.unpack_from('<I',b,opt+16)[0]),'timestamp_raw':timestamp,'sections':nsec,'inno_markers':[x.decode() for x in [b'Inno Setup Setup Data',b'Inno Setup'] if x in b]}
def info(p):
    return {'path':str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else p.name,'bytes':p.stat().st_size,'sha256':digest(p),'pe':pe(p) if p.suffix.lower() in ('.exe','.dll') else None}
files=[p for p in ROOT.rglob('*') if p.is_file()]
groups=collections.defaultdict(lambda:{'files':0,'bytes':0})
for p in files:
    rel=p.relative_to(ROOT).parts
    group='/'.join(rel[:3]) if rel[0]=='legacy' else rel[0]
    groups[group]['files']+=1;groups[group]['bytes']+=p.stat().st_size
selected=[INSTALLER,APP/'TL.exe',APP/'unins000.exe',APP/'launcher/bootstrap.jar',APP/'launcher/launcher.jar',APP/'jre/bin/java.exe',APP/'jre/bin/javaw.exe',APP/'jre/bin/server/jvm.dll']
selected += list((APP/'game/versions/1.21.11/natives').glob('*.dll'))
selected += list((APP/'game/versions/1.21.11').glob('*.jar*'))
selected += list((APP/'jre/java-runtime-delta').rglob('java.exe'))
selected += list((APP/'jre/java-runtime-delta').rglob('jvm.dll'))
jars={}
for p in (APP/'launcher').glob('*.jar'):
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        jars[p.name]={'entries':len(names),'classes':sum(n.endswith('.class') for n in names),'manifest':z.read('META-INF/MANIFEST.MF').decode('utf-8','replace'),'license_entries':[n for n in names if any(x in n.lower() for x in ('license','copying','notice'))]}
vpath=APP/'game/versions/1.21.11/1.21.11.json'
v=json.loads(vpath.read_text(encoding='utf-8'))
metadata={k:v.get(k) for k in ['id','type','mainClass','javaVersion','assetIndex','assets','downloads','arguments','minecraftArguments','inheritsFrom','minimumLauncherVersion','logging']}
metadata['libraries']=v.get('libraries',[])
assets=[]
for p in (APP/'game/assets/indexes').glob('*.json'):
    try:
        a=json.loads(p.read_text());objs=a.get('objects',{});present=valid=0
        for x in objs.values():
            h=x.get('hash','');obj=APP/'game/assets/objects'/h[:2]/h
            if obj.is_file():
                present+=1
                valid+=digest(obj,'sha1')==h
        assets.append({'index':p.name,'sha256':digest(p),'objects':len(objs),'present':present,'sha1_valid':valid})
    except Exception as e: assets.append({'index':p.name,'error':str(e)})
libs=[]
for l in v.get('libraries',[]):
    for role,d in [('artifact',l.get('downloads',{}).get('artifact',{})),*l.get('downloads',{}).get('classifiers',{}).items()]:
        from urllib.parse import urlparse
        libpath=d.get('path') or urlparse(d.get('url','')).path.lstrip('/')
        if not libpath: continue
        p=APP/'game/libraries'/libpath
        libs.append({'name':l['name'],'role':role,'path':libpath,'rules':l.get('rules',[]),'present':p.is_file(),'sha1_valid':digest(p,'sha1')==d.get('sha1') if p.is_file() else None})
result={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tool':{'python':sys.version},'scope':str(ROOT),'summary':dict(groups),'selected_files':[info(p) for p in selected if p.is_file()],'installer_sha1':digest(INSTALLER,'sha1'),'installer_md5':digest(INSTALLER,'md5'),'jars':jars,'version_metadata':metadata,'version_metadata_sha256':digest(vpath),'asset_verification':assets,'library_verification':libs,'runtime_release_paths':[str(p.relative_to(APP)) for p in APP.rglob('release') if p.is_file()]}
client=APP/'game/versions/1.21.11/1.21.11.jar'
result['client_sha1_valid']=digest(client,'sha1')==v.get('downloads',{}).get('client',{}).get('sha1')
(OUT/'inventory.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['summary','selected_files','installer_sha1','installer_md5','jars','asset_verification','runtime_release_paths']},indent=2))
