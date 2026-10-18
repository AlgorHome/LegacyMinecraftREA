# Phase 6B.3b signing and dependency preparation

2026-10-17, America/Chicago. **Static preparation complete; signing, console
access, installation, activation and execution remain BLOCKED pending approval.**

## Owner-reported Xbox observations

- Dev Home: working.
- OS/build: `10.26100.9445`, retained exactly as supplied, not silently normalized.
- Default classification: App; actual diagnostic classification is unobserved.
- Microsoft.VCLibs.140.00 x64 UWP installation: **UNKNOWN**.
- No console configuration changes, as reported by owner.

These are owner observations, not a Codex console inspection. No Device Portal
connection occurred. The candidate below does not imply the framework is absent
or present on Xbox, or that it should be installed there.

## Preserved diagnostic

Built source `4101f7ee07d1c74911ffbf5cd2a44aff608c401d`, review/current HEAD
`df23adb6dbe948079510cf12eb64d5fd23542256`, branch
`research/phase6b1-runtime-diagnostics`, clean. Source bytes were compared with the
pinned commit and build hashes. Static D00 audit rerun: PASS; no JNI/Java enabled.

Unsigned APPX: **ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558**.
Identity remains AlgorHome.LegacyForge.RuntimeDiagnostics / CN=LegacyForgeDiagnostics
/0.1.1.0/x64, no capabilities. No rebuild, signing, package modification or
production/authentication/entitlement change occurred.

## Concrete official framework candidate

Source: Microsoft-owned [WinGet release v1.29.380](https://github.com/microsoft/winget-cli/releases/tag/v1.29.380),
asset `DesktopAppInstaller_Dependencies.zip`. Its dependency metadata identifies
standard UWP VCLibs separately from UWPDesktop. No WinGet installation/command or
App Installer execution was used. The archive was downloaded only for static
inspection; only the fixed x64 UWP APPX and three DLL data files were extracted.
All third-party bytes remain outside Git and outside the diagnostic package.

| Candidate check | Result |
|---|---|
| Official archive provenance | PASS: Microsoft release API/asset; complete archive SHA256 matches API-published digest |
| Archive SHA256 | ba875afe9d190f61218985ac0292a99d1db710bf93e13c68944ca9d89f0d82d1 |
| Original archive member | x64/Microsoft.VCLibs.140.00_14.0.33519.0_x64.appx |
| Candidate APPX SHA256 | **9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283** |
| Manifest | PASS: Microsoft.VCLibs.140.00, version14.0.33519.0, x64; Framework=true; Windows.Universal |
| Publisher | PASS: CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US |
| Binary architecture | PASS: all11 packaged DLL PE headers are x64/0x8664 |
| Required direct CRT exports | PASS: all17 imported symbols present; MSVCP140_APP8, VCRUNTIME140_APP8, VCRUNTIME140_1_APP1 |
| APPX signature | PASS: SDK SignTool verify /pa /v exit0, zero warnings/errors; Microsoft Corporation signer, Microsoft Root Certificate Authority2011 chain, verified timestamp |
| License classification | CONFIRMED: Microsoft redistribution list includes unmodified retail standard-UWP VCLibs APPX; not licensed as WinGet MIT |
| Owner's applicable license terms | BLOCKED: licensing/redistribution entitlement confirmation not supplied; no unconditional legal clearance inferred |
| Console framework state / runtime compatibility | UNKNOWN / NOT EXECUTED; export presence is not Xbox transitive/API-set resolution |

Microsoft's [VS2022 redistribution list](https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution#universal-windows-apps-and-windows-store-apps)
identifies standard UWP retail VCLibs APPX as distributable unmodified subject to
applicable Visual Studio license terms. No embedded license file exists in this
candidate; the applicable external terms and owner confirmation must be retained.
Do not substitute the WinGet repository license for the framework's terms.

Candidate cache, relative to ReverseLegacyCraft:
`analysis-local/phase6b3b-dependency/Microsoft.VCLibs.140.00.x64.official.appx`.
Acquisition hashes, manifest, per-DLL hashes, imported symbol lists and signature
result are captured in [READINESS-EVIDENCE.json](READINESS-EVIDENCE.json).
Static inspection used trusted SDK SignTool/dumpbin as data readers, never loaded
or executed candidate DLLs. No Microsoft runtime binary was committed to Git.

## Remaining gates, shortest sequence

1. Owner supplies authorized read-only framework inventory, or leaves it UNKNOWN.
   No inventory claim is inferred from Dev Home working or the OS string. Portal
   access itself still needs authorization; no package download/install on Xbox is
   recommended merely because this research candidate is available.
2. Confirm applicable license terms and nominate/approve the dedicated diagnostic
   certificate workflow. Certificate creation is a separate write approval.
3. After signing approval only: create/inspect the nonexportable local key if
   needed, sign a fresh APPX copy, verify signature and unchanged payload, record
   signed SHA256. No production key/identity or private-key export.
4. Review exact signed/dependency hashes and approve installation separately;
   actual installation may need no framework upload if a suitable one is present.
5. Approve one D00 activation and owner-only receipt retrieval separately. Preserve
   registration, activation, initial graphics, writing, retrieval and overall D00
   outcomes independently, including graphics-failure evidence.

See [certificate workflow](CERTIFICATE-WORKFLOW.md) and
[final predeployment checklist](FINAL-PREDEPLOYMENT-CHECKLIST.md).
No certificate created/imported, diagnostic APPX signed, dependency installed,
application launched, console contacted or archived installer executed.
