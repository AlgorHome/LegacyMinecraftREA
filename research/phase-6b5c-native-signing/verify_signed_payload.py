"""Read signed/unsigned APPX, block map and native-only inputs; no target loading."""
import base64,hashlib,json,struct,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
OUT=Path(__file__).parent
RUN=Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5c-signing\20261017-173712-e540416b')
record=json.loads((RUN/'SIGNING-VERIFICATION.json').read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
signed_path=Path(record['signedPath'])
signed_bytes=signed_path.read_bytes()
assert sha(signed_bytes)=='d4629d1f494f73db7dcb6290bee8c5c9f28375c8630c531e58b3ee95a6f05908'
with zipfile.ZipFile(record['unsignedPath']) as original,zipfile.ZipFile(signed_path) as signed:
    assert signed.testzip() is None and len(set(signed.namelist()))==len(signed.namelist())
    added=set(signed.namelist())-set(original.namelist())
    assert added=={'AppxSignature.p7x','AppxMetadata/CodeIntegrity.cat'}
    assert not set(original.namelist())-set(signed.namelist())
    unchanged=[]
    for name in original.namelist():
        if name=='[Content_Types].xml':continue
        before,after=original.read(name),signed.read(name)
        assert before==after,name
        unchanged.append({'path':name,'sha256':sha(after),'byte_identical':True})
    def types(data):return {(n.tag,tuple(sorted(n.attrib.items()))) for n in ET.fromstring(data)}
    oldtypes,newtypes=types(original.read('[Content_Types].xml')),types(signed.read('[Content_Types].xml'))
    assert oldtypes<=newtypes
    newdeclarations=[dict(attrs) for _,attrs in newtypes-oldtypes]
    assert len(newdeclarations)==2
    for d in newdeclarations:
        assert d in ({'PartName':'/AppxSignature.p7x','ContentType':'application/vnd.ms-appx.signature'},{'PartName':'/AppxMetadata/CodeIntegrity.cat','ContentType':'application/vnd.ms-pkiseccat'})
    blockmap=ET.fromstring(signed.read('AppxBlockMap.xml'))
    assert blockmap.attrib['HashMethod']=='http://www.w3.org/2001/04/xmlenc#sha256'
    block_results=[]
    for file in blockmap:
        name=file.attrib['Name'].replace('\\','/')
        data=signed.read(name);assert len(data)==int(file.attrib['Size'])
        blocks=[n for n in file if n.tag=='{http://schemas.microsoft.com/appx/2010/blockmap}Block']
        assert len(blocks)==(len(data)+65535)//65536
        for child in file:
            if child.tag=='{http://schemas.microsoft.com/appx/2021/blockmap}FileHash':
                assert base64.b64decode(child.attrib['Hash'])==hashlib.sha256(data).digest()
            else:assert child in blocks,'unexpected block-map extension'
        for i,block in enumerate(blocks):
            assert base64.b64decode(block.attrib['Hash'])==hashlib.sha256(data[i*65536:(i+1)*65536]).digest()
        info=signed.getinfo(name);offset=info.header_offset
        assert signed_bytes[offset:offset+4]==b'PK\x03\x04'
        name_size,extra_size=struct.unpack_from('<HH',signed_bytes,offset+26)
        assert 30+name_size+extra_size==int(file.attrib['LfhSize'])
        block_results.append({'path':name,'blocks_checked':len(blocks),'size_and_local_header_match':True})
    ns={'p':'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
    manifest=ET.fromstring(signed.read('AppxManifest.xml'))
    identity=manifest.find('p:Identity',ns).attrib
    application=manifest.find('p:Applications/p:Application',ns).attrib
    assert identity=={'Name':'AlgorHome.LegacyForge.NativeDiagnostics','Publisher':'CN=LegacyForgeDiagnostics','Version':'0.2.0.0','ProcessorArchitecture':'x64'}
    assert application=={'Id':'App','Executable':'NativeCapabilities.exe','EntryPoint':'LegacyForgeNativeDiagnostics.App'}
    assert not any(n.tag.rsplit('}',1)[-1] in ('Capability','DeviceCapability') for n in manifest.iter())
    inputs=json.loads(signed.read('native-inputs.json').decode('utf-8-sig'))
    assert inputs['sourceCommit']==inputs['compiledSourceCommit']=='a3f72874241914f6048d4ca9ec4fc0edc978625d'
    assert inputs['caseId']=='D06-HW01' and inputs['nativeOnly'] is True and inputs['jniEnabled'] is False
    assert inputs['definitions']==['LFN_NATIVE_ONLY=1','LFN_JNI_ENABLED=0','LFD_D00_ONLY=1','LFN_CASE_D06_HW01=1']
    for entry in inputs['packageFiles']:assert sha(signed.read(entry['path']))==entry['sha256']
    inventory=json.loads(signed.read('native-inventory.json'))
    assert inventory['native_only'] and not inventory['java_jni_enabled']
    assert not inventory['runtime_files'] and not inventory['fixtures'] and not inventory['extra_modules']
    assert set(x['path'] for x in block_results)==set(x['path'] for x in inputs['packageFiles'])|{'native-inputs.json'}
    result={'verdict':'PASS','signed_path':str(signed_path),'signed_sha256':sha(signed_bytes),'unsigned_sha256':sha(Path(record['unsignedPath']).read_bytes()),'unchanged_original_payload_and_blockmap':unchanged,'added_signing_metadata':sorted(added),'content_type_changes':newdeclarations,'blockmap_checks':block_results,'manifest_identity':identity,'application':application,'capabilities':[],'classification':'App is intended; console classification requires later owner inspection, not derivable from manifest','native_only_safety_preserved':True,'source_commit':inputs['sourceCommit'],'target_executed':False}
    (OUT/'SIGNED-PAYLOAD-VERIFICATION.json').write_text(json.dumps(result,indent=2))
    (OUT/'SIGNED-MANIFEST.xml').write_bytes(signed.read('AppxManifest.xml'))
    print(json.dumps({'verdict':'PASS','byte_identical_original_members':len(unchanged),'blockmap_files_checked':len(block_results),'signed_sha256':result['signed_sha256']}))
