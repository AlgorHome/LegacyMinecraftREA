from pathlib import Path
import json,csv,hashlib,re,datetime,importlib.util
BASE=Path(__file__).parent;DOC=BASE.parent/'docs/research/legacy-launcher'
cases=[]
for name,prefix in [('WINDOWS-SANDBOX-TESTS.md','W'),('XBOX-SERIES-X-TESTS.md','X')]:
 for line in (DOC/name).read_text(encoding='utf-8').splitlines():
  match=re.match(r'\| ('+prefix+r'\d{2}) \| (.*?) \| (.*?) \|',line)
  if not match:continue
  test_id,action,acceptance=match.groups()
  fields=['environment.os_build','observation.exit_or_hresult']
  if prefix=='W':fields+=['environment.isolation_type','environment.isolation_approved','artifacts.installer_sha256']
  else:fields+=['environment.console_model','environment.debugger_attached','artifacts.appx_sha256']
  if test_id in ['W10','W11','X03','X04','X05','X06','X07','X08','X09','X10','X11','X12']:
   fields+=['artifacts.jvm_sha256','target.runtime_id','target.java_major']
  if test_id in ['W10','W11','X05','X06','X07','X08','X09','X10','X11','X12']:
   fields+=['target.minecraft_version','target.loader','target.loader_version','artifacts.glfw_sha256','artifacts.mesa_sha256','artifacts.manifest_sha256']
  if test_id=='W09':fields+=['artifacts.valid_publisher_fixture_sha256','observation.signature_acceptance','observation.signature_rejections']
  if test_id=='X03':fields+=['target.jni_requested','target.jni_accepted','observation.synthetic_java_result']
  if test_id=='X02':fields+=['observation.memory_peak_bytes','observation.resource_samples']
  if test_id=='X06':fields+=['observation.graphics_version','observation.presented_frames','observation.graphics_capability_results']
  if test_id in ['W12','X11']:fields+=['observation.auth_stage_results','observation.ownership_result']
  blockers=(['APPROVED_ISOLATED_WINDOWS_GUEST_UNAVAILABLE'] if prefix=='W' else ['CONSOLE_ACCESS_OR_OWNER_RECEIPT_UNAVAILABLE','EXACT_APPROVED_APPX_RUNTIME_PACKAGE_NOT_SUPPLIED'])
  if test_id=='W09':blockers+=['TRUSTED_CORRECTLY_PUBLISHER_SIGNED_FIXTURE_UNAVAILABLE']
  if test_id in ['W12','X11']:blockers+=['OWNER_ACCOUNT_ACTION_NOT_PERFORMED']
  cases.append({'test_id':test_id,'scope':'actual Windows target' if prefix=='W' else 'actual Xbox Series X package','action':action,'criteria':[{'id':test_id+'.result','requirement':acceptance}],'required_pass_fields':list(dict.fromkeys(fields)),'current_status':'BLOCKED','blockers':blockers})
assert len(cases)==25
matrix=DOC/'evidence/target-validation-matrix.csv';rows=list(csv.DictReader(matrix.open(encoding='utf-8')))
target_plans=[]
for r in rows:
 blockers=['APPROVED_XBOX_PACKAGE_NOT_SUPPLIED','NO_NEW_OWNER_HARDWARE_RECEIPT']
 if r['minecraftVersion']=='1.12.2':blockers+=['PROVIDER_NOT_IMPLEMENTED_IN_APPROVED_CATALOG']
 if r['javaRuntime'] in ['java17','legacy']:blockers+=['JNI_21_REQUEST_VS_OLDER_RUNTIME_AGREEMENT_UNVERIFIED']
 r['blocker']='; '.join(blockers)
 r['requiredTestIds']='X01;X02;X03;X04;X05;X06;X07;X08;X09;X10;X11;X12;X13'
 r['requiredArtifactHashes']='appx;jvm;glfw;mesa;manifest;loader-artifacts'
 r['sourceImplementationStatus']='UNSUPPORTED_PROVIDER' if r['minecraftVersion']=='1.12.2' else 'SOURCE_PRESENT_RUNTIME_UNVERIFIED'
 target_plans.append({'target_id':r['targetId'],'source_commit':'d1453434ceefe73bef5aff497194e09f39dde7e1','minecraft_version':r['minecraftVersion'],'loader':r['loader'],'loader_version':r['loaderVersion'],'runtime_id':r['javaRuntime'],'java_major_expected':{'java21':21,'java17':17,'legacy':8}.get(r['javaRuntime']),'source_support_label':r['supportLevel'],'source_implementation_status':r['sourceImplementationStatus'],'required_test_ids':r['requiredTestIds'].split(';'),'required_artifact_hashes':r['requiredArtifactHashes'].split(';'),'loader_preparation_requirements':{'fabric':['exact inherited Fabric profile JSON','Fabric loader and intermediary JAR hashes','compatible patched filesystem/remap components'],'forge':['exact installer/profile metadata','client processor input/output hashes','final main/module/classpath arguments'],'neoforge':['exact installer/install profile','NeoForm and tool processor input/output hashes','final main/module/classpath arguments'],'vanilla':['exact vanilla metadata/client hashes','supported vanilla launch provider']}[r['loader']],'blockers':blockers,'new_runtime_status':'BLOCKED','accepted_receipts':[]})
