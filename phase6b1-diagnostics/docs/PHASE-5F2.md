# Phase 5F.2 — Persistent Installed button

Draft — Windows compilation and Xbox Series X validation pending.

For Modrinth/CurseForge **mod** details, the Install action now shows **Installed** using the chosen Settings highlight color when project metadata proves the mod is enabled in the active profile, or **Installed - Off** if only a disabled copy exists. A press on either state gives a status message rather than starting a duplicate install. The detail state is recomputed on opening and on successful job completion, and visible browse cards refresh after successful installs. A failed installation does not set the installed state. Modpacks, shaders and other content retain their established install controls because this version has no equivalent proven per-project install records for them. Manually imported mods without project IDs cannot be reliably identified.

## Xbox tests
1. Open not-yet-installed mod details: Install is present. Install into a compatible non-vanilla disposable profile and verify Installed appears immediately.
2. Close and reopen detail: Installed persists; restart launcher and verify it remains.
3. A on Installed does not trigger a duplicate installation.
4. Disable via Profiles: reopening the detail shows Installed - Off; re-enable and reopen.
5. Switch to a profile without the mod, reopen: Install is shown; return to original and recheck.
6. Failed download doesn't switch to Installed; controller navigation, Settings color choice, auth and Play/Repair safeguards remain intact.
