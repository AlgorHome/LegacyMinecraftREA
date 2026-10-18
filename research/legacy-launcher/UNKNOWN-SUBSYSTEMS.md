# Remaining unknowns and blocked tests

Research continuation: 2026-10-17. Scope retains every mission phase and all 56 approved target rows.

| Area | Updated evidence / remaining condition | Status |
|---|---|---|
| Installer contents |770 decoded/checksummed records; original launcher 1.159.2/bootstrap 1.32.2; 431 installed content matches | Confirmed static recovery E11 |
| Historical authenticity/acquisition/update chain | Unsigned artifact; mutable timestamps; no independently authenticated publisher release hash or event history | Unknown historical facts; not recoverable from an unrecorded event |
| Retained desktop history | Six hashed logs corroborate recorded metadata/download/start/audio/exit sequence; all already identify launcher 1.169.4/bootstrap 1.40.3 | Confirmed message presence E18; no archived-build transition, fresh execution or Xbox pass |
| Wrapper/bootstrap declared linkage | Embedded launcher/bootstrap.jar and JRE/restart config offsets; native CreateProcess call | Confirmed static configuration E06/E11; execution BLOCKED |
| Update verification/replacement | Signed-path framing/key/algorithms, checksum/temp/copy/restart and local/remote comparison traced in original/installed code | Confirmed static branches E12/E13; failure/durability/replay/rotation outcomes Unknown/BLOCKED |
| Update positive fixture | E20 public response independently verifies against the identical archived/installed embedded key; raw fixture retained locally | Fixture availability Confirmed; actual target verifier/updater behavior remains BLOCKED |
| Configuration/accounts | Properties/Gson temporary sibling writes/moves, migration/backup and token-string serializer/refresh paths traced | Confirmed static E12; actual account values not read; OS protection/crash behavior Unknown |
| Forge/Fabric resolution | Official/extra profiles, duplicate/parent inheritance handling, Forge-family mod-list/classpath/argument paths traced | Confirmed static E13; exact remote-generated loader/processor execution BLOCKED |
| Full upstream catalog plans | E21 verifies22 unique Minecraft JSONs,20 exact Fabric profiles and34 resolved Forge/NeoForge Maven releases, retaining unresolved Forge and vanilla rows | Confirmed metadata presence/hash identities; processors, patched artifacts and hardware execution remain BLOCKED |
| Downloader recovery | Partial/range/redirect/error/abort and integrity branches traced | Confirmed static E12; packet-loss/disk-full/interruption/concurrency outcomes BLOCKED |
| Minecraft service support/registration | Generic official Microsoft/XSTS contracts found; no public authoritative Minecraft launcher API contract established | Unknown current permission/scopes; live tests BLOCKED, no credentials |
| Java 17/8/JNI21 |Source selection discrepancy and JNI contract confirmed; packaged runtimes absent | Execution BLOCKED until exact artifacts and approved isolated/device environment |
| Native loading/graphics/input/audio |291 native occurrences/import/export graph; shim/GameInput/Mesa/lifecycle source audited | Static inventory complete within declared format bounds; dynamic resolution, ABI/device behavior BLOCKED |
| Xbox resources/lifecycle | Actual package/resource/driver/console evidence not available | Owner-run X01–X13 BLOCKED; procedures prepared |
| Every catalog target |56 rows retained, all new runtime verdicts explicitly BLOCKED | No row omitted or silently called PASSED |
| Legacy Forge exact version | Approved 1.12.2 Forge row literally says `selected`; both 1.12.2 providers are absent | Exact loader resolution and provider implementation remain required; no production edits made |
| Diagnostic artifacts | X03–X08 require an independently built and approved diagnostic package | Source preparation and checker controls do not establish packaged JNI/native/graphics/input/audio behavior |

See PHASE-STATUS, WINDOWS-SANDBOX-TESTS and XBOX-SERIES-X-TESTS for full criteria. User explicitly confirmed no configured VM, no Device Portal/remote console access, and static-only authorization. No installations, unknown binary execution, device connections, account tests or production changes occurred. Remaining infrastructure work requires later explicit owner approval and evidence; it is not a reason to stop useful static analysis or invent successful tests.
