"""Original local evidence validator. No diagnostic, DLL, console or driver execution."""
from pathlib import Path
import datetime as dt
import hashlib,json,re,shutil,uuid,zipfile

OUT=Path(__file__).parent
ROOT=OUT.parents[2]
PRIVATE=ROOT/'analysis-local/phase6b5-hw01-acceptance'
(PRIVATE/'originals').mkdir(parents=True,exist_ok=True)
receipt_path=Path(r'C:\Users\arinze\Desktop\D06-HW01-594ACA53-FC63-4709-9C8B-BE96BEDD84BD.json')
photo_path=Path(r'C:\Users\arinze\AppData\Local\Temp\codex-clipboard-b62a5941-c029-4ba0-8144-0be8cd9f8f02.png')
sha=lambda data:hashlib.sha256(data).hexdigest()
raw=receipt_path.read_bytes();photo=photo_path.read_bytes()
assert sha(raw)=='14d609bddfe39019ed4808a23190319895a4b9d4d7117eb072c6f74014a49bc7'
for src,name in [(receipt_path,receipt_path.name),(photo_path,'Xbox-D06-HW01-PASS.png')]:
    target=PRIVATE/'originals'/name
    if target.exists():assert target.read_bytes()==src.read_bytes()
    else:shutil.copy2(src,target)

def no_duplicates(pairs):
    result={}
    for k,v in pairs:
        assert k not in result,('duplicate JSON key',k)
        result[k]=v
    return result
def read_json(data):return json.loads(data.decode('utf-8-sig'),object_pairs_hook=no_duplicates)
receipt=read_json(raw)
build=ROOT/'phase6b1-diagnostics/diagnostics/NativeCapabilities/out/20261017-173106-d79a3eae'
unsigned=build/'NativeCapabilities.unsigned.appx'
signed=ROOT/'analysis-local/phase6b5c-signing/20261017-173712-e540416b/NativeDiagnostics.D06-HW01.0.2.0.0.signed.appx'
assert sha(unsigned.read_bytes())=='79722c961dd677a2c89610599aec2e9537727dead6d66e2e3e8ff522da8b2501'
assert sha(signed.read_bytes())=='d4629d1f494f73db7dcb6290bee8c5c9f28375c8630c531e58b3ee95a6f05908'
roles={'executable_sha256':'NativeCapabilities.exe','manifest_sha256':'AppxManifest.xml','build_inputs_sha256':'native-inputs.json','policy_sha256':'profiles/D06-HW01.json','schema_sha256':'contracts/native-receipt.schema.json','inventory_sha256':'native-inventory.json'}
comparisons=[]
with zipfile.ZipFile(unsigned) as z,zipfile.ZipFile(signed) as s:
    for role,member in roles.items():
        data=z.read(member);assert data==s.read(member)
        expected=sha(data);assert receipt['payload_hashes'][role]==expected
        comparisons.append({'role':role,'member':member,'independently_pinned_sha256':expected,'receipt_match':True,'signed_payload_match':True})
    schema=read_json(z.read(roles['schema_sha256']))
    inputs=read_json(z.read('native-inputs.json'))
    policy=read_json(z.read('profiles/D06-HW01.json'))

allowed={'$schema','$id','$comment','$defs','$ref','title','description','type','additionalProperties','properties','required','const','enum','format','pattern','minimum','maximum'}
def validate(value,s,path='$'):
    assert not set(s)-allowed,('unimplemented keyword',set(s)-allowed)
    if '$ref' in s:
        assert s['$ref'].startswith('#/$defs/')
        validate(value,schema['$defs'][s['$ref'].split('/')[-1]],path)
    if 'type' in s:
        kinds={'object':isinstance(value,dict),'string':type(value) is str,'integer':type(value) is int,'boolean':type(value) is bool}
        assert s['type'] in kinds and kinds[s['type']],(path,'type')
    if 'const' in s:assert type(value)==type(s['const']) and value==s['const'],(path,'const')
    if 'enum' in s:assert value in s['enum'],(path,'enum')
    if 'minimum' in s:assert value>=s['minimum'],(path,'minimum')
    if 'maximum' in s:assert value<=s['maximum'],(path,'maximum')
    if 'pattern' in s:assert re.search(s['pattern'],value),(path,'pattern')
    if s.get('format')=='uuid':
        assert re.fullmatch(r'[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}',value)
        uuid.UUID(value)
    if s.get('format')=='date-time':
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})',value)
        assert dt.datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo is not None
    if isinstance(value,dict):
        assert set(s.get('required',[]))<=set(value),(path,'required')
        for key,entry in value.items():
            if key in s.get('properties',{}):validate(entry,s['properties'][key],path+'.'+key)
            else:assert s.get('additionalProperties',True) is not False,(path,'additional property',key)
