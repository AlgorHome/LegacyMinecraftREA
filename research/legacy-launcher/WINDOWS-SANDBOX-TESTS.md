# Reproducible isolated Windows test procedure

Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.

**Status: BLOCKED.** User confirmed no configured isolated Windows VM/Sandbox and explicitly prohibited archived-launcher execution until an isolated environment is available and approved. No Windows features were enabled, VM created or software installed. Read-only Hyper-V enumeration returned insufficient permission; Windows Sandbox was not found at the checked standard path. Existing installed7-Zip19 could only identify an incomplete ZIP fragment, so it was not treated as a valid Inno inventory. The independent decoder completed static inventory without installation.

## Environment the owner must prepare

Use a disposable Windows 11 VM or supported Windows Sandbox edition, a fresh local user and no personal credentials. Obtain separate approval before creating/installing/enabling infrastructure or executing the archived launcher. Keep the original installer hash fixed. Start from an offline VM checkpoint, with no shared clipboard, host home-directory mount, host credential store, printers, audio/video redirection or personal data. Map only a dedicated research-artifact folder read-only and copy working files into the guest's disposable disk. Keep all target writes in the guest.

The included `tests/offline.wsb.example` is a reviewable template only: it has no automatic launcher command and has not been activated. Windows Sandbox configuration and edition requirements are documented by [Microsoft](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/); [WSB controls](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) govern networking/redirection/mappings. Do not treat a GPU-disabled synthetic renderer as a performance test.

## Test matrix (every row currently BLOCKED)

| ID | Controlled action after approval | Expected evidence / pass criterion |
|---|---|---|
| W01 | Verify guest isolation and hashes before launching | Guest OS/build/account class; no personal stores/mappings; exact installer SHA256; network-disabled state |
| W02 | Snapshot guest, run installer offline into guest-only location | Installation receipt/exit, guest-only file inventory/hashes, uninstall/shortcut/config changes; compare770 payload identities; do not execute uninstaller implicitly |
| W03 | Launch archived launcher offline | Actual wrapper→bootstrap→launcher process tree and JVM command identities; no successful network calls; missing-cache errors/cancellation visible |
| W04 | Start from empty guest game cache; approve narrowly scoped public network downloads | Recorded catalog→version JSON→client/library/native/asset/runtime requests, status/size/hash and destination; no Microsoft sign-in |
| W05 | Compare warm-cache versus empty-cache preparation | Existing valid content reused, missing/corrupt synthetic copies re-fetched; complete receipts; only guest test files may be altered |
| W06 | Interrupt transfer and resume using guest snapshot/test copies | Bounded retries, partial-range behavior, final hash checking, no success for truncated output |
| W07 | Simulate full/readonly guest test volume and cancellation | Explicit error and recoverable state; no false install completion; preserve snapshot for comparison |
| W08 | Exercise configuration/profile migration with synthetic empty accounts only | Settings precedence, temporary-file and replace behavior, malformed JSON/error backup, restart persistence; no real token values |
| W09 | Hash-pinned E20 signed metadata plus corrupted/truncated copies; run only in approved guest | Check matching embedded-key fixture origin/hash; actual signed-path acceptance and corrupted/truncated rejection receipts; never substitute an analyst key or change the target trust anchor |
| W10 | Test each loader path identified from exact metadata | Parent/duplicate resolution, native/classpath/options and processor behavior; pin every artifact; no blanket Forge/Fabric parity result |
| W11 | Game process/exit/error controls after explicit game-execution approval | Correct JVM major, args/native identities, exit handling and UI restore; game/account requirements respected |
| W12 | Owner-controlled account tests, separately authorized | Microsoft/XBL/XSTS/Minecraft/ownership/profile outcomes only; no account names, tokens, device codes or raw auth traffic retained |

For W04 onward, change only the guest test environment and record the approval and resulting network mode. Never enable networking by editing the offline template silently. Use a fresh snapshot for update/authentication experiments. Negative tests must not delete or corrupt host files. Restore the disposable guest snapshot only with owner approval; this report performs no destructive action.

## Receipt discipline

Use `tests/result.template.json`. Record test ID, exact artifact/package hashes, environment build, action, expected/observed result, exit/HRESULT, failure classification and sanitized counters. PASS requires an actual observation satisfying the stated criterion. UNTESTED/BLOCKED is not PASS; an inconclusive run records INCONCLUSIVE. Do not save raw command lines containing account arguments or browser/auth captures. Desktop success does not establish Xbox compatibility.

## Machine-readable acceptance and receipts

`tests/test-cases.json` enumerates W01–W12 and X01–X13 with required pass fields and current blockers. Its target_plans retain all 56 exact version/loader/runtime tuples, loader-preparation requirements, package/runtime/native/manifest hashes and required X-gate references. The 1.12.2 provider limitation and Java 17/8 JNI question have their own blockers.

Validate an owner-prepared sanitized receipt without executing targets or contacting a device:

```powershell
python -B tools/verify-test-receipts.py tests/test-cases.json tests/result.template.json
```

A valid BLOCKED receipt is still BLOCKED. A PASS receipt requires actual-observation evidence, every criterion, nonempty required fields and hash-bound sanitized attachments. The validator checks structure/reference integrity, not the truth of an operator's claim. There is no deployment, connection, credential collection or automatic execution in this command.

Nested primary sections reject unknown field names. Free text, nested values and attachment contents still require manual privacy review before publication. Windows W10/W11 record the actual selected desktop native inventory and graphics provider, which need not be the Xbox Mesa/GLFW adaptation. All account gates remain in scope and blocked pending separate owner action.

For W09, [E20](SIGNED-UPDATE-FIXTURE.md) now supplies a public response independently verified against the identical archived/installed embedded key. Original bytes/key remain local, with response SHA256 `9081bab55e8c8ba72ff3c63a1c2cbb85ba523bd2ef357b94e272ba913cf5c52c`. The fixture-availability blocker is closed. The public key alone cannot create a valid signature; a separately generated analyst-key fixture cannot pass the target-key test. E20's independent bit-flip rejection does not run the actual verifier. Actual acceptance, corrupted/truncated rejection, update application and recovery remain BLOCKED pending the approved guest. The matching embedded trust anchor does not independently authenticate the installer publisher or historical update chain.
