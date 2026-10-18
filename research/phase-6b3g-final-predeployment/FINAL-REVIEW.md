# Phase 6B.3g — final Xbox D00 predeployment review

2026-10-17, America/Chicago. **Documentation/read-only review complete. No package
installation or activation authorized or performed.**

## Owner-observed console inventory

| Field | Observed value | Evidence limit |
|---|---|---|
| OS build | 10.26100.9445 | Owner-supplied string, retained verbatim |
| Dev Home | Working | Owner observation |
| Default classification | App | Not a post-install diagnostic observation |
| Installed package Name | Microsoft.VCLibs.140.00 | Exact standard-UWP name, not UWPDesktop |
| Version | 14.0.33519.0 | Owner inventory |
| Architecture | x64 | Owner inventory |
| Publisher | **NOT DISPLAYED** | Unknown; not copied from the local fallback manifest |
| Framework flag | **UNKNOWN** | Not inferred from package name/version |
| PackageFullName | **UNKNOWN** | Not constructed or guessed |
| Console changes | None reported | No Codex console connection |

The matching package is observed present; its publisher/framework properties and
complete dependency suitability are not fully verified. The local fallback's
identity and hash do not prove the installed console package has identical bytes.

## Read-only metadata options

Owner can open the existing Portal Home/My games & apps or package-manager entry's
read-only details and record PackageFullName, Publisher and any explicit Framework/
IsFramework field. Do not use Launch, Install, Update, Uninstall or configuration
actions. Exact fields exposed depend on the console build; this review cannot
promise a Framework widget exists. No Portal access was performed here.

If the visible details omit metadata, the documented owner-operated read-only
inventory request is `GET /api/app/packagemanager/packages` on the already trusted,
authenticated Portal origin. Its response includes PackageFullName and Publisher,
so it may resolve those two gaps. The published schema does **not** promise an
IsFramework field; keep that field UNKNOWN unless actually returned/displayed.
Inspect only the matching record, not account data. Do not paste credentials,
copy-as-curl commands, cookies, user SIDs or whole network captures into chat.

