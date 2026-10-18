"""Finalize derived research only. Never executes supplied target artifacts."""
from pathlib import Path
from collections import Counter
import csv
import datetime
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/research/legacy-launcher'
PIN = 'd1453434ceefe73bef5aff497194e09f39dde7e1'
SRC = ROOT / 'analysis-local/legacyforge-d145343'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def append_once(name, marker, text):
    path = DOC / name
    content = path.read_text(encoding='utf-8')
    if marker not in content:
        path.write_text(content.rstrip() + '\n\n' + text.strip() + '\n', encoding='utf-8')

required = ['README.md','PROVENANCE.md','FILE-INVENTORY.md','ARCHITECTURE.md',
            'INSTALLATION-PIPELINE.md','AUTH-BOUNDARIES.md','JVM-RUNTIME.md',
            'XBOX-UWP-COMPATIBILITY.md','LEGACYFORGE-GAP-ANALYSIS.md',
            'EVIDENCE-INDEX.md','UNKNOWN-SUBSYSTEMS.md','PHASE-6-ROADMAP.md']
plan = json.loads((DOC/'tests/test-cases.json').read_text(encoding='utf-8'))
matrix = list(csv.DictReader((DOC/'evidence/target-validation-matrix.csv').open(encoding='utf-8')))
source_rows = list(csv.DictReader((SRC/'config/versions.tsv').read_text(encoding='utf-8').replace('\\t', '\t').splitlines(), delimiter='\t'))

errors = []
for name in required:
    if not (DOC/name).is_file():
        errors.append('missing required document: ' + name)
expected_ids = {'W%02d'%i for i in range(1,13)} | {'X%02d'%i for i in range(1,14)}
if len(plan['cases']) != 25 or {c['test_id'] for c in plan['cases']} != expected_ids:
    errors.append('test case coverage differs')
if any(c['current_status'] != 'BLOCKED' for c in plan['cases']):
    errors.append('unsubstantiated behavioral status')
keys = ('minecraftVersion','loader','loaderVersion','javaRuntime')
source_tuples = {tuple(row[k] for k in keys) for row in source_rows}
matrix_tuples = {tuple(row[k] for k in keys) for row in matrix}
plan_tuples = {tuple(t[k] for k in ('minecraft_version','loader','loader_version','runtime_id')) for t in plan['target_plans']}
if len(source_rows) != 56 or len(matrix) != 56 or len(plan['target_plans']) != 56 or source_tuples != matrix_tuples or source_tuples != plan_tuples:
    errors.append('56 exact target tuples differ')
if any(r['newRuntimeTestStatus'] != 'BLOCKED' for r in matrix):
    errors.append('unsubstantiated target verdict')
if any(t['new_runtime_status'] != 'BLOCKED' or t['accepted_receipts'] for t in plan['target_plans']):
    errors.append('unexpected actual execution receipt')
if {r['javaRuntime'] for r in matrix} != {'current','java21','java17','legacy'}:
    errors.append('runtime family omitted')

head = subprocess.run(['git','-C',str(SRC),'rev-parse','HEAD'], capture_output=True, text=True, check=True).stdout.strip()
status = subprocess.run(['git','-C',str(SRC),'status','--porcelain'], capture_output=True, text=True, check=True).stdout
if head != PIN or status:
    errors.append('approved source pin or clean state differs')

# Restrict publication to authored text and derived metadata, not working binaries.
extensions = {'.md','.json','.csv','.txt','.example','.py','.java'}
for path in DOC.rglob('*'):
    if not path.is_file():
        continue
    rel = path.relative_to(DOC).as_posix()
    if path.suffix.lower() not in extensions or '__pycache__' in path.parts:
        errors.append('unexpected publication artifact: ' + rel)
        continue
    content = path.read_text(encoding='utf-8')
    if re.search(r'C:[\\/]+Users[\\/]+arinze|[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}',content):
        errors.append('personal path or token-like pattern: ' + rel)
    if path.suffix == '.json':
        json.loads(content)
    if path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if link.startswith(('http:','https:','#')):
                continue
            destination = link.split('#')[0]
            generated_integrity = (path.parent/destination).resolve() == (DOC/'evidence/research-integrity.json').resolve()
            if destination and not generated_integrity and not (path.parent/destination).is_file():
                errors.append('broken local link in ' + rel)
wsb = ET.fromstring((DOC/'tests/offline.wsb.example').read_text(encoding='utf-8'))
if any(wsb.findtext(k) != 'Disable' for k in ('Networking','ClipboardRedirection','AudioInput','VideoInput','PrinterRedirection','vGPU')) or wsb.find('LogonCommand') is not None or wsb.find('MappedFolders') is not None:
    errors.append('offline template controls changed')

# Bind all original analyst scripts. Recovered/proprietary working artifacts excluded.
tool_manifest = DOC / 'evidence/analyst-tool-hashes.json'
old = json.loads(tool_manifest.read_text(encoding='utf-8'))
script_paths = {ROOT/x['path'] for x in old}
script_paths.update((ROOT/'analysis-local/final-audit').rglob('*.py'))
script_paths.update((DOC/'tools').glob('*.py'))
script_paths.update((DOC/'tests/probes').glob('*.java'))
tools = []
for path in sorted(script_paths):
    if not path.is_file() or not path.is_relative_to(ROOT):
        errors.append('analyst source missing or outside research workspace')
        continue
    tools.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)})
tool_manifest.write_text(json.dumps(tools,indent=2)+'\n',encoding='utf-8')

result = {
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Publication structure, source pin, exact plan coverage and file integrity; not behavioral or privacy certification',
    'source_commit': head, 'production_source_clean': not bool(status),
    'required_documents': len(required),
    'test_gate_count': len(plan['cases']),
    'test_gate_statuses': dict(Counter(c['current_status'] for c in plan['cases'])),
    'target_rows': len(matrix), 'exact_source_matrix_plan_tuples_equal': source_tuples == matrix_tuples == plan_tuples,
    'runtime_family_counts':dict(Counter(r['javaRuntime'] for r in matrix)),
    'target_statuses':dict(Counter(r['newRuntimeTestStatus'] for r in matrix)),
    'actual_behavioral_tests_executed_by_investigation':0,
    'actual_behavioral_passes':0,
    'errors':errors,
}
(DOC/'evidence/research-integrity.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
with (DOC/'evidence/SHA256SUMS.txt').open('w',encoding='utf-8') as output:
    for path in sorted(DOC.rglob('*')):
        if path.is_file() and path.name != 'SHA256SUMS.txt':
            output.write(sha(path) + '  ' + path.relative_to(DOC).as_posix() + '\n')
for line in (DOC/'evidence/SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    digest, rel = line.split('  ',1)
    if sha(DOC/rel) != digest:
        errors.append('publication checksum mismatch: ' + rel)
result['publication_file_count'] = len([p for p in DOC.rglob('*') if p.is_file()])
result['publication_checksum_manifest_sha256'] = sha(DOC/'evidence/SHA256SUMS.txt')
(ROOT/'analysis-local/final-audit/publication-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
if errors:
    raise SystemExit(1)
