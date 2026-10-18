"""Inspect compiler/package artifacts only; never execute diagnostic code."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import struct
import zipfile

WORK = Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics')
PROJECT = WORK/'diagnostics/RuntimeDiagnostics'
OUT = max((PROJECT/'out').iterdir(), key=lambda path:path.stat().st_mtime)
sha = lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
receipt = json.loads((OUT/'build-receipt.json').read_text(encoding='utf-8-sig'))
verification = json.loads((OUT/'static-verification.json').read_text(encoding='utf-8-sig'))
errors = []
if receipt['status'] != 'BUILD_STATIC_CHECK_PASS_NOT_EXECUTED' or receipt['targetExecuted']:
    errors.append('not a successful compile/static-only receipt')
for source in receipt['sourceFiles']:
    if sha(PROJECT/source['path']) != source['sha256']:
        errors.append('source differs from compiled snapshot: '+source['path'])
if any(c['exitCode'] != 0 for c in receipt['commands']):
    errors.append('a compiler/static tool failed')
stage = OUT/'package'
exe = stage/'RuntimeDiagnostics.exe'
java = stage/'Fixtures/classes/diagnostic/JniSmoke.class'
appx = OUT/'RuntimeDiagnostics.unsigned.appx'
blob = exe.read_bytes()
pe = struct.unpack_from('<I',blob,60)[0]
machine = struct.unpack_from('<H',blob,pe+4)[0]
dll_flags = struct.unpack_from('<H',blob,pe+24+70)[0]
if machine != 0x8664 or not dll_flags & 0x1000:
    errors.append('not an x64 AppContainer image')
major = struct.unpack_from('>H',java.read_bytes(),6)[0]
if major != 65:
    errors.append('fixture not Java21 bytecode')
with zipfile.ZipFile(appx) as archive:
    if archive.testzip() is not None:
        errors.append('APPX CRC error')
    names = archive.namelist()
    if any(n.replace('\\','/').startswith('Runtime/') for n in names):
        errors.append('unexpected native runtime bundled')
    if 'AppxSignature.p7x' in names:
        errors.append('unexpected signing action')
    for path in stage.rglob('*'):
        if path.is_file():
            rel = path.relative_to(stage).as_posix()
            if archive.read(rel) != path.read_bytes():
                errors.append('APPX stage mismatch: '+rel)
if verification.get('runtimeStatus') != 'BLOCKED_RUNTIME_NOT_SUPPLIED':
    errors.append('unexpected runtime availability claim')
warnings = []
for path in (OUT/'logs').glob('*.log'):
    for line in path.read_text(encoding='utf-8-sig',errors='replace').splitlines():
        if re.search(r'warning (C\d+|LNK\d+)',line):
            warnings.append(path.name)
result = {
    'schema':'legacyforge-phase6b1-compilation-evidence-v1',
    'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'baseline':receipt['baseline'],
    'branch':'research/phase6b1-runtime-diagnostics',
    'local_build_id':receipt['buildId'],
    'compilation':'PASS',
    'source_inputs_match_current_files':not any('source differs' in x for x in errors),
    'compiler_and_static_commands':[{'role':c['role'],'exitCode':c['exitCode']} for c in receipt['commands']],
    'tools':[{'role':t['role'],'fileVersion':t.get('fileVersion'),'sha256':t['sha256']} for t in receipt['tools']],
    'source_files':receipt['sourceFiles'],
    'license_files':receipt['licenseFiles'],
    'native_executable':{'architecture':'x64','appcontainer_flag':bool(dll_flags&0x1000),'sha256':sha(exe),'bytes':exe.stat().st_size},
    'java_fixture':{'classfile_major':major,'sha256':sha(java),'bytes':java.stat().st_size},
    'unsigned_appx':{'sha256':sha(appx),'bytes':appx.stat().st_size,'crc_and_staged_contents_match':True,'signed':False},
    'static_verification':verification,
    'warning_logs':warnings,
    'execution':{'D00':'NOT_EXECUTED_APPROVAL_REQUIRED','S21':'BLOCKED_APPROVED_RUNTIME_NOT_SUPPLIED','signing':'BLOCKED_SIGNING_INPUT_NOT_SUPPLIED','deployment':'NOT_AUTHORIZED_NOT_PERFORMED','target_binaries_executed':0},
    'errors':errors,
}
if errors:
    print(json.dumps(result,indent=2));raise SystemExit(1)
(PROJECT/'docs/COMPILATION-RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('compilation','source_inputs_match_current_files','native_executable','java_fixture','unsigned_appx','warning_logs','execution','errors')},indent=2))
