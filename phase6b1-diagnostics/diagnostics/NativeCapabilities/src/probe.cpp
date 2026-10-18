// SPDX-License-Identifier: Apache-2.0
#include "native.h"
#include <d3d11.h>
#include <dxgi1_2.h>

namespace lfn {
namespace {
static_assert(D3D11_SRV_DIMENSION_TEXTURE2D==4 && DXGI_FORMAT_R8G8B8A8_UNORM==28);
static_assert(D3D11_BIND_SHADER_RESOURCE==8 && D3D11_USAGE_DEFAULT==0);
D3D11_TEXTURE2D_DESC RequestedDescriptor() {
    D3D11_TEXTURE2D_DESC value{};
    value.Width=1;value.Height=1;value.MipLevels=1;value.ArraySize=1;
    value.Format=DXGI_FORMAT_R8G8B8A8_UNORM;
    value.SampleDesc.Count=1;value.SampleDesc.Quality=0;
    value.Usage=D3D11_USAGE_DEFAULT;value.BindFlags=D3D11_BIND_SHADER_RESOURCE;
    value.CPUAccessFlags=0;value.MiscFlags=0;
    return value;
}
Json Descriptor(D3D11_TEXTURE2D_DESC const& value) {
    Json result;
    Number(result,L"width",value.Width);Number(result,L"height",value.Height);
    Number(result,L"mip_levels",value.MipLevels);Number(result,L"array_size",value.ArraySize);
    Number(result,L"format",static_cast<unsigned>(value.Format));
    Number(result,L"sample_count",value.SampleDesc.Count);Number(result,L"sample_quality",value.SampleDesc.Quality);
    Number(result,L"usage",static_cast<unsigned>(value.Usage));Number(result,L"bind_flags",value.BindFlags);
    Number(result,L"cpu_access_flags",value.CPUAccessFlags);Number(result,L"misc_flags",value.MiscFlags);
    return result;
}
bool SameDescriptor(D3D11_TEXTURE2D_DESC const& a,D3D11_TEXTURE2D_DESC const& b) {
    // Compare every defined field, never padding bytes.
    return a.Width==b.Width && a.Height==b.Height && a.MipLevels==b.MipLevels && a.ArraySize==b.ArraySize &&
        a.Format==b.Format && a.SampleDesc.Count==b.SampleDesc.Count && a.SampleDesc.Quality==b.SampleDesc.Quality &&
        a.Usage==b.Usage && a.BindFlags==b.BindFlags && a.CPUAccessFlags==b.CPUAccessFlags && a.MiscFlags==b.MiscFlags;
}
D3D11_SHADER_RESOURCE_VIEW_DESC RequestedSrvDescriptor() {
    D3D11_SHADER_RESOURCE_VIEW_DESC value{};
    value.Format=DXGI_FORMAT_R8G8B8A8_UNORM;
    value.ViewDimension=D3D11_SRV_DIMENSION_TEXTURE2D;
    value.Texture2D.MostDetailedMip=0;value.Texture2D.MipLevels=1;
    return value;
}
Json SrvDescriptor(D3D11_SHADER_RESOURCE_VIEW_DESC const& value) {
    Json result;
    Number(result,L"format",static_cast<unsigned>(value.Format));
    Number(result,L"view_dimension",static_cast<unsigned>(value.ViewDimension));
    // Never inspect Texture2D union members for a different returned dimension.
    if(value.ViewDimension==D3D11_SRV_DIMENSION_TEXTURE2D) {
        Number(result,L"most_detailed_mip",value.Texture2D.MostDetailedMip);
        Number(result,L"mip_levels",value.Texture2D.MipLevels);
    }
    return result;
}
bool SameSrvDescriptor(D3D11_SHADER_RESOURCE_VIEW_DESC const& a,D3D11_SHADER_RESOURCE_VIEW_DESC const& b) {
    return a.Format==b.Format && a.ViewDimension==b.ViewDimension &&
        b.ViewDimension==D3D11_SRV_DIMENSION_TEXTURE2D &&
        a.Texture2D.MostDetailedMip==b.Texture2D.MostDetailedMip && a.Texture2D.MipLevels==b.Texture2D.MipLevels;
}
void InspectOwningDevice(ID3D11Device* device,ID3D11ShaderResourceView* srv,
    std::shared_ptr<Receipt> const& receipt,Json const& details,std::wstring& status,std::wstring& reason) {
    if(!receipt->Checkpoint(L"BEFORE_GET_DEVICE",details)){status=L"BLOCKED";reason=L"DEVICE_IDENTITY_CHECKPOINT_FAILED";return;}
    if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"DEADLINE_BEFORE_DEVICE_IDENTITY_CALL";return;}
    {
        winrt::com_ptr<ID3D11Device> returnedDevice;
        {
            winrt::com_ptr<IUnknown> originalIdentity,owningIdentity;
            Flag(details,L"get_device_called",true);
            srv->GetDevice(returnedDevice.put()); // void; acquires one owned device reference.
            Flag(details,L"owning_device_returned",bool(returnedDevice));
            if(!returnedDevice){status=L"FAILED";reason=L"OWNING_DEVICE_OUTPUT_MISSING";}
            else if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"DEVICE_IDENTITY_CALL_RETURNED_LATE";}
            else {
                // __uuidof(IUnknown) is IID_IUnknown, with no extra GUID library dependency.
                Flag(details,L"original_device_identity_query_attempted",true);
                HRESULT originalHr=device->QueryInterface(__uuidof(IUnknown),originalIdentity.put_void());
                Text(details,L"original_device_identity_query_hresult",Hex(originalHr));Number(details,L"original_device_identity_query_hresult_signed",originalHr);
                Flag(details,L"original_device_identity_returned",bool(originalIdentity));
                if(originalHr!=S_OK){status=L"FAILED";reason=L"ORIGINAL_DEVICE_IDENTITY_QUERY_NOT_S_OK";}
                else if(!originalIdentity){status=L"FAILED";reason=L"ORIGINAL_DEVICE_IDENTITY_OUTPUT_MISSING";}
                else if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"ORIGINAL_DEVICE_IDENTITY_QUERY_RETURNED_LATE";}
                else {
                    Flag(details,L"returned_device_identity_query_attempted",true);
                    HRESULT owningHr=returnedDevice->QueryInterface(__uuidof(IUnknown),owningIdentity.put_void());
                    Text(details,L"returned_device_identity_query_hresult",Hex(owningHr));Number(details,L"returned_device_identity_query_hresult_signed",owningHr);
                    Flag(details,L"returned_device_identity_returned",bool(owningIdentity));
                    if(owningHr!=S_OK){status=L"FAILED";reason=L"RETURNED_DEVICE_IDENTITY_QUERY_NOT_S_OK";}
                    else if(!owningIdentity){status=L"FAILED";reason=L"RETURNED_DEVICE_IDENTITY_OUTPUT_MISSING";}
                    else if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"RETURNED_DEVICE_IDENTITY_QUERY_RETURNED_LATE";}
                    else {
                        bool equal=originalIdentity.get()==owningIdentity.get();
                        Flag(details,L"identity_comparison_performed",true);Flag(details,L"canonical_identity_equal",equal);
                        status=equal?L"PASS":L"FAILED";
                        reason=equal?L"SRV_OWNING_DEVICE_IDENTITY_CONFIRMED":L"OWNING_DEVICE_IDENTITY_MISMATCH";
                    }
                }
            }
            // Both temporary QI references release before the returned device.
        }
        Flag(details,L"temporary_identity_references_released",true);
    }
    Flag(details,L"returned_device_reference_released",true);
    if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"RETURNED_DEVICE_IDENTITY_OPERATION_RETURNED_LATE";}
}
void CreateOneSrv(ID3D11Device* device,ID3D11Texture2D* texture,
    std::shared_ptr<Receipt> const& receipt,Json const& details,std::wstring& status,std::wstring& reason) {
    if(!receipt->Checkpoint(L"BEFORE_CREATE_SRV",details)){status=L"BLOCKED";reason=L"SRV_CHECKPOINT_FAILED";return;}
    if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"DEADLINE_BEFORE_SRV_CALL";return;}
    auto requested=RequestedSrvDescriptor();
    {
        winrt::com_ptr<ID3D11ShaderResourceView> srv;
        Flag(details,L"srv_attempted",true);
        // Exactly one view factory call, explicit descriptor, nonnull output storage.
        HRESULT srvHr=device->CreateShaderResourceView(texture,&requested,srv.put());
        Text(details,L"srv_hresult",Hex(srvHr));Number(details,L"srv_hresult_signed",srvHr);
        Flag(details,L"srv_returned",bool(srv));
        if(srvHr!=S_OK) {
            status=L"FAILED";reason=L"SRV_CREATION_FAILED";
            if(srvHr==E_ACCESSDENIED || srvHr==E_NOTIMPL || srvHr==E_NOINTERFACE || srvHr==DXGI_ERROR_UNSUPPORTED){status=L"BLOCKED";reason=L"SRV_API_OR_POLICY_UNAVAILABLE";}
            else if(SUCCEEDED(srvHr)){reason=L"SRV_ALLOCATION_NOT_CONFIRMED";}
        } else if(!srv){status=L"FAILED";reason=L"SRV_OUTPUT_MISSING";}
        else if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"SRV_CALL_RETURNED_LATE";}
        else {
            D3D11_SHADER_RESOURCE_VIEW_DESC returned{};
            srv->GetDesc(&returned); // void metadata query, no invented HRESULT.
            Flag(details,L"srv_get_desc_called",true);details.Insert(L"srv_returned_descriptor",SrvDescriptor(returned));
            bool matches=SameSrvDescriptor(requested,returned);Flag(details,L"srv_descriptors_match",matches);
            if(matches){InspectOwningDevice(device,srv.get(),receipt,details,status,reason);}
            else {status=L"FAILED";reason=L"SRV_DESCRIPTOR_MISMATCH";}
        }
        // SRV reference leaves scope while the caller still owns the texture.
    }
    Flag(details,L"srv_reference_released",true);
    if(details.GetNamedBoolean(L"temporary_identity_references_released",false) && details.GetNamedBoolean(L"returned_device_reference_released",false))Flag(details,L"device_references_released_before_srv",true);
    if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"SRV_OPERATION_RETURNED_LATE";}
}
void CreateOneTexture(ID3D11Device* device,D3D11_TEXTURE2D_DESC const& requested,
    std::shared_ptr<Receipt> const& receipt,Json const& details,std::wstring& status,std::wstring& reason) {
    if(!receipt->Checkpoint(L"BEFORE_CREATE_TEXTURE",details)){status=L"BLOCKED";reason=L"TEXTURE_CHECKPOINT_FAILED";return;}
    if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"DEADLINE_BEFORE_TEXTURE_CALL";return;}
    {
        winrt::com_ptr<ID3D11Texture2D> texture;
        Flag(details,L"texture_attempted",true);
        // Exactly one allocation attempt, no initial data, nonnull output pointer.
        HRESULT textureHr=device->CreateTexture2D(&requested,nullptr,texture.put());
        Text(details,L"texture_hresult",Hex(textureHr));Number(details,L"texture_hresult_signed",textureHr);
        Flag(details,L"texture_returned",bool(texture));
        if(textureHr!=S_OK) {
            status=L"FAILED";reason=L"TEXTURE_CREATION_FAILED";
            if(textureHr==E_ACCESSDENIED || textureHr==E_NOTIMPL || textureHr==E_NOINTERFACE || textureHr==DXGI_ERROR_UNSUPPORTED){status=L"BLOCKED";reason=L"TEXTURE_API_OR_POLICY_UNAVAILABLE";}
            else if(SUCCEEDED(textureHr)){reason=L"TEXTURE_ALLOCATION_NOT_CONFIRMED";}
        } else if(!texture){status=L"FAILED";reason=L"TEXTURE_OUTPUT_MISSING";}
        else if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"TEXTURE_CALL_RETURNED_LATE";}
        else {
            D3D11_TEXTURE2D_DESC returned{};
            texture->GetDesc(&returned); // void API; no invented GetDesc HRESULT.
            Flag(details,L"get_desc_called",true);details.Insert(L"returned_descriptor",Descriptor(returned));
            bool matches=SameDescriptor(requested,returned);Flag(details,L"descriptors_match",matches);
            if(matches){CreateOneSrv(device,texture.get(),receipt,details,status,reason);}
            else {status=L"FAILED";reason=L"TEXTURE_DESCRIPTOR_MISMATCH";}
        }
        // Scoped texture reference releases even on unexpected HRESULT/non-null output.
    }
    Flag(details,L"texture_reference_released",true);
    if(details.GetNamedBoolean(L"srv_reference_released",false))Flag(details,L"srv_released_before_texture",true);
    if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"TEXTURE_OPERATION_RETURNED_LATE";}
}
}
void Probe(std::shared_ptr<Receipt> const& receipt) {
    Json details;Text(details,L"requested_driver_type",L"HARDWARE");Number(details,L"requested_driver_type_value",D3D_DRIVER_TYPE_HARDWARE);
    Number(details,L"requested_feature_level",D3D_FEATURE_LEVEL_11_0);Number(details,L"creation_flags",D3D11_CREATE_DEVICE_BGRA_SUPPORT);
    Flag(details,L"software_fallback_allowed",false);Flag(details,L"render_or_present_tested",false);
    auto requested=RequestedDescriptor();details.Insert(L"requested_descriptor",Descriptor(requested));
    Text(details,L"format_name",L"DXGI_FORMAT_R8G8B8A8_UNORM");Number(details,L"format_value",DXGI_FORMAT_R8G8B8A8_UNORM);
    Flag(details,L"initial_data_supplied",false);Flag(details,L"nonnull_output_pointer",true);
    Flag(details,L"texture_attempted",false);Flag(details,L"get_desc_called",false);
    details.Insert(L"srv_requested_descriptor",SrvDescriptor(RequestedSrvDescriptor()));
    Flag(details,L"srv_nonnull_output_pointer",true);Flag(details,L"srv_attempted",false);Flag(details,L"srv_get_desc_called",false);
    Text(details,L"identity_interface",L"IID_IUnknown");Flag(details,L"get_device_nonnull_output_pointer",true);
    Flag(details,L"get_device_called",false);Flag(details,L"original_device_identity_query_attempted",false);Flag(details,L"returned_device_identity_query_attempted",false);Flag(details,L"identity_comparison_performed",false);
    auto before=Memory();details.Insert(L"memory_before",before);
    if(!before.GetNamedBoolean(L"available",false)){receipt->Finish(L"BLOCKED",L"MEMORY_OBSERVATION_UNAVAILABLE",details);return;}
    double usage=before.GetNamedNumber(L"usage_bytes"),limit=before.GetNamedNumber(L"limit_bytes");
    if(limit<usage || limit-usage<256.0*1024*1024){receipt->Finish(L"BLOCKED",L"INSUFFICIENT_OBSERVED_HEADROOM",details);return;}
    if(!receipt->Checkpoint(L"BEFORE_CREATE_DEVICE",details)){receipt->Finish(L"BLOCKED",L"RECEIPT_PREREQUISITE_FAILED",details);return;}
    if(receipt->Expired() || receipt->Terminal()){receipt->Finish(L"INCONCLUSIVE",L"DEADLINE_BEFORE_DEVICE_CALL",details);return;}
    std::wstring status=L"FAILED",reason=L"DEVICE_CREATION_FAILED";
    {
        winrt::com_ptr<ID3D11Device> device;winrt::com_ptr<ID3D11DeviceContext> context;
        D3D_FEATURE_LEVEL chosen{};D3D_FEATURE_LEVEL const levels[]={D3D_FEATURE_LEVEL_11_0};
        // Exactly one device-creation call. No alternate driver, flags, levels or retry.
        HRESULT hr=D3D11CreateDevice(nullptr,D3D_DRIVER_TYPE_HARDWARE,nullptr,D3D11_CREATE_DEVICE_BGRA_SUPPORT,levels,1,D3D11_SDK_VERSION,device.put(),&chosen,context.put());
        receipt->DeviceObservation(hr,static_cast<unsigned>(chosen));Text(details,L"creation_hresult",Hex(hr));Number(details,L"creation_hresult_signed",hr);Number(details,L"selected_feature_level",chosen);
        Flag(details,L"device_returned",bool(device));Flag(details,L"context_returned",bool(context));
        if(hr!=S_OK) {
            if(hr==DXGI_ERROR_UNSUPPORTED || hr==E_NOINTERFACE || hr==E_NOTIMPL || hr==E_ACCESSDENIED){status=L"BLOCKED";reason=L"DEVICE_API_OR_POLICY_UNAVAILABLE";}
        } else if(!device || !context || chosen!=D3D_FEATURE_LEVEL_11_0){reason=L"DEVICE_OUTPUT_OR_LEVEL_MISMATCH";}
        else if(receipt->Expired() || receipt->Terminal()){status=L"INCONCLUSIVE";reason=L"DEVICE_CALL_RETURNED_LATE";}
        else {
            auto dxgi=device.try_as<IDXGIDevice>();
            if(!dxgi){status=L"BLOCKED";reason=L"DXGI_CLASSIFICATION_UNAVAILABLE";Text(details,L"classification_hresult",Hex(E_NOINTERFACE));}
            else {
                winrt::com_ptr<IDXGIAdapter> adapter;hr=dxgi->GetAdapter(adapter.put());Text(details,L"get_adapter_hresult",Hex(hr));
                if(FAILED(hr)){status=L"BLOCKED";reason=L"ADAPTER_CLASSIFICATION_UNAVAILABLE";}
                else {
                    auto adapter1=adapter.try_as<IDXGIAdapter1>();
                    if(!adapter1){status=L"BLOCKED";reason=L"ADAPTER1_UNAVAILABLE";Text(details,L"classification_hresult",Hex(E_NOINTERFACE));}
                    else {DXGI_ADAPTER_DESC1 desc{};hr=adapter1->GetDesc1(&desc);Text(details,L"get_desc_hresult",Hex(hr));
                        if(FAILED(hr)){status=L"BLOCKED";reason=L"ADAPTER_DESCRIPTION_UNAVAILABLE";}
                        else {Number(details,L"adapter_flags",desc.Flags);bool software=(desc.Flags&DXGI_ADAPTER_FLAG_SOFTWARE)!=0;Flag(details,L"adapter_software_flag",software);
                            if(software){reason=L"SOFTWARE_ADAPTER_UNDER_HARDWARE_REQUEST";}
                            else {CreateOneTexture(device.get(),requested,receipt,details,status,reason);}}
                    }
                }
            }
        }
        if(device && status!=L"PASS")Text(details,L"device_removed_reason",Hex(device->GetDeviceRemovedReason()));
        // Scoped COM pointers release context, device and adapter references on this worker.
    }
    Flag(details,L"test_resources_released",true);
    auto after=Memory();details.Insert(L"memory_after_release",after);
    if(status==L"PASS") {
        if(!after.GetNamedBoolean(L"available",false)){status=L"BLOCKED";reason=L"FINAL_MEMORY_OBSERVATION_UNAVAILABLE";}
        else if(after.GetNamedNumber(L"usage_bytes")-usage>64.0*1024*1024){status=L"FAILED";reason=L"OBSERVED_MEMORY_GROWTH_EXCEEDED";}
    }
    receipt->Finish(status,reason,details);
}
}
