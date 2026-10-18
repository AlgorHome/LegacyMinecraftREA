# Xbox Series X owner-run validation procedure

Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.

**Status: BLOCKED.** Real Xbox Series X/Developer Mode and prior APPX deployment were reported by the owner. No Device Portal address or Codex remote access is configured. The owner can install approved packages manually. No console connection, authentication, deployment or execution was attempted. No credentials are requested or stored.

## Prepare a reproducible package and baseline

Use exactly LegacyForge commit `d1453434ceefe73bef5aff497194e09f39dde7e1`, preserve production authentication and entitlement code, and record any separately approved diagnostic-source changes in an independent package/repository. Do not silently use a later main revision. Record APPX SHA256, package identity/version, dependencies, exact packaged JVM/shim/Mesa hashes, console OS/build and Developer Mode state. A source checkout with six Mesa DLLs is insufficient to identify a deployed runtime.

The owner builds/signs the approved package using the repository's existing `build.ps1` and documented prerequisites in a separate build workspace; command flags must be checked against that pinned script before use. This investigation did not build or install it. Do not point a build at the read-only evidence checkout. Source `scripts/validate-modern-version-matrix.ps1` checks staged manifest/artifact/config presence; it is not a gameplay test and was not run against nonexistent staging outputs.

The owner uses their existing Developer Mode deployment route. If Device Portal is later configured, the owner retains credentials and performs sign-in locally. See [Microsoft Xbox tools](https://learn.microsoft.com/en-us/previous-versions/windows/uwp/xbox-apps/introduction-to-xbox-tools) and [Device Portal API family coverage](https://learn.microsoft.com/en-gb/previous-versions/windows/uwp/debug-test-perf/device-portal-api-core). Do not assume desktop dump endpoints exist on Xbox. No network connection is authorized by this procedure alone.

## Gates (all BLOCKED pending owner execution)

| ID | Action / evidence | Pass criterion |
|---|---|---|
| X01 | Owner installs approved exact package; record identity/build/dependencies | Package activates on Series X; actual executable/runtime hashes match receipt |
| X02 | Run outside debugger and measure memory/CPU/GPU during launcher idle/load | Actual package resource budget recorded; no inference from historical generic limits or expandedResources declaration |
| X03 | Synthetic JVM invocation for each current/java21/java17/legacy package | LoadPackagedLibrary/JNI API result, requested/accepted JNI version, Java major and exception result captured; no game/account required |
| X04 | Synthetic filesystem/thread/ZIPFS tests using app-local data | Read/write/rename/ZIP behavior within allowed roots; no broad-file capability assumption |
| X05 | JNI/native load probe against exact packaged/selected modules | Every required module/dependency/symbol resolves through actual package policy; full errors retained without credentials |
| X06 | Graphics probe: context version/profile/extensions, shader compile/link, draw/present | Required backend/capabilities verified; compare actual GL extensions with glfwExtensionSupported behavior; no success from an empty window alone |
| X07 | Controller, keyboard, pointer/focus/disconnect/reconnect | Button/axis/mouse/UI behavior matches explicit expectations; test mapping/hats/Win32-HWND-dependent consumers separately |
| X08 | Audio probe including device loss | Playback/capture policy, device switching, latency/failure result measured; historical desktop OpenAL log is insufficient |
| X09 | Suspend/resume and terminate/relaunch | No stuck keys, invalid context/audio, save loss or unsafe second-JVM reuse; record lifecycle markers and frame/resource changes |
| X10 | Download/repair of approved target with existing account gate respected | Exact manifest/counters/hashes; no bypass to make Local Launcher Mode repair/play succeed |
| X11 | Owner-authorized legitimate owned target launch | Existing entitlement/profile checks pass legitimately; exact version/loader/runtime/native/graphics tuple recorded; gameplay observable |
| X12 | Repeat per catalog row and regression profile | Each of 56 rows independently PASSED/FAILED/BLOCKED/INCONCLUSIVE; unsupported legacy provider remains explicit |
| X13 | Phase 5F.2 UI regression | Installed/Installed-Off persistence, no duplicate install, correct active profile, failed download and account gates retained |

X03–X08 require a separately built synthetic diagnostic package or approved diagnostic mode; no such package exists in the supplied artifacts and none was fabricated as a completed test. X10/X11 must respect existing ownership conditions and need separately authorized owner account use. The owner must not provide credentials, access/refresh tokens, codes, account names or raw authentication logs to Codex.

An independently written [Java source fixture](tests/probes/README.md) now compiles for Java8 and covers a limited thread/app-local filesystem/ZIPFS-read subset. It was never executed and supplies no JNI/native/graphics/input/audio harness or Xbox package. E21 metadata pins the expected `current` runtime major25; check actual package hashes and observed Java major rather than inferring it from a catalog label. All four runtime families remain required.

## Complete matrix and return format

`evidence/target-validation-matrix.csv` contains all 56 approved catalog rows:20 Fabric,18 Forge,17 NeoForge and 1 vanilla; 12 current,40 Java 21,2 Java 17 and 2 legacy runtime assignments. Four rows have source support level testing and 52 experimental; these labels are not passed tests. Every new runtime verdict is BLOCKED until evidence arrives. The two1.12.2 rows explicitly lack their provider in the catalog.

Return only an allowlisted receipt using tests/result.template.json: test/target IDs, package/JVM/native hashes, console OS/build, result/HRESULT, counts, measured timings/resources and a brief sanitized symptom. Keep local raw logs private until reviewed/redacted. Phase 5F.2 testing reported by the user is retained as user-provided UI regression evidence; the pinned PHASE-5F2.md still says validation pending, so there is no checked-in independent runtime receipt to extrapolate from.

## Machine-readable acceptance and receipts

`tests/test-cases.json` enumerates W01–W12 and X01–X13 with required pass fields and current blockers. Its target_plans retain all 56 exact version/loader/runtime tuples, loader-preparation requirements, package/runtime/native/manifest hashes and required X-gate references. The 1.12.2 provider limitation and Java 17/8 JNI question have their own blockers.

Validate an owner-prepared sanitized receipt without executing targets or contacting a device:

```powershell
python -B tools/verify-test-receipts.py tests/test-cases.json tests/result.template.json
```

A valid BLOCKED receipt is still BLOCKED. A PASS receipt requires actual-observation evidence, every criterion, nonempty required fields and hash-bound sanitized attachments. The validator checks structure/reference integrity, not the truth of an operator's claim. There is no deployment, connection, credential collection or automatic execution in this command.

X12 additionally requires one exact approved catalog tuple and validated X01–X11/X13 prerequisite receipts with consistent package, runtime, native, manifest and loader identities. The `1.12.2` Forge `selected` label is unresolved in the approved source and its provider is absent; the validator rejects a claimed runnable PASS for that row. Both legacy rows remain listed. Aggregate coverage of all 56 rows and all four runtime families requires a separate review; validating one receipt cannot establish it. Free text and attachments still require manual privacy review.
