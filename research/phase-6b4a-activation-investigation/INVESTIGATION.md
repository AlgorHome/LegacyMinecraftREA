# Phase 6B.4a — Xbox D00 activation failure investigation

2026-10-17. Read-only target investigation; only local research evidence was written.
No second launch, Portal connection, logging session, package/source modification,
signing, installation, framework/trust change or production execution occurred.

## Preserved incident

Owner reports Xbox Series X OS build **10.26100.9445**, installation/identity
registration PASS, one launch attempted, diagnostic subsequently **Not running**,
Portal error **-2015297530 / 0x87E10006**, message **Failed to launch the application.**
D00 UI not observed; receipt persistence UNKNOWN. The one launch allowance is
consumed. PackageFullName was visible but truncated in the owner's screenshot;
its complete value remains UNKNOWN and is not reconstructed here.

The textual owner evidence is preserved in OWNER-OBSERVATIONS.json. No screenshot
was attached to this request or located among the image attachments inspected;
therefore screenshot preservation/visual verification is BLOCKED, not completed.
Owner should retain the original locally; a later supplied original can be hashed
and copied into the evidence directory without another launch. Do not replace it
with a recreated image or expose Portal credentials in a shared copy.

| Evidence field | Result | Limit |
|---|---|---|
| Package installation/registration | PASS, owner reported | exact identity matched in prior installation observation |
| Activation attempt | FAILED, owner reported | exact Portal code above; no proof executable never started |
| Sustained process | Not running after attempt | a short-lived process remains possible |
| UI rendering | NOT OBSERVED | rendering success not established; initialization stage unknown |
| Native-control execution | UNKNOWN / unverified | no D00 receipt collected |
| Receipt persistence | UNKNOWN | absence of collection is not absence of receipt |
| Overall D00 acceptance | FAILED | successful hardware run not demonstrated |

Expected registered identity remains AlgorHome.LegacyForge.RuntimeDiagnostics,
CN=LegacyForgeDiagnostics, 0.1.1.0, x64, classification App. Classification is
console metadata reported by the owner, not a manifest field proving activation.

## What the error establishes

Exact-code searches of Microsoft Learn and Xbox Support did not locate a public
authoritative definition or a documented symbol for 0x87E10006. Do not assign it a
specific dependency, signing, entitlement or API failure solely from its number.

Separate anecdotal evidence:

- A user-filed issue in the Microsoft-owned AI Dev Gallery repository reports the
  same code and an unsupported-app message on Xbox. This is a bug report, not a
  Microsoft error reference or confirmed root cause:
  https://github.com/microsoft/ai-dev-gallery/issues/354
- A community report describes a packaged Unreal app installing but failing to
  launch with this code:
  https://www.reddit.com/r/unrealengine/comments/1o6ctvx/

These support investigating application-model compatibility; they do not prove
the current cause. No community reinstall, security, classification or policy
workaround was adopted. No authoritative claim of a general UWP prohibition is
made, and historical success of the owner's launcher remains separate evidence.

## Artifact audit and working-launcher comparison

STATIC-COMPARISON.json contains all direct/delay imports, PE fields, package and
executable hashes. Both manifests were read directly from the packages and saved
as diagnostic-manifest.xml and working-launcher-reference-manifest.xml. The helper
static_compare.py reads ZIP/PE bytes only and invokes no target code. It reuses
only the pure parse function from analysis-local/native_audit.py, excluding that
script's broad top-level scans.

Signed diagnostic SHA256 remains
**51e5c74462e79a296335beab4830f479e861e7132e0f660c680f6974d3b27530**;
RuntimeDiagnostics.exe SHA256
**418a77107f02f28dc8df882e4a31ea744d93f9c3d5470aa267ffc03a8eca4231**.
REA package inventory agrees with the root/member identities, reports no integrity
contradictions within its ZIP inventory scope, and did not execute the artifact:
`ev_59e14a0d9d83b03cb8c579bdc9853a4fb2189003099b0a1df566f9bc9982613f`;
nested inventory `ev_37bd361b0c729ebf39da1ea10608e604038782dd87eaa90601635ea5e3079ad1`.
This is not a new CMS or APPX cryptographic-signature check. Preserved prior
findings remain CMS/content integrity PASS and Windows SignTool /pa FAIL,
CERT_E_UNTRUSTEDROOT 0x800B0109. No trust alteration is justified by this incident.

