# D00-only controlled validation preparation

Status: PREPARATION ONLY / EXECUTION BLOCKED. Nothing below has been run.
This procedure requires a subsequent explicit approval for the named artifact,
isolated guest and actions. It does not authorize Xbox access or any JNI test.

## Gates before execution

1. Resolve SAFETY-REVIEW.md requirement 8. Preferred: separately approve a
   diagnostic-only change that disables all S21 input handlers/worker entry in a
   D00-only build, then review its source and new artifact hash. The present
   f77bd4c package has a runtime-absence barrier, not that compiled lock. Do not
   treat instructions to avoid a button as equivalent to a hard disable.
2. Name a disposable Windows 11 x64 VM, its OS build and snapshot; use a disposable
   local account with no personal files/credentials or Minecraft/LegacyForge data.
   No shared host drives, clipboard, device/USB redirection or host profile mounts.
   Transfer only reviewed artifacts via a temporary read-only transfer medium,
   detach it, and disconnect guest networking before activation. Do not use the
   host as the test environment. An unconfigured VM or generic Sandbox is BLOCKED.
3. Confirm UWP registration and a suitable virtual graphics device work in this
   guest. The UI requests hardware D3D11; do not silently enable host GPU sharing
   or weaken isolation to fix a failure. Approve that environment change separately
   or record DIAGNOSTIC_UI_UNAVAILABLE/activation failure. Snapshot first.
4. Verify exact reviewed source/package, default runtime inventory false/false,
   no runtime payload, no new capabilities and correct diagnostic identity.
   For the existing unsigned artifact the SHA256 is
   `930f6844eea2777433886d1d347b6925206d2cfd51fccf4a36b1206ab8cf9f08`.
   A rebuilt or signed artifact has a new hash; record it, signer and verify unchanged
   payload hashes. Never substitute a runtime-bearing package.

## Minimum signing and Windows deployment inputs

- Owner-selected local signing certificate/key accessible through an owner-controlled
  certificate store or secure signing service. Subject must match manifest publisher
  `CN=LegacyForgeDiagnostics`; code-signing use, validity and chain must be suitable.
  Retain the private key and any password locally. Do not send certificates, PFX,
  keys or passwords through chat. Public subject/thumbprint and verification results
  are sufficient review metadata. Do not reuse production identity or key implicitly.
- Approved unsigned APPX, Windows SDK SignTool, SHA256 signing matching block-map
  algorithm, optional approved timestamp policy, and guest trust in the signing chain.
  Owner performs trust/signing only after approval. Verify signature and record the
  resulting signed hash. Publisher changes require a rebuild and renewed review.
- Trusted Microsoft-signed **x64 UWP** Microsoft.VCLibs.140.00 framework satisfying
  the manifest; record version/hash/signature. Desktop VC redistributable EXEs do
  not satisfy this APPX dependency. Missing framework or signer/trust inputs: BLOCKED.

Microsoft documents publisher matching and signing in [package signing](https://learn.microsoft.com/en-us/windows/uwp/packaging/create-certificate-package-signing)
and [SignTool](https://learn.microsoft.com/en-us/windows/win32/appxpkg/how-to-sign-a-package-using-signtool).

After explicit approval, inside the guest only: enable the applicable development/
sideload policy, establish approved signer trust, install/register the signed APPX
and its framework with Windows package deployment, and inspect the resulting
identity/version/publisher. [Add-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/add-appxpackage)
supports the signed package and DependencyPath inputs. Do not use all-user
provisioning, replace production packages, or launch RuntimeDiagnostics.exe directly.
No installation command has been executed by this review.

## Future Windows D00 run: exact sequence

1. Preserve pre-run package list, guest OS/graphics configuration, approved source,
   unsigned/signed hashes, signer verification and dependency versions. Record only
   sanitized identifiers. Confirm the diagnostic LocalState is initially clean;
   use a fresh guest rather than delete another application's data.
2. With the package registered and network detached, resolve the actual diagnostic
   package family name. Activate its `<diagnostic-package-family-name>!App` using
   Windows Start/application activation. Do not select production LegacyForge.
   Do not press Enter/controller A or click the Java button in the current package.
   Those procedural restrictions do not waive the hard-disable gate above.
3. Observe for up to 30 seconds using an external timer. D00 starts automatically
   after UI initialization. Capture the status display. No S21 action is authorized.
4. Read only this guest's
   `%LOCALAPPDATA%/Packages/<diagnostic-PFN>/LocalState/Phase6B1Receipts/D00-*.json`.
   Expect schema `legacyforge-phase6b1-runtime-receipt-v1`, case D00, terminal true,
   status PASS, reason D00_ACTIVATED_HASHES_RECORDED, expected identity true,
   complete role hashes and resource observations. Verify hashes against approved
   payload; check no S21 receipt exists. Missing metrics can have numeric HRESULTs
   and availability false; do not invent values. Resource availability is separate
   from activation success.
5. FAILED/BLOCKED/RECEIPT_ERROR, missing/partial receipt or a hang is not PASS.
   At the manual observation deadline record INCONCLUSIVE for the run; do not
   overwrite the app's receipt. Preserve existing JSON/tmp files and sanitized OS
   activation error/event codes. Close only the identified diagnostic window through
   the OS; if unresponsive, preserve evidence then discard/revert the disposable VM.
   No taskkill by image name, wildcard process stop, or production data cleanup.
6. Owner-controlled export: screenshot and diagnostic receipt copies only, scan for
   paths/account/device identifiers before sharing; hash the exported files. Close
   the application and preserve evidence before reverting the snapshot. Report
   D00 only; no inference about JNI, dependency closure, graphics certification,
   gameplay or Xbox hardware success.

## Xbox Series X deployment requirements — deferred

Required later: owner-controlled Series X in Developer Mode/Dev Home; recorded OS
version and app/game resource classification; reviewed signed x64 diagnostic APPX,
trusted matching UWP VCLibs and accepted signing policy. No Minecraft ownership,
Minecraft installation, Xbox Live integration or gameplay is needed for D00.
Dev Mode/platform setup itself is owner responsibility; no credentials are needed
by the diagnostic.

Choose and separately authorize an owner-operated deployment route: supported
Visual Studio remote deployment (requires appropriate project/deployment setup;
this build is a script-built APPX, not a ready VS solution), or Xbox Device Portal
package upload with its dependency package(s). Microsoft describes [UWP deployment](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/deploying-and-debugging-uwp-apps)
and [Xbox Device Portal](https://learn.microsoft.com/en-us/previous-versions/windows/uwp/xbox-apps/device-portal-xbox).
The latter is older Xbox-family documentation; verify actual Series X Dev Home
options and trust behavior with the owner before deployment. Do not assume Windows
PowerShell registration commands run on the console. Portal credentials stay with
the owner. No Portal access is authorized by this document.

After separate deployment/run approval: owner installs only diagnostic identity
and framework, launches once, supplies no Java input, captures D00 display/receipt
via an approved retrieval route, and closes only that app. If receipt retrieval is
unavailable, screenshot-only evidence is insufficient for durable-receipt acceptance.
Windows PASS is not Xbox PASS. Console installation, activation and evidence
collection all remain BLOCKED/NOT EXECUTED.

Open blockers: explicit run approval; hard Java-disabled package; confirmed isolated
guest and graphics; local signing/trust inputs; trusted framework; separately approved
Xbox deployment route and receipt retrieval. No proprietary binaries are required.
