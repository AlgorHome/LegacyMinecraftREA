# Phase 5C.3 — Installed, missing, and unknown dependency indicators

Status: implementation committed for Windows compilation and Xbox Series X validation.

## Behavior
Modrinth dependency details now compare required project IDs against the **active profile**'s existing per-JAR install metadata. These metadata records are already written by LegacyForge when installing mods.

- **Installed (recorded)**: a required project ID matches a recorded ID for a JAR currently present in the active profile.
- **Missing from this profile**: no match was recorded **and all present JAR files have valid project IDs** in LegacyForge's metadata.
- **Unknown**: the dependency has no Modrinth project ID, or at least one installed JAR lacks usable project metadata; we cannot safely conclude that the dependency is absent.

The snapshot is captured before the background Modrinth request. This is an observational UI feature and does not alter installation, dependencies, files, licensing, or Minecraft gameplay eligibility.

## Xbox acceptance
- [ ] Build and render preview, then install the signed APPX.
- [ ] Test a required dependency installed by LegacyForge: shows **Installed (recorded)**.
- [ ] On a fully indexed profile without that dependency, shows **Missing from this profile**.
- [ ] With a manually added JAR lacking metadata, unrecognized dependencies show **Unknown** rather than a false missing claim.
- [ ] Switch active profiles and reopen detail; verify status follows the active profile.
- [ ] Check empty dependency lists, failed API requests, scrolling, compatibility warnings, and controller navigation.
- [ ] Confirm no gameplay or entitlement changes.

Future increments can resolve friendly project names and distinguish exact dependency versions from project-level matches; **Installed (recorded)** is not a guarantee of the requested version or Xbox runtime compatibility.
