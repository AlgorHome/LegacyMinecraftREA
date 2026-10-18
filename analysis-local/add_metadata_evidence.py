from pathlib import Path
import json,hashlib,re,datetime
BASE=Path(__file__).parent;DOC=BASE.parent/'docs/research/legacy-launcher'
d=json.loads((BASE/'official-metadata-check.json').read_text())
d['recorded_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(DOC/'evidence/official-metadata-check.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
check=d['checks'][0]['selected_version'];libs=check['libraries'];valid=sum(x['present_in_official'] and x['artifact_sha1_equal'] and x['artifact_url_equal'] for x in libs['checks'])
assert check['sha1_valid'] and check['local_asset_index_sha1_valid'] and all(check['official_asset_index_fields_equal'].values())
assert valid==len(libs['checks'])==107
def append(n,s):
 p=DOC/n;p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n'+s.strip()+'\n',encoding='utf-8')
append('INSTALLATION-PIPELINE.md','''## Independent official metadata comparison [E17]

An unauthenticated HTTPS request to the official Mojang v2 catalog selected version1.21.11 and fetched only its public JSON metadata. Version JSON SHA1 `718cd84b4912691fe5de829aab6876a4b7f6c5c4` matches the catalog declaration; SHA256 is `471a6eeadf1c74f84ed5d4290fb7234b746373478a4d6ac651962b93f0cb36d9`. Local ID, main class, Java requirement and download descriptors equal the official fields. All107 locally described library artifact SHA1/URL pairs match corresponding official entries. The local asset index's SHA1 matches the independently obtained official value `e81d9e2536723a11eb68e11c5642708926b8be5f`.

The local assetIndex object has an extra `known` field, so whole-object equality is false while every official assetIndex field agrees. This is normalization, not a mismatch in index identity. Keep the local serialized schema separate from the official schema. No client/library/runtime binary or asset object was downloaded by this check. Current metadata verification does not authenticate the historical installer or constitute a game launch.
''')
append('DOWNLOADS-TO-LEGACYFORGE.md','''## Verified metadata example for a Fabric target [E17]

The public [Fabric profile endpoint](https://meta.fabricmc.net/v2/versions/loader/1.21.11/0.19.5/profile/json) returned ID `fabric-loader-0.19.5-1.21.11`, parent `1.21.11`, main class `net.fabricmc.loader.impl.launch.knot.KnotClient`, eight library entries and argument metadata. Response SHA256: `5f5f7769b2305da29cb73c19c3e5698c9dc6813326a13c373d7dda5be64827b3`. This is a direct public JSON observation, independent of proprietary extra-version mirrors.

For that exact LegacyForge catalog row, the independently implementable chain is: official vanilla1.21.11 metadata→Fabric0.19.5 profile inheritance→merged libraries/main class/conditional arguments→existing per-target manifest/download repair→existing packaged Java21/GLFW/Mesa adaptations→existing ownership/profile checks→embedded JVM. The first metadata steps are now independently corroborated; downstream artifact preparation and Xbox execution remain BLOCKED. No upstream installer or game executable was run.
''')
append('LOADER-RESOLUTION.md','''## Independently corroborated upstream profile [E17]

The official Fabric1.21.11/0.19.5 JSON response independently confirms inheritance, KnotClient entrypoint, eight libraries and argument metadata. This explains how a lawful upstream profile can replace dependence on proprietary extra-version catalogs in an independent implementation. It does not establish equivalence with the launcher's private server-generated Forge/Fabric profiles, nor prove the catalog target runs on Xbox. Exact response hashes and normalized comparisons are in evidence/official-metadata-check.json.
''')
append('EVIDENCE-INDEX.md','''## E17 — Public metadata verification

`python analysis-local/official_metadata_check.py` requests public JSON only: Mojang version_manifest_v2, its selected1.21.11 JSON and Fabric1.21.11/0.19.5 profile JSON. No credentials, artifact binaries or asset objects are requested. Version metadata's declared SHA1 validates; all107 library artifact hash/URL pairs agree with local normalized metadata; the local asset index agrees with the independently retrieved official hash. Fabric confirms the eight-library inherited KnotClient profile. Data/hash/result summaries are in evidence/official-metadata-check.json. The current catalog is time-varying; selected content-addressed version/profile response hashes bind this observation. These are external metadata checks, not target execution tests or publisher-authenticity proof for the archived installer.
''')
append('PHASE-STATUS.md','''## Additional Phase D corroboration

E17 independently fetched public official metadata without authentication or binary download: the selected Mojang version JSON validates against its catalog hash; all107 local library artifact hash/URL pairs and the asset index identity agree; the official Fabric profile demonstrates the inherited eight-library KnotClient target. This closes the initial local-metadata-only comparison limitation for those exact fields. Every runtime/device test remains BLOCKED.
''')
# Correct small prose/link-label defects without altering code identifiers or URLs.
fixes={'MC. Xbox':'MC.Xbox','Connected6.4.0':'Connected REA 6.4.0','Ghidra12.1.4':'Ghidra 12.1.4','Required12':'Required 12','starts116840856':'starts at 116840856','its770':'its 770','occupy74':'occupy 74','begins1202688':'begins at 1202688','with a2,097,152 -byte':'with a 2,097,152-byte','contains5,275':'contains 5,275','glfwExtensionSupported3979':'glfwExtensionSupported (line 3979)','glfwGetWin32Window4123':'glfwGetWin32Window (line 4123)','version1.21.11':'version 1.21.11','All107':'All 107','all107':'all 107','Fabric1.21.11':'Fabric 1.21.11','selected1.21.11':'selected 1.21.11','vanilla1.21.11':'vanilla 1.21.11','Fabric0.19.5':'Fabric 0.19.5','Java21/':'Java 21/'}
for p in DOC.glob('*.md'):
 s=p.read_text(encoding='utf-8')
 for a,b in fixes.items():s=s.replace(a,b)
 s=re.sub(r';(?=\d)', '; ',s);s=re.sub(r',(?=148|622|431)', ', ',s)
 p.write_text(s,encoding='utf-8')
tools=json.loads((DOC/'evidence/analyst-tool-hashes.json').read_text())
for n in ['official_metadata_check.py','finalize_continuation.py','continue_reports.py','add_metadata_evidence.py']:
 tools.append({'path':'analysis-local/'+n,'sha256':hashlib.sha256((BASE/n).read_bytes()).hexdigest()})
(DOC/'evidence/analyst-tool-hashes.json').write_text(json.dumps(tools,indent=2))
with (DOC/'evidence/SHA256SUMS.txt').open('w',encoding='utf-8') as f:
 for p in sorted(DOC.rglob('*')):
  if p.is_file() and p.name!='SHA256SUMS.txt':f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(DOC).as_posix()+'\n')
print(json.dumps({'official_library_pairs_validated':valid,'asset_index_hash_valid':True,'version_metadata_hash_valid':True,'fabric_profile_observed':d['checks'][1].get('observed')},indent=2))
