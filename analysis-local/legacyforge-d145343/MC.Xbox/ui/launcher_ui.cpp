#include "launcher_ui.h"
#include "installed_highlight.h"

#include "mod_source.h"

#include "mods_browser.h"
#include "auth_screen.h"
#include "launcher_mouse.h"
#include "launcher_common.h"
#include "minecraft_auth.h"
#include "minecraft_launch.h"
#include "profiles.h"
#include "remote_file_server.h"
#include "telemetry.h"

#include <algorithm>
#include <chrono>
#include <thread>
#include <string_view>
#include <winrt/Windows.UI.Core.h>
#include <winrt/Windows.UI.Text.Core.h>
#include <winrt/Windows.UI.ViewManagement.h>

#include <wrl.h>

using Microsoft::WRL::ComPtr;
using namespace ABI::Windows::UI::Core;

extern ComPtr<ICoreWindow> g_authWindow;

static bool IsVirtualKeyDown(ICoreWindow* window, ABI::Windows::System::VirtualKey key) {
    if (!CoreWindowAcceptsInput()) return false;
    if (!window) return false;
    CoreVirtualKeyStates state = CoreVirtualKeyStates_None;
    if (FAILED(window->GetKeyState(key, &state))) {
        return false;
    }
    return (state & CoreVirtualKeyStates_Down) == CoreVirtualKeyStates_Down;
}

bool AnyVirtualKeyDown(ICoreWindow* window, std::initializer_list<ABI::Windows::System::VirtualKey> keys) {
    for (const auto key : keys) {
        if (IsVirtualKeyDown(window, key)) {
            return true;
        }
    }
    return false;
}
void ProcessAuthUiEvents() {
    if (!g_authWindow) return;
    static bool dispatcherErrorLogged = false;

    ComPtr<ICoreDispatcher> dispatcher;
    HRESULT hr = g_authWindow->get_Dispatcher(dispatcher.GetAddressOf());
    if (FAILED(hr) || !dispatcher) {
        if (!dispatcherErrorLogged) {
            dispatcherErrorLogged = true;
            WriteLogF(L"Auth screen get_Dispatcher failed hr=0x%08X", hr);
        }
        return;
    }

    boolean hasThreadAccess = false;
    hr = dispatcher->get_HasThreadAccess(&hasThreadAccess);
    if (FAILED(hr) || !hasThreadAccess) {
        if (!dispatcherErrorLogged) {
            dispatcherErrorLogged = true;
            WriteLogF(L"Auth screen dispatcher access unavailable hr=0x%08X access=%d",
                hr, hasThreadAccess ? 1 : 0);
        }
        return;
    }

    hr = dispatcher->ProcessEvents(CoreProcessEventsOption_ProcessAllIfPresent);
    if (FAILED(hr) && !dispatcherErrorLogged) {
        dispatcherErrorLogged = true;
        WriteLogF(L"Auth screen ProcessEvents failed hr=0x%08X", hr);
    }
}

LauncherMouse& LauncherMouseInstance() {
    static LauncherMouse instance;
    return instance;
}

void RenderAuth(AuthScreenRenderer* renderer, const AuthUiState& state) {
    ProcessAuthUiEvents();
    if (renderer) {
        LauncherMouse& mouse = LauncherMouseInstance();
        mouse.Update(renderer->Width(), renderer->Height());
        if (mouse.Visible()) {
            renderer->SetCursor(mouse.X(), mouse.Y(), true);
        }
        renderer->Render(state);
    }
}

void SleepWithAuthUi(AuthScreenRenderer* renderer, AuthUiState& state, int milliseconds) {
    const auto start = std::chrono::steady_clock::now();
    while (true) {
        const auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now() - start).count();
        if (elapsed >= milliseconds) break;

        RenderAuth(renderer, state);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void RenderPreparationProgress(
    AuthScreenRenderer* renderer,
    AuthUiState& state,
    const wchar_t* status,
    const wchar_t* detail,
    float progress) {
    state.title = L"Preparing Minecraft";
    state.showDeviceCode = false;
    state.status = status ? status : L"Preparing runtime";
    state.detail = detail ? detail : L"";
    state.progress = progress;
    state.secondsRemaining = 0;
    state.isError = false;
    RenderAuth(renderer, state);
}

bool RunLaunchTaskWithLiveUi(
    AuthScreenRenderer* renderer,
    AuthUiState& state,
    const std::vector<std::wstring>& launchLogPaths,
    const std::wstring& loaderLabel,
    const std::function<bool(LaunchProgressCallback progress)>& launchTask) {
    state.title = L"Preparing Minecraft";
    state.showDeviceCode = false;
    state.showLaunchLog = true;
    state.isError = false;
    state.secondsRemaining = 0;
    state.status = L"Starting Minecraft";
    state.detail = loaderLabel.empty()
        ? L"Preparing launch files."
        : (L"Preparing " + loaderLabel + L" and launch files.");
    state.progress = 0.12f;
    state.launchLogText = ReadLaunchLogTailForUi(launchLogPaths);
    RenderAuth(renderer, state);

    LaunchProgressCallback progress = [&](const wchar_t* status, const wchar_t* detail, float value) {
        state.status = status ? status : L"Starting Minecraft";
        state.detail = detail ? detail : L"";
        state.progress = value;
        state.launchLogText = ReadLaunchLogTailForUi(launchLogPaths);
        state.animation = static_cast<float>((GetTickCount64() % 100000) / 1000.0);
        RenderAuth(renderer, state);
    };

    return launchTask(progress);
}

static void ShowRemoteFilesPage(ICoreWindow* window, AuthScreenRenderer* renderer, AuthUiState& state, const std::wstring& runtimeRoot) {
    WriteLog(L"Remote files page opened");
    StartRemoteFileServer(runtimeRoot);

    state.showMainMenu = false;
    state.showModsPage = false;
    state.showRemoteFiles = true;
    state.showDeviceCode = false;
    state.isError = false;

    bool backWasDown = false;
    while (true) {
        if (RemoteFileServerRunning()) {
            state.status = L"Remote file manager is running";
            state.detail = L"Open " + RemoteFileServerUrl() + L"\nPIN: " + a2w(RemoteFileServerPin().c_str());
        } else {
            state.status = L"Remote file manager is not running";
            state.detail = L"Could not start the LAN server on port 27632. Check that another copy is not already running.";
            state.isError = true;
        }

        state.animation = static_cast<float>((GetTickCount64() % 100000) / 1000.0);
        RenderAuth(renderer, state);

        LauncherMouse& mouse = LauncherMouseInstance();
        const bool clickBack = mouse.Visible() && mouse.TakeClick() &&
            renderer->HitTest(mouse.X(), mouse.Y()) == launchhit::kBack;

        const bool backDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Escape,
            ABI::Windows::System::VirtualKey_GamepadB
        });
        if ((backDown && !backWasDown) || clickBack) {
            StopRemoteFileServer();
            state.showRemoteFiles = false;
            state.showMainMenu = true;
            state.isError = false;
            state.status = L"Remote file manager stopped";
            state.detail = L"";
            WriteLog(L"Remote files page closed");
            return;
        }

        backWasDown = backDown;
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }
}

