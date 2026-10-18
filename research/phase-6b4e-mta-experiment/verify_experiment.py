"""Verify source and APPX bytes only. No diagnostic/DLL execution."""
import ast
import hashlib
import json
import struct
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

OUT=Path(__file__).parent
ROOT=OUT.parents[2]
REPO=ROOT/'phase6b1-diagnostics'
REL='diagnostics/RuntimeDiagnostics/'
BASE=REPO/REL/'out/20261017-140332-19d39263'
NEW=REPO/REL/'out/20261017-142300-e07d5ee8'
sha=lambda data:hashlib.sha256(data).hexdigest()
def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args])

oldapp=git('show','c70a17e:'+REL+'src/app.cpp')
newapp=(REPO/REL/'src/app.cpp').read_bytes()
assert oldapp.count(b'winrt::apartment_type::single_threaded')==1
assert oldapp.replace(b'winrt::apartment_type::single_threaded',b'winrt::apartment_type::multi_threaded')==newapp
assert not git('diff','c70a17e','HEAD','--',REL+'include',REL+'contracts',REL+'src/native_control.cpp',REL+'src/report.cpp',REL+'src/jni_smoke.cpp',REL+'build.ps1')
changed=git('diff','--name-only','c70a17e','HEAD').decode().splitlines()
assert set(changed)=={REL+'src/app.cpp',REL+'package/Package.appxmanifest',REL+'tools/verify_artifacts.py',REL+'docs/MTA-EXPERIMENT.md'}

# Extract the existing pure parser AST only; omit its top-level scans.
parser_path=ROOT/'analysis-local/native_audit.py'
tree=ast.parse(parser_path.read_text())
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='parse')
scope={'struct':struct,'hashlib':hashlib}
exec(compile(ast.Module(body=[function],type_ignores=[]),'<static-pe-parser>','exec'),scope)
ns={'p':'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
with zipfile.ZipFile(BASE/'RuntimeDiagnostics.unsigned.appx') as old, zipfile.ZipFile(NEW/'RuntimeDiagnostics.unsigned.appx') as new:
    assert set(old.namelist())==set(new.namelist())
    assert 'AppxSignature.p7x' not in new.namelist() and new.testzip() is None
    first,last=[ET.fromstring(z.read('AppxManifest.xml')) for z in (old,new)]
    assert first.find('p:Identity',ns).get('Version')=='0.1.2.0'
    assert last.find('p:Identity',ns).get('Version')=='0.1.3.0'
    assert last.find('p:Applications/p:Application',ns).get('EntryPoint')=='LegacyForgeDiagnostics.App'
    identity=dict(last.find('p:Identity',ns).attrib)
    last.find('p:Identity',ns).set('Version','0.1.2.0')
    assert ET.tostring(first)==ET.tostring(last)
    images=[scope['parse'](Path('unused'),OUT,'diagnostic',z.read('RuntimeDiagnostics.exe'),'RuntimeDiagnostics.exe') for z in (old,new)]
    assert images[0]['imports']==images[1]['imports']
    assert images[0]['delay_imports']==images[1]['delay_imports']
    assert images[1]['machine']=='0x8664'
    changes=[]
    for name in sorted(old.namelist()):
        a,b=old.read(name),new.read(name)
        if a!=b:
            item={'path':name,'baseline_sha256':sha(a),'experiment_sha256':sha(b)}
            if name.endswith('.json'):
                item['JSON_semantically_equal']=json.loads(a.decode('utf-8-sig'))==json.loads(b.decode('utf-8-sig'))
            changes.append(item)
    audit=json.loads((NEW/'d00-safety-audit.json').read_text())
    assert audit['verdict']=='PASS' and audit['configuration']=='D00Only' and not audit['capabilities']
    receipt=json.loads((NEW/'build-receipt.json').read_text(encoding='utf-8-sig'))
    assert receipt['sourceCommit']==git('rev-parse','HEAD').decode().strip()
    assert receipt['d00Only'] and all(c['exitCode']==0 for c in receipt['commands'])
    before=json.loads((OUT/'PRESERVATION-BEFORE.json').read_text(encoding='utf-8-sig'))
    for item in before:
        assert sha(Path(item['path']).read_bytes())==item['sha256']
    (OUT/'PRESERVATION-AFTER.json').write_text(json.dumps({'all_unchanged':True,'files':before},indent=2))
    result={'verdict':'PASS_STATIC_ONLY','source_commit':receipt['sourceCommit'],'source_changed_paths':changed,'sole_runtime_source_change':'entry-thread STA to MTA','manifest_only_change':'Version 0.1.2.0 to 0.1.3.0','identity':identity,'entrypoint':'LegacyForgeDiagnostics.App','capabilities':[],'unsigned_artifact':str(NEW/'RuntimeDiagnostics.unsigned.appx'),'unsigned_sha256':sha((NEW/'RuntimeDiagnostics.unsigned.appx').read_bytes()),'direct_imports_identical':True,'delay_imports_identical':True,'static_PE_baseline':images[0],'static_PE_experiment':images[1],'package_member_differences':changes,'preservation_PASS':True,'signed':False,'executed':False}
    (OUT/'EXPERIMENT-VERIFICATION.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('static_PE_baseline','static_PE_experiment')},indent=2))
