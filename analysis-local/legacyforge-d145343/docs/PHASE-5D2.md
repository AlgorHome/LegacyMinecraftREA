# Phase 5D.2 — Reversible per-profile mod toggle

**Draft: build and Xbox tests pending.**

- In a profile's installed mod grid, A renames the selected `.jar` to `.jar.disabled` or vice versa without moving it outside the profile. Filenames are checked for destination collisions; failures display a status.
- Both enabled and disabled mods appear in the same profile grid; disabled mods are labelled `[OFF]`. The original per-JAR install metadata stays associated with the original `.jar` filename.
- X removal retains its two-step confirmation and can delete a disabled file too. Dependency-status snapshots exclude disabled JARs.
- Y profile rename, A action buttons, B and existing profile switching are unchanged.

**Limitations:** This first increment does not prevent disabling mods required by other mods. A future safeguard should inspect reverse dependencies. Profile card counts still count enabled JARs; the installed-mod detail view includes disabled files. No mod execution on Xbox is implied.

## Xbox test plan

1. Use a disposable profile with a mod installed and open its installed-mod grid.
2. Press A on a mod: `[OFF]` appears. Confirm the file remains in storage with `.jar.disabled` suffix.
3. Press A again: `[OFF]` disappears and the original `.jar` filename returns.
4. Disable, restart, and verify the `[OFF]` label and file persist; enable after restart.
5. Verify other profiles are unaffected; confirm X removal still requires confirmation and B cancels.
6. Recheck dependency status, profile rename, Modrinth browsing, and Microsoft sign-in.
