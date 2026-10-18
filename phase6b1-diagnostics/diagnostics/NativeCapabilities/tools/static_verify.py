"""Original static build/package auditor; never loads or executes target code."""
from pathlib import Path
import argparse,hashlib,json,re,struct,zlib,zipfile,xml.etree.ElementTree as ET
from receipt_contract import read_json, self_test, DESC, SRV_DESC

def sha(data):return hashlib.sha256(data).hexdigest()
def assets(root):
    root.mkdir(parents=True,exist_ok=True)
    def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    for name,w,h in [('StoreLogo.png',50,50),('Square150x150Logo.png',150,150),('Square44x44Logo.png',44,44),('SplashScreen.png',620,300)]:
        raw=b''.join(b'\0'+bytes((22,32,48,255))*w for _ in range(h))
        (root/name).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))

def pe_imports(data):
    assert data[:2]==b'MZ';off=struct.unpack_from('<I',data,60)[0];assert data[off:off+4]==b'PE\0\0'
    machine,count=struct.unpack_from('<HH',data,off+4);size=struct.unpack_from('<H',data,off+20)[0];o=off+24
    assert machine==0x8664 and struct.unpack_from('<H',data,o)[0]==0x20b
    assert struct.unpack_from('<H',data,o+68)[0]==2 and struct.unpack_from('<H',data,o+70)[0]&0x1000
    sections=[]
    for i in range(count):
        at=o+size+40*i;vsize,va,rsize,ptr=struct.unpack_from('<IIII',data,at+8);sections.append((va,rsize,ptr))
    def pos(rva):return next(ptr+rva-va for va,rsize,ptr in sections if va<=rva<va+rsize)
    def cstr(p):return data[p:data.index(0,p)].decode('ascii')
    rva,_=struct.unpack_from('<II',data,o+112+8);result=[]
    if rva:
        p=pos(rva)
        for i in range(512):
            entry=struct.unpack_from('<IIIII',data,p+20*i)
            if not any(entry):break
            names=[];t=pos(entry[0] or entry[4])
            for j in range(8192):
                value=struct.unpack_from('<Q',data,t+8*j)[0]
                if not value:break
                names.append('ordinal:'+str(value&65535) if value&(1<<63) else cstr(pos(value)+2))
            result.append({'module':cstr(pos(entry[3])),'symbols':names})
    delay_rva,delay_size=struct.unpack_from('<II',data,o+112+13*8)
    assert delay_rva==0 and delay_size==0,'unexpected delayed code loading'
    return result

