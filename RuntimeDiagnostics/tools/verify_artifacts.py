"""Original static build/package verification; never loads a target module or JVM."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, re, struct, zlib, xml.etree.ElementTree as ET, zipfile

IDENTITY = 'AlgorHome.LegacyForge.RuntimeDiagnostics'
LOAD_ORDER = ['bin/vcruntime140.dll', 'bin/vcruntime140_1.dll', 'bin/msvcp140.dll',
              'bin/jli.dll', 'bin/server/jvm.dll', 'bin/java.dll']
def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def confined(root, name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name or name.startswith('/'):
        raise ValueError('invalid relative path')
    parts = PurePosixPath(name).parts
    if any(x in ('..', '.') for x in parts) or str(PurePosixPath(name)) != name:
        raise ValueError('noncanonical relative path')
    p = root.joinpath(*parts)
    if not p.resolve().is_relative_to(root.resolve()): raise ValueError('path escapes root')
    for q in [p, *p.parents]:
        if q == root.parent: break
        if q.is_symlink() or q.is_junction(): raise ValueError('link/reparse target rejected')
    return p
def png(path, w, h):
    def chunk(tag, data): return struct.pack('>I', len(data))+tag+data+struct.pack('>I', zlib.crc32(tag+data)&0xffffffff)
    # Original simple diagnostic cross; no existing branding or external resource.
    raw = b''.join(b'\0'+b''.join(bytes((50,190,210,255)) if abs(x-w//2)<max(2,w//12) or abs(y-h//2)<max(2,h//12) else bytes((22,32,48,255)) for x in range(w)) for y in range(h))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
def assets(root):
    root.mkdir(parents=True, exist_ok=True)
    for name,w,h in [('StoreLogo.png',50,50),('Square150x150Logo.png',150,150),('Square44x44Logo.png',44,44),('SplashScreen.png',620,300)]: png(root/name,w,h)
def runtime_check(runtime, inv):
    if inv.get('schema')!='legacyforge-runtime-inventory-v1' or inv.get('available') is not True or inv.get('approvedForDiagnosticPackaging') is not True:
        raise ValueError('runtime requires explicit approved available inventory')
    if inv.get('expectedJavaMajor')!=21 or inv.get('architecture')!='x64': raise ValueError('only exact reviewed Java21 x64 runtime admitted')
    if inv.get('loadOrder') != LOAD_ORDER: raise ValueError('unexpected runtime load order')
    names=set()
    for entry in inv.get('files',[]):
        name=entry['path']; p=confined(runtime,name)
        # Match the runtime host's deliberately narrow inventory grammar so an
        # admitted package cannot fail solely on different path normalization.
        if len(name)>512 or any(not re.fullmatch(r'[A-Za-z0-9_+.-]+', part) or part.endswith('.') for part in name.split('/')):
            raise ValueError('runtime path outside diagnostic host grammar')
        if name.casefold() in names: raise ValueError('duplicate runtime path')
        names.add(name.casefold())
        if not p.is_file() or digest(p)!=entry.get('sha256'): raise ValueError('runtime file missing/hash mismatch')
        if not entry.get('sourceId') or not entry.get('role'): raise ValueError('runtime provenance/role missing')
        lic=confined(runtime,entry.get('licensePath'))
        license_name=entry['licensePath']
        if len(license_name)>512 or any(not re.fullmatch(r'[A-Za-z0-9_+.-]+', part) or part.endswith('.') for part in license_name.split('/')):
            raise ValueError('license path outside diagnostic host grammar')
        if not lic.is_file() or digest(lic)!=entry.get('licenseSha256'): raise ValueError('runtime license missing/hash mismatch')
        if p.suffix.lower()=='.dll':
            b=p.read_bytes(); pe=struct.unpack_from('<I',b,60)[0]
            if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\0\0' or struct.unpack_from('<H',b,pe+4)[0]!=0x8664: raise ValueError('runtime DLL is not x64 PE')
    actual={p.relative_to(runtime).as_posix().casefold() for p in runtime.rglob('*') if p.is_file()}
    if actual!=names or not set(LOAD_ORDER)<= {e['path'] for e in inv['files']}: raise ValueError('runtime inventory must cover every file and required modules')
    for p in runtime.rglob('*'): confined(runtime,p.relative_to(runtime).as_posix())
    release=runtime/'release'
    if not release.is_file(): raise ValueError('runtime release identity missing')
    fields=dict(line.split('=',1) for line in release.read_text().splitlines() if '=' in line)
    if not fields.get('JAVA_VERSION','').strip('"').startswith('21.') or fields.get('OS_ARCH','').strip('"') not in ('amd64','x86_64'):
        raise ValueError('runtime release is not Java21 x64')
    return {'runtimeFiles':len(names),'runtimeStatus':'STATIC_HASH_CHECKED_NOT_EXECUTED'}
def verify(package):
    doc=ET.parse(package/'AppxManifest.xml').getroot(); ns={'p':'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
    ident=doc.find('p:Identity',ns)
    if ident.attrib.get('Name')!=IDENTITY or ident.attrib.get('Publisher')!='CN=LegacyForgeDiagnostics' or ident.attrib.get('ProcessorArchitecture')!='x64': raise ValueError('package identity mismatch')
    if any(x.tag.rsplit('}',1)[-1] in ('Capability','DeviceCapability') for x in doc.iter()): raise ValueError('baseline package must have no capabilities')
    app=doc.find('p:Applications/p:Application',ns)
    if app.attrib.get('Id')!='App' or app.attrib.get('EntryPoint')!='LegacyForgeDiagnostics.App' or app.attrib.get('Executable')!='RuntimeDiagnostics.exe': raise ValueError('entrypoint mismatch')
    if ident.attrib.get('Version')!='0.1.3.0': raise ValueError('MTA experiment version mismatch')
    exe=package/'RuntimeDiagnostics.exe'; b=exe.read_bytes(); pe=struct.unpack_from('<I',b,60)[0]
    if b[:2]!=b'MZ' or b[pe:pe+4]!=b'PE\0\0' or struct.unpack_from('<H',b,pe+4)[0]!=0x8664: raise ValueError('diagnostic executable not x64')
    if struct.unpack_from('<H',b,pe+24+68)[0]!=2 or not struct.unpack_from('<H',b,pe+24+70)[0]&0x1000: raise ValueError('diagnostic executable missing GUI/AppContainer flags')
    inputs=json.loads((package/'diagnostic-inputs.json').read_text(encoding='utf-8-sig'))
    d00=inputs.get('configuration')=='D00Only'
    if inputs.get('configuration') not in ('D00Only','Java21Smoke'): raise ValueError('explicit configuration required')
    inv=json.loads((package/'runtime-inventory.json').read_text(encoding='utf-8-sig'))
    if inv.get('schema')!='legacyforge-runtime-inventory-v1' or inv.get('expectedJavaMajor')!=21 or inv.get('architecture')!='x64': raise ValueError('runtime inventory contract mismatch')
    if not isinstance(inv.get('available'),bool): raise ValueError('runtime availability must be explicit boolean')
    expected_fixtures=set() if d00 else {'Fixtures/classes/diagnostic/JniSmoke.class'}
    if {e['path'] for e in inv.get('fixtureFiles',[])}!=expected_fixtures: raise ValueError('exact synthetic fixture inventory required')
    if not inv['available'] and (inv.get('files') or (package/'Runtime').exists()): raise ValueError('unavailable runtime must not carry runtime files')
    if d00:
        if inv.get('available') is not False or inv.get('approvedForDiagnosticPackaging') is not False or inv.get('files') or inv.get('loadOrder') or inv.get('fixtureFiles'):
            raise ValueError('D00-only forbids runtime/fixture approval or inputs')
        expected={'LICENSE.txt','RuntimeDiagnostics.exe','runtime-inventory.json','diagnostic-inputs.json','AppxManifest.xml',
                  'profiles/native-control.json','Assets/StoreLogo.png','Assets/Square150x150Logo.png',
                  'Assets/Square44x44Logo.png','Assets/SplashScreen.png'}
        if {p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()} != expected:
            raise ValueError('D00-only exact payload allowlist mismatch')
        if 'D00 ONLY' not in ET.tostring(doc,encoding='unicode'): raise ValueError('D00 manifest label missing')
        for forbidden in ('LoadPackagedLibrary','JNI_CreateJavaVM','JNI_GetDefaultJavaVMInitArgs','SMOKE_WORKER_STARTED','SMOKE_WATCHDOG_DEADLINE'):
            if forbidden.encode() in b or forbidden.encode('utf-16le') in b: raise ValueError('S21 loader/worker marker in D00 binary')
    for e in inv['fixtureFiles']:

        p=confined(package,e['path'])
        if digest(p)!=e['sha256']: raise ValueError('fixture hash mismatch')
        raw=p.read_bytes()
        if raw[:4]!=b'\xca\xfe\xba\xbe' or struct.unpack_from('>H',raw,6)[0]!=65: raise ValueError('fixture not Java21 classfile')
    result=runtime_check(package/'Runtime',inv) if inv.get('available') else {'runtimeStatus':'BLOCKED_RUNTIME_NOT_SUPPLIED'}
    inputs=json.loads((package/'diagnostic-inputs.json').read_text(encoding='utf-8-sig'))
    if inputs.get('schema')!='legacyforge-diagnostic-inputs-v1' or inputs.get('runtimeInventorySha256')!=digest(package/'runtime-inventory.json'): raise ValueError('input identity contract mismatch')
    actual={p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file() and p.name!='diagnostic-inputs.json'}
    declared=[e['path'] for e in inputs['packageFiles']]
    if len(set(declared))!=len(declared) or set(declared)!=actual: raise ValueError('package inventory coverage mismatch')
    for e in inputs['packageFiles']:
        if digest(confined(package,e['path']))!=e['sha256']: raise ValueError('package input hash mismatch')
    result.update({'configuration':inputs['configuration'],'identity':IDENTITY,'staticVerification':'PASS','targetExecuted':False,'packageFiles':len(inputs['packageFiles'])})
    return result
def main():
    p=argparse.ArgumentParser(); p.add_argument('--assets',type=Path); p.add_argument('--runtime-root',type=Path); p.add_argument('--runtime-inventory',type=Path); p.add_argument('--package',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
    if a.assets: assets(a.assets); return
    if a.runtime_root: r=runtime_check(a.runtime_root,json.loads(a.runtime_inventory.read_text(encoding='utf-8-sig')))
    elif a.package: r=verify(a.package)
    else: p.error('one operation required')
    if a.output: a.output.write_text(json.dumps(r,indent=2),encoding='utf-8')
    print(json.dumps(r))
if __name__=='__main__': main()
