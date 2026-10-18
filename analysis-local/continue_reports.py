from pathlib import Path
import json,hashlib,csv,collections,re
BASE=Path(__file__).parent.parent;LOCAL=BASE/'analysis-local';DOC=BASE/'docs/research/legacy-launcher';SRC=LOCAL/'legacyforge-d145343'
PIN='d1453434ceefe73bef5aff497194e09f39dde7e1'
I=json.loads((LOCAL/'installer-payload-evidence.json').read_text());H=json.loads((LOCAL/'installer-header-evidence.json').read_text());N=json.loads((LOCAL/'native-audit-local.json').read_text());F=json.loads((LOCAL/'jar-static/continuation/static-flow-evidence.json').read_text());X=json.loads((LOCAL/'extended-static-local.json').read_text());C=json.loads((LOCAL/'decoder-crosschecks.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,s):
 p=DOC/name
 if p.exists():
  assert p.read_text(encoding='utf-8')==s.strip()+'\n',p
  return
 p.write_text(s.strip()+'\n',encoding='utf-8')
def replace(name,old,new):
 p=DOC/name;s=p.read_text(encoding='utf-8');assert old in s,(name,old);p.write_text(s.replace(old,new),encoding='utf-8')
def append(name,s):
 p=DOC/name;p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n'+s.strip()+'\n',encoding='utf-8')
def link(p,n):return f'[{p}:{n}](https://github.com/AlgorHome/LegacyForge/blob/{PIN}/{p}#L{n})'
HEADER='Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.\n\n'

write('INSTALLER-CONTENTS.md', '# Archived installer contents and installed comparison\n\n'+HEADER+'''## Verified nonexecuting recovery [E11]

The installer SHA256 remains `a7c997ba3c3e91c048f80f96f08754948428f6d3fe4001bab79c4ae09d06c5e0`. Independent Python standard-library inspection recovered the Inno Unicode data-format marker `6.1.0` at file offsets751888 and115841256. The marker is a storage-format identifier, not proof of the exact installer compiler release.

The valid metadata block starts at115841320: stored999,527 bytes, decoded5,085,511 bytes, header and244 chunk CRC32 checks validated. Decoded SHA256: `b1c3a29ec0144f6b4613d0ba5d64f05c9693ec32d04000ffb7c21c20714927c3`. The second checked block starts116840856, stored10,884 bytes, decoded56,980 bytes; its770 location descriptors each occupy74 bytes.

The single solid data chunk begins1202688 and uses LZMA2 with a2,097,152-byte dictionary. Decoding produced432,715,852 bytes. SHA256 of the filtered solid stream is `98f38fa6ec39b19762aa2d4106f5c9e95e71258cc479f17056979dcd0ccc76dc`. All770 payload records match their declared SHA1 after reversing the applicable x86 instruction-storage transform. Of these,622 already match before transforming;148 need the inverse transform. No installer, JAR, EXE or DLL was run. Only two original JARs and the installed nested bootstrap application JAR were materialized locally for static inspection, outside the publication folder.

The decoder is a bounded inspector for this exact format/artifact, not a general installer extractor. Format mechanics were checked against [innoextract stream/data sources](https://github.com/dscharrer/innoextract/tree/master/src); code was not taken from the proprietary launcher. CRC/SHA1 consistency establishes internal decoding correctness, not upstream publisher authenticity.

## Original versus installed identity

| Artifact | Installer payload | Installed snapshot | Conclusion |
|---|---|---|---|
| launcher.jar | 5,441,684 bytes;1.159.2+legacy; SHA2565f1f1b8ef187c5fcea69830d4dec87c84447a6c134c314fe5a840340e4ee5e6c | 5,496,812 bytes;1.169.4+legacy; SHA256364b9add9a3b0e74e553439b3f0e33a573bb5d28667adc028180d509b0459eec | Confirmed different payloads |
| bootstrap.jar | 9,612,033 bytes;1.32.2+legacy; SHA256df2d2516e905cdc87a68ec456f881664a5b158ba810934251d7b70a740679588 | 11,026,138 bytes;1.40.3+legacy; SHA25609ba7517c8a9b30780ff9a6de230b8905247835ae0da914d66991e2b3b4b6c4e | Confirmed different payloads |
| Native/runtime/dependencies | 770 decoded records; declarations include root JRE and jre/x86 | 431 installed non-game files have SHA1 equal to an installer record, including the wrapper | Confirmed shared content; not a complete historical update chain |
| Minecraft client/assets | No game-cache destination in the inspected installer destination declarations | 1.21.11 client, libraries/assets and Java21 runtime exist | Inferred later on-demand installation; installer itself is a launcher/runtime distribution |

Original launcher metadata declares `ru.turikhay.tlauncher.TLauncher` and34 library descriptors. Its older namespace alone does not identify another similarly named product. Original bootstrap contains5,275 ZIP entries; launcher1,422. Both have now been examined separately from installed copies. [E11/E13]

**Confirmed wrapper configuration:** TL.exe contains `jre;x86` at file offset408392, `-Xmx128m -Dtlauncher.bootstrap.restartExec=TL.exe` at408404, `launcher\\bootstrap.jar` at408456 and `_JAVA_OPTIONS=-Dtlauncher.launch4j=true` at408484. Alongside the earlier native CreateProcessA call, this establishes declared native-wrapper/bootstrap linkage. Actual command-line expansion and resulting runtime process remain unexecuted. [E06/E11]

**Unknown historical facts:** exact update/download timestamps and intermediate builds, whether an external/manual replacement occurred, original acquisition event and independently authenticated publisher signature/hash. Decoding the installer cannot reconstruct events that were not recorded. Current publisher pages corroborate product naming and research-only source availability, not the archived artifact's authenticity.

Machine evidence: `evidence/installer-payload-summary.json`; local decoder commands in EVIDENCE-INDEX. Destination strings are retained as declarations; their order was not promoted into a formally parsed file-table/path-to-record mapping. Content matches use hashes independently of that order.
''')

write('UPDATE-AND-RECOVERY.md','# Bootstrap updates, configuration, accounts and recovery\n\n'+HEADER+'''## Signature and update handling [E12/E13]

This continuation distinguishes archived bootstrap1.32.2 from installed1.40.3. Both contain direct signature-checking instructions, rather than merely suggestive class names.

| Observation | Exact static locator | Status / scope |
|---|---|---|
| Installed update URI template | UpdateMeta$1.lambda$fetchUpdateMeta$0 offset3: https://%s/%s/bootstrap.json.mgz.signed | Confirmed endpoint construction; selected host/traffic not observed |
| Signature required for signed-path response | Installed UpdateMeta.readQueue: URL.getPath→endsWith(.signed) offsets73–81; SignedStream construction120–126; explicit validateSignature155 | Confirmed conditional policy; not universal signing of every possible URL/input |
| Archived response verification | Archived UpdateMeta.fetchAttempts: .signed114, SignedStream157/163, explicit validateSignature192 | Confirmed older implementation has corresponding path |
| Signature framing/key | SignedStream.readSignature expects256 bytes; installed class initializer reads public.der, builds X509EncodedKeySpec/RSA key | Confirmed compiled trust anchor; source/public-key rotation policy unknown |
| Algorithms | ChecksumStream uses SHA-256; validateSignature encodes digest text; verify selects SHA1withRSA | Confirmed exact historical scheme; do not call it SHA256withRSA or invent a vulnerability |
| Failure | Missing/truncated framing throws StreamNotSignedException; invalid verification throws InvalidStreamSignatureException; signature exception returns false | Confirmed narrow failure branches; interruption/real remote responses untested |
| Metadata parsing | UpdateMeta.fetchFrom reads stream to string and Gson; readQueue explicitly validates before accepting signed result | Confirmed static order; callers supplying raw inputs are a separate trust boundary |
| File download | bootstrap DownloadTask.downloadUrl: connect10,000ms, read5,000ms; temp file; SHA256 compare when supplied; create destination directories; Files.copy(REPLACE_EXISTING) | Confirmed; replacement copy is not evidence of atomic replacement or power-loss durability |
| Copy/retry/cleanup | DownloadTask executes URL candidate loop; handles copy/lock failures; temporary file deletion on normal/finally paths | Confirmed branches; all filesystem failure combinations require dynamic tests |
| Bootstrap self-replacement | Updater.doUpdate downloads to temp; reopens input/output and copies; Updater.execute optionally restarts via ProcessBuilder.start | Confirmed; traced method has no demonstrated transactional old-version backup/rollback |
| Launcher selection | Bootstrap$4.execute compares local/remote versions and SHA256; can retain newer local version or fetch remote; Bootstrap$1 downloads libraries; Bootstrap$2 invokes IPC start | Confirmed source behavior; exact historical update chain remains Unknown |

Raw public keys and reconstructed method listings stay local. The presence of a signature scheme does not authenticate a separately obtained installer and does not establish every update transport policy.

## Configuration and profile persistence [E12]

SimpleConfiguration.save writes Java Properties to `<settings>.tmp`, closes the stream, then Files.move. ProfileManager.saveProfiles writes Gson JSON to a temporary sibling and moves with REPLACE_EXISTING. The observed ProfileManager call uses no ATOMIC_MOVE flag. ProfileManager.loadProfiles has migration/read-error/backup-writing branches. This improves the previous “configuration recovery untraced” status, but no crash/power-loss or full-disk tests were run.

MinecraftUserJsonizer MicrosoftTokenPayload constructor directly copies access-token/refresh-token strings and expiry into payload fields; MinecraftTokenPayload copies game token and expiry. Its serializer uses Gson to build JSON, which ProfileManager writes through normal Java output streams. **Confirmed:** token strings are application-level JSON serialization fields in this traced persistence path; no encryption/vault operation appears on that path. **Unknown:** actual saved account contents, OS encryption/ACLs and protections outside this path. No real token/profile was read and no vulnerability is asserted solely from architecture.

MinecraftOAuthRefresh.refreshIfNeeded first attempts a profile request with the supplied game token; a profile-request exception routes to refreshExplicitly. refreshExplicitly repeats Microsoft refresh→XBL→XSTS→Minecraft→ownership→profile→conversion. Plain/authlib/Ely/Mojang/Microsoft provider classes and serializers remain separate. Do not carry alternative-provider behavior into LegacyForge's legitimate ownership boundary.

## Game downloader recovery [E12]

DownloaderTask.run distinguishes PartialDownloadException, GaveUpDownloadException and AbortedDownloadException; exhausted/error branches remove destination/auxiliary files and notify completion/error handlers. downloadURL supports partial-file length checks and append output, Accept-Ranges/resume handling; setupConnectionFollowingRedirects handles Range/206, success codes and301/302/307/308 Location redirects, with a10-redirect limit branch. DownloaderTask.download separates local I/O failures from remote retries/fallback. Sha1Downloadable/AssetDownloadable still validate content at completion.

**Unknown until execution:** actual retry timing under packet loss, interruption races, disk-full results, final-file visibility during partial writes and metadata trust under hostile replacement. Static path extraction into a directory does not establish canonical path confinement; all untrusted ZIP paths and repository-controlled destination normalization need their own explicit validation. No “safe extraction” or remotely exploitable finding is inferred without reachability/reproduction.

## Independent LegacyForge implications

Keep content integrity, metadata authenticity, transaction/durability and account protection separate. Extend existing repair receipts. Preserve PasswordVault and entitlement checks. If independently designing signed metadata, specify a current approved trust/rotation policy; do not copy this launcher's key material or historical algorithm choices. Windows fault-injection tests in WINDOWS-SANDBOX-TESTS are BLOCKED.
''')

write('LOADER-RESOLUTION.md','# Forge/Fabric and version inheritance resolution\n\n'+HEADER+'''## Archived and installed launcher paths [E13]

The original installer launcher1.159.2 has now been inspected alongside installed1.169.4. This resolves the earlier lack of original-build pipeline evidence.

**Confirmed:** original OfficialVersionList.getRawList offset4 embeds the Mojang version_manifest.json endpoint. Repository enum initialization calls TLauncher.getOfficialRepo/getExtraRepo/getAssetsRepo/getLibraryRepo and uses local/official/extra version repositories. Original ExtraVersionList.getCompleteVersion builds `versions/<id>.json`, parses CompleteVersion, and assigns version/source metadata. These are declarative version profiles; a Forge/Fabric download is not one monolithic game bundle.

**Confirmed:** original CompleteVersion.resolve carries an inheritance-history list, raises DuplicateInheritanceException on duplicate inheritance and ParentNotFoundException when a parent cannot be resolved, recursively resolves the parent, and copies child state into the result. resolveFamily recognizes Forge/Fabric families. Installed equivalents preserve the same broad version/library/argument abstraction; exact metadata merge details are build-specific and should not be replaced by an invented universal algorithm.

**Confirmed:** original MinecraftLauncher.processModpack requests rule-filtered mods and branches by ModpackType. Forge-family paths construct a temporary ModList file and `--modListFile`, or `--fml.mods` and `--fml.mavenRoots` arguments according to the branch. It records a warning and returns an empty list if mod-list generation fails. The same method family exists in installed code. This is evidence of launcher metadata/modpack preparation, not execution of an official Forge installer.

**Confirmed:** RepositoryProxy includes files.minecraftforge.net and maven.fabricmc.net host constants in the original snapshot; installed snapshot expands proxy configuration. Static library repositories include official Minecraft libraries/assets plus launcher-configured fallback/repository machinery. The active mirror, returned loader version JSON and exact remote-generated patched artifacts were not captured. No private launcher mirror was queried to obtain game/loader binaries.

**Important limit:** these artifacts establish consumption of extra version profiles, library resolution, parent merging, native/classpath/argument preparation and Forge-family mod lists. They do not establish that the inspected launcher runs every official Forge/Fabric installer or locally reproduces every upstream processor. A dedicated independent Fabric/Forge processor specification must use current loader documentation and exact target metadata. The static index does not justify claiming universal processor parity.

The original launchMinecraft method calls JavaProcessLauncher.createProcess at189, ProcessBuilder.environment at194 and ProcessBuilder.start at321. downloadResources calls JavaManager.installVersionNow and VersionManager.downloadVersion. Thus the archived artifact itself supports the external desktop game JVM model documented for the installed build.

## Mapping to LegacyForge

LegacyForge's exact pinned source already implements distinct Fabric, Forge and NeoForge providers. Its manifest generator obtains Fabric profile JSON and Forge/NeoForge installer/profile metadata from their upstream repositories; its native host performs loader-specific artifact/classpath/JVM preparation. See DOWNLOADS-TO-LEGACYFORGE and the gap analysis for exact functions.

**Proposed:** independently normalize upstream metadata into a plan containing exact parent chain, libraries/native classifiers, loader processors, main class/module/classpath, conditional arguments, Java/runtime target and verified artifacts. Keep that plan distinct from executing processors or claiming Xbox support. Legacy Launcher's extra-version profiles can explain an architectural pattern; their code, server data, patched libraries and resources are not to be copied into LegacyForge.

All56 pinned catalog targets are retained in `evidence/target-validation-matrix.csv`; no target was removed to reduce scope. Exact loader and runtime support still requires per-target execution. Static source/catalog checks are not gameplay tests.
''')

counts=collections.Counter(x['architecture'] for x in N['images'])
write('NATIVE-DEPENDENCIES.md','# Native dependency and platform boundary audit\n\n'+HEADER+f'''## Coverage [E14]

All239 installed target EXE/DLL files and6 pinned Mesa DLLs were parsed. Recursive ZIP inspection added46 DLL occurrences from native archives (up to two nested JAR levels;64MiB per entry). Total291 PE observations: {counts['x86_64']} x86-64, {counts['x86']} x86 and {counts['arm64']} ARM64. No parser errors were recorded. Duplicate archive/extracted copies are occurrences, not291 distinct runtime-loaded modules.

The audit recorded1,714 standard/delay-import module edges,46 delay-import module occurrences and56,489 named-export entries across these images. External/system/API-set edges are explicitly unresolved. Candidate matches are by module basename, role and CPU; they do not emulate loader order. Graph metadata is in evidence/native-dependency-graph.json; no DLL contents are published.

Representative import-module sets independently matched GNU objdump for TL.exe, selected GLFW, OpenAL and Java17 JVM. Eight selected Java classes also matched trusted javap checks, including original process launch, original/installed signature code and profile persistence. These12 analyzer cross-checks passed; they are **not**12 passed target/runtime tests.

## Actual pinned adaptation [E15]

- '''+link('MC.Xbox/launch/minecraft_launch.cpp',663)+''': packaged runtime preload; JNI_CreateJavaVM at1335 onward; native path overrides1179–1203.
- '''+link('MC.Xbox/launch/runtime_manager.cpp',1079)+''': runtime family/patch selection; PrepareTargetNativeDir1310 selects/extracts natives and overlays packaged GLFW.
- '''+link('glfw_shim/glfw_uwp.cpp',1563)+''': PollGameInputGamepad uses GameInput readings; controller-to-GLFW buttons/axes conversion and keyboard/mouse bridges exist.
- GLFW exports at3952 swap through WGL bridge or EGL; glfwGetProcAddress3987 tries WGL, EGL and packaged OpenGL entrypoints. A working backend requires actual context/function/presentation validation.
- glfwExtensionSupported3978 always returns false; glfwGetWin32Window4122 returns NULL. glfwGetJoystickHats returns no hats and glfwUpdateGamepadMappings returns success without applying supplied mappings. These are **Confirmed interface limitations**, not proof every game/mod fails. Test consumers that use these interfaces.
- '''+link('MC.Xbox/App.cpp',112)+''': suspension logs/marker/telemetry and resume marker clearing exist. This does not prove game audio/context/resource restoration or safe native/JVM reuse.

Pinned Mesa DLLs are opengl32, libgallium_wgl, dxil, spirv_to_dxil, vulkan_dzn and z-1. The import graph shows app CRT dependencies in several Mesa components; opengl32 imports libgallium_wgl and the latter imports z-1. Presence of vulkan_dzn does not prove the selected Minecraft path uses Vulkan. dxil includes desktop-named imports; import spelling alone does not establish Xbox API compatibility.

## Package and missing runtime artifacts

Package.appxmanifest declares x64 Windows.Universal and VCLibs plus internet/private networking, runFullTrust, broadFileSystemAccess, expandedResources and microphone. No explicit codeGeneration declaration was found in that checked manifest. This is a recorded declaration set, not proof of a capability grant, certification or JIT prohibition. Microsoft's documented UWP JIT route exists; exact modified-runtime memory/API behavior requires validation.

No built APPX/MSIX/LegacyForge executable, packaged JVM or built GLFW shim was present in the pinned checkout inventory. Six Mesa binaries can be audited, but the exact deployed JVM/shim package cannot be hashed or tested from absent files. All catalog runtime tests remain BLOCKED, with the source comparison retained for all56 rows.

## Remaining load-time unknowns

Static import/export inventories cannot resolve all GetProcAddress targets, generated code, registration via JNI_RegisterNatives, actual dependency search order, device drivers, shader/runtime feature support or lifecycle outcomes. Archive x86/ARM64 natives must not be selected merely because their files exist; the actual Xbox package/native selection is x64. No audit result declares arbitrary Windows DLLs UWP-compatible.

Oracle's [JNI invocation contract](https://docs.oracle.com/en/java/javase/17/docs/specs/jni/invocation.html) makes requested JNI version part of the API contract. The pinned host requests JNI_VERSION_21 while Java17/legacy runtime selections exist. The discrepancy is confirmed; its exact packaged-runtime response is BLOCKED pending those binaries and an approved isolated/device test. No target JVM was loaded through ctypes, JNI, reflection or another host during this investigation.
''')

write('WINDOWS-SANDBOX-TESTS.md','# Reproducible isolated Windows test procedure\n\n'+HEADER+'''**Status: BLOCKED.** User confirmed no configured isolated Windows VM/Sandbox and explicitly prohibited archived-launcher execution until an isolated environment is available and approved. No Windows features were enabled, VM created or software installed. Read-only Hyper-V enumeration returned insufficient permission; Windows Sandbox was not found at the checked standard path. Existing installed7-Zip19 could only identify an incomplete ZIP fragment, so it was not treated as a valid Inno inventory. The independent decoder completed static inventory without installation.

## Environment the owner must prepare

Use a disposable Windows11 VM or supported Windows Sandbox edition, a fresh local user and no personal credentials. Obtain separate approval before creating/installing/enabling infrastructure or executing the archived launcher. Keep the original installer hash fixed. Start from an offline VM checkpoint, with no shared clipboard, host home-directory mount, host credential store, printers, audio/video redirection or personal data. Map only a dedicated research-artifact folder read-only and copy working files into the guest's disposable disk. Keep all target writes in the guest.

The included `tests/offline.wsb.example` is a reviewable template only: it has no automatic launcher command and has not been activated. Windows Sandbox configuration and edition requirements are documented by [Microsoft](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/); [WSB controls](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) govern networking/redirection/mappings. Do not treat a GPU-disabled synthetic renderer as a performance test.

## Test matrix (every row currently BLOCKED)

| ID | Controlled action after approval | Expected evidence / pass criterion |
|---|---|---|
| W01 | Verify guest isolation and hashes before launching | Guest OS/build/account class; no personal stores/mappings; exact installer SHA256; network-disabled state |
| W02 | Snapshot guest, run installer offline into guest-only location | Installation receipt/exit, guest-only file inventory/hashes, uninstall/shortcut/config changes; compare770 payload identities; do not execute uninstaller implicitly |
| W03 | Launch archived launcher offline | Actual wrapper→bootstrap→launcher process tree and JVM command identities; no successful network calls; missing-cache errors/cancellation visible |
| W04 | Start from empty guest game cache; approve narrowly scoped public network downloads | Recorded catalog→version JSON→client/library/native/asset/runtime requests, status/size/hash and destination; no Microsoft sign-in |
| W05 | Compare warm-cache versus empty-cache preparation | Existing valid content reused, missing/corrupt synthetic copies re-fetched; complete receipts; only guest test files may be altered |
| W06 | Interrupt transfer and resume using guest snapshot/test copies | Bounded retries, partial-range behavior, final hash checking, no success for truncated output |
| W07 | Simulate full/readonly guest test volume and cancellation | Explicit error and recoverable state; no false install completion; preserve snapshot for comparison |
| W08 | Exercise configuration/profile migration with synthetic empty accounts only | Settings precedence, temporary-file and replace behavior, malformed JSON/error backup, restart persistence; no real token values |
| W09 | Isolated synthetic update fixtures with valid/invalid/truncated signatures | Signed-path acceptance/rejection and failure receipts; no internet-controlled target update or authentication; do not alter production code to force success |
| W10 | Test each loader path identified from exact metadata | Parent/duplicate resolution, native/classpath/options and processor behavior; pin every artifact; no blanket Forge/Fabric parity result |
| W11 | Game process/exit/error controls after explicit game-execution approval | Correct JVM major, args/native identities, exit handling and UI restore; game/account requirements respected |
| W12 | Optional owner-controlled account tests, separately authorized | Microsoft/XBL/XSTS/Minecraft/ownership/profile outcomes only; no account names, tokens, device codes or raw auth traffic retained |

For W04 onward, change only the guest test environment and record the approval and resulting network mode. Never enable networking by editing the offline template silently. Use a fresh snapshot for update/authentication experiments. Negative tests must not delete or corrupt host files. Restore the disposable guest snapshot only with owner approval; this report performs no destructive action.

## Receipt discipline

Use `tests/result.template.json`. Record test ID, exact artifact/package hashes, environment build, action, expected/observed result, exit/HRESULT, failure classification and sanitized counters. PASS requires an actual observation satisfying the stated criterion. UNTESTED/BLOCKED is not PASS; an inconclusive run records INCONCLUSIVE. Do not save raw command lines containing account arguments or browser/auth captures. Desktop success does not establish Xbox compatibility.
''')

write('XBOX-SERIES-X-TESTS.md','# Xbox Series X owner-run validation procedure\n\n'+HEADER+'''**Status: BLOCKED.** Real Xbox Series X/Developer Mode and prior APPX deployment were reported by the owner. No Device Portal address or Codex remote access is configured. The owner can install approved packages manually. No console connection, authentication, deployment or execution was attempted. No credentials are requested or stored.

## Prepare a reproducible package and baseline

Use exactly LegacyForge commit `d1453434ceefe73bef5aff497194e09f39dde7e1`, preserve production authentication and entitlement code, and record any separately approved diagnostic-source changes in an independent package/repository. Do not silently use a later main revision. Record APPX SHA256, package identity/version, dependencies, exact packaged JVM/shim/Mesa hashes, console OS/build and Developer Mode state. A source checkout with six Mesa DLLs is insufficient to identify a deployed runtime.

The owner builds/signs the approved package using the repository's existing `build.ps1` and documented prerequisites in a separate build workspace; command flags must be checked against that pinned script before use. This investigation did not build or install it. Do not point a build at the read-only evidence checkout. Source `scripts/validate-modern-version-matrix.ps1` checks staged manifest/artifact/config presence; it is not a gameplay test and was not run against nonexistent staging outputs.

The owner uses their existing Developer Mode deployment route. If Device Portal is later configured, the owner retains credentials and performs sign-in locally. See [Microsoft Xbox tools](https://learn.microsoft.com/en-us/previous-versions/windows/uwp/xbox-apps/introduction-to-xbox-tools) and [Device Portal API family coverage](https://learn.microsoft.com/en-gb/previous-versions/windows/uwp/debug-test-perf/device-portal-api-core). Do not assume desktop dump endpoints exist on Xbox. No network connection is authorized by this procedure alone.

## Gates (all BLOCKED pending owner execution)

| ID | Action / evidence | Pass criterion |
|---|---|---|
| X01 | Owner installs approved exact package; record identity/build/dependencies | Package activates on Series X; actual executable/runtime hashes match receipt |
| X02 | Run outside debugger and measure memory/CPU/GPU during launcher idle/load | Actual package resource budget recorded; no inference from historical generic limits or expandedResources declaration |
| X03 | Synthetic JVM invocation for each current/java21/java17/legacy package | LoadPackagedLibrary/JNI API result, requested/accepted JNI version, Java major and exception result captured; no game/account required |
| X04 | Synthetic filesystem/thread/ZIPFS tests using app-local data | Read/write/rename/ZIP behavior within allowed roots; no broad-file capability assumption |
| X05 | JNI/native load probe against exact packaged/selected modules | Every required module/dependency/symbol resolves through actual package policy; full errors retained without credentials |
| X06 | Graphics probe: context version/profile/extensions, shader compile/link, draw/present | Required backend/capabilities verified; compare actual GL extensions with glfwExtensionSupported behavior; no success from an empty window alone |
| X07 | Controller, keyboard, pointer/focus/disconnect/reconnect | Button/axis/mouse/UI behavior matches explicit expectations; test mapping/hats/Win32-HWND-dependent consumers separately |
| X08 | Audio probe including device loss | Playback/capture policy, device switching, latency/failure result measured; historical desktop OpenAL log is insufficient |
| X09 | Suspend/resume and terminate/relaunch | No stuck keys, invalid context/audio, save loss or unsafe second-JVM reuse; record lifecycle markers and frame/resource changes |
| X10 | Download/repair of approved target with existing account gate respected | Exact manifest/counters/hashes; no bypass to make Local Launcher Mode repair/play succeed |
| X11 | Owner-authorized legitimate owned target launch | Existing entitlement/profile checks pass legitimately; exact version/loader/runtime/native/graphics tuple recorded; gameplay observable |
| X12 | Repeat per catalog row and regression profile | Each of56 rows independently PASSED/FAILED/BLOCKED/INCONCLUSIVE; unsupported legacy provider remains explicit |
| X13 | Phase5F.2 UI regression | Installed/Installed-Off persistence, no duplicate install, correct active profile, failed download and account gates retained |

X03–X08 require a separately built synthetic diagnostic package or approved diagnostic mode; no such package exists in the supplied artifacts and none was fabricated as a completed test. X10/X11 must respect existing ownership conditions and need separately authorized owner account use. The owner must not provide credentials, access/refresh tokens, codes, account names or raw authentication logs to Codex.

## Complete matrix and return format

`evidence/target-validation-matrix.csv` contains all56 approved catalog rows:20 Fabric,18 Forge,17 NeoForge and1 vanilla;12 current,40 Java21,2 Java17 and2 legacy runtime assignments. Four rows have source support level testing and52 experimental; these labels are not passed tests. Every new runtime verdict is BLOCKED until evidence arrives. The two1.12.2 rows explicitly lack their provider in the catalog.

Return only an allowlisted receipt using tests/result.template.json: test/target IDs, package/JVM/native hashes, console OS/build, result/HRESULT, counts, measured timings/resources and a brief sanitized symptom. Keep local raw logs private until reviewed/redacted. Phase5F.2 testing reported by the user is retained as user-provided UI regression evidence; the pinned PHASE-5F2.md still says validation pending, so there is no checked-in independent runtime receipt to extrapolate from.
''')

write('PHASE-STATUS.md','# Full Phase 6A status and completion criteria\n\n'+HEADER+'''No phases or catalog targets have been removed. This ledger separates static research delivered from infrastructure-dependent work that cannot presently be performed.

| Phase | Static result | Remaining outcome / status |
|---|---|---|
| A — Environment/provenance | Archive content matched; installer decoded and all770 payload hashes validated; original/installed version identities separated;431 installed content matches | Historical acquisition/update events and unsigned publisher authenticity Unknown; runtime installer observation BLOCKED |
| B — REA | Connected6.4.0/Ghidra12.1.4 used; evidence exported; trusted Java/PE parsers and independent analyzer checks recorded | No setup/install needed; no provider failure was presented as successful analysis |
| C — Architecture | Original and installed entrypoints/UI/config/profile/update/process boundaries traced; config persistence and update conditional verification expanded | Lifecycle/fault/recovery observations BLOCKED; static branch presence is not runtime outcome |
| D — Installation | Official/extra version resolution, inheritance, library/native/assets/runtime/classpath/argument and Forge-family metadata paths documented | Exact remote version-profile/processor results and interrupted downloads require approved isolated tests: BLOCKED |
| E — Authentication | Original/installed auth/ownership chain, refresh, token serialization and LegacyForge secure-storage/gates compared | Present service registration/permission and live ownership behavior Unknown/BLOCKED; no credentials collected |
| F — JVM/native/UWP |291 PE observations, delay-import graph, exact package declarations, JNI discrepancy, shim limitations and existing adaptations documented | Actual packaged JVM/shim not supplied; Windows/console execution/JIT/graphics/audio/input/lifecycle BLOCKED |
| G — LegacyForge gaps | Exact approved commit compared; all56 target rows retained with source support/runtime/loader assignments | No independent per-target hardware receipts; all new runtime verdicts BLOCKED |
| H — Deliverables | Required12 documents retained and extended; additional installer/update/loader/native/test/status documents and sanitized evidence provided | No claim all behavioral tests or hardware criteria have passed |

## Mission completion criteria

- Archived application identity and relevant inventory: **Confirmed**, including original launcher1.159.2/bootstrap1.32.2 extracted statically.
- Installation/launch paths documented as far as observed static evidence permits: **Delivered**, with original/installed differences and unobserved remote/processor boundaries retained.
- Java/native dependencies identified: **Delivered static inventory**, not runtime certification.
- Xbox incompatibilities/unknowns: **Delivered**, including specific GLFW interface limitations and missing deployed runtime evidence.
- Exact LegacyForge comparison and actionable roadmap: **Delivered**, without production changes.
- No prohibited artifacts committed/pushed: **Confirmed for this investigation**; research folder includes derived metadata and original prose/tools/templates only.
- Dynamic Windows/Xbox verification requested later: **BLOCKED**, not PASSED or silently omitted.

The owner explicitly confirmed no approved isolated Windows environment and no Codex console access, and instructed static-only work. These constraints prevent honest execution completion. Test procedures and receipts are prepared so the remaining work can resume without changing scope once infrastructure and execution approval exist.
''')

(DOC/'tests').mkdir(exist_ok=True)
(DOC/'tests/offline.wsb.example').write_text('''<Configuration>
  <Networking>Disable</Networking>
  <ClipboardRedirection>Disable</ClipboardRedirection>
  <AudioInput>Disable</AudioInput>
  <VideoInput>Disable</VideoInput>
  <PrinterRedirection>Disable</PrinterRedirection>
  <vGPU>Disable</vGPU>
</Configuration>
''')
receipt={'schema':'legacyforge-phase6a-test-receipt-v1','test_id':'X01','status':'BLOCKED','reason':'Approved isolated environment or console/package evidence unavailable','source_commit':PIN,'environment':{'type':None,'os_build':None,'console_model':None,'debugger_attached':None,'network_mode':None},'artifacts':{'appx_sha256':None,'launcher_sha256':None,'jvm_sha256':None,'glfw_sha256':None,'mesa_sha256':None,'manifest_sha256':None},'target':{'minecraft_version':None,'loader':None,'loader_version':None,'runtime_id':None,'java_major':None,'jni_requested':None,'jni_accepted':None},'observation':{'exit_or_hresult':None,'duration_ms':None,'memory_peak_bytes':None,'checked_files':None,'reused_files':None,'downloaded_files':None,'hash_failures':None,'graphics_version':None,'presented_frames':None,'symptom':None},'constraints':['No credentials, tokens, device codes, account identifiers or raw authenticated URLs','PASS requires actual evidence; use FAILED/BLOCKED/INCONCLUSIVE appropriately']}
(DOC/'tests/result.template.json').write_text(json.dumps(receipt,indent=2))
rows=list(csv.DictReader((SRC/'config/versions.tsv').open(),delimiter='\t'))
with (DOC/'evidence/target-validation-matrix.csv').open('w',newline='',encoding='utf-8') as f:
 fields=list(rows[0])+['targetId','newRuntimeTestStatus','blocker'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for row in rows:w.writerow({**row,'targetId':row['minecraftVersion']+'-'+row['loader']+'-'+row['loaderVersion'],'newRuntimeTestStatus':'BLOCKED','blocker':'No deployed runtime/package evidence or approved console access; preserve source support declaration'})
installer_summary={k:I[k] for k in ['installer_sha256','location_records','solid_chunk_offset','compression','dictionary_bytes','decoded_bytes','decoded_sha256','raw_hash_valid_count','instruction_filtered_valid_count','decoded_valid_count','installed_content_matches','limitations']}
installer_summary['jar_identities']=[{k:x[k] for k in ['record','file_offset','bytes','sha1','sha256','entries']}|{'versions':{k:v.get('version') for k,v in x['metadata'].items()}} for x in I['jar_metadata']]
installer_summary['payload_records']=I['records'];installer_summary['metadata_block']=[{k:v for k,v in x.items() if k!='strings'} for x in H['blocks']];installer_summary['location_block']=H['location_block'];installer_summary['destination_declarations']=I['destination_strings']
(DOC/'evidence/installer-payload-summary.json').write_text(json.dumps(installer_summary,indent=2))
native={'coverage':{'images':len(N['images']),'roles':dict(collections.Counter(x['role'] for x in N['images'])),'architectures':dict(counts),'delay_import_module_occurrences':sum(len(x['delay_imports']) for x in N['images']),'named_export_occurrences':sum(len(x['named_exports']) for x in N['images'])},'images':[],'edges':N['edges'],'limitations':N['limitations'],'errors':N['errors']}
for x in N['images']:
 native['images'].append({k:x[k] for k in ['role','path','bytes','sha256','architecture']}|{'import_modules':[v['module'] for v in x['imports']],'delay_import_modules':[v['module'] for v in x['delay_imports']],'named_export_count':len(x['named_exports']),'selected_runtime_exports':[v for v in x['named_exports'] if v['name'] in ['JNI_CreateJavaVM','JNI_GetDefaultJavaVMInitArgs','JNI_GetCreatedJavaVMs','JNI_OnLoad','glfwInit','glfwCreateWindow','glfwSwapBuffers','wglGetProcAddress']]})
(DOC/'evidence/native-dependency-graph.json').write_text(json.dumps(native,indent=2))
(DOC/'evidence/decoder-crosschecks.json').write_text(json.dumps(C,indent=2))
selected=[]
for dataset in [F,X]:
 for c in dataset['classes'].values():
  if re.search(r'(SignedStream|ChecksumStream|UpdateMeta|DownloadTask|Updater|ProfileManager|MinecraftUserJsonizer|MinecraftOAuthRefresh|MinecraftLauncher|CompleteVersion|OfficialVersionList|ExtraVersionList|RepositoryProxy|SimpleConfiguration)$',c['class']):
   selected.append({'artifact':c.get('artifact','installed-bootstrap-or-launcher'),'class':c['class'],'class_sha256':c['sha256'],'methods':[{'name':m['name'],'descriptor':m['descriptor'],'bytecode_length':m['bytecode_length']} for m in c['methods']]})
flow_summary={'continuation_scan':{'classes':F['class_count'],'methods':F['method_count']},'archive_and_installed_scan':{'classes':X['class_count'],'methods':X['method_count']},'artifact_identities':X['artifacts'],'selected_class_locations':selected,'limitations':['Counts describe indexed structure, not manual inspection of every method or executed coverage','Instruction observations and raw class data remain local; methods/offset conclusions are documented in reports']}
(DOC/'evidence/extended-static-index.json').write_text(json.dumps(flow_summary,indent=2))

# Replace stale first-pass statements rather than leave contradictory unknowns.
replace('README.md',"The installer-to-installed update history is **Unknown**. [E01–E04]","The original installer payload is now statically recovered: launcher `1.159.2+legacy`, bootstrap `1.32.2+legacy`, with all770 payload records hash-validated. Intermediate update history remains **Unknown**. [E01–E04/E11]")
replace('README.md','The read-only research package is delivered. Exhaustive analysis, exact historical update reconstruction, every loader behavior, and Xbox gameplay validation remain open in UNKNOWN-SUBSYSTEMS.','The static research package is expanded across all phases. See [full phase status](PHASE-STATUS.md), [installer contents](INSTALLER-CONTENTS.md), [update/recovery](UPDATE-AND-RECOVERY.md), [loader resolution](LOADER-RESOLUTION.md), [native audit](NATIVE-DEPENDENCIES.md), [Windows procedures](WINDOWS-SANDBOX-TESTS.md) and [Xbox procedures](XBOX-SERIES-X-TESTS.md). Historical events/current service permissions remain unknown; infrastructure-dependent execution is explicitly BLOCKED.')
replace('PROVENANCE.md','| Link between installer and installed JARs | Update mechanism surfaces exist, but no authenticated update history/package-content comparison | Unknown E01/E02/E03 |','| Installer payload comparison | Original launcher1.159.2/bootstrap1.32.2 recovered; both differ from installed copies;431 installed non-game content matches | Confirmed E11; intermediate history Unknown |')
replace('PROVENANCE.md','**Inferred:** Inno Setup packaging; exact packaging version and full embedded payload remain **Unknown**, because no installer was run or bulk-unpacked.','**Confirmed continuation [E11]:** Inno Unicode6.1.0 storage-format blocks and the complete770-record solid payload were decoded without running the installer; every declared content hash validated. Exact compiler release and historical install/update actions remain Unknown. See INSTALLER-CONTENTS.')
replace('FILE-INVENTORY.md','**Unknown:** which files came inside the original installer versus later downloads. [E01/E03]','**Confirmed continuation [E11]:** original installer payload inventory and hashes now identify its launcher/bootstrap and bundled runtime/dependency content.431 installed non-game files match installer payload records; game-cache files are absent from inspected destination declarations. Exact later acquisition/update chronology remains Unknown. See INSTALLER-CONTENTS.')
replace('JVM-RUNTIME.md','This parser covered standard PE imports, not delay imports, dynamic function names, all JNI exports, call reachability or Xbox API certification.','The first parser covered standard imports. Continuation E14 expands this to291 PE observations with standard/delay imports, named exports, archive-native inspection and a candidate dependency graph; runtime dynamic resolution, reachability and Xbox API certification remain unverified.')
replace('JVM-RUNTIME.md','The release fields observed for Java 21 did not identify a vendor, so none is assigned here.','The Java21 release fields do not identify a vendor; PE VersionInfo separately reports CompanyName Microsoft and ProductName OpenJDK Platform21.0.7. That is an embedded metadata claim, not independent publisher provenance.')
append('PROVENANCE.md','''## Continuation: publisher references and license boundary [E16]

The [publisher source page](https://docs.llaun.ch/en/launcher/source) describes reference/research use and links LegacyLauncher/archive, whose [license](https://raw.githubusercontent.com/LegacyLauncher/archive/master/LICENSE.txt) says All rights reserved. The public [website](https://llaun.ch/en) states downloads were halted after a Mojang complaint and disclaims Mojang/Microsoft affiliation. These documentary observations corroborate naming/restrictions, not historical installer authenticity. No proprietary source was incorporated into LegacyForge; only independently written summaries and analyst metadata are published here.
''')
append('ARCHITECTURE.md','''## Continuation findings

The original installer1.159.2 and bootstrap1.32.2 are now directly inspected [E11/E13]. Native wrapper resource strings name launcher/bootstrap.jar and its restart/JRE configuration, resolving the prior declared-linkage gap; actual execution remains BLOCKED. UPDATE-AND-RECOVERY adds exact signed-path/checksum/persistence branches; LOADER-RESOLUTION adds original-build inheritance/Forge-family behavior; NATIVE-DEPENDENCIES records291 native observations and existing shim limitations. Read the maps as structural/static relationships, not captured process/network traces.
''')
append('INSTALLATION-PIPELINE.md','''## Continuation: original installer and loader evidence

E11/E13 now confirm the archived launcher itself has the official catalog endpoint, extra version-profile path, inheritance exceptions, Java install orchestration and external ProcessBuilder launch. LOADER-RESOLUTION describes exactly which Forge-family mod-list and profile behaviors were recovered. Earlier references to unknown loader semantics remain true for unobserved remote/prepared processor content and execution, but no longer mean the relevant static paths were left unexamined. UPDATE-AND-RECOVERY documents range/redirect/error/persistence branches. Windows runtime/fault tests are BLOCKED, with full procedures prepared.
''')
append('AUTH-BOUNDARIES.md','''## Continuation: persistence, refresh and service support

E12 traces raw token-string getters into JSON payload fields, Gson serialization and normal Java file output. Application-level JSON serialization is Confirmed for the traced path; actual saved contents, OS protection/ACLs and account values were not inspected. Refresh repeats the ownership/profile chain after token refresh. E13 confirms the original archived launcher also contains the Microsoft/XBL/XSTS/Minecraft/ownership/profile flow. Neither provider architecture grants permission to bypass ownership.

Official [authorization-code](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow) and [device-flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code) documents establish generic Microsoft identity contracts; [XSTS guidance](https://learn.microsoft.com/en-us/gaming/gdk/docs/services/fundamentals/s2s-auth-calls/service-authentication/security-tokens/live-security-tokens?view=gdk-2604) describes relying-party-specific Xbox tokens. They do not authorize every Minecraft relying party/client. No authoritative public Minecraft launcher API contract was established for the observed service endpoints; registration/scopes/current service permission and live ownership remain Unknown/BLOCKED. No account or token test was run.
''')
append('XBOX-UWP-COMPATIBILITY.md','''## Continuation: measured static scope and actual blockers

NATIVE-DEPENDENCIES expands the native audit to291 PE observations including archive DLLs and delay imports. Specific GLFW source limitations include false extension queries, NULL Win32 window handles, absent hats and ignored mapping updates; investigate consumers instead of extrapolating universal failure. GameInput/controller and suspension/resume source hooks are already present. Exact package capability declarations are recorded without assuming they are granted on Xbox. [E14/E15]

Microsoft's [Xbox UWP limitations](https://learn.microsoft.com/en-us/uwp/extension-sdks/uwp-limitations-on-xbox) additionally limit folder picker scenarios, drag/drop, broad filesystem access, key credentials and roaming settings; this does not imply all PasswordVault APIs fail. Runtime verification requires the actual package/device. Owner-confirmed missing VM/remote-console infrastructure makes every new behavioral test BLOCKED. The complete56-row matrix and XBOX-SERIES-X-TESTS preserve the full scope.
''')
append('LEGACYFORGE-GAP-ANALYSIS.md','''## Continuation findings [E14/E15]

The native graph includes all six checked-in Mesa DLLs; no built APPX/LegacyForge/JVM/GLFW package outputs were present. The x64 Universal manifest declares capabilities including broadFileSystemAccess/runFullTrust/expandedResources, but no explicit codeGeneration was found. Declaration presence/absence is not runtime grant/prohibition evidence. Controller GameInput and lifecycle marker hooks exist. GLFW extension queries always return false; Win32 HWND retrieval returns NULL; hats/custom mapping behavior is limited. Exact source anchors and loader/graphics implications are in NATIVE-DEPENDENCIES.

All56 catalog targets are retained in evidence/target-validation-matrix.csv with source labels and new runtime status BLOCKED. The pinned PHASE-5F2.md still describes validation pending; the owner's later test report is separately attributed and does not validate every runtime tuple. Review existing scripts/validate-modern-version-matrix.ps1 as a staged-file validator, not hardware proof. No production change occurred.
''')
append('PHASE-6-ROADMAP.md','''## Continuation and full-scope execution handoff

Installer decoding and original-build comparison are now completed statically. Update/download/profile/inheritance traces and native graphs are expanded. Preserve all56 targets and use the prepared Windows/Xbox procedures and receipt template; no infrastructure-dependent test is passed. Include extension-query/Win32-handle/gamepad-mapping consumers in graphics/input validation. Do not install or execute archived code until a disposable environment is approved; the owner explicitly retained static-only authorization. No scope reduction or production/authentication/entitlement change is proposed by this research handoff.
''')
append('DOWNLOADS-TO-LEGACYFORGE.md','''## Continuation: direct archived-build confirmation

The exact installer now yields launcher1.159.2 and bootstrap1.32.2, separately hash-bound from the installed updates. The archived launcher directly uses Mojang catalog→extra/official profile→inheritance→library/runtime/download→external Java process paths. Its Forge-family mod-list preparation and extra-version profiles are documented in LOADER-RESOLUTION. LegacyForge's full56-row catalog remains intact; use its existing approved manifest/downloader/embedded-host path and verify each exact runtime tuple. Static extraction does not turn later Windows downloads into Xbox-compatible binaries.
''')

# Replace the old unresolved ledger with current answered vs externally blocked status.
(DOC/'UNKNOWN-SUBSYSTEMS.md').write_text('''# Remaining unknowns and blocked tests

Research continuation: 2026-10-17. Scope retains every mission phase and all56 approved target rows.

| Area | Updated evidence / remaining condition | Status |
|---|---|---|
| Installer contents |770 decoded/checksummed records; original launcher1.159.2/bootstrap1.32.2;431 installed content matches | Confirmed static recovery E11 |
| Historical authenticity/acquisition/update chain | Unsigned artifact; mutable timestamps; no independently authenticated publisher release hash or event history | Unknown historical facts; not recoverable from an unrecorded event |
| Wrapper/bootstrap declared linkage | Embedded launcher/bootstrap.jar and JRE/restart config offsets; native CreateProcess call | Confirmed static configuration E06/E11; execution BLOCKED |
| Update verification/replacement | Signed-path framing/key/algorithms, checksum/temp/copy/restart and local/remote comparison traced in original/installed code | Confirmed static branches E12/E13; failure/durability/replay/rotation outcomes Unknown/BLOCKED |
| Configuration/accounts | Properties/Gson temporary sibling writes/moves, migration/backup and token-string serializer/refresh paths traced | Confirmed static E12; actual account values not read; OS protection/crash behavior Unknown |
| Forge/Fabric resolution | Official/extra profiles, duplicate/parent inheritance handling, Forge-family mod-list/classpath/argument paths traced | Confirmed static E13; exact remote-generated loader/processor execution BLOCKED |
| Downloader recovery | Partial/range/redirect/error/abort and integrity branches traced | Confirmed static E12; packet-loss/disk-full/interruption/concurrency outcomes BLOCKED |
| Minecraft service support/registration | Generic official Microsoft/XSTS contracts found; no public authoritative Minecraft launcher API contract established | Unknown current permission/scopes; live tests BLOCKED, no credentials |
| Java17/8/JNI21 |Source selection discrepancy and JNI contract confirmed; packaged runtimes absent | Execution BLOCKED until exact artifacts and approved isolated/device environment |
| Native loading/graphics/input/audio |291 native occurrences/import/export graph; shim/GameInput/Mesa/lifecycle source audited | Static inventory complete within declared format bounds; dynamic resolution, ABI/device behavior BLOCKED |
| Xbox resources/lifecycle | Actual package/resource/driver/console evidence not available | Owner-run X01–X13 BLOCKED; procedures prepared |
| Every catalog target |56 rows retained, all new runtime verdicts explicitly BLOCKED | No row omitted or silently called PASSED |

See PHASE-STATUS, WINDOWS-SANDBOX-TESTS and XBOX-SERIES-X-TESTS for full criteria. User explicitly confirmed no configured VM, no Device Portal/remote console access, and static-only authorization. No installations, unknown binary execution, device connections, account tests or production changes occurred. Remaining infrastructure work requires later explicit owner approval and evidence; it is not a reason to stop useful static analysis or invent successful tests.
''',encoding='utf-8')

append('EVIDENCE-INDEX.md',f'''## Continuation evidence and corrected first-pass limitations

| ID | Reproducible evidence | Result / boundary |
|---|---|---|
| E11 | installer_static.py; installer_payload.py; installer-payload-summary.json | Header/location CRCs and all770 payload SHA1 values validate after required instruction decoding; original launcher/bootstrap identities recovered;431 installed content matches |
| E12 | continuation/analyze.py + query.py; focused method/branch offsets in UPDATE-AND-RECOVERY |400 indexed classes /2,170 methods, with exact signature/update/config/token/refresh/downloader branches; indexed counts are not execution coverage |
| E13 | extended_static.py + query_extended.py; extended-static-index.json |2,296 archived/installed structural classes /14,160 member methods indexed; selected original loader/inheritance/process/auth methods traced |
| E14 | native_audit.py; native-dependency-graph.json |291 image occurrences,1,714 standard/delay edges,46 delay module occurrences,56,489 named-export entries; zero parser errors; loader resolution not emulated |
| E15 | pinned Package.appxmanifest, GLFW/App/lifecycle code, versions.tsv | Exact capability declarations and interface limits;56 catalog rows; no built package/JVM/shim artifacts observed |
| E16 | Official publisher/Microsoft/Oracle links and user-confirmed environment status | Research-only source restriction, identity/JNI/platform contracts; no approved VM or remote Xbox infrastructure; all behavioral tests BLOCKED |

Static analyzer cross-checks: eight selected trusted javap classes and four GNU objdump import-module sets passed. Details in evidence/decoder-crosschecks.json; objdump version2.47.20260726. They are analyzer checks only. A later 7-Zip19 listing failed with headers/unconfirmed-start/tail warnings and showed a ZIP fragment; it did not inventory the installer. The independent Inno inspector replaced that failed route. The first payload view showed148 mismatches before reversing executable-storage filtering; all770 verified afterward. No corruption/vulnerability claim relied on the intermediate mismatch. A missing __file__ in the extended parser harness and a wrapper-string command syntax error were corrected; final evidence comes from successful runs.

Reproduce locally from the research root, in this dependency order:

```powershell
python analysis-local/installer_static.py
python analysis-local/installer_payload.py
python analysis-local/extended_static.py
python analysis-local/native_audit.py
python analysis-local/verify_static_decoders.py
```

The installer inspector uses Python lzma/zlib/hashlib and verifies bounds/checksums. It is specific to the current artifact and6.1.0 data format. Selected archived JARs/nested installed bootstrap are materialized in analysis-local/installer-extracted-local for static ZIP/javap inspection only. Never publish that directory, installer-header-local.bin, installer-locations-local.bin, local flow indexes or decoder outputs containing reconstructed instructions. No target Java/native code was loaded/executed.

Scripts/tool hashes and every publication file are bound in evidence/SHA256SUMS.txt and evidence/analyst-tool-hashes.json. Source checkout remains at `{PIN}` and clean. Old statements that installer payload, original-build pipeline, delay imports or signature implementation had not yet been inspected are superseded by E11–E16 and the updated documents. History, live service permission and unavailable hardware remain honestly Unknown/BLOCKED.
''')
toolnames=['installer_static.py','installer_payload.py','extended_static.py','query_extended.py','native_audit.py','verify_static_decoders.py','wrapper_strings.py','jar-static/continuation/analyze.py','jar-static/continuation/query.py']
(DOC/'evidence/analyst-tool-hashes.json').write_text(json.dumps([{'path':'analysis-local/'+n,'sha256':sha(LOCAL/n)} for n in toolnames],indent=2))
with (DOC/'evidence/SHA256SUMS.txt').open('w',encoding='utf-8') as f:
 for p in sorted(DOC.rglob('*')):
  if p.is_file() and p.name!='SHA256SUMS.txt':f.write(sha(p)+'  '+p.relative_to(DOC).as_posix()+'\n')
print(json.dumps({'markdown':len(list(DOC.glob('*.md'))),'files':len([p for p in DOC.rglob('*') if p.is_file()]),'target_rows':len(rows),'payload_valid':I['decoded_valid_count'],'native_occurrences':len(N['images'])},indent=2))
