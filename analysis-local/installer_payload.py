"""Nonexecuting, bounded decoding of this installer's one solid data chunk.
Uses Python lzma and the already checksum-verified location table. No code loads.
"""
from pathlib import Path
import json,struct,lzma,hashlib,io,zipfile,re
OUT=Path(__file__).parent
raw=(OUT.parent/'LegacyLauncher_Installer_legacy.exe').read_bytes()
table=(OUT/'installer-locations-local.bin').read_bytes()
assert len(table)%74==0
records=[]
for i in range(len(table)//74):
 x=struct.unpack_from('<IIIQQQ20sQIIH',table,i*74)
 records.append({'id':i,'first_slice':x[0],'last_slice':x[1],'chunk_offset':x[2],'file_offset':x[3],'bytes':x[4],'chunk_bytes':x[5],'sha1':x[6].hex(),'flags':x[-1]})
assert all(x['first_slice']==x['last_slice']==x['chunk_offset']==0 for x in records)
start=raw.index(b'zlb\x1a');assert start==1202688
prop=raw[start+4];assert prop<=40
dictsize=((2|(prop&1))<<(prop//2+11)) if prop!=40 else 0xffffffff
assert dictsize<=64*1024*1024
dec=lzma.LZMADecompressor(format=lzma.FORMAT_RAW,filters=[{'id':lzma.FILTER_LZMA2,'dict_size':dictsize}])
data=dec.decompress(raw[start+5:start+4+records[0]['chunk_bytes']],max_length=512*1024*1024)
assert dec.eof,'incomplete or budget-exhausted stream'
assert len(data)==max(x['file_offset']+x['bytes'] for x in records)
matches=[];mismatch=[];jars=[]
def undo_instruction_filter(buf):
 # Inno >=5.3.9 format semantics described by innoextract exefilter.hpp.
 # Independent in-memory implementation: skip operands and 64KiB boundaries.
 out=bytearray(buf);skip=0
 for match in re.finditer(rb'[\xe8\xe9]',buf):
  i=match.start()
  if i<skip or i%65536>65531 or i+5>len(buf):continue
  skip=i+5;high=buf[i+4]
  if high not in (0,255):continue
  relative=(int.from_bytes(buf[i+1:i+4],'little')-(i+5))&0xffffff
  out[i+1:i+4]=relative.to_bytes(3,'little')
  out[i+4]=high^(255 if relative&0x800000 else 0)
 return bytes(out)
filtered_valid=0;content_hashes={}
for x in records:
 b=data[x['file_offset']:x['file_offset']+x['bytes']]
 valid=hashlib.sha1(b).hexdigest()==x['sha1']
 x['stored_bytes_sha1_valid']=valid
 if x['flags']&16:
  b=undo_instruction_filter(b)
  x['decoded_bytes_sha1_valid']=hashlib.sha1(b).hexdigest()==x['sha1']
  filtered_valid+=x['decoded_bytes_sha1_valid']
 else:x['decoded_bytes_sha1_valid']=valid
 x['decoded_sha256']=hashlib.sha256(b).hexdigest()
 content_hashes[x['sha1']]=x['id']
 if valid:matches.append(x['id'])
 else:mismatch.append(x['id'])
 if valid and b[:2]==b'PK':
  try:
   z=zipfile.ZipFile(io.BytesIO(b));meta={}
   for name in z.namelist():
    if re.search(r'(^|/)(launcher-meta|bootstrap-meta|meta)\.json$',name) and ('META-INF' in name or 'tlauncher' in name):
     try:meta[name]=json.loads(z.read(name))
     except Exception:pass
   if meta:
    jars.append({'record':x['id'],'file_offset':x['file_offset'],'bytes':len(b),'sha1':x['sha1'],'sha256':hashlib.sha256(b).hexdigest(),'metadata':meta,'entries':len(z.namelist())})
   # Keep only archived launcher/bootstrap JARs for later static class inspection.
   if x['id'] in (3,4):
    p=OUT/'installer-extracted-local';p.mkdir(exist_ok=True)
    (p/('bootstrap.jar' if x['id']==3 else 'launcher.jar')).write_bytes(b)
  except zipfile.BadZipFile:pass
header=(OUT/'installer-header-local.bin').read_bytes()
paths=[]
for m in re.finditer(rb'(?:[ -~]\0){6,}',header):
 s=m.group().decode('utf-16le')
 if s.startswith('{app}\\'):paths.append({'header_offset':m.start(),'destination':s})
comparison=[]
app=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft')
for p in app.rglob('*'):
 if p.is_file() and not p.is_relative_to(app/'game'):
  h=hashlib.sha1(p.read_bytes()).hexdigest()
  if h in content_hashes:comparison.append({'installed_path':p.relative_to(app).as_posix(),'installer_record':content_hashes[h],'sha1':h})
result={'installer_sha256':hashlib.sha256(raw).hexdigest(),'locations_sha256':hashlib.sha256(table).hexdigest(),'location_records':len(records),'solid_chunk_offset':start,'compression':'LZMA2','dictionary_bytes':dictsize,'decoded_bytes':len(data),'decoded_sha256':hashlib.sha256(data).hexdigest(),'records':records,'raw_hash_valid_count':len(matches),'raw_hash_mismatch_ids':mismatch,'instruction_filtered_valid_count':filtered_valid,'decoded_valid_count':sum(x['decoded_bytes_sha1_valid'] for x in records),'jar_metadata':jars,'destination_strings':paths,'installed_content_matches':comparison,'limitations':['Destination strings are declarations, not an installer execution trace','Historical update path and publisher authenticity remain unverified']}
(OUT/'installer-payload-evidence.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['records','destination_strings','installed_content_matches','raw_hash_mismatch_ids','jar_metadata']},indent=2))
print('JAR_IDENTITIES',[(x['record'],x['sha256'],{k:v.get('version') for k,v in x['metadata'].items()}) for x in jars])
print('INSTALLED_CONTENT_MATCHES',len(comparison))
print('FIRST_DESTINATIONS',paths[:12],'destination_count',len(paths))