static std::wstring CrashHeadline(const telemetry::CrashRecord& record) {
    if (record.repeatCount >= 3) {
        return L"Minecraft has crashed " + std::to_wstring(record.repeatCount) + L" launches in a row";
    }
    if (record.exception.find(L"unknown_") != std::wstring::npos) {
        return L"Minecraft closed unexpectedly";
    }
    if (record.phase == L"mod_load") return L"Minecraft crashed while loading mods";
    if (record.phase == L"jvm_init") return L"Minecraft crashed while starting up";
    if (record.phase == L"ingame") return L"Minecraft crashed while playing";
    return L"Minecraft closed unexpectedly";
}

static std::wstring CrashSuspectLine(const telemetry::CrashRecord& record) {
    if (!record.suspectedMod.empty()) {
        std::wstring line = L"Suspected: " + record.suspectedMod;
        if (!record.detail.targetMethod.empty()) {
            line += L"\nIt asked for something this version of Minecraft does not have.";
        }
        return line;
    }
    if (!record.detail.symbol.empty()) {
        // ole32 is com, and jna cannot LoadLibrary a system dll from a uwp package
        if (record.detail.symbol.find("Ole32") != std::string::npos) {
            return L"A mod asked Windows for hardware details, which this console blocks.\n"
                   L"Mods that probe the GPU this way cannot run here yet.";
        }
        return L"A mod asked for " + a2w(record.detail.symbol.c_str()) +
            L", which this console does not provide.";
    }
    if (record.exception.find(L"heap_exhausted") != std::wstring::npos) {
        return L"This pack ran out of memory (" + record.message + L").\n"
               L"The console has about 5 GB for everything, so very large packs cannot load.";
    }
    if (record.exception.find(L"unknown_") != std::wstring::npos) {
        return L"Nothing readable was left behind, so there is no diagnosis for this one.";
    }
    if (!record.message.empty()) return record.message;
    return record.exception;
}

static std::wstring CrashTraceText(const telemetry::CrashRecord& record) {
    std::wstring text = record.exception;
    if (!record.message.empty()) text += L"\n" + record.message;
    text += L"\n";
    for (const std::wstring& frame : record.frames) {
        text += L"\n  at " + frame;
    }
    if (record.frames.empty()) text += L"\nNo stack trace was recovered.";
    text += L"\n\nfingerprint " + record.fingerprint;
    text += L"\nbuild " + record.launcherBuild + L", " + record.mcVersion + L" " + record.loader;
    if (!record.zip.empty()) {
        text += L"\n\nThe full logs are zipped at:\n" + record.zip +
            L"\nOpen Remote Files on the main menu to read it on a phone or PC.";
    }
    return text;
}

static void ShowCrashScreen(ICoreWindow* window, AuthScreenRenderer* renderer, AuthUiState& state) {
    const telemetry::CrashRecord record = telemetry::ReadLastCrash();
    if (!record.found) return;

    WriteLogF(L"Crash screen shown for %s, repeat %d",
        record.fingerprint.c_str(), record.repeatCount);

    const bool showConsent =
        telemetry::Configured() && telemetry::Consent() == telemetry::ConsentState::Unanswered;

    const bool wasShowingMenu = state.showMainMenu;
    state.showMainMenu = false;
    state.showModsPage = false;
    state.showRemoteFiles = false;
    state.showDeviceCode = false;
    state.showCrashScreen = true;
    state.crashHeadline = CrashHeadline(record);
    state.crashSuspectLine = CrashSuspectLine(record);
    state.crashTrace = CrashTraceText(record);
    state.crashConsentPayload = telemetry::ConsentPayloadPreview(record);
    state.crashAskConsent = showConsent;
    state.crashDetailsOpen = false;
    state.crashDetailScroll = 0;
    state.crashSelected = 0;
    state.crashButtonCount = showConsent ? 3 : 2;
    state.crashFootnote = showConsent
        ? L"You can change this later, and reading the crash never sends anything."
        : L"Press B or select Dismiss to carry on.";

    bool leftWas = false;
    bool rightWas = false;
    bool selectWas = false;
    bool backWas = false;
    bool upWas = false;
    bool downWas = false;

    while (true) {
        state.animation = static_cast<float>((GetTickCount64() % 100000) / 1000.0);
        RenderAuth(renderer, state);

        LauncherMouse& mouse = LauncherMouseInstance();
        int clicked = -1;
        if (mouse.Visible() && mouse.TakeClick()) {
            const int hit = renderer->HitTest(mouse.X(), mouse.Y());
            if (hit >= launchhit::kCrashButtonBase && hit < launchhit::kCrashButtonBase + 3) {
                clicked = hit - launchhit::kCrashButtonBase;
            }
        }

        const bool leftDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Left,
            ABI::Windows::System::VirtualKey_GamepadDPadLeft,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickLeft
        });
        const bool rightDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Right,
            ABI::Windows::System::VirtualKey_GamepadDPadRight,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickRight
        });
        const bool upDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Up,
            ABI::Windows::System::VirtualKey_GamepadDPadUp,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickUp
        });
        const bool downDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Down,
            ABI::Windows::System::VirtualKey_GamepadDPadDown,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickDown
        });
        const bool selectDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Enter,
            ABI::Windows::System::VirtualKey_Space,
            ABI::Windows::System::VirtualKey_GamepadA
        });
        const bool backDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Escape,
            ABI::Windows::System::VirtualKey_GamepadB
        });

        if (leftDown && !leftWas && state.crashButtonCount > 0) {
            state.crashSelected = (state.crashSelected + state.crashButtonCount - 1) % state.crashButtonCount;
        }
        if (rightDown && !rightWas && state.crashButtonCount > 0) {
            state.crashSelected = (state.crashSelected + 1) % state.crashButtonCount;
        }
        if (upDown && !upWas && state.crashDetailScroll > 0) --state.crashDetailScroll;
        if (downDown && !downWas) {
            const std::wstring& body = state.crashDetailsOpen
                ? state.crashTrace
                : state.crashConsentPayload;
            int lines = 1;
            for (const wchar_t ch : body) {
                if (ch == L'\n') ++lines;
            }
            if (state.crashDetailScroll < lines - 4) ++state.crashDetailScroll;
        }

        if (backDown && !backWas) break;

        const int pressed = clicked >= 0 ? clicked : ((selectDown && !selectWas) ? state.crashSelected : -1);
        if (pressed < 0) {
            leftWas = leftDown;
            rightWas = rightDown;
            upWas = upDown;
            downWas = downDown;
            selectWas = selectDown;
            backWas = backDown;
            std::this_thread::sleep_for(std::chrono::milliseconds(16));
            continue;
        }

        if (state.crashAskConsent) {
            if (pressed == 0) {
                telemetry::SendLastCrashOnce(record);
                state.crashFootnote = L"Sending this one report. Reporting stays off.";
            } else if (pressed == 1) {
                if (telemetry::SetConsent(telemetry::ConsentState::Always)) {
                    telemetry::SendLastCrashOnce(record);
                    telemetry::FlushQueueAsync();
                    state.crashFootnote = L"Reporting is on. Turn it off any time from Settings.";
                } else {
                    state.crashFootnote = L"Reporting could not be turned on. Nothing was sent.";
                }
            } else {
                if (telemetry::SetConsent(telemetry::ConsentState::Never)) {
                    telemetry::ClearQueue();
                    state.crashFootnote = L"Nothing will be sent. Crashes are still explained here.";
                } else {
                    state.crashFootnote = L"Reporting could not be turned off.";
                }
            }
            state.crashAskConsent = false;
            state.crashSelected = 0;
            state.crashButtonCount = 2;
            state.crashDetailScroll = 0;
        } else if (pressed == 0) {
            state.crashDetailsOpen = !state.crashDetailsOpen;
            state.crashDetailScroll = 0;
        } else {
            break;
        }

        leftWas = leftDown;
        rightWas = rightDown;
        upWas = upDown;
        downWas = downDown;
        selectWas = selectDown;
        backWas = backDown;
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }

    telemetry::ClearLastCrash();

    // wait for release before the menu resets its edge detection
    while (AnyVirtualKeyDown(window, {
        ABI::Windows::System::VirtualKey_Enter,
        ABI::Windows::System::VirtualKey_Space,
        ABI::Windows::System::VirtualKey_GamepadA,
        ABI::Windows::System::VirtualKey_Escape,
        ABI::Windows::System::VirtualKey_GamepadB
    })) {
        RenderAuth(renderer, state);
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }

    state.showCrashScreen = false;
    state.showMainMenu = wasShowingMenu;
    WriteLog(L"Crash screen dismissed");
}

