"""Read unsigned/signed APPX data; never execute or modify either target."""
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).parent
RUN = Path(r'C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b4f-signing\20261017-143140-118313f1')
record = json.loads((RUN/'SIGNING-VERIFICATION.json').read_text(encoding='utf-8-sig'))
sha = lambda data: hashlib.sha256(data).hexdigest()
with zipfile.ZipFile(record['unsignedPath']) as original, zipfile.ZipFile(record['signedPath']) as signed:
    assert len(signed.namelist()) == len(set(signed.namelist()))
    assert signed.testzip() is None
    additions = set(signed.namelist()) - set(original.namelist())
    assert additions == {'AppxSignature.p7x', 'AppxMetadata/CodeIntegrity.cat'}
    assert not set(original.namelist()) - set(signed.namelist())
    unchanged = []
    for name in original.namelist():
        if name == '[Content_Types].xml':
            continue
        before, after = original.read(name), signed.read(name)
        assert before == after, name
        unchanged.append({'path':name,'sha256':sha(after),'byte_identical':True})
    def declarations(data):
        return {(node.tag,tuple(sorted(node.attrib.items()))) for node in ET.fromstring(data)}
    before, after = declarations(original.read('[Content_Types].xml')), declarations(signed.read('[Content_Types].xml'))
    assert before <= after
    extra = after - before
    # Only signature/catalog content-type declarations may be introduced.
    for tag, values in extra:
        item = dict(values)
        assert item in (
            {'PartName':'/AppxSignature.p7x','ContentType':'application/vnd.ms-appx.signature'},
            {'PartName':'/AppxMetadata/CodeIntegrity.cat','ContentType':'application/vnd.ms-pkiseccat'},
        )
    manifest = ET.fromstring(signed.read('AppxManifest.xml'))
    ns={'p':'http://schemas.microsoft.com/appx/manifest/foundation/windows10'}
    identity=manifest.find('p:Identity',ns).attrib
    app=manifest.find('p:Applications/p:Application',ns).attrib
    assert identity == {'Name':'AlgorHome.LegacyForge.RuntimeDiagnostics','Publisher':'CN=LegacyForgeDiagnostics','Version':'0.1.3.0','ProcessorArchitecture':'x64'}
    assert app == {'Id':'App','Executable':'RuntimeDiagnostics.exe','EntryPoint':'LegacyForgeDiagnostics.App'}
    assert not any(n.tag.rsplit('}',1)[-1] in ('Capability','DeviceCapability') for n in manifest.iter())
    inventory=json.loads(signed.read('runtime-inventory.json').decode('utf-8-sig'))
    assert not inventory['available'] and not inventory['approvedForDiagnosticPackaging']
    assert not any(inventory.get(k) for k in ('files','loadOrder','fixtureFiles'))
    inputs=json.loads(signed.read('diagnostic-inputs.json').decode('utf-8-sig'))
    assert inputs['sourceCommit']=='553c6554f40f1372b0ea09f6badbbb98e133a9ab'
    assert inputs['configuration']=='D00Only'
    for member in inputs['packageFiles']:
        assert sha(signed.read(member['path'])) == member['sha256']
    result={'verdict':'PASS','signed_sha256':sha(Path(record['signedPath']).read_bytes()),'unsigned_sha256':sha(Path(record['unsignedPath']).read_bytes()),'original_payload_and_blockmap_byte_identical':True,'unchanged_members':unchanged,'added_signing_metadata':sorted(additions),'added_content_type_declarations':[dict(v) for _,v in extra],'identity':identity,'application':app,'capabilities':[],'D00_only_inventory':True,'source_commit':inputs['sourceCommit'],'target_executed':False}
    (OUT/'PAYLOAD-VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'verdict':result['verdict'],'unchanged_members':len(unchanged),'signing_metadata':sorted(additions),'signed_sha256':result['signed_sha256']}))

