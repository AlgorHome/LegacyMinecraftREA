import zipfile, hashlib, json, struct, pathlib, re, io
ROOT=pathlib.Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft\launcher')
OUT=pathlib.Path(__file__).parent
def cls(data):
    p=8
    def u1():
        nonlocal p
        v=data[p]; p+=1; return v
    def u2():
        nonlocal p
        v=struct.unpack_from('>H',data,p)[0]; p+=2; return v
    def u4():
        nonlocal p
        v=struct.unpack_from('>I',data,p)[0]; p+=4; return v
    n=u2(); cp=[None]*n; i=1
    while i<n:
        t=u1()
        if t==1:
            l=u2(); cp[i]=(t,data[p:p+l].decode('utf-8','replace')); p+=l
        elif t in (3,4): cp[i]=(t,);p+=4
        elif t in (5,6): cp[i]=(t,);p+=8;i+=1
        elif t in (7,8,16,19,20): cp[i]=(t,u2())
        elif t in (9,10,11,12,17,18): cp[i]=(t,u2(),u2())
        elif t==15: cp[i]=(t,u1(),u2())
        else: raise ValueError(t)
        i+=1
    def utf(i): return cp[i][1]
    def cname(i): return utf(cp[i][1])
    flags=u2(); name=cname(u2()); sup=u2()
    interfaces=u2(); p+=2*interfaces
    def members():
        nonlocal p
        result=[]
        for _ in range(u2()):
            f=u2(); nm=utf(u2()); desc=utf(u2()); attrs=[]
            for _ in range(u2()):
                an=utf(u2()); l=u4(); attrs.append(an);p+=l
            result.append({'name':nm,'descriptor':desc,'flags':f})
        return result
    fields=members(); methods=members()
    refs=[]
    for c in cp:
        if c and c[0] in (9,10,11):
            nt=cp[c[2]]; refs.append(cname(c[1])+'.'+utf(nt[1])+utf(nt[2]))
    strings=[utf(c[1]) for c in cp if c and c[0]==8]
    return {'name':name,'major':struct.unpack_from('>H',data,6)[0],'super':cname(sup) if sup else None,'fields':fields,'methods':methods,'refs':refs,'strings':strings}
inventory={}; records={}
for fn in ['launcher.jar','bootstrap.jar']:
    path=ROOT/fn
    with zipfile.ZipFile(path) as z:
        names=z.namelist(); manifest=z.read('META-INF/MANIFEST.MF').decode('utf-8','replace')
        classes=[n for n in names if n.endswith('.class')]
        inventory[fn]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'entries':len(names),'classes':len(classes),'manifest':manifest,'resources':[n for n in names if not n.endswith('.class') and not n.endswith('/')][:500]}
        for n in classes:
            if n.startswith(('org/tlauncher/','net/legacylauncher/','ru/turikhay/','org/legacylauncher/')):
                records[fn+':'+n]=cls(z.read(n))
        if fn=='bootstrap.jar':
            for member in names:
                if re.search(r'BOOT-INF/lib/(bootstrap-|common-|utils-|bridge\.jar)',member):
                    with zipfile.ZipFile(io.BytesIO(z.read(member))) as nz:
                        for n in nz.namelist():
                            if n.endswith('.class') and n.startswith(('net/legacylauncher/','ru/turikhay/')):
                                records[fn+'!'+member+':'+n]=cls(nz.read(n))
        for member in ['META-INF/launcher-meta.json','META-INF/bootstrap-meta.json','net/legacylauncher/updater/default.json','ru/turikhay/tlauncher/meta.json','LICENSE.txt']:
            if member in names:
                if member.startswith('META-INF/') and member.endswith('-meta.json'):
                    meta=json.loads(z.read(member)); inventory[fn]['metadata']={k:meta[k] for k in ['version','shortBrand','brand','javaVersion','entryPoint','bridgedEntryPoint','entrypoints'] if k in meta}
                print('RESOURCE',fn,member,z.read(member).decode('utf-8','replace')[:9000])
(OUT/'inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
# Only publish our structural metadata; no target bytes or arbitrary string pool dumps.
public={k:{kk:vv for kk,vv in v.items() if kk!='strings'} for k,v in records.items()}
(OUT/'class-index.json').write_text(json.dumps(public,indent=2),encoding='utf-8')
print('LOCAL_CLASSES',len(records))
for k,v in records.items():
    if any(s in k for s in ('MinecraftLauncher.class','AssetsManager.class','JavaManager.class','ProfileManager.class','VersionLists.class','Account.class','BootstrapStarter.class','Bootstrap.class','LegacyLauncher.class','Authenticator.class','JavaRuntimeLocalDiscoverer.class','JavaRuntimeRemoteListFetcher.class')):
        print(k,'METHODS',','.join(m['name'] for m in v['methods']))
