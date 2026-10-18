from pathlib import Path
import json,hashlib,csv

BASE=Path(__file__).parent.parent
LOCAL=BASE/'analysis-local'
DOC=BASE/'docs/research/legacy-launcher'
DOC.mkdir(parents=True,exist_ok=True)
(DOC/'evidence').mkdir(exist_ok=True)
D=json.loads((LOCAL/'inventory.json').read_text())
R=json.loads((LOCAL/'runtime-evidence.json').read_text())
J=json.loads((LOCAL/'jar-static/inventory.json').read_text())
S=json.loads((LOCAL/'legacyforge-source-evidence.json').read_text())
A=json.loads((LOCAL/'archive-metadata-sanitized.json').read_text(encoding='utf-8-sig'))
SIG=json.loads((LOCAL/'signatures.json').read_text(encoding='utf-8-sig'))
PIN='d1453434ceefe73bef5aff497194e09f39dde7e1'
GH=f'https://github.com/AlgorHome/LegacyForge/blob/{PIN}/'
def src(path,line):return f'[{path}:{line}]({GH}{path}#L{line})'
def write(name,text):
 p=DOC/name
 if p.exists():raise FileExistsError(p)
 p.write_text(text.strip()+'\n',encoding='utf-8')
HEADER='Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.\n\n'

write('README.md', '''# LegacyForge Phase 6A: Legacy Launcher research

'''+HEADER+f'''Baseline: LegacyForge `{PIN}` on `main`, explicitly approved by the user. Source checkout remained clean. Research documents are separate from that checkout and production code.

**Confirmed:** the archived installer and installed launcher are different version identities. The 117,751,681-byte installer matches the archive's published SHA-1 and MD5 and reports file version `1.159.2.0`. Installed launcher metadata reports `1.169.4+legacy`; bootstrap reports `1.40.3+legacy`. The selected installed game is Minecraft `1.21.11`. The installer-to-installed update history is **Unknown**. [E01–E04]

**Confirmed:** the installed application uses a native Windows wrapper, a Java bootstrap, Swing UI, version/dependency managers and an external game JVM. The selected game requests Java 21 and uses Windows LWJGL 3.3.3 dependencies. LegacyForge already implements an embedded JVM and its own GLFW/Mesa adaptation. Copying the desktop launcher/startup path would not establish Xbox compatibility. [E02–E07]

Start with [how version downloads transfer to LegacyForge](DOWNLOADS-TO-LEGACYFORGE.md), then [installation pipeline](INSTALLATION-PIPELINE.md), [gap analysis](LEGACYFORGE-GAP-ANALYSIS.md), and [roadmap](PHASE-6-ROADMAP.md).

## Documents

- [Provenance](PROVENANCE.md): archive identity, signatures, hashes and restrictions.
- [File inventory](FILE-INVENTORY.md): bounded directory and executable inventory.
- [Architecture](ARCHITECTURE.md): subsystem and dependency maps.
- [Authentication boundaries](AUTH-BOUNDARIES.md): accounts, ownership and token handling.
- [JVM/runtime](JVM-RUNTIME.md): Java selection, classpath and native dependencies.
- [Xbox/UWP compatibility](XBOX-UWP-COMPATIBILITY.md): observed behavior versus platform needs.
- [Evidence index](EVIDENCE-INDEX.md): identifiers, tools, reproducible commands and limitations.
- [Unknown subsystems](UNKNOWN-SUBSYSTEMS.md): unanswered questions and required probes.

## Interpretation and completion boundary

**Confirmed** means artifact bytes, selected method instructions, pinned source, or a cited official document establish the stated narrow fact. **Inferred** means those observations support an explanation without proving runtime behavior. **Unknown** means required evidence is absent. Source presence does not prove execution, endpoint constants do not prove network traffic, and hash agreement does not prove publisher authenticity.

The read-only research package is delivered. Exhaustive analysis, exact historical update reconstruction, every loader behavior, and Xbox gameplay validation remain open in UNKNOWN-SUBSYSTEMS. The user's report that Phase 5F.2 was Xbox Series X-tested is retained as user-provided context, not independent validation of all targets.

No target executable, installer, JAR, bundled Java, or game was run. Trusted analysis tools parsed target bytes. No installs, network authentication, production edits, Git commits or pushes were performed. No proprietary binaries, game assets, raw profiles, token values, decompiled listings or raw class pools are in this research folder. Local-only analyst working data lives in `analysis-local/` outside it; do not bulk-publish that directory or the workspace root.
''')

rows=[]
for f in D['selected_files']:
 pe=f['pe'];typ=(pe['format']+' / '+pe.get('architecture','?')+' / subsystem '+str(pe.get('subsystem','?'))) if pe else 'ZIP/JAR'
 rows.append(f"| `{f['path'].replace(chr(92),'/')}` | {f['bytes']:,} | {typ} | `{f['sha256']}` |")
write('PROVENANCE.md','''# Provenance

'''+HEADER+'''## Archive and local identity

**Confirmed [E01]:** [Internet Archive item](https://archive.org/details/legacy-launcher-for-minecraft), identifier `legacy-launcher-for-minecraft`, title “Legacy Launcher for Minecraft,” published `2024-02-26 21:00:34` as recorded by the archive. Its creator field claims “Legacy Launcher Team.” The description's independence/safety assertions are uploader claims, not verified provenance or a malware assessment. The archive item exposes no license URL in the inspected metadata.

Source download URL: `https://archive.org/download/legacy-launcher-for-minecraft/LegacyLauncher_Installer_legacy.exe`.

**Confirmed:** local installer `LegacyLauncher_Installer_legacy.exe`, 117,751,681 bytes, SHA-256 `a7c997ba3c3e91c048f80f96f08754948428f6d3fe4001bab79c4ae09d06c5e0`. Local SHA-1 `00bddca8bba387a76d6f18fc942859acf9ff5a60` and MD5 `53eea8664d54198e1989301b12f795da` equal the archive's published values. SHA-256 is locally calculated; the archive metadata did not publish it. These checks bind the local file to the archived item, not to a signed upstream publisher.

Local filesystem creation time was `2026-10-17T05:38:41.2577661Z` (2026-10-17 00:38:41 America/Chicago); last write `05:39:00.5248089Z`. **Inferred:** likely local acquisition on October 17. **Unknown:** exact download event/source chain; timestamps are mutable and no readable Zone.Identifier stream was available. The installer was found in the research workspace during inspection; an initial workspace listing also showed it under the launcher workspace. No agent move/delete operation occurred.

## Separate version identities

| Object | Observation | Status/evidence |
|---|---|---|
| Installer PE version | File `1.159.2.0`; product `rolling`; “Legacy Launcher Stable”; company “Legacy Launcher Team” | Confirmed E01 |
| Installed launcher | `META-INF/launcher-meta.json`: `1.169.4+legacy`, Stable, Java `[11,)` | Confirmed E02 |
| Installed bootstrap | `META-INF/bootstrap-meta.json`: `1.40.3+legacy`; Spring Boot wrapper 2.7.18 | Confirmed E02 |
| Selected installed game | Version JSON and directory `1.21.11`; Java major 21, component `java-runtime-delta` | Confirmed E04 |
| Link between installer and installed JARs | Update mechanism surfaces exist, but no authenticated update history/package-content comparison | Unknown E01/E02/E03 |

The `.tlauncher` directory and old package names do not establish equivalence with another similarly named product.

## Signatures, packaging and architecture

**Confirmed [E01/E05]:** Get-AuthenticodeSignature reports `NotSigned` for the installer and TL.exe. They are x86 PE32 GUI images (subsystem 2). The installed JVM images are x86-64 PE32+; java.exe uses console subsystem 3 and javaw.exe GUI subsystem 2. Wrapper CPU architecture is independent of game CPU architecture. Installer and uninstaller contain Inno Setup data markers. **Inferred:** Inno Setup packaging; exact packaging version and full embedded payload remain **Unknown**, because no installer was run or bulk-unpacked.

**Confirmed:** bundled Java 17 java.exe reports Azul Zulu 17, version 17.0.3, Authenticode status `Valid`. Signer subject `Azul Systems, Inc.`, issuer DigiCert SHA2 Assured ID Code Signing CA; thumbprint `2BAACB41471E70059550B6FC7DE2BBC09B09F795`; certificate validity March 20, 2020 to June 18, 2023 UTC; timestamp subject DigiCert Timestamp 2022 - 2. A historical signing certificate's expiry alone does not override the returned Windows validation status. No standalone certificate-chain audit or revocation-policy analysis was performed. See sanitized signatures evidence for exact metadata and Java 21 result.

## Licenses and publication boundary

**Confirmed [E10]:** launcher `LICENSE.txt` references Apache/MIT third-party projects, Minecraft EULA-covered modified content, and CC BY-SA icon packs; bundled JRE includes module legal files and OpenJFX licensing. This is not evidence of a blanket license to reproduce the launcher or its resources. Archive availability and an “open_source_software” collection name do not establish redistribution rights.

The [Minecraft EULA](https://www.minecraft.net/en-us/eula) restricts redistribution of Mojang content. This report records a conservative publication boundary rather than a legal clearance: publish independently written behavior descriptions and curated metadata; retain proprietary artifacts, tokens, assets and reconstructed listings locally. No software was committed or redistributed by this investigation.

## Relevant hashes

Paths beginning `legacy/` are relative to the local launcher workspace; installer path is relative to the research workspace.

| File | Bytes | Format / CPU / subsystem | SHA-256 |
|---|---:|---|---|
'''+ '\n'.join(rows))

