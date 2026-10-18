"""Validate Phase 6A evidence receipts. Does not execute software or contact devices.

Usage: python verify-test-receipts.py <test-cases.json> <receipt.json> [receipt...]
Success validates receipt completeness and attachment hashes, not truth of observations.
X12 checks one catalog tuple and its linked gates. All-56-target/four-runtime coverage
and manual privacy review remain separate; this tool does not certify either.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re

COMMIT = 'd1453434ceefe73bef5aff497194e09f39dde7e1'
STATUSES = {'PASS', 'FAILED', 'BLOCKED', 'INCONCLUSIVE'}
COMMON = {'schema', 'test_id', 'status', 'reason', 'source_commit', 'environment',
          'artifacts', 'target', 'observation', 'constraints', 'evidence'}
SECTION_FIELDS = {
    'environment': {'type', 'os_build', 'console_model', 'debugger_attached', 'network_mode', 'isolation_type', 'isolation_approved'},
    'artifacts': {'appx_sha256', 'launcher_sha256', 'installer_sha256', 'jvm_sha256', 'glfw_sha256', 'mesa_sha256', 'manifest_sha256', 'valid_publisher_fixture_sha256', 'graphics_provider_sha256', 'native_inventory_sha256', 'loader_inventory_sha256'},
    'target': {'minecraft_version', 'loader', 'loader_version', 'runtime_id', 'java_major', 'jni_requested', 'jni_accepted'},
    'observation': {'exit_or_hresult', 'duration_ms', 'memory_peak_bytes', 'checked_files', 'reused_files', 'downloaded_files', 'hash_failures', 'graphics_version', 'presented_frames', 'symptom', 'signature_acceptance', 'signature_rejections', 'synthetic_java_result', 'resource_samples', 'graphics_capability_results', 'auth_stage_results', 'ownership_result'},
    'evidence': {'kind', 'observed_at_utc', 'observer_role', 'criteria_results', 'attachments', 'prerequisite_receipts'},
}

def value_at(data, key):
    for name in key.split('.'):
        if not isinstance(data, dict) or name not in data:
            return None
        data = data[name]
    return data

def validate(receipt, cases, receipt_path, plans=None, seen=None):
    errors = []
    if not isinstance(receipt, dict):
        return ['receipt must be an object']
    if receipt.get('schema') != 'legacyforge-phase6a-test-receipt-v1':
        errors.append('unknown receipt schema')
    extra = set(receipt) - COMMON
    if extra:
        errors.append('unknown top-level fields')
    for section, allowed in SECTION_FIELDS.items():
        val = receipt.get(section)
        if val is not None and (not isinstance(val, dict) or set(val) - allowed):
            errors.append('invalid or unknown fields in section: ' + section)
    case = cases.get(receipt.get('test_id'))
    if case is None:
        errors.append('unknown test_id')
    if receipt.get('source_commit') != COMMIT:
        errors.append('source_commit does not match approved pin')
    status = receipt.get('status')
    if status not in STATUSES:
        errors.append('invalid status')
    if status != 'PASS':
        if not receipt.get('reason'):
            errors.append('non-PASS receipt requires a reason')
        return errors
    for key in (case or {}).get('required_pass_fields', []):
        v = value_at(receipt, key)
        if v is None or v == '' or v == [] or v == {}:
            errors.append('missing field: ' + key)
        if key.endswith('_sha256') and not (isinstance(v, str) and re.fullmatch(r'[a-fA-F0-9]{64}', v)):
            errors.append('invalid hash: ' + key)
    if str(receipt.get('test_id', '')).startswith('W'):
        if value_at(receipt, 'environment.isolation_approved') is not True:
            errors.append('Windows PASS requires approved guest isolation')
        if value_at(receipt, 'environment.isolation_type') not in ('virtual-machine', 'windows-sandbox'):
            errors.append('Windows PASS requires virtual-machine or windows-sandbox isolation')
    if str(receipt.get('test_id', '')).startswith('X'):
        if value_at(receipt, 'environment.console_model') != 'Xbox Series X':
            errors.append('Xbox PASS requires the specified Xbox Series X hardware')
    if receipt.get('test_id') == 'X02' and value_at(receipt, 'environment.debugger_attached') is not False:
        errors.append('resource measurement must occur outside a debugger')
    current_plan = None
    if receipt.get('test_id') == 'X12':
        target = receipt.get('target', {})
        if not isinstance(target, dict):
            target = {}
        matches = [p for p in plans or [] if all(target.get(k) == p.get(k) for k in ('minecraft_version', 'loader', 'loader_version', 'runtime_id'))]
        if len(matches) != 1:
            errors.append('X12 PASS must match one exact approved catalog target')
        else:
            current_plan = matches[0]
            if current_plan.get('source_implementation_status') == 'UNSUPPORTED_PROVIDER' or current_plan.get('loader_version') == 'selected':
                errors.append('approved source does not support a runnable resolved provider for this target')
            expected_major = current_plan.get('java_major_expected')
            if expected_major is not None and target.get('java_major') != expected_major:
                errors.append('Java major does not match target runtime family')
    evidence = receipt.get('evidence')
    if not isinstance(evidence, dict) or evidence.get('kind') != 'actual-test-observation':
        errors.append('PASS requires actual-test-observation evidence')
        return errors
    if not evidence.get('observed_at_utc') or not evidence.get('observer_role'):
        errors.append('PASS requires observation time and observer role')
    try:
        observed = datetime.datetime.fromisoformat(evidence.get('observed_at_utc', '').replace('Z', '+00:00'))
        if observed.utcoffset() != datetime.timedelta(0):
            errors.append('observation timestamp must include UTC timezone')
    except (ValueError, TypeError, AttributeError):
        errors.append('invalid UTC observation timestamp')
    criteria = evidence.get('criteria_results', {})
    if not isinstance(criteria, dict):
        errors.append('criteria_results must be an object')
        criteria = {}
    for criterion in (case or {}).get('criteria', []):
        if criteria.get(criterion['id']) is not True:
            errors.append('criterion has no passing observation: ' + criterion['id'])
    attachments = evidence.get('attachments')
    if not isinstance(attachments, list) or not attachments:
        errors.append('PASS requires at least one sanitized evidence attachment')
    else:
        for item in attachments:
            if not isinstance(item, dict):
                errors.append('invalid attachment entry')
                continue
            rel = item.get('path', '')
            if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
                errors.append('attachment must be a confined relative path')
                continue
            root = receipt_path.parent.resolve()
            path = (root / rel).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append('attachment missing or outside receipt directory')
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            declared = item.get('sha256')
            if not isinstance(declared, str) or declared.lower() != digest:
                errors.append('attachment hash mismatch')
    if receipt.get('test_id') == 'X12' and current_plan is not None:
        root = receipt_path.parent.resolve()
        visited = set(seen or ())
        resolved_receipt = receipt_path.resolve()
        if resolved_receipt in visited or len(visited) > 32:
            return errors + ['cyclic or excessive prerequisite receipt references']
        visited.add(resolved_receipt)
        found = set()
        prereqs = evidence.get('prerequisite_receipts', [])
        if not isinstance(prereqs, list):
            prereqs = []
            errors.append('prerequisite_receipts must be a list')
        for rel in prereqs:
            if not isinstance(rel, str) or Path(rel).is_absolute() or '..' in Path(rel).parts:
                errors.append('invalid prerequisite path')
                continue
            path = (root / rel).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                errors.append('prerequisite receipt missing or outside receipt directory')
                continue
            try:
                prior = json.loads(path.read_text(encoding='utf-8'))
                prior_id = prior.get('test_id')
                required_ids = {'X%02d' % i for i in range(1, 12)} | {'X13'}
                if prior_id not in required_ids or prior.get('status') != 'PASS':
                    errors.append('prerequisite is not a required passing gate')
                    continue
                if validate(prior, cases, path, plans, visited):
                    errors.append('prerequisite receipt does not validate')
                    continue
                if value_at(prior, 'artifacts.appx_sha256').lower() != value_at(receipt, 'artifacts.appx_sha256').lower():
                    errors.append('prerequisite package hash differs')
                    continue
                if prior_id not in ('X01', 'X02', 'X13') and any(value_at(prior, 'target.' + k) != value_at(receipt, 'target.' + k) for k in ('minecraft_version', 'loader', 'loader_version', 'runtime_id')):
                    errors.append('prerequisite target tuple differs')
                    continue
                prior_fields = set(cases[prior_id].get('required_pass_fields', []))
                current_fields = set(cases['X12'].get('required_pass_fields', []))
                shared_hashes = sorted(key for key in prior_fields & current_fields
                                       if key.startswith('artifacts.') and key.endswith('_sha256'))
                if any(str(value_at(prior, key)).lower() != str(value_at(receipt, key)).lower()
                       for key in shared_hashes):
                    errors.append('prerequisite runtime/native/manifest identity differs')
                    continue
                if 'target.java_major' in prior_fields and value_at(prior, 'target.java_major') != value_at(receipt, 'target.java_major'):
                    errors.append('prerequisite Java major differs')
                    continue
                found.add(prior_id)
            except (OSError, ValueError, TypeError, AttributeError):
                errors.append('unreadable or malformed prerequisite receipt')
        missing = ({'X%02d' % i for i in range(1, 12)} | {'X13'}) - found
        if missing:
            errors.append('missing validated prerequisite gates: ' + ','.join(sorted(missing)))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cases', type=Path)
    parser.add_argument('receipts', nargs='+', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.cases.read_text(encoding='utf-8'))
    cases = {c['test_id']: c for c in plan['cases']}
    failed = False
    for path in args.receipts:
        try:
            result = validate(json.loads(path.read_text(encoding='utf-8')), cases, path, plan.get('target_plans', []))
        except (OSError, ValueError, TypeError, KeyError):
            result = ['unreadable or malformed receipt']
        failed |= bool(result)
        print(json.dumps({'receipt': path.name, 'errors': result,
                          'meaning': 'Format and evidence references only; no runtime result independently verified.'}))
    return int(failed)

if __name__ == '__main__':
    raise SystemExit(main())
