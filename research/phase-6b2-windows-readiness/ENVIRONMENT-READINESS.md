# Phase 6B.2 Windows D00 environment readiness

2026-10-17, America/Chicago. **NOT READY FOR WINDOWS D00 EXECUTION APPROVAL.**
Preparation and read-only checks are complete. No suitable guest could be selected
or inspected. No VM was started, created or reconfigured; no feature was enabled.
No signing, certificate creation/import, package installation, activation, archived
installer execution, console contact or production modification occurred.

## Approved artifact re-verification

| Item | Result |
|---|---|
| Branch/current HEAD | PASS: research/phase6b1-runtime-diagnostics / df23adb6dbe948079510cf12eb64d5fd23542256; clean |
| Built source | PASS: all recorded input bytes match commit 4101f7ee07d1c74911ffbf5cd2a44aff608c401d and build evidence |
| Unsigned APPX | PASS: ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558; 59,847 bytes |
| Manifest | PASS: AlgorHome.LegacyForge.RuntimeDiagnostics; CN=LegacyForgeDiagnostics; 0.1.1.0; x64; App / Windows.PartialTrustApplication |
| Capabilities/dependencies | PASS: none; Windows.Universal >=10.0.17763.0; Microsoft.VCLibs.140.00 >=14.0.0.0, Microsoft publisher |
| D00 lock | PASS, static: preprocessing excludes S21 handlers/workers/actions; direct entry rejects E_ACCESSDENIED; no JNI/runtime loader path |
| Payload | PASS: exact approved payload/ZIP bytes; no JVM, DLL/class/runtime/Minecraft/auth payload or package signature |

Static checks were rerun using tools/audit_d00.py as a data reader, never loading the
EXE. Source evidence: [D00 safety review](../../../phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/docs/D00-SAFETY-REVIEW.md)
and [build evidence](../../../phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/docs/D00-BUILD-EVIDENCE.json).
New static audit: `phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/out/20261017-122521-8ece767b/phase6b2-reverification.json`
relative to ReverseLegacyCraft. Windows/C++WinRT loader imports remain as previously
documented; transitive module resolution is not experimentally verified.

## Environment findings and unmet prerequisites

| Prerequisite | Verdict | Evidence / next required input |
|---|---|---|
| Windows host | PASS | Windows 11 Pro x64, 10.0.26300; hypervisor present. This host is not the selected test guest. |
| Hyper-V infrastructure | PASS, limited | Get-VM command exists; vmms, vmcompute and hns are running. Presence is not a guest-readiness result. |
| Hyper-V VM inventory | BLOCKED | Get-VM permission denied; config directory access denied. Medium-integrity token, Administrators SID deny-only. Owner/admin read-only inventory needed; no self-elevation attempted. |
| Optional feature state | BLOCKED | Sandbox, Hyper-V-All and VirtualMachinePlatform queries require elevation. No state inferred from query failure. |
| Windows Sandbox | BLOCKED | Standard System32 launcher absent; feature state not readable. Not launched. Default networking/clipboard would be unsuitable; vGPU-disabled WARP may not satisfy this app's hardware D3D11 request. |
| Other VM products | BLOCKED | VMware/VirtualBox commands and standard install/default VM locations not found. Not proof that no custom installation exists. |
| Disposable Windows 11 x64 guest | BLOCKED | None verified/selected. Proposed route: owner-designated disposable full VM; Hyper-V is an available candidate platform, not an approved guest. |
| Isolated local account / clean data | BLOCKED | No guest access; no account, credentials, domain state or personal-data cleanliness attested. |
| No shared drives/clipboard/devices | BLOCKED | Guest/session configuration unavailable. Owner must attest and provide read-only configuration evidence. |
| Guest UWP sideloading | BLOCKED | Guest OS edition/policy, AppXSvc and registration support unverified. |
| Guest graphics | BLOCKED | No guest driver/DX feature evidence. App requests hardware D3D11 with feature levels 11_1,11_0,10_1,10_0; ordinary Hyper-V video or WARP alone is not proof of support. No graphics changes made. |
| Guest x64 UWP VCLibs | BLOCKED | Host has Microsoft.VCLibs.140.00 14.0.33519.0 X64/X86, IsFramework true. Host installation is not guest installation. No redistributable APPX found in the checked SDK/VS locations. |
| Signing | BLOCKED | SDK SignTool exists. No CN=LegacyForgeDiagnostics certificate found in CurrentUser/My or LocalMachine/My metadata; other owner-controlled signers not ruled out. No private key accessed/exported. |
| Guest network disconnected | BLOCKED | No guest/NIC inspection possible. Must be disconnected at hypervisor and confirmed before activation; no network changes made now. |
| Snapshot / receipt retention / rollback | BLOCKED | No guest or snapshot identifier; owner must select the exact disposable guest and evidence-retention route. |
| Exact future procedures | PASS, prepared | OWNER-RUNBOOK.md; placeholders deliberately prevent claiming a selected guest or signed hash. |

The current session cannot establish an existing VM's identity, safety or graphics
support. It would be inaccurate to invent a guest or declare execution ready. A
configured fresh guest (or owner-provided read-only evidence) is required before
the report can change. A planned VM name is not evidence of an available VM.

## Decision

**BLOCKED:** select/inspect the disposable guest, verify isolation and graphics,
resolve guest VCLibs and sideload policy, nominate the local signer/trust plan and
snapshot, then obtain explicit signing/install/activation approval. Merely granting
run approval does not satisfy missing infrastructure. Keep the pinned source and
unsigned artifact unchanged. Java and Xbox remain out of scope.

Microsoft references checked today: [Sandbox configuration](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file),
[Hyper-V session sharing](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/enhanced-session-mode),
[certificate requirements](https://learn.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing),
[SignTool](https://learn.microsoft.com/en-us/windows/msix/package/sign-app-package-using-signtool),
[Add-AppxPackage](https://learn.microsoft.com/en-us/powershell/module/appx/add-appxpackage).