groups='\n'.join(f"| `{k}` | {v['files']:,} | {v['bytes']:,} |" for k,v in D['summary'].items())
write('FILE-INVENTORY.md','''# File inventory

'''+HEADER+'''**Confirmed [E04]:** inventory covered the supplied `.tlauncher` tree recursively, including launcher, game, runtime and log directory counts. It did not follow an installer execution or inventory arbitrary user directories. Game saves, account/profile values and log contents were excluded from the publishable inventory.

| Relative directory/file group | Files | Bytes |
|---|---:|---:|
'''+groups+'''

```text
.tlauncher/
  legacy.properties                  bootstrap-level settings (values excluded)
  logs/                              historical logs (raw content excluded)
  legacy/Minecraft/
    TL.exe                           x86 Windows wrapper
    tl.args                          bootstrap arguments and settings path
    tl.properties                    launcher preferences (values excluded)
    unins000.exe, unins000.dat        installation bookkeeping
    launcher/
      bootstrap.jar                  outer Spring Boot ZIP with nested JARs
      launcher.jar                   installed application
      libraries/                     launcher dependencies
    jre/
      release, bin/, lib/, legal/     Java 17 launcher runtime
      java-runtime-delta/windows-x64/java-runtime-delta/
                                     Java 21 game runtime
    game/
      versions/1.21.11/               metadata, client, backup, extracted natives
      libraries/                     version libraries and native JARs
      assets/indexes/29.json
      assets/objects/<prefix>/<hash>
      tlauncher_profiles.json         not copied or read for token values
      logs/                          historical only
```

**Confirmed:** launcher.jar contains 1,329 ZIP entries and 1,112 classes. bootstrap.jar contains 116 outer entries and 70 outer classes, plus nested application/dependency JARs; outer counts do not measure nested classes. Its nested libraries include FlatLaf, Gson, JNA, Commons, DBus transports and bootstrap/bridge/common/utils components. Names/version strings describe packaged dependencies, not proof every component loads on Windows. [E02]

**Confirmed:** a game client and cache are already present, not merely launcher components. The selected client JAR is 31,152,600 bytes and matches version metadata SHA-1; its `.bak` has the same SHA-256. Asset index 29 lists 4,591 objects, all present and SHA-1-matching. Of 107 version-metadata library download entries, 75 files are present and all 75 hashes match; the 32 absent entries identify macOS/Linux artifacts. This is a bounded check against local metadata, not authenticated upstream revalidation or a complete launch-readiness verdict. [E04]

**Confirmed:** download/install methods also exist, so this populated installation supports on-demand component acquisition. **Unknown:** which files came inside the original installer versus later downloads. [E01/E03]

Complete relevant executable/JAR paths and sizes are in `evidence/relevant-files.csv`; selected executable/JAR/native hashes are in PROVENANCE. Static dependency metadata is in `evidence/static-summary.json`. No game contents are included.
''')

write('ARCHITECTURE.md','''# Architecture

'''+HEADER+'''The following map combines confirmed structural/static-call evidence with inferred edges explicitly labeled. It is not an observed execution trace. [E02/E03/E05/E06]

```mermaid
flowchart TD
  A[TL.exe: x86 native wrapper] -->|Inferred startup linkage| B[bootstrap.jar / Spring JarLauncher]
  B -->|Inferred prepare / bridge / update| C[launcher.jar: LegacyLauncher entrypoints]
  C --> UI[Swing JFrame / FlatLaf UI]
  C --> CFG[Configuration / ProfileManager]
  C --> VM[VersionManager / version repositories]
  C --> JM[JavaManager / runtime manifests]
  C --> AM[AssetsManager / Downloader]
  C --> AUTH[Microsoft / XBL / XSTS / Minecraft account flow]
  VM --> ML[MinecraftLauncher staged preparation]
  JM --> ML
  AM --> ML
  AUTH --> ML
  ML -->|Confirmed static call| PB[ProcessBuilder.start]
  PB -->|Inferred process result| GAME[Desktop game JVM]
  GAME --> N[JNI: LWJGL / GLFW / OpenAL / JNA]
```

**Confirmed:** `TL.exe` contains Launch4j and javaw strings and calls CreateProcessA in `FUN_00405126`, call site `0x40524e`. `tl.args` points to `launcher/launcher.jar`, `launcher/libraries` and `tl.properties`. The exact native-wrapper → bootstrap argument linkage has not been traced end to end. [E05/E06]

**Confirmed:** bootstrap manifest selects `org.springframework.boot.loader.JarLauncher` and `net.legacylauncher.bootstrap.BootstrapStarter`. Launcher metadata selects `LegacyLauncherEntrypoint` and bridged entry. `LegacyLauncherFrame` extends Swing JFrame; FlatLaf is packaged. [E02/E03]

| Subsystem | Confirmed static evidence | Remaining limit |
|---|---|---|
| Initialization | Launcher entry metadata; MinecraftLauncher.collectInfo | Full lifecycle branches untraced |
| Configuration | Configuration, SimpleConfiguration, AbstractConfiguration; preferences keys only inventoried | Exact setting precedence and rollback untraced |
| Profiles/accounts | ProfileManager.loadProfiles/saveProfiles uses Gson, temp output and Files.move; migration of launcher_profiles.json | Crash durability and storage protection unknown |
| Version selection | VersionManager.getVersionSyncInfo; resolveCompleteVersion; Official/Extra/Local lists | All mirrors and custom versions untested |
| Runtime discovery | JavaManager configuration, JavaRuntimeLocal/remote fetcher/installers | Actual selected path not captured live |
| Downloads | downloadResources queues runtime/version/assets; checks abort/error state | Retry/cancellation behavior not exhaustively traced |
| Game process | constructProcess → launchMinecraft → JavaProcessLauncher/ProcessBuilder.start | No process launched by this investigation |
| Error/exit control | onJavaProcessEnded, onJavaProcessError, killProcess, postLaunch methods | User-facing behavior and shutdown race handling untested |
| Updates | Nested bootstrap prepare/download/start/self-update surfaces, signed-stream/checksum types | Verification/trust/rollback policy unknown; type names alone are insufficient |

## Dependency graph and transferable boundary

```mermaid
flowchart LR
  V[Version JSON] --> RULE[OS / architecture / feature rules]
  RULE --> LIB[Library JARs + native classifier archives]
  V --> CLIENT[Client JAR / main class]
  V --> IDX[Asset index] --> OBJ[Content-addressed objects]
  V --> JAVA[Required Java component / major]
  LIB --> CP[Classpath + native directory]
  CLIENT --> CP
  CP --> LAUNCH[Launch preparation]
  OBJ --> LAUNCH
  JAVA --> LAUNCH
  ACC[Authenticated entitled profile] --> LAUNCH
```

**Confirmed:** these generic installation contracts are represented in method calls and selected version data. Swing branding, account-provider UI, launcher self-updater, settings presentation and bootstrap IPC are launcher-specific. **Inferred:** independent metadata resolution, hashing/caching and repair behavior can inform LegacyForge. Desktop subprocess/native-window behavior requires adaptation to LegacyForge's existing JNI/GLFW/Mesa path. [E03/E04/E07]
''')