def verify(build):
    stage=build/'package';root=Path(__file__).resolve().parents[1]
    expected={'NativeCapabilities.exe','AppxManifest.xml','native-inputs.json','native-inventory.json','LICENSE.txt','profiles/D06-SRV03.json','contracts/native-receipt.schema.json','Assets/StoreLogo.png','Assets/Square150x150Logo.png','Assets/Square44x44Logo.png','Assets/SplashScreen.png'}
    assert {p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file()}==expected
    ns={'p':'http://schemas.microsoft.com/appx/manifest/foundation/windows10'};manifest=ET.parse(stage/'AppxManifest.xml').getroot()
    ident=manifest.find('p:Identity',ns).attrib
    assert ident=={'Name':'AlgorHome.LegacyForge.NativeDiagnostics','Publisher':'CN=LegacyForgeDiagnostics','Version':'0.2.5.0','ProcessorArchitecture':'x64'}
    assert manifest.find('p:Applications/p:Application',ns).attrib=={'Id':'App','Executable':'NativeCapabilities.exe','EntryPoint':'LegacyForgeNativeDiagnostics.App'}
    assert not any(n.tag.rsplit('}',1)[-1] in ('Capability','DeviceCapability') for n in manifest.iter())
    dependencies=[dict(n.attrib) for n in manifest.find('p:Dependencies',ns)]
    assert dependencies==[{'Name':'Windows.Universal','MinVersion':'10.0.17763.0','MaxVersionTested':'10.0.26100.0'},{'Name':'Microsoft.VCLibs.140.00','MinVersion':'14.0.0.0','Publisher':'CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US'}]
    inventory=json.loads((stage/'native-inventory.json').read_text())
    assert inventory['native_only'] and not inventory['java_jni_enabled'] and all(not inventory[k] for k in ('runtime_files','fixtures','extra_modules'))
    policy=json.loads((stage/'profiles/D06-SRV03.json').read_text())
    assert policy['case_id']=='D06-SRV03' and policy['feature_levels']==[45056] and policy['creation_flags']==32 and policy['deadline_ms']==10000
    assert policy['minimum_headroom_bytes']==268435456 and policy['maximum_observed_growth_bytes']==67108864 and policy['device_attempts_maximum']==1 and not policy['software_fallback'] and not policy['swapchain_or_presentation']
    inputs=json.loads((stage/'native-inputs.json').read_text(encoding='utf-8-sig'))
    assert inputs['caseId']=='D06-SRV03' and inputs['nativeOnly'] and not inputs['jniEnabled'] and inputs['sourceCommit']==inputs['compiledSourceCommit']
    assert set(inputs['compiledSources'])=={'src/app.cpp','src/report.cpp','src/probe.cpp'}
    assert inputs['definitions']==['LFN_NATIVE_ONLY=1','LFN_JNI_ENABLED=0','LFD_D00_ONLY=1','LFN_CASE_D06_SRV03=1']
    assert set(e['path'] for e in inputs['packageFiles'])==expected-{'native-inputs.json'}
    for item in inputs['packageFiles']:assert sha((stage/item['path']).read_bytes())==item['sha256']
    for item in inputs['sourceFiles']:assert sha((root/item['path']).read_bytes())==item['sha256']
    source='\n'.join((root/name).read_text() for name in inputs['compiledSources'])
    forbidden=['JNI_CreateJavaVM','JNI_GetDefaultJavaVMInitArgs','RequestJavaSmoke','RunJava21Smoke','CreateSwapChain','CreateRenderTargetView','Present(','CheckFormatSupport(','CreateTexture1D','CreateTexture3D','CreateBuffer','CreateVertexShader','CreatePixelShader','D3DCompile','Draw(','DrawIndexed(','Map(','CopyResource','ReadFromSubresource','D3D_DRIVER_TYPE_WARP','D3D_DRIVER_TYPE_REFERENCE','TerminateProcess','TerminateThread','CreateProcess']
    for token in forbidden:assert token not in source,token
    assert source.count('D3D11CreateDevice(')==1
    assert not re.search(r'\b(?:CreateBuffer|Create\w*Shader|Create(?:RenderTarget|DepthStencil|UnorderedAccess)View|CreateSwapChain\w*|Draw\w*|Dispatch|Clear\w*|Copy\w*|Map|Unmap|Present\w*)\s*\(',source)
    assert source.count('->CreateTexture2D(')==1 and 'CreateTexture2D(&requested,nullptr,texture.put())' in source
    assert source.count('->GetDesc(&returned)')==2
    assert source.count('->CreateShaderResourceView(')==1 and 'CreateShaderResourceView(texture,&requested,srv.put())' in source
    assert source.count('->GetResource(')==0
    assert source.count('->GetDevice(')==1 and 'GetDevice(returnedDevice.put())' in source
    assert source.count('->QueryInterface(__uuidof(IUnknown)')==2
    assert 'device->QueryInterface(__uuidof(IUnknown),originalIdentity.put_void())' in source
    assert 'returnedDevice->QueryInterface(__uuidof(IUnknown),owningIdentity.put_void())' in source
    assert 'if(!returnedDevice)' in source and 'if(originalHr!=S_OK)' in source and 'if(owningHr!=S_OK)' in source
    assert 'else if(!originalIdentity)' in source and 'else if(!owningIdentity)' in source
    assert 'originalIdentity.get()==owningIdentity.get()' in source
    assert 'get_device_hresult' not in source and 'BEFORE_GET_DEVICE' in source
    assert source.index('Flag(details,L"temporary_identity_references_released",true)')<source.index('Flag(details,L"returned_device_reference_released",true)')
    assert source.index('InspectOwningDevice(device,srv.get()')<source.index('Flag(details,L"srv_reference_released",true)')
    assert 'device_references_released_before_srv' in source
    assert 'if(srvHr!=S_OK)' in source and 'else if(!srv)' in source
    assert 'BEFORE_CREATE_SRV' in source and 'srv_released_before_texture' in source
    assert not re.search(r'\b(?:[A-Z]{2}Set\w*|OMSet\w*|IASet\w*|CreateShaderResourceView[0-9]+)\s*\(',source)
    for field in ['Format','ViewDimension','Texture2D.MostDetailedMip','Texture2D.MipLevels']:
        assert 'a.'+field+'==b.'+field in source
    assert 'if(value.ViewDimension==D3D11_SRV_DIMENSION_TEXTURE2D)' in source
    assert source.index('winrt::com_ptr<ID3D11ShaderResourceView> srv')<source.index('Flag(details,L"srv_reference_released",true)')
    assert source.index('CreateOneSrv(device,texture.get()')<source.index('Flag(details,L"texture_reference_released",true)')
    assert 'if(textureHr!=S_OK)' in source and 'else if(!texture)' in source and 'SameDescriptor(requested,returned)' in source
    assert 'BEFORE_CREATE_TEXTURE' in source and 'texture_reference_released' in source
    probe=(root/'src/probe.cpp').read_text()
    assert not re.search(r'\b(?:for|while)\s*\(',probe),'probe must not loop GPU operations'
    for field in ['Width','Height','MipLevels','ArraySize','Format','SampleDesc.Count','SampleDesc.Quality','Usage','BindFlags','CPUAccessFlags','MiscFlags']:
        assert 'a.'+field+'==b.'+field in probe
    assert policy['requested_descriptor']==DESC and policy['texture_attempts_maximum']==1
    assert policy['initial_data_supplied'] is False and policy['nonnull_output_pointer'] is True
    assert policy['texture_views_created'] is True and not policy['buffer_creation'] and not policy['shader_execution']
    assert policy['srv_requested_descriptor']==SRV_DESC and policy['srv_attempts_maximum']==1
    assert policy['srv_descriptor_explicit'] and policy['srv_nonnull_output_pointer'] and policy['srv_release_before_texture']
    assert policy['pipeline_binding'] is False
    assert policy['get_device_attempts_maximum']==1 and policy['get_device_nonnull_output_pointer']
    assert policy['identity_interface']=='IID_IUnknown' and policy['identity_query_attempts_maximum_per_object']==1
    assert policy['canonical_identity_equality_required'] and policy['device_refs_release_before_srv']
    schema=read_json((stage/'contracts/native-receipt.schema.json').read_bytes())
    assert schema['properties']['schema']['const']=='legacyforge-native-capability-receipt-v6'
    contract_tests=self_test(schema,stage)
    assert 'command!=lfn::Case' in source and 'ActivationKind::Launch' in source and 'started.exchange(true)' in source
    assert 'init_apartment(winrt::apartment_type::multi_threaded)' in source
    assert 'if(status==L"PASS" && Expired())' in source and 'terminal_.exchange(true)' in source
    assert 'try_lock_for' in source and 'VERIFY_BY_RETRIEVAL' in source and 'ShowAsync' in source
    assert 'if(final || !Terminal())result_.persistence=error' in source
    for name in ('app','report','probe'):
        pre=(build/f'objects/{name}.i').read_text(encoding='utf-8',errors='strict')
        for token in ('JNI_CreateJavaVM','JNI_GetDefaultJavaVMInitArgs','RequestJavaSmoke','RunJava21Smoke'):
            assert token not in pre,token
        if name=='probe':assert re.search(r'HRESULT hr\s*=\s*D3D11CreateDevice\(',pre)
    exe=(stage/'NativeCapabilities.exe').read_bytes();imports=pe_imports(exe)
    symbols={s for module in imports for s in module['symbols']}
    assert 'D3D11CreateDevice' in symbols
    assert not symbols.intersection({'LoadPackagedLibrary','TerminateProcess','TerminateThread','CreateProcessW','CreateProcessA','JNI_CreateJavaVM','JNI_GetDefaultJavaVMInitArgs'})
    modules={m['module'].lower() for m in imports}
    assert not modules.intersection({'jvm.dll','java.dll','jli.dll','d2d1.dll','dwrite.dll','dxgi.dll','opengl32.dll','d3dcompiler_47.dll','d3dcompiler_43.dll'})
    # DXGI classification uses COM vtables; no DXGI factory creation/import is required.
    package=build/'NativeCapabilities.unsigned.appx'
    payload=[]
    with zipfile.ZipFile(package) as z:
        assert len(z.namelist())==len(set(z.namelist())) and z.testzip() is None
        assert set(z.namelist())==expected|{'AppxBlockMap.xml','[Content_Types].xml'}
        for name in sorted(expected):
            b=z.read(name);assert b==(stage/name).read_bytes();payload.append({'path':name,'bytes':len(b),'sha256':sha(b)})
    return {'verdict':'PASS_STATIC_ONLY','sourceCommit':inputs['sourceCommit'],'identity':ident,'entryPoint':'LegacyForgeNativeDiagnostics.App','capabilities':[],'dependencies':dependencies,'payload':payload,'nativeImports':imports,'nativeImportClosure':'System/API-set/framework references require target loader validation; no claim of complete Xbox closure','unsignedAppxSha256':sha(package.read_bytes()),'jniExcluded':True,'oneHardwareCallSite':True,'oneTextureCreationCallSite':True,'requestedDescriptor':DESC,'oneSrvCreationCallSite':True,'requestedSrvDescriptor':SRV_DESC,'twoResourceGetDescCallSites':True,'oneGetDeviceCallSite':True,'explicitIUnknownQueryCallSites':2,'noGetDeviceHresult':True,'receiptContractTests':contract_tests,'noSwapchainOrPresentationCode':True,'executed':False,'signed':False,'ui':'Platform MessageDialog; Xbox behavior NOT EXECUTED','limits':['Source/race/failure review is static, not a runtime test','Blocked native and file calls cannot be cancelled','First terminal ownership and late-PASS guard inspected only']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--assets',type=Path);p.add_argument('--build',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    if a.assets:assets(a.assets)
    else:
        result=verify(a.build);a.output.write_text(json.dumps(result,indent=2));print('PASS: native D06-SRV03 static artifact audit; target not executed')
