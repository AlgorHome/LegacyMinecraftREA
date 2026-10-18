# Owner-operated Xbox Series X D00 runbook

**PREPARATION ONLY. Nothing here authorizes console access, signing, deployment
or launch. Stop at each separate approval gate. Do not execute the archived launcher.**

## 1. Before console access

Review XBOX-READINESS.md and SIGNING-AND-DEPENDENCIES.md. Resolve the diagnostic
signer, framework provenance and signed-artifact gates first. Keep the pinned
unsigned APPX unchanged. Record its signed successor's new SHA256 and unchanged
payload comparison; no production signing identity, Java, Minecraft or proprietary
launcher content may enter the diagnostic package.

Owner must separately approve inspecting/using their particular Series X in Dev
Mode. Then record console OS/build, Dev Home status, available development storage,
and this diagnostic's app/game classification. Do not change the global app/game
default or production LegacyForge classification. Existing hardware/Dev Mode reports
are history, not a fresh compatibility test.

## 2. Owner opens Device Portal — separate access approval

Use the HTTPS endpoint actually displayed in the owner's Dev Home Remote Access
settings; do not guess an address, scan the LAN or paste credentials into chat.
Owner configures/authenticates locally. Verify endpoint/transport identity directly
against the owner's console before accepting any expected development certificate.
No blanket TLS-validation disablement, credential-bearing URL, automation token,
HAR capture or HTTP traffic monitoring is needed.

Use a private owner-controlled LAN between PC and console. Internet access is not
needed by D00 itself; management LAN access is needed by Device Portal. If the
owner requires no Internet during testing, provide LAN without WAN after normal
Dev Mode setup; do not confuse it with a fully disconnected console. Do not change
network/account/entitlement policy on behalf of this plan. If platform setup needs
unavailable connectivity, stop and record the prerequisite.

Microsoft's [Xbox Portal documentation](https://learn.microsoft.com/en-us/windows/uwp/xbox-apps/device-portal-xbox)
describes owner-local Dev Home access and individual app actions. Its older Xbox
documentation is a procedure reference; actual Series X UI/build behavior remains
unverified. Missing controls are a blocker, not permission to install another app.

## 3. Inventory and baseline — no launch

In Portal's app/package manager, inspect only the diagnostic identity and required
framework. Record exact Name, Publisher, Version, architecture, package full name,
package family name and classification. Keep user/account/SID data private.

- Expected diagnostic Name: AlgorHome.LegacyForge.RuntimeDiagnostics.
- Publisher: CN=LegacyForgeDiagnostics; Version0.1.1.0; x64; application Id App.
- Framework: Microsoft.VCLibs.140.00, Microsoft publisher, suitable x64 UWP version.
- Record prior diagnostic registration and receipt filenames/sizes/times if present;
  do not delete them. A new process/run ID and before/after listing distinguish a
  new test from stale receipts. If identity/version collides, stop for review rather
  than uninstalling or overwriting an existing package automatically.

The desktop host's framework is not proof of the console's installed dependency.
Do not re-sign Microsoft's framework or copy loose runtime DLLs into the APPX.

## 4. Install the separate diagnostic — deployment approval required

Approve the exact signed APPX hash, signer result and framework hash/installed
identity before proceeding. In the owner Portal's Home/Apps manager install flow:

1. Choose the **signed** RuntimeDiagnostics APPX as the app package.
2. Add only the verified Microsoft x64 UWP VCLibs dependency, if required and not
   already supplied by the console. Do not upload desktop redistributable EXEs,
   Java, PFX/key material, Minecraft, installer archives or unrelated packages.
3. Leave any automatic launch-after-install option **off**. If the UI cannot
   separate installation from launch, stop until the owner approves a route that can.
4. Submit install and wait for its final completion/error. Upload acceptance is not
   proof of successful registration. Preserve sanitized deployment result/HRESULT.
5. Re-read the diagnostic's exact registered identity and dependency. Record
   registration PASS only when installation completed and identity matches.

