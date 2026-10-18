# Evidence index and reproducibility

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

## Findings ledger

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
| search_strings(regex bootstrap\|tl.args\|javaw\|CreateProcess\|Launch4j) | ev_c957ce041c8dac3c6abc5ea7cdcbc00fba0ff66a97dfb93abdfc8a43b7943a39; Launch4j0x40908a, javaw0x4094b3, CreateProcessA0x4144ae |
| find_xrefs_to_name(CreateProcessA) | ev_2d6e8b015ea8a740629560944e8aa79068bd2a6756e3de1c96fe5ab5235c2fbb; unresolved bare name; use qualified symbol |
| search_strings(regex bootstrap.jar\|tl.args\|tl.properties\|jre) | ev_0828a5402616aa822a373d0692de9498ae1959cb017c45014799f959cf8b2434; defined JRE discovery strings |
| search_procedures(CreateProcess) | ev_1cd6be6e6a69c7e419093cb34d3bd64aa76a5733b3f23998ca3ebc3758b99db6; KERNEL32.DLL:: CreateProcessA |
| procedure_references(KERNEL32.DLL:: CreateProcessA,incoming) | ev_4fca140dc3ee7fd2c54bd33833b23bb74b60a1eb917c9e0a9c1f5a87231248b1; call0x40524e in FUN_00405126 |
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
- `net.legacylauncher.user.minecraft.MinecraftOAuthAuthenticate.authenticate`; strategy.gos. GameOwnershipValidator.checkGameOwnership.
- `net.legacylauncher.ui.LegacyLauncherFrame` superclass JFrame; launcher metadata and nested bootstrap class structures.

Focused method evidence binds these identifiers to launcher.jar SHA256 `364b9add...`; nested bootstrap structural observations bind outer bootstrap SHA256 `09ba7517...`. Static invoke presence does not prove a branch executes.

## Local reproducibility

Tools: PowerShell7.6.5; Python3.14.7; git2.55.0.windows.5; trusted javap21.0.12.1 from the existing Ghidra JDK; REA6.4.0; Ghidra 12.1.4. Analyst scripts use Python standard library only. No target JRE executable was invoked.

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
- An initial library verifier expected downloads.artifact.path; local normalized JSON omitted it. Deriving paths from artifact URLs produced 107 entries,75 present/valid. No conclusion uses the erroneous initial zero count.
- Web renderer could not read the archive metadata/GitHub API JSON; direct unauthenticated HTTPS metadata reads succeeded.
- Java class parser initially misadvanced interface metadata; corrected and rerun. Two guessed class names were absent; real names were selected from ZIP inventory. No finding depends on those failed guesses.
- Bare CreateProcessA name lookup failed; qualified imported symbol then resolved. Ghidra decompilation had a stack-tracking warning, so exact process parameters were not inferred from unreliable stack rendering.
- First-pass boundary: no target execution, installer extraction, live authentication, official component download, console test, or comprehensive third-party license review. Continuation E11 later performs nonexecuting installer recovery. Existing file hashes verify local content against local metadata, not trustworthiness.

## Publication files

`evidence/static-summary.json` contains curated artifact identities, directory counts, per-library hash results, standard native imports and pinned source hashes. `evidence/relevant-files.csv` contains relevant installed EXE/DLL/JAR paths, sizes and SHA256 only. `evidence/signatures.json` contains returned Windows signature/version metadata without personal paths. `evidence/SHA256SUMS.txt` binds the complete deliverable set.

Local-only `analysis-local` includes proprietary class structure/constants summaries and REA reconstructed text; it is outside the publication folder. No binary, asset, credential, raw profile or raw log is copied into the deliverables. None of the investigation output has been committed or pushed.

## Continuation evidence and corrected first-pass limitations

