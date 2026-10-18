from pathlib import Path
import re,json,hashlib
p=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft\TL.exe');b=p.read_bytes();out=[]
for encoding,pattern in [('ascii',rb'[ -~]{5,}'),('utf-16le',rb'(?:[ -~]\0){5,}')]:
 for m in re.finditer(pattern,b):
  s=m.group().decode(encoding)
  if re.search(r'bootstrap|tl.args|launcher|\.jar|jre|Launch4j|packageMode',s,re.I):out.append({'offset':m.start(),'encoding':encoding,'value':s})
r={'sha256':hashlib.sha256(b).hexdigest(),'strings':out}
(Path(__file__).parent/'wrapper-strings.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
