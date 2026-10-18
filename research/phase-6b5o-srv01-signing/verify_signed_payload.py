"""Read signed/unsigned APPX, block map and native-only inputs; no target loading."""
import base64,hashlib,json,struct,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
OUT=Path(__file__).parent
RUN=Path('C:\\Users\\arinze\\Desktop\\ReverseLegacyCraft\\analysis-local\\phase6b5o-signing\\20261017-190225-a21c9a46')
record=json.loads((RUN/'SIGNING-VERIFICATION.json').read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
signed_path=Path(record['signedPath'])
signed_bytes=signed_path.read_bytes()
assert sha(signed_bytes)=='da28a5c22cb27b913b2bf296155c9d9bc5745e37ff3b2af88832f7661e042724'
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
    assert identity=={'Name':'AlgorHome.LegacyForge.NativeDiagnostics','Publisher':'CN=LegacyForgeDiagnostics','Version':'0.2.3.0','ProcessorArchitecture':'x64'}
    assert application=={'Id':'App','Executable':'NativeCapabilities.exe','EntryPoint':'LegacyForgeNativeDiagnostics.App'}
    assert not any(n.tag.rsplit('}',1)[-1] in ('Capability','DeviceCapability') for n in manifest.iter())
    inputs=json.loads(signed.read('native-inputs.json').decode('utf-8-sig'))
    assert inputs['sourceCommit']==inputs['compiledSourceCommit']=='e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8'
    assert inputs['caseId']=='D06-SRV01' and inputs['nativeOnly'] is True and inputs['jniEnabled'] is False
    assert inputs['definitions']==['LFN_NATIVE_ONLY=1','LFN_JNI_ENABLED=0','LFD_D00_ONLY=1','LFN_CASE_D06_SRV01=1']
    for entry in inputs['packageFiles']:assert sha(signed.read(entry['path']))==entry['sha256']
    inventory=json.loads(signed.read('native-inventory.json'))
    assert inventory['native_only'] and not inventory['java_jni_enabled']
    assert not inventory['runtime_files'] and not inventory['fixtures'] and not inventory['extra_modules']
    # Independently compare the six member hashes with approved pre-sign build evidence.
    approved=json.loads((OUT.parent/'phase-6b5-d06-srv01/BUILD-EVIDENCE.json').read_text())
    for role,member in approved['payloadRoleMembers'].items():
        assert sha(signed.read(member))==approved['payloadRoleSha256'][role]
    schema=json.loads(signed.read('contracts/native-receipt.schema.json'))
    assert schema['properties']['schema']['const']=='legacyforge-native-capability-receipt-v4'
    assert schema['properties']['case_id']['const']=='D06-SRV01'
    policy=json.loads(signed.read('profiles/D06-SRV01.json'))
    assert policy['case_id']=='D06-SRV01' and policy['format_value']==28 and policy['requested_descriptor']==dict(width=1,height=1,mip_levels=1,array_size=1,format=28,sample_count=1,sample_quality=0,usage=0,bind_flags=8,cpu_access_flags=0,misc_flags=0)
    assert policy['texture_attempts_maximum']==policy['device_attempts_maximum']==1
    assert not policy['software_fallback'] and policy['texture_views_created'] is True and not policy['buffer_creation'] and not policy['shader_execution']
    assert policy['initial_data_supplied'] is False and policy['nonnull_output_pointer'] is True
    assert policy['srv_requested_descriptor']==dict(format=28,view_dimension=4,most_detailed_mip=0,mip_levels=1)
    assert policy['srv_attempts_maximum']==1 and policy['srv_nonnull_output_pointer'] and policy['srv_descriptor_explicit']
    assert policy['srv_release_before_texture'] and not policy['pipeline_binding']
    import sys
    sys.path.insert(0,str(Path(approved['buildDirectory']).parents[1]/'tools'))
    from static_verify import pe_imports
    assert pe_imports(signed.read('NativeCapabilities.exe'))==approved['nativeImports']
    assert set(x['path'] for x in block_results)==set(x['path'] for x in inputs['packageFiles'])|{'native-inputs.json'}
    result={'verdict':'PASS','signed_path':str(signed_path),'signed_sha256':sha(signed_bytes),'unsigned_sha256':sha(Path(record['unsignedPath']).read_bytes()),'unchanged_original_payload_and_blockmap':unchanged,'added_signing_metadata':sorted(added),'content_type_changes':newdeclarations,'blockmap_checks':block_results,'manifest_identity':identity,'application':application,'capabilities':[],'classification':'App is intended; console classification requires later owner inspection, not derivable from manifest','native_only_safety_preserved':True,'source_commit':inputs['sourceCommit'],'target_executed':False,'sixApprovedRoleHashesMatch':True,'nativeImportsMatchApprovedBuild':True,'receiptSchema':'legacyforge-native-capability-receipt-v4','onlyCase':'D06-SRV01'}
    (OUT/'SIGNED-PAYLOAD-VERIFICATION.json').write_text(json.dumps(result,indent=2))
    (OUT/'SIGNED-MANIFEST.xml').write_bytes(signed.read('AppxManifest.xml'))
    print(json.dumps({'verdict':'PASS','byte_identical_original_members':len(unchanged),'blockmap_files_checked':len(block_results),'signed_sha256':result['signed_sha256']}))
