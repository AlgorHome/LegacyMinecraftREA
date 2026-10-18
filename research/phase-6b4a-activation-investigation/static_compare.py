"""Read package bytes only. Does not load or execute either target image."""
import ast
import hashlib
import json
import struct
import zipfile
from pathlib import Path

OUT = Path(__file__).parent
parser_source = Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\native_audit.py').read_text()
# Reuse only the existing pure PE parser; do not execute its top-level scans.
tree = ast.parse(parser_source)
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'parse')
scope = {'struct': struct, 'hashlib': hashlib}
exec(compile(ast.Module(body=[function], type_ignores=[]), '<pure-pe-parser>', 'exec'), scope)
packages = [
    ('diagnostic', Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b3d-signing\20261017-132111-5ff08807\RuntimeDiagnostics.D00.signed.appx'), 'RuntimeDiagnostics.exe'),
    ('working-launcher-reference', Path(r'C:\Users\arinze\LegacyForge\output\LegacyForge_1.0.0.35.appx'), 'LegacyForge.exe'),
]
result = {'mode': 'STATIC_BYTES_ONLY', 'packages': [], 'limitations': [
    'Reference package hardware success is owner-reported; installed console bytes were not read.',
    'PE imports do not prove Xbox export availability, API policy acceptance, or execution.',
    'No runtime loader, console connection, signature revalidation, or target execution.',
]}
for role, path, exe in packages:
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024*1024), b''):
            digest.update(block)
    with zipfile.ZipFile(path) as archive:
        manifest = archive.read('AppxManifest.xml').decode('utf-8-sig')
        payload = archive.read(exe)
        pe = scope['parse'](Path('unused'), path.parent, role, payload, exe)
        offset = struct.unpack_from('<I', payload, 60)[0] + 24
        pe['entry_rva'] = hex(struct.unpack_from('<I', payload, offset + 16)[0])
        pe['subsystem'] = struct.unpack_from('<H', payload, offset + 68)[0]
        flags = struct.unpack_from('<H', payload, offset + 70)[0]
        pe['dll_characteristics'] = hex(flags)
        pe['appcontainer'] = bool(flags & 0x1000)
        pe['nx_compatible'] = bool(flags & 0x100)
        pe['dynamic_base'] = bool(flags & 0x40)
        (OUT / (role + '-manifest.xml')).write_text(manifest, encoding='utf-8')
        result['packages'].append({'role': role, 'path': str(path), 'sha256': digest.hexdigest(), 'manifest_sha256': hashlib.sha256(archive.read('AppxManifest.xml')).hexdigest(), 'executable': pe})
first, second = [p['executable'] for p in result['packages']]
def imports(image):
    return {(i['module'].lower(), f) for i in image['imports'] for f in i['functions']}
result['diagnostic_only_imports'] = [{'module': m, 'function': f} for m, f in sorted(imports(first) - imports(second))]
(OUT/'STATIC-COMPARISON.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({'packages': [{'role': p['role'], 'sha256': p['sha256'], 'exe_sha256':p['executable']['sha256'], 'appcontainer':p['executable']['appcontainer'], 'subsystem':p['executable']['subsystem'], 'modules':[i['module'] for i in p['executable']['imports']], 'delay_imports':p['executable']['delay_imports']} for p in result['packages']], 'diagnostic_only_imports':result['diagnostic_only_imports']}, indent=2))