validate(receipt,schema)
assert receipt['source_commit']==inputs['sourceCommit']==inputs['compiledSourceCommit']=='a3f72874241914f6048d4ca9ec4fc0edc978625d'
assert receipt['build_id']==inputs['buildId']=='20261017-173106-d79a3eae'
assert receipt_path.name=='D06-HW01-'+receipt['run_id']+'.json'
assert receipt['run_id']=='594ACA53-FC63-4709-9C8B-BE96BEDD84BD'
assert receipt['process_instance_id']!=receipt['run_id']
assert receipt['status']=='PASS' and receipt['terminal'] is True and receipt['stage']=='FINAL'
assert receipt['reason']=='HARDWARE_DEVICE_CREATED_AND_CLASSIFIED'
assert receipt['sequence']==3 and receipt['last_durable_checkpoint_stage']=='BEFORE_CREATE_DEVICE'
assert 0<=receipt['elapsed_monotonic_ms']<receipt['deadline_ms']==policy['deadline_ms']==10000
d=receipt['details']
assert d['creation_hresult']=='0x00000000' and d['creation_hresult_signed']==0
assert d['requested_driver_type']=='HARDWARE' and d['requested_driver_type_value']==1
assert d['requested_feature_level']==d['selected_feature_level']==45056
assert d['creation_flags']==policy['creation_flags']==32
assert d['software_fallback_allowed'] is False and d['adapter_software_flag'] is False and not d['adapter_flags']&2
assert d['device_returned'] is True and d['context_returned'] is True and d['test_resources_released'] is True
assert d['get_adapter_hresult']==d['get_desc_hresult']=='0x00000000'
assert d['render_or_present_tested'] is False
before,after=d['memory_before'],d['memory_after_release']
assert before['available'] and after['available']
headroom=before['limit_bytes']-before['usage_bytes']
growth=after['usage_bytes']-before['usage_bytes']
assert headroom>=policy['minimum_headroom_bytes'] and growth<=policy['maximum_observed_growth_bytes']
frozen=read_json((ROOT/'docs/research/phase-6b5-native-capabilities/BASELINE-PRESERVATION.json').read_bytes())
for item in frozen['artifacts']+frozen['diagnosticSourceFiles']:assert sha(Path(item['path']).read_bytes())==item['sha256']
assert receipt_path.read_bytes()==raw and photo_path.read_bytes()==photo
result={'verdict':'PASS_D06_HW01_ONLY','receipt_sha256':sha(raw),'original_receipt':str(receipt_path),'preserved_receipt':str(PRIVATE/'originals'/receipt_path.name),'photo_sha256':sha(photo),'preserved_photo':str(PRIVATE/'originals/Xbox-D06-HW01-PASS.png'),'schema_validation':'PASS: all used schema keywords, local refs, formats, field restrictions; duplicate keys rejected','source_commit':receipt['source_commit'],'build_id':receipt['build_id'],'run_id':receipt['run_id'],'process_instance_id':receipt['process_instance_id'],'observed_at_utc':receipt['observed_at_utc'],'observed_at_America_Chicago':'2026-10-17 17:42:23.639 CDT','sequence':3,'elapsed_monotonic_ms':receipt['elapsed_monotonic_ms'],'headroom_before_bytes':headroom,'observed_growth_bytes':growth,'payload_comparison':comparisons,'photo_match':'Visually inspected supplied image: exact run ID, case, version, PASS/reason, HRESULT0, level0xB000 and saved-receipt message match','persistence':'PASS for retrieved final original and matching UI saved message; no power-loss guarantee','frozen_D00_unchanged':True,'limits':['Xbox hardware origin and retrieval route owner-attested; raw receipt is not signed','Clock accuracy/remote file listing not independently verified','Scoped reference release asserted by source/receipt, not proof driver frees every allocation','Photo contains exact run ID but no capture time; matching run is stronger than a timestamp guess','Rendering/presentation/OpenGL/LWJGL/Java/JNI/Minecraft untested'],'new_diagnostic_execution':False,'console_access':False}
(OUT/'HARDWARE-VERIFICATION.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