No separate signing-certificate upload/import is prescribed for Xbox: the
[core install contract](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#install-an-app)
distinguishes it from Desktop/IoT. Unexpected certificate/trust errors are BLOCKED
for review; do not bypass them. Portal HTTPS certificate and APPX signer differ.

This script-built project has no ready Visual Studio deployment solution. Do not
assume the desktop Add-AppxPackage command runs on Xbox. The planned supported
route is the owner-operated Portal package/dependency flow; no REST POST has been
issued by Codex. Registration approval alone does not authorize activation.

## 5. Activate once — explicit D00 run approval required

Owner selects only the exact diagnostic entry in Dev Home or its Portal app
actions, then Launch. Do not launch production LegacyForge. D00 starts
automatically; no keyboard/controller Java action exists in this build.

Start an external30-second observation timer. Record visible D00 ONLY title,
D00 status, any sanitized numeric activation error, and whether a process/window
was observed. UI drawing is not formal D06 graphics certification. Do not infer
durable persistence from a status screenshot alone.

D00 has no automatic30-second kill watchdog; S21's watchdog is compiled out.
If the app hangs, record the observation deadline as INCONCLUSIVE and owner-close
only this diagnostic via its own app action/console Quit. No broad process kill,
console reset or app-data cleanup. Preserve existing receipt/checkpoint evidence.

## 6. Retrieve only diagnostic LocalState — retrieval approval required

Use Portal File Explorer's **LocalAppData** location and the installed diagnostic's
exact package entry, then **LocalState/Phase6B1Receipts**. Use actual registration
metadata; do not guess the publisher suffix or browse another app's storage. Record
before/after directory listings. Download only new D00-*.json and corresponding
*.tmp evidence if present; original receipt writes are bounded to128 KiB each.
Do not upload, rename, delete, modify ACLs or install a third-party file manager.

Microsoft's [App File Explorer API](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#app-file-explorer)
documents Xbox support. For an owner-approved read-only fallback, these are request
shapes only, not issued commands; URL-encode values and use exact returned paths:

```text
GET /api/filesystem/apps/knownfolders
GET /api/filesystem/apps/files?knownfolderid=LocalAppData&packagefullname=<EXACT-DIAGNOSTIC-PACKAGE-FULL-NAME>
GET /api/filesystem/apps/files?knownfolderid=LocalAppData&packagefullname=<EXACT-DIAGNOSTIC-PACKAGE-FULL-NAME>&path=<RETURNED-LOCALSTATE-RECEIPT-SUBPATH>
GET /api/filesystem/apps/file?knownfolderid=LocalAppData&packagefullname=<EXACT-DIAGNOSTIC-PACKAGE-FULL-NAME>&path=<RETURNED-RECEIPT-DIRECTORY>&filename=<NEW-D00-JSON-FILENAME>
```

Package **full name**, family name and identity Name are different. The API requires
packagefullname for LocalAppData. Authentication stays in the owner's local browser/
approved client; never put credentials in URLs, logs or scripts. If LocalState is
unavailable or download fails, record retrieval BLOCKED and retain the app/data.
Do not substitute screenshot-only evidence for durable-receipt acceptance.

On the PC, store downloads in a new per-run evidence directory. Preserve originals
read-only, hash them with Get-FileHash -Algorithm SHA256, and make separately marked
sanitized copies if needed. Receipt contents are JSON data, not executable input.
Check schema legacyforge-phase6b1-runtime-receipt-v1, D00 case, a new run/process ID,
version/source baseline, expected identity and approved payload hashes. Compare both
top-level identities and terminal details.role_hashes when that stage was reached
against phase6b1a's D00-BUILD-EVIDENCE.json artifactAudit.payload entries. Do not accept
mere self-consistency or a stale receipt from an earlier run.

Full D00 acceptance requires terminal=true, status PASS, reason
D00_ACTIVATED_HASHES_RECORDED, expected identity=true, complete matching required
role hashes, and no persistence error. Required roles: RuntimeDiagnostics.exe,
AppxManifest.xml, diagnostic-inputs.json, runtime-inventory.json and
profiles/native-control.json. Retain any missing-metric numeric error/availability
flags without inventing zero values. No S21 receipt is expected.

## 7. Preserve graphics-failure evidence separately

Current src/app.cpp:96-136 attempts receipt creation before checking renderReady.
If initialization/rendering failed it can write terminal FAILED with
DIAGNOSTIC_UI_UNAVAILABLE instead of running native_control.cpp. Retrieve that file
through the same path even if no useful UI appeared. Its fresh binding/checkpoint
can establish activation and durable writing; it cannot establish full D00 PASS
or native-control role/resource-test completion. If the failure occurred before
receipt creation, preserve the portal error/time/process observation and report
persistence UNKNOWN/INCONCLUSIVE, not FAILED merely because no download exists.

Use EVIDENCE-FIELDS.json to keep registration, activation, D00 rendering, durable
receipt writing, retrieval and overall acceptance separate. In a graphics failure,
registration may PASS and persistence may PASS while rendering fails and overall
D00 remains FAILED/DIAGNOSTIC_UI_UNAVAILABLE. Formal graphics/input/audio/JNI tests
remain NOT EXECUTED. No headless fallback or weaker graphics criterion is introduced.

## 8. Evidence retention and eventual cleanup

Preserve receipt/hash, sanitized screenshot, exact signed/unsigned/dependency hashes,
source/review commits, owner-recorded OS/classification, registration result and
activation/render observations. Keep raw account/device data and screenshots local
until redacted; no memory dump or broad console collection is required.

Do not uninstall/reinstall, leave Dev Mode with an option that removes apps, clear
LocalState or reset the console before retrieval. There is no VM-style checkpoint
rollback on the real console in this plan. After evidence is preserved, a separate
owner cleanup approval may remove only the exact diagnostic identity. Never remove
the shared Microsoft framework, production LegacyForge, its signing identity/data
or other apps. Leave existing app/game/network defaults unchanged.