static void ShowSettingsPage(ICoreWindow* window, AuthScreenRenderer* renderer, AuthUiState& state) {
    constexpr int kSettingsRows = 4;
    WriteLog(L"Settings page opened");

    state.showMainMenu = false;
    state.showModsPage = false;
    state.showRemoteFiles = false;
    state.showDeviceCode = false;
    state.showSettings = true;
    state.settingsSelected = 0;
    state.settingsNote.clear();
    state.settingsConfigured = telemetry::Configured();
    state.settingsReportingOn = telemetry::ConsentGranted();
    state.settingsInstallId = telemetry::InstallIdText();
    state.settingsModSource = modsource::Current();
    state.settingsHighlightColor = installedhighlight::CurrentIndex();
    state.settingsCurseForgeKeyHint = modsource::CurseForgeKeyHint();

    bool upWas = false;
    bool downWas = false;
    bool selectWas = false;
    bool backWas = false;

    while (true) {
        state.animation = static_cast<float>((GetTickCount64() % 100000) / 1000.0);
        RenderAuth(renderer, state);

        LauncherMouse& mouse = LauncherMouseInstance();
        int clicked = -1;
        bool clickedBack = false;
        if (mouse.Visible() && mouse.TakeClick()) {
            const int hit = renderer->HitTest(mouse.X(), mouse.Y());
            if (hit == launchhit::kBack) clickedBack = true;
            if (hit >= launchhit::kSettingsRowBase && hit < launchhit::kSettingsRowBase + kSettingsRows) {
                clicked = hit - launchhit::kSettingsRowBase;
            }
        }

        const bool upDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Up,
            ABI::Windows::System::VirtualKey_GamepadDPadUp,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickUp
        });
        const bool downDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Down,
            ABI::Windows::System::VirtualKey_GamepadDPadDown,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickDown
        });
        const bool selectDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Enter,
            ABI::Windows::System::VirtualKey_Space,
            ABI::Windows::System::VirtualKey_GamepadA
        });
        const bool backDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Escape,
            ABI::Windows::System::VirtualKey_GamepadB
        });

        if (upDown && !upWas) {
            state.settingsSelected = (state.settingsSelected + kSettingsRows - 1) % kSettingsRows;
        }
        if (downDown && !downWas) {
            state.settingsSelected = (state.settingsSelected + 1) % kSettingsRows;
        }

        if ((backDown && !backWas) || clickedBack) break;

        const int pressed = clicked >= 0 ? clicked : ((selectDown && !selectWas) ? state.settingsSelected : -1);
        if (pressed == 0) {
            const bool turnOn = !state.settingsReportingOn;
            if (telemetry::SetConsent(turnOn ? telemetry::ConsentState::Always : telemetry::ConsentState::Never)) {
                state.settingsReportingOn = turnOn;
                if (turnOn) {
                    telemetry::FlushQueueAsync();
                    state.settingsNote = L"Reporting is on. Anything waiting will be retried.";
                } else {
                    telemetry::ClearQueue();
                    state.settingsNote = L"Reporting is off. Pending reports were deleted.";
                }
            } else {
                state.settingsNote = turnOn
                    ? L"Reporting could not be turned on."
                    : L"Reporting could not be turned off.";
            }
        } else if (pressed == 1) {
            if (telemetry::ResetInstallId()) {
                state.settingsInstallId = telemetry::InstallIdText();
                state.settingsNote = L"A new reporting id was created.";
            } else {
                state.settingsNote = L"The reporting id could not be reset.";
            }
        } else if (pressed == 2) {
            const ModSource next = state.settingsModSource == ModSource::CurseForge
                ? ModSource::Modrinth
                : ModSource::CurseForge;
            if (modsource::SetCurrent(next)) {
                state.settingsModSource = next;
                state.settingsCurseForgeKeyHint = modsource::CurseForgeKeyHint();
                if (next == ModSource::CurseForge && state.settingsCurseForgeKeyHint.empty()) {
                    state.settingsNote = L"CurseForge selected, but no API key is set. Add one in Remote Files.";
                } else {
                    state.settingsNote = std::wstring(L"Mods will come from ") +
                        modsource::DisplayName(next) + L".";
                }
            } else {
                state.settingsNote = L"The mod source could not be changed.";
            }
        } else if (pressed == 3) {
            const int next = (state.settingsHighlightColor + 1) % installedhighlight::kCount;
            if (installedhighlight::SetIndex(next)) {
                state.settingsHighlightColor = next;
                state.settingsNote = std::wstring(L"Installed mod highlight: ") + installedhighlight::Name(next);
            } else {
                state.settingsNote = L"Could not save highlight color.";
            }
        }

        upWas = upDown;
        downWas = downDown;
        selectWas = selectDown;
        backWas = backDown;
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }

    state.showSettings = false;
    state.showMainMenu = true;
    state.status = telemetry::ConsentGranted()
        ? L"Crash reporting is on"
        : L"Crash reporting is off";
    state.detail = L"";
    WriteLog(L"Settings page closed");
}


