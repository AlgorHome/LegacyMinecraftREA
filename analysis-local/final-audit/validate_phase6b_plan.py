"""Read/check planning documents; never build or execute a target."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / 'docs/research/phase-6b-runtime-validation'
DOSSIER = ROOT / 'docs/research/legacy-launcher'
SOURCE = ROOT / 'analysis-local/legacyforge-d145343'
PIN = 'd1453434ceefe73bef5aff497194e09f39dde7e1'
errors = []
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
sealed = []
for line in (DOSSIER/'evidence/SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    expected, rel = line.split('  ', 1)
    actual = sha(DOSSIER/rel)
    sealed.append({'path':rel,'matches':expected == actual})
    if expected != actual:
        errors.append('sealed Phase6A file changed: ' + rel)
head = subprocess.run(['git','-C',str(SOURCE),'rev-parse','HEAD'],check=True,capture_output=True,text=True).stdout.strip()
dirty = subprocess.run(['git','-C',str(SOURCE),'status','--porcelain'],check=True,capture_output=True,text=True).stdout
if head != PIN or dirty:
    errors.append('approved production source drift')
required = ['README.md','PHASE-6A-EVIDENCE-SUMMARY.md','WINDOWS-EXECUTION-PLAN.md',
            'XBOX-DIAGNOSTIC-HARNESS.md','HARDWARE-ACCEPTANCE.md','DIAGNOSTIC-MATRIX.md',
            'LEGACY-1.12.2-ASSESSMENT.md','PLATFORM-REFERENCES.md','receipt.template.json']
for name in required:
    if not (PLAN/name).is_file():
        errors.append('missing plan: ' + name)
link_count = 0
for path in PLAN.iterdir():
    if not path.is_file():
        continue
    if path.suffix not in ('.md','.json','.txt'):
        errors.append('unexpected implementation/binary artifact: ' + path.name)
        continue
    text = path.read_text(encoding='utf-8')
    if path.suffix == '.json':
        json.loads(text)
    if re.search(r'C:[\\/]+Users[\\/]+arinze|-----BEGIN .*PRIVATE KEY-----', text):
        errors.append('personal path or key pattern: ' + path.name)
    if path.suffix == '.md':
        for dest in re.findall(r'\]\(([^)]+)\)',text):
            if dest.startswith(('https:','http:','#')):
                continue
            link_count += 1
            target = (path.parent/dest.split('#')[0]).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append('broken/outside-research link: ' + path.name + ' -> ' + dest)
matrix = (PLAN/'DIAGNOSTIC-MATRIX.md').read_text(encoding='utf-8')
cases = re.findall(r'^\| (D\d{2}) \|',matrix,re.M)
if cases != ['D%02d'%i for i in range(19)]:
    errors.append('D00-D18 mapping incomplete or duplicate')
receipt = json.loads((PLAN/'receipt.template.json').read_text(encoding='utf-8'))
if receipt['status'] != 'PLANNED' or receipt['claims']['target_executed'] is not False:
    errors.append('template claims execution')
if any(value is not None for value in receipt['observation'].values()):
    errors.append('template contains fabricated observations')
source_hashes = {
    'MC.Xbox/launch/minecraft_launch.cpp':'c37eade570d45fbdad0ba876be3347729b1000e579692c1819d059dbf80b5b12',
    'MC.Xbox/launch/runtime_manager.cpp':'fad066071b9c8914350d719fd08e2ea516daa59b6087b83ba45c96bb4787eeaf',
    'glfw_shim/glfw_uwp.cpp':'0dde9a0c2e0e9b6f028fae5efe9d45a8a81a1e26e330bb72d42cacc3a4ad4d10',
}
for rel, expected in source_hashes.items():
    if sha(SOURCE/rel) != expected:
        errors.append('source hash differs: ' + rel)
result = {
    'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Planning structure, links, source identity and sealed evidence integrity only; not runtime validation',
    'source_commit':head,'production_source_clean':not bool(dirty),
    'sealed_phase6a_manifest_sha256':sha(DOSSIER/'evidence/SHA256SUMS.txt'),
    'sealed_phase6a_entries_checked':len(sealed),
    'sealed_phase6a_unchanged':all(x['matches'] for x in sealed),
    'required_planning_documents_and_template':len(required),
    'local_links_checked':link_count,'mapped_diagnostic_case_count':len(cases),
    'initial_profiles':['NATIVE-CONTROL','S21'],
    'deferred_profiles':['S17','S8','S25'],
    'implementation_created':False,'builds_performed':0,'target_executions':0,
    'production_changes':False,'authentication_or_entitlement_changes':False,
    'third_party_binary_downloads':0,'actual_hardware_passes':0,
    'approval_state':'AWAITING_EXPLICIT_APPROVAL_FOR_IMPLEMENTATION_AND_EXECUTION',
    'errors':errors,
}
(PLAN/'planning-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
with (PLAN/'SHA256SUMS.txt').open('w',encoding='utf-8') as output:
    for path in sorted(PLAN.iterdir()):
        if path.is_file() and path.name != 'SHA256SUMS.txt':
            output.write(sha(path)+'  '+path.name+'\n')
for line in (PLAN/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    expected, rel = line.split('  ',1)
    if sha(PLAN/rel) != expected:
        errors.append('plan checksum mismatch: ' + rel)
print(json.dumps(result,indent=2))
if errors:
    raise SystemExit(1)