with matrix.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
plan={'schema':'legacyforge-phase6a-test-cases-v1','source_commit':'d1453434ceefe73bef5aff497194e09f39dde7e1','observation_policy':'No PASS without actual corresponding target/device observation; static/analyzer/synthetic control checks do not substitute.','cases':cases,'target_plans':target_plans,'limitations':['Receipt validation checks completeness and hash references; it cannot certify observation truth','Every current behavioral case and target remains BLOCKED','All 56 approved targets are retained; unsupported legacy providers are not silently counted as tested']}
(DOC/'tests/test-cases.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
t=json.loads((DOC/'tests/result.template.json').read_text(encoding='utf-8'))
t['evidence']={'kind':None,'observed_at_utc':None,'observer_role':None,'criteria_results':{},'attachments':[]}
t['environment']['isolation_type']=None;t['environment']['isolation_approved']=False;t['artifacts']['installer_sha256']=None
(DOC/'tests/result.template.json').write_text(json.dumps(t,indent=2),encoding='utf-8')
for n in ['WINDOWS-SANDBOX-TESTS.md','XBOX-SERIES-X-TESTS.md']:
 p=DOC/n;s=p.read_text(encoding='utf-8')
 if n.startswith('WINDOWS'):
  s=s.replace('Isolated synthetic update fixtures with valid/invalid/truncated signatures','Retained genuine publisher-signed metadata plus corrupted/truncated copies; run only in approved guest')
  s=s.replace('Signed-path acceptance/rejection and failure receipts; no internet-controlled target update or authentication; do not alter production code to force success','Validate authentic fixture origin/key/hash first; signed-path acceptance and corrupted/truncated rejection receipts; never substitute an analyst key or change the target trust anchor')
 s+='''
## Machine-readable acceptance and receipts

`tests/test-cases.json` enumerates W01–W12 and X01–X13 with required pass fields and current blockers. Its target_plans retain all 56 exact version/loader/runtime tuples, loader-preparation requirements, package/runtime/native/manifest hashes and required X-gate references. The 1.12.2 provider limitation and Java 17/8 JNI question have their own blockers.

Validate an owner-prepared sanitized receipt without executing targets or contacting a device:

```powershell
python tools/verify-test-receipts.py tests/test-cases.json tests/result.template.json
```

A valid BLOCKED receipt is still BLOCKED. A PASS receipt requires actual-observation evidence, every criterion, nonempty required fields and hash-bound sanitized attachments. The validator checks structure/reference integrity, not the truth of an operator's claim. There is no deployment, connection, credential collection or automatic execution in this command.
'''
  # Fix W09 explicitly: possession of public key cannot generate a valid vendor signature.
 if n.startswith('WINDOWS'):
  s+='''
For W09, a correctly publisher-signed response must be obtained from a retained trusted response or independently verified official public endpoint, with original bytes/hash and matching embedded-key identity preserved locally. The public key alone cannot create a valid signature. Corrupted/truncated copies provide negative cases. A separately generated analyst-key fixture validates only an independent harness and cannot pass the actual launcher's publisher-key test. No trusted positive fixture is currently supplied; W09 remains BLOCKED.
'''
 p.write_text(s,encoding='utf-8')
# Verification of the new validator itself, using synthetic records only.
module_path=DOC/'tools/verify-test-receipts.py';spec=importlib.util.spec_from_file_location('receipt_validator',module_path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
cm={c['test_id']:c for c in cases};blocked=t.copy();blocked['test_id']='X01';assert not mod.validate(blocked,cm,DOC/'tests/result.template.json')
fake=json.loads(json.dumps(t));fake['status']='PASS';assert mod.validate(fake,cm,DOC/'tests/result.template.json')
unknown=json.loads(json.dumps(t));unknown['test_id']='X99';assert mod.validate(unknown,cm,DOC/'tests/result.template.json')
assert len(target_plans)==56 and len([r for r in target_plans if r['source_implementation_status']=='UNSUPPORTED_PROVIDER'])==2
result={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case_count':25,'target_count':56,'unsupported_provider_rows':2,'validator_self_checks':{'blocked_template_accepted_as_blocked':True,'unsupported_case_rejected':True,'unsubstantiated_pass_rejected':True},'behavioral_tests_executed':0,'status':'BLOCKED_REQUIRES_REAL_ENVIRONMENT_AND_EVIDENCE'}
(BASE/'final-audit/acceptance-plan-checks.json').parent.mkdir(parents=True,exist_ok=True)
(BASE/'final-audit/acceptance-plan-checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
