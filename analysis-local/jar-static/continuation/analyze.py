import zipfile, pathlib, struct, json, io, hashlib, re
ROOT=pathlib.Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft\launcher')
OUT=pathlib.Path(__file__).parent
def parse(b):
 p=8; cp=[None]; methods=[]
 def n(k):
  nonlocal p
  x=int.from_bytes(b[p:p+k],'big'); p+=k; return x
 count=n(2);i=1
 while i<count:
  t=n(1)
  if t==1:
   l=n(2);cp.append((t,b[p:p+l].decode('utf-8','replace')));p+=l
  elif t in (3,4): cp.append((t,n(4)))
  elif t in (5,6): cp.append((t,n(8)));cp.append(None);i+=1
  elif t in (7,8,16,19,20): cp.append((t,n(2)))
  elif t in (9,10,11,12,17,18): cp.append((t,n(2),n(2)))
  elif t==15:cp.append((t,n(1),n(2)))
  else:raise ValueError(t)
  i+=1
 def resolve(i):
  c=cp[i]
  if c[0] in (1,3,4,5,6):return str(c[1])
  if c[0] in (7,8,16,19,20):return resolve(c[1])
  if c[0] in (9,10,11):return resolve(c[1])+'.'+resolve(c[2])
  if c[0]==12:return resolve(c[1])+resolve(c[2])
  return repr(c)
 n(2);name=resolve(n(2));sup=n(2);interfaces=n(2);p+=interfaces*2
 fields=[]
 for kind in ['fields','methods']:
  for _ in range(n(2)):
   flags=n(2); nm=resolve(n(2)); desc=resolve(n(2)); code=None; exceptions=[];cv=None
   for a in range(n(2)):
    an=resolve(n(2));sz=n(4);end=p+sz
    if an=='Code':
     stack=n(2);loc=n(2);l=n(4);code=b[p:p+l];p+=l
     for ex in range(n(2)):
      start=n(2);stop=n(2);handler=n(2);etype=n(2);exceptions.append({'start':start,'end':stop,'handler':handler,'type':resolve(etype) if etype else 'finally'})
    elif an=='ConstantValue':cv=resolve(n(2))
    p=end
   if kind=='fields':fields.append({'name':nm,'descriptor':desc,'constant':cv})
   else:methods.append({'name':nm,'descriptor':desc,'flags':flags,'code':code,'exceptions':exceptions})
 return name,cp,resolve,fields,methods
