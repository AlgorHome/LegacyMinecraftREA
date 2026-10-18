"""Prepared offline original-receipt verifier. No target execution or console access.
Call only with the exact local JSON the owner retrieved; never edits the input.
Formal acceptance still requires separate provenance/photo/run-association review.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,sys,zipfile
ROOT=Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft')
OUT=Path(__file__).parent
COMMIT='4457142ff1fd9e01371eb446612c70162ce93357'
UNSIGNED_SHA='526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8'
SIGNED_SHA='ead7016c94e551fac43e2b622b323354bfa4506fe507f44bf5e98f112b8f0c3f'
ROLES={'executable_sha256':'NativeCapabilities.exe','manifest_sha256':'AppxManifest.xml',
       'build_inputs_sha256':'native-inputs.json','policy_sha256':'profiles/D06-RES01a.json',
       'schema_sha256':'contracts/native-receipt.schema.json','inventory_sha256':'native-inventory.json'}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('receipt',type=Path)
    p.add_argument('--expected-receipt-sha256',help='Optional independent owner pin; no fabricated default')
    a=p.parse_args();raw=a.receipt.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
    digest=sha(raw)
    if a.expected_receipt_sha256:assert digest==a.expected_receipt_sha256.lower(),'receipt hash mismatch'
    private=ROOT/'analysis-local/phase6b5l-res01a-retrieval/originals'
    private.mkdir(parents=True,exist_ok=True)
    # Hash-based evidence directory prevents overwriting a different supplied original.
    preserve=private/digest;preserve.mkdir(exist_ok=True)
    saved=preserve/a.receipt.name
    if saved.exists():assert saved.read_bytes()==raw
    else:shutil.copy2(a.receipt,saved)
    pins=json.loads((OUT/'EXPECTED-PAYLOADS.json').read_text())
    assert sha(Path(pins['unsignedPath']).read_bytes())==UNSIGNED_SHA
    assert sha(Path(pins['signedPath']).read_bytes())==SIGNED_SHA
    native=ROOT/'phase6b1-diagnostics/diagnostics/NativeCapabilities'
    with zipfile.ZipFile(pins['unsignedPath']) as z,zipfile.ZipFile(pins['signedPath']) as signed:
        inputs=json.loads(z.read('native-inputs.json').decode('utf-8-sig'))
        validator_pin=next(x['sha256'] for x in inputs['sourceFiles'] if x['path'].replace('\\','/')=='tools/receipt_contract.py')
        assert sha((native/'tools/receipt_contract.py').read_bytes())==validator_pin
        sys.dont_write_bytecode=True;sys.path.insert(0,str(native/'tools'))
        from receipt_contract import read_json,validate
        receipt=read_json(raw);schema=read_json(z.read('contracts/native-receipt.schema.json'))
        validate(receipt,schema)
        assert receipt['source_commit']==inputs['sourceCommit']==inputs['compiledSourceCommit']==COMMIT
        assert receipt['build_id']==inputs['buildId']=='20261017-183031-15ba7835'
        assert a.receipt.name=='D06-RES01a-'+receipt['run_id']+'.json','original name/run mismatch'
        matches=[]
        for role,member in ROLES.items():
            data=z.read(member);actual=sha(data)
            assert actual==receipt['payload_hashes'][role]
            assert data==signed.read(member)
            matches.append(dict(role=role,member=member,independentlyHashedSha256=actual,match=True))
        policy=read_json(z.read('profiles/D06-RES01a.json'))
        assert receipt['deadline_ms']==policy['deadline_ms']==10000
        if receipt['status']=='PASS':
            d=receipt['details']
            assert d['requested_descriptor']==d['returned_descriptor']==policy['requested_descriptor']
            assert d['memory_before']['limit_bytes']-d['memory_before']['usage_bytes']>=policy['minimum_headroom_bytes']
            assert d['memory_after_release']['usage_bytes']-d['memory_before']['usage_bytes']<=policy['maximum_observed_growth_bytes']
    assert a.receipt.read_bytes()==raw and saved.read_bytes()==raw
    result=dict(receiptSha256=digest,preservedOriginal=str(saved),independentOwnerHashSupplied=bool(a.expected_receipt_sha256),
                schemaAndBinding='PASS',receiptStatus=receipt['status'],terminal=receipt['terminal'],
                case=receipt['case_id'],version=receipt['package_version'],runId=receipt['run_id'],
                processId=receipt['process_instance_id'],reason=receipt['reason'],sequence=receipt['sequence'],
                elapsedMs=receipt['elapsed_monotonic_ms'],payloadMatches=matches,details=receipt['details'],
                visiblePass='OWNER_REPORTED_UNCORRELATED',photograph='NOT_SUPPLIED_TO_THIS_VERIFIER',
                formalAcceptance='PENDING_INDEPENDENT_ASSOCIATION_AND_FINAL_REVIEW',
                consoleClock='NOT_INDEPENDENTLY_VERIFIED',newTargetExecution=False,consoleAccess=False)
    (preserve/'LOCAL-VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
