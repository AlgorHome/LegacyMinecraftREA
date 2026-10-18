# Phase 5E.2 — Interrupted download retry safety

Draft, build and Series X testing pending.

The mod, resource/shader and modpack download paths now validate that a stale staging file was removed before reusing its path. If cleanup fails, the operation aborts with a clear error, without writing or promoting the previous partial download. Successful cleanup is logged.

The modpack transfer path also attempts to delete a partial cache download if the download operation reports failure. Modrinth SHA-1 validation and the existing staged-file promotion remain unchanged. CurseForge and other downloads without a provided hash still cannot be cryptographically verified; this is a limited recovery improvement, not fully transactional downloads or resumable transfers.

## Console test plan
1. Build signed APPX for MC 1.21.11 / Fabric 0.19.5 and use disposable test profiles.
2. Interrupt a Modrinth mod download, retry, and check that no partial JAR becomes installed; if the staging file remains, a retry should clear it.
3. Confirm a successful verified download installs normally.
4. Reproduce an inaccessible stale staging path if safely possible; verify retry aborts with an error rather than continuing.
5. Retry a modpack and resource/shader download; verify stale-cache cleanup.
6. Restart and confirm profiles, enabled/disabled state, dependency warnings, R3 inspection, search, and sign-in still work.
