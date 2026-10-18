# Phase 6B.4d — version-separated activation triage

2026-10-17. Read-only source/artifact analysis and preparation only. No code or
package change, signing, console access, launch, update, trust/dependency change,
debugger or tracing session occurred. Only local research documents were written.

## Chronology gate

Keep the prior 0.1.1.0 failed activation (0x87E10006, Not running, no observed UI,
receipt UNKNOWN) separate from the owner-confirmed 0.1.2.0 update/registration PASS.
The final owner clarification attributes the brief appearance/apparent crash to
0.1.2.0 and says 0.1.1.0 did not run at all. Preserve that latter statement as no
visible run, not proof that no short-lived process existed. The structured update
result says no deliberate launch; the triggering action and exact attempt count
remain unknown. Do not conclude auto-launch was enabled or a manual launch occurred.

Owner initially replied **Both 3 and 2**. A targeted follow-up produced:
**version 0.1.1.0  didn't run ant all. But version 0.1.2.0 ran for a split second then crached.**
Version attribution is therefore resolved by owner testimony; onset/trigger and
exception remain unverified. OBSERVATIONS.json preserves both replies separately
without replacing the original 0.1.1.0 incident. No new execution was requested or
performed to obtain this clarification. Screenshot/full package name/logs remain
unavailable. Brief appearance is not confirmed D00 UI rendering or native control.

| Observation | 0.1.1.0 | 0.1.2.0 |
|---|---|---|
| Registration | PASS, owner | PASS, owner |
| Activation outcome | failed/no visible run, 0x87E10006 | failed/apparent brief startup then crash, 0x8027025B, owner |
| Rendered D00 UI | not observed | unconfirmed; splash/brief surface is insufficient |
| Native control / durable receipt | UNKNOWN | UNKNOWN |
| Manual versus automatic trigger | prior one-attempt incident retained | UNKNOWN; structured result reports no deliberate launch |

## Error codes: evidence and limits

**0x8027025B / -2144927141:** Microsoft defines
E_APPLICATION_ACTIVATION_EXEC_FAILURE, meaning the app did not start. This was
also verified in the installed SDK10.0.26100.0 shared/winerror.h:62203-62209.
It is a generic activation failure, not proof of an apartment mismatch or crash
stage. Do not confuse it with 0x8027025A (activation timeout) or 0x8027025C
(temporary license error). No entitlement change follows from this code.

