# Missing artifacts and separate approval gates

No runtime archives downloaded. Public web/API metadata, license/specification pages and a body-free Corretto HEAD lookup were used for research only. Existing local runtime was read in place, not copied, extracted, packaged or executed.

## Smallest next provenance gate

Either provide an existing original official archive path for read-only verification, or separately authorize acquisition of the following exact publisher artifacts into a new qualification evidence location. This document is not that authorization.

| Artifact | Official URL | Expected identity/status |
| --- | --- | --- |
| Selected ZIP | https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip |205,073,461 bytes; published SHA256 `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e` |
| Published checksum text | https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip.sha256.txt | Metadata value should agree; not an independent signature |
| Detached signature | https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip.sig | Must verify against exact ZIP and independently authenticated Adoptium publisher key |
| Artifact build metadata | https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip.json | Version/build/source/provenance cross-check |
| Publisher verification key/instructions | Official Adoptium channel; exact fingerprint still UNKNOWN | Public key only; establish trusted fingerprint independently, not from the same untrusted attachment |
| Version-matched source archive/notices | Official release source asset OpenJDK21U-jdk-sources_21.0.12.1_1.tar.gz and sidecars,115,126,841 bytes | Optional for initial private provenance comparison if not needed there; redistribution source-compliance route still needs review before release |

After such approval: checksum and detached-signature verification; safe read-only archive-member examination (no installers/executables); map each needed member to local files and record any differences; no overwrite of the local image. Any archive extraction must also be within that explicit read-only qualification/staging authorization. Stop on checksum/signature/version/member mismatch. No current tool/download/signer installation is authorized.

The ZIP is the preferred reference; no MSI/EXE installation is needed. Do not obtain alternative vendors, Java17/8/25, Minecraft, Bandit bundles or patch archives just to qualify this first candidate. If an authenticated member manifest is obtained instead of ZIP, record exactly what it authenticates and retain remaining gaps.

## Package-policy gate after provenance

Approve the exact J0 module list, package-relative paths, CRT/framework scheme, no-VM call policy and known unresolved system imports for a controlled experiment. Existing installed VCLibs may suffice, but cannot be assumed to substitute exact imports; no fallback dependency download/install. Do not copy host system DLLs, bypass package loader policy or add capabilities as an unreviewed repair.

## Later approvals

Separate J0 source/unsigned-build approval; then independent signing, installation-only, one launch, receipt retrieval, formal acceptance and cleanup approvals. Repeat explicit gates for J1 and J2; success of one does not authorize another. JVM query/creation implementation is outside this phase. D00 native-only lock stays intact; proposed Java identity remains separate.

**J0 readiness: BLOCKED.** Precise preparation inputs missing: authenticated whole-image/archive linkage (especially unsigned lib/modules/config), approved module/CRT policy and source/build authorization. Xbox API behavior remains UNKNOWN and may be tested under a later controlled risk acceptance, without first requiring a successful runtime.
