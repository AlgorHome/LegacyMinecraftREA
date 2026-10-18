"""Local-only evidence analysis. Does not load/run native targets or access Xbox."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft')
OUT=Path(__file__).parent
PRIVATE=ROOT/'analysis-local/phase6b5-fmt01-hardware-acceptance/originals'
PRIVATE.mkdir(parents=True,exist_ok=True)
receipt_path=Path(r'C:\Users\arinze\Desktop\D06-FMT01-D10A4D4B-45B4-4E67-972F-5B7A13675204.json')
photo_path=Path(r'C:\Users\arinze\AppData\Local\Temp\codex-clipboard-bc68cd2c-bddb-42f5-a0a8-2c7b83f911be.png')
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=receipt_path.read_bytes();photo=photo_path.read_bytes()
assert sha(raw)=='453d84192d19a698513513742468dae8509c74973ecd9645fe08266cb1184893'
for source,name,data in [(receipt_path,receipt_path.name,raw),(photo_path,'Xbox-D06-FMT01-PASS.png',photo)]:
 target=PRIVATE/name
 if target.exists():assert target.read_bytes()==data
 else:shutil.copy2(source,target)
repo=ROOT/'phase6b1-diagnostics';native=repo/'diagnostics/NativeCapabilities'
commit='bbe3a42c422e4328d5f98c07a9370fa948d0cbbf'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==commit
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip()
build=native/'out/20261017-180047-9ad3700d'
unsigned=build/'NativeCapabilities.unsigned.appx'
signed=ROOT/'analysis-local/phase6b5f-signing/20261017-180640-31684a3e/NativeDiagnostics.D06-FMT01.0.2.1.0.signed.appx'
assert sha(unsigned.read_bytes())=='24dc6835408f9a5d38d1ab56ec82dfd550cf0dc183e495defa836299d77dd03d'
assert sha(signed.read_bytes())=='ae19e5ff93438bcf8a3c9e0d42ad0323908ee83d95231cba9dcd9a319fd5d8ef'
# Reuse only the independently pinned original offline validator, not target code.
validator=native/'tools/receipt_contract.py'
source=subprocess.check_output(['git','show',commit+':diagnostics/NativeCapabilities/tools/receipt_contract.py'],cwd=repo)
assert validator.read_bytes().replace(b'\r\n',b'\n')==source.replace(b'\r\n',b'\n')
sys.path.insert(0,str(native/'tools'))
from receipt_contract import read_json,validate
receipt=read_json(raw)
roles={'executable_sha256':'NativeCapabilities.exe','manifest_sha256':'AppxManifest.xml','build_inputs_sha256':'native-inputs.json','policy_sha256':'profiles/D06-FMT01.json','schema_sha256':'contracts/native-receipt.schema.json','inventory_sha256':'native-inventory.json'}
approved=read_json((ROOT/'docs/research/phase-6b5-d06-fmt01/BUILD-EVIDENCE.json').read_bytes())
comparisons=[]
with zipfile.ZipFile(unsigned) as z,zipfile.ZipFile(signed) as s:
 for role,member in roles.items():
  data=z.read(member);actual=sha(data)
  assert actual==approved['payloadRoleSha256'][role]==receipt['payload_hashes'][role]
  assert data==s.read(member)==(build/'package'/member).read_bytes()
  comparisons.append(dict(role=role,member=member,independently_hashed_sha256=actual,receipt_match=True,signed_payload_match=True))
 schema=read_json(z.read(roles['schema_sha256']))
 assert z.read(roles['schema_sha256'])==(ROOT/'docs/research/phase-6b5-d06-fmt01/RECEIPT-SCHEMA.json').read_bytes()
 inputs=read_json(z.read('native-inputs.json'));policy=read_json(z.read('profiles/D06-FMT01.json'))
 for f in inputs['packageFiles']:assert sha(z.read(f['path']))==f['sha256']
 for f in inputs['sourceFiles']:assert sha((native/f['path']).read_bytes())==f['sha256']
validate(receipt,schema)
assert receipt['source_commit']==inputs['sourceCommit']==inputs['compiledSourceCommit']==commit
assert receipt['build_id']==inputs['buildId']==approved['buildId']=='20261017-180047-9ad3700d'
assert receipt_path.name==receipt['case_id']+'-'+receipt['run_id']+'.json'
assert receipt['run_id']=='D10A4D4B-45B4-4E67-972F-5B7A13675204'
assert receipt['status']=='PASS' and receipt['stage']=='FINAL' and receipt['terminal'] is True
assert receipt['reason']=='RGBA8_REQUIRED_FORMAT_SUPPORT_CONFIRMED'
d=receipt['details'];mask=d['format_support_raw']
assert mask==int(d['format_support_hex'],16)==0x33fef3f3 and mask&0x4220==0x4220
assert d['required_support_mask']==policy['required_support_mask']==0x4220
assert d['format_value']==policy['format_value']==28 and d['format_name']==policy['format_name']
assert d['creation_hresult']==d['query_hresult']=='0x00000000' and d['query_attempted'] is True
assert d['requested_feature_level']==d['selected_feature_level']==45056
assert receipt['sequence']==4 and receipt['last_durable_checkpoint_stage']=='BEFORE_FORMAT_QUERY'
assert receipt['deadline_ms']==policy['deadline_ms']==10000 and 0<=receipt['elapsed_monotonic_ms']<10000
assert not receipt['java_jni_enabled'] and not receipt['minecraft_or_gameplay_tested'] and not receipt['all_d06_certified']
before,after=d['memory_before'],d['memory_after_release']
headroom=before['limit_bytes']-before['usage_bytes'];growth=after['usage_bytes']-before['usage_bytes']
assert headroom>=policy['minimum_headroom_bytes'] and growth<=policy['maximum_observed_growth_bytes']
frozen=read_json((ROOT/'docs/research/phase-6b5f-fmt01-signing/SIGNING-VERIFICATION.json').read_bytes())
for f in frozen['preservedFiles']:assert sha(Path(f['path']).read_bytes())==f['sha256']
assert receipt_path.read_bytes()==raw and photo_path.read_bytes()==photo
result=dict(verdict='PASS_D06_FMT01_ONLY',receipt_path=str(receipt_path),receipt_sha256=sha(raw),receipt_bytes=len(raw),photo_path=str(photo_path),photo_sha256=sha(photo),photo_bytes=len(photo),preserved_originals=str(PRIVATE),schema_validation='PASS_PINNED_V2_STRUCTURE_AND_CASE_ORACLE',source_commit=commit,build_id=receipt['build_id'],package_name=receipt['package_name'],package_version=receipt['package_version'],architecture=receipt['architecture'],run_id=receipt['run_id'],process_instance_id=receipt['process_instance_id'],status=receipt['status'],reason=receipt['reason'],stage=receipt['stage'],terminal=receipt['terminal'],sequence=receipt['sequence'],last_durable_checkpoint_stage=receipt['last_durable_checkpoint_stage'],observed_at_utc=receipt['observed_at_utc'],observed_at_chicago=datetime.datetime.fromisoformat(receipt['observed_at_utc'].replace('Z','+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=-5))).isoformat(),elapsed_ms=receipt['elapsed_monotonic_ms'],deadline_ms=receipt['deadline_ms'],headroom_before_bytes=headroom,observed_memory_growth_bytes=growth,payload_comparisons=comparisons,details=d,baseline_files_verified_unchanged=len(frozen['preservedFiles']),photo_association='Visually inspected supplied original: exact run UUID/case/version/PASS/reason/S_OK/11_0/saved-receipt message match; photo does not display query mask or query HRESULT',persistence='Retrieved original terminal receipt plus matching UI saved message; new FMT01 UUID, version/build binding distinguish stale HW01 evidence',limits=['Owner attests Xbox Series X origin and retrieval; receipt/photo are not hardware-attested signatures','Receipt UTC clock accuracy and remote file listing/timestamps not independently verified','Sequence/checkpoint consistency checked; earlier overwritten checkpoint bytes not supplied','Scoped COM-reference release is not proof of all driver allocations freed','No app texture creation/rendering/presentation/OpenGL/LWJGL/Java/JNI/Minecraft tested'],new_target_execution=False,console_access=False,source_modified=False)
(OUT/'HARDWARE-VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['verdict','receipt_sha256','photo_sha256','elapsed_ms','headroom_before_bytes','observed_memory_growth_bytes','baseline_files_verified_unchanged']},indent=2))
