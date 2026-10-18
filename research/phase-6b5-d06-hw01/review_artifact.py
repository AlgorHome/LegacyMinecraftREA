"""Additional static provenance/framework export/schema review. No target execution."""
import ast,hashlib,json,struct,subprocess,zipfile
from pathlib import Path
OUT=Path(__file__).parent
ROOT=OUT.parents[2]
REPO=ROOT/'phase6b1-diagnostics'
BUILD=REPO/'diagnostics/NativeCapabilities/out/20261017-173106-d79a3eae'
sha=lambda b:hashlib.sha256(b).hexdigest()
audit=json.loads((BUILD/'static-safety.json').read_text())
record=json.loads((BUILD/'build-receipt.json').read_text(encoding='utf-8-sig'))
assert record['status']=='BUILD_STATIC_PASS_NOT_EXECUTED'
assert all(c['exitCode']==0 for c in record['commands'])
commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
assert commit==audit['sourceCommit']==record['sourceCommit']
paths=subprocess.check_output(['git','-C',str(REPO),'diff','--name-only','553c655','HEAD'],text=True).splitlines()
assert all(p.startswith('diagnostics/NativeCapabilities/') for p in paths)
assert not subprocess.check_output(['git','-C',str(REPO),'status','--porcelain'],text=True).strip()
preserved=json.loads((ROOT/'docs/research/phase-6b5-native-capabilities/BASELINE-PRESERVATION.json').read_text(encoding='utf-8-sig'))
for item in preserved['artifacts']+preserved['diagnosticSourceFiles']:
    assert sha(Path(item['path']).read_bytes())==item['sha256'],item['path']

parser_source=ROOT/'analysis-local/native_audit.py'
tree=ast.parse(parser_source.read_text())
function=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='parse')
scope={'struct':struct,'hashlib':hashlib}
exec(compile(ast.Module(body=[function],type_ignores=[]),'<pure-parser>','exec'),scope)
framework=Path(r'C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\x64\Microsoft.VCLibs.140.00_14.0.33519.0_x64.appx')
assert sha(framework.read_bytes())=='9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283'
matches=[]
with zipfile.ZipFile(framework) as z:
    for module in audit['nativeImports']:
        if module['module'].lower() in ('msvcp140_app.dll','vcruntime140_app.dll','vcruntime140_1_app.dll'):
            name=next(n for n in z.namelist() if Path(n).name.lower()==module['module'].lower())
            info=scope['parse'](Path('unused'),OUT,'framework',z.read(name),name)
            names={e['name'] for e in info['named_exports']}
            missing=[n for n in module['symbols'] if n not in names]
            assert not missing,(module['module'],missing)
            matches.append({'module':module['module'],'required_exports':module['symbols'],'all_present':True,'framework_module_sha256':info['sha256']})
schema=json.loads((REPO/'diagnostics/NativeCapabilities/contracts/native-receipt.schema.json').read_text())
def check_schema(s):
    if isinstance(s,dict):
        if '$ref' in s:
            assert s['$ref'].startswith('#/$defs/') and s['$ref'].split('/')[-1] in schema['$defs']
        if s.get('type')=='object':
            assert set(s.get('required',[]))<=set(s.get('properties',{}))
        for value in s.values():check_schema(value)
    elif isinstance(s,list):
        for value in s:check_schema(value)
check_schema(schema)
assert schema['properties']['case_id']['const']=='D06-HW01'
assert schema['properties']['package_name']['const']=='AlgorHome.LegacyForge.NativeDiagnostics'
assert schema['properties']['java_jni_enabled']['const'] is False
result={'mode':'STATIC_REVIEW_ONLY','verdict':'PASS_STATIC_ONLY','source_commit':commit,'unsigned_appx':str(BUILD/'NativeCapabilities.unsigned.appx'),'unsigned_sha256':audit['unsignedAppxSha256'],'changes_confined_to_new_project':True,'frozen_baseline_artifacts_and_sources_unchanged':True,'CRT_export_comparison':matches,'framework_reference_sha256':'9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283','system_api_sets':'Unresolved against Xbox; Microsoft contract review plus exact direct symbol inventory, not complete transitive loader proof','receipt_schema':'JSON syntax, local references, required/property consistency and case/native flags checked; no target receipt produced','signed':False,'installed':False,'executed':False}
(OUT/'ADDITIONAL-STATIC-REVIEW.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

