# Phase 6B.1a rebuilt D00-only safety review

2026-10-17, America/Chicago. **PASS for source/build/static-package review;
application execution remains NOT EXECUTED and requires explicit approval.**

Branch: `research/phase6b1-runtime-diagnostics`.
Built source commit: `4101f7ee07d1c74911ffbf5cd2a44aff608c401d`.
Prior reviewed source: `f77bd4cdabb4955a95eb6b9224159604731645c7`.
Production comparison baseline: `d1453434ceefe73bef5aff497194e09f39dde7e1`.
Evidence added after the built source commit is documentation only; the build
receipt/input manifest bind that exact source commit and individual input hashes.

## Artifact

- Unsigned APPX: `out/20261017-122521-8ece767b/RuntimeDiagnostics.unsigned.appx`.
- Size: **59,847 bytes**.
- SHA256: **ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558**.
- Identity: `AlgorHome.LegacyForge.RuntimeDiagnostics` / `CN=LegacyForgeDiagnostics`
  / `0.1.1.0` / `x64`; application Id `App`; partial-trust UWP entry point.
- Capabilities: **none**.
- Dependencies: Windows.Universal minimum `10.0.17763.0`, manifest tested version
  `10.0.26100.0`; Microsoft.VCLibs.140.00 >=`14.0.0.0`, Microsoft publisher.
- Runtime files, runtime load order and Java fixtures: **empty**. Availability and
  diagnostic-runtime approval are both **false**. No S21 profile or Java class.

The exact manifest attributes, all **31 direct import modules**, remaining Windows
loader imports and every payload SHA256 are recorded in
[D00-BUILD-EVIDENCE.json](D00-BUILD-EVIDENCE.json). No third-party binary payload
is included; Microsoft platform/framework dependencies are external requirements.

## Requested patch requirements

| # | Verdict | Evidence |
|---|---|---|
| 1. Explicit compile-time D00 configuration | PASS | `include/build_config.h:4-8` defaults to 1, validates 0/1; `build.ps1:3,87` selects D00Only and supplies /DLFD_D00_ONLY=1 for every translation unit. |
| 2. Disable S21 activation/entry/worker/UI | PASS | `src/app.cpp:76,138,234,283,311,397,424,442` guards S21 result/request/worker/watchdog, event registration, polling and action UI. Preprocessed app.i contains none of those definitions/registrations. Activation arguments are not dispatched as test requests. |
| 3. Reject accidental S21 dispatch before loading | PASS | `src/jni_smoke.cpp:8-17` compiles only the synchronous E_ACCESSDENIED stub; JNI headers and implementation are excluded. Verified preprocessed body, with no scheduling, inventory access or loader call. No live stub invocation is claimed. |
| 4. Independent identity/LocalState | PASS | `package/Package.appxmanifest:5,9` retains name/publisher/App, increments version only; unchanged `src/report.cpp:175,251` uses diagnostic ApplicationData.LocalFolder/Phase6B1Receipts. An update can retain earlier diagnostic data; a fresh VM is required for clean runs. |
| 5. No runtime/Minecraft/auth/proprietary binary bundle | PASS | Exact 10-file original diagnostic staged payload allowlist plus two APPX metadata files; ZIP bytes match verified stage. `build.ps1:19` rejects every Java/runtime input in D00Only. No DLL/class/runtime payload. |
| 6. Preserve D00 and receipt schema | PASS | Native control, report.cpp and contracts/receipt.schema.json are byte-identical to f77bd4c; SHA256 values recorded in evidence. No production file changed. |
| 7. D00-only UI/docs | PASS | Manifest display/description, title at `src/app.cpp:254,411`, explanatory text and no Java action; D00-ONLY.md is current. Older documents have an explicit historical/configuration notice. No rendered UI acceptance is claimed. |
| 8. Compile/package new unsigned APPX | PASS | Four native compile steps, two preprocess steps, link, static imports, generated assets, package verification, MakeAppx and final audit all exit 0. MSVC14.44.35207 / SDK10.0.26100.0. No C/LNK warnings. No Java compiler/header tools used. |
| 9. Record source/hash/manifest/dependencies | PASS | This report and D00-BUILD-EVIDENCE.json record source commit, build/tool/input hashes, commands, identity, empty capabilities, framework and direct imports. |
| 10. Read-only rebuilt-artifact review / prior requirement 8 | PASS | Preprocessed exclusion and rejection stub, absent LoadPackagedLibrary/JNI imports/markers, exact staged/ZIP payload and no-runtime inventory verified. **Prior safety-review requirement 8 now PASSES statically**: Java execution is compile-time disabled, independently of runtime absence. |

Three independent read-only reviews (compile-time guards; package/dependencies;
D00/data/schema preservation) found no blocking defects and independently verified
the APPX hash.

Eight additional static/negative checks passed: untampered package accepted;
unexpected DLL, Java fixture and S21 profile rejected; runtime approval flag
rejected; RuntimeRoot, RuntimeInventory and JavaHome21 parameters each rejected
before output creation or compiler invocation. These tests inspect/mutate test
copies as data; they do not execute any EXE/class/JVM fixture.

## Boundaries and remaining blockers

Windows C++/WinRT support still imports LoadLibraryExW, GetProcAddress and
FreeLibrary. These are not evidence that JNI is enabled. Local SDK
`cppwinrt/winrt/base.h:4581,6096,6123-6131` implements platform activation and
combase support with these APIs; its hash is recorded. No LoadPackagedLibrary,
JNI_CreateJavaVM or process creation/termination import survives. Actual system
module resolution and transitive dependencies remain untested.

D00 has no automatic 30-second watchdog. S21's worker/watchdog is compiled out.
The receipt implementation still flushes/replaces bounded files in diagnostic
LocalState and reports persistence errors; this does not guarantee power-loss
durability or prevent arbitrary OS/native failure. D00 hashes are observations
to compare with the approved payload, not an external allowlist check.

No target execution, signing, trust change, installation/registration, Xbox
deployment, Device Portal access, credentials or production changes occurred.
Signing, trusted x64 UWP VCLibs, approved isolated Windows graphics/environment
and explicit D00 run approval remain BLOCKED inputs. Xbox is separately blocked.
No claim is made about JNI feasibility, graphics/input/audio capabilities,
Minecraft ownership, entitlement, gameplay or Xbox hardware success.

Reproduce build/prepare later validation using [D00-ONLY.md](D00-ONLY.md).
The earlier f77bd4c safety report is historical; its missing compile-time gate is
resolved only for this newly identified D00Only source/artifact. A Java21Smoke
build or changed package is outside this review and requires its own approval.