Local working-reference package:
`C:/Users/arinze/LegacyForge/output/LegacyForge_1.0.0.35.appx`, SHA256
**aaeb1c0bccf3a062699e5fd3744b73609748bf5c4246191a4d9bd4bdad6628ab**;
LegacyForge.exe SHA256
**7ae793d5e8a8a7a7e9ac43e57caf45d7c2b1edf9dbfe3850bc1d4da842b0a0c5**.
It is the local Phase 5F.2 reference associated with the owner's hardware-tested
launcher. Console bytes/hash were not obtained; exact installed-byte equivalence
is not independently established. Pinned source comparison used
d1453434ceefe73bef5aff497194e09f39dde7e1, not an assumed current production HEAD.
Diagnostic checkout remains unchanged/clean at its review state.

| Property | Diagnostic | Working launcher reference |
|---|---|---|
| Package identity | separate RuntimeDiagnostics / CN=LegacyForgeDiagnostics / 0.1.1.0 | AlgorHome.LegacyForge / CN=AlgorHome / 1.0.0.35 |
| Application Id | App | App |
| Executable | RuntimeDiagnostics.exe exists, AMD64 | LegacyForge.exe exists, AMD64 |
| EntryPoint | Windows.PartialTrustApplication | MC.App |
| Device family | Windows.Universal | Windows.Universal |
| MinVersion / MaxVersionTested | 10.0.17763.0 / 10.0.26100.0 | 10.0.15063.0 / 10.0.26100.0 |
| VCLibs declaration | Microsoft.VCLibs.140.00, min14.0.0.0, Microsoft publisher | same declaration |
| Manifest capabilities | none | internetClient, internetClientServer, privateNetworkClientServer, runFullTrust, broadFileSystemAccess, expandedResources, microphone |
| PE subsystem | 2, Windows GUI | 2, Windows GUI |
| PE AppContainer bit | set | not set |
| Direct import modules | 31 | 13 |
| Delay imports | none | none |
| CRT route | MSVCP140_APP, VCRUNTIME140_APP, VCRUNTIME140_1_APP and UCRT contracts | no direct CRT DLL imports in launcher EXE |
| Native app startup | init_apartment(single_threaded), CoreApplication::Run | RoInitialize(RO_INIT_MULTITHREADED), coreApp->Run |

Both import d3d11.dll, d2d1.dll, DWrite.dll, bcrypt.dll and WinRT/COM interfaces.
Diagnostic also has file, threading, heap, time, loader and CRT API-set imports;
the complete module/function list is in JSON. Comparing module/function pairs
does not equate differently routed KERNEL32/API-set imports. The diagnostic has
no jvm.dll direct/delay import and no Java/Minecraft payload. Generic
LoadLibraryExW/GetProcAddress imports alone are not evidence of JVM execution;
the D00 compile-time gates remain unchanged.

No known unsupported Xbox import was conclusively identified. UWP header/link
success and /APPCONTAINER do not prove every import resolves on Xbox. The reviewed
local VCLibs fallback provides all 17 direct CRT exports, but its bytes were not
read from the console. Registration confirms accepted package dependency
resolution; it does not validate all native loader exports or transitive imports.
Do not install the fallback to test an unsupported hypothesis. No WACK result or
Xbox native-loader trace is available for this investigation.

## Ranked hypotheses and minimal proposed corrections

1. **Activation-model mismatch — HIGH confidence as a static discrepancy;
   MEDIUM-HIGH as the cause of this incident.** Microsoft documents the lower-case
   windows.partialTrustApplication marker as packagedClassicApp/appContainer,
   distinct from ordinary UWP windowsApp activation. The diagnostic spells the
   marker Windows.PartialTrustApplication; case normalization on Xbox was not
   tested. Either interpretation needs review: recognized marker selects the
   desktop-style model; a literal class interpretation would name a class this
   source does not define. Its actual startup implements DiagnosticSource /
   IFrameworkViewSource and CoreApplication::Run. Working MC.App uses the UWP path.
   Smallest experimental change: replace only the diagnostic Application EntryPoint
   with a diagnostic-specific UWP class identifier, e.g. LegacyForgeDiagnostics.App,
   following the working CoreApplication::Run pattern. Verify startup/class mapping
   statically; do not claim a renamed manifest string alone is a proven repair.
   Keep identity, capabilities, AppContainer isolation and D00 gates unchanged.