ops={16:('bipush',1),17:('sipush',2),18:('ldc',1),19:('ldc_w',2),20:('ldc2_w',2),132:('iinc',2),169:('ret',1),178:('getstatic',2),179:('putstatic',2),180:('getfield',2),181:('putfield',2),182:('invokevirtual',2),183:('invokespecial',2),184:('invokestatic',2),185:('invokeinterface',4),186:('invokedynamic',4),187:('new',2),188:('newarray',1),189:('anewarray',2),192:('checkcast',2),193:('instanceof',2),197:('multianewarray',3),200:('goto_w',4),201:('jsr_w',4)}
for i in list(range(21,26))+list(range(54,59)):ops[i]=('local',1)
branches=['ifeq','ifne','iflt','ifge','ifgt','ifle','if_icmpeq','if_icmpne','if_icmplt','if_icmpge','if_icmpgt','if_icmple','if_acmpeq','if_acmpne','goto','jsr']
for i,op in enumerate(branches,153):ops[i]=(op,2)
ops[198]=('ifnull',2);ops[199]=('ifnonnull',2)
zero={0:'nop',1:'aconst_null',2:'iconst_m1',3:'iconst_0',4:'iconst_1',5:'iconst_2',6:'iconst_3',7:'iconst_4',8:'iconst_5',9:'lconst_0',10:'lconst_1',87:'pop',89:'dup',172:'ireturn',173:'lreturn',174:'freturn',175:'dreturn',176:'areturn',177:'return',190:'arraylength',191:'athrow',194:'monitorenter',195:'monitorexit'}
def decode(code,res):
 out=[];p=0
 while p<len(code):
  off=p;o=code[p];p+=1
  if o in (170,171):
   while p%4:p+=1
   default=int.from_bytes(code[p:p+4],'big',signed=True)+off;p+=4
   if o==170:
    lo=int.from_bytes(code[p:p+4],'big',signed=True);hi=int.from_bytes(code[p+4:p+8],'big',signed=True);p+=8
    targets=[int.from_bytes(code[q:q+4],'big',signed=True)+off for q in range(p,p+(hi-lo+1)*4,4)];p+=(hi-lo+1)*4
   else:
    n=int.from_bytes(code[p:p+4],'big');p+=4;targets={str(int.from_bytes(code[q:q+4],'big',signed=True)):int.from_bytes(code[q+4:q+8],'big',signed=True)+off for q in range(p,p+n*8,8)};p+=n*8
   out.append({'offset':off,'op':'switch','default':default,'targets':targets});continue
  if o==196:
   nextop=code[p];p+=5 if nextop==132 else 3;continue
  op,l=ops.get(o,(zero.get(o,'op_'+str(o)),0));arg=code[p:p+l];p+=l
  if o in (18,19,20,178,179,180,181,182,183,184,185,187,189,192,193,197):
   idx=int.from_bytes(arg[:1] if o==18 else arg[:2],'big');out.append({'offset':off,'op':op,'ref':res(idx)})
  elif o in range(153,169) or o in (198,199,200,201):out.append({'offset':off,'op':op,'target':off+int.from_bytes(arg,'big',signed=True)})
  elif o in (16,17):out.append({'offset':off,'op':op,'value':int.from_bytes(arg,'big',signed=True)})
  elif o in zero:out.append({'offset':off,'op':op})
 return out
artifacts=[]; classes={}
with zipfile.ZipFile(ROOT/'launcher.jar') as z:
 for path in z.namelist():
  if path.endswith('.class') and (path.startswith(('net/legacylauncher/configuration/','net/legacylauncher/downloader/','net/legacylauncher/user/','net/legacylauncher/managers/Profile','net/legacylauncher/managers/Account','net/legacylauncher/minecraft/auth/','net/legacylauncher/util/FileUtil','net/legacylauncher/repository/'))):classes['launcher.jar!'+path]=z.read(path)
with zipfile.ZipFile(ROOT/'bootstrap.jar') as z:
 for nested in z.namelist():
  if nested.startswith('BOOT-INF/lib/') and re.search(r'/(bootstrap-|common-|utils-|bridge\.jar)',nested):
   raw=z.read(nested);artifacts.append({'member':nested,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
   with zipfile.ZipFile(io.BytesIO(raw)) as nz:
    for path in nz.namelist():
     if path.endswith('.class') and (path.startswith('net/legacylauncher/bootstrap/') or any(s in path for s in ['Config','Account','Crypto','UserSet','FileUtil','Stream','RepoSettings','RepoHost','Signature','PublicKey','Token'])):classes['bootstrap.jar!'+nested+'!'+path]=nz.read(path)
result={};total=0
for key,raw in classes.items():
 name,cp,res,fields,methods=parse(raw);ml=[]
 for m in methods:
  code=m.pop('code');m['bytecode_length']=len(code) if code else 0;m['observations']=decode(code,res) if code else [];ml.append(m);total+=1
 result[key]={'class':name,'sha256':hashlib.sha256(raw).hexdigest(),'fields':fields,'methods':ml}
(OUT/'static-flow-evidence.json').write_text(json.dumps({'method_count':total,'class_count':len(result),'nested_artifacts':artifacts,'classes':result},indent=2),encoding='utf-8')
print('classes',len(result),'methods',total,'json_bytes',(OUT/'static-flow-evidence.json').stat().st_size)