| ID | Reproducible evidence | Result / boundary |
|---|---|---|
| E11 | installer_static.py; installer_payload.py; installer-payload-summary.json | Header/location CRCs and all 770 payload SHA1 values validate after required instruction decoding; original launcher/bootstrap identities recovered; 431 installed content matches |
| E12 | continuation/analyze.py + query.py; focused method/branch offsets in UPDATE-AND-RECOVERY |400 indexed classes /2,170 methods, with exact signature/update/config/token/refresh/downloader branches; indexed counts are not execution coverage |
| E13 | extended_static.py + query_extended.py; extended-static-index.json |2,296 archived/installed structural classes /14,160 member methods indexed; selected original loader/inheritance/process/auth methods traced |
| E14 | native_audit.py; native-dependency-graph.json |291 image occurrences,1,714 standard/delay edges,46 delay module occurrences,56,489 named-export entries; zero parser errors; loader resolution not emulated |
| E15 | pinned Package.appxmanifest, GLFW/App/lifecycle code, versions.tsv | Exact capability declarations and interface limits; 56 catalog rows; no built package/JVM/shim artifacts observed |
| E16 | Official publisher/Microsoft/Oracle links and user-confirmed environment status | Research-only source restriction, identity/JNI/platform contracts; no approved VM or remote Xbox infrastructure; all behavioral tests BLOCKED |

Static analyzer cross-checks: eight selected trusted javap classes and four GNU objdump import-module sets passed. Details in evidence/decoder-crosschecks.json; objdump version 2.47.20260726. They are analyzer checks only. A later 7-Zip19 listing failed with headers/unconfirmed-start/tail warnings and showed a ZIP fragment; it did not inventory the installer. The independent Inno inspector replaced that failed route. The first payload view showed148 mismatches before reversing executable-storage filtering; all 770 verified afterward. No corruption/vulnerability claim relied on the intermediate mismatch. A missing __file__ in the extended parser harness and a wrapper-string command syntax error were corrected; final evidence comes from successful runs.

Reproduce locally from the research root, in this dependency order:

```powershell
python analysis-local/installer_static.py
python analysis-local/installer_payload.py
python analysis-local/extended_static.py
python analysis-local/native_audit.py
python analysis-local/verify_static_decoders.py
```

The installer inspector uses Python lzma/zlib/hashlib and verifies bounds/checksums. It is specific to the current artifact and 6.1.0 data format. Selected archived JARs/nested installed bootstrap are materialized in analysis-local/installer-extracted-local for static ZIP/javap inspection only. Never publish that directory, installer-header-local.bin, installer-locations-local.bin, local flow indexes or decoder outputs containing reconstructed instructions. No target Java/native code was loaded/executed.

Scripts/tool hashes and every publication file are bound in evidence/SHA256SUMS.txt and evidence/analyst-tool-hashes.json. Source checkout remains at `d1453434ceefe73bef5aff497194e09f39dde7e1` and clean. Old statements that installer payload, original-build pipeline, delay imports or signature implementation had not yet been inspected are superseded by E11–E16 and the updated documents. History, live service permission and unavailable hardware remain honestly Unknown/BLOCKED.

## E17 — Public metadata verification

`python analysis-local/official_metadata_check.py` requests public JSON only: Mojang version_manifest_v2, its selected 1.21.11 JSON and Fabric 1.21.11/0.19.5 profile JSON. No credentials, artifact binaries or asset objects are requested. Version metadata's declared SHA1 validates; all 107 library artifact hash/URL pairs agree with local normalized metadata; the local asset index agrees with the independently retrieved official hash. Fabric confirms the eight-library inherited KnotClient profile. Data/hash/result summaries are in evidence/official-metadata-check.json. The current catalog is time-varying; selected content-addressed version/profile response hashes bind this observation. These are external metadata checks, not target execution tests or publisher-authenticity proof for the archived installer.

## E18 — Retained historical messages

[Historical corroboration](HISTORICAL-CORROBORATION.md) and [compact evidence](evidence/historical-corroboration.json) bind six input logs, 26,994 lines, exact SHA256 identities and bounded line citations. They corroborate recorded catalog/version/runtime/assets/library/client preparation, download completion, Java 21.0.7, LWJGL 3.3.3+5, OpenAL initialization and desktop exit code 0. The records already identify launcher 1.169.4/bootstrap 1.40.3, so the archived-to-installed update transition remains Unknown. Message presence is the confirmed fact; no new execution test passes. Raw logs and the full repetitive URL list remain local.