write('INSTALLATION-PIPELINE.md','''# Installation pipeline

'''+HEADER+'''## How Legacy Launcher gets Minecraft versions

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
''')

write('DOWNLOADS-TO-LEGACYFORGE.md','''# Version downloads: from Legacy Launcher to LegacyForge

'''+HEADER+'''The transferable behavior is “resolve a version into a verified installation plan.” LegacyForge already does much of it. Porting the desktop executable, downloaded Windows JVM or Windows GLFW does not supply the Xbox runtime adaptation. [E03/E07/E08]

## Existing path at the approved commit

**Confirmed [E07]:** LegacyForge prepares approved targets at build/tooling time and consumes packaged download manifests on the console. This differs from assuming that it resolves every arbitrary new Mojang version live at runtime.

```mermaid
flowchart TD
  C[config/versions.tsv: approved target] --> BUILD[Build/tooling: new-download-manifest.ps1]
  MOJ[Mojang manifest v2 + selected version JSON] --> BUILD
  LOAD[Fabric profile or Forge/NeoForge installer metadata] --> BUILD
  BUILD --> TSV[Packaged runtime/manifests/target.tsv: paths, sizes, SHA1, URLs]
  TSV --> CONSOLE[Console: ResolveVersionInfo / EnsureRuntimeDownloads]
  WEB[Official component endpoints] -->|Only missing / hash-mismatched files| CACHE[App-local asset, library and client cache]
  CONSOLE --> CACHE
  CACHE --> NAT[PrepareTargetNativeDir + packaged native overrides]
  PKG[Packaged Xbox-adapted JVM / GLFW / Mesa] --> JVM[LoadPackagedLibrary + JNI_CreateJavaVM]
  NAT --> JVM
  AUTH[Existing Microsoft + Minecraft entitlement checks] --> START[Loader-specific main class / game entry]
  JVM --> START
```

| Legacy Launcher behavior | LegacyForge equivalent already present | What needs attention |
|---|---|---|
| Fetch available versions | Build script queries official version_manifest_v2.json, finds exact ID and follows version.url | Exposing all manifest IDs in UI must not imply runtime support |
| Version JSON/client | Build script records JSON and downloads.client URL/hash/size as TSV entries | Preserve exact source metadata identity and receipts |
| Select libraries | Add-MinecraftLibraries / Test-LibraryAllowed | Ordered Windows/x64 handling exists; os.version fails closed; features/conditional args need explicit contract |
| Assets | Add-Assets records index and hash-addressed objects | Reuse content-addressed caching and verify completion |
| Download/repair | EnsureRuntimeDownloads checks SHA1, bounds workers 1–8, retries .download files, rejects mismatch, moves verified result | Add structured repair/install receipts; do not rewrite existing pipeline |
| Java choice | ResolveJavaRuntimeInfo selects current/java21/java17/legacy (jre/jre21/jre17/jre8) and versioned filesystem/ZIPFS patches | Do not replace Xbox runtime with downloaded Mojang desktop java.exe |
| Native preparation | PrepareTargetNativeDir extracts selected LWJGL/JNA DLLs and overlays packaged GLFW | File presence is not ABI/graphics compatibility; validate exact native versions |
| Classpath/main | CollectManifestLibraryJars; loader finalizers and classpath hooks | Keep loader-specific processors, module options and main classes |
| Startup | PreloadJvm + RunEmbeddedMinecraft load packaged modules and invoke JNI_CreateJavaVM | No desktop ProcessBuilder/java.exe transplant; verify requested JNI version for each runtime |
| Accounts/ownership | Existing OAuth device flow → XBL → XSTS → Minecraft → entitlement → profile | Preserve protections and token redaction unchanged |

Exact source anchors: '''+src('scripts/new-download-manifest.ps1',547)+', '+src('scripts/new-download-manifest.ps1',155)+', '+src('scripts/new-download-manifest.ps1',534)+', '+src('MC.Xbox/launch/runtime_manager.cpp',770)+', '+src('MC.Xbox/launch/runtime_manager.cpp',1079)+', '+src('MC.Xbox/launch/runtime_manager.cpp',1166)+', '+src('MC.Xbox/launch/runtime_manager.cpp',1310)+', '+src('MC.Xbox/launch/minecraft_launch.cpp',663)+', '+src('MC.Xbox/launch/minecraft_launch.cpp',1335)+'''.

## What happens for 1.21.11

**Confirmed:** the approved `config/versions.tsv` already lists experimental 1.21.11 targets: Fabric 0.19.5, Forge 61.2.1 and NeoForge 21.11.45, all assigned java21. This is a catalog/support declaration, not proof each combination runs on Xbox. The examined Legacy Launcher installation supplies vanilla 1.21.11 evidence; it does not validate those loader combinations. [E04/E07]

**Proposed independent workflow:** select one catalog target, generate/review its exact dependency manifest, package the compatible runtime/native bridge, let the console download only missing/mismatched client/library/asset files, prepare loader/native state, verify runtime readiness, retain entitlement/profile checks, then invoke the existing embedded JVM entry path. Gate support claims per version + loader + JVM + native/graphics combination.

**Confirmed:** the script fetches Fabric profile JSON from `https://meta.fabricmc.net/v2/versions/loader/<minecraft>/<loader>/profile/json`. Forge metadata/artifacts come through `maven.minecraftforge.net`, NeoForge through `maven.neoforged.net/releases`; the script reads installer/profile data and provider code handles client preparation. These are LegacyForge source observations, not recovered Legacy Launcher behavior or executed installers. [E07]

## If a live version picker is desired later

**Proposed:** keep “available upstream,” “downloaded,” and “validated for Xbox” separate. An independently written runtime resolver could fetch an official catalog and exact JSON, evaluate inheritance/rules/features, derive a bounded plan, verify metadata/hash/size, then reuse EnsureRuntimeDownloads. Approve a platform/runtime profile before offering Play. Use explicit errors for unsupported rules or loader processors; never silently flatten conditional values. Adding live arbitrary-version support is separate engineering work and was not implemented during Phase 6A.

Portable content contracts: JSON resolution, Maven paths, hash-addressed asset caching, size/hash repair and deterministic classpaths. Platform work: packaged JVM API/JIT behavior, native loading, GLFW/CoreWindow, Mesa graphics, input/audio, filesystem patches and lifecycle. Download success establishes installation state; hardware runtime evidence establishes gameplay readiness.
''')

