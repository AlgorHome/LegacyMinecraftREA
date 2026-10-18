# Forge/Fabric and version inheritance resolution

Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.

## Archived and installed launcher paths [E13]

The original installer launcher 1.159.2 has now been inspected alongside installed1.169.4. This resolves the earlier lack of original-build pipeline evidence.

**Confirmed:** original OfficialVersionList.getRawList offset 4 embeds the Mojang version_manifest.json endpoint. Repository enum initialization calls TLauncher.getOfficialRepo/getExtraRepo/getAssetsRepo/getLibraryRepo and uses local/official/extra version repositories. Original ExtraVersionList.getCompleteVersion builds `versions/<id>.json`, parses CompleteVersion, and assigns version/source metadata. These are declarative version profiles; a Forge/Fabric download is not one monolithic game bundle.

**Confirmed:** original CompleteVersion.resolve carries an inheritance-history list, raises DuplicateInheritanceException on duplicate inheritance and ParentNotFoundException when a parent cannot be resolved, recursively resolves the parent, and copies child state into the result. resolveFamily recognizes Forge/Fabric families. Installed equivalents preserve the same broad version/library/argument abstraction; exact metadata merge details are build-specific and should not be replaced by an invented universal algorithm.

**Confirmed:** original MinecraftLauncher.processModpack requests rule-filtered mods and branches by ModpackType. Forge-family paths construct a temporary ModList file and `--modListFile`, or `--fml.mods` and `--fml.mavenRoots` arguments according to the branch. It records a warning and returns an empty list if mod-list generation fails. The same method family exists in installed code. This is evidence of launcher metadata/modpack preparation, not execution of an official Forge installer.

**Confirmed:** RepositoryProxy includes files.minecraftforge.net and maven.fabricmc.net host constants in the original snapshot; installed snapshot expands proxy configuration. Static library repositories include official Minecraft libraries/assets plus launcher-configured fallback/repository machinery. The active mirror, returned loader version JSON and exact remote-generated patched artifacts were not captured. No private launcher mirror was queried to obtain game/loader binaries.

**Important limit:** these artifacts establish consumption of extra version profiles, library resolution, parent merging, native/classpath/argument preparation and Forge-family mod lists. They do not establish that the inspected launcher runs every official Forge/Fabric installer or locally reproduces every upstream processor. A dedicated independent Fabric/Forge processor specification must use current loader documentation and exact target metadata. The static index does not justify claiming universal processor parity.

The original launchMinecraft method calls JavaProcessLauncher.createProcess at 189, ProcessBuilder.environment at 194 and ProcessBuilder.start at 321. downloadResources calls JavaManager.installVersionNow and VersionManager.downloadVersion. Thus the archived artifact itself supports the external desktop game JVM model documented for the installed build.

## Mapping to LegacyForge

LegacyForge's exact pinned source already implements distinct Fabric, Forge and NeoForge providers. Its manifest generator obtains Fabric profile JSON and Forge/NeoForge installer/profile metadata from their upstream repositories; its native host performs loader-specific artifact/classpath/JVM preparation. See DOWNLOADS-TO-LEGACYFORGE and the gap analysis for exact functions.

**Proposed:** independently normalize upstream metadata into a plan containing exact parent chain, libraries/native classifiers, loader processors, main class/module/classpath, conditional arguments, Java/runtime target and verified artifacts. Keep that plan distinct from executing processors or claiming Xbox support. Legacy Launcher's extra-version profiles can explain an architectural pattern; their code, server data, patched libraries and resources are not to be copied into LegacyForge.

All 56 pinned catalog targets are retained in `evidence/target-validation-matrix.csv`; no target was removed to reduce scope. Exact loader and runtime support still requires per-target execution. Static source/catalog checks are not gameplay tests.

## Independently corroborated upstream profile [E17]

The official Fabric 1.21.11/0.19.5 JSON response independently confirms inheritance, KnotClient entrypoint, eight libraries and argument metadata. This explains how a lawful upstream profile can replace dependence on proprietary extra-version catalogs in an independent implementation. It does not establish equivalence with the launcher's private server-generated Forge/Fabric profiles, nor prove the catalog target runs on Xbox. Exact response hashes and normalized comparisons are in evidence/official-metadata-check.json.

E21 extends public metadata observations to every approved catalog row: all 20 exact Fabric profiles, all 34 resolved Forge/NeoForge release coordinates, 22 hash-verified Mojang version JSONs, one explicit unresolved Forge label and one vanilla row. See [full plans](CATALOG-METADATA-PLANS.md). Profile library counts vary; exact Forge/NeoForge processor inputs/outputs, patched artifacts, final launch behavior and Xbox support remain unexecuted.
