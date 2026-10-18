from pathlib import Path
import struct,json,hashlib,re
ROOT=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft')
OUT=Path(__file__).parent
def pe_imports(p):
 b=p.read_bytes();pe=struct.unpack_from('<I',b,60)[0];n=struct.unpack_from('<H',b,pe+6)[0];sz=struct.unpack_from('<H',b,pe+20)[0];opt=pe+24;plus=struct.unpack_from('<H',b,opt)[0]==0x20b;dd=opt+(112 if plus else 96)
 sections=[struct.unpack_from('<8sIIII',b,opt+sz+40*i) for i in range(n)]
 def offset(rva):
  for _,vs,va,rs,rp in sections:
   if va<=rva<va+max(vs,rs):return rp+rva-va
  raise ValueError('unmapped RVA')
 def cs(at):return b[at:b.index(0,at)].decode('ascii','replace')
 irva,isz=struct.unpack_from('<II',b,dd+8);imports=[]
 if not irva:return []
 pos=offset(irva)
 for _ in range(1000):
  oft,ts,fw,name,ft=struct.unpack_from('<IIIII',b,pos);pos+=20
  if not any([oft,ts,fw,name,ft]):break
  module=cs(offset(name));q=offset(oft or ft);functions=[];step=8 if plus else 4;fmt='<Q' if plus else '<I';high=1<<(step*8-1)
  for j in range(10000):
   val=struct.unpack_from(fmt,b,q+j*step)[0]
   if not val:break
   functions.append('ordinal:'+str(val&0xffff) if val&high else cs(offset(val)+2))
  imports.append({'module':module,'functions':functions})
 return imports
paths=[ROOT/'TL.exe',ROOT/'jre/bin/server/jvm.dll',ROOT/'jre/java-runtime-delta/windows-x64/java-runtime-delta/bin/server/jvm.dll']+list((ROOT/'game/versions/1.21.11/natives').glob('*.dll'))
result={'imports':[],'releases':[],'historical_log_observations':[],'config_key_names':[]}
for p in paths:
 if p.is_file():result['imports'].append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'imports':pe_imports(p),'limitations':'Static standard imports only; delay imports and dynamically resolved functions not covered.'})
for p in ROOT.rglob('release'):
 if p.is_file():
  data=dict(re.findall(r'^(JAVA_VERSION|OS_ARCH|OS_NAME|IMPLEMENTOR|IMPLEMENTOR_VERSION)="(.*)"$',p.read_text(),re.M))
  result['releases'].append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'values':data})
for p in [ROOT/'tl.properties']:
 if p.is_file():result['config_key_names'] += [line.split('=',1)[0] for line in p.read_text().splitlines() if '=' in line and not line.startswith('#')]
# Deliberately inspect only technology-bearing lines; never collect session/auth or command-line values.
p=ROOT/'game/logs/latest.log'
if p.is_file():
 for number,line in enumerate(p.read_text(errors='replace').splitlines(),1):
  if any(x.lower() in line.lower() for x in ['accessToken','username','uuid','session','Bearer','token']):continue
  if re.search(r'(LWJGL version|OpenGL vendor|OpenGL renderer|OpenGL version|Backend library|Using OpenAL|OpenAL initialized)',line,re.I):
   result['historical_log_observations'].append({'path':'game/logs/latest.log','line':number,'text':line[:500]})
(OUT/'runtime-evidence.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'releases':result['releases'],'historical_log_observations':result['historical_log_observations'],'imports_summary':[{'path':i['path'],'modules':[m['module'] for m in i['imports']],'important_functions':[f for m in i['imports'] for f in m['functions'] if re.search('CreateProcess|CreateWindow|wgl|LoadLibrary|GetProcAddress|VirtualProtect|XInput|DirectSound',f)]} for i in result['imports']]},indent=2))