Sources: [Xbox Portal details](https://learn.microsoft.com/en-us/windows/uwp/xbox-apps/device-portal-xbox),
[installed-package response schema](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#get-installed-apps).
An API/UI omission is not confirmed absence or permission to replace the package.

## Immutable local evidence

- Signed diagnostic SHA256 rechecked:
  `51e5c74462e79a296335beab4830f479e861e7132e0f660c680f6974d3b27530`.
- Signed artifact:
  `C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b3d-signing/20261017-132111-5ff08807/RuntimeDiagnostics.D00.signed.appx`.
- CMS signature and Windows APPX signed-content digest verification: **PASS** from
  Phase6B.3e. Windows default SignTool /pa trust: **FAIL**, exit1,
  `CERT_E_UNTRUSTEDROOT / 0x800B0109`. These remain separate results.
- Signer subject/thumbprint: CN=LegacyForgeDiagnostics /
  D6245FB640D520EDED8F8A987B364BCADE01D01D. No key access or trust change here.
- Source4101f7ee07d1c74911ffbf5cd2a44aff608c401d / review/current HEAD
  df23adb6dbe948079510cf12eb64d5fd23542256; clean checkout.
- Independent diagnostic identity: AlgorHome.LegacyForge.RuntimeDiagnostics,
  publisher CN=LegacyForgeDiagnostics, version0.1.1.0, x64, application Id App;
  no capabilities. D00-only configuration and original payload remain unchanged.
- Verified standard-UWP fallback, preserved without installation/re-signing:
  `C:/Users/arinze/Desktop/DesktopAppInstaller_Dependencies/x64/Microsoft.VCLibs.140.00_14.0.33519.0_x64.appx`.
  SHA256 `9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283`.

## Stage A — future owner-controlled INSTALLATION ONLY

**Requires a new installation approval naming the signed hash and existing-framework
route. No activation or fallback installation is included.**

Before approval, preferably resolve Publisher/PackageFullName through the read-only
options above. Framework flag remains unknown if omitted. If those metadata gaps
cannot be resolved, the owner must explicitly acknowledge them in any controlled
installation-only approval; they must not silently become PASS. Console dependency
resolution can then be observed as part of that separately approved installation.

Future owner steps, after that explicit approval:

1. Rehash the exact signed APPX and confirm the value above. Use existing Portal
   connection/authentication; no Remote Access, trust or security configuration changes.
2. Record a baseline inventory for the diagnostic identity. If already installed or
   a same-identity collision exists, stop for review; do not overwrite/update/uninstall.
3. In the existing owner Portal package-install UI, select **only** the signed D00
   diagnostic APPX. **Leave dependency uploads empty** and use the existing console
   framework first. Do not select the fallback file or any certificate/PFX/runtime.
4. Disable/leave off automatic launch. If the available flow cannot separate install
   from launch, stop; installation approval does not permit auto-activation.
5. Submit once and wait for the final deployment result. An upload/HTTP200 acceptance
   is not completed registration. Preserve the sanitized result code and time.
6. On success, inspect the registered diagnostic's exact Name, Publisher, Version,
   architecture and package full name. Compare with the expected identity above.
   Record actual classification without changing the default or package setting.
7. **Stop after registration evidence. Do not Launch.** Registration success establishes
   that the console accepted/resolved the package under its policy; it does not prove
   D00 runtime, graphics or receipt success, or expose a previously hidden Framework flag.

No fallback dependency installation is justified merely by missing UI properties.
If resolution fails, collect the exact error and stop. Adding the fallback requires
its own need assessment, exact-hash approval and applicable redistribution conditions.
The primary existing-framework route distributes no replacement Microsoft framework.

## Independent later approvals

| Stage | Scope of a future approval | Current result |
|---|---|---|
| Installation/registration | Exact signed APPX only, existing framework first, no auto-launch | NOT EXECUTED |
| Activation | One exact diagnostic launch; initial graphics and overall D00 observed independently | NOT EXECUTED |
| Receipt retrieval | Download only the diagnostic's LocalState/Phase6B1Receipts using its actual PackageFullName; preserve originals/hash | NOT EXECUTED |
| Cleanup | After evidence preservation, remove only diagnostic identity if owner approves; no shared-framework removal | NOT EXECUTED |

The prior [owner runbook](../phase-6b3-xbox-readiness/OWNER-DEPLOYMENT-RUNBOOK.md)
describes receipt retrieval and graphics-failure evidence. A valid failure receipt
can establish activation/writing while rendering and overall D00 fail. Registration,
activation, rendering, durable writing, retrieval and overall acceptance stay separate.
Cleanup is not implicitly approved by installation, activation or evidence collection.

## Mandatory stop conditions

| Condition | Owner response |
|---|---|
| Hash/identity mismatch before upload | Do not submit; preserve evidence and stop |
| Certificate/signature rejection | Record exact code/message and build; no trust import, certificate replacement, re-signing or publisher edits |
| Dependency resolution failure | Record required Name/Publisher/minimum version and exact error; no automatic fallback install/update/removal |
| Registration failure/pending timeout/ambiguous result | Preserve result; no repeated install, uninstall/reinstall or security changes |
| Unexpected registered Name, Publisher, Version, architecture or identity collision | Do not launch; preserve inventory and stop; cleanup needs separate approval |
| Install flow forces activation or extra package/security changes | Stop before submitting |

## Final blockers

Publisher, PackageFullName and Framework metadata are not fully observed. Resolve
what existing read-only details expose, or explicitly retain those uncertainties
in a separately approved installation-only test. No such write approval exists now.
Xbox certificate acceptance and dependency resolution are untested outcomes of that
future stage, not reasons to change host trust in advance. The PC's /pa trust failure
is preserved; it does not by itself prove Xbox rejection or package corruption.

No package, signing key, trust store, console setting or production code was changed.
Only these new local review documents/evidence were written. **Stop before deployment.**