// Offline launcher identities are UI metadata only, never Minecraft credentials.
static std::wstring LocalIdsFile() {
    return GetLocalStateDir() + L"\\accounts\\local_ids.txt";
}
static void LoadLocalIds(AuthUiState& s) {
    s.localNames.clear();
    s.localActive = -1;
    s.localCursor = -1;
    std::wstring raw;
    if (!ReadTextFile(LocalIdsFile(), raw) || raw.size() > 2048) return;
    size_t pos = raw.find(L'\n');
    if (pos == std::wstring::npos) return;
    const std::wstring active = TrimWhitespace(raw.substr(0, pos));
    ++pos;
    while (pos < raw.size() && s.localNames.size() < 12) {
        size_t end = raw.find(L'\n', pos);
        std::wstring name = TrimWhitespace(raw.substr(pos, end == std::wstring::npos ? std::wstring::npos : end - pos));
        if (!name.empty() && name.size() <= 24 &&
            name.find_first_of(L"\\/:*?\"<>|\r\t") == std::wstring::npos &&
            std::find(s.localNames.begin(), s.localNames.end(), name) == s.localNames.end())
            s.localNames.push_back(name);
        if (end == std::wstring::npos) break;
        pos = end + 1;
    }
    for (int i = 0; i < static_cast<int>(s.localNames.size()); ++i)
        if (s.localNames[i] == active) s.localActive = i;
    s.localCursor = s.localActive >= 0 ? s.localActive : (s.localNames.empty() ? -1 : 0);
}
static bool SaveLocalIds(const AuthUiState& s) {
    if (!EnsureDirectoryTree(GetLocalStateDir() + L"\\accounts")) return false;
    std::wstring body = (s.localActive >= 0 && s.localActive < static_cast<int>(s.localNames.size()))
        ? s.localNames[s.localActive] : L"";
    body += L"\n";
    for (const auto& n : s.localNames) body += n + L"\n";
    return WriteTextFile(LocalIdsFile(), body);
}
static void LocalIdAction(AuthUiState& s, int kind) {
    // 0 select/create, 1 new, 2 previous, 3 next, 4 ask delete.
    const int count = static_cast<int>(s.localNames.size());
    if (kind == 1 || (kind == 0 && count == 0)) {
        if (count >= 12) { s.accountsMessage = L"Maximum 12 local identities."; return; }
        int n = 1;
        std::wstring name;
        do { name = L"Local " + std::to_wstring(n++); }
        while (std::find(s.localNames.begin(), s.localNames.end(), name) != s.localNames.end());
        s.localNames.push_back(name);
        s.localCursor = static_cast<int>(s.localNames.size()) - 1;
        s.localActive = s.localCursor;
        s.localDeletePending = false;
        s.accountsMessage = SaveLocalIds(s) ? L"Local identity saved (launcher only)." : L"Could not save identity.";
        return;
    }
    if (count == 0) { s.accountsMessage = L"Press A to create a local identity."; return; }
    if (s.localCursor < 0 || s.localCursor >= count) s.localCursor = 0;
    if (kind == 2 || kind == 3) {
        s.localCursor = (s.localCursor + count + (kind == 2 ? -1 : 1)) % count;
        s.localDeletePending = false;
        s.accountsMessage = L"A Select  |  X New  |  Y Delete";
        return;
    }
    if (kind == 4) {
        s.localDeletePending = true;
        s.accountsMessage = L"Delete selected local identity? A Confirm / B Cancel";
        return;
    }
    if (s.localDeletePending) {
        const int old = s.localCursor;
        s.localNames.erase(s.localNames.begin() + old);
        s.localActive = s.localActive == old ? -1 : (s.localActive > old ? s.localActive - 1 : s.localActive);
        s.localCursor = s.localNames.empty() ? -1 : (std::min)(old, static_cast<int>(s.localNames.size()) - 1);
        s.localDeletePending = false;
        s.accountsMessage = SaveLocalIds(s) ? L"Local identity deleted." : L"Could not save deletion.";
        return;
    }
    s.localActive = s.localCursor;
    s.accountsMessage = SaveLocalIds(s) ? L"Local identity selected. Minecraft is not unlocked." : L"Could not save selection.";
}
static void OpenAccounts(AuthUiState& s) {
    s.showAccounts = true;
    s.selectedAccountIndex = 0;
    s.localDeletePending = false;
    LoadLocalIds(s);
    s.accountsMessage = L"A Select  |  Local: X New / Y Delete  |  B Back";
}


// Dedicated Xbox CoreText session; no sharing with the Mods search edit context.
class LocalIdentityKeyboard {
public:
    ~LocalIdentityKeyboard() { End(); }

