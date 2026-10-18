"""Static comparison only; does not load or execute target images."""
import hashlib
import json
import struct
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft')
REPO = ROOT/'phase6b1-diagnostics'
OUT = Path(__file__).parent
BASE = REPO/'diagnostics/RuntimeDiagnostics/out/20261017-122521-8ece767b'
NEW = REPO/'diagnostics/RuntimeDiagnostics/out/20261017-140332-19d39263'
sha = lambda b: hashlib.sha256(b).hexdigest()
ns = {'p':'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
with zipfile.ZipFile(BASE/'RuntimeDiagnostics.unsigned.appx') as a, zipfile.ZipFile(NEW/'RuntimeDiagnostics.unsigned.appx') as b:
    assert set(a.namelist()) == set(b.namelist())
    differences = []
    for name in sorted(a.namelist()):
        before, after = a.read(name), b.read(name)
        if before != after:
            item = {'path':name,'before_sha256':sha(before),'after_sha256':sha(after)}
            if name.endswith('.json'):
                item['json_semantically_equal'] = json.loads(before.decode('utf-8-sig')) == json.loads(after.decode('utf-8-sig'))
            differences.append(item)
    old = ET.fromstring(a.read('AppxManifest.xml'))
    new = ET.fromstring(b.read('AppxManifest.xml'))
    assert old.find('p:Identity',ns).attrib['Version'] == '0.1.1.0'
    assert new.find('p:Identity',ns).attrib['Version'] == '0.1.2.0'
    assert old.find('p:Applications/p:Application',ns).attrib['EntryPoint'] == 'Windows.PartialTrustApplication'
    assert new.find('p:Applications/p:Application',ns).attrib['EntryPoint'] == 'LegacyForgeDiagnostics.App'
    new.find('p:Identity',ns).set('Version','0.1.1.0')
    new.find('p:Applications/p:Application',ns).set('EntryPoint','Windows.PartialTrustApplication')
    assert ET.tostring(old) == ET.tostring(new), 'additional manifest change'
    def pe(data):
        off = struct.unpack_from('<I',data,60)[0]
        count = struct.unpack_from('<H',data,off+6)[0]
        osz = struct.unpack_from('<H',data,off+20)[0]
        sections = {}
        ranges = []
        for i in range(count):
            start = off+24+osz+i*40
            name = data[start:start+8].rstrip(b'\0').decode()
            size, ptr = struct.unpack_from('<II',data,start+16)
            sections[name] = sha(data[ptr:ptr+size])
            va = struct.unpack_from('<I',data,start+12)[0]
            ranges.append((va, size, ptr))
        debug_rva, debug_size = struct.unpack_from('<II',data,off+24+112+6*8)
        stamp_offsets = [off+8]
        if debug_rva:
            debug_ptr = next(ptr+debug_rva-va for va,size,ptr in ranges if va <= debug_rva < va+size)
            stamp_offsets += [debug_ptr+i+4 for i in range(0,debug_size,28)]
        return {'timestamp':struct.unpack_from('<I',data,off+8)[0], 'sections':sections, 'timestamp_offsets':stamp_offsets}
    oldpe, newpe = pe(a.read('RuntimeDiagnostics.exe')), pe(b.read('RuntimeDiagnostics.exe'))
    changed_sections = [name for name in oldpe['sections'] if oldpe['sections'][name] != newpe['sections'].get(name)]
    before_exe, after_exe = a.read('RuntimeDiagnostics.exe'), b.read('RuntimeDiagnostics.exe')
    pe_byte_differences = [{'offset':i, 'before':x, 'after':y} for i,(x,y) in enumerate(zip(before_exe,after_exe)) if x != y]
    assert oldpe['timestamp_offsets'] == newpe['timestamp_offsets']
    allowed = {offset+j for offset in oldpe['timestamp_offsets'] for j in range(4)}
    assert len(before_exe) == len(after_exe) and all(x['offset'] in allowed for x in pe_byte_differences), 'non-timestamp executable difference'

    # The complete native source, headers and schema must remain baseline-identical.
    code = subprocess.check_output(['git','-C',str(REPO),'diff','df23adb','HEAD','--','diagnostics/RuntimeDiagnostics/src','diagnostics/RuntimeDiagnostics/include','diagnostics/RuntimeDiagnostics/contracts'])
    assert not code
    cpp = (REPO/'diagnostics/RuntimeDiagnostics/src/app.cpp').read_text()
    startup = cpp[cpp.index('int __stdcall wWinMain'):]
    assert 'init_apartment(winrt::apartment_type::single_threaded)' in startup
    audit = json.loads((NEW/'d00-safety-audit.json').read_text())
    assert audit['verdict'] == 'PASS' and not audit['capabilities']
    assert 'AppxSignature.p7x' not in b.namelist()
    result = {'verdict':'PASS_STATIC_ONLY','baseline_build':str(BASE),'experiment_build':str(NEW),'experiment_commit':subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip(),'unsigned_appx_sha256':sha((NEW/'RuntimeDiagnostics.unsigned.appx').read_bytes()),'exact_manifest_changes':{'EntryPoint':['Windows.PartialTrustApplication','LegacyForgeDiagnostics.App'],'Version':['0.1.1.0','0.1.2.0']},'all_native_source_headers_schema_unchanged':True,'entry_thread_STA_unchanged':True,'PE_identical_except_COFF_and_debug_timestamps':True,'PE_section_hashes_identical':not changed_sections,'PE_changed_sections':changed_sections,'PE_byte_differences':pe_byte_differences,'PE_lengths':[len(before_exe),len(after_exe)],'baseline_PE':oldpe,'experiment_PE':newpe,'package_member_differences':differences,'signed':False,'target_executed':False}
    (OUT/'EXPERIMENT-COMPARISON.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
