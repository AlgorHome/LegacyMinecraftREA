# Phase 5D.4 — Read-only installed mod inspection

**Draft — Windows build and Xbox Series X validation pending.**

Press **R3 (right stick)** on an installed mod card to open a read-only inspection panel. Keyboard **F1** also opens it. B closes inspection without leaving profile details. The panel shows the filename, enabled/disabled state, recorded Modrinth project ID, recorded title, dependency flag, and enabled dependents known to LegacyForge's per-profile metadata. It explicitly cautions that manually imported mods may lack metadata and Xbox runtime compatibility is unverified.

Existing A toggle, X two-step deletion and Y profile rename actions are unchanged. The inspection panel does not modify mod files or profile metadata.

## Xbox validation

1. Open a profile's installed mod grid and press R3. Check project ID, name, filename and status.
2. Inspect a disabled mod: state displays Disabled.
3. Inspect a library with recorded dependents and check the dependent names/count.
4. Inspect a manually imported mod with no metadata: fields show Unknown.
5. Press B to close inspection and confirm A/X/Y remain functional.
6. Restart and check previous toggle/removal behavior, browsing and sign-in.