    bool Begin(ICoreWindow* rawWindow, const std::wstring& initial) {
        try {
            winrt::copy_from_abi(window_, rawWindow);
            value_ = initial;
            caret_ = static_cast<int>(value_.size());
            using namespace winrt::Windows::UI::Text::Core;
            auto manager = CoreTextServicesManager::GetForCurrentView();
            edit_ = manager.CreateEditContext();
            edit_.InputPaneDisplayPolicy(CoreTextInputPaneDisplayPolicy::Manual);
            edit_.InputScope(CoreTextInputScope::Search);
            textToken_ = edit_.TextRequested([this](auto&&, CoreTextTextRequestedEventArgs const& args) {
                auto range = args.Request().Range();
                const int n = static_cast<int>(value_.size());
                const int a = (std::max)(0, (std::min)(range.StartCaretPosition, n));
                const int b = (std::max)(a, (std::min)(range.EndCaretPosition, n));
                args.Request().Text(winrt::hstring(std::wstring_view(value_).substr(a, b - a)));
            });
            selectToken_ = edit_.SelectionRequested([this](auto&&, CoreTextSelectionRequestedEventArgs const& args) {
                args.Request().Selection(CoreTextRange{ caret_, caret_ });
            });
            updateToken_ = edit_.TextUpdating([this](auto&&, CoreTextTextUpdatingEventArgs const& args) {
                const auto range = args.Range();
                const int n = static_cast<int>(value_.size());
                const int a = (std::max)(0, (std::min)(range.StartCaretPosition, n));
                const int b = (std::max)(a, (std::min)(range.EndCaretPosition, n));
                std::wstring inserted;
                for (const wchar_t ch : std::wstring_view(args.Text())) {
                    if (ch == L'\r' || ch == L'\n') { submitted_ = true; continue; }
                    if ((ch >= L'A' && ch <= L'Z') ||
                        (ch >= L'a' && ch <= L'z') ||
                        (ch >= L'0' && ch <= L'9') ||
                        ch == L' ' || ch == L'_' || ch == L'-')
                        inserted.push_back(ch);
                }
                const size_t remaining = 24 - (value_.size() - static_cast<size_t>(b - a));
                if (inserted.size() > remaining) inserted.resize(remaining);
                value_ = value_.substr(0, a) + inserted + value_.substr(b);
                caret_ = (std::max)(0, (std::min)(args.NewSelection().EndCaretPosition,
                    static_cast<int>(value_.size())));
                args.Result(CoreTextTextUpdatingResult::Succeeded);
            });
            selectUpdateToken_ = edit_.SelectionUpdating([this](auto&&, CoreTextSelectionUpdatingEventArgs const& args) {
                caret_ = (std::max)(0, (std::min)(args.Selection().EndCaretPosition,
                    static_cast<int>(value_.size())));
                args.Result(CoreTextSelectionUpdatingResult::Succeeded);
            });
            layoutToken_ = edit_.LayoutRequested([this](auto&&, CoreTextLayoutRequestedEventArgs const& args) {
                auto bounds = args.Request().LayoutBounds();
                const auto rect = window_.Bounds();
                bounds.TextBounds(rect);
                bounds.ControlBounds(rect);
            });
            keyToken_ = window_.KeyDown([this](auto&&, winrt::Windows::UI::Core::KeyEventArgs const& args) {
                if (!active_) return;
                if (args.VirtualKey() == winrt::Windows::System::VirtualKey::Enter) {
                    submitted_ = true;
                    args.Handled(true);
                } else if (args.VirtualKey() == winrt::Windows::System::VirtualKey::Back) {
                    if (caret_ > 0 && caret_ <= static_cast<int>(value_.size())) {
                        value_.erase(static_cast<size_t>(caret_ - 1), 1);
                        --caret_;
                        try {
                            using namespace winrt::Windows::UI::Text::Core;
                            edit_.NotifyTextChanged(CoreTextRange{ caret_, caret_ + 1 }, 0,
                                CoreTextRange{ caret_, caret_ });
                            edit_.NotifySelectionChanged(CoreTextRange{ caret_, caret_ });
                        } catch (...) {}
                    }
                    args.Handled(true);
                }
            });
            try { pane_ = winrt::Windows::UI::ViewManagement::InputPane::GetForCurrentView(); } catch (...) {}
            active_ = true;
            edit_.NotifyFocusEnter();
            edit_.NotifyTextChanged(CoreTextRange{ 0, 0 }, caret_, CoreTextRange{ caret_, caret_ });
            edit_.NotifySelectionChanged(CoreTextRange{ caret_, caret_ });
            if (pane_) pane_.TryShow();
            return true;
        } catch (const winrt::hresult_error& e) {
            WriteLogF(L"Local identity CoreText failed hr=0x%08X", static_cast<unsigned>(e.code()));
            End();
            return false;
        } catch (...) {
            End();
            return false;
        }
    }
    void End() {
        active_ = false;
        if (pane_) { try { pane_.TryHide(); } catch (...) {} }
        if (edit_) { try { edit_.NotifyFocusLeave(); } catch (...) {} }
        if (window_ && keyToken_.value) { try { window_.KeyDown(keyToken_); } catch (...) {} }
        if (edit_) {
            try {
                if (textToken_.value) edit_.TextRequested(textToken_);
                if (selectToken_.value) edit_.SelectionRequested(selectToken_);
                if (updateToken_.value) edit_.TextUpdating(updateToken_);
                if (selectUpdateToken_.value) edit_.SelectionUpdating(selectUpdateToken_);
                if (layoutToken_.value) edit_.LayoutRequested(layoutToken_);
            } catch (...) {}
        }
        pane_ = nullptr;
        edit_ = nullptr;
        window_ = nullptr;
    }
    const std::wstring& Text() const { return value_; }
    bool Submitted() const { return submitted_; }
    bool KeyboardVisible() const {
        if (!pane_) return false;
        try { return pane_.Visible(); } catch (...) { return false; }
    }
private:
    winrt::Windows::UI::Core::CoreWindow window_{nullptr};
    winrt::Windows::UI::Text::Core::CoreTextEditContext edit_{nullptr};
    winrt::Windows::UI::ViewManagement::InputPane pane_{nullptr};
    winrt::event_token textToken_{};
    winrt::event_token selectToken_{};
    winrt::event_token updateToken_{};
    winrt::event_token selectUpdateToken_{};
    winrt::event_token layoutToken_{};
    winrt::event_token keyToken_{};
    std::wstring value_;
    int caret_ = 0;
    bool active_ = false;
    bool submitted_ = false;
};

static bool IsValidLocalIdentityName(const std::wstring& name, const AuthUiState& state,
                                     int renamingIndex, std::wstring& problem) {
    if (name.empty() || name.size() > 24) {
        problem = L"Name must be 1-24 characters.";
        return false;
    }
    for (const wchar_t ch : name) {
        if (!((ch >= L'A' && ch <= L'Z') || (ch >= L'a' && ch <= L'z') ||
              (ch >= L'0' && ch <= L'9') || ch == L' ' || ch == L'_' || ch == L'-')) {
            problem = L"Only letters, numbers, spaces, _ and - are supported.";
            return false;
        }
    }
    for (int i = 0; i < static_cast<int>(state.localNames.size()); ++i) {
        if (i != renamingIndex && ToLowerW(state.localNames[i]) == ToLowerW(name)) {
            problem = L"An identity with that name already exists.";
            return false;
        }
    }
    return true;
}

