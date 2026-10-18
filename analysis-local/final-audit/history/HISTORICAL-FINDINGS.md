# Historical evidence audit

This pass reads only `logs/launcher.log*` and `legacy/Minecraft/game/logs/*.log*` under the supplied `.tlauncher` root. It executed no launcher, installer, game, authentication flow, or console command. **Confirmed below means a recorded message exists in a hashed historical log.** It does not certify the assertion, sender, clock, success, file integrity, or a newly observed run.

Six source files contain 26,994 lines, yielding 16,372 allowlisted structured records. Five lines matching the explicit sensitive-field exclusion were wholly omitted; no raw lines are retained. Unmatched fields, queries, credentials, account/device identifiers, command lines, and local path values are excluded. The larger record counts include repeated progress messages; they are not counts of unique downloads, game sessions, or independently observed events.

## Findings and boundaries

| Finding | Historical source and exact location | Assessment |
|---|---|---|
| Every retained launcher log opens with the newer launcher and bootstrap identities: 1.169.4 and 1.40.3. | `logs/launcher.log`, `.1`, `.2`, `.3`: lines 2 and 3 in each file; sanitized records 1-2, 107-108, 148-149, 160-161. | Confirmed recorded identities. No retained record mentions the archived 1.159.2 or 1.32.2 identities. The installer-to-installed update transition is still unknown within this bounded log set. |
| The older Mojang version catalog endpoint is recorded. | `logs/launcher.log.3`: lines 31 and 36, records 168-169, clock values 00:51:08.810-00:51:08.943; also present in the other three launcher logs. | Confirmed URL mentions: `https://launchermeta.mojang.com/mc/game/version_manifest.json`. Log presence does not prove a particular HTTP response or downloaded body. |
| The selected 1.21.11 profile URL follows the catalog record. | `logs/launcher.log.3`: line 80, record 191, 00:52:31.437. | Confirmed public URL mention with package hash `718cd84b4912691fe5de829aab6876a4b7f6c5c4`. |
| Asset/runtime metadata follows the selected profile. | `logs/launcher.log.3`: asset-index endpoint at lines 113-114; runtime-manifest endpoint at line 124; endpoint grouping in `historical-findings-index.json`. | Confirmed metadata mentions. The local profile and previously collected static verification remain the authority for how the metadata fields are interpreted. |
| This retained record set mentions Mojang runtime content, 4,591 unique asset URLs, 43 unique allowlisted library URLs, and one client JAR URL. | `logs/launcher.log.3`: runtime/other object URLs first line 142 and last line 5154; asset URLs first line 2926 and last line 25875; allowlisted library URLs first line 25884 and last line 26335; client JAR URL lines 26342-26343. | Confirmed public URL mentions. The library count is deliberately limited by the URL allowlist and is not the complete library count. Runtime and assets overlap in the recorded ordering. A URL mention alone is not a completed or verified transfer. |
| A fixed download-completion message is recorded after those transfer messages. | `logs/launcher.log.3`: line 26360, record 16260, 00:54:59.510. | Confirmed recorded completion message; no independent transfer capture or fault injection occurred. |
| Java 21.0.7 and backend LWJGL 3.3.3+5 are recorded after completion. | `logs/launcher.log.3`: Java lines 26372-26373, records 16268-16269, 00:55:01.631; LWJGL line 26393, record 16276, 00:55:10. The corresponding compressed game log has LWJGL at line 4, record 16306. | Confirmed technology version messages. No inference that Xbox uses this Java build or graphics stack. |
| OpenAL initialization and sound-engine startup are recorded. | `legacy/Minecraft/game/logs/2026-10-17-1.log.gz`: decompressed lines 19-20, 00:55:14; mirrored in `logs/launcher.log.3` lines 26408-26409. `latest.log` has the same event classes at lines 19-20 and 50-51. | Confirmed messages. Launcher/game logs duplicate some messages; these are not six independent successful sessions. No audible output, device choice, input, graphics rendering, or gameplay was observed by this audit. |
| Two launcher records report game process exit code 0, following stopping messages. | `logs/launcher.log.3`: stopping line 26437, exit line 26439, record 16302, 00:56:04.603. `logs/launcher.log`: stopping line 213, exit line 215, record 103, 00:58:36.963. Game logs end with stopping messages at decompressed `.gz` line 48 and `latest.log` line 67. | Confirmed recorded exit codes only. This narrows the lack of any historical launch/exit evidence, but does not establish fault recovery, gameplay, resource behavior, or a new clean test pass. |
| HTTP 502 is also recorded in each launcher session containing game exit evidence. | `logs/launcher.log.3`: line 26446, record 16305, 00:56:06.851. `logs/launcher.log`: line 142, record 59, 00:57:03.180. | Confirmed recorded HTTP status only. Request identity and account-related values were not retained or analyzed, and the status is not an entitlement verdict. |

Clock values are copied as recorded; no timezone assumption is applied. Cross-file ordering and rotation order are not asserted. The date-bearing game filename identifies one retained file; it does not independently authenticate the clock. All line numbers for `.gz` refer to the decompressed UTF-8 text, not compressed byte offsets. Record ordinals are one-based positions in `historical-evidence-sanitized.json`'s `records` array and are repeated in the selected-event index.

## Work still requiring different evidence

The historical logs close the absence of any recorded desktop download/start/audio/exit sequence. They do **not** complete approved disposable-Windows installation, fault/interruption/repair/update/recovery tests, present account authentication/entitlement tests, exact historical acquisition or intermediate update provenance, or packaged Xbox tests across the 56 catalog targets. Those remain blocked by the previously stated environment and execution constraints. No historical message has been converted into a PASSED dynamic-test result.

## Local evidence files

- `collect_history.py`: input scope, privacy allowlist, fixed event recognizers, and output policy.
- `historical-evidence-sanitized.json`: input hashes and all allowlisted records; no raw log text.
- `historical-evidence-summary.json`: aggregate counts and deduplicated public endpoints.
- `summarize_history.py` and `historical-findings-index.json`: category first/last references and the small selected-event index.
- `validate_history.py` and `validation.json`: source hash stability and output schema/privacy validation.

All files in this directory are analyst-created local evidence. No production source was changed and no artifact was committed, pushed, or redistributed by this pass.