write('AUTH-BOUNDARIES.md','''# Authentication and licensing boundaries

'''+HEADER+'''## Installed launcher's architecture

**Confirmed [E03]:** `MinecraftOAuthAuthenticate.authenticate` contains the sequence Microsoft authorization-code OAuth → Xbox Live → XSTS → Minecraft services token → GameOwnershipValidator → Minecraft profile/conversion. Constants identify login.live.com OAuth endpoints, user.auth.xboxlive.com, xsts.auth.xboxlive.com, api.minecraftservices.com authentication/login_with_xbox, entitlements/license and minecraft/profile. These are recovered implementation endpoints, not verified current service contracts or captured traffic.

**Confirmed:** GameOwnershipValidator sends a Bearer-authorized entitlement request, rejects empty item lists and requires both `product_minecraft` and `game_minecraft` entries in this inspected implementation. PlainUser/PlainAuth and other account-provider classes also exist; a launcher-local identity is not proof of Microsoft authentication or Java ownership. Third-party modes are not an implementation pattern for bypassing ownership.

**Confirmed:** ProfileManager persists account/profile sets through Gson with temporary output and Files.move. MinecraftUserJsonizer payload types include Microsoft and Minecraft token objects. Token values and actual profile contents were not inspected. **Unknown:** encryption/protection at rest, renewal lifecycle in every provider, and full redaction coverage. Do not call this secure-vault storage without additional evidence.

## Downloading versus launching

**Confirmed:** catalog/library/asset/runtime acquisition is structurally separate from the Microsoft authentication flow. Public metadata/artifact acquisition can be an installation-preparation activity without collecting a user's Microsoft credentials. That does not authorize copying restricted game content to a research repository or demonstrate legitimate unauthenticated gameplay. [E03/E10]

**Inferred:** maintain distinct states for local launcher profile, Microsoft sign-in, Minecraft services authorization, ownership validation, and game profile. A downloaded client JAR or Xbox console sign-in is insufficient evidence of Java entitlement. No ownership or online-session check was bypassed or tested here.

## Preserve LegacyForge's existing boundaries

**Confirmed [E07]:** '''+src('MC.Xbox/auth/minecraft_auth.cpp',391)+''' sequences XBL/XSTS/Minecraft authentication, then entitlement and profile retrieval. `EnsureMinecraftEntitlement` at line 332 accepts recognized `game_minecraft` or `product_minecraft` items; do not silently copy the installed launcher's different both-item predicate. Present service compatibility was not authenticated or tested.

**Confirmed:** refresh tokens use Windows PasswordVault/PasswordCredential in minecraft_auth.cpp:17–61. Local sessions are separate in App.cpp:515–554; launcher_ui.cpp:1083 and 1108 block Play/Repair without the existing ownership boundary. `common/launch_diagnostics.h:9–15` redacts both token argument syntaxes; minecraft_launch.cpp uses that helper when logging game args. This narrow helper does not prove all possible JVM/user-supplied text is redacted.

**Proposed:** retain those checks and storage. Any account changes require separate scope. Use synthetic credentials for future tests and keep access/refresh tokens, device codes, personal UUID/name/account records and raw authentication logs out of research artifacts. No authentication was performed in this investigation.
''')

write('JVM-RUNTIME.md','''# JVM and native runtime analysis

'''+HEADER+'''## Separate launcher Java from game Java

| Layer | Confirmed observation | Evidence |
|---|---|---|
| Native entry wrapper | TL.exe is x86 PE GUI; Launch4j/javaw strings and CreateProcessA call | E05/E06 |
| Installed launcher | 1.169.4+legacy metadata requires Java 11 or newer | E02 |
| Bundled launcher runtime | Azul Zulu 17.0.3, x86-64 Windows, JavaFX modules | E01/E05 |
| Selected game metadata | 1.21.11 requires java-runtime-delta, Java major 21 | E04 |
| Additional installed runtime | jre/java-runtime-delta/windows-x64/java-runtime-delta/release says 21.0.7; native java/jvm files are x86-64 | E04/E05 |

**Unknown:** actual selected executable and flags in a captured live launch; two installed runtimes and metadata are not proof of the active process path. The release fields observed for Java 21 did not identify a vendor, so none is assigned here.

## Desktop launch construction

**Confirmed [E03/E04]:** JavaManager chooses local/recommended/custom configurations and remote component manifests. JavaRuntimeLocal maps platform to executable path. MinecraftLauncher constructs the classpath with CompleteVersion.getClassPath and checks file existence; it extracts selected native libraries to a writable directory. Metadata/argument construction supplies `-Djava.library.path`, JNA/LWJGL extraction locations, `-cp`, main class, launcher identity, heap/encoding options and game placeholders. The inspected game placeholders include username, UUID, access token, clientId and XUID; no values were collected.

`launchMinecraft` invokes JavaProcessLauncher.createProcess and ProcessBuilder.start. TL.exe separately has a native CreateProcessA call. These are desktop process assumptions; they are not LegacyForge's startup contract.

## Native and operating-system dependencies

**Confirmed [E04/E05]:** the installed native directory contains x86-64 glfw.dll, lwjgl.dll, lwjgl_opengl.dll, lwjgl_stb.dll, jemalloc.dll, OpenAL.dll and a JNA dispatch DLL. Metadata names LWJGL 3.3.3 components, including additional freetype/tinyfd native archives. An extracted directory snapshot is not an exhaustive dynamic-load inventory.

Static imports show:

- GLFW: USER32/GDI32/SHELL32/KERNEL32; CreateWindowExW and LoadLibrary/GetProcAddress paths.
- JVMs: Windows kernel/user/security/network/timer APIs plus VCRUNTIME140, VCRUNTIME140_1 and CRT API sets; VirtualProtect, process creation and dynamic loading.
- LWJGL components: dynamic loader and symbol lookup APIs; lack of a direct OpenGL DLL import does not prove OpenGL absence.
- OpenAL: WINMM, USER32, OLE32 and dynamic-loading APIs.

This parser covered standard PE imports, not delay imports, dynamic function names, all JNI exports, call reachability or Xbox API certification. No import-list-only conclusion claims every imported desktop API is unavailable on UWP.

**Confirmed historical evidence [E09]:** existing game log lines report LWJGL 3.3.3+5 and OpenAL initialization. They predate this analysis and were not reproduced; they establish recorded messages, not a new verified play session.

## Implications for LegacyForge

**Confirmed [E07]:** PreloadJvm loads packaged modules; RunEmbeddedMinecraft resolves JNI_CreateJavaVM. The project already patches Java filesystem/ZIPFS behavior and routes LWJGL/JNA paths, uses its GLFW shim and selects an OpenGL DLL. It also prevents starting a second JVM in the same launcher process, reflecting lifecycle limits.

**Confirmed source discrepancy:** ResolveJavaRuntimeInfo allows Java 17/8 families, while RunEmbeddedMinecraft assigns JNI_VERSION_21 unconditionally. **Unknown impact:** no older-runtime startup was run. Validate the invocation contract and runtime version per target before proposing a fix. Do not assume newer JNI invocation versions are accepted by an older runtime.

**Unknown:** complete Java/JNI/native ABI compatibility, graphics profile/extension support, audio/input behavior, resource pressure, suspend/resume and every loader's runtime effects on Xbox. See compatibility matrix and staged roadmap; desktop library downloads alone cannot resolve them.
''')

