"""Bounded, nonexecuting Inno header decoder. Independent analyst implementation.
Format references: innoextract src/stream/block.cpp and lzma.cpp (not copied).
This is a partial format inspector, not a general Inno extractor.
"""
from pathlib import Path
import struct,zlib,lzma,re,json,hashlib
ROOT=Path(__file__).parent
P=ROOT.parent/'LegacyLauncher_Installer_legacy.exe'
b=P.read_bytes();marker=b'Inno Setup Setup Data (6.1.0) (u)\0'
offsets=[m.start() for m in re.finditer(re.escape(marker),b)]
out={'installer_sha256':hashlib.sha256(b).hexdigest(),'version_markers':offsets,'blocks':[]}
for off in offsets:
 pos=off+64
 if pos+9>len(b):continue
 crc,size,compressed=struct.unpack_from('<IIB',b,pos)
 if size>len(b)-pos-9 or zlib.crc32(b[pos+4:pos+9])!=crc:continue
 raw=b[pos+9:pos+9+size];parts=[];chunks=0
 for i in range(0,len(raw),4100):
  chunk=raw[i:i+4100]
  if len(chunk)<5:raise ValueError('truncated checksum block')
  if zlib.crc32(chunk[4:])!=struct.unpack_from('<I',chunk)[0]:raise ValueError('chunk checksum mismatch')
  parts.append(chunk[4:]);chunks+=1
 packed=b''.join(parts)
 if compressed:
  prop=packed[0];dictsize=struct.unpack_from('<I',packed,1)[0]
  if dictsize>64*1024*1024:raise ValueError('dictionary budget')
  dec=lzma.LZMADecompressor(format=lzma.FORMAT_RAW,filters=[{'id':lzma.FILTER_LZMA1,'dict_size':dictsize,'lc':prop%9,'lp':(prop//9)%5,'pb':prop//45}])
  data=dec.decompress(packed[5:],max_length=32*1024*1024)
  if not dec.eof:raise ValueError('header decode incomplete/budget')
 else:data=packed
 # Binary decompressed metadata remains local only; no executable is materialized.
 (ROOT/'installer-header-local.bin').write_bytes(data)
 nextpos=pos+9+size
 ncrc,nsize,ncompressed=struct.unpack_from('<IIB',b,nextpos)
 assert zlib.crc32(b[nextpos+4:nextpos+9])==ncrc
 second=b[nextpos+9:nextpos+9+nsize];secondparts=[]
 for i in range(0,len(second),4100):
  piece=second[i:i+4100];assert zlib.crc32(piece[4:])==struct.unpack_from('<I',piece)[0];secondparts.append(piece[4:])
 packed2=b''.join(secondparts)
 if ncompressed:
  prop2=packed2[0];ds2=struct.unpack_from('<I',packed2,1)[0];assert ds2<=64*1024*1024
  decoder2=lzma.LZMADecompressor(format=lzma.FORMAT_RAW,filters=[{'id':lzma.FILTER_LZMA1,'dict_size':ds2,'lc':prop2%9,'lp':prop2//9%5,'pb':prop2//45}])
  locations=decoder2.decompress(packed2[5:],max_length=32*1024*1024);assert decoder2.eof
 else:locations=packed2
 (ROOT/'installer-locations-local.bin').write_bytes(locations)
 out['location_block']={'offset':nextpos,'stored_bytes':nsize,'decoded_bytes':len(locations),'decoded_sha256':hashlib.sha256(locations).hexdigest(),'header_crc_valid':True,'chunks_crc_valid':True}
 ascii_strings=[{'offset':m.start(),'value':m.group().decode()} for m in re.finditer(rb'[ -~]{6,}',data)]
 wide_strings=[{'offset':m.start(),'value':m.group().decode('utf-16le')} for m in re.finditer(rb'(?:[ -~]\0){6,}',data)]
 relevant=[s for s in wide_strings+ascii_strings if re.search(r'\.jar|\.exe|\.dll|legacy|https?://|jre|version|checksum|sha|license|minecraft|tlauncher',s['value'],re.I)]
 out['blocks'].append({'offset':pos,'stored_bytes':size,'decoded_bytes':len(data),'header_crc_valid':True,'chunk_crc_valid':True,'chunks':chunks,'decoded_sha256':hashlib.sha256(data).hexdigest(),'strings':relevant})
(ROOT/'installer-header-evidence.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'version_markers':offsets,'blocks':[{k:v for k,v in x.items() if k!='strings'} for x in out['blocks']],'strings':out['blocks'][0]['strings'][:60] if out['blocks'] else []},indent=2))
