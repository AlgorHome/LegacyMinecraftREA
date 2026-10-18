from pathlib import Path
import json,hashlib,zipfile,subprocess,sys,uuid
ROOT=Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft');REPO=ROOT/'phase6b1-diagnostics';OUT=Path(__file__).parent
RECEIPT=Path(r'C:\Users\arinze\Desktop\D06-SRV02-8A125555-353C-4C3D-AD19-D8849FD138A8.json');PHOTO=Path(r'C:\Users\arinze\Desktop\IMG_5565.JPG')
COMMIT='c81d0f48286513f7a7579a1d2d786cca4f5e60e2'
sha=lambda b:hashlib.sha256(b).hexdigest()
hashfile=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
build=load(ROOT/'docs/research/phase-6b5-d06-srv02/BUILD-EVIDENCE.json')
sign=load(ROOT/'docs/research/phase-6b5t-srv02-signing/SIGNING-VERIFICATION.json')
frozen=load(ROOT/'docs/research/phase-6b5-d06-srv02/BASELINE-PRESERVATION.json')
preserved={x['path']:x['sha256'] for x in sign['preservedFiles']}
for folder in ('phase-6b5t-srv02-signing','phase-6b5r-srv01-hardware-acceptance'):
 for p in (ROOT/'docs/research'/folder).rglob('*'):
  if p.is_file():preserved[str(p)]=hashfile(p)
receipt_hash=hashfile(RECEIPT);photo_hash=hashfile(PHOTO)
assert receipt_hash=='307dde1773ff9f5aba5b44862c7e9ef1c4179d97035161d873d832364a6e0436'
assert len(frozen['files'])==175
assert all(hashfile(x['path'])==x['sha256'] for x in frozen['files'])
assert all(hashfile(p)==h for p,h in preserved.items())
unsigned=Path(sign['unsignedPath']);signed=Path(sign['signedPath'])
assert hashfile(unsigned)==build['unsignedAppxSha256']=='88cde899358b6eaade1658802831c5a914b8e637cf1466321b233fa8a2788c31'
assert hashfile(signed)=='a77e31a5922bca35a09084dbe885b5d13ed1207571f66458644d5ac7ee8738d5'
assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()==COMMIT
assert subprocess.check_output(['git','-C',str(REPO),'status','--porcelain'],text=True).strip()==''
for name in ['tools/receipt_contract.py','src/probe.cpp','src/report.cpp','src/app.cpp','profiles/D06-SRV02.json']:
 rel='diagnostics/NativeCapabilities/'+name
 assert subprocess.check_output(['git','-C',str(REPO),'show',COMMIT+':'+rel]).replace(b'\r\n',b'\n')==(REPO/rel).read_bytes().replace(b'\r\n',b'\n'),name
sys.path.insert(0,str(REPO/'diagnostics/NativeCapabilities/tools'))
from receipt_contract import read_json,validate,DESC,SRV_DESC
r=read_json(RECEIPT.read_bytes())
with zipfile.ZipFile(unsigned) as u,zipfile.ZipFile(signed) as s:
 schema=read_json(u.read('contracts/native-receipt.schema.json'))
 assert u.read('contracts/native-receipt.schema.json')==(ROOT/'docs/research/phase-6b5-d06-srv02/RECEIPT-SCHEMA.json').read_bytes()
 validate(r,schema)
 policy=read_json(u.read('profiles/D06-SRV02.json'))
 inputs=read_json(u.read('native-inputs.json'))
 assert inputs['sourceCommit']==inputs['compiledSourceCommit']==r['source_commit']==COMMIT
 assert inputs['buildId']==r['build_id']==build['buildId']
 roles=[]
 for role,member in build['payloadRoleMembers'].items():
  digest=sha(u.read(member))
  assert digest==build['payloadRoleSha256'][role]==r['payload_hashes'][role]
  assert u.read(member)==s.read(member)
  roles.append(dict(role=role,member=member,independentSha256=digest,receiptMatches=True,pinnedBuildMatches=True,signedBytesMatch=True))
