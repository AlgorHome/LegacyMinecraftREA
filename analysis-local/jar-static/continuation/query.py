import pathlib,json,sys,re
d=json.loads((pathlib.Path(__file__).parent/'static-flow-evidence.json').read_text())
for k,c in d['classes'].items():
 if re.search(sys.argv[1],c['class']):
  print('\nCLASS',c['class'],'SHA256',c['sha256'])
  if len(sys.argv)<3:print('METHODS',[(m['name'],m['descriptor'],m['bytecode_length']) for m in c['methods']]);continue
  for m in c['methods']:
   if re.search(sys.argv[2],m['name']):
    print('METHOD',m['name'],m['descriptor'],'EXCEPTIONS',m['exceptions'])
    for o in m['observations']:
     if len(sys.argv)<4 or re.search(sys.argv[3],str(o)):print(o)
