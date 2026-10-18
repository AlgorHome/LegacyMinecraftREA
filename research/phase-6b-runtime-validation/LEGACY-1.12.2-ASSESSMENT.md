# Legacy 1.12.2 assessment — Phase 6B planning only

Date: 2026-10-17 (America/Chicago). Approved source: `AlgorHome/LegacyForge`, exact commit `d1453434ceefe73bef5aff497194e09f39dde7e1`. The checkout was read without running its scripts or binaries. No provider, test, package, authentication, entitlement, or Phase 6A dossier changes are made by this document. **Confirmed** means static source observation; **Inferred** means interpretation; **Unknown** means evidence is insufficient. Proposed fixtures and statuses below do not exist as implemented behavior unless stated explicitly.

## Finding and boundaries

**Confirmed, high confidence:** both 1.12.2 catalog rows explicitly say `Legacy provider not implemented yet`. Forge uses the unresolved literal loader version `selected`; vanilla uses `none`; both select runtime family `legacy`, support label `experimental`, controller provider `none`. See [config/versions.tsv:56–57](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/config/versions.tsv#L56). These are source declarations, not a chosen Forge release, an installation manifest, a runtime receipt, or gameplay support.

The missing legacy provider, unresolved Forge version, Java 8 packaging, invocation contract, legacy metadata interpretation, and graphics/native API compatibility are **separate blockers**. Solving one cannot establish the others.

| Question | Evidence and conclusion | Confidence |
|---|---|---|
| Does a general Forge provider exist? | **Confirmed:** `LoaderFinalizeVersionInfo` dispatches Forge to `ForgeFinalizeVersionInfo`; classpath/options/artifact hooks likewise exist. Do not call all Forge support missing. | High |
| Is a vanilla provider selected? | **Confirmed:** `LoaderId` includes Unknown/Fabric/NeoForge/Forge; `ParseLoaderId` maps other strings to Unknown. The finalization switch defaults to `supported=false`. Thus the catalog's vanilla row has no vanilla finalizer in this dispatch. | High |
| Does generic Forge dispatch guarantee 1.12.2 support? | **Confirmed:** `ForgeManifestReady` checks nonempty manifest, assetIndex, launchVersion and mainClass, with no explicit Minecraft-version range test. **Inferred:** this predicate is metadata presence, not a certificate of legacy semantics. | High / Medium |
| Is `selected` an approved Forge build? | **Confirmed:** no. `build.ps1` excludes `selected` and `none` loaderVersion rows from `$manifestTargets`. The exact 1.12.2 Forge build remains **Unknown/unselected**. | High |
| Is older Forge artifact preparation already implemented? | **Confirmed:** existing Forge preparation has MCP/SRG and no-MCP branches, including installer `data/client.lzma`, installertools/FART and client artifact paths. **Unknown:** whether any exact 1.12.2 installer format and processors match those branches. Existing branches cannot be relabeled 1.12.2 support. | High |
| Are legacy Java runtime names present? | **Confirmed:** `ResolveJavaRuntimeInfo` maps legacy/java8/jdk8/8 to `jre8`, filesystem-8 and zipfs-8 patch names. A search of tracked text found those three names only in that selector; the inspected build packaging block packages current, exact21 and optional17, not8. **Unknown:** an externally prepared package could differ; no such package is supplied by this checkout. | High within checkout |
| Is Java 8 invocation proven? | **Confirmed:** the shared launch path requests `JNI_VERSION_21`, adds modular/native-access arguments and module patch options; legacy selection alone does not adapt that contract. **Unknown:** exact Java8 acceptance and package execution; no VM was run. | High / Unknown runtime |
| Are LaunchWrapper, old Forge/FML main/tweaker, LWJGL2 and its native requirements established? | **Unknown for an approved 1.12.2 artifact set:** no selected Forge release/metadata or runtime artifacts were inspected here. Bounded repository text searches found no LaunchWrapper entrypoint or LWJGL2 Display/input implementation. This is not proof that every legacy mechanism is absent from every source dependency. | Bounded static negative |

## Reproducible source anchors

All links identify the approved commit, not current main.

- [loader_common.h:15–22](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/loaders/loader_common.h#L15) and [loader_common.cpp:18–22](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/loaders/loader_common.cpp#L18): loader enum/parser; [loader.cpp:9–27](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/loaders/loader.cpp#L9): provider finalization. Other dispatch hooks:30–92.
- [forge.cpp:561–577](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/loaders/forge.cpp#L561): `ForgeManifestReady` and `ForgeFinalizeVersionInfo`; [118–175](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/loaders/forge.cpp#L118) and [247–275](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/loaders/forge.cpp#L247): readiness and artifact branch selection. Hooks:580–687. There is no explicit 1.12.2 whitelist in the cited finalizer.
- [build.ps1:599–606](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/build.ps1#L599): unresolved loader labels excluded from manifest targets; [1204–1224](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/build.ps1#L1204): packaged runtime/patch families.
- [new-download-manifest.ps1:371–410](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/scripts/new-download-manifest.ps1#L371): Forge Maven version prefix construction and installer path; `Get-LoaderProfile` expects `version.json`, whereas vanilla returns null. [413–435](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/scripts/new-download-manifest.ps1#L413): installer `install_profile.json`; [547–562](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/scripts/new-download-manifest.ps1#L547): official Minecraft manifest/version/client records. These are existing tooling expectations, not verified old-installer layouts.
- [runtime_manager.cpp:1079–1116](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/runtime_manager.cpp#L1079): runtime selector; [1166–1212](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/runtime_manager.cpp#L1166): packaged target metadata and loader finalization.
- [minecraft_launch.cpp:1091–1159](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L1091): shared VM options/patch assumptions; [1352–1363](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L1352): fixed JNI21 invocation; [921–927](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L921): second-VM guard.
- [glfw_uwp.cpp:2997–3011](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L2997): existing GLFW3-style shim API. This is not evidence of LWJGL2 Display/input JNI compatibility.

The official [JNI Invocation API contract](https://docs.oracle.com/en/java/javase/17/docs/specs/jni/invocation.html#jni_getdefaultjavavminitargs) describes requested JNI-version support and negative errors for unsupported requests; it also states multiple VMs in one process are unsupported. A synthetic future diagnostic should record the requested version, runtime-reported version, exact result and runtime identity. No claim about an actual packaged Java8 failure follows from reading the specification.

## Proposed contract and fixtures

These are planning requirements for an independently implemented provider; no code or fixture is created now.

| Proposed fixture | Required acceptance behavior |
|---|---|
| Catalog row with `selected` or `none` as Forge version | `BlockedUnselectedLoaderVersion`; no invented Maven coordinate, network request, installer, patcher or game entrypoint. Vanilla's no-loader identity must be handled separately, not passed through Forge resolution. |
| Exact future approved Forge coordinate and schema identity | Bind Minecraft version, Forge version, installer metadata schema, hashes, main/tweaker, libraries and processing plan to one receipt. Unsupported or missing schema fields return `UnsupportedLegacyMetadata`; no guessed `version.json`/`install_profile.json` equivalence. |
| Legacy argument string, inherited metadata, conditional libraries and native classifiers | Deterministic synthetic fixtures resolve inheritance and argument tokenization/rules explicitly; reject unsupported features and unresolved placeholders. Hash/address selection must be reproducible. |
| Forged metadata with only four nonempty finalizer fields | A new semantic provider contract must still report `Unverified`/`Unsupported`; current `ForgeManifestReady` alone cannot mark runtime ready. |
| Missing Java8 package, wrong bitness/major, missing native or unknown hash | Explicit `BlockedRuntimeMissing`, `UnsupportedRuntimeArchitecture` or `BlockedNativeIdentity`; do not silently fall back to current Java or desktop GLFW. |
| JNI version/options unsupported by selected runtime | Preserve numeric result/stage/runtime identity and fail before Java entry. Separate JNI capability from supported VM options and Java module-patch format. No retries creating another JVM in the same process. |
| LWJGL2 candidate interface capability | If approved later, use original synthetic JNI/window/input/audio probes against an identified ABI; record required entrypoints and actual results. Passing GLFW3 probes does not satisfy this fixture. |
| Absent processor or native ABI contract | `UnsupportedLegacyProcessor`/`UnsupportedNativeABI`; resolving official release metadata or downloading a file must never count as processor parity or runtime validation. |

**Unknown:** exact old Forge processors, LaunchWrapper/tweaker chain, library/native versions, installation inheritance and resources mapping remain tied to a future specifically selected and approved artifact/metadata set. Official release metadata can establish identity/availability; it cannot establish execution behavior or processor equivalence. This document selects no Forge build.

## Representative no-game diagnostic order

1. First propose one Java21 package-independent synthetic host fixture: runtime identity/bitness, supported JNI version, original Java main, return/error handling, filesystem/threading and one identified native symbol. Isolate each VM test in a fresh diagnostic process/package activation; keep production second-VM safeguards.
2. Only after that baseline, conditionally propose Java17 and Java8 representatives if exact lawful runtime builds and a compatible host/package design are supplied and approved. Java8 needs its own options/patch ABI assessment, not only a lower JNI constant. A synthetic runtime pass remains separate from legacy provider support.
3. Treat current/Java25 as conditional: `current` is a source runtime label, not proof of major25. Propose a Java25 representative only if an approved package identity establishes that major and a requirement warrants it.
4. Do not attempt all 56 catalog rows. Representative family probes precede any later exact-target validation; no Minecraft game JAR, Microsoft login, entitlement exercise or account token is necessary for these proposed synthetic diagnostics.

## Status and future authorization

Current status: **Blocked for 1.12.2 runtime validation**, with confirmed catalog/provider boundaries and unresolved legacy dependencies. No new hardware evidence is produced. User-reported Phase5F.2 Xbox testing does not validate a Java8/1.12.2 combination.

A future authorization would need to identify the diagnostic implementation/package changes, exact runtime/native provenance, build/install/activation scope, target console/OS/package identity and permitted synthetic execution. Selecting a Forge build, acquiring metadata/artifacts, executing installer processors, or running a game are separate future scopes. Production/authentication/entitlement changes are not authorized by this plan. Record package hash, actual capabilities, runtime and loaded native identities, requested/returned JNI versions, VM options, probe results, resource limits, input/audio and lifecycle outcomes before claiming readiness. External blockers are the unavailable approved Java8 package/ABI proof, unselected Forge coordinate, unverified legacy provider contract and absent new Xbox diagnostic receipts.

## Source identity and hashes

SHA-256 values below describe the files actually read from the detached approved checkout. They are not packaged runtime hashes.

| Source path | SHA-256 |
|---|---|
| config/versions.tsv | `acbd5fca365058b94dc5d01aacd13b5a67373eb8b5611b17cd5f539a4dba2a55` |
| MC.Xbox/launch/loaders/loader_common.h | `4a8713a339905c1b5f9cdb59c3db6f9c9016330b6149f904800f52a3ebc0db8c` |
| MC.Xbox/launch/loaders/loader_common.cpp | `b637905b5b5fdbfec40b364115d578bc24eb946e4620502b42996d6f88ae2b55` |
| MC.Xbox/launch/loaders/loader.cpp | `f40258d52e054db388244c3849fd67055cd62744a29c0c249be848cf73b8ccb5` |
| MC.Xbox/launch/loaders/forge.cpp | `467e46d864fa9c4868bd5d8da5ab9ef23be6a681c136831dae273378769da001` |
| MC.Xbox/launch/runtime_manager.cpp | `fad066071b9c8914350d719fd08e2ea516daa59b6087b83ba45c96bb4787eeaf` |
| MC.Xbox/launch/minecraft_launch.cpp | `c37eade570d45fbdad0ba876be3347729b1000e579692c1819d059dbf80b5b12` |
| scripts/new-download-manifest.ps1 | `843bde309ed1b1a32a06e7f11430d93f8a63d485c79ca6677886fdce57954b32` |
| build.ps1 | `0e68582568ee6bd0f920e822c88ea8284d5f84d823b1d4597caa5e45ea7c6b8a` |
| glfw_shim/glfw_uwp.cpp | `0dde9a0c2e0e9b6f028fae5efe9d45a8a81a1e26e330bb72d42cacc3a4ad4d10` |