## Acceptance-plan and receipt-checker audit

[Machine-readable cases](tests/test-cases.json) and [target matrix](evidence/target-validation-matrix.csv) preserve all 25 gates and all 56 approved tuples. [Original receipt checker](tools/verify-test-receipts.py) validates format, exact X12 tuple/prerequisite consistency, isolation/hardware declarations and confined attachment hashes. Independent synthetic controls reproduced six issues in the earlier checker and satisfied 31 of 31 controls after correction. These are analyst-tool checks, never target behavior. The control source/results and before/after snapshots remain in `analysis-local/final-audit/completion`; their original-script hashes are listed in `evidence/analyst-tool-hashes.json`.

Receipt acceptance does not certify observation truth, redact free text/attachments or automatically establish aggregate 56-target/four-runtime coverage. No synthetic control receipt is included as an actual result. Generated analyst bytecode/cache was moved out of the publication folder; commands use `python -B` to suppress regeneration. [Research integrity](evidence/research-integrity.json) records the final source pin, full plan coverage, blocked counts and publication checks.

## E19 — Execution prerequisites and original source fixture

[Execution readiness](EXECUTION-READINESS.md) and [curated observations](evidence/execution-readiness.json) distinguish installed host analysis/build tooling from absent execution surfaces. Existing Ghidra JDK21 is confirmed separately from standard-root JDK discovery. No approved disposable guest, exact APPX/runtime/shim/dependency set, diagnostic package, console access or fresh owner hardware/account receipt was established. Public exact-pin workflow and repository-release queries returned no package in their bounded scope.

The independently written [RuntimeProbe.java](tests/probes/RuntimeProbe.java) compiled with trusted JDK21 `javac --release 8`, producing two class files of major version 52. Source SHA256 is `56a6250ddf494136c6214fab269966ec2c099b60642002a28becd543ec58ddfd`. Class files remain local and the probe was never run. [Probe contract](tests/probes/README.md) covers fresh app-local synthetic data, bounded thread, read/write/hash/rename and ZIPFS readback; it explicitly excludes JNI/native/graphics/input/audio/account certification. Compilation is an analyst-source check, not a physical test.

## E20 — Signed metadata positive fixture

[Signed-update fixture](SIGNED-UPDATE-FIXTURE.md) and [evidence](evidence/signed-update-fixture.json) record one bounded unauthenticated public metadata response derived from static host/channel/template evidence. Its signature independently verifies against the identical archived/installed embedded RSA key; local signature/payload bit changes fail the independent verifier. Response SHA256 is `9081bab55e8c8ba72ff3c63a1c2cbb85ba523bd2ef357b94e272ba913cf5c52c`. Raw response, decoded metadata and key bytes remain local; referenced binaries were not fetched.

This closes W09 fixture availability only. It does not execute the actual verifier/updater, prove application/rollback behavior, independently establish installer publisher identity, or reconstruct historical events. Exact framing, key/artifact identities, source locators, algorithm, response bounds and controls are in E20.

## E21 — All 56 upstream metadata plans

[Catalog metadata plans](CATALOG-METADATA-PLANS.md) and [machine-readable summaries](evidence/catalog-metadata-plans.json) retain every approved tuple. All 22 unique Minecraft version JSONs matched their official catalog SHA1; all 20 exact Fabric profiles resolved; all 34 resolved Forge/NeoForge coordinates were listed in their public Maven indexes. The remaining Forge `selected` label is explicitly unresolved, and vanilla has no loader-release lookup.

The response URL/time/hash ledger binds this time-varying observation. Mojang 26.x metadata declares Java25. Fabric library/profile differences are retained rather than normalized into an assumed universal layout. Maven presence does not resolve processor outputs, prove binary integrity or certify a package. No component binary, installer, game, authenticated account or console was accessed. All 56 new runtime verdicts remain BLOCKED.
