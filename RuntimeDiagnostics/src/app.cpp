// SPDX-License-Identifier: Apache-2.0
#include "diagnostics.h"
#include <d2d1_1.h>
#include <d3d11_1.h>
#include <dwrite.h>
#include <dxgi1_2.h>
#include <algorithm>
#include <chrono>
#include <iterator>
#include <mutex>
#include <thread>
#include <winrt/Windows.ApplicationModel.h>
#include <winrt/Windows.ApplicationModel.Activation.h>
#include <winrt/Windows.ApplicationModel.Core.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#if !LFD_D00_ONLY
#include <winrt/Windows.Gaming.Input.h>
#endif
#include <winrt/Windows.System.h>
#include <winrt/Windows.UI.Core.h>
#include <winrt/Windows.UI.Input.h>
#include <winrt/Windows.UI.ViewManagement.h>

// Direct2D exposes DrawText; the unrelated Win32 generic-text macro must not
// rename the COM method to DrawTextW in this translation unit.
#ifdef DrawText
#undef DrawText
#endif

namespace {
using namespace winrt;
using namespace Windows::ApplicationModel::Core;
using namespace Windows::UI::Core;

struct UiState {
    std::mutex mutex;
    std::wstring native = L"D00 activation: waiting";
    #if LFD_D00_ONLY
    std::wstring java = L"D00-only build: Java/JNI disabled at compile time";
#else
    std::wstring java = L"Java 21 smoke: not started";
#endif
    std::wstring note = L"No Minecraft, accounts, network or game content.";
    bool nativeReady = false;
    bool displayReady = false;
#if !LFD_D00_ONLY
    bool smokeRequested = false;
    bool deadlineWon = false;
#endif
    bool closed = false;
    std::shared_ptr<lfd::Receipt> nativeReceipt;
#if !LFD_D00_ONLY
    std::shared_ptr<lfd::Receipt> javaReceipt;
#endif
};

std::shared_ptr<UiState> ProcessUi() {
    static auto state = std::make_shared<UiState>();
    return state;
}
std::atomic<bool> nativeControlStarted{false};

void ShowNativeResult(std::shared_ptr<UiState> const& ui,
                      std::shared_ptr<lfd::Receipt> const& receipt) {
    DWORD persistence = receipt->PersistenceError();
    auto status = receipt->Status();
    std::lock_guard<std::mutex> lock(ui->mutex);
    ui->nativeReady = ui->displayReady && !persistence && status == L"PASS" && receipt->Terminal();
    ui->native = persistence ? L"D00: RECEIPT ERROR — Java is blocked" : L"D00: " + status;
    ui->note = persistence ? L"Receipt persistence failed. Close the app; no pass is claimed." :
        (ui->nativeReady ? L"Activation receipt saved in this diagnostic app's LocalState." :
            L"Activation/display prerequisite unavailable. Java remains blocked; inspect the receipt.");
}

#if !LFD_D00_ONLY
void ShowJavaResult(std::shared_ptr<UiState> const& ui,
                    std::shared_ptr<lfd::Receipt> const& receipt) {
    DWORD persistence = receipt->PersistenceError();
    auto status = receipt->Status();
    std::lock_guard<std::mutex> lock(ui->mutex);
    if (persistence) {
        ui->java = L"Java 21: RECEIPT ERROR — no saved pass is claimed";
        ui->note = L"Close the app. A fresh process is required for any later attempt.";
    } else if (ui->deadlineWon) {
        ui->java = L"Java 21: INCONCLUSIVE — 30 second deadline";
        ui->note = L"The watchdog cannot cancel a blocked native call. Owner: close this app.";
    } else {
        ui->java = L"Java 21: " + status;
        ui->note = L"Inspect the saved receipt. Another attempt requires owner termination and a fresh process.";
    }
}

#endif

void StartNativeControl(std::shared_ptr<UiState> const& ui, bool renderReady) {
    if (nativeControlStarted.exchange(true)) return;
    // One call is made from the framework-view Run method. This worker never
    // loads a JVM and does not capture the view or any renderer object.
    std::thread([ui, renderReady] {
        std::shared_ptr<lfd::Receipt> receipt;
        try {
            winrt::init_apartment(winrt::apartment_type::multi_threaded);
            receipt = std::make_shared<lfd::Receipt>(L"D00");
            {
                std::lock_guard<std::mutex> lock(ui->mutex);
                ui->nativeReceipt = receipt;
                ui->native = L"D00 activation: recording package and resource evidence";
            }
            if (renderReady) {
                lfd::RunNativeControl(receipt);
            } else {
                lfd::Json details;
                lfd::Flag(details, L"jvm_loaded", false);
                lfd::Flag(details, L"ui_render_is_d06_test", false);
                receipt->Finish(L"FAILED", L"DIAGNOSTIC_UI_UNAVAILABLE", details);
            }
        } catch (winrt::hresult_error const& error) {
            if (receipt) {
                lfd::Json details;
                lfd::Number(details, L"hresult", static_cast<int32_t>(error.code()));
                receipt->Finish(L"FAILED", L"D00_OBSERVATION_ERROR", details);
            }
        } catch (...) {
            if (receipt) receipt->Finish(L"FAILED", L"D00_OBSERVATION_ERROR");
        }
        if (receipt) {
            ShowNativeResult(ui, receipt);
        } else {
            std::lock_guard<std::mutex> lock(ui->mutex);
            ui->native = L"D00: RECEIPT INITIALIZATION ERROR — Java is blocked";
            ui->note = L"No receipt or activation pass is claimed. Owner: close this app.";
            ui->nativeReady = false;
        }
    }).detach();
}

#if !LFD_D00_ONLY
void RequestJavaSmoke(std::shared_ptr<UiState> const& ui) {
    {
        std::lock_guard<std::mutex> lock(ui->mutex);
        if (!ui->nativeReady || !ui->displayReady || ui->smokeRequested || ui->closed) return;
        // This guard is set before creating any worker or attempting a VM.
        // Even a blocked/failed attempt requires a fresh process afterwards.
        ui->smokeRequested = true;
        ui->java = L"Java 21 smoke: starting dedicated MTA worker";
        ui->note = L"One smoke attempt per process. The UI remains independent of the JVM worker.";
    }
    std::thread([ui] {
        std::shared_ptr<lfd::Receipt> receipt;
        try {
            winrt::init_apartment(winrt::apartment_type::multi_threaded);
            receipt = std::make_shared<lfd::Receipt>(L"S21-JNI21");
            {
                std::lock_guard<std::mutex> lock(ui->mutex);
                ui->javaReceipt = receipt;
            }
            lfd::Json starting;
            lfd::Text(starting, L"execution_owner", L"DEDICATED_MTA_WORKER");
            lfd::Flag(starting, L"fresh_process_required_for_retry", true);
            receipt->Checkpoint(L"SMOKE_WORKER_STARTED", starting);

            std::thread([ui, receipt] {
                try {
                    winrt::init_apartment(winrt::apartment_type::multi_threaded);
                    auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(30);
                    while (std::chrono::steady_clock::now() < deadline) {
                        if (receipt->Terminal()) return;
                        std::this_thread::sleep_for(std::chrono::milliseconds(50));
                    }
                    lfd::Json detail;
                    lfd::Number(detail, L"deadline_ms", 30000);
                    lfd::Flag(detail, L"watchdog_can_cancel_native_call", false);
                    lfd::Flag(detail, L"owner_termination_required", true);
                    bool won = receipt->Finish(L"INCONCLUSIVE", L"SMOKE_WATCHDOG_DEADLINE", detail);
                    if (won) {
                        std::lock_guard<std::mutex> lock(ui->mutex);
                        ui->deadlineWon = true;
                    }
                    ShowJavaResult(ui, receipt);
                } catch (...) {
                    // Do not terminate another thread or retry a VM if the
                    // observer itself fails. Preserve the existing checkpoint.
                    std::lock_guard<std::mutex> lock(ui->mutex);
                    ui->java = L"Java 21: watchdog observation unavailable";
                    ui->note = L"No completion is inferred. Owner: close this app if it does not finish.";
                }
            }).detach();

            lfd::RunJava21Smoke(receipt);
            if (!receipt->Terminal()) receipt->Finish(L"INCONCLUSIVE", L"SMOKE_RETURNED_WITHOUT_RESULT");
        } catch (winrt::hresult_error const& error) {
            if (receipt) {
                lfd::Json details;
                lfd::Number(details, L"hresult", static_cast<int32_t>(error.code()));
                receipt->Finish(L"FAILED", L"SMOKE_WORKER_ERROR", details);
            }
        } catch (...) {
            if (receipt) receipt->Finish(L"FAILED", L"SMOKE_WORKER_ERROR");
        }
        if (receipt) {
            ShowJavaResult(ui, receipt);
        } else {
            std::lock_guard<std::mutex> lock(ui->mutex);
            ui->java = L"Java 21: RECEIPT INITIALIZATION ERROR";
            ui->note = L"No completion is inferred. Close the app before another attempt.";
        }
    }).detach();
}

#endif

struct DiagnosticView : winrt::implements<DiagnosticView, IFrameworkView> {
    void Initialize(CoreApplicationView const& view) {
        activated_ = view.Activated([weak = get_weak()](auto const&, auto const&) {
            if (auto self = weak.get()) self->window_.Activate();
        });
        applicationView_ = view;
    }