static void EditLocalIdentityName(ICoreWindow* window, AuthScreenRenderer* renderer,
                                  AuthUiState& state, bool rename) {
    const int index = state.localCursor;
    if (rename && (index < 0 || index >= static_cast<int>(state.localNames.size()))) {
        state.accountsMessage = L"Choose a saved local identity before renaming.";
        return;
    }
    if (!rename && state.localNames.size() >= 12) {
        state.accountsMessage = L"Maximum 12 local identities.";
        return;
    }
    state.localNameEditing = true;
    state.localNameRenaming = rename;
    state.localNameDraft = rename ? state.localNames[static_cast<size_t>(index)] : L"";
    LocalIdentityKeyboard keyboard;
    if (!keyboard.Begin(window, state.localNameDraft)) {
        state.localNameEditing = false;
        state.accountsMessage = L"Xbox keyboard unavailable. No changes saved.";
        return;
    }

    bool priorA = true;
    bool priorB = true;
    bool canceled = false;
    while (true) {
        ProcessAuthUiEvents();
        state.localNameDraft = keyboard.Text();
        RenderAuth(renderer, state);
        const bool a = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Enter,
            ABI::Windows::System::VirtualKey_GamepadA
        });
        const bool b = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Escape,
            ABI::Windows::System::VirtualKey_GamepadB
        });
        if (b && !priorB && !keyboard.KeyboardVisible()) {
            canceled = true;
            break;
        }
        if (keyboard.Submitted() || (a && !priorA && !keyboard.KeyboardVisible())) break;
        priorA = a;
        priorB = b;
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }
    keyboard.End();
    state.localNameEditing = false;
    if (canceled) {
        state.accountsMessage = L"Name editing cancelled.";
        return;
    }
    const std::wstring desired = TrimWhitespace(state.localNameDraft);
    std::wstring issue;
    if (!IsValidLocalIdentityName(desired, state, rename ? index : -1, issue)) {
        state.accountsMessage = issue;
        return;
    }
    const auto beforeNames = state.localNames;
    const int beforeActive = state.localActive;
    const int beforeCursor = state.localCursor;
    if (rename) {
        state.localNames[static_cast<size_t>(index)] = desired;
    } else {
        state.localNames.push_back(desired);
        state.localCursor = static_cast<int>(state.localNames.size()) - 1;
        state.localActive = state.localCursor;
    }
    if (!SaveLocalIds(state)) {
        state.localNames = beforeNames;
        state.localActive = beforeActive;
        state.localCursor = beforeCursor;
        state.accountsMessage = L"Failed to write local identity file.";
    } else {
        state.accountsMessage = rename ? L"Local identity renamed." : L"Local identity created.";
    }
}

MainMenuAction ShowMainMenu(ICoreWindow* window, const LaunchAuthConfig& authConfig, const std::wstring& runtimeRoot,
                            bool localSession, const std::wstring& localName) {
    AuthScreenRenderer rendererInstance;
    AuthScreenRenderer* renderer = nullptr;
    if (rendererInstance.Initialize(window)) {
        renderer = &rendererInstance;
    } else {
        WriteLog(L"Main menu renderer failed");
        return localSession ? MainMenuAction::ReturnToSignIn : MainMenuAction::Play;
    }

    AuthUiState state;
    state.title = L"LegacyForge Launcher";
    state.showDeviceCode = false;
    state.showMainMenu = true;
    state.isLocalSession = localSession;
    state.homePlayerName = localSession ? localName : a2w(authConfig.username.c_str());
    state.status = localSession ? L"Local launcher session - Minecraft Play unavailable" :
        L"Signed in as " + state.homePlayerName;
    EnsureProfilesInitialized(runtimeRoot);
    auto refreshHomeSummary = [&]() {
        const std::wstring activeId = GetActiveProfileId(runtimeRoot);
        const Profile activeProfile = GetProfileById(runtimeRoot, activeId);
        const LaunchTarget activeTarget = ResolveProfileTarget(runtimeRoot, activeProfile);
        state.homeProfileName = activeProfile.name;
        state.homeTargetText = TargetProfileText(activeTarget);
        state.homeModCount = ProfileModCount(runtimeRoot, activeId);
    };
    refreshHomeSummary();
    // The selected offline identity can change while Accounts is open. Home's
    // display name must follow that selection without restarting the launcher.
    // This is presentation metadata only and never changes Microsoft auth.
    auto syncLocalHomeIdentity = [&]() {
        if (!localSession) return;
        if (state.localActive >= 0 &&
            state.localActive < static_cast<int>(state.localNames.size()))
            state.homePlayerName = state.localNames[static_cast<size_t>(state.localActive)];
        else
            state.homePlayerName = L"Local Launcher";
    };

    int selected = 0;
    bool upWasDown = false;
    bool downWasDown = false;
    bool selectWasDown = false;
    bool accountBackWasDown = false;
    bool localXWasDown = false;
    bool localYWasDown = false;
    bool localLeftWasDown = false;
    bool localRightWasDown = false;
    bool localRenameWasDown = false;

    ShowCrashScreen(window, renderer, state);

    WriteLog(L"Main menu opened");
    while (true) {
        LauncherMouse& mouse = LauncherMouseInstance();
        int hovered = -1;
        if (mouse.Visible()) {
            for (int i = 0; i < renderer->MainMenuItemCount(); ++i) {
                D2D1_RECT_F r;
                if (renderer->MainMenuItemRect(i, r) &&
                    mouse.X() >= r.left && mouse.X() <= r.right &&
                    mouse.Y() >= r.top && mouse.Y() <= r.bottom) {
                    hovered = i;
                }
            }
            if (hovered >= 0) {
                selected = hovered;
            }
        }
        if (state.showAccounts) {
            state.animation = static_cast<float>((GetTickCount64() % 100000) / 1000.0);
            RenderAuth(renderer, state);
            const bool goUp = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Up,
                ABI::Windows::System::VirtualKey_GamepadDPadUp
            });
            const bool goDown = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Down,
                ABI::Windows::System::VirtualKey_GamepadDPadDown
            });
            const bool goSelect = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Enter,
                ABI::Windows::System::VirtualKey_GamepadA
            });
            const bool goBack = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Escape,
                ABI::Windows::System::VirtualKey_GamepadB
            });
            if (goUp && !upWasDown) {
                state.selectedAccountIndex = (state.selectedAccountIndex + 4) % 5;
            }
            if (goDown && !downWasDown) {
                state.selectedAccountIndex = (state.selectedAccountIndex + 1) % 5;
            }
            const bool localX = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_GamepadX
            });
            const bool localY = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_GamepadY
            });
            const bool localLeft = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Left,
                ABI::Windows::System::VirtualKey_GamepadDPadLeft
            });
            const bool localRight = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Right,
                ABI::Windows::System::VirtualKey_GamepadDPadRight
            });
            const bool localRename = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_GamepadRightShoulder,
                ABI::Windows::System::VirtualKey_F2
            });
            if (state.selectedAccountIndex == 1 && !state.localDeletePending) {
                if (localX && !localXWasDown) EditLocalIdentityName(window, renderer, state, false);
                if (localRename && !localRenameWasDown) EditLocalIdentityName(window, renderer, state, true);
                if (localY && !localYWasDown) LocalIdAction(state, 4);
                if (localLeft && !localLeftWasDown) LocalIdAction(state, 2);
                if (localRight && !localRightWasDown) LocalIdAction(state, 3);
            }
            if (goSelect && !selectWasDown) {
                if (state.selectedAccountIndex == 1) {
                    if (state.localDeletePending || !state.localNames.empty())
                        LocalIdAction(state, 0);
                    else
                        EditLocalIdentityName(window, renderer, state, false);
                } else switch (state.selectedAccountIndex) {
                case 0:
                    state.accountsMessage = L"Microsoft account connected. Use Sign out on Home to switch.";
                    break;
                case 2:
                    state.accountsMessage = L"Ely.by integration is not implemented yet.";
                    break;
                case 3:
                    state.accountsMessage = L"Get Minecraft Java Edition from minecraft.net.";
                    break;
                default:
                    state.accountsMessage = L"Only Microsoft verifies ownership in this build.";
                    break;
                }
            }
            // Covers newly created, renamed, selected and deleted identities.
            // Do not confuse cursor movement with an actual active selection.
            syncLocalHomeIdentity();
            if (goBack && !accountBackWasDown) {
                if (state.localDeletePending) {
                    state.localDeletePending = false;
                    state.accountsMessage = L"Delete cancelled.";
                } else {
                    state.showAccounts = false;
                    state.showMainMenu = true;
                }
            }
            localXWasDown = localX;
            localYWasDown = localY;
            localLeftWasDown = localLeft;
            localRightWasDown = localRight;
            localRenameWasDown = localRename;
            upWasDown = goUp;
            downWasDown = goDown;
            selectWasDown = goSelect;
            accountBackWasDown = goBack;
            std::this_thread::sleep_for(std::chrono::milliseconds(16));
            continue;
        }
        // Release previous Account-panel keys before accepting Home input.
        accountBackWasDown = false;
        state.selectedMenuIndex = selected;
        state.animation = static_cast<float>((GetTickCount64() % 100000) / 1000.0);
        RenderAuth(renderer, state);

        const bool upDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Up,
            ABI::Windows::System::VirtualKey_GamepadDPadUp,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickUp
        });
        const bool downDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Down,
            ABI::Windows::System::VirtualKey_GamepadDPadDown,
            ABI::Windows::System::VirtualKey_GamepadLeftThumbstickDown
        });
        const bool selectDown = AnyVirtualKeyDown(window, {
            ABI::Windows::System::VirtualKey_Enter,
            ABI::Windows::System::VirtualKey_Space,
            ABI::Windows::System::VirtualKey_GamepadA
        });

        if (upDown && !upWasDown) {
            selected = (selected + kMainMenuItems - 1) % kMainMenuItems;
            state.detail = L"";
        }
        if (downDown && !downWasDown) {
            selected = (selected + 1) % kMainMenuItems;
            state.detail = L"";
        }
        const bool mouseClicked = mouse.TakeClick();
        if ((selectDown && !selectWasDown) || (mouseClicked && hovered >= 0)) {
            if (selected == 0) {
                if (localSession) {
                    state.detail = L"Sign in with Microsoft to verify Minecraft ownership.";
                    selectWasDown = selectDown;
                    continue;
                }
                WriteLog(L"Main menu: Play selected");
                StopRemoteFileServer();
                return MainMenuAction::Play;
            }
            if (selected == 1) {
                WriteLog(L"Main menu: Mods selected");
                ShowModsPage(window, renderer, state, runtimeRoot);
                refreshHomeSummary();
            } else if (selected == 2) {
                WriteLog(L"Main menu: Accounts selected");
                state.showMainMenu = false;
                OpenAccounts(state);
                syncLocalHomeIdentity();
            } else if (selected == 3) {
                WriteLog(L"Main menu: Remote files selected");
                ShowRemoteFilesPage(window, renderer, state, runtimeRoot);
            } else if (selected == 4) {
                WriteLog(L"Main menu: Settings selected");
                ShowSettingsPage(window, renderer, state);
            } else if (selected == 5) {
                if (localSession) {
                    state.detail = L"Repair requires a Microsoft Minecraft session.";
                    selectWasDown = selectDown;
                    continue;
                }
                WriteLog(L"Main menu: Repair downloads selected");
                StopRemoteFileServer();
                state.status = L"Repairing downloaded files";
                state.detail = L"Downloaded Minecraft files will be rechecked";
                RenderAuth(renderer, state);
                SleepWithAuthUi(renderer, state, 350);
                return MainMenuAction::RepairDownloads;
            } else {
                WriteLog(L"Main menu: Sign out selected");
                StopRemoteFileServer();
                state.status = localSession ? L"Leaving local launcher" : L"Signing out";
                state.detail = localSession ? L"Return to sign-in" : L"Clearing saved Microsoft session";
                RenderAuth(renderer, state);
                SleepWithAuthUi(renderer, state, 350);
                return localSession ? MainMenuAction::ReturnToSignIn : MainMenuAction::SignOut;
            }
        }

        upWasDown = upDown;
        downWasDown = downDown;
        selectWasDown = selectDown;
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }
}