assert r['schema']=='legacyforge-native-capability-receipt-v5' and r['status']=='PASS' and r['terminal'] and r['stage']=='FINAL'
assert r['reason']=='SRV_BACKING_RESOURCE_IDENTITY_CONFIRMED' and r['sequence']==6
assert r['last_durable_checkpoint_stage']=='BEFORE_GET_RESOURCE' and r['receipt_persistence_result']=='VERIFY_BY_RETRIEVAL'
assert r['run_id']=='8A125555-353C-4C3D-AD19-D8849FD138A8' and RECEIPT.name=='D06-SRV02-'+r['run_id']+'.json'
assert uuid.UUID(r['run_id']).version==uuid.UUID(r['process_instance_id']).version==4
assert r['run_id']!=r['process_instance_id']
assert (r['package_name'],r['package_publisher'],r['package_version'],r['architecture'],r['application_id'],r['expected_package_identity'])==('AlgorHome.LegacyForge.NativeDiagnostics','CN=LegacyForgeDiagnostics','0.2.4.0','x64','App',True)
assert not any(r[k] for k in ('java_jni_enabled','minecraft_or_gameplay_tested','all_d06_certified','watchdog_cancels_native_calls'))
d=r['details']
assert d['requested_descriptor']==d['returned_descriptor']==policy['requested_descriptor']==DESC
assert d['srv_requested_descriptor']==d['srv_returned_descriptor']==policy['srv_requested_descriptor']==SRV_DESC
for stem in ('creation','texture','srv','texture_identity_query','resource_identity_query'):
 assert d[stem+'_hresult']=='0x00000000' and d[stem+'_hresult_signed']==0
assert d['get_resource_called'] and d['backing_resource_returned'] and d['canonical_identity_equal']
assert not any('get_resource' in k and 'hresult' in k for k in d)
probe=(REPO/'diagnostics/NativeCapabilities/src/probe.cpp').read_text()
assert probe.count('srv->GetResource(resource.put())')==1
assert probe.count('->QueryInterface(__uuidof(IUnknown),')==2
assert 'originalIdentity.get()==backingIdentity.get()' in probe
before=d['memory_before'];after=d['memory_after_release']
headroom=before['limit_bytes']-before['usage_bytes'];growth=after['usage_bytes']-before['usage_bytes']
assert headroom>=policy['minimum_headroom_bytes'] and growth<=policy['maximum_observed_growth_bytes']
assert r['elapsed_monotonic_ms']==62<r['deadline_ms']==policy['deadline_ms']==10000
assert hashfile(RECEIPT)==receipt_hash and hashfile(PHOTO)==photo_hash
assert all(hashfile(p)==h for p,h in preserved.items())
result=dict(verdict='PASS_D06_SRV02_ONLY',receipt=dict(path=str(RECEIPT),sha256=receipt_hash,bytes=RECEIPT.stat().st_size,schema=r['schema'],terminalSequence=6,elapsedMs=62,runId=r['run_id'],processInstanceId=r['process_instance_id'],observedAtUtcUnverified=r['observed_at_utc']),photograph=dict(path=str(PHOTO),sha256=photo_hash,bytes=PHOTO.stat().st_size,visuallyReviewed=True,exactRunIdMatch=True,savedReceiptMessageVisible=True,versionAndCaseMatch=True),sourceCommit=COMMIT,buildId=r['build_id'],unsignedSha256=hashfile(unsigned),signedSha256=hashfile(signed),sixRoleChecks=roles,schemaAndSemanticValidation='PASS',creationAndDescriptorPolicy='PASS',voidGetResourceSingleSourceCall='PASS',canonicalIdentityQueries='PASS',releaseOrderSourceAndReceipt='PASS',memory=dict(before=before,afterRelease=after,headroomBytes=headroom,growthBytes=growth,growthMiB=growth/1048576,policyPass=True),deadline='PASS: 62ms below 10000ms, no native cancellation claim',persistence='PASS: owner-retrieved matching run final JSON; no independent console read performed',checkpoints='Final sequence 6 and predecessor BEFORE_GET_RESOURCE consistent with pinned source; earlier checkpoint bytes not supplied',frozenBaselineFilesVerified=175,totalPreservedFilesVerified=len(preserved),originalEvidenceUnchanged=True,sourceUnchanged=True,targetExecutedByReviewer=False,consoleAccess=False,stages=dict(registration='Owner-attested through matching running package identity; no independent portal inspection',activation='PASS: photograph and terminal run evidence',visibleStatus='PASS',nativeCase='PASS',receipt='PASS',persistence='PASS within retrieval provenance limits',overall='PASS_D06_SRV02_ONLY'),chainTrust='Prior SignTool verification FAILED CERT_E_UNTRUSTEDROOT; unchanged, independent of acceptance')
(OUT/'HARDWARE-VERIFICATION.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(verdict=result['verdict'],receiptSha256=receipt_hash,photoSha256=photo_hash,sixRoles=len(roles),memoryGrowthMiB=growth/1048576,frozenBaselines=175,totalPreserved=len(preserved)),indent=2))
