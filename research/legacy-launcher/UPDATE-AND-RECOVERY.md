# Bootstrap updates, configuration, accounts and recovery

Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.

## Signature and update handling [E12/E13]

This continuation distinguishes archived bootstrap 1.32.2 from installed1.40.3. Both contain direct signature-checking instructions, rather than merely suggestive class names.

| Observation | Exact static locator | Status / scope |
|---|---|---|
| Installed update URI template | UpdateMeta$1.lambda$fetchUpdateMeta$0 offset 3: https://%s/%s/bootstrap.json.mgz.signed | Confirmed endpoint construction; selected host/traffic not observed |
| Signature required for signed-path response | Installed UpdateMeta.readQueue: URL.getPath→endsWith(.signed) offsets 73–81; SignedStream construction120–126; explicit validateSignature155 | Confirmed conditional policy; not universal signing of every possible URL/input |
| Archived response verification | Archived UpdateMeta.fetchAttempts: .signed114, SignedStream157/163, explicit validateSignature192 | Confirmed older implementation has corresponding path |
| Signature framing/key | SignedStream.readSignature expects 256 bytes; installed class initializer reads public.der, builds X509EncodedKeySpec/RSA key | Confirmed compiled trust anchor; source/public-key rotation policy unknown |
| Algorithms | ChecksumStream uses SHA-256; validateSignature encodes digest text; verify selects SHA1withRSA | Confirmed exact historical scheme; do not call it SHA256withRSA or invent a vulnerability |
| Failure | Missing/truncated framing throws StreamNotSignedException; invalid verification throws InvalidStreamSignatureException; signature exception returns false | Confirmed narrow failure branches; interruption/real remote responses untested |
| Metadata parsing | UpdateMeta.fetchFrom reads stream to string and Gson; readQueue explicitly validates before accepting signed result | Confirmed static order; callers supplying raw inputs are a separate trust boundary |
| File download | bootstrap DownloadTask.downloadUrl: connect10,000 ms, read5,000 ms; temp file; SHA256 compare when supplied; create destination directories; Files.copy(REPLACE_EXISTING) | Confirmed; replacement copy is not evidence of atomic replacement or power-loss durability |
| Copy/retry/cleanup | DownloadTask executes URL candidate loop; handles copy/lock failures; temporary file deletion on normal/finally paths | Confirmed branches; all filesystem failure combinations require dynamic tests |
| Bootstrap self-replacement | Updater.doUpdate downloads to temp; reopens input/output and copies; Updater.execute optionally restarts via ProcessBuilder.start | Confirmed; traced method has no demonstrated transactional old-version backup/rollback |
| Launcher selection | Bootstrap$4.execute compares local/remote versions and SHA256; can retain newer local version or fetch remote; Bootstrap$1 downloads libraries; Bootstrap$2 invokes IPC start | Confirmed source behavior; exact historical update chain remains Unknown |

Raw public keys and reconstructed method listings stay local. The presence of a signature scheme does not authenticate a separately obtained installer and does not establish every update transport policy.

**Confirmed continuation [E20]:** a bounded public metadata fixture now independently verifies against the same embedded archived/installed key, with locally modified payload/signature controls rejected by the independent verifier. [Exact response and limits](SIGNED-UPDATE-FIXTURE.md) close fixture availability. Actual updater acceptance, rejection, application, interruption and recovery are still BLOCKED; the target verifier was never executed.

## Configuration and profile persistence [E12]

SimpleConfiguration.save writes Java Properties to `<settings>.tmp`, closes the stream, then Files.move. ProfileManager.saveProfiles writes Gson JSON to a temporary sibling and moves with REPLACE_EXISTING. The observed ProfileManager call uses no ATOMIC_MOVE flag. ProfileManager.loadProfiles has migration/read-error/backup-writing branches. This improves the previous “configuration recovery untraced” status, but no crash/power-loss or full-disk tests were run.

MinecraftUserJsonizer MicrosoftTokenPayload constructor directly copies access-token/refresh-token strings and expiry into payload fields; MinecraftTokenPayload copies game token and expiry. Its serializer uses Gson to build JSON, which ProfileManager writes through normal Java output streams. **Confirmed:** token strings are application-level JSON serialization fields in this traced persistence path; no encryption/vault operation appears on that path. **Unknown:** actual saved account contents, OS encryption/ACLs and protections outside this path. No real token/profile was read and no vulnerability is asserted solely from architecture.

MinecraftOAuthRefresh.refreshIfNeeded first attempts a profile request with the supplied game token; a profile-request exception routes to refreshExplicitly. refreshExplicitly repeats Microsoft refresh→XBL→XSTS→Minecraft→ownership→profile→conversion. Plain/authlib/Ely/Mojang/Microsoft provider classes and serializers remain separate. Do not carry alternative-provider behavior into LegacyForge's legitimate ownership boundary.

## Game downloader recovery [E12]

DownloaderTask.run distinguishes PartialDownloadException, GaveUpDownloadException and AbortedDownloadException; exhausted/error branches remove destination/auxiliary files and notify completion/error handlers. downloadURL supports partial-file length checks and append output, Accept-Ranges/resume handling; setupConnectionFollowingRedirects handles Range/206, success codes and 301/302/307/308 Location redirects, with a10-redirect limit branch. DownloaderTask.download separates local I/O failures from remote retries/fallback. Sha1Downloadable/AssetDownloadable still validate content at completion.

**Unknown until execution:** actual retry timing under packet loss, interruption races, disk-full results, final-file visibility during partial writes and metadata trust under hostile replacement. Static path extraction into a directory does not establish canonical path confinement; all untrusted ZIP paths and repository-controlled destination normalization need their own explicit validation. No “safe extraction” or remotely exploitable finding is inferred without reachability/reproduction.

## Independent LegacyForge implications

Keep content integrity, metadata authenticity, transaction/durability and account protection separate. Extend existing repair receipts. Preserve PasswordVault and entitlement checks. If independently designing signed metadata, specify a current approved trust/rotation policy; do not copy this launcher's key material or historical algorithm choices. Windows fault-injection tests in WINDOWS-SANDBOX-TESTS are BLOCKED.

## Additional path/configuration traces [E12/E13]

Installed MinecraftLauncher.unpackNatives directly combines the native directory with ZipEntry.getName (offsets 337–340) and opens the resulting path for output (387). Its decoded direct path has directory/META-INF filtering but no demonstrated canonical-child containment check. Reachability of attacker-controlled archives and exploit impact were not established; this is not a confirmed vulnerability. Independent extraction should reject absolute/traversal/link escapes, and blocked guest tests should exercise synthetic ZIP names within a disposable environment. Do not copy this extraction pattern as a safety contract.

Configuration.init extracts argument configuration entries (35), tracks constant argument values (333), parses configuration representations (376) and attempts a save (722) with an I/O error handler. This confirms command-line/config interaction and persistence branches; actual precedence for every setting remains an observation target for W08, rather than a fabricated universal ordering.