write('XBOX-UWP-COMPATIBILITY.md','''# Xbox UWP compatibility matrix

'''+HEADER+'''Feasibility below is scoped to the observed behavior, not a blanket verdict on Java or Xbox. Source implementation and user-reported Phase 5F.2 testing are not independent validation of each version/loader combination. [E07/E08]

| Component | Observed Windows behavior | Xbox UWP requirement / existing LegacyForge path | Evidence | Feasibility | Unknowns |
|---|---|---|---|---|---|
| Java runtime | Launcher 11+, bundled17; game1.21.11 requires21; desktop JVM APIs | Packaged adapted JVM, correct Java/JNI version; existing in-process host | E02/E04/E05/E07; [JIT memory API](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotectfromapp) | Inferred: existing host is relevant; direct desktop-runtime reuse unproven | JVM patches/imports/JIT/W^X, older JNI versions, console execution |
| Process launch | TL CreateProcessA; Java ProcessBuilder.start | Existing LoadPackagedLibrary + JNI_CreateJavaVM path | E03/E06/E07; [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw) | Unknown for arbitrary desktop subprocesses; avoid transplanting that assumption | Package/security context and child-process support; irrelevant subprocess options |
| LWJGL/JNI natives | Windows x64 DLLs and writable extraction directories | Package-compatible imports/ABI and native loading; existing override preparation | E05/E07; [LoadPackagedLibrary](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-loadpackagedlibrary) | Inferred: downloaded DLL presence alone is insufficient | Every selected/transitive DLL, dynamic loading routes, JNI exports |
| Graphics/windowing | GLFW desktop window APIs, LWJGL OpenGL bindings | Existing GLFW CoreWindow shim + Mesa runtime dependencies | E05/E07; [OpenGL ES porting](https://learn.microsoft.com/en-us/windows/uwp/gaming/port-from-opengl-es-2-0-to-directx-11-1) | Unknown per game/version; existing adaptation must be validated | Required desktop OpenGL context/extensions, shaders, presentation and performance |
| Input | Desktop GLFW/UI assumptions | CoreWindow/gamepad integration; Windows.Gaming.Input contract | E05/E07; [input for games](https://learn.microsoft.com/en-us/windows/uwp/gaming/input-for-games) | Inferred: UI navigation and gameplay input are separate validations | Focus, relative mouse, keyboard, controllers, lifecycle |
| Audio | Windows OpenAL imports; historical initialization messages | UWP-compatible audio backend and native ABI | E05/E09 | Unknown on Xbox for this exact selected dependency set | Device activation, mixing/latency, suspend/resume |
| Filesystem | Writable desktop cache, native extraction and process working directory | App-local writable storage; packaged runtime assets; existing Java patches | E03/E07; [file access](https://learn.microsoft.com/en-us/windows/apps/develop/files/file-access-permissions) | Confirmed: broadFileSystemAccess unsupported on Xbox; app package read-only | Path semantics, capacity, external content and native load paths |
| Authentication | OAuth/XBL/XSTS/Minecraft + ownership/profile | Existing PasswordVault and entitlement/profile gates | E03/E07; [device flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code) | Confirmed source exists; live service validation Unknown | Registration/scopes, renewal, service errors and account protection |
| Resources | Desktop process/JVM heap and native allocations | Actual Xbox package budget measured outside debugger | [Microsoft historical resource guidance](https://learn.microsoft.com/en-us/previous-versions/windows/uwp/xbox-apps/system-resource-allocation) | Unknown for deployed package | Package classification, memory/CPU/GPU, hardware/OS, non-debug measurements |

**Confirmed official contract:** VirtualProtectFromApp supports JIT with codeGeneration and disallows simultaneous write/execute protection. It is incorrect to conclude “UWP cannot JIT.” LoadPackagedLibrary searches the package dependency graph and disallows absolute/parent-traversal paths. Neither contract proves that this desktop JVM/native set works on Xbox.

**Confirmed official scope:** FullTrustProcessLauncher belongs to Windows Desktop Extension SDK and is not an evidenced Xbox escape hatch. Current generic CreateProcessW documentation includes UWP in its requirements; that row alone does not establish Xbox arbitrary desktop process permission. [FullTrustProcessLauncher](https://learn.microsoft.com/en-us/uwp/api/windows.applicationmodel.fulltrustprocesslauncher?view=winrt-26100)

The resource guidance is under previous-versions and dated 2017; its published 1GB app/5GB game figures require current package/device verification. No new hardware test occurred. Xbox gameplay feasibility remains **Unknown** for the unvalidated combinations identified here.
''')

