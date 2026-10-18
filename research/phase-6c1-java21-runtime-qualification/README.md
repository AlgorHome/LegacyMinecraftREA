# Phase6C.1 - Java21 runtime qualification

**Recommended candidate: Eclipse Temurin HotSpot JDK21.0.12.1+1-LTS, Windows x64. J0 readiness: BLOCKED.** This is an exact candidate for further qualification, not an approved UWP runtime or a fully authenticated package input.

VERIFIED: an existing local image at `C:\Users\arinze\AppData\Local\LegacyForge\jdks\jdk-21.0.12.1` contains490 files/343,823,876 bytes;127 PE files all report x64. All files were independently SHA-256 hashed. Six selected JVM/Java/JLI/CRT files have Valid Windows Authenticode observations. JVM exports and local JNI headers were read statically. No Java DLL was loaded or runtime executed.

DOCUMENTED: [Adoptium release](https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.12.1%2B1) and publisher API identify the ZIP `OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip`,205,073,461 bytes, published SHA-256 `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e`. This is a **publisher-declared archive hash**, not a locally calculated ZIP hash. The original ZIP is not in the inspected local candidate locations. Extracted-image metadata/signatures do not establish byte-for-byte equality with that archive.

BLOCKED: authenticating the complete archive/member set; reviewing the exact proposed J0 package allowlist/CRT resolution; unresolved Xbox system/API-set/delay-load/dynamic dependency behavior; later implementation and execution approvals. Static dependency evidence is detailed in [inventory](NATIVE-DEPENDENCY-INVENTORY.md), not presented as complete runtime closure.

## Evidence vocabulary

VERIFIED = directly inspected local bytes or locally recomputed comparison. DOCUMENTED = official publisher/specification statement. INFERRED = design/interpretation requiring validation. UNKNOWN = insufficient evidence. BLOCKED = an unmet input/approval prevents a gate. An export, query, VM creation, Java result and cleanup are separate observations.

## Documents

[CANDIDATE-COMPARISON](CANDIDATE-COMPARISON.md), [SELECTED-RUNTIME](SELECTED-RUNTIME.md), [LICENSE-AND-PROVENANCE](LICENSE-AND-PROVENANCE.md), [NATIVE-DEPENDENCY-INVENTORY](NATIVE-DEPENDENCY-INVENTORY.md), [UWP-COMPATIBILITY-RISKS](UWP-COMPATIBILITY-RISKS.md), [JNI-CONTRACT-REVIEW](JNI-CONTRACT-REVIEW.md), [J0-J1-J2-ACCEPTANCE-PLAN](J0-J1-J2-ACCEPTANCE-PLAN.md), [REQUIRED-DOWNLOADS-AND-APPROVALS](REQUIRED-DOWNLOADS-AND-APPROVALS.md), [BASELINE-PRESERVATION](BASELINE-PRESERVATION.md), [DECISION-REPORT](DECISION-REPORT.md).

Only new analytical documents/metadata were created. No runtime archive download/extraction, code implementation, compilation, signing, installation, Java loading/execution, Xbox access, game/auth operation or certificate/trust configuration change. Public web/API/license/specification metadata was read; the Corretto URL check used HEAD without receiving the archive body. No Bandit bundle/patch/source imported.

Research date2026-10-17 America/Chicago. Exact publisher retrieval UTC recorded in PUBLISHER-METADATA.json (UTC date may beOct18). Existing SRV03 unsigned branch/artifact and all accepted baselines preserved; state not changed by qualification.
