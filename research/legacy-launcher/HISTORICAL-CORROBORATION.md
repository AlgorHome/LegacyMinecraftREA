# Historical corroboration [E18]

E18 is a bounded, offline audit of six existing log files. It adds historical records of a desktop download/start/audio/exit sequence. **Confirmed here means that the specified message was recorded in a source with the listed SHA-256.** No installer, launcher, game, account flow, or Xbox test was executed by this audit; no execution test receives a PASS.

The compact, publication-safe evidence is [evidence/historical-corroboration.json](evidence/historical-corroboration.json). Raw logs, command lines, account/device identifiers, credentials, URL queries, and the complete asset URL list are excluded.

## Input boundary and identities

Paths below are relative to the supplied `.tlauncher` root. The two game logs are limited to the supplied `legacy/Minecraft/game/logs` directory. Compressed-log line numbers refer to decompressed UTF-8 text.

| Source | Lines | SHA-256 |
|---|---:|---|
| `logs/launcher.log` | 223 | `4c9e0489a1c7e4e42a9e70299e842a411f96539cef42706785c2c0e5d9edfb62` |
| `logs/launcher.log.1` | 162 | `cc8a61c5ac5f9e560faefd23d1629b0d05032f815d2f5a3e4500e7a815d905e0` |
| `logs/launcher.log.2` | 47 | `9165f4817a047d5eb31ad3dfc944f89c693c6a248f04008b47d9619b461e78fb` |
| `logs/launcher.log.3` | 26,447 | `d0c00a3357727c644fdf176f0f367cbe9cda3337f9423826705d612bbdd008f3` |
| `legacy/Minecraft/game/logs/2026-10-17-1.log.gz` | 48 | `b625a78bcaaa2142a4372d9d75b6badd2041c69d715b47b683f91a0e36c824b9` |
| `legacy/Minecraft/game/logs/latest.log` | 67 | `9585099fff1b81224ddf9d396fa2ca0f62b2c5c4a4900ce4ba2ae6dd517d97f2` |

The six files contain 26,994 lines. An allowlist-only parser retained 16,372 local structured records, including repetitive progress messages; five lines matching explicit sensitive-field exclusions were omitted in full. These are record counts, not independent downloads or sessions. Output schema/privacy validation passed and source hashes remained stable at validation.

Each launcher log records the newer launcher **1.169.4** at line 2 and bootstrap **1.40.3** at line 3. No retained record mentions the archived **1.159.2** or **1.32.2** identities. Consequently, these logs do **not** establish the archived-to-installed update transition, intermediate versions, acquisition history, or publisher authenticity.

## Recorded sequence

This table follows source-line order in `logs/launcher.log.3`; runtime and asset transfers overlap. Clock values are reproduced as technical fields, with no timezone assumption or cross-file chronological claim.

| Recorded evidence | Source lines | Clock as recorded | Interpretation limit |
|---|---|---|---|
| Mojang version catalog URL | 31, 36 | 00:51:08.810–00:51:08.943 | Mentions `https://launchermeta.mojang.com/mc/game/version_manifest.json`; does not independently prove the response body. |
| Minecraft 1.21.11 version-profile URL | 80–82 | 00:52:31.437–00:52:32.604 | Public metadata mention; package hash `718cd84b4912691fe5de829aab6876a4b7f6c5c4`. |
| Asset index and runtime manifest URLs | 113–114; 124 | 00:52:32.774–00:52:34.187 | Corroborates the metadata stages documented in the static installation pipeline. |
| 196 unique Mojang runtime/other content URLs | 142–5154 | 00:52:34.441–00:52:53.873 | Bounded public `/v1/objects` endpoint mentions, excluding the client JAR; not an independently verified runtime transfer count. |
| 4,591 unique asset URLs | 2926–25875 | 00:52:39.053–00:54:38.523 | Endpoint mentions under `resources.download.minecraft.net`; transfer completion/integrity requires separate evidence. |
| 43 unique allowlisted library URLs | 25884–26335 | 00:54:38.541–00:54:49.134 | Partial count imposed by the public URL allowlist; not the total library inventory. |
| Client JAR URL | 26342–26343 | 00:54:49.144 | Public object hash `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`. |
| Download-completion event | 26360 | 00:54:59.510 | Recorded completion assertion; no fresh transfer capture or interruption test. |
| Java 21.0.7 | 26372–26373 | 00:55:01.631 | Recorded technology version, not the deployed Xbox runtime identity. |
| LWJGL 3.3.3+5 | 26393 | 00:55:10 | Recorded backend version, also present at decompressed game-log line 4. |
| OpenAL initialization and sound-engine startup | 26408–26409 | 00:55:14 | Also at decompressed game-log lines 19–20; duplicate records do not establish separate sessions or audible output. |
| Game stopping, then process exit code 0 | 26437; 26439 | 00:56:04; 00:56:04.603 | Recorded desktop exit status; not a gameplay, recovery, or Xbox verdict. |

The later `logs/launcher.log` also records LWJGL 3.3.3+5 at line 150, audio initialization/startup at lines 165–166 and 196–197, stopping at line 213, and exit code 0 at line 215. The corresponding `latest.log` records backend identity at line 4, audio events at lines 19–20 and 50–51, and stopping at line 67. These overlaps must not be counted as independent observations.

HTTP status 502 also appears at `logs/launcher.log.3:26446` and `logs/launcher.log:142`. This audit retains only the status code; it does not attribute those records to an account action or treat them as an authentication/entitlement verdict.

## What this resolves and leaves open

The audit supplies previously unindexed historical corroboration for the official catalog/metadata/content download chain and recorded desktop Java/backend/audio/exit behavior. Historical logs can be edited, rotated, incomplete, or affected by clock changes; message presence does not authenticate a sender or independently validate a claimed operation.

Disposable-Windows installer/fault/interruption/repair/update/recovery tests, present account authentication and entitlement tests, exact acquisition/intermediate-update provenance, and packaged Xbox runtime/graphics/audio/input/lifecycle/gameplay tests across all 56 catalog targets remain unresolved or BLOCKED under the existing infrastructure and execution constraints. None has been silently removed or replaced with a historical PASS. E18 changes no production code, authentication, or entitlement checks.
