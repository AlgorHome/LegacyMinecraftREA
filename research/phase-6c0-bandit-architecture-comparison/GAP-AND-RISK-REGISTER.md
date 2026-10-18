# Gap and risk register

Research-only snapshot. Bandit pin `ba42117784ce201eb10ab5220ee25382e76cec1f`; source links below or in [inventory](UPSTREAM-SOURCE-INVENTORY.md). Priority describes investigation value, not likelihood/probability or a promised timeline.

| ID / priority | Evidence classification and confidence | Unresolved obstacle | Consequence | Smallest evidence needed / disposition |
| --- | --- | --- | --- | --- |
| R01 P0 | VERIFIED_LOCAL high: six sampled source-file hashes equal | Existing code provenance/permissions not established here | Public redistribution decision cannot rely on public readability | Review ownership/grants and notices; no code changes in this phase |
| R02 P0 | UNKNOWN runtime identity; source packaging high | Official Java21 vendor/build/hash/license and import closure unselected | Cannot responsibly package or execute VM probe yet | Static candidate inventory and dependency/license review before J0 |
| R03 P0 | UPSTREAM_SOURCE_OBSERVED JNI21; VERIFIED_LOCAL same call | No accepted LegacyForge embedded VM/checksum result | Minecraft feasibility remains fundamentally open | J0 load, J1 query, J2 interpreter-only original Java, separate cold processes |
| R04 P0 | UNKNOWN JIT/AOT/platform constraints | Dynamic executable-memory/actual compiled-method behavior | Pure interpreted success may not support intended workload | J3 real compilation witness later; no arbitrary code/security change |
| R05 P1 | VERIFIED_LOCAL D3D11 passes only; UNKNOWN D3D12 | Hardware D3D12 device availability on exact package/Series X build | Mesa route may fail before GL startup | N12 single hardware device case, no resources/queues/presentation |
| R06 P1 | UPSTREAM_SOURCE_OBSERVED WGL calls; source labels high, binary provenance UNKNOWN | Mesa DLL source/build/signature/SBOM/ABI closure | Cannot assume tracked binary distribution is safely reusable | M0 provenance first; independent exact candidate before M1 |
| R07 P1 | Source shows WGL versus EGL doc drift | Context ABI/thread ownership/GL extensions | EGL-only reconstruction could target wrong backend | Specify independent candidate's actual window/context contract |
| R08 P1 | VERIFIED_LOCAL source concern, UNKNOWN run | Multiple CoreWindow swapchain ownership | Startup/graphics initialization can fail despite native device pass | One exclusive backend/window owner, later controlled present fixture |
| R09 P1 | UNKNOWN full lifecycle | JVM, context/audio/input behavior on suspend/close/resume | A launch success could still lose state or hang | Later original lifecycle fixture with real owner-induced transitions |
| R10 P1 | VERIFIED_LOCAL sampled memory only | Actual VM/GL/GPU budgets, peaks and cleanup | Game-sized workload may exceed app resources | Bounded memory receipts; no quota/exhaust-to-crash experiment |
| R11 P1 | UPSTREAM_DOCUMENTED input; source implements callbacks | Controller/text/mouse build-specific transitions | Implemented APIs may fail focus/reconnect or optional peripherals | Prompted native transitions and exact build identity; no inferred pass |
| R12 P1 | UPSTREAM_DOCUMENTED OpenAL dependency, UNKNOWN output | Exact native audio closure and audible behavior | Startup/library success is not audible proof | Original platform PCM first, separately approved OpenAL later |
| R13 P1 | Source/module patches high; UNKNOWN full Java IO | UWP File/NIO/ZIPFS/locking/natives assumptions | Mod loaders may fail after VM startup | Own-directory bounded Java IO/ZIPFS cases; never weaken sandbox |
| R14 P1 | VERIFIED_LOCAL/UPSTREAM_SOURCE_OBSERVED catalog |1.12.2 provider absent, Forge selected unresolved, jre8 not packaged by inspected path | Catalog row is not a launchable target | Keep deferred; metadata/provider/runtime/LWJGL2 questions separate |
| R15 P1 | UPSTREAM_DOCUMENTED experiment catalog; high source labels | Forge/NeoForge target-specific processors/patches/modules | Native passes do not demonstrate loader/game support | Exact target/artifact plan only after independent runtime/GL prerequisites |
| R16 P2 | VERIFIED_LOCAL S21 disabled, SRV03 static-only | New mission's SRV03 state is stale | Could waste rebuilds or mislabel it hardware-accepted | Preserve deb4407 unsigned artifact; do not execute automatically |
| R17 P2 | UPSTREAM_DOCUMENTED inconsistent config/docs | Fabric0.19.5 vs older0.19.2/0.19.3 references, mouse/EGL prose | Wrong support/runtime assumptions | Prefer pinned config/source contract; retain contradictions |
| R18 P1 | VERIFIED_LOCAL previous signing result | Windows chain trust fails0x800B0109 while CMS/content pass | Cannot call normal chain validation successful | Keep separate; no trust import or re-sign authorized |
| R19 P1 | Owner-reported host7.8GB RAM/~30GB free; not re-inventoried | No disposable Windows guest available; limited build space | Full Windows11 VM/Mesa toolchain can exceed available resources | Keep Windows execution BLOCKED; small existing-tools source builds later, no automatic VM/features change |
| R20 P1 | Historical local acceptance uses owner receipts/photos | No independently signed hardware attestation; clocks/telemetry limited | Cannot extrapolate timings/compatibility across versions | Preserve exact run/build/member hashes; label owner provenance |

## Independent implementation boundary

Useful concepts: per-target verified content plan; explicit runtime/graphics/input/audio adapters; packaged-native dependency inventory; one-case receipts; fail-closed capability checks; one VM per cold activation. These are platform/design concepts, not authorization to import the upstream implementation. The exact production files already present are frozen, not retrospectively declared independently authored.

## Minecraft and loaders

Bandit docs specify legitimate device sign-in, token exchange/entitlement/profile then verified official downloads. Source catalog stores target tuples, not proof of independent gameplay. Vanilla/Forge1.12.2 legacy rows remain unimplemented; Forge's literal selected is not an exact Maven release. Generic Forge dispatch exists, so calling all Forge support absent is wrong. Loader metadata readiness is not a guarantee an old installer or LaunchWrapper/LWJGL2 path works. The prior [1.12.2 assessment](../phase-6b-runtime-validation/LEGACY-1.12.2-ASSESSMENT.md) keeps those blockers separate. No game/authentication/download action proposed in first probes.
