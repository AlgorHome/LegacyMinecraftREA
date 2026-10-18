# LegacyForge Phase 5B — Profile management

Status: first increment implemented on feature branch, Windows compilation and Xbox Series X validation pending.

## Changes

The Mods → Profiles page now supports **Y on a profile card** to make it the active Minecraft installation without entering its detail screen. Only saved profile cards activate; New Profile and restore-backup cards are ignored. The existing Y Rename inside profile details remains unchanged.

The active card is labelled **Active profile**; inactive cards show **Y Set active**. Each card already displays Minecraft version and loader from `ResolveProfileTarget`, with installed mod counts from `ProfileModCount`. After switching, the page reloads the active profile, updates its browse target, and keeps the selected card visible; returning to Home continues using the existing profile-summary refresh.

This does not change authentication, game launch eligibility, the profile storage format, or mod file installation. Local Launcher Mode can use profile management without enabling Minecraft gameplay.

## Xbox acceptance

- [ ] Run UI previews and build APPX successfully from this feature branch.
- [ ] Enter Local Launcher Mode, open Profiles & Mods → Profiles.
- [ ] Select a nonactive profile card and press Y. Confirm the active badge and target version/loader update.
- [ ] Switch between Fabric/Forge/NeoForge/Vanilla profiles when configured; check browser version/loader target follows.
- [ ] Return to Home and verify its active profile summary updates.
- [ ] Restart and ensure the active profile persists.
- [ ] Press A to inspect a profile; confirm Y inside details still opens Rename rather than activating.
- [ ] Confirm X delete, create, mod collections, search and Microsoft sign-in still work.

Do not interpret mod-management success as proof of Minecraft Java gameplay on Xbox.
