# Phase 5D.3 — Dependency-aware disable warning

Status: draft branch, not yet compiled or Xbox-tested.

When **A** would disable an enabled mod with recorded dependents, LegacyForge uses its existing per-profile `requiredBy` project metadata to find **enabled**, recorded dependents. The first A press warns and shows the dependent count and an example; a second A on the same selection confirms. **B** cancels without closing the profile. Changing selection also cancels. Disabled dependents do not trigger warnings. A on disabled mods still re-enables directly.

This is a **best-effort warning** based on known install metadata, not complete dependency analysis. It doesn't guarantee safety for manually imported mods or missing dependency relationships. No game launch/auth changes.

## Console acceptance
1. Create disposable profile containing an installed library and a mod recorded as depending on it.
2. Highlight library and press A once. Confirm warning and no .jar change.
3. B cancels; change selection cancels.
4. A twice on the same library disables; A re-enables.
5. A on an unrelated mod toggles without warning.
6. Restart, verify state persists and profiles/browsing/sign-in still work.
