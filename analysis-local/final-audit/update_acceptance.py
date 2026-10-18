from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/research/legacy-launcher'
p = DOC / 'tests/test-cases.json'
plan = json.loads(p.read_text(encoding='utf-8'))
for case in plan['cases']:
    tid = case['test_id']
    name = 'WINDOWS-SANDBOX-TESTS.md' if tid.startswith('W') else 'XBOX-SERIES-X-TESTS.md'
    match = re.search(r'^\| ' + tid + r' \| (.*?) \| (.*?) \|$', (DOC/name).read_text(encoding='utf-8'), re.M)
    assert match, tid
    case['action'] = match.group(1)
    case['criteria'][0]['requirement'] = match.group(2)
    fields = case['required_pass_fields']
    if tid in ('W10', 'W11'):
        fields[:] = [f for f in fields if f not in ('artifacts.glfw_sha256', 'artifacts.mesa_sha256')]
        fields += ['artifacts.native_inventory_sha256', 'artifacts.graphics_provider_sha256']
    if tid == 'X04':
        fields += ['artifacts.jvm_sha256', 'target.runtime_id', 'target.java_major']
    if tid in ('W10', 'W11', 'X10', 'X11', 'X12'):
        fields += ['artifacts.loader_inventory_sha256']
    if tid in ('X03', 'X04', 'X05', 'X06', 'X07', 'X08'):
        case['blockers'].append('APPROVED_DIAGNOSTIC_PACKAGE_NOT_SUPPLIED')
    case['required_pass_fields'] = list(dict.fromkeys(fields))
    case['blockers'] = list(dict.fromkeys(case['blockers']))
    if tid == 'W09' and (DOC/'evidence/signed-update-fixture.json').is_file():
        fixture = json.loads((DOC/'evidence/signed-update-fixture.json').read_text(encoding='utf-8'))
        assert fixture['verification']['result'] == 'VALID'
        case['blockers'] = [b for b in case['blockers'] if b != 'TRUSTED_CORRECTLY_PUBLISHER_SIGNED_FIXTURE_UNAVAILABLE']
        case['available_positive_fixture'] = {
            'evidence_id':'E20', 'response_sha256':fixture['response_sha256'],
            'embedded_key_der_sha256':fixture['key']['der_sha256'],
            'url':fixture['requested_url'],
            'independent_verification':'VALID',
            'actual_target_acceptance':'BLOCKED',
            'raw_fixture_published':False,
        }
for target in plan['target_plans']:
    if target['loader_version'] == 'selected':
        target['blockers'].append('EXACT_LOADER_VERSION_UNRESOLVED_IN_APPROVED_SOURCE')
    target['blockers'].append('APPROVED_DIAGNOSTIC_PACKAGE_NOT_SUPPLIED')
    target['blockers'] = list(dict.fromkeys(target['blockers']))
plan['limitations'] += [
    'Nested field names are restricted; free text and attachment bytes still require manual privacy review',
    'X12 receipt validation binds exact tuples and predecessor receipts; aggregate 56-target and four-runtime-family completeness requires a separate coverage review',
    'Synthetic checker controls and compilation of independently written probes are analyst checks, never behavioral target passes',
]
plan['limitations'] = list(dict.fromkeys(plan['limitations']))
p.write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
matrix = DOC / 'evidence/target-validation-matrix.csv'
with matrix.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
by_id = {t['target_id']: t for t in plan['target_plans']}
for row in rows:
    row['blocker'] = '; '.join(by_id[row['targetId']]['blockers'])
with matrix.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
template = DOC / 'tests/result.template.json'
record = json.loads(template.read_text(encoding='utf-8'))
for key in ('valid_publisher_fixture_sha256', 'native_inventory_sha256', 'graphics_provider_sha256', 'loader_inventory_sha256'):
    record['artifacts'][key] = None
record['evidence']['prerequisite_receipts'] = []
template.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'cases': len(plan['cases']), 'targets': len(plan['target_plans']), 'behavioral_passes': 0}))
