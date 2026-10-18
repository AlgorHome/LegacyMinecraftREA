"""Original offline SRV02 receipt/schema oracle; never runs native target code.
Synthetic fixtures are contract tests only, not console observations.
"""
import copy,datetime,hashlib,json,re,uuid
DESC=dict(width=1,height=1,mip_levels=1,array_size=1,format=28,sample_count=1,
          sample_quality=0,usage=0,bind_flags=8,cpu_access_flags=0,misc_flags=0)
SRV_DESC=dict(format=28,view_dimension=4,most_detailed_mip=0,mip_levels=1)

def read_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, ('duplicate key', key)
            result[key] = value
        return result
    return json.loads(data.decode('utf-8-sig'), object_pairs_hook=unique)

def structure(value, schema, root=None):
    root = schema if root is None else root
    keywords = {'$schema', '$id', '$comment', '$defs', '$ref', 'title', 'description',
                'type', 'const', 'enum', 'properties', 'additionalProperties',
                'required', 'minimum', 'maximum', 'format', 'pattern'}
    assert not set(schema) - keywords, 'unsupported schema keyword'
    if '$ref' in schema:
        assert schema['$ref'].startswith('#/$defs/')
        structure(value, root['$defs'][schema['$ref'].split('/')[-1]], root)
    if 'type' in schema:
        assert type(value) is {'object': dict, 'string': str, 'integer': int,
                              'boolean': bool}[schema['type']], 'type'
    if 'const' in schema:
        assert type(value) is type(schema['const']) and value == schema['const'], 'const'
    if 'enum' in schema:
        assert value in schema['enum'], 'enum'
    if 'pattern' in schema:
        assert re.search(schema['pattern'], value), 'pattern'
    if 'minimum' in schema:
        assert value >= schema['minimum'], 'minimum'
    if 'maximum' in schema:
        assert value <= schema['maximum'], 'maximum'
    if schema.get('format') == 'uuid':
        assert re.fullmatch(r'[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}', value)
        uuid.UUID(value)
    if schema.get('format') == 'date-time':
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', value)
        assert datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).tzinfo
    if isinstance(value, dict):
        assert set(schema.get('required', [])) <= set(value), 'required'
        for key, item in value.items():
            if key in schema.get('properties', {}):
                structure(item, schema['properties'][key], root)
            else:
                assert schema.get('additionalProperties', True), ('unknown field', key)

