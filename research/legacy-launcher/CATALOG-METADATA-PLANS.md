# All 56 catalog metadata plans [E21]

Public observation: 2026-10-17T06:57:10.757039Z to 2026-10-17T06:57:13.691931Z. Approved source: d1453434ceefe73bef5aff497194e09f39dde7e1.

This independently written analyst script requested public JSON/XML only. No JAR, DLL, installer, game, asset or runtime was downloaded; no account or console was contacted. All 56 new runtime verdicts remain **BLOCKED**.

## Method and source

The pinned scripts/new-download-manifest.ps1 names Mojang (line547), Fabric profile (380), Forge repository/coordinate join (371-388), and NeoForge repository (398). Maven indexes are standard group/artifact sidecars at those same source-defined bases. Source pin, catalog SHA256 and endpoint templates are checked before requests.

Reproduce with python -B analysis-local/final-audit/completion/check_catalog_metadata.py. It uses standard library, four workers, 12-second I/O timeouts, a 30-second response wall bound, a 6-MiB body cap, explicit HTTPS JSON/XML endpoint validation and no retries. Raw metadata bodies are not published.

All 56 rows and 22 unique Minecraft versions are retained; 20 exact Fabric profiles were requested. All URLs, statuses, response hashes, descriptor summaries and target plans are in [catalog-metadata-plans.json](evidence/catalog-metadata-plans.json).

## Observed summary

| Check | Result |
|---|---|
| Minecraft version metadata | {"FOUND_HASH_VERIFIED_METADATA": 22} |
| Exact Fabric profiles | {"FOUND_EXACT_PROFILE": 20} |
| Loader metadata/index presence | {"EXACT_RELEASE_LISTED": 34, "FOUND_EXACT_PROFILE": 20, "NOT_APPLICABLE_VANILLA": 1, "UNRESOLVED_SOURCE_LOADER_VERSION": 1} |
| Actual runtime/device execution | 0 executed; 56 BLOCKED |

## Every retained target

| Target | Source runtime | Minecraft metadata | Loader metadata |
|---|---|---|---|
| 26.2-fabric-0.19.5 | current | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 26.2-forge-65.1.3 | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.2-neoforge-26.2.0.82 | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.1.2-fabric-0.19.5 | current | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 26.1.2-forge-64.1.3 | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.1.2-neoforge-26.1.2.107 | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.1.1-fabric-0.19.5 | current | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 26.1.1-forge-63.0.2 | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.1.1-neoforge-26.1.1.15-beta | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.1-fabric-0.19.5 | current | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 26.1-forge-62.0.9 | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 26.1-neoforge-26.1.0.19-beta | current | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.11-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.11-forge-61.2.1 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.11-neoforge-21.11.45 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.10-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.10-forge-60.1.15 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.10-neoforge-21.10.64 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.9-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.9-forge-59.0.5 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.9-neoforge-21.9.16-beta | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.8-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.8-forge-58.1.22 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.8-neoforge-21.8.54 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.7-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.7-forge-57.0.3 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.7-neoforge-21.7.25-beta | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.6-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.6-forge-56.0.9 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.6-neoforge-21.6.20-beta | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.5-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.5-forge-55.1.13 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.5-neoforge-21.5.98 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.4-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.4-forge-54.1.18 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.4-neoforge-21.4.157 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.3-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.3-forge-53.1.12 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.3-neoforge-21.3.97 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.2-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.2-neoforge-21.2.1-beta | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.1-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21.1-forge-52.1.16 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21.1-neoforge-21.1.250 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.21-forge-51.0.33 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.21-neoforge-21.0.167 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.20.4-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.20.4-neoforge-20.4.237 | java17 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.20.1-fabric-0.19.5 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.20.1-forge-47.4.20 | java21 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.19.2-fabric-0.14.25 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.18.2-forge-40.2.27 | java17 | FOUND_HASH_VERIFIED_METADATA | EXACT_RELEASE_LISTED |
| 1.16.5-fabric-0.14.25 | java21 | FOUND_HASH_VERIFIED_METADATA | FOUND_EXACT_PROFILE |
| 1.12.2-forge-selected | legacy | FOUND_HASH_VERIFIED_METADATA | UNRESOLVED_SOURCE_LOADER_VERSION |
| 1.12.2-vanilla-none | legacy | FOUND_HASH_VERIFIED_METADATA | NOT_APPLICABLE_VANILLA |

## Primary response identity ledger

Exact public endpoints and observed response SHA256 are below. Successful Mojang version JSON also matched its catalog-declared SHA1. Catalogs/indexes/profile responses are mutable; these hashes bind the observation.

