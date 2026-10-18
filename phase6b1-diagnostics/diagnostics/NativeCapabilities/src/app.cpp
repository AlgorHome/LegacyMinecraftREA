// SPDX-License-Identifier: Apache-2.0
#include "native.h"
#include <chrono>
#include <functional>
#include <thread>
#include <winrt/Windows.ApplicationModel.Activation.h>
#include <winrt/Windows.ApplicationModel.Core.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.UI.Core.h>
#include <winrt/Windows.UI.Popups.h>
#include <winrt/Windows.UI.ViewManagement.h>

namespace {
using namespace winrt;
using namespace Windows::ApplicationModel::Core;
using namespace Windows::UI::Core;
using namespace Windows::UI::Popups;
struct View : implements<View,IFrameworkView> {
    CoreWindow window_{nullptr};CoreApplicationView view_{nullptr};
    event_token activated_{},closed_{};
    std::shared_ptr<lfn::ProbeState> state_=std::make_shared<lfn::ProbeState>();
    Windows::Foundation::IAsyncOperation<IUICommand> dialogOperation_{nullptr};
    void Show(std::wstring const& content) {
        // Platform UI owns drawing; this program has no swapchain/target/presentation code.
        try {MessageDialog dialog{content,L"Native Diagnostics — D06-SRV03"};dialogOperation_=dialog.ShowAsync();}
        catch(...) {try {Windows::UI::ViewManagement::ApplicationView::GetForCurrentView().Title(L"Native Diagnostics — D06-SRV03: UI unavailable; inspect receipt");}catch(...) {}}
    }
    void Initialize(CoreApplicationView const& view) {
        view_=view;
        activated_=view.Activated([weak=get_weak()](auto const&,Windows::ApplicationModel::Activation::IActivatedEventArgs const& args){
            if(auto self=weak.get()) {
                try {
                    self->window_.Activate();
                    if(self->state_->started.exchange(true))return;
                    if(args.Kind()!=Windows::ApplicationModel::Activation::ActivationKind::Launch){self->Show(L"BLOCKED: unsupported activation. No test dispatched.");return;}
                    auto command=args.as<Windows::ApplicationModel::Activation::LaunchActivatedEventArgs>().Arguments();
                    if(!command.empty() && command!=lfn::Case){self->Show(L"BLOCKED: unknown case. No worker or device call dispatched.");return;}
                    self->Start();
                }catch(...){self->Show(L"INCONCLUSIVE: startup/receipt initialization failed. No saved PASS claimed.");}
            }
        });
    }
    void SetWindow(CoreWindow const& window) {window_=window;closed_=window.Closed([state=state_](auto const&,auto const&){state->closed=true;});}
    void Load(hstring const&){}
    void Run(){window_.Dispatcher().ProcessEvents(CoreProcessEventsOption::ProcessUntilQuit);}
    void Uninitialize(){state_->closed=true;if(view_)view_.Activated(activated_);if(window_)window_.Closed(closed_);}
    void Start(){
        state_->receipt=std::make_shared<lfn::Receipt>();auto state=state_;
        if(!state->receipt->Checkpoint(L"STARTED")){Show(L"BLOCKED: initial receipt persistence failed. No device call.");return;}
        state->receipt->ArmDeadline();
        auto dispatcher=window_.Dispatcher();auto weak=get_weak();
        auto notify=[state,dispatcher,weak]{
            if(state->closed || state->notified.exchange(true))return;
            try {dispatcher.RunAsync(CoreDispatcherPriority::Normal,[state,weak]{
                if(auto self=weak.get()) {
                    auto result=state->receipt->Snapshot();
                    std::wstring text=L"Case: D06-SRV03 / package 0.2.5.0\nTest status: "+result.status+L"\nReason: "+result.reason+L"\nHardware request: yes; no software fallback\nDevice creation HRESULT: "+result.creation+L"\nFeature level: "+result.feature+L"\nReceipt persistence: "+(result.persistence==0?std::wstring(L"saved; verify downloaded JSON"):std::wstring(L"NOT CONFIRMED / error ")+std::to_wstring(result.persistence))+L"\nRun: "+state->receipt->RunId()+L"\nJava/JNI excluded. One SRV owning-device identity query; no pipeline binding or rendering. Verify creation and identity results in JSON.\nClose this message; no additional test will run.";
                    self->Show(text);
                }
            });}catch(...){}
        };
        std::thread([state,notify]{
            try {init_apartment(apartment_type::multi_threaded);
                while(!state->receipt->Terminal() && !state->closed && !state->receipt->Expired())std::this_thread::sleep_for(std::chrono::milliseconds(25));
                if(!state->receipt->Terminal())state->receipt->Finish(L"INCONCLUSIVE",state->closed?L"OWNER_CLOSED":L"NATIVE_CALL_DEADLINE");
                while(state->receipt->Terminal() && !state->receipt->Settled() && !state->receipt->Expired() && !state->closed)std::this_thread::sleep_for(std::chrono::milliseconds(25));
            }catch(...) {try{state->receipt->Finish(L"INCONCLUSIVE",L"OBSERVER_UNAVAILABLE");}catch(...) {}}
            notify();
        }).detach();
        std::thread([state,notify]{
            try {init_apartment(apartment_type::multi_threaded);if(!state->receipt->Terminal())lfn::Probe(state->receipt);}
            catch(hresult_error const& e){try{lfn::Json d;lfn::Text(d,L"exception_hresult",lfn::Hex(e.code()));state->receipt->Finish(L"FAILED",L"NATIVE_EXCEPTION",d);}catch(...) {}}
            catch(...){try{state->receipt->Finish(L"FAILED",L"NATIVE_EXCEPTION_UNCLASSIFIED");}catch(...) {}}
            notify();
        }).detach();
    }
};
struct Source : implements<Source,IFrameworkViewSource>{IFrameworkView CreateView(){return make<View>();}};
}
int __stdcall wWinMain(HINSTANCE,HINSTANCE,PWSTR,int){
    try {winrt::init_apartment(winrt::apartment_type::multi_threaded);Windows::ApplicationModel::Core::CoreApplication::Run(winrt::make<Source>());return 0;}
    catch(winrt::hresult_error const& e){return static_cast<int32_t>(e.code());}catch(...){return static_cast<int>(E_FAIL);}
}
