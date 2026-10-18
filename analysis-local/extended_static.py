from pathlib import Path
import json,re,hashlib,zipfile,io,struct,subprocess,collections
OUT=Path(__file__).parent
APP=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft')
CODE=(OUT/'jar-static/continuation/analyze.py').read_text()
ns={'__file__':str(OUT/'jar-static/continuation/analyze.py')};exec(CODE[:CODE.index('artifacts=[]')],ns)
classes={};artifacts=[]
for role,path in [('archived-launcher',OUT/'installer-extracted-local/launcher.jar'),('archived-bootstrap',OUT/'installer-extracted-local/bootstrap.jar'),('installed-launcher',APP/'launcher/launcher.jar')]:
 raw=path.read_bytes();artifacts.append({'role':role,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for n in z.namelist():
   if not n.endswith('.class') or not n.startswith(('ru/turikhay/tlauncher/','net/legacylauncher/','net/minecraft/launcher/')):continue
   b=z.read(n);name,cp,res,fields,methods=ns['parse'](b)
   relevant=any(x in name.lower() for x in ['version','library','rule','argument','minecraftlauncher','tlauncher','launcher/launcher','java','repository','download','forge','fabric','fileutil','configuration','profile','update','signed'])
   # Only retain method observations for substantive research classes, member metadata otherwise.
   ml=[]
   for m in methods:
    c=m.pop('code');m['bytecode_length']=len(c or b'')
    m['observations']=ns['decode'](c,res) if c and relevant else []
    ml.append(m)
   classes[role+'!'+n]={'class':name,'artifact':role,'sha256':hashlib.sha256(b).hexdigest(),'methods':ml,'fields':fields}
result={'artifacts':artifacts,'classes':classes,'class_count':len(classes),'method_count':sum(len(c['methods']) for c in classes.values())}
(OUT/'extended-static-local.json').write_text(json.dumps(result,indent=2))
# Small structural loader-routing index: no class bodies copied to deliverables.
routes=[]
for c in classes.values():
 for m in c['methods']:
  obs=[o for o in m['observations'] if re.search(r'fabric|forge|installer|installertools|profile/json',str(o),re.I)]
  if obs:routes.append({'artifact':c['artifact'],'class':c['class'],'method':m['name'],'descriptor':m['descriptor'],'class_sha256':c['sha256'],'observations':obs})
(OUT/'loader-routing-local.json').write_text(json.dumps(routes,indent=2))
print(json.dumps({'artifacts':artifacts,'class_count':result['class_count'],'method_count':result['method_count'],'loader_routes':len(routes),'route_identifiers':[{'artifact':x['artifact'],'class':x['class'],'method':x['method'],'matches':len(x['observations'])} for x in routes]},indent=2))
