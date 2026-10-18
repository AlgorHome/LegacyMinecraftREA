# Installation pipeline

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

## How Legacy Launcher gets Minecraft versions

**Confirmed [E03]:** `OfficialVersionList.getRawList` references `https://launchermeta.mojang.com/mc/game/version_manifest.json`, repository request/parsing and error paths. This manifest is a catalog of version IDs and metadata locations, not a single Minecraft download. `VersionManager.getVersionSyncInfo` and `VersionSyncInfo.resolveCompleteVersion` resolve selected metadata; CompleteVersion supports inheritance and merging. ExtraVersionList also resolves repository `versions/<id>.json`. The exact live chosen mirror was not observed.

**Confirmed:** the selected local 1.21.11 metadata declares the official client URL, assets index URL, library coordinates/URLs, main class, arguments, and required Java component. Its serialization is launcher-normalized (for example artifact paths may be omitted and argument values wrapped as objects), so it must not be assumed byte-identical to upstream Mojang JSON. [E04]

| Step | Endpoint / format / local result | Confirmed mechanism and failure handling |
|---|---|---|
| 1. Catalog | Official manifest URL above; JSON | OfficialVersionList.getRawList parses repository response; exact cache fallback unknown |
| 2. Version metadata | URL selected by catalog or extra repository; JSON → versions/<id>/<id>.json | resolveCompleteVersion, inheritance/merging methods; complete cycle/error handling unknown |
| 3. Libraries | Per-artifact URL, commonly libraries.minecraft.net; Maven coordinates → game/libraries/...jar | getRelevantLibraries, Library.appliesToCurrentEnvironment → Rule.getAppliedAction; classpath file-existence checks |
| 4. Natives | Native JAR ZIP entries → versions/<id>/natives | getExtractFiles / unpackNatives uses ZipFile and filesystem copies; all malformed-entry/path-confinement behavior untraced |
| 5. Asset index | Selected assetIndex.url → assets/indexes/<id>.json | AssetsManager local/remote index parsing; size/optional hash tests |
| 6. Assets | resources.download.minecraft.net/<hash first 2>/<hash> → assets/objects/<prefix>/<hash> | AssetIndex hash paths; AssetDownloadable/Sha1Downloadable completion rejects mismatches |
| 7. Java | launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json | JavaRuntimeRemoteListFetcher platform/component selection; installation and integrity interfaces; space checks in downloadResources |
| 8. Loader | Extra/version metadata and library machinery | Generic infrastructure confirmed; exact Legacy Launcher Forge/Fabric installers, endpoint priority, processors and failure recovery remain Unknown |
| 9. Arguments | Metadata + selected account/config → JVM flags, classpath, main class and game args | createJvmArgs/createArgumentsSubstitutor/CompleteVersion.addArguments; modern/legacy paths present |
| 10. Repair | Existing files + expected length/hash | AssetsManager/checkFile and hash-checking downloadable completions; downloadResources reports aborted/error state; full retry/durability policy Unknown |

All rows are static implementation observations, not captured network transactions. Public component metadata can be fetched independently of Microsoft sign-in in the inspected architecture; that separation does not grant game ownership or bypass authenticated launch requirements. [E03]

## Concrete selected-version example

**Confirmed [E04]:** for local `1.21.11`, metadata main class is `net.minecraft.client.main.Main`; Java requirement is component `java-runtime-delta`, major 21. Client URL is `https://piston-data.mojang.com/v1/objects/ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd/client.jar`, expected size 31,152,600 bytes and SHA-1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`. The locally calculated client hash matches.

Asset index is `29`, declared URL `https://piston-meta.mojang.com/v1/packages/e81d9e2536723a11eb68e11c5642708926b8be5f/29.json`, declared SHA-1 `e81d9e2536723a11eb68e11c5642708926b8be5f`. The 4,591 object hashes were verified against the local index; upstream index bytes/signature were not fetched or authenticated in this pass. The file inventory contains 75 hash-matching metadata-listed library downloads. Absent non-Windows libraries do not imply a damaged Windows cache.

The selected game is not bundled into one launcher EXE download: client, libraries, native archives, assets and Java have separate identities and storage. **Unknown:** which subset the original installer shipped. [E01/E03/E04]

## LegacyForge mapping

See [DOWNLOADS-TO-LEGACYFORGE](DOWNLOADS-TO-LEGACYFORGE.md) for the existing implementation, build-time versus console-time responsibilities, loader differences and proposed independent changes. Do not execute Legacy Launcher code, use its private mirrors, or copy its patched resources to implement that mapping.

## Continuation: original installer and loader evidence

E11/E13 now confirm the archived launcher itself has the official catalog endpoint, extra version-profile path, inheritance exceptions, Java install orchestration and external ProcessBuilder launch. LOADER-RESOLUTION describes exactly which Forge-family mod-list and profile behaviors were recovered. Earlier references to unknown loader semantics remain true for unobserved remote/prepared processor content and execution, but no longer mean the relevant static paths were left unexamined. UPDATE-AND-RECOVERY documents range/redirect/error/persistence branches. Windows runtime/fault tests are BLOCKED, with full procedures prepared.

## Independent official metadata comparison [E17]

An unauthenticated HTTPS request to the official Mojang v2 catalog selected version 1.21.11 and fetched only its public JSON metadata. Version JSON SHA1 `718cd84b4912691fe5de829aab6876a4b7f6c5c4` matches the catalog declaration; SHA256 is `471a6eeadf1c74f84ed5d4290fb7234b746373478a4d6ac651962b93f0cb36d9`. Local ID, main class, Java requirement and download descriptors equal the official fields. All 107 locally described library artifact SHA1/URL pairs match corresponding official entries. The local asset index's SHA1 matches the independently obtained official value `e81d9e2536723a11eb68e11c5642708926b8be5f`.

The local assetIndex object has an extra `known` field, so whole-object equality is false while every official assetIndex field agrees. This is normalization, not a mismatch in index identity. Keep the local serialized schema separate from the official schema. No client/library/runtime binary or asset object was downloaded by this check. Current metadata verification does not authenticate the historical installer or constitute a game launch.
