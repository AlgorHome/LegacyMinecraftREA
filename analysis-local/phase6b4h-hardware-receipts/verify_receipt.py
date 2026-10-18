"""Read original receipt/build only. Validate every keyword used by pinned schema."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import shutil
import uuid
import zipfile

ROOT=Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft')
OUT=Path(__file__).parent
SOURCE=Path(r'C:\Users\arinze\Desktop\D00-0799F3FD-1056-4709-9302-202AA86C4C5D.json')
EXPECTED='1d247637c6551e2da289eecd3b343e0728b57aa4385a852590f61444fe888b7f'
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=SOURCE.read_bytes()
assert sha(raw)==EXPECTED
original=OUT/'originals'/SOURCE.name
if original.exists():
    assert original.read_bytes()==raw
else:
    shutil.copy2(SOURCE,original)
receipt=json.loads(raw.decode('utf-8-sig'))
schema_path=ROOT/'phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/contracts/receipt.schema.json'
schema_raw=schema_path.read_bytes()
schema=json.loads(schema_raw)
allowed={'$schema','$id','$comment','title','description','type','properties','patternProperties','additionalProperties','required','const','enum','format','pattern','minimum'}
def validate(value,s,path='$'):
    assert not set(s)-allowed, ('unimplemented schema keyword',set(s)-allowed)
    if 'const' in s: assert type(value)==type(s['const']) and value==s['const'],(path,'const')
    if 'enum' in s: assert value in s['enum'],(path,'enum')
    if 'type' in s:
        kind=s['type']
        ok={'object':isinstance(value,dict),'string':isinstance(value,str),'boolean':type(value) is bool,'integer':type(value) is int}
        assert kind in ok and ok[kind],(path,'type')
    if 'minimum' in s: assert value>=s['minimum'],(path,'minimum')
    if 'pattern' in s: assert re.search(s['pattern'],value),(path,'pattern')
    if s.get('format')=='uuid':
        assert re.fullmatch(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}',value),(path,'UUID shape')
        uuid.UUID(value)
    if s.get('format')=='date-time':
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})',value),(path,'date-time')
        assert dt.datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo
    if isinstance(value,dict):
        assert set(s.get('required',[]))<=set(value),(path,'missing fields')
        for key,entry in value.items():
            matched=False
            if key in s.get('properties',{}):
                validate(entry,s['properties'][key],path+'.'+key);matched=True
            for pattern,subschema in s.get('patternProperties',{}).items():
                if re.search(pattern,key): validate(entry,subschema,path+'.'+key);matched=True
            if not matched: assert s.get('additionalProperties',True) is not False,(path,key,'additional property')
validate(receipt,schema)
assert receipt['case_id']=='D00' and receipt['package_version']=='0.1.3.0'
assert receipt['status']=='PASS' and receipt['stage']=='FINAL' and receipt['terminal'] is True
assert receipt['reason']=='D00_ACTIVATED_HASHES_RECORDED' and receipt['expected_package_identity'] is True
assert SOURCE.name=='D00-'+receipt['run_id']+'.json'
assert receipt['sequence']==2 and receipt['elapsed_monotonic_ms']==31
assert receipt['last_durable_checkpoint_stage']=='D00_ACTIVATION_STARTED'
assert receipt['last_durable_checkpoint_details']['jvm_loaded'] is False
details=receipt['details']
assert details['expected_package_identity'] is True and details['required_role_hashes_complete'] is True
assert details['source_baseline']==receipt['source_baseline']
assert details['scope']=='D00_ACTIVATION_IDENTITIES_RESOURCES_ONLY'
assert all(details[name] is False for name in ['jvm_loaded','graphics_capability_tested','input_capability_tested','audio_capability_tested','native_dependency_closure_tested'])
pin=json.loads((OUT/'PINNED-ROLE-HASHES.json').read_text(encoding='utf-8-sig'))
package=ROOT/'phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/out/20261017-142300-e07d5ee8/RuntimeDiagnostics.unsigned.appx'
assert sha(package.read_bytes())==pin['unsignedSha256']
comparison=[]
with zipfile.ZipFile(package) as archive:
    for role in pin['expectedRoles']:
        expected=sha(archive.read(role['path']))
        assert expected==role['sha256']==receipt['identities'][role['role']]==details['role_hashes'][role['role']]
        assert not receipt['identities'].get(role['role']+'_error')
        assert not details['role_hashes'].get(role['role']+'_error')
        comparison.append({'role':role['role'],'expected_from_pinned_APPX':expected,'receipt_matches':True})

# Manual privacy review: this receipt contains fixed technical fields, metrics,
# random run/process UUIDs and package hashes; no account/device/network identifiers.
# Preserve a separate reviewed copy without inventing redactions.
sanitized=OUT/'sanitized'/SOURCE.name
if sanitized.exists(): assert sanitized.read_bytes()==raw
else: sanitized.write_bytes(raw)
assert SOURCE.read_bytes()==raw and original.read_bytes()==raw
result={'receipt_checks':'PASS','original_path':str(SOURCE),'preserved_copy':str(original),'receipt_sha256':EXPECTED,'original_bytes_preserved':True,'schema_validation':'PASS - all keywords used by pinned schema checked with local standard-library validator','schema_sha256':sha(schema_raw),'case':'D00','version':'0.1.3.0','status':receipt['status'],'reason':receipt['reason'],'run_id':receipt['run_id'],'process_instance_id':receipt['process_instance_id'],'observed_at_utc':receipt['observed_at_utc'],'observed_at_America_Chicago':'2026-10-17 14:33:43.607 CDT','sequence':receipt['sequence'],'elapsed_monotonic_ms':receipt['elapsed_monotonic_ms'],'role_comparison':comparison,'persistence_evidence':'Retrieved terminal file with durable-checkpoint marker; no separate PersistenceError field exists in receipt; photo shows receipt-saved success message','privacy_review':'No personal account/device/network identifiers found in supplied fixed fields; reviewed copy unchanged','sanitized_copy_sha256':sha(sanitized.read_bytes()),'photo_correlation':'PASS supporting visual evidence; photo shows D00 PASS and saved receipt; run association owner-attested, no visible run/time ID','photo_sha256':'74f383324231a453d88474ebc8a83a4ffb7c178f720c0384cbe6b8b7be8bf6fa','formal_overall_acceptance':'PASS - native D00 scope only','limits':['Receipt is not cryptographically signed; Xbox origin/retrieval context is owner-attested','Receipt timestamp is console-reported; not a measured clock synchronization','Sequence2 is structurally consistent; previous file versions are not separately preserved','Durable write strategy is not power-loss durability certification']}
(OUT/'RECEIPT-VERIFICATION.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

