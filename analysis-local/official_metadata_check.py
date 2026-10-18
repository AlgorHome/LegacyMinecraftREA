"""Public JSON metadata only: never downloads a game/client/library/runtime binary."""
from pathlib import Path
import urllib.request,json,hashlib
OUT=Path(__file__).parent
APP=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher\legacy\Minecraft')
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LegacyForge-Phase6A-static-metadata-research'})
 with urllib.request.urlopen(req,timeout=25) as r:
  b=r.read(8*1024*1024+1)
  if len(b)>8*1024*1024:raise ValueError('metadata budget')
  return json.loads(b),{'url':url,'final_url':r.url,'bytes':len(b),'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest()}
result={'scope':'Unauthenticated public JSON metadata only; no target execution or component binaries','checks':[]}
try:
 manifest,m=get('https://piston-meta.mojang.com/mc/game/version_manifest_v2.json')
 entry=next(x for x in manifest['versions'] if x['id']=='1.21.11')
 version,v=get(entry['url']);v['expected_sha1']=entry.get('sha1');v['sha1_valid']=v['sha1']==entry.get('sha1')
 local=json.loads((APP/'game/versions/1.21.11/1.21.11.json').read_text(encoding='utf-8'))
 fields=['id','mainClass','javaVersion','assetIndex','downloads'];v['critical_fields_equal']={k:local.get(k)==version.get(k) for k in fields}
 # Compare asset index bytes locally to the hash delivered by independent official metadata.
 index=APP/'game/assets/indexes'/f"{version['assetIndex']['id']}.json"
 v['local_asset_index_sha1']=hashlib.sha1(index.read_bytes()).hexdigest();v['local_asset_index_sha1_valid']=v['local_asset_index_sha1']==version['assetIndex']['sha1']
 v['official_asset_index_fields_equal']={k:local['assetIndex'].get(k)==val for k,val in version['assetIndex'].items()}
 v['local_asset_index_extra_field_names']=sorted(set(local['assetIndex'])-set(version['assetIndex']))
 official_libs={x['name']:x for x in version.get('libraries',[])};local_libs={x['name']:x for x in local.get('libraries',[])}
 checks=[]
 for name,item in local_libs.items():
  other=official_libs.get(name,{})
  la=item.get('downloads',{}).get('artifact',{});oa=other.get('downloads',{}).get('artifact',{})
  checks.append({'name':name,'present_in_official':bool(other),'artifact_sha1_equal':la.get('sha1')==oa.get('sha1'),'artifact_url_equal':la.get('url')==oa.get('url')})
 v['libraries']={'official_count':len(official_libs),'local_count':len(local_libs),'checks':checks,'official_only_names':sorted(set(official_libs)-set(local_libs))}
 result['checks'].append({'kind':'mojang-version','manifest':m,'selected_version':v,'observed':{k:version.get(k) for k in ['id','mainClass','javaVersion','assetIndex']}})
except Exception as e:result['checks'].append({'kind':'mojang-version','error':str(e)})
try:
 data,meta=get('https://meta.fabricmc.net/v2/versions/loader/1.21.11/0.19.5/profile/json')
 result['checks'].append({'kind':'fabric-profile','metadata':meta,'observed':{'id':data.get('id'),'inheritsFrom':data.get('inheritsFrom'),'mainClass':data.get('mainClass'),'libraries':len(data.get('libraries',[])),'has_arguments':bool(data.get('arguments'))}})
except Exception as e:result['checks'].append({'kind':'fabric-profile','error':str(e)})
(OUT/'official-metadata-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
