# Phase 5C — Mod compatibility visibility

Status: first increment on feature branch, **PC compilation and Xbox hardware tests pending**.

## First increment

Modrinth browsing already requests project type, Minecraft version and loader facets and the existing compatibility feed warns about certain known Xbox failures. These are separate checks: filtering for a Minecraft target does **not** verify Java mod execution in the Xbox UWP environment.

On mod details the new compatibility context shows the currently selected browsing target (Minecraft version and loader) alongside the label **Xbox UWP runtime: not verified**. The existing known-issue compatibility warning and explicit installation acknowledgement remain in place. Details status messages from installation override the informational text when nonempty.

No entitlement behavior, API filters, dependency installer behavior, existing profile management or mod file writes are changed.

## Xbox acceptance

- [ ] Build and package APPX on Windows and check Mods detail layout.
- [ ] In Local Launcher Mode browse Modrinth mods and open details: confirm target version/loader and **Xbox UWP runtime: not verified** are visible.
- [ ] Switch browsing target version/loader and confirm the context changes.
- [ ] Confirm known Xbox incompatibility warnings still appear and installation acknowledgement is unchanged.
- [ ] Check Modrinth search, refresh, profiles, controller Back, and Microsoft sign-in regressions.

Next increments: dependency disclosure and target-version/loader mismatch detection using project metadata; do not interpret filtering as verified installation or gameplay.