[Authoritative Microsoft error reference](https://learn.microsoft.com/en-us/windows/win32/com/com-error-codes-4).

**0x87E10006 / -2015297530:** retain the exact original Portal message. The prior
investigation found no public authoritative definition. Community unsupported-app
reports are context, not a definitive cause; see ../phase-6b4a-activation-investigation/INVESTIGATION.md.
Although the owner now attributes the observations to different versions, that alone does
not prove the manifest experiment improved activation or reached native code.

## Startup sequence audit

Current diagnostic commit c70a17ecd4022452a963697196f362c8f286ed57, clean checkout:

1. src/app.cpp:486-496 wWinMain initializes single_threaded, constructs
   DiagnosticSource and calls CoreApplication::Run. HRESULT exceptions become
   process return codes; catch-all returns E_FAIL. Neither path writes an early
   activation receipt or a separate startup log.
2. DiagnosticSource::CreateView supplies DiagnosticView. Initialize subscribes
   activation; the callback calls window_.Activate(). SetWindow attaches window
   callbacks. Several operations here can throw outside the renderer catch;
   a propagated failure could occur before any D00 receipt exists.
3. DiagnosticView::Run attempts CreateRenderer and Render. Device creation is
   D3D_DRIVER_TYPE_HARDWARE, with D3D11/D2D/DWrite/CoreWindow swapchain setup.
   The catch does not retain the exact renderer HRESULT; it sets renderReady=false.
4. StartNativeControl then starts a separate MTA worker, constructs a D00 receipt
   and runs native control if rendering succeeded; otherwise it attempts a
   FAILED/DIAGNOSTIC_UI_UNAVAILABLE receipt. Worker apartment/receipt-constructor
   failure before a receipt exists yields no durable receipt evidence.

The compiled SDK C++/WinRT base.h:6529-6535 implements init_apartment through
CoInitializeEx. Changing its argument alone changes COINIT_APARTMENTTHREADED to
COINIT_MULTITHREADED. The known-working pinned LegacyForge
d1453434ceefe73bef5aff497194e09f39dde7e1 MC.Xbox/App.cpp:921 onward calls
RoInitialize(RO_INIT_MULTITHREADED), then obtains ICoreApplication and Run(AppSource).
It also performs production-specific module/relay/lifecycle work that should not
be copied into the diagnostic. The comparison is the startup apartment model,
not permission to reproduce those unrelated operations.

Microsoft's native DirectX UWP example uses an MTA entry thread; CoreApplication
creates the UI ASTA. Ordinary STA initialization on the initial entry thread is
not equivalent to that runtime-created UI ASTA.
[Microsoft DirectX app-object guide](https://learn.microsoft.com/en-us/windows/uwp/gaming/about-the-uwp-user-interface-and-directx).
The [Microsoft native application-model article](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/august/windows-with-c-the-windows-runtime-application-model)
also explains the MTA startup requirement. This is strong static evidence for an
experiment, not a runtime diagnosis of this console failure.

## Ranked causes for the owner-attributed post-update failure

| Rank | Hypothesis | Support | Uncertainty / smallest discriminator |
|---|---|---|---|
| 1 | COM apartment mismatch | STA before Run differs from Microsoft MTA startup and working launcher | Static discrepancy HIGH confidence; causal confidence MEDIUM, no underlying HRESULT/log. One argument change is the smallest controlled experiment. |
| 2 | Exception during framework/view initialization | Early HRESULT catch returns without logging; view/activation/window operations can throw before receipt worker | No exception/exit record. An existing package-scoped failure record could identify the stage; do not add logging changes to the apartment experiment. |
| 3 | Graphics/device creation failure | Hardware D3D/D2D/DWrite initialization can fail | Caught renderer errors normally still permit failure receipt; brief splash is not rendered D00 UI. Existing receipt may discriminate. Keep hardware criteria unchanged. |
| 4 | Dependency/native import loading failure | /MD CRT/API-set dependencies must resolve before startup | Registration and local reviewed CRT exports reduce suspicion, but installed console export closure is unverified. Loader/module details needed; do not install fallback speculatively. |
| 5 | Activation contract still unsuitable | Exact LegacyForgeDiagnostics.App contract not hardware-validated | Ordinary UWP pattern is statically supported; changed error cannot prove success or cause without attribution. Do not revert/rewrite entry point as part of MTA experiment. |

Ranks reflect comparative evidence, not probabilities or confirmed causes. A
transient splash can occur before app rendering and does not prove graphics PASS.
All registration, activation, rendering, native-control and persistence fields
remain independent; no current-version overall PASS is claimed.

## Prepared owner read-only identity/receipt procedure

This is a proposed narrow collection procedure, not a console action performed
by Codex. Obtain explicit owner collection approval before downloading receipts
or logs under the prior separate retrieval gate. No launch is needed to inspect
existing files. Use the current authenticated Portal without configuration changes.

1. Open the installed diagnostic's read-only details. Record exact Name
   AlgorHome.LegacyForge.RuntimeDiagnostics, Publisher CN=LegacyForgeDiagnostics,
   Version0.1.2.0, x64, App classification, PackageFullName, PackageFamilyName and
   package-relative app ID if exposed. Copy text rather than a truncated screenshot.
2. If the UI truncates the identifier, the owner can inspect only the matching
   record from GET /api/app/packagemanager/packages on the same existing authenticated
   Portal origin. Microsoft documents PackageFullName, PackageFamilyName,
   PackageRelativeId, Publisher and version there, including Xbox support:
   [inventory reference](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/device-portal-api-core#get-installed-apps).
   Do not export RegisteredUsers, SIDs, cookies, credentials or full console inventory.
3. If the existing file explorer exposes app-local storage, select only this exact
   package/container. Navigate only LocalState/Phase6B1Receipts. Do not assume the
   PC path C:/Users/.../AppData exists on Xbox. If app-local storage or this exact
   mapping is unavailable, record collection BLOCKED; do not enable shares or
   change Remote Access/security to obtain it.
4. List D00 JSON/tmp names, sizes and modification times first. Same-identity
   update may retain 0.1.1.0 files. Preserve all relevant files in this diagnostic
   directory, never deleting/replacing originals or browsing other app containers.
5. After retrieval approval, download only relevant D00-<run UUID>.json and
   corresponding tmp files to a new local evidence folder. Record actual source
   package, retrieval time, filename/size and local Get-FileHash SHA256. Parse
   copies; keep original bytes. No full-package, account-store or console dump.
6. Attribute each receipt using package_version, case_id D00, run_id,
   process_instance_id, observed_at_utc, sequence/stage/terminal status and package
   role hashes against the approved version's artifact. Timestamp alone is weak
   evidence; current registration does not make an old receipt current. If fields
   conflict or are missing, mark attribution UNKNOWN. Report no directory/no
   matching file/access denied separately; none proves the process never started.

Receipt interpretation: final PASS with D00_ACTIVATED_HASHES_RECORDED plus correct
binding/hashes supports native control and persistence. DIAGNOSTIC_UI_UNAVAILABLE
supports reaching the worker/persistence while graphics fails. A checkpoint/tmp
supports only its completed stage; an old 0.1.1.0 PASS is not 0.1.2.0 success.
Missing/partial receipts are not PASS and do not justify a new launch.

## Prepared activation-log retrieval, existing evidence only

Preserve the existing Portal failure detail and any already available record for
this package, restricted to the actual failure time (initially +/-2 minutes;
do not widen automatically). Required fields only: time, exact package/application
ID and version if present, HRESULT/exit/exception code, named failing module and
activation stage. Keep old/new events separate. Capture a cropped/sanitized copy
for sharing while retaining the original privately. No original screenshot/log
has been supplied to Codex in this turn.

If Portal exposes only broad event streams/ETW, or requires Start logging, a
debugger, reproduction or a console-wide crash dump, stop: this preparation does
not authorize those actions. Do not assume desktop AppModel-Runtime event
channels are exposed on this Xbox build. Record unavailable evidence explicitly.
Do not collect account credentials, tokens, private keys, unrelated processes,
memory dumps or production LegacyForge logs.

## Smallest follow-up experiment and approval gates

With version attribution clarified, propose a new isolated diagnostic branch/commit
with ONLY src/app.cpp wWinMain's
init_apartment(apartment_type::single_threaded) changed to multi_threaded.
Keep CoInitializeEx through the same helper (do not also switch to RoInitialize),
LegacyForgeDiagnostics.App, renderer, dependencies, capabilities, native control,
receipt schema and D00 gates unchanged. Any deliberate future package-version
increment and generated build metadata must be recorded separately. Do not add
startup logging or other fixes to this single-variable experiment. It remains
unimplemented and unsigned here.

Next gates, in order:

1. Version attribution is resolved by the owner follow-up. Preserve the remaining
   unknown trigger/attempt count; identify timing/action from recollection or
   existing records only if available. No new launch for clarification.
2. Separately authorize narrow existing diagnostic receipt/activation-detail
   collection if desired; preserve 0.1.2.0 registration/data while troubleshooting.
3. Authorize diagnostic-only MTA source modification/build/static review. No such
   code approval is inferred from this analysis request.
4. Signing, owner update and one activation remain separate later approvals, each
   naming the exact new artifact. No retry of either currently installed artifact.

Both signed and unsigned artifact hashes were freshly rechecked; see
PRESERVATION-HASHES.json. Previous CMS/content integrity PASS and Windows
CERT_E_UNTRUSTEDROOT remain historical findings, not rerun trust assertions.
The source remains clean at c70a17e, D00 default/compiled configuration unchanged,
all Java/JNI routes disabled and production baseline d145343 preserved. STOP.