    void SetWindow(CoreWindow const& window) {
        window_ = window;
        auto weak = get_weak();
        closed_ = window.Closed([weak](auto const&, auto const&) {
            if (auto self = weak.get()) {
                self->closedFlag_ = true;
                std::lock_guard<std::mutex> lock(self->ui_->mutex);
                self->ui_->closed = true;
            }
        });
        resized_ = window.SizeChanged([weak](auto const&, auto const&) {
            if (auto self = weak.get()) self->resizePending_ = true;
        });
#if !LFD_D00_ONLY
        key_ = window.KeyDown([weak](auto const&, KeyEventArgs const& args) {
            if (auto self = weak.get()) {
                if (args.VirtualKey() == Windows::System::VirtualKey::Enter ||
                    args.VirtualKey() == Windows::System::VirtualKey::GamepadA) {
                    RequestJavaSmoke(self->ui_);
                    args.Handled(true);
                }
            }
        });
        pointer_ = window.PointerPressed([weak](auto const&, PointerEventArgs const& args) {
            if (auto self = weak.get()) {
                auto point = args.CurrentPoint().Position();
                if (point.X >= 48 && point.X <= self->width_ - 48 &&
                    point.Y >= 320 && point.Y <= 388) RequestJavaSmoke(self->ui_);
            }
        });
#endif
        try {
#if LFD_D00_ONLY
            Windows::UI::ViewManagement::ApplicationView::GetForCurrentView().Title(L"LegacyForge Runtime Diagnostics  -  D00 ONLY");
#else
            Windows::UI::ViewManagement::ApplicationView::GetForCurrentView().Title(L"LegacyForge Runtime Diagnostics");
#endif
        } catch (...) { }
    }