| Metadata endpoint | HTTP/status | Response SHA256 |
|---|---|---|
| [Mojang catalog](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json) | 200 / FETCHED | ac37f92737df1a9d7660047136fedd3edebd90bd6e552f53ddc3f222079bc8fa |
| [1.12.2](https://piston-meta.mojang.com/v1/packages/832d95b9f40699d4961394dcf6cf549e65f15dc5/1.12.2.json) | 200 / FETCHED | 56dac2e1caa872d7e37a7b5523056cd812dca94f912ad2bd652817bee60edca4 |
| [1.16.5](https://piston-meta.mojang.com/v1/packages/fba9f7833e858a1257d810d21a3a9e3c967f9077/1.16.5.json) | 200 / FETCHED | 3eeeab7b3165cc5263dc26ff8fe114fdb718b75a0244efead9d19635d090ba72 |
| [1.18.2](https://piston-meta.mojang.com/v1/packages/334b33fcba3c9be4b7514624c965256535bd7eba/1.18.2.json) | 200 / FETCHED | 3df8f7b5e0ae5ccfd73adc9e00daf407a7274b138daab5793e58d14f2ab74144 |
| [1.19.2](https://piston-meta.mojang.com/v1/packages/ed548106acf3ac7e8205a6ee8fd2710facfa164f/1.19.2.json) | 200 / FETCHED | daa5085a617194df8ab930c0b03161ef01a654ccd15cc57f97c659f4c96e986f |
| [1.20.1](https://piston-meta.mojang.com/v1/packages/a5cf661d31d9dfcd3d1645be80f43954f63f63b0/1.20.1.json) | 200 / FETCHED | e50169ba5c14ce07c82fb638118449c24f5eb5082e95005c480917aae3635be3 |
| [1.20.4](https://piston-meta.mojang.com/v1/packages/2c592ccd71ca2d5dadebeb6543ad6b18e6f43305/1.20.4.json) | 200 / FETCHED | cc81633f25e8e412a94dfb953a7b91702714e1e9ed1b680f520495d56d1ea301 |
| [1.21](https://piston-meta.mojang.com/v1/packages/c47b4c513b2883240565102b076054e347eac738/1.21.json) | 200 / FETCHED | cdd1a44db7b5e8787723c1f6c7c7dc3a4638d96a31ddc84aeb27d3f30efa802a |
| [1.21.1](https://piston-meta.mojang.com/v1/packages/499680d659b7a0ccb2fa9a809c345c5baf2ace7d/1.21.1.json) | 200 / FETCHED | 8047141a4d8de5ce23cc8390df56373b3a6c10f063d47b7bf3ea64e8c84666e9 |
| [1.21.10](https://piston-meta.mojang.com/v1/packages/b14d03617088d907aef01138b042e8e5c1ab35d4/1.21.10.json) | 200 / FETCHED | 3680286cdcfde9f4c540938a20d7fe917f5f189bf326791f6a9fc9d8798aea29 |
| [1.21.11](https://piston-meta.mojang.com/v1/packages/718cd84b4912691fe5de829aab6876a4b7f6c5c4/1.21.11.json) | 200 / FETCHED | 471a6eeadf1c74f84ed5d4290fb7234b746373478a4d6ac651962b93f0cb36d9 |
| [1.21.2](https://piston-meta.mojang.com/v1/packages/c14db17c663edf3d7a698488263a21b1df6d02af/1.21.2.json) | 200 / FETCHED | 793e3fd0451354a26aaa00253dcb6600add11f9d2a90f7bdef75ddf5b38c2b45 |
| [1.21.3](https://piston-meta.mojang.com/v1/packages/05284f7158ec319013fa51f7ff44f8132dc9f428/1.21.3.json) | 200 / FETCHED | 624e04bd23311f4a66a5226ee48d9642398a3adeadd43dbd81b037712d98e774 |
| [1.21.4](https://piston-meta.mojang.com/v1/packages/a1cebdbaa1a44b7d8214a81be1d94316a8404d87/1.21.4.json) | 200 / FETCHED | 4a1ab6e4e22a01c1144c0c6d61081fefaedb1b6d837f93b47973313f459632fc |
| [1.21.5](https://piston-meta.mojang.com/v1/packages/b341cd0e91419ab72b5d9dadad8d86a045d6b9a7/1.21.5.json) | 200 / FETCHED | 1751e36c5dda2bbf847d543d4f9a59c51035fe474b8528aca7f76c688f32fe88 |
| [1.21.6](https://piston-meta.mojang.com/v1/packages/8dd125560431a618094435343acccd45191bb006/1.21.6.json) | 200 / FETCHED | ea1c91ccb9760c9f7e697c29ed679427dd20cdac9ce35937125e5690973df6dd |
| [1.21.7](https://piston-meta.mojang.com/v1/packages/24c116056f9d403403d7b7c06fe018e75aaca464/1.21.7.json) | 200 / FETCHED | b7ebf2fb9a9cc655f874386a55731e87fa20d35fcbae43bb92ddb4df081fc51a |
| [1.21.8](https://piston-meta.mojang.com/v1/packages/5d557fffba309d5d68efa24a42bf73856008c5e3/1.21.8.json) | 200 / FETCHED | d439baefd3a0a208a3784d473e24ef8e92388a38afa2770af7723c9508d6366e |
| [1.21.9](https://piston-meta.mojang.com/v1/packages/91f383c21d8cd06abc9a569f2976b58da192a642/1.21.9.json) | 200 / FETCHED | 3cca801f41f83059092c88f7de3ea74247da4c394f3e672b7a41451151c293d5 |
| [26.1](https://piston-meta.mojang.com/v1/packages/8667c5278895a6ae31e05ab99ba044ef33fca092/26.1.json) | 200 / FETCHED | c4c4fc8662cc7023213adb94bd38c113730c663df594e548b99f53409365021b |
| [26.1.1](https://piston-meta.mojang.com/v1/packages/3a5e8b26e76711c22ce8391be68ada73983f2b95/26.1.1.json) | 200 / FETCHED | 94e2daa407e6fa9d3c9eac6bba11ef189dd9de1e87abb9b2cda59c2fbf3826bf |
| [26.1.2](https://piston-meta.mojang.com/v1/packages/8cca2c0efc47ef22351e5073bb1f5e7ab339279b/26.1.2.json) | 200 / FETCHED | eda7bac4a0a1ff847efccf5a51f66e990521b2c09320fecd3679bc6921c7623e |
| [26.2](https://piston-meta.mojang.com/v1/packages/91ef51b7d36ca092c5c02aba42f0f40c7cc1db84/26.2.json) | 200 / FETCHED | 8d009c6ed0b7b8c65bfff515a1ff8b12cc8df72627bb0e355ecbce9f7bc34f9c |
| [1.16.5-fabric-0.14.25](https://meta.fabricmc.net/v2/versions/loader/1.16.5/0.14.25/profile/json) | 200 / FETCHED | 9914d5d219bf7ff78dbb4bfb01d84303e4542442d287db941ea0501290b2c4af |
| [1.19.2-fabric-0.14.25](https://meta.fabricmc.net/v2/versions/loader/1.19.2/0.14.25/profile/json) | 200 / FETCHED | 43be48c0148fba9db302e7f43ca6a1b3e64553f1a5540c51364aa0568940389d |
| [1.20.1-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.20.1/0.19.5/profile/json) | 200 / FETCHED | c377ce45e0539b899e23ff1e21862892265c4360a60380faac6931d6c6566841 |
| [1.20.4-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.20.4/0.19.5/profile/json) | 200 / FETCHED | e59989fd491a4c3bc54fd30cd3a9c44b89a19e0bebd1418906e5540b9bb7aec0 |
| [1.21-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21/0.19.5/profile/json) | 200 / FETCHED | 8195dc3a3388118a238463f66b36ce4d51e3606f1c5b6a6c40dd116e61cafd29 |
| [1.21.1-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.1/0.19.5/profile/json) | 200 / FETCHED | deeaad9592bf8e47e8f9d9578cf03bd2f45f2895eb698560460e3533562ea5dc |
| [1.21.10-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.10/0.19.5/profile/json) | 200 / FETCHED | 5669a0d8483a93d05ecd6473992e4d187fdb2a323ee012bab829121b73ca896b |
| [1.21.11-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.11/0.19.5/profile/json) | 200 / FETCHED | 5f5f7769b2305da29cb73c19c3e5698c9dc6813326a13c373d7dda5be64827b3 |
| [1.21.2-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.2/0.19.5/profile/json) | 200 / FETCHED | 6a3214bbf836e4535fcf12f1c3ae2c4f7abd8b8d73c2241d2e9405d8fdb011c1 |
| [1.21.3-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.3/0.19.5/profile/json) | 200 / FETCHED | 145b43b1071f3043e2d9b72be242ccd16bbc6c14cbb7c5874c51ed6950261571 |
| [1.21.4-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.4/0.19.5/profile/json) | 200 / FETCHED | 907f6c8c519edee4c289a6c44874caa8ba4482f655c22b31002a8f004d91f21e |
| [1.21.5-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.5/0.19.5/profile/json) | 200 / FETCHED | c61078f1786089d9b04f19428b350ffbf2a85bee7847c6e30d3cbf5f5cb293d2 |
| [1.21.6-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.6/0.19.5/profile/json) | 200 / FETCHED | 206f383f6edc01328d8bcc5825d7b82ed3662748a066893f82c19be29a15f75d |
| [1.21.7-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.7/0.19.5/profile/json) | 200 / FETCHED | 548c76fc4700490f711ec3247fbb6d0eb481539f3e2d595d54b6cdc03f95c7a4 |
| [1.21.8-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.8/0.19.5/profile/json) | 200 / FETCHED | 06c3d3cf64ec47c220c81eef2763fe5e7a9fe438a8d2c2aef71b0d4b486174ea |
| [1.21.9-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/1.21.9/0.19.5/profile/json) | 200 / FETCHED | 702bb9412188bea7be8b1e45614a1d18894f8ce653e35509a50f17c1e630467e |
| [26.1-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/26.1/0.19.5/profile/json) | 200 / FETCHED | 9acf81691e951c20629fcbfe20645f5a9f7edf8daa2197baba9865a2fb9a86e4 |
| [26.1.1-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/26.1.1/0.19.5/profile/json) | 200 / FETCHED | 0458109c8c4f7f669a0ebb3493639a10035a6cd95659818d1cb6cb93066df59d |
| [26.1.2-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/26.1.2/0.19.5/profile/json) | 200 / FETCHED | 013349e571eaf9c4ccb5a05c27e741bd99c2f352d57ffa96cb48af9f44e312cf |
| [26.2-fabric-0.19.5](https://meta.fabricmc.net/v2/versions/loader/26.2/0.19.5/profile/json) | 200 / FETCHED | 7570c8a71e01817674afeb6d43975c163893384935345de0bad88298d8e7b53f |
| [Maven forge](https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml) | 200 / FETCHED | 197cb8638bfa8cda3c807785e465971de3d71506ceee689f4661495de041215c |
| [Maven neoforge](https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml) | 200 / FETCHED | 27766ff635d5a28e1bf339caa9bd0c78e0a3abc09254534a133dbfd0936df468 |

## Interpretation and remaining evidence

**Confirmed metadata** establishes only the recorded response content. Client and asset-index URL/SHA1/size are descriptors; no binary content was fetched. Library counts precede platform/rule selection. Fabric establishes exact inheritance/main-class/library-coordinate metadata without runtime testing.

The four 26.x Mojang version JSON documents declare Java 25 (java-runtime-epsilon). Every 1.21.x version here declares Java 21; 1.18.2/1.19.2/1.20.1/1.20.4 declare Java 17, and 1.12.2/1.16.5 declare Java 8. These are vanilla metadata requirements, not proof of loader compatibility or the Java major actually packaged by LegacyForge.

All 20 Fabric profiles identify the exact requested parent and loader. Four 26.x profiles list seven libraries and omit an intermediary coordinate. Fourteen profiles list eight libraries and two list eleven; those sixteen contain their exact intermediary coordinate. Absence of that older dependency pattern is recorded rather than treated as a version mismatch. An initial analyst check unnecessarily required intermediary in every profile; it was corrected to use exact parent and loader identity before finalizing this evidence.

**EXACT_RELEASE_LISTED** means the precise Forge minecraftVersion-loaderVersion or NeoForge loaderVersion occurs in the returned Maven index. Installer contents, processor inputs/outputs, patched artifacts and final module/classpath arguments remain unresolved by this check. A Maven listing never becomes a loader-installation or Xbox-gameplay pass.

The retained 1.12.2 Forge row stays unresolved because approved source says selected. Both 1.12.2 providers remain absent. HTTP failures, network unknowns, returned-index absence and unresolved versions are kept distinct. No target is dropped.

Actual Windows/update/repair tests still require an approved disposable environment. [E20's hash-pinned positive fixture](SIGNED-UPDATE-FIXTURE.md) is now available and independently verifies against the embedded trust anchor; actual updater acceptance, malformed-input rejection and recovery remain unexecuted. Real Xbox tests still require approved exact packages, diagnostic probes and owner hardware observations; legitimate account tests remain owner-controlled. Metadata cannot replace missing runtime/account/history evidence.

The execution plan now records the observed vanilla Java baseline and exact metadata URL/SHA1/SHA256 for every row, with `current` expected major25 for all twelve current-family rows. Fifty-one source runtime labels match the vanilla declared major; five select a higher Java major. None is below the declared vanilla baseline. This compares labels with metadata only: a higher major is not proof that an older loader, game, native library or filesystem patch works with it. Exact packaged runtimes, JNI versions and all 56 hardware outcomes remain unverified.
