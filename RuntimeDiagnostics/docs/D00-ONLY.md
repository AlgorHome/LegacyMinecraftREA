# Phase 6B.1a D00-only safety contract

The default build is **D00Only**, with `LFD_D00_ONLY=1` explicitly passed to every
native translation unit. `include/build_config.h` also defaults to 1 for manual
builds, rejects values other than 0/1, and is included by the common header.

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration D00Only -Package
```

Requirements: Windows x64, PowerShell 7, Python 3.12+, existing MSVC 14.44.35207
C++/UWP store libraries and Windows SDK 10.0.26100.0 including C++/WinRT and
MakeAppx. **No JDK, JNI headers or Java compiler is required for D00Only.** No
dependency downloads occur. Only trusted compiler, linker, preprocessor, static
inspection and packaging tools are run; the app is never run by this command.

`-JavaHome21`, `-RuntimeRoot` and `-RuntimeInventory` are rejected in D00Only
before outputs/tools are started. Each build uses a new ignored output directory;
it cannot accidentally reuse an older runtime-bearing staging tree.

## Compile-time and dispatch boundaries

- S21 keyboard/pointer handlers, gamepad polling, UI button, result function,
  request function, MTA worker and watchdog are excluded with preprocessor guards.
- JNI headers and the entire JNI implementation are excluded. An accidental direct
  `RunJava21Smoke` call throws E_ACCESSDENIED synchronously. It does not schedule
  anything, create an S21 receipt, inspect runtime inventory or load a module.
- Activation always starts D00; activation arguments are not parsed as test commands.
  There is no S21 command-line/protocol activation path.
- The retained Java21Smoke build requires explicit configuration and reviewed JDK
  inputs. It is a different artifact and is not cleared by D00-only approval.
- D00 native control, report implementation and receipt schema are unchanged from
  f77bd4c. In particular, D00 has no automatic 30-second cancellation watchdog.

## Package and isolated data

The same independent name `AlgorHome.LegacyForge.RuntimeDiagnostics`, publisher
`CN=LegacyForgeDiagnostics`, x64 architecture and application Id `App` remain.
Version is now `0.1.1.0`; manifest display/description and on-screen title identify
D00 ONLY. Same diagnostic identity retains its own existing diagnostic LocalState
if updated, so use a fresh guest for clean validation. Production identity/data
are never used. Receipt directory remains LocalState/Phase6B1Receipts.

No capabilities are declared. Dependencies remain Windows.Universal
10.0.17763.0 minimum (10.0.26100.0 tested manifest metadata) and Microsoft's
Microsoft.VCLibs.140.00 framework >=14.0.0.0. No runtime/framework DLL is bundled.
The package contains only the original diagnostic EXE, generated PNGs, diagnostic
inventories, D00 profile, Apache license and APPX metadata. No Java class, JVM,
S21 profile, Minecraft content, authentication material or proprietary launcher.

## Static evidence and acceptance limits

The build preprocesses app.cpp and jni_smoke.cpp with the same definitions used
for compilation. `tools/audit_d00.py` reads those outputs, direct imports and the
APPX as data: no S21 handlers/worker/call survive; the direct-call rejection is
present; no LoadPackagedLibrary/JNI/process-control import is present; ZIP members and
staged payload bytes match. Windows C++/WinRT support still imports LoadLibraryExW,
GetProcAddress and FreeLibrary for platform activation; this is recorded explicitly,
not represented as proof that the process loads no libraries. `tools/verify_artifacts.py` enforces an exact D00
payload allowlist, false runtime approval/availability and empty fixture/load lists.

Build receipts bind source commit, input hashes, compiler/tool hashes and exit codes;
`d00-safety-audit.json` records unsigned APPX hash, identity, capabilities, manifest
dependencies, direct imports and all payload hashes. Consult D00-SAFETY-REVIEW.md
and D00-BUILD-EVIDENCE.json for the reviewed artifact. Static acceptance is not a
claim of application activation, successful storage, transitive dependency closure
or hardware behavior. The rejection stub is inspected/compiled, never executed.

## Future execution procedure — approval still required

1. Approve the exact new unsigned/signed artifact and a disposable Windows 11 x64
   guest with an appropriate reviewed graphics device. Snapshot it; no personal
   accounts, host data shares, clipboard, Minecraft or production LegacyForge.
2. Owner signs locally with a suitable signer matching CN=LegacyForgeDiagnostics;
   private key/password stay local. Record signature and signed hash; approve guest
   trust changes and trusted x64 UWP VCLibs dependency. No chat secrets are needed.
3. After deployment/activation approval, register the signed diagnostic APPX and
   framework inside the guest, disconnect guest networking and launch only its
   `<diagnostic-PFN>!App`. Do not run the raw EXE. D00 starts automatically.
4. Observe for 30 seconds using an external timer; inspect D00-*.json under this
   package's LocalState/Phase6B1Receipts. Expect terminal PASS with reason
   D00_ACTIVATED_HASHES_RECORDED, expected identity, complete role hashes matching
   the approved payload, and no S21 receipt. Metrics may be unavailable with numeric
   errors; UI drawing does not prove graphics/input/audio capabilities.
5. Missing receipt, RECEIPT_ERROR, failure or hang is not PASS. Preserve JSON/tmp,
   screenshot and sanitized activation codes. Close only this diagnostic app or
   revert the disposable guest; no broad process-kill or production cleanup.
6. Export only sanitized evidence and hashes, then revert after evidence is preserved.

Xbox deployment remains separately blocked: owner-controlled Series X Dev Mode,
accepted signing policy, matching x64 UWP framework and an approved deployment/
receipt-retrieval route are needed. No Device Portal contact or console deployment
is authorized here; no Minecraft ownership/gameplay is required for D00. The older
XBOX-ACCEPTANCE.md Java steps are not part of this run. No application execution,
signing, registration, deployment or production change is performed by this patch.
