# LegacyForge UI V2 — Home Dashboard and Accounts

Status: **Home V2 first implementation committed on a feature branch; PC preview and Xbox test pending.** Account manager and alternate account-provider implementation remain future work.

## Design principles

- Xbox Series X|S Developer Mode first: readable at 10-foot viewing distance, TV-safe margins, D-pad/controller-first focus, no hover-only actions.
- Legacy Launcher-inspired account chooser with original LegacyForge layout and green accent.
- Preserve the proven Microsoft device-code authorization and Java Edition entitlement verification as the default.
- Keep game profile selection separate from account identity; a local profile is not an authenticated Minecraft account.
- Never present unavailable account providers as working sign-in methods.

## Home dashboard

Layout: dark background, header with **LEGACYFORGE** and “Minecraft Java. Reforged for Xbox.”; left column active-profile card and navigation; right feature card with large **Play Minecraft** action and readiness status. Provide accessible focus borders and readable error messages.

Display only real state: authenticated Minecraft player name when known, actual active profile, Minecraft version, loader, mod count when available. Unknown values should show “Not selected” rather than fabricated data.

| Control | Behavior | Existing integration / implementation |
| --- | --- | --- |
| Play Minecraft (default focus) | Starts current target after ownership and runtime validation | Existing `MainMenuAction::Play` |
| Profiles | Navigate to existing profile manager; selecting a profile updates home summary | Existing Mods/Profiles functionality; dedicated route is new |
| Mods | Open mods browser and profile mod manager | Existing `MainMenuAction::Mods` |
| Accounts | Open new account manager; Microsoft account is initially the only real provider | New route; existing sign-in/sign-out preserved |
| Remote Files | Existing local-network transfer page | Existing `MainMenuAction::RemoteFiles` |
| Settings | Existing configuration screen | Existing `MainMenuAction::Settings` |
| Repair downloads | Existing repair operation | Existing `MainMenuAction::Repair` |
| Sign out | Clear authenticated session using existing logout handler and return to Microsoft sign-in | Existing `MainMenuAction::SignOut` |

### Xbox navigation

- D-pad up/down: move within navigation list; left/right: switch between navigation and primary Play/summary region.
- A: activate the focused action. B: back from subpage or cancel modal (never sign out inadvertently).
- The existing focus and hit-test implementation is the starting point; do not expose controller hints until corresponding input handlers exist.
- Focus must remain visible at all times, with a clear recovery target when a modal closes.
- Do not remap Play/Repair/Sign Out actions while merely changing the visual menu; migrate their identifiers and selection indices together.

## Accounts panel — Legacy Launcher-inspired

Entry: Home → Accounts → **Add Account**. An overlay uses two columns: saved accounts on left (when supported), account methods on right. Buttons should be large and controller-focusable. Back returns without changing authentication.

| Account option | UI label | Behavior / scope |
| --- | --- | --- |
| Microsoft | **Microsoft Account · Recommended** | Existing Microsoft device-code login, Xbox Live/XSTS/Minecraft token exchange and Java entitlement check. Default active provider. |
| Local | **Local Profile** | Create a display-name-only launcher profile for settings and UI testing. Must not create fake Microsoft/Xbox tokens or imply premium Java ownership. Disable authenticated Java game launching until a supported, legitimate launch mode is implemented and evaluated. |
| Ely.by | **Custom Skin Service (Ely.by)** | Future optional provider. Requires separate provider API research, user consent, secure token storage and an explicit support matrix. A skin provider is not proof of Minecraft Java ownership. Mark **Coming later**; do not fake sign-in. |
| Shop | **Get Minecraft Java Edition** | Informational action opening an official purchase/info page via an available URL mechanism. No in-app purchase claim. |
| Help | **Account Help** | Explain Microsoft device-code sign-in, Java ownership and limitations of other profile types. |

**Suggested account card fields:** display name; provider badge; verification state; last used (if tracked); active selection. Never display access/refresh tokens. Only show account removal after persistent multi-account storage exists; sign out is not the same as deleting an account.

## Account flows

```text
App starts
  ├─ valid cached Microsoft session → Home
  └─ no authenticated session → Microsoft Auth V2
                                   └─ More sign-in options → Accounts / Add Account
Home → Accounts → Add Account (future)
  ├─ Microsoft → existing device-code authorization
  ├─ Local Profile → local identity editor (non-entitled; no authenticated game launch)
  ├─ Custom Skin Service → Coming later / explanation
  ├─ Get Minecraft → official help/purchase info
  └─ Account Help → instructions
```

No alternate account method should skip Microsoft ownership checks for authenticated Minecraft launching. Keep account identifiers, session state, and game profiles in distinct data models.

## Implementation steps

1. **Dashboard renderer (implemented, pending verification):** adjust `MC.Xbox/ui/auth_screen.h` main-menu layout, add an explicit home UI state in `MC.Xbox/ui/auth_ui_state.h`, and update desktop previews in `tools/ui-preview/ui_preview.cpp`. Wire existing actions without behavioral changes.
2. **Controller and hit-test mapping (preserved existing six actions, pending verification):** update `MC.Xbox/ui/launcher_ui.cpp` navigation and focus logic; test all existing actions and back behavior.
3. **Accounts overlay:** add UI state, account-method choice focus handling, Microsoft re-entry and help text, without introducing unsupported providers.
4. **Local Profile UI/data model:** implement local-only display identity separately; never confuse it with Microsoft authorization or game ownership.
5. **Future optional Ely.by adapter:** design and evaluate separate secure provider support before enabling a login action.
6. **Visual assets:** original icon, blur/background art with appropriate rights, no dependence on the archived launcher executable.

