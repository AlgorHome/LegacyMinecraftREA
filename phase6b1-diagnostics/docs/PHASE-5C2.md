# Phase 5C.2 — Required dependency visibility

**Status:** draft code, Windows build and Xbox Series X validation pending.

For Modrinth mod details, LegacyForge now fetches version-specific dependency metadata for the selected Minecraft version and loader, matching the existing installer's version-selection preference (release first). The details body lists up to eight required dependency identifiers and reports additional required items numerically. The lookup is read-only and does not install or remove files.

**Important limitations:** Dependencies are shown using Modrinth project IDs (or version IDs if project IDs are absent), not resolved display names. The feature does **not** currently check whether they are installed, missing, or compatible with Xbox UWP. Unlisted runtime requirements may exist. If the matching-version lookup fails, details say so rather than implying no dependencies. CurseForge details remain unchanged.

## Xbox acceptance
1. Build the feature branch and launch LegacyForge in Local Launcher Mode.
2. Select a Modrinth mod and scroll details to **Required Dependencies (Modrinth)**.
3. Test a mod with declared dependencies and a mod without declared dependencies.
4. Change target Minecraft version/loader; reopen details and confirm the summary updates or reports no matching release.
5. Disable network and confirm dependency fetch errors are presented without breaking description navigation.
6. Verify known Xbox compatibility warnings, installation behavior, profiles, search and authentication remain unchanged.

Future 5C.3 work can resolve names and compare dependency project IDs with per-profile installation metadata before labeling items Installed or Missing.