    void Load(winrt::hstring const&) { }

    void Run() {
        bool renderReady = false;
        try {
            CreateRenderer(); Render(); renderReady = true;
            std::lock_guard<std::mutex> lock(ui_->mutex);
            ui_->displayReady = true;
        }
        catch (...) {
            try {
                Windows::UI::ViewManagement::ApplicationView::GetForCurrentView().Title(
                    L"Runtime Diagnostics — display unavailable; Java blocked");
            } catch (...) { }
        }
        StartNativeControl(ui_, renderReady);
        while (!closedFlag_) {
            window_.Dispatcher().ProcessEvents(CoreProcessEventsOption::ProcessAllIfPresent);
            if (closedFlag_) break;
            if (renderReady) {
                try {
                    if (resizePending_) { Resize(); resizePending_ = false; }
#if !LFD_D00_ONLY
                    PollGamepad();
#endif
                    Render();
                } catch (...) {
                    renderReady = false;
                    std::lock_guard<std::mutex> lock(ui_->mutex);
                    ui_->nativeReady = false;
                    ui_->displayReady = false;
                    ui_->note = L"Display failure. No further smoke request is permitted; close the app.";
                }
            } else {
                std::this_thread::sleep_for(std::chrono::milliseconds(16));
            }
        }
        // Detached workers own their shared state/receipt. There is no UI-thread
        // join, thread cancellation, JVM unload, or second-VM recovery attempt.
    }