gaprows=[
('Embedded JVM','Already implemented / Confirmed','MC.Xbox/launch/minecraft_launch.cpp',663,'PreloadJvm; RunEmbeddedMinecraft:1335 loads JVM and invokes JNI; do not replace with desktop subprocess'),
('Runtime families','Partial / Confirmed','MC.Xbox/launch/runtime_manager.cpp',1079,'ResolveJavaRuntimeInfo supports jre/jre21/jre17/jre8 and patches; file existence is not readiness'),
('Java/JNI version agreement','Unknown impact / Confirmed source discrepancy','MC.Xbox/launch/minecraft_launch.cpp',1353,'JNI_VERSION_21 fixed while catalog/runtime selection includes 17/8 families'),
('Version resolution','Already implemented at build time / Confirmed','scripts/new-download-manifest.ps1',547,'Official manifest v2 → version JSON → per-target TSV; live arbitrary-version console resolver not established'),
('Library rules','Partial / Confirmed','scripts/new-download-manifest.ps1',126,'Ordered Windows/x64 rules; os.version explicitly throws; feature contract needs work'),
('Conditional arguments','Partial / Confirmed','scripts/new-download-manifest.ps1',323,'Convert-ArgumentArrayToList extracts object.value without evaluating object.rules; scoped use at non-Fabric loader argument conversion'),
('Assets','Already implemented / Confirmed','scripts/new-download-manifest.ps1',534,'Add-Assets records index and hash-addressed object URLs'),
('Repair','Already implemented / Confirmed','MC.Xbox/launch/runtime_manager.cpp',770,'EnsureRuntimeDownloads checks SHA1, bounded workers, retries, temporary output and verified moves'),
('Classpath','Already implemented / Confirmed','MC.Xbox/launch/minecraft_launch.cpp',504,'CollectManifestLibraryJars and LoaderAdjustClasspath select game/loader libraries and packaged overrides'),
('Natives','Partial readiness / Confirmed','MC.Xbox/launch/runtime_manager.cpp',1310,'PrepareTargetNativeDir extracts selected archives and overlays packaged GLFW; presence checks do not prove ABI compatibility'),
('Graphics/window shim','Already implemented; behavior unverified here','glfw_shim/glfw_uwp.cpp',3009,'glfwCreateWindow/CoreWindow integration; mesa-runtime/README lists opengl32/libgallium_wgl/dxil/spirv_to_dxil/z-1 dependencies'),
('Fabric provider','Already implemented / Confirmed','MC.Xbox/launch/loaders/fabric.cpp',9,'FinalizeVersionInfo, CollectExtraClasspathJars, AddJvmOptions'),
('Forge provider','Already implemented; per-target validation Unknown','MC.Xbox/launch/loaders/forge.cpp',146,'PrepareForgeOfficialClientArtifacts; finalization/classpath/JVM/artifact hooks at568–648'),
('NeoForge provider','Already implemented; per-target validation Unknown','MC.Xbox/launch/loaders/neoforge.cpp',139,'Preparation plus finalization/classpath/JVM/artifact hooks at437–531'),
('Authentication/ownership','Already implemented / Confirmed','MC.Xbox/auth/minecraft_auth.cpp',391,'BuildMinecraftAuth with entitlement/profile gates; preserve unchanged'),
('Credential storage','Already implemented / Confirmed','MC.Xbox/auth/minecraft_auth.cpp',17,'PasswordVault refresh-token persistence; no plaintext-token finding established'),
('Token diagnostic redaction','Already implemented for game args / Confirmed','MC.Xbox/common/launch_diagnostics.h',9,'Handles separate and equals forms of accessToken; does not establish universal log redaction'),
('Local profiles','Already implemented / Confirmed','MC.Xbox/ui/launcher_ui.cpp',1083,'Local session Play/Repair gates; account distinction retained'),
('Installed mod buttons','Already implemented / Confirmed','MC.Xbox/mods/mods_browser.cpp',400,'MarkInstalledBrowseCards/RefreshDetailInstalledState use active profile and recorded project IDs'),
('Legacy 1.12.2 provider','Missing as catalog declaration / Confirmed','config/versions.tsv',56,'Forge and vanilla rows explicitly say legacy provider not implemented yet; not all older versions are supported'),
('Desktop startup transplant','Incompatible assumption / Inferred','MC.Xbox/launch/minecraft_launch.cpp',1335,'Project expects embedded/patched host; downloaded java.exe/standard GLFW is not demonstrated substitute'),
('Per-target gameplay readiness','Unknown','config/versions.tsv',14,'Experimental catalog rows are not independent console validation receipts')]
write('LEGACYFORGE-GAP-ANALYSIS.md','''# LegacyForge gap analysis

'''+HEADER+f'''Only approved commit `{PIN}` is compared. “Already implemented” describes source, not comprehensive execution validation. Source identifiers/hashes are retained in E07. Production/authentication/entitlement code was not changed.

| Area | Status | Exact source anchor | Finding |
|---|---|---|---|
'''+ '\n'.join(f'| {a} | {b} | {src(c,d)} | {e} |' for a,b,c,d,e in gaprows)+'''

## Priorities

**Proposed P0:** make runtime readiness explicit per target/runtime/JNI/native/graphics combination; investigate fixed JNI_VERSION_21 against Java17/8 catalog families before changing behavior. Current evidence is a source discrepancy, not a reproduced failure.

**Proposed P1:** define rule/argument handling and preserve fail-closed behavior for unsupported conditions. Extend repair with receipts and native/runtime outcomes. Do not label those core services missing.

**Proposed P2:** evaluate a live upstream version browser separately from the existing approved target catalog. Keep unsupported/experimental status visible and preserve ownership/account checks. No broad parity claim with Legacy Launcher is supported by this investigation.
''')

write('UNKNOWN-SUBSYSTEMS.md','''# Unknown subsystems and remaining evidence

'''+HEADER+'''| Question | Status / reason | Smallest next evidence |
|---|---|---|
| Exact installer payload → installed versions | Unknown: hashes identify archive artifact but installer not unpacked; newer JAR versions present | Nonexecuting Inno payload inventory with approved available parser; compare contained hashes separately |
| Upstream publisher authenticity | Unknown: installer/wrapper unsigned; archive metadata is uploader-controlled | Independently authenticated upstream release hashes or signed distribution evidence |
| Exact acquisition event | Unknown: mutable filesystem timestamps, no readable Zone.Identifier | User acquisition record or original retained download provenance |
| Native wrapper/bootstrap full linkage | Partial: strings/imports/process call and argument file known | Focused static references from resource/config parsing to JVM command construction |
| Bootstrap update trust/rollback | Unknown: signed-stream/checksum classes are structural evidence only | Trace key selection, signature enforcement, failure/rollback and update endpoints |
| Configuration precedence/atomic durability | Partial: settings/profile methods and temp move known | Focused branch analysis with synthetic data; execution needs separate approval |
| Exact Legacy Launcher Forge/Fabric flow | Unknown beyond version/library infrastructure | Scoped static loader/extra-version path and installer-process analysis; never execute installer implicitly |
| All auth-provider behavior/storage protection | Unknown: serializers include token payloads; no raw values inspected | Code-only protection/redaction/refresh tracing; synthetic data if later authorized |
| Full downloader recovery/security | Partial: size/hash/abort handling known | Trace retries, cache promotion, interrupted writes, path confinement, concurrency and integrity metadata trust |
| Official current auth contracts | Unknown live applicability of recovered endpoints | Official service documentation plus separately approved account test in isolated environment |
| Java17/8 with fixed JNI_VERSION_21 | Confirmed source discrepancy; execution impact Unknown | Supported JNI invocation negotiation test on exact packaged runtime; preserve account boundary |
| Every native transitive import/dynamic load | Unknown: standard imports only | Delay-import/export/ABI/API audit and exact packaged/native version matrix |
| Graphics/audio/input on Xbox | Unknown for this exact selected game/dependency/loader set | Approved isolated console tests with versioned logs and observable pass/fail criteria |
| Resource/suspend/resume behavior | Unknown: no new hardware observations | Exact console/OS/package identity; non-debug memory/GPU/CPU and lifecycle measurements |
| All experimental LegacyForge targets | Unknown: source/catalog presence and user Phase5F.2 test report are narrower evidence | Per target + loader + JVM + native/graphics results; controller mod compatibility |

Research does not require executing targets to resolve every static gap. Exhaust useful static methods first. Before installation, target execution, authentication, destructive changes or pushes, obtain the approval required by the mission. Approved execution must use an isolated environment with no personal credentials. No such approval was requested or exercised in this pass.
''')