bool ResolveLaunchAuthConfig(ICoreWindow* window, LaunchAuthConfig& out, std::wstring& localName) {
    localName.clear();
    AuthScreenRenderer rendererInstance;
    AuthScreenRenderer* renderer = nullptr;
    if (rendererInstance.Initialize(window)) {
        renderer = &rendererInstance;
    }

    AuthUiState state;
    state.title = L"Signing in";
    state.showDeviceCode = false;
    state.progress = 0.12f;
    state.verificationUri = L"microsoft.com/link";
    state.status = L"Checking saved Microsoft session";
    RenderAuth(renderer, state);

    const std::string savedRefreshToken = LoadRefreshToken();
    if (!savedRefreshToken.empty()) {
        MicrosoftTokenResponse refreshed;
        std::string error;
        if (RefreshMicrosoftToken(savedRefreshToken, refreshed, error)) {
            if (!refreshed.refreshToken.empty()) {
                SaveRefreshToken(refreshed.refreshToken);
            }
            state.status = L"Verifying Minecraft ownership";
            state.detail = L"Using saved Microsoft session";
            state.progress = 0.58f;
            RenderAuth(renderer, state);
            if (BuildMinecraftAuth(refreshed.accessToken, out, error)) {
                state.status = L"Signed in as " + a2w(out.username.c_str());
                state.detail = L"";
                state.progress = 1.0f;
                RenderAuth(renderer, state);
                SleepWithAuthUi(renderer, state, 700);
                return true;
            }
        }

        WriteLogF(L"Saved auth failed: %s", a2w(error.c_str()).c_str());
        ClearRefreshToken();
    }

    DeviceCodeResponse device;
    std::string error;
    if (!RequestDeviceCode(device, error)) {
        state.status = L"Microsoft sign-in failed";
        state.detail = a2w(error.c_str());
        state.isError = true;
        RenderAuth(renderer, state);
        SleepWithAuthUi(renderer, state, 5000);
        return false;
    }

    state.userCode = a2w(device.userCode.c_str());
    state.verificationUri = a2w(device.verificationUri.c_str());
    state.title = L"Microsoft sign-in";
    state.showDeviceCode = true;
    state.progress = -1.0f;
    state.status = L"Waiting for Microsoft sign-in";
    state.detail = L"Use the account that owns Minecraft Java Edition.";
    state.secondsRemaining = device.expiresIn;
    RenderAuth(renderer, state);

    // Allow controller-only browsing of account options during device-code polling.
    bool xWasDown = false;
    bool bWasDown = false;
    bool upWasDown = false;
    bool downWasDown = false;
    bool selectWasDown = false;
    bool localYWasDown = false;
    bool localLeftWasDown = false;
    bool localRightWasDown = false;
    bool localRenameWasDown = false;
    bool startWasDown = false;
    auto waitWithAccountOptions = [&](int milliseconds) {
        const auto start = std::chrono::steady_clock::now();
        while (std::chrono::duration_cast<std::chrono::milliseconds>(
                   std::chrono::steady_clock::now() - start).count() < milliseconds) {
            const bool x = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_X,
                ABI::Windows::System::VirtualKey_GamepadX
            });
            const bool back = AnyVirtualKeyDown(window, {
                ABI::Windows::System::VirtualKey_Escape,
                ABI::Windows::System::VirtualKey_GamepadB
            });
            if (x && !xWasDown && !state.showAccounts) {
                OpenAccounts(state);
            }
            if (state.showAccounts) {
                const bool start = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_GamepadMenu
                });
                if (start && !startWasDown && state.selectedAccountIndex == 1 &&
                    state.localActive >= 0 &&
                    state.localActive < static_cast<int>(state.localNames.size())) {
                    localName = state.localNames[static_cast<size_t>(state.localActive)];
                    state.showAccounts = false;
                    return;
                }
                startWasDown = start;
                const bool up = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_Up,
                    ABI::Windows::System::VirtualKey_GamepadDPadUp
                });
                const bool down = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_Down,
                    ABI::Windows::System::VirtualKey_GamepadDPadDown
                });
                const bool select = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_Enter,
                    ABI::Windows::System::VirtualKey_GamepadA
                });
                if (up && !upWasDown) state.selectedAccountIndex = (state.selectedAccountIndex + 4) % 5;
                if (down && !downWasDown) state.selectedAccountIndex = (state.selectedAccountIndex + 1) % 5;
                const bool left = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_Left,
                    ABI::Windows::System::VirtualKey_GamepadDPadLeft
                });
                const bool right = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_Right,
                    ABI::Windows::System::VirtualKey_GamepadDPadRight
                });
                const bool y = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_GamepadY
                });
                const bool rename = AnyVirtualKeyDown(window, {
                    ABI::Windows::System::VirtualKey_GamepadRightShoulder,
                    ABI::Windows::System::VirtualKey_F2
                });
                if (state.selectedAccountIndex == 1 && !state.localDeletePending) {
                    if (x && !xWasDown) EditLocalIdentityName(window, renderer, state, false);
                    if (rename && !localRenameWasDown) EditLocalIdentityName(window, renderer, state, true);
                    if (y && !localYWasDown) LocalIdAction(state, 4);
                    if (left && !localLeftWasDown) LocalIdAction(state, 2);
                    if (right && !localRightWasDown) LocalIdAction(state, 3);
                }
                if (select && !selectWasDown) {
                    if (state.selectedAccountIndex == 1) {
                        if (state.localDeletePending || !state.localNames.empty())
                            LocalIdAction(state, 0);
                        else
                            EditLocalIdentityName(window, renderer, state, false);
                    } else switch (state.selectedAccountIndex) {
                    case 0: state.accountsMessage = L"Press B to return to Microsoft sign-in."; break;
                    case 2: state.accountsMessage = L"Ely.by integration is coming later."; break;
                    case 3: state.accountsMessage = L"Minecraft Java information: minecraft.net"; break;
                    default: state.accountsMessage = L"Microsoft verifies Java Edition ownership."; break;
                    }
                }
                upWasDown = up;
                downWasDown = down;
                selectWasDown = select;
                localLeftWasDown = left;
                localRightWasDown = right;
                localYWasDown = y;
                localRenameWasDown = rename;
                if (back && !bWasDown) {
                    if (state.localDeletePending) {
                        state.localDeletePending = false;
                        state.accountsMessage = L"Delete cancelled.";
                    } else {
                        state.showAccounts = false;
                    }
                }
            } else {
                upWasDown = false;
                downWasDown = false;
                selectWasDown = false;
            }
            xWasDown = x;
            bWasDown = back;
            RenderAuth(renderer, state);
            std::this_thread::sleep_for(std::chrono::milliseconds(70));
        }
    };

    auto expiresAt = std::chrono::steady_clock::now() + std::chrono::seconds(device.expiresIn);
    int interval = device.interval;
    while (std::chrono::steady_clock::now() < expiresAt) {
        state.secondsRemaining = static_cast<int>(
            std::chrono::duration_cast<std::chrono::seconds>(expiresAt - std::chrono::steady_clock::now()).count());
        state.status = L"Waiting for Microsoft sign-in";
        state.detail = L"Use the account that owns Minecraft Java Edition.";
        waitWithAccountOptions(interval * 1000);
        if (!localName.empty()) return false;

        state.status = L"Checking sign-in";
        state.detail.clear();
        RenderAuth(renderer, state);

        DevicePollResult poll = PollDeviceToken(device.deviceCode);
        if (poll.status == DevicePollStatus::Pending) {
            continue;
        }
        if (poll.status == DevicePollStatus::SlowDown) {
            interval += 5;
            continue;
        }
        if (poll.status == DevicePollStatus::Failed) {
            state.status = L"Microsoft sign-in failed";
            state.detail = a2w(poll.error.c_str());
            state.isError = true;
            RenderAuth(renderer, state);
            SleepWithAuthUi(renderer, state, 7000);
            return false;
        }

        if (!poll.token.refreshToken.empty()) {
            SaveRefreshToken(poll.token.refreshToken);
        }

        state.status = L"Verifying Minecraft ownership";
        state.detail.clear();
        RenderAuth(renderer, state);

        if (BuildMinecraftAuth(poll.token.accessToken, out, error)) {
            state.status = L"Signed in as " + a2w(out.username.c_str());
            state.secondsRemaining = 0;
            state.detail.clear();
            RenderAuth(renderer, state);
            SleepWithAuthUi(renderer, state, 900);
            return true;
        }

        state.status = L"Minecraft sign-in failed";
        state.detail = a2w(error.c_str());
        state.isError = true;
        RenderAuth(renderer, state);
        SleepWithAuthUi(renderer, state, 8000);
        return false;
    }

    state.showAccounts = false;
    state.status = L"Microsoft sign-in expired";
    state.detail = L"Restart the app to request a new code.";
    state.isError = true;
    state.secondsRemaining = 0;
    RenderAuth(renderer, state);
    SleepWithAuthUi(renderer, state, 5000);
    return false;
}