def validate(receipt,schema):
    structure(receipt,schema)
    assert receipt['run_id'].lower()!=receipt['process_instance_id'].lower()
    d=receipt['details']
    for stem in ['creation','texture','srv','original_device_identity_query','returned_device_identity_query']:
        if stem+'_hresult' in d:
            value=int(d[stem+'_hresult'],16)
            assert d[stem+'_hresult_signed']==(value if value<2**31 else value-2**32)
    if 'requested_descriptor' in d:assert d['requested_descriptor']==DESC
    if 'texture_hresult' in d:assert d.get('texture_attempted') is True
    if not d.get('texture_attempted',False):
        assert not {'texture_hresult','texture_hresult_signed','texture_returned','returned_descriptor','descriptors_match'}&set(d)
    if d.get('get_desc_called',False):
        assert d['texture_hresult']=='0x00000000' and d['texture_returned'] is True
        assert d['descriptors_match']==(d['requested_descriptor']==d['returned_descriptor'])
    else:
        assert not {'returned_descriptor','descriptors_match'}&set(d)
    if 'srv_requested_descriptor' in d:assert d['srv_requested_descriptor']==SRV_DESC
    if d.get('srv_attempted',False):
        assert d['texture_hresult']=='0x00000000' and d['texture_returned'] is True
        assert d['get_desc_called'] and d['descriptors_match'] and d['returned_descriptor']==DESC
    else:
        assert not {'srv_hresult','srv_hresult_signed','srv_returned','srv_returned_descriptor','srv_descriptors_match'}&set(d)
    if 'srv_hresult' in d:assert d.get('srv_attempted') is True
    if d.get('srv_get_desc_called',False):
        assert d['srv_hresult']=='0x00000000' and d['srv_returned'] is True
        returned=d['srv_returned_descriptor']
        if returned['view_dimension']==4:
            assert set(returned)==set(SRV_DESC),'all four Texture2D view fields required'
        else:
            assert set(returned)=={'format','view_dimension'},'inactive union must not be read'
        assert d['srv_descriptors_match']==(d['srv_requested_descriptor']==returned)
    else:
        assert not {'srv_returned_descriptor','srv_descriptors_match'}&set(d)
    if d.get('get_device_called',False):
        assert d['srv_hresult']=='0x00000000' and d['srv_returned'] is True
        assert d['srv_get_desc_called'] and d['srv_descriptors_match'] and d['srv_returned_descriptor']==SRV_DESC
    else:
        assert 'owning_device_returned' not in d
    for stem in ['original_device','returned_device']:
        key=stem+'_identity_query'
        if d.get(key+'_attempted',False):
            assert d['get_device_called'] and d['owning_device_returned'] is True
            assert key+'_hresult' in d and stem+'_identity_returned' in d
        else:
            assert not {key+'_hresult',key+'_hresult_signed',stem+'_identity_returned'}&set(d)
    if d.get('returned_device_identity_query_attempted',False):
        assert d['original_device_identity_query_hresult']=='0x00000000' and d['original_device_identity_returned'] is True
    if d.get('identity_comparison_performed',False):
        assert d['identity_interface']=='IID_IUnknown'
        assert d['original_device_identity_query_hresult']==d['returned_device_identity_query_hresult']=='0x00000000'
        assert d['original_device_identity_returned'] is True and d['returned_device_identity_returned'] is True
        assert 'canonical_identity_equal' in d
    else:
        assert 'canonical_identity_equal' not in d,'no comparison of null/invalid identity outputs'
    if receipt['status']=='NOT EXECUTED':
        assert receipt['terminal'] is False and not d.get('texture_attempted',False)
        assert 'creation_hresult' not in d and not d.get('srv_attempted',False)
    if receipt['status']=='PASS':
        assert receipt['terminal'] is True and receipt['stage']=='FINAL'
        assert receipt['reason']=='SRV_OWNING_DEVICE_IDENTITY_CONFIRMED'
        assert d['texture_attempted'] and d['texture_hresult']=='0x00000000'
        assert d['texture_returned'] and d['get_desc_called'] and d['descriptors_match']
        assert d['requested_descriptor']==d['returned_descriptor']==DESC
        assert d['initial_data_supplied'] is False and d['nonnull_output_pointer'] is True
        assert d['format_name']=='DXGI_FORMAT_R8G8B8A8_UNORM' and d['format_value']==28
        assert d['creation_hresult']=='0x00000000'
        assert d['device_returned'] and d['context_returned']
        assert d['texture_reference_released'] and d['test_resources_released']
        assert d['srv_attempted'] and d['srv_hresult']=='0x00000000' and d['srv_returned']
        assert d['srv_get_desc_called'] and d['srv_descriptors_match']
        assert d['srv_requested_descriptor']==d['srv_returned_descriptor']==SRV_DESC
        assert d['srv_nonnull_output_pointer'] is True
        assert d['srv_reference_released'] and d['srv_released_before_texture']
        assert d['get_device_called'] and d['get_device_nonnull_output_pointer'] is True
        assert d['owning_device_returned'] and d['identity_comparison_performed'] and d['canonical_identity_equal']
        assert d['original_device_identity_query_attempted'] and d['returned_device_identity_query_attempted']
        assert d['temporary_identity_references_released'] and d['returned_device_reference_released'] and d['device_references_released_before_srv']
        assert d['selected_feature_level']==d['requested_feature_level']==45056
        assert d['requested_driver_type']=='HARDWARE' and d['requested_driver_type_value']==1
        assert d['creation_flags']==32 and d['software_fallback_allowed'] is False
        assert d['render_or_present_tested'] is False
        assert d['get_adapter_hresult']==d['get_desc_hresult']=='0x00000000'
        assert d['adapter_software_flag'] is False and not d['adapter_flags']&2
        assert receipt['sequence']==6 and receipt['last_durable_checkpoint_stage']=='BEFORE_GET_DEVICE'
        assert receipt['elapsed_monotonic_ms']<receipt['deadline_ms']
        before,after=d['memory_before'],d['memory_after_release']
        assert before['available'] and after['available']
        assert before['limit_bytes']-before['usage_bytes']>=268435456
        assert after['usage_bytes']-before['usage_bytes']<=67108864

def bind_payload(receipt,stage):
    roles={'executable_sha256':'NativeCapabilities.exe','manifest_sha256':'AppxManifest.xml',
           'build_inputs_sha256':'native-inputs.json','policy_sha256':'profiles/D06-SRV03.json',
           'schema_sha256':'contracts/native-receipt.schema.json','inventory_sha256':'native-inventory.json'}
    assert receipt['payload_hashes']=={k:hashlib.sha256((stage/v).read_bytes()).hexdigest() for k,v in roles.items()}
    inputs=read_json((stage/'native-inputs.json').read_bytes())
    assert receipt['source_commit']==inputs['sourceCommit']==inputs['compiledSourceCommit']
    assert receipt['build_id']==inputs['buildId']

