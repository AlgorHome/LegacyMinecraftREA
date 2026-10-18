# Phase 5E.3c — Installed browser highlighting

Draft: compilation and Series X testing pending.

Browser results and recommendations now compare their project IDs against per-JAR recorded install metadata in the active mod profile. An enabled match shows **Installed in active profile** with accent border and text; a disabled-only match shows **Installed - disabled** with accent border. Unknown/manual mods with no matching recorded ID are not labelled installed (the lack of an indicator is not proof they are absent). The profile-list's existing active badge behavior is untouched.

The indicator is refreshed on tab results load and paginated fetch. After changing the active profile, refresh the results to compare against that profile. No remote API calls are added; results are derived from local metadata. This is a browse-only feature; it does not change installs or entitlement checks.

## Xbox validation
1. Install a recorded mod in disposable profile A; refresh browser results, verify accent border and **Installed in active profile**.
2. Disable the mod; refresh results, verify **Installed - disabled**.
3. Re-enable; refresh and verify active indication.
4. Switch to profile B without the mod, refresh, and verify no installed highlight; return to A, refresh.
5. Check unindexed manually imported mods do not produce misleading project matches, and scrolling/paging maintains indicators.
6. Confirm R3 inspection, X removal, navigation, Microsoft sign-in and Local Launcher Mode still work.
