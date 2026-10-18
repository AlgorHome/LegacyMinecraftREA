"""Static PE directory/import/export graph. Never loads a DLL into this process."""
from pathlib import Path
import struct,json,hashlib,collections,zipfile,io
OUT=Path(__file__).parent
APP=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft')
SRC=OUT/'legacyforge-d145343'
def parse(p,root,role,payload=None,label=None):
 b=p.read_bytes() if payload is None else payload;off=struct.unpack_from('<I',b,60)[0];assert b[off:off+4]==b'PE\0\0'
 mach,n=struct.unpack_from('<HH',b,off+4);osz=struct.unpack_from('<H',b,off+20)[0];o=off+24;plus=struct.unpack_from('<H',b,o)[0]==0x20b
 base=struct.unpack_from('<Q' if plus else '<I',b,o+(24 if plus else 28))[0];dd=o+(112 if plus else 96);nd=struct.unpack_from('<I',b,dd-4)[0]
 sec=[struct.unpack_from('<8sIIII',b,o+osz+40*i) for i in range(n)]
 def at(r):
  for _,vs,va,rs,rp in sec:
   if va<=r<va+rs and rp+r-va<len(b):return rp+r-va
  raise ValueError('unmapped RVA '+hex(r))
 def cs(q):return b[q:b.index(0,q)].decode('ascii','replace')
 def directory(i):return struct.unpack_from('<II',b,dd+8*i) if i<nd else (0,0)
 def thunks(r):
  q=at(r);step=8 if plus else 4;fmt='<Q' if plus else '<I';out=[]
  for j in range(50000):
   v=struct.unpack_from(fmt,b,q+step*j)[0]
   if not v:break
   out.append('ordinal:'+str(v&65535) if v&(1<<(8*step-1)) else cs(at(v)+2))
  return out
 imports=[];delays=[];exports=[]
 r,s=directory(1)
 if r:
  q=at(r)
  for j in range(2000):
   x=struct.unpack_from('<IIIII',b,q+j*20)
   if not any(x):break
   imports.append({'module':cs(at(x[3])),'functions':thunks(x[0] or x[4])})
 r,s=directory(13)
 if r:
  q=at(r)
  for j in range(2000):
   x=struct.unpack_from('<8I',b,q+j*32)
   if not any(x):break
   adjust=lambda v:v if x[0]&1 else v-base
   delays.append({'module':cs(at(adjust(x[1]))),'functions':thunks(adjust(x[4] or x[3]))})
 r,s=directory(0)
 if r:
  x=struct.unpack_from('<IIHHIIIIIII',b,at(r));ordinalbase,nfunc,nnames,functab,nametab,ordtab=x[5:]
  for j in range(nnames):
   nr=struct.unpack_from('<I',b,at(nametab)+4*j)[0];idx=struct.unpack_from('<H',b,at(ordtab)+2*j)[0];fr=struct.unpack_from('<I',b,at(functab)+4*idx)[0]
   exports.append({'name':cs(at(nr)),'ordinal':ordinalbase+idx,'rva':hex(fr),'forwarder':cs(at(fr)) if r<=fr<r+s else None})
 return {'role':role,'path':label or p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'machine':hex(mach),'architecture':{0x8664:'x86_64',0x14c:'x86',0xaa64:'arm64'}.get(mach,'unknown'),'imports':imports,'delay_imports':delays,'named_exports':exports}
images=[];errors=[]
for role,root in [('installed-target',APP),('pinned-legacyforge',SRC)]:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in ('.exe','.dll'):
   try:images.append(parse(p,root,role))
   except Exception as e:errors.append({'role':role,'path':p.relative_to(root).as_posix(),'error':str(e)})
def jar_scan(raw,label,depth=0):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for entry in z.infolist():
   if entry.file_size>64*1024*1024:continue
   member=label+'!'+entry.filename
   if entry.filename.lower().endswith('.dll'):
    try:images.append(parse(Path('unused'),APP,'packaged-native-archive',z.read(entry),member))
    except Exception as e:errors.append({'role':'packaged-native-archive','path':member,'error':str(e)})
   elif depth<2 and entry.filename.lower().endswith('.jar'):
    jar_scan(z.read(entry),member,depth+1)
for p in APP.rglob('*.jar'):
 try:jar_scan(p.read_bytes(),p.relative_to(APP).as_posix())
 except zipfile.BadZipFile:errors.append({'role':'archive','path':p.relative_to(APP).as_posix(),'error':'BadZipFile'})
edges=[]
for im in images:
 for kind in ['imports','delay_imports']:
  for dep in im[kind]:
   candidates=[x['path'] for x in images if x['role']==im['role'] and Path(x['path']).name.lower()==dep['module'].lower() and x['architecture']==im['architecture']]
   edges.append({'role':im['role'],'from':im['path'],'kind':kind,'module':dep['module'],'same_architecture_candidates':candidates,'resolution':'unresolved-external-or-system' if not candidates else 'candidate-only-not-loader-order'})
result={'images':images,'errors':errors,'edges':edges,'limitations':['Static directory parsing only; no module loaded','Candidate graph does not emulate Windows or UWP search order','Runtime GetProcAddress/LoadLibrary targets and ordinal-only exports remain outside this PE-image scan','Native archive DLL entries are inspected recursively through two nested JAR levels, up to64MiB per entry; other platform binary formats are outside this PE audit','API import presence is not proof of runtime reachability or UWP certification']}
(OUT/'native-audit-local.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'images':len(images),'roles':dict(collections.Counter(x['role'] for x in images)),'architectures':dict(collections.Counter(x['architecture'] for x in images)),'import_edges':len(edges),'delay_import_modules':sum(len(x['delay_imports']) for x in images),'named_exports':sum(len(x['named_exports']) for x in images),'errors':errors,'source_images':[{'path':x['path'],'sha256':x['sha256'],'imports':[d['module'] for d in x['imports']],'delay':[d['module'] for d in x['delay_imports']]} for x in images if x['role']=='pinned-legacyforge']},indent=2))