2. **STA entry thread before CoreApplication::Run — HIGH confidence discrepancy;
   MEDIUM causal confidence.** src/app.cpp:486-496 initializes single_threaded at
   line488; pinned MC.Xbox/App.cpp:921 onward initializes RO_INIT_MULTITHREADED.
   Microsoft's native application-model documentation says entry startup expects
   an MTA before Run creates the UI thread. Smallest independent correction:
   change that one diagnostic init_apartment argument to multi_threaded. An early
   HRESULT is returned by wWinMain without a D00 receipt, so current observations
   fit but do not prove this path. Do not confuse the runtime-created UI ASTA with
   the initial entry thread.

3. **Native loader/dependency export failure — LOW-MEDIUM confidence.** The
   diagnostic's /MD build adds CRT/API-set imports absent as direct dependencies
   of the working EXE. Framework name/version/x64 registration matches and prior
   local export audit passes, reducing but not eliminating this hypothesis.
   Next discriminator is a pre-existing package-specific activation/loader record.
   No dependency replacement or static-CRT rewrite is justified yet.

4. **Incorrect Portal application selection/identity mapping — LOW confidence.**
   Owner matched registered identity, but full name is truncated and exact
   application relative ID was not preserved. Read-only inventory of this one
   package can close the gap. Smallest correction, only if a mismatch is found,
   is selecting the correct App entry in a future separately authorized test;
   no rename, uninstall or classification change.

5. **Renderer initialization or later native-control failure — LOW confidence as
   explanation for this Portal code.** Both use hardware D3D11; diagnostic
   DiagnosticView::Run catches renderer failure and starts the receipt worker
   with renderReady=false. It can emit DIAGNOSTIC_UI_UNAVAILABLE. A pre-Run failure,
   sudden process crash or storage error can still leave no final receipt. Inspect
   only existing diagnostic evidence before proposing graphics changes. Do not
   weaken hardware D3D11 or add WARP merely to obtain a PASS.

6. **Certificate, capability, OS-family or classification problem — LOW confidence.**
   Installation/identity PASS, matching VCLibs declaration, x64 Universal targeting,
   console App classification and a sufficiently recent build provide contrary
   evidence. Windows host trust failure is not proof of Xbox launch distrust.
   No broad capability copying, production certificate reuse, App-to-Game switch,
   lowered isolation or OS/security change is warranted.

Authoritative model sources:

- [Application schema](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-f-application),
  combinations of activation attributes: separates packagedClassicApp and windowsApp.
- [CoreApplication documentation](https://learn.microsoft.com/en-us/uwp/api/windows.applicationmodel.core.coreapplication):
  native view-provider startup and UWP-only API scope.
- [Microsoft native application-model article](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/august/windows-with-c-the-windows-runtime-application-model):
  MTA startup and runtime-created UI thread. This is historical Microsoft guidance,
  not a decoding of the present Xbox error.

## Existing evidence/log gate

No approved authenticated console session or package-scoped activation log file
is available to Codex in this turn. No ETW tracing or broad log export was started.
Activation-log inspection is therefore BLOCKED by unavailable evidence, not PASS.
If the existing owner Portal already exposes the failed request details or an
existing app-specific crash/activation record, preserve only this diagnostic's
record around the single attempt: timestamp, package/application identifier,
HRESULT, module name and exception/loader text. Do not enable tracing, attach a
debugger, reproduce the failure, collect account fields or export console-wide logs.
Do not assume desktop AppModel event channels are exposed on this Xbox build.

The existing read-only installed-package inventory can resolve PackageFullName:
[Microsoft inventory API](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/device-portal-api-core#get-installed-apps).
Use the current authenticated origin and only the matched record. No credential,
trust or Remote Access changes; no Codex console access. Existing receipts, if
separately approved for collection, must come only from that exact diagnostic
LocalState/Phase6B1Receipts. Missing access is not permission for a wider collection.

## Next separately approved experiment

Prefer obtaining the untruncated identifier, original screenshot and already
existing package-specific failure details first, without launching again.
If they do not contradict the leading hypothesis, propose a **diagnostic-only
manifest activation-model correction** as the smallest first controlled variant.
Preserve this failed artifact and all receipts. Repackaging requires updated input
hash evidence and a reviewable new version; any signing, installation and one
subsequent launch require their own explicit authorizations.

Keep the STA-to-MTA startup correction as an independently tracked follow-up,
rather than silently bundling both hypotheses and claiming which fixed it.
An owner-approved combined correctness patch could fix both, but would sacrifice
single-variable causal attribution and must say so. No source patch, rebuild,
repackaging or second execution was performed here. STOP for further approval.