write('PHASE-6-ROADMAP.md','''# Phase 6 engineering roadmap

'''+HEADER+'''These are independent implementation proposals, not production changes made by Phase 6A. Preserve current entitlement checks, Credential Locker storage, local-session boundaries, mods behavior and established Xbox adaptation.

| Priority / proposal | Existing code to extend | Concrete acceptance evidence |
|---|---|---|
| P0: target/runtime readiness record | ResolveJavaRuntimeInfo, ResolveVersionInfo, RunEmbeddedMinecraft, target catalog | Version/loader, runtime identity/major, supported JNI invocation, native hashes/ABI, graphics provider and explicit Unknown/Unsupported/Validated state |
| P0: resolve Java/JNI agreement | Fixed JNI_VERSION_21 assignment versus java17/legacy families | Independent synthetic invocation tests for exact packaged runtime; supported version chosen/negotiated, no false success; explicit failure with runtime identity |
| P1: deterministic metadata rule contract | Test-LibraryAllowed and Convert-ArgumentArrayToList | Fixtures for ordered allow/disallow, OS/arch/version/features, conditional string/array args, unsupported conditions and loader module options |
| P1: repair receipts | EnsureRuntimeDownloads and PrepareTargetNativeDir | Manifest hash + target, checked/reused/downloaded counts, mismatch/retry/cancellation results, promotion result and native/runtime readiness; no token values |
| P1: exact native/graphics validation | Existing GLFW shim, Mesa packaging, Java/native patches | Exact module versions/imports, JNI exports, minimal window/context/shader/presentation/input/audio probes |
| P2: version discovery UX | Existing build-generated target manifests/catalog | Distinguish upstream availability, downloaded state, experimental target and hardware-validated support; no automatic enablement from catalog presence |
| P2: loader-specific support expansion | Existing Fabric/Forge/NeoForge providers; missing 1.12.2 provider boundary | Reproducible processor/classpath/main/options output; explicit per-target unsupported outcomes; no reuse of proprietary launcher implementation |

Evidence motivating proposals: E03/E04 establish version-driven requirements; E07 establishes existing services and narrower gaps; E08 establishes platform contracts and remaining requirements. Any implementation should describe the permitted behavior independently, with synthetic fixtures and official metadata contracts, without copying proprietary code/resources.

## Future execution gates, requiring separate authorization

1. Verify package activation and actual console/OS/package identity.
2. Validate the selected JVM primitive and supported JNI invocation version in isolation.
3. Run a minimal synthetic Java entrypoint, filesystem/threading and error propagation.
4. Validate packaged JNI/native symbol loading and selected module identity.
5. Create the required graphics context, verify capabilities, draw/present a synthetic frame.
6. Exercise input/audio and suspend/resume within measured memory/resources.
7. Validate an owned authenticated game launch for one exact target/loader; redact receipts.
8. Expand only after recording exact versions, results, limitations and regressions.

These gates are proposed validation design, not tests performed in this research pass. Existing Phase5F.2 hardware testing reported by the user remains relevant context but cannot be extrapolated to all catalog targets. Download completion alone must never become a gameplay feasibility claim.
''')

