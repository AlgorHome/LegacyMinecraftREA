# LegacyForge UI V2 — design and implementation

> Status: Phase 1 (account screen) implemented on feature branch; Xbox runtime test pending.

## Goals

Legacy Launcher-inspired design for Xbox Series X|S with clear controller readability, Minecraft profile context, and a distinct LegacyForge identity. The first iteration changes only the sign-in presentation; it does **not** alter Microsoft OAuth/device polling, Java Edition entitlement checks, saved sessions, or the Java runtime.

## Auth screen V2 (implemented)

- LegacyForge masthead and Minecraft Java / Xbox identity.
- Two-column TV-safe layout: account code/URL/status on the left; Minecraft-themed native block motif and three instructions on the right.
- Large one-time device code and the verification URL supplied by Microsoft.
- Status and countdown driven by existing authentication state, with clear error/expiry messaging.
- No QR code, no unimplemented buttons, and no on-Xbox password entry.
- Sign-in is completed on another device at the displayed Microsoft link; the app continues to poll and enters the launcher after authentication.

### Existing actions retained

The launcher automatically polls for sign-in. Once signed in, it verifies account ownership and displays the normal launcher menu. If the code expires or the request fails, the existing flow reports the error and the app must be reopened for a new code. A controller-driven Retry action is a *future feature*, not part of this change.

## UI roadmap (not yet implemented)

1. **Home/dashboard:** account name, active profile, Minecraft version, mod loader, large Play area and Xbox-focus navigation. Preserve existing working menu actions.
2. **Profiles and versions:** select Fabric / Forge / NeoForge / vanilla profiles using the existing `profiles` and `launch/loaders` APIs.
3. **Mods:** integrate browse/install with clear warnings for unsupported native libraries and experimental targets.
4. **Settings:** input assistance, accessibility/focus indicators, download diagnostics and opt-in reporting.
5. **Artwork:** independently designed LegacyForge launcher icon, splash screen and dashboard background.

## Engineering ownership

| Area | Current location | Guidance |
| --- | --- | --- |
| Auth UI renderer | `MC.Xbox/ui/auth_screen.h` | QR-free Xbox-safe Direct2D layout |
| UI data model | `MC.Xbox/ui/auth_ui_state.h` | Keep device code, URL, status, expiry |
| Auth controller/orchestration | `MC.Xbox/ui/launcher_ui.cpp` | Preserve device flow; remove QR generation |
| Auth backend | `MC.Xbox/auth/minecraft_auth.cpp` | Leave untouched in Phase 1 |
| Static preview | `tools/ui-preview/ui_preview.cpp` | Waiting, expired and error states |

## Build and validation

From a **Windows development PC** with the Visual Studio C++ toolchain, Windows SDK and Java dependencies already configured:

```powershell
.\tools\ui-preview\render.ps1
.\build.ps1
```

Inspect `signin-device-code.png`, `signin-expired.png` and `signin-error.png` in `.local\ui-preview` (or the chosen `-OutDir`). These render previews; they do not prove Xbox compatibility.

### Xbox acceptance checklist

- New app package installs and launches on Series X Dev Mode.
- Screen clearly shows LegacyForge, code and the true Microsoft verification URL; no QR image.
- Text is not clipped at the console's display resolution and respects TV overscan.
- Countdown updates while authorization is pending; error and expiry messages are legible.
- Completing sign-in on a second device reaches the normal authenticated launcher menu.
- Existing saved sign-in, Minecraft entitlement checks and vanilla/Fabric launch continue to work.
- If a regression occurs, revert this UI-only change rather than modifying the authentication backend.

## Notes

Do not commit personal one-time sign-in codes, login tokens, or device-generated logs containing credentials. Existing third-party source credits and license obligations remain intact.