## Acceptance tests

- [ ] Desktop previews render home, Accounts, Add Account, focus and error states.
- [ ] Home uses real profile/loader/version data and does not truncate on a TV.
- [ ] A activates Play/Mods/Settings/Remote Files/Repair exactly as before; B navigates back without signing out.
- [ ] Microsoft Auth V2 still completes device-code authentication and ownership validation.
- [ ] Signing out clears the Microsoft session only through existing logout logic.
- [ ] Local Profile is visibly labeled non-authenticated and cannot impersonate an entitled Java account.
- [ ] Unsupported providers have disabled or informational actions, not misleading login buttons.
- [ ] Xbox APPX builds, upgrades, launches, navigates with controller and reaches the existing home screen.
- [ ] Existing Java Edition vanilla and Fabric test launches are rechecked independently.

## Scope boundary

This document captures design and engineering requirements. It is **not** evidence that the features beyond Auth V2 are already implemented or hardware-tested. Preserve the validated Auth V2 build as a rollback checkpoint.

## Home V2 implementation note

The first implementation retains exactly six functional actions. Index 0 is the large Play button and indices 1–5 are sidebar buttons: Profiles & Mods (existing Mods page, which includes Profiles), Remote Files, Settings, Repair downloads, and Sign out. No dedicated Accounts action is shown until account-management code exists. Player, active profile, Minecraft target and mod count are populated from runtime state. The desktop preview includes `main-menu`, `home-mods-focus` and `home-no-profile` scenes. Build/hardware checks remain required.

## Accounts UI V2 first implementation

The Accounts navigation entry and account-options page are implemented on `feature/legacyforge-accounts-v2`, pending compilation and Xbox testing. Microsoft remains the existing authenticated account, while Local Profile and Ely.by display explicit *coming later* status. Get Minecraft and Help present information rather than opening external links. D-pad up/down moves option focus, A displays option information, B returns Home. No provider credentials are requested and no alternate Minecraft entitlement flow is present.

## Pre-login Accounts navigation

The Microsoft device-code page now offers **X Other Account Options**. Xbox X opens Accounts while the code is pending; D-pad navigates, A displays availability information and B returns to sign-in. Minecraft ownership is not required to browse the panel. Other methods remain informational. Microsoft device-code polling continues. PC build and Xbox testing pending.

## Phase 4A/B: Local launcher identities (implemented on feature branch; untested on console)

Under **Accounts → Local Profile**, A creates the first named identity (`Local 1`) if none exists. Use X to create additional sequentially named identities (maximum 12), Left/Right to browse, A to select, Y then A to confirm deletion or B to cancel. The UI displays the selected and active identities. Names/selection persist in UWP LocalState `accounts\\local_ids.txt` with no Microsoft tokens or passwords. All input actions are available without Minecraft Java ownership through X at the sign-in screen.

This is a deliberately bounded first step: custom name entry via Xbox on-screen keyboard, full rename workflow, and a non-authenticated dashboard preview are **not** yet implemented. Local launcher identities do not confer Java Edition ownership or enable Play; authenticated Minecraft still requires Microsoft verification.

### Local identity Xbox acceptance

- [ ] Microsoft device-code screen still opens Accounts using X.
- [ ] Local Profile A creates `Local 1`; another X creates `Local 2`.
- [ ] Left/Right browses, A changes the active local identity.
- [ ] Close and reopen launcher; both identities and selected active name persist.
- [ ] Y then B cancels deletion; Y then A deletes; restart confirms persistence.
- [ ] The Microsoft flow, B navigation, and other account information still work.
- [ ] No unauthenticated Minecraft Play action becomes available.

## Phase 4C: Xbox keyboard name editor (feature branch; requires compilation)

The local Accounts option now supports name entry on Xbox using UWP CoreTextEditContext and InputPane, following the existing Mods keyboard implementation. Local Profile: X opens a new identity editor, A opens it when the list is empty, RB/F2 renames the selected entry, Y retains delete confirmation. A or Enter saves once the editor is ready, B cancels. Names are trimmed, limited to 1–24 characters (letters, digits, space, underscore, dash), and must be unique ignoring case. Existing saved Local 1/Local 2 identities and active selection are loaded from the same LocalState file. The feature does not enable unauthenticated Minecraft gameplay.

Xbox tests: create and rename custom names using the on-screen keyboard; check duplicates, blank names, keyboard cancel, restart persistence, delete controls, and Microsoft login regression.

## Phase 5A — Mod browser search recovery (feature branch)

The existing Modrinth/CurseForge search, version filters, loader filters and pagination are retained. The first Phase 5A change adds two controller actions: **X**, while the search control is focused and its Xbox keyboard is closed, clears the search and reloads the current source; **Y**, while result cards are focused, reloads that tab's results and resets scroll to the first card. These actions are disabled for profile tabs and while modals, edits, or installs are in progress. Search and refresh do not change the active Minecraft profile or launch permissions.

**Acceptance:** compile and preview; on an Xbox in Local Launcher Mode open Mods, select Modrinth Popular, search a term, close OSK, X clears results; focus cards, Y refreshes results. Verify failures remain visible and version/loader filters, paging, profile controls, Minecraft authentication, and Home navigation are unaffected.