# Only derived metadata goes in the publication boundary.
safe={'research_date':'2026-10-17','legacyforge_commit':PIN,'inventory_captured_utc':D['captured_utc'],'selected_files':D['selected_files'],'directory_summary':D['summary'],'installed_launcher':J['launcher.jar']['metadata'],'installed_bootstrap':J['bootstrap.jar']['metadata'],'selected_game':{k:D['version_metadata'][k] for k in ['id','mainClass','javaVersion','assetIndex']},'client_sha1_valid':D['client_sha1_valid'],'asset_verification':D['asset_verification'],'library_verification':D['library_verification'],'native_static_imports':R['imports'],'runtime_releases':R['releases'],'archive':A,'source_hashes':S['sourceHashes'],'limitations':['Static findings, no new target execution','Native parser covers standard imports only','Local metadata is not authenticated upstream metadata','No account data or token values collected']}
(DOC/'evidence/static-summary.json').write_text(json.dumps(safe,indent=2),encoding='utf-8')
with (DOC/'evidence/relevant-files.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['relative_path','bytes','sha256'])
 root=Path(r'C:\Users\arinze\AppData\Roaming\.tlauncher')
 for p in sorted((root/'legacy/Minecraft').rglob('*')):
  if p.is_file() and p.suffix.lower() in ['.exe','.dll','.jar']:
   h=hashlib.sha256(p.read_bytes()).hexdigest()
   w.writerow([p.relative_to(root).as_posix(),p.stat().st_size,h])
sig_safe=[]
for x in SIG:
 x['Name']=Path(x['Name']).name if 'ReverseLegacyCraft' in x['Name'] else x['Name'].split('\\.tlauncher\\')[-1]
 sig_safe.append(x)
(DOC/'evidence/signatures.json').write_text(json.dumps(sig_safe,indent=2),encoding='utf-8')

write('EVIDENCE-INDEX.md','''# Evidence index and reproducibility

'''+HEADER+'''## Findings ledger

| ID | Evidence / locator | What is Confirmed | Confidence and limit |
|---|---|---|---|
| E01 | archive metadata + local installer hashes/version + Windows Authenticode | Archive content match; local version fields/signature status; local timestamps | High for bytes/returned metadata; publisher and acquisition chain Unknown |
| E02 | launcher.jar META-INF/launcher-meta.json; bootstrap manifest and META-INF/bootstrap-meta.json | Installed launcher/bootstrap versions, entries, declared Java requirement/entrypoints | High static; no installer equivalence or execution implied |
| E03 | Focused Java bytecode methods listed below; local jar-static summaries | Direct invokes/constants/fields used for pipeline/auth/process claims | High for instructions; branches/reachability/exhaustive policy unproven |
| E04 | Local selected version JSON, client, libraries, asset index and objects | Local version requirements and hash comparisons; bounded file inventory | High against local metadata; no upstream authenticity or runtime verdict |
| E05 | Standard PE headers/imports and jre release files | CPU/subsystem/import names and declared runtime versions | High static; delay/dynamic imports and load behavior Unknown |
| E06 | REA Ghidra TL.exe evidence IDs below | Launch4j/javaw strings; native CreateProcessA call/reference | High static; wrapper/bootstrap argument chain partial |
| E07 | Exact approved LegacyForge commit and source hashes in static-summary | Functions and source discrepancies cited in gap analysis | High source; no independent hardware execution |
| E08 | Microsoft/Mojang official links in compatibility/provenance documents | Documented platform/license contracts, scoped to cited text | High documentary; current deployed package applicability may be Unknown |
| E09 | Existing game/logs/latest.log, lines 4/19/50 inspected with technology-only allowlist | Recorded LWJGL3.3.3+5 and OpenAL initialization messages | Historical, not reproduced; no raw log or account data retained in docs |
| E10 | launcher LICENSE.txt; JRE legal layout; linked official EULA | License notices and absence of demonstrated blanket redistribution grant | Documentary; legal clearance not established |

## REA records

REA 6.4.0 MCP was already connected. Official [README](https://github.com/morluto/rea) and [installation instructions](https://github.com/morluto/rea/blob/main/docs/installation.md) were read before analysis commands. Documented setup entry is `npx rea-agents setup`; no setup/update/configuration change was required or applied. Current upstream documentation may describe a later release; actual connected schemas and version controlled this investigation.

Ghidra 12.1.4 available with trusted JDK21.0.12.1; Hopper unavailable on Windows; IDA not configured. These are observed availability results, not installation attempts. Java analysis used ZIP/class parsing and trusted javap rather than pretending a REA Java decompiler ran.

| Operation / exact inputs | REA Evidence ID / result |
|---|---|
| binary_session({}) | No prior target open; server6.4.0; Ghidra available, Hopper/IDA unavailable |
| inspect_pe_resources(installer,max_file_bytes=134217728) | ev_161ae1604024412e2fe82e55c5c75b58b7cd7fac896200ee31a98a860e851858 |
| open_binary(TL.exe,provider_id=ghidra) | SHA256 2b11f487...; x86 PE |
| search_strings(regex bootstrap\\|tl.args\\|javaw\\|CreateProcess\\|Launch4j) | ev_c957ce041c8dac3c6abc5ea7cdcbc00fba0ff66a97dfb93abdfc8a43b7943a39; Launch4j0x40908a, javaw0x4094b3, CreateProcessA0x4144ae |
| find_xrefs_to_name(CreateProcessA) | ev_2d6e8b015ea8a740629560944e8aa79068bd2a6756e3de1c96fe5ab5235c2fbb; unresolved bare name; use qualified symbol |
| search_strings(regex bootstrap.jar\\|tl.args\\|tl.properties\\|jre) | ev_0828a5402616aa822a373d0692de9498ae1959cb017c45014799f959cf8b2434; defined JRE discovery strings |
| search_procedures(CreateProcess) | ev_1cd6be6e6a69c7e419093cb34d3bd64aa76a5733b3f23998ca3ebc3758b99db6; KERNEL32.DLL::CreateProcessA |
| procedure_references(KERNEL32.DLL::CreateProcessA,incoming) | ev_4fca140dc3ee7fd2c54bd33833b23bb74b60a1eb917c9e0a9c1f5a87231248b1; call0x40524e in FUN_00405126 |
| procedure_pseudo_code(0x405126) | ev_97cd5b6c09db60db112f2487d68956201dfbf582ebecb650ab6d0d943899f513; process call + wait/exit-code handling; stack-tracking warning retained locally |
| export_evidence_bundle(analysis-local/rea-evidence.json) | 7 records, 62,223 bytes; local-only because it includes reconstructed text |
| close_binary({}) | Successful; ephemeral analysis target closed |

Native analysis profile SHA256: `b9d116ea480a02cc8773b19372074a3caf77785cbc080b1ac7133b5110e40b17`. Ghidra evidence binds the original TL.exe hash. No target image modifications or broad decompilation occurred. Zero REA recorded unknowns is an API ledger count, not a claim this investigation has no unknowns.

## Focused Java method identifiers

- `net.legacylauncher.minecraft.launcher.MinecraftLauncher`: collectInfo, downloadResources, unpackNatives, constructClassPath, createJvmArgs, createArgumentsSubstitutor, constructProcess, launchMinecraft, killProcess, onJavaProcessEnded, onJavaProcessError.
- `net.minecraft.launcher.process.JavaProcessLauncher.createProcess`; ProcessBuilder.environment/start invokes in launchMinecraft.
- `net.minecraft.launcher.updater.OfficialVersionList.getRawList`; ExtraVersionList.getCompleteVersion; VersionSyncInfo.resolveCompleteVersion.
- `net.minecraft.launcher.versions.CompleteVersion`: getRelevantLibraries, getClassPath, getExtractFiles, addArguments; Library.appliesToCurrentEnvironment; Rule.getAppliedAction.
- `net.legacylauncher.managers.AssetsManager`: collectAssets/checkFile; AssetIndex.getHash/getPath; AssetDownloadable.onComplete; Sha1Downloadable.onComplete.
- `net.legacylauncher.jre.JavaRuntimeRemoteListFetcher.doFetch`; JavaRuntimeLocal.getExecutableFile; JavaManager.checkIntegrity.
- `net.legacylauncher.managers.ProfileManager.loadProfiles/saveProfiles`; MinecraftUserJsonizer token payload fields.
- `net.legacylauncher.user.minecraft.MinecraftOAuthAuthenticate.authenticate`; strategy.gos.GameOwnershipValidator.checkGameOwnership.
- `net.legacylauncher.ui.LegacyLauncherFrame` superclass JFrame; launcher metadata and nested bootstrap class structures.

Focused method evidence binds these identifiers to launcher.jar SHA256 `364b9add...`; nested bootstrap structural observations bind outer bootstrap SHA256 `09ba7517...`. Static invoke presence does not prove a branch executes.

## Local reproducibility

Tools: PowerShell7.6.5; Python3.14.7; git2.55.0.windows.5; trusted javap21.0.12.1 from the existing Ghidra JDK; REA6.4.0; Ghidra12.1.4. Analyst scripts use Python standard library only. No target JRE executable was invoked.

Working roots: research workspace `ReverseLegacyCraft`; target `.tlauncher/legacy/Minecraft`. The exact approved source is retained read-only at `analysis-local/legacyforge-d145343`; `git rev-parse HEAD` matched the pin and `git status --short` was empty.

Commands used to reproduce local observations, from the research workspace (these run analyst tools, not the target):

```powershell
python analysis-local/inventory.py
python analysis-local/runtime-evidence.py
python analysis-local/jar-static/inspect_jars.py
python analysis-local/jar-static/focus.py
git -C analysis-local/legacyforge-d145343 rev-parse HEAD
git -C analysis-local/legacyforge-d145343 status --short
Get-FileHash -Algorithm SHA256 -LiteralPath <artifact-path>
Get-AuthenticodeSignature -LiteralPath <exe-path>
```

Trusted static disassembly template: `<trusted-Ghidra-JDK>/bin/javap.exe -p -c -classpath <launcher.jar> <selected-class>`. Never replace it with running the target JAR or bundled runtime. Inventory script's local paths are explicit; reproduce against the same artifact identities, or change paths and record the new hashes. Read-only metadata request: `Invoke-RestMethod https://archive.org/metadata/legacy-launcher-for-minecraft`; only curated public fields were retained. Source acquisition used public HTTPS and a new detached checkout at the approved hash; no network authentication.

## Failures and limitations retained

- An initial unbounded rg inventory preview was truncated; grouped counts and relevant-file CSV replaced it. Truncated output was not used as full coverage evidence.
- An initial library verifier expected downloads.artifact.path; local normalized JSON omitted it. Deriving paths from artifact URLs produced107 entries,75 present/valid. No conclusion uses the erroneous initial zero count.
- Web renderer could not read the archive metadata/GitHub API JSON; direct unauthenticated HTTPS metadata reads succeeded.
- Java class parser initially misadvanced interface metadata; corrected and rerun. Two guessed class names were absent; real names were selected from ZIP inventory. No finding depends on those failed guesses.
- Bare CreateProcessA name lookup failed; qualified imported symbol then resolved. Ghidra decompilation had a stack-tracking warning, so exact process parameters were not inferred from unreliable stack rendering.
- No new target execution, installer extraction, live authentication, official component download, console test, or comprehensive third-party license review. Existing file hashes verify local content against local metadata, not trustworthiness.

## Publication files

`evidence/static-summary.json` contains curated artifact identities, directory counts, per-library hash results, standard native imports and pinned source hashes. `evidence/relevant-files.csv` contains relevant installed EXE/DLL/JAR paths, sizes and SHA256 only. `evidence/signatures.json` contains returned Windows signature/version metadata without personal paths. `evidence/SHA256SUMS.txt` binds the complete deliverable set.

Local-only `analysis-local` includes proprietary class structure/constants summaries and REA reconstructed text; it is outside the publication folder. No binary, asset, credential, raw profile or raw log is copied into the deliverables. None of the investigation output has been committed or pushed.
''')

with (DOC/'evidence/SHA256SUMS.txt').open('w',encoding='utf-8') as f:
 for p in sorted(DOC.rglob('*')):
  if p.is_file() and p.name!='SHA256SUMS.txt':f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(DOC).as_posix()+'\n')
print(json.dumps({'docs':str(DOC),'markdown_files':len(list(DOC.glob('*.md'))),'files':len([p for p in DOC.rglob('*') if p.is_file()])}))
