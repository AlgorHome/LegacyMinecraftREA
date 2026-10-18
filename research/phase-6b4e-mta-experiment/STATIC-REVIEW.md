# Phase 6B.4e — MTA startup experiment static review

2026-10-17. **PASS: x64 compilation, unsigned packaging and static verification.**
No target execution, signing, installation/update, console access, certificate
store operation or dependency modification occurred.

## Source and artifact

Branch: research/phase6b4e-mta-startup.
Commit: **553c6554f40f1372b0ea09f6badbbb98e133a9ab**.
Parent: c70a17ecd4022452a963697196f362c8f286ed57, preserved on its prior branch.

Unsigned APPX:
`C:/Users/arinze/Desktop/ReverseLegacyCraft/phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/out/20261017-142300-e07d5ee8/RuntimeDiagnostics.unsigned.appx`

SHA256: **0595e9936aa4091ebdcce3e23b4e43fdba014d88267b4aaa0656fbd9cddb307e**.
Executable SHA256: 89997350241657405fc38e596788c91b45c9e5978288d066ece51e3f42a4a6b9.

Identity: AlgorHome.LegacyForge.RuntimeDiagnostics;
Publisher CN=LegacyForgeDiagnostics; Version0.1.3.0; x64; Application Id App;
EntryPoint LegacyForgeDiagnostics.App. Zero capabilities. Windows.Universal
min10.0.17763.0/max tested10.0.26100.0; Microsoft.VCLibs.140.00 >=14.0.0.0 with
unchanged Microsoft publisher. No framework or third-party runtime is bundled.

## Exact change scope

SOURCE-DIFF.patch and EXPERIMENT-VERIFICATION.json record the comparison to c70a17e.

1. src/app.cpp:488: single_threaded -> multi_threaded in wWinMain only.
2. package/Package.appxmanifest: Version0.1.2.0 -> 0.1.3.0 only.
3. tools/verify_artifacts.py: pins version0.1.3.0 and updates its mismatch message.
4. docs/MTA-EXPERIMENT.md: explains scope, startup rationale and future evidence.

The comparison helper asserts the entire app.cpp equals the parent's bytes after
that exact one substitution. Native control, graphics, report implementation,
receipt contract, JNI rejection, headers and build script remain unchanged.
Manifest XML becomes identical to the parent after normalizing only Version.
No production paths changed. All runtime changes are confined to the startup
apartment enum; the version and verifier changes are separately disclosed.

Microsoft's [native DirectX UWP application guidance](https://learn.microsoft.com/en-us/windows/uwp/gaming/about-the-uwp-user-interface-and-directx)
uses an MTA entry thread and a runtime-created UI ASTA. Existing CoreApplication
startup passes DiagnosticSource (IFrameworkViewSource) directly to Run, compatible
with this model. The change retains the SDK init_apartment helper's CoInitializeEx
call and all surrounding flow; it does not switch to RoInitialize or move the
renderer onto another thread. The working pinned LegacyForge entry uses
RoInitialize(RO_INIT_MULTITHREADED); its unrelated module/relay operations were
not copied. This is supported static reasoning, not hardware validation.

## Build and safety evidence

From the experiment checkout, existing Windows x64 MSVC14.44.35207 UWP/store
libraries, SDK10.0.26100.0/C++WinRT/MakeAppx, PowerShell7 and Python:

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration D00Only -Package
```

Every recorded build command returned exit0. Build receipt binds this commit,
compiler/tool hashes, source inputs and outputs. This command runs trusted build
and static inspection tools; it never invokes the diagnostic executable.

| Review | Result |
|---|---|
| Compilation/link x64 | PASS |
| MakeAppx unsigned package/manifest validation | PASS |
| Exact D00 payload inventory and hashes | PASS |
| Preprocessed D00-only source/rejection audit | PASS |
| All TU configuration | LFD_D00_ONLY=1 |
| S21 UI/handlers/worker/watchdog/JNI loader | excluded; direct-call E_ACCESSDENIED stub retained |
| Java/runtime/fixture inputs | unavailable/unapproved/empty; no Java/Minecraft/auth files |
| Direct native import module/function lists | identical to 0.1.2.0 |
| Delay import lists | identical (none) |
| Native PE | AMD64, GUI, AppContainer as enforced by package verifier |
| Added capabilities/dependencies | none |
| Signature member | absent; unsigned |
| Executable/hardware test | NOT PERFORMED |

Generic static-verification.json runtimeStatus BLOCKED_RUNTIME_NOT_SUPPLIED
describes the intentionally absent Java input, not a D00 build failure. Build
runtimeStatus DISABLED_COMPILE_TIME_D00_ONLY and D00 audit PASS are preserved.

Changed ZIP members: manifest, executable, diagnostic-inputs.json, native-control
profile JSON and block map. The native profile is semantically identical (key
order only); inventories bind new commit/build/source and payload hashes. The
executable reflects the changed startup argument plus incidental build metadata.
No claim of identical machine code is made for this startup experiment. Remaining
members are byte-identical; complete imports/member hashes are in the JSON audit.

## Preservation and future evidence

PRESERVATION-BEFORE/AFTER.json prove unchanged bytes for both previous signed and
unsigned packages, original certificate public metadata and the separate owner
Xbox observations. No existing receipt file was supplied or collected; receipt
persistence remains UNKNOWN, not manufactured evidence. Prior observation:
0.1.1.0 no visible run/0x87E10006; owner attributes brief appearance/apparent crash
and 0x8027025B to 0.1.2.0. The post-update trigger/attempt count remains unknown.

Source branches/commits remain reachable: original 4101f7e and review df23adb,
activation parent c70a17e, new 553c655. Production comparison baseline d145343
is preserved. No binaries or private signing material were committed.

Version0.1.3.0 identifies a future same-family update, not a side-by-side package.
No identity/publisher/architecture/Application Id change was made. Later approved
updates may retain all diagnostic LocalState, including older receipts; full
package name changes with version. Preserve current registration and old evidence
until update approval. Future receipts must be bound to version0.1.3.0, new
run/process UUIDs, observed time and approved role hashes; no storage clearing.

## Remaining risks and next gates

Compilation does not establish cause or repair of 0x8027025B. Early exceptions
can still return without receipts; native loader/API compatibility and hardware
graphics remain unverified. UI ASTA creation/activation, worker scheduling,
rendering, durable receipts and overall D00 acceptance require separately
approved observation, with each result recorded independently.

Next gate is review/approval for signing one exact copy of this unsigned hash.
Owner update, one controlled launch and narrow receipt collection remain separate
later authorizations. No new launch allowance is inferred. STOP at static review.