    void Uninitialize() {
        {
            std::lock_guard<std::mutex> lock(ui_->mutex);
            ui_->closed = true;
        }
        if (applicationView_) applicationView_.Activated(activated_);
        if (window_) {
            window_.Closed(closed_);
            window_.SizeChanged(resized_);
#if !LFD_D00_ONLY
            window_.KeyDown(key_);
            window_.PointerPressed(pointer_);
#endif
        }
    }

private:
    void CreateRenderer() {
        UINT flags = D3D11_CREATE_DEVICE_BGRA_SUPPORT;
        D3D_FEATURE_LEVEL levels[] = {D3D_FEATURE_LEVEL_11_1, D3D_FEATURE_LEVEL_11_0,
            D3D_FEATURE_LEVEL_10_1, D3D_FEATURE_LEVEL_10_0};
        D3D_FEATURE_LEVEL chosen{};
        winrt::check_hresult(D3D11CreateDevice(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr,
            flags, levels, static_cast<UINT>(std::size(levels)), D3D11_SDK_VERSION,
            device_.put(), &chosen, context_.put()));
        auto dxgiDevice = device_.as<IDXGIDevice>();
        D2D1_FACTORY_OPTIONS options{};
        winrt::check_hresult(D2D1CreateFactory(D2D1_FACTORY_TYPE_SINGLE_THREADED,
            __uuidof(ID2D1Factory1), &options, d2dFactory_.put_void()));
        winrt::check_hresult(d2dFactory_->CreateDevice(dxgiDevice.get(), d2dDevice_.put()));
        winrt::check_hresult(d2dDevice_->CreateDeviceContext(D2D1_DEVICE_CONTEXT_OPTIONS_NONE, drawing_.put()));
        winrt::check_hresult(DWriteCreateFactory(DWRITE_FACTORY_TYPE_SHARED,
            __uuidof(IDWriteFactory), reinterpret_cast<IUnknown**>(writeFactory_.put())));
        winrt::check_hresult(writeFactory_->CreateTextFormat(L"Segoe UI", nullptr,
            DWRITE_FONT_WEIGHT_NORMAL, DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            20.0f, L"en-US", text_.put()));
        winrt::check_hresult(writeFactory_->CreateTextFormat(L"Segoe UI", nullptr,
            DWRITE_FONT_WEIGHT_SEMI_BOLD, DWRITE_FONT_STYLE_NORMAL, DWRITE_FONT_STRETCH_NORMAL,
            34.0f, L"en-US", title_.put()));
        winrt::check_hresult(drawing_->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::White), brush_.put()));
        auto adapter = winrt::com_ptr<IDXGIAdapter>{};
        winrt::check_hresult(dxgiDevice->GetAdapter(adapter.put()));
        auto factory = winrt::com_ptr<IDXGIFactory2>{};
        winrt::check_hresult(adapter->GetParent(__uuidof(IDXGIFactory2), factory.put_void()));
        auto bounds = window_.Bounds();
        width_ = std::max(320.0f, bounds.Width);
        height_ = std::max(240.0f, bounds.Height);
        DXGI_SWAP_CHAIN_DESC1 description{};
        description.Width = static_cast<UINT>(width_);
        description.Height = static_cast<UINT>(height_);
        description.Format = DXGI_FORMAT_B8G8R8A8_UNORM;
        description.SampleDesc.Count = 1;
        description.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
        description.BufferCount = 2;
        description.SwapEffect = DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL;
        description.Scaling = DXGI_SCALING_STRETCH;
        description.AlphaMode = DXGI_ALPHA_MODE_IGNORE;
        winrt::check_hresult(factory->CreateSwapChainForCoreWindow(device_.get(),
            winrt::get_unknown(window_), &description, nullptr, swapchain_.put()));
        CreateTarget();
    }

    void CreateTarget() {
        auto surface = winrt::com_ptr<IDXGISurface>{};
        winrt::check_hresult(swapchain_->GetBuffer(0, __uuidof(IDXGISurface), surface.put_void()));
        auto properties = D2D1::BitmapProperties1(
            D2D1_BITMAP_OPTIONS_TARGET | D2D1_BITMAP_OPTIONS_CANNOT_DRAW,
            D2D1::PixelFormat(DXGI_FORMAT_B8G8R8A8_UNORM, D2D1_ALPHA_MODE_IGNORE), 96, 96);
        winrt::check_hresult(drawing_->CreateBitmapFromDxgiSurface(surface.get(), &properties, target_.put()));
        drawing_->SetTarget(target_.get());
        drawing_->SetDpi(96, 96);
    }

    void Resize() {
        auto bounds = window_.Bounds();
        width_ = std::max(320.0f, bounds.Width);
        height_ = std::max(240.0f, bounds.Height);
        drawing_->SetTarget(nullptr);
        target_ = nullptr;
        context_->ClearState();
        context_->Flush();
        winrt::check_hresult(swapchain_->ResizeBuffers(2, static_cast<UINT>(width_),
            static_cast<UINT>(height_), DXGI_FORMAT_B8G8R8A8_UNORM, 0));
        CreateTarget();
    }

    void DrawTextLine(std::wstring const& text, float top, float bottom,
                      D2D1_COLOR_F color, bool heading = false) {
        brush_->SetColor(color);
        drawing_->DrawText(text.c_str(), static_cast<UINT32>(text.size()),
            heading ? title_.get() : text_.get(), D2D1::RectF(48, top, width_ - 48, bottom), brush_.get());
    }

    void Render() {
        std::wstring native, java, note;
#if !LFD_D00_ONLY
        bool enabled = false, requested = false;
#endif
        {
            std::lock_guard<std::mutex> lock(ui_->mutex);
            native = ui_->native; java = ui_->java; note = ui_->note;
#if !LFD_D00_ONLY
            enabled = ui_->nativeReady && !ui_->smokeRequested;
            requested = ui_->smokeRequested;
#endif
        }
        drawing_->BeginDraw();
        drawing_->Clear(D2D1::ColorF(0.035f, 0.050f, 0.075f));
#if LFD_D00_ONLY
        DrawTextLine(L"Runtime Diagnostics  -  D00 ONLY", 42, 100,
#else
        DrawTextLine(L"LegacyForge Runtime Diagnostics", 42, 100,
#endif
            D2D1::ColorF(0.94f, 0.97f, 1.0f), true);
#if LFD_D00_ONLY
        DrawTextLine(L"Phase 6B.1a / native control only / no Java actions", 106, 146,
#else
        DrawTextLine(L"Phase 6B.1  /  independent synthetic evidence", 106, 146,
#endif
            D2D1::ColorF(0.50f, 0.72f, 0.88f));
        DrawTextLine(native, 174, 224, D2D1::ColorF(0.82f, 0.91f, 0.98f));
        DrawTextLine(java, 242, 302, D2D1::ColorF(0.82f, 0.91f, 0.98f));
#if !LFD_D00_ONLY
        brush_->SetColor(enabled ? D2D1::ColorF(0.13f, 0.43f, 0.63f) : D2D1::ColorF(0.15f, 0.20f, 0.25f));
        drawing_->FillRoundedRectangle(D2D1::RoundedRect(
            D2D1::RectF(48, 320, width_ - 48, 388), 8, 8), brush_.get());
        DrawTextLine(requested ? L"Smoke already requested — fresh process required" :
            L"Enter / controller A / click: Run Java 21 smoke", 338, 382,
            enabled ? D2D1::ColorF(1.0f, 1.0f, 1.0f) : D2D1::ColorF(0.56f, 0.64f, 0.71f));
#else
        DrawTextLine(L"D00 starts automatically. No interactive test actions.", 338, 400,
            D2D1::ColorF(0.56f, 0.64f, 0.71f));
#endif
        DrawTextLine(note, 422, 514, D2D1::ColorF(0.70f, 0.79f, 0.86f));
        DrawTextLine(L"Receipts: app-local Phase6B1Receipts. UI drawing is not a graphics capability test.",
            534, height_ - 24, D2D1::ColorF(0.47f, 0.58f, 0.67f));
        winrt::check_hresult(drawing_->EndDraw());
        winrt::check_hresult(swapchain_->Present(1, 0));
    }

#if !LFD_D00_ONLY
    void PollGamepad() {
        bool pressed = false;
        try {
            auto gamepads = Windows::Gaming::Input::Gamepad::Gamepads();
            for (auto const& pad : gamepads) {
                auto buttons = pad.GetCurrentReading().Buttons;
                if ((buttons & Windows::Gaming::Input::GamepadButtons::A) !=
                    Windows::Gaming::Input::GamepadButtons::None) pressed = true;
            }
        } catch (...) { }
        if (pressed && !gamepadWasDown_) RequestJavaSmoke(ui_);
        gamepadWasDown_ = pressed;
    }

#endif

    std::shared_ptr<UiState> ui_ = ProcessUi();
    CoreWindow window_{nullptr};
    CoreApplicationView applicationView_{nullptr};
    winrt::event_token activated_{}, closed_{}, resized_{};
    bool closedFlag_ = false, resizePending_ = false;
#if !LFD_D00_ONLY
    winrt::event_token key_{}, pointer_{};
    bool gamepadWasDown_ = false;
#endif
    float width_ = 1280, height_ = 720;
    winrt::com_ptr<ID3D11Device> device_;
    winrt::com_ptr<ID3D11DeviceContext> context_;
    winrt::com_ptr<IDXGISwapChain1> swapchain_;
    winrt::com_ptr<ID2D1Factory1> d2dFactory_;
    winrt::com_ptr<ID2D1Device> d2dDevice_;
    winrt::com_ptr<ID2D1DeviceContext> drawing_;
    winrt::com_ptr<ID2D1Bitmap1> target_;
    winrt::com_ptr<ID2D1SolidColorBrush> brush_;
    winrt::com_ptr<IDWriteFactory> writeFactory_;
    winrt::com_ptr<IDWriteTextFormat> text_, title_;
};

struct DiagnosticSource : winrt::implements<DiagnosticSource, IFrameworkViewSource> {
    IFrameworkView CreateView() { return winrt::make<DiagnosticView>(); }
};
}

int __stdcall wWinMain(HINSTANCE, HINSTANCE, PWSTR, int) {
    try {
        winrt::init_apartment(winrt::apartment_type::multi_threaded);
        CoreApplication::Run(winrt::make<DiagnosticSource>());
        return 0;
    } catch (winrt::hresult_error const& error) {
        return static_cast<int32_t>(error.code());
    } catch (...) {
        return static_cast<int>(E_FAIL);
    }
}
