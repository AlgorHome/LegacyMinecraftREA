from pathlib import Path
import json,re,sys
d=json.loads((Path(__file__).parent/'extended-static-local.json').read_text())
for c in d['classes'].values():
 if sys.argv[1] not in c['artifact'] or not re.search(sys.argv[2],c['class']):continue
 print('CLASS',c['artifact'],c['class'],'SHA256',c['sha256'])
 for m in c['methods']:
  if len(sys.argv)>3 and not re.search(sys.argv[3],m['name']):continue
  print('METHOD',m['name'],m['descriptor'],'bytes',m['bytecode_length'])
  if len(sys.argv)>4:
   for o in m['observations']:
    if re.search(sys.argv[4],str(o)):print(o)
