"""Read-only D00 build/ZIP audit. Never imports or executes the target program."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET


def sha(data):
    return hashlib.sha256(data).hexdigest()


def audit(build):
    package = build / 'RuntimeDiagnostics.unsigned.appx'
    stage = build / 'package'
    app = (build / 'objects/app.i').read_text(encoding='utf-8', errors='strict')
    jni = (build / 'objects/jni_smoke.i').read_text(encoding='utf-8', errors='strict')
    for token in ('void RequestJavaSmoke(', 'void ShowJavaResult(',
                  'void PollGamepad(', 'key_ = window.KeyDown(',
                  'pointer_ = window.PointerPressed(', 'PollGamepad();',
                  'RunJava21Smoke(receipt)', 'SMOKE_WORKER_STARTED',
                  'SMOKE_WATCHDOG_DEADLINE', 'Run Java 21 smoke'):
        if token in app:
            raise ValueError('S21 activation/worker survived preprocessing: ' + token)
    # The only surviving definition is the fail-closed synchronous rejection stub.
    stub = re.search(r'void RunJava21Smoke\(std::shared_ptr<Receipt> const&\)\s*\{([^{}]*)\}', jni)
    if not stub or not re.fullmatch(r'\s*winrt::throw_hresult\([\s()HRESULT]*0x80070005L[\s()]*\);\s*', stub.group(1)):
        raise ValueError('S21 rejection stub missing')
    for token in ('JNI_CreateJavaVM', 'JNI_GetDefaultJavaVMInitArgs',
                  'HMODULE loaded = LoadPackagedLibrary(', '#include <jni.h>'):
        if token in jni:
            raise ValueError('JNI implementation survived preprocessing: ' + token)
    imports = (build / 'logs/static-imports.log').read_text(encoding='utf-8-sig')
    if any(token in imports for token in ('LoadPackagedLibrary', 'JNI_CreateJavaVM', 'TerminateProcess',
                                         'CreateProcess')):
        raise ValueError('unapproved loader/process API import')
    modules = sorted(set(re.findall(r'^    ([A-Za-z0-9_.-]+\.dll)\s*$', imports, re.M)), key=str.lower)
    with zipfile.ZipFile(package) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        names = z.namelist()
        if len(set(names)) != len(names):
            raise ValueError('duplicate ZIP members')
        expected = {p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file()}
        metadata = {'AppxBlockMap.xml', '[Content_Types].xml'}
        if set(names) != expected | metadata:
            raise ValueError('unexpected payload/signature/packaging member')
        payload = []
        for name in sorted(expected):
            data = z.read(name)
            if data != (stage / name).read_bytes():
                raise ValueError('ZIP payload differs from verified stage')
            payload.append({'path': name, 'bytes': len(data), 'sha256': sha(data)})
        inventory = json.loads(z.read('runtime-inventory.json').decode('utf-8-sig'))
        if inventory.get('available') is not False or inventory.get('approvedForDiagnosticPackaging') is not False or any(inventory.get(k) for k in ('files', 'loadOrder', 'fixtureFiles')):
            raise ValueError('D00 runtime/fixture barrier mismatch')
        inputs = json.loads(z.read('diagnostic-inputs.json').decode('utf-8-sig'))
        if inputs.get('configuration') != 'D00Only':
            raise ValueError('wrong configuration')
        ns = {'p': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
        manifest = ET.fromstring(z.read('AppxManifest.xml'))
        identity = manifest.find('p:Identity', ns).attrib
        dependencies = [dict(x.attrib) for x in manifest.find('p:Dependencies', ns)]
        capabilities = [dict(x.attrib) for x in manifest.iter()
                        if x.tag.rsplit('}', 1)[-1] in ('Capability', 'DeviceCapability')]
        if capabilities:
            raise ValueError('capability added')
    return {'schema': 'legacyforge-d00-static-safety-v1', 'verdict': 'PASS',
            'priorReviewRequirement8': 'PASS_STATIC_COMPILE_TIME_DISABLED',
            'sourceCommit': inputs['sourceCommit'], 'configuration': 'D00Only',
            'targetExecuted': False, 'signed': False, 'deployed': False,
            'appxSha256': sha(package.read_bytes()), 'appxBytes': package.stat().st_size,
            'identity': identity, 'capabilities': capabilities,
            'manifestDependencies': dependencies, 'directImportModules': modules,
            'systemLoaderImports': [x for x in ('LoadLibraryExW', 'GetProcAddress', 'FreeLibrary') if x in imports],
            'payload': payload,
            'limits': ['No activation or runtime behavior tested',
                       'Direct imports are not resolved transitive dependency closure',
                       'Synchronous rejection stub inspected, never invoked']}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.build)
    a.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS: D00 static source/package audit; target not executed')
