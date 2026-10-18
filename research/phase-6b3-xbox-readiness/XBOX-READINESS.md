# Phase 6B.3 Xbox Series X D00 deployment readiness

2026-10-17, America/Chicago. **Preparation complete; signing, deployment and
execution remain BLOCKED pending inputs and explicit authorization.** No console
was contacted. No private key was accessed/exported, certificate created, package
signed/installed/launched, dependency downloaded or production code modified.

Windows execution remains deferred/BLOCKED. Owner-reported host assessment:
Windows 11 Pro x64, 7.8 GB RAM, approximately30 GB free on the sole C: drive,
Hyper-V enabled/no existing VMs, Sandbox disabled. No full VM is proposed here.

## Revalidated artifact

| Property | Result |
|---|---|
| Built source | PASS: 4101f7ee07d1c74911ffbf5cd2a44aff608c401d; all build input bytes match that commit and recorded hashes |
| Review/current HEAD | PASS: df23adb6dbe948079510cf12eb64d5fd23542256; research/phase6b1-runtime-diagnostics; clean |
| Production baseline | d1453434ceefe73bef5aff497194e09f39dde7e1; no changes |
| Unsigned APPX | PASS: 59,847 bytes; SHA256 ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558 |
| Identity | AlgorHome.LegacyForge.RuntimeDiagnostics / CN=LegacyForgeDiagnostics / 0.1.1.0 / x64 |
| Entry/capabilities | App / Windows.PartialTrustApplication; no capabilities |
| Manifest dependencies | Windows.Universal >=10.0.17763.0; Microsoft.VCLibs.140.00 >=14.0.0.0, Microsoft publisher |
| D00 safety lock | PASS, static: LFD_D00_ONLY=1; S21 UI/handlers/workers/JNI implementation excluded; direct Java entry synchronously rejects E_ACCESSDENIED |
| Payload | PASS: exact original diagnostic allowlist; no DLLs, Java classes/runtimes, Minecraft/auth/proprietary launcher files; no package signature |

Source/read-only audit references: [D00 safety report](../../../phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/docs/D00-SAFETY-REVIEW.md),
[build evidence](../../../phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/docs/D00-BUILD-EVIDENCE.json),
and [this phase's machine-readable evidence](READINESS-EVIDENCE.json).
The source/report/schema and diagnostic LocalState separation are unchanged.
Existing Windows/C++WinRT support loader imports remain; no experimental module
resolution or platform compatibility is inferred from static compilation.

## Xbox-specific signing distinction

The proposed route is an owner-signed APPX with the exact diagnostic publisher,
using a separate development key retained in the owner's certificate store. A
commercial Store signing identity or production LegacyForge key is not needed for
this diagnostic development procedure. Exact certificate checks and commands are
in SIGNING-AND-DEPENDENCIES.md; no signing has occurred.

Microsoft's [Device Portal core API](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#install-an-app)
specifies a separate signing-certificate upload for Desktop/IoT, not Xbox. Do not
translate Windows TrustedPeople import commands into console instructions. This
does not prove this console will accept a given package: its current Developer
Mode/build/policy must be confirmed by the owner. Portal HTTPS identity is also
distinct from APPX signing identity. No TLS bypass automation is prepared.

## Dependencies and provenance

Required external native framework: **x64 UWP Microsoft.VCLibs.140.00**, publisher
`CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US`.
Direct CRT imports include MSVCP140_APP.dll, VCRUNTIME140_APP.dll and
VCRUNTIME140_1_APP.dll. The manifest floor is necessary but not proof that every
required export exists in an arbitrarily old framework. Windows API sets and
graphics DLLs are platform dependencies; no JVM, desktop VC EXE, Java or other
launcher dependency is required or permitted.

Host package metadata confirms Store-signed Microsoft.VCLibs.140.00 14.0.33519.0
X64/X86 in OK state. That is **not** an Xbox inventory check or a redistributable
artifact. No standalone VCLibs APPX was found in the checked LegacyForge/research,
Microsoft SDK or VS BuildTools redist locations; no VCLibs cache folder was found
in the checked Visual Studio package cache. This is a scoped search, not proof of
absence on every disk. No installed WindowsApps files were copied/repacked.

**Upload dependency provenance: BLOCKED.** Need either an owner-confirmed suitable
framework already installed on the console, or an unmodified Microsoft-distributed
x64 UWP framework APPX with source/license, identity, SHA256 and valid Microsoft
signature verification. No hash or provenance claim is invented for a missing file.
The dependency checklist defines the exact verification gate.

## Blockers and approval gates

| Gate | State |
|---|---|
| Pinned source/unsigned artifact/static lock | PASS |
| Separate signer | BLOCKED: no matching diagnostic certificate in the checked CurrentUser/My or LocalMachine/My stores; no signer nominated |
| Signed artifact/hash/signature/payload comparison | BLOCKED: signing not authorized or performed |
| Xbox OS/Dev Home/identity/resource classification | BLOCKED: owner must record current values; previous Developer Mode availability is owner history, not fresh inspection |
| Framework installed on Xbox or verified upload APPX | BLOCKED: no console access; no candidate redistributable available |
| Portal route/authentication/HTTPS verification | BLOCKED: owner-local setup and explicit connection/deployment authorization needed; credentials must stay local |
| Registration, activation, renderer, receipt writing, overall D00 | NOT EXECUTED; separate fields in OWNER-DEPLOYMENT-RUNBOOK.md |
| LocalState receipt listing/download | BLOCKED until exact diagnostic package full name and portal access are owner-confirmed |

Next permitted decision: review/approve a nominated diagnostic signer and dependency
verification inputs. Signing approval does not authorize deployment, and deployment
approval does not automatically authorize launch. Console inspection/access itself
also remains outside this preparation run. No broad sweep or Java test is proposed.