def self_test(schema,stage):
    r={k:s['const'] for k,s in schema['properties'].items() if 'const' in s}
    r.update(source_commit='0'*40,build_id='20261017-000000-00000000',
             run_id='11111111-1111-4111-8111-111111111111',process_instance_id='22222222-2222-4222-8222-222222222222',
             status='PASS',reason='SRV_OWNING_DEVICE_IDENTITY_CONFIRMED',stage='FINAL',terminal=True,
             sequence=6,elapsed_monotonic_ms=100,observed_at_utc='2026-10-17T00:00:00Z',
             last_durable_checkpoint_stage='BEFORE_GET_DEVICE',
             payload_hashes={k:'0'*64 for k in schema['properties']['payload_hashes']['required']})
    d=dict(format_name='DXGI_FORMAT_R8G8B8A8_UNORM',format_value=28,texture_attempted=True,
           texture_hresult='0x00000000',texture_hresult_signed=0,texture_returned=True,
           get_desc_called=True,descriptors_match=True,requested_descriptor=DESC.copy(),returned_descriptor=DESC.copy(),
           initial_data_supplied=False,nonnull_output_pointer=True,creation_hresult='0x00000000',creation_hresult_signed=0,
           device_returned=True,context_returned=True,texture_reference_released=True,test_resources_released=True,
           srv_attempted=True,srv_hresult='0x00000000',srv_hresult_signed=0,srv_returned=True,
           srv_get_desc_called=True,srv_descriptors_match=True,srv_requested_descriptor=SRV_DESC.copy(),
           srv_returned_descriptor=SRV_DESC.copy(),srv_reference_released=True,srv_released_before_texture=True,srv_nonnull_output_pointer=True,
           selected_feature_level=45056,requested_feature_level=45056,requested_driver_type='HARDWARE',requested_driver_type_value=1,
           creation_flags=32,software_fallback_allowed=False,render_or_present_tested=False,
           get_adapter_hresult='0x00000000',get_desc_hresult='0x00000000',adapter_flags=0,adapter_software_flag=False,
           memory_before=dict(available=True,usage_bytes=1000000,limit_bytes=1073741824),
           memory_after_release=dict(available=True,usage_bytes=2000000,limit_bytes=1073741824))
    d.update(identity_interface='IID_IUnknown',get_device_nonnull_output_pointer=True,get_device_called=True,
             owning_device_returned=True,original_device_identity_query_attempted=True,returned_device_identity_query_attempted=True,
             original_device_identity_query_hresult='0x00000000',original_device_identity_query_hresult_signed=0,original_device_identity_returned=True,
             returned_device_identity_query_hresult='0x00000000',returned_device_identity_query_hresult_signed=0,returned_device_identity_returned=True,
             identity_comparison_performed=True,canonical_identity_equal=True,temporary_identity_references_released=True,
             returned_device_reference_released=True,device_references_released_before_srv=True)
    r['details']=d;validate(r,schema);valid=['PASS canonical nonnull IUnknown identity']
    def reset_identity(data):
        for key in list(data):
            if key.startswith(('get_device','owning_device','device_references','original_device_identity','returned_device_identity','identity_','canonical_','temporary_identity','returned_device')):data.pop(key)
        data.update(get_device_called=False,original_device_identity_query_attempted=False,returned_device_identity_query_attempted=False,identity_comparison_performed=False)

    def no_srv_desc(status,reason,hr,signed,returned):
        v=copy.deepcopy(r);v.update(status=status,reason=reason)
        reset_identity(v['details'])
        v['details'].update(srv_hresult=hr,srv_hresult_signed=signed,srv_returned=returned,srv_get_desc_called=False)
        for k in ['srv_returned_descriptor','srv_descriptors_match']:v['details'].pop(k)
        validate(v,schema);valid.append(reason);return v
    sf=no_srv_desc('FAILED','SRV_ALLOCATION_NOT_CONFIRMED','0x00000001',1,True)
    no_srv_desc('FAILED','SRV_OUTPUT_MISSING','0x00000000',0,False)
    no_srv_desc('BLOCKED','SRV_API_OR_POLICY_UNAVAILABLE','0x80070005',-2147024891,False)
    no_srv_desc('FAILED','SRV_CREATION_FAILED','0x80004005',-2147467259,False)
    mismatch=copy.deepcopy(r);mismatch.update(status='FAILED',reason='SRV_DESCRIPTOR_MISMATCH')
    reset_identity(mismatch['details'])
    mismatch['details']['srv_returned_descriptor']['mip_levels']=2;mismatch['details']['srv_descriptors_match']=False
    validate(mismatch,schema);valid.append('FAILED active SRV mismatch')
    dimension=copy.deepcopy(mismatch);dimension['details']['srv_returned_descriptor']=dict(format=28,view_dimension=3)
    validate(dimension,schema);valid.append('FAILED wrong dimension, no inactive union values')
    texture_fail=copy.deepcopy(r);texture_fail.update(status='FAILED',reason='TEXTURE_OUTPUT_MISSING')
    reset_identity(texture_fail['details'])
    for k in list(texture_fail['details']):
        if k.startswith('srv_'):texture_fail['details'].pop(k)
    texture_fail['details'].update(srv_attempted=False,srv_get_desc_called=False,texture_returned=False,get_desc_called=False)
    for k in ['returned_descriptor','descriptors_match']:texture_fail['details'].pop(k)
    validate(texture_fail,schema);valid.append('FAILED prerequisite texture, no SRV attempt')
    timeout=copy.deepcopy(r);timeout.update(status='INCONCLUSIVE',reason='NATIVE_CALL_DEADLINE',details={})
    validate(timeout,schema);valid.append('INCONCLUSIVE no returned driver data')
    not_run=copy.deepcopy(r);not_run.update(status='NOT EXECUTED',reason='NOT_EXECUTED',terminal=False,stage='STARTED',sequence=1,last_durable_checkpoint_stage='',details={})
    validate(not_run,schema);valid.append('NOT EXECUTED')
    checkpoint=copy.deepcopy(not_run);checkpoint.update(status='RUNNING',reason='STARTED')
    validate(checkpoint,schema);valid.append('RUNNING')
    missing=copy.deepcopy(r);reset_identity(missing['details'])
    missing.update(status='FAILED',reason='OWNING_DEVICE_OUTPUT_MISSING')
    missing['details'].update(get_device_called=True,owning_device_returned=False,temporary_identity_references_released=True,returned_device_reference_released=True,device_references_released_before_srv=True)
    validate(missing,schema);valid.append('FAILED GetDevice null, no invented HRESULT')
    qi_fail=copy.deepcopy(r);qi_fail.update(status='FAILED',reason='ORIGINAL_DEVICE_IDENTITY_QUERY_NOT_S_OK')
    qi_fail['details'].update(original_device_identity_query_hresult='0x80004002',original_device_identity_query_hresult_signed=-2147467262,original_device_identity_returned=False,returned_device_identity_query_attempted=False,identity_comparison_performed=False)
    for key in ['returned_device_identity_query_hresult','returned_device_identity_query_hresult_signed','returned_device_identity_returned','canonical_identity_equal']:qi_fail['details'].pop(key)
    validate(qi_fail,schema);valid.append('FAILED first QI, no second query/comparison')
    second_fail=copy.deepcopy(r);second_fail.update(status='FAILED',reason='RETURNED_DEVICE_IDENTITY_QUERY_NOT_S_OK')
    second_fail['details'].update(returned_device_identity_query_hresult='0x80004002',returned_device_identity_query_hresult_signed=-2147467262,returned_device_identity_returned=False,identity_comparison_performed=False);second_fail['details'].pop('canonical_identity_equal')
    validate(second_fail,schema);valid.append('FAILED second QI, no comparison')
    unequal=copy.deepcopy(r);unequal.update(status='FAILED',reason='OWNING_DEVICE_IDENTITY_MISMATCH');unequal['details']['canonical_identity_equal']=False
    validate(unequal,schema);valid.append('FAILED distinct canonical identities')
    null_first=copy.deepcopy(qi_fail);null_first.update(reason='ORIGINAL_DEVICE_IDENTITY_OUTPUT_MISSING')
    null_first['details'].update(original_device_identity_query_hresult='0x00000000',original_device_identity_query_hresult_signed=0)
    validate(null_first,schema);valid.append('FAILED first QI S_OK null output')
    null_second=copy.deepcopy(second_fail);null_second.update(reason='RETURNED_DEVICE_IDENTITY_OUTPUT_MISSING')
    null_second['details'].update(returned_device_identity_query_hresult='0x00000000',returned_device_identity_query_hresult_signed=0)
    validate(null_second,schema);valid.append('FAILED second QI S_OK null output')
    rejected=[]
    def bad(name,v):
        try:validate(v,schema)
        except (AssertionError,KeyError,ValueError):rejected.append(name);return
        raise AssertionError('accepted malformed fixture: '+name)
    for field in DESC:
        v=copy.deepcopy(r);v['details']['returned_descriptor'][field]+=1;bad('texture field '+field,v)
    for field in SRV_DESC:
        v=copy.deepcopy(r);v['details']['srv_returned_descriptor'][field]+=1;bad('SRV field '+field,v)
    for field,value in [('srv_attempted',False),('srv_returned',False),('srv_get_desc_called',False),
                        ('srv_reference_released',False),('srv_released_before_texture',False),
                        ('srv_nonnull_output_pointer',False),('texture_reference_released',False),
                        ('test_resources_released',False),('adapter_software_flag',True),('texture_returned',False)]:
        v=copy.deepcopy(r);v['details'][field]=value;bad(field,v)
    v=copy.deepcopy(sf);v.update(status='PASS',reason=r['reason']);bad('S_FALSE is not SRV allocation PASS',v)
    v=copy.deepcopy(r);v['details']['srv_hresult']='0x80004005';bad('failed SRV HRESULT cannot have a valid descriptor',v)
    for field,value in [('case_id','D06-RES01a'),('package_version','0.2.2.0'),('elapsed_monotonic_ms',10000),
                        ('terminal',False),('process_instance_id',r['run_id']),('sequence',4)]:
        v=copy.deepcopy(r);v[field]=value;bad(field,v)
    v=copy.deepcopy(r);v['details']['srv_returned_descriptor'].pop('most_detailed_mip');bad('missing active SRV field',v)
    v=copy.deepcopy(dimension);v['details']['srv_returned_descriptor']['mip_levels']=1;bad('inactive union field retained',v)
    for key,value in [('get_device_called',False),('owning_device_returned',False),('get_device_nonnull_output_pointer',False),
                      ('original_device_identity_returned',False),('returned_device_identity_returned',False),('identity_comparison_performed',False),
                      ('canonical_identity_equal',False),('temporary_identity_references_released',False),
                      ('returned_device_reference_released',False),('device_references_released_before_srv',False)]:
        v=copy.deepcopy(r);v['details'][key]=value;bad(key,v)
    v=copy.deepcopy(qi_fail);v['details']['canonical_identity_equal']=True;bad('failed QI cannot compare two null identities',v)
    v=copy.deepcopy(r);v['details']['returned_device_identity_query_hresult']='0x00000001';v['details']['returned_device_identity_query_hresult_signed']=1;bad('QI S_FALSE is not canonical identity success',v)
    v=copy.deepcopy(r);v['details']['get_device_hresult']='0x00000000';bad('invented GetDevice HRESULT',v)
    v=copy.deepcopy(r);v['details']['original_device_identity_address']=123456;bad('raw pointer address prohibited',v)
    v=copy.deepcopy(r);v['case_id']='D06-SRV01';bad('old SRV01 case',v)
    v=copy.deepcopy(r);v['package_version']='0.2.3.0';bad('old SRV01 version',v)
    for field,value in [('schema','legacyforge-native-capability-receipt-v5'),('case_id','D06-SRV02'),('package_version','0.2.4.0')]:
        v=copy.deepcopy(r);v[field]=value;bad('stale SRV02 '+field,v)
    for key in ['get_device_hresult','get_resource_hresult','original_device_identity_address','returned_device_identity_address']:
        v=copy.deepcopy(r);v['details'][key]='0x00000000';bad('forbidden field '+key,v)
    for stem in ['original_device','returned_device']:
        v=copy.deepcopy(r);v['details'][stem+'_identity_query_hresult']='0x00000001';v['details'][stem+'_identity_query_hresult_signed']=1;bad(stem+' QI S_FALSE',v)
    v=copy.deepcopy(r);v['details']['memory_before']['limit_bytes']=2000000;bad('headroom below minimum',v)
    v=copy.deepcopy(r);v['details']['memory_after_release']['usage_bytes']=100000000;bad('observed memory growth over limit',v)
    v=copy.deepcopy(r);v['last_durable_checkpoint_stage']='BEFORE_GET_RESOURCE';bad('stale predecessor checkpoint',v)
    try:bind_payload(r,stage)
    except AssertionError:rejected.append('forged payload binding')
    else:raise AssertionError('accepted forged payload')
    try:read_json(b'{"status":"PASS","status":"FAILED"}')
    except AssertionError:rejected.append('duplicate JSON keys')
    else:raise AssertionError('accepted duplicate JSON')
    return dict(syntheticValidCases=len(valid),validCases=valid,syntheticRejectedCases=rejected,
                executedTarget=False,scope='offline structure/semantic oracle; no native API execution')
