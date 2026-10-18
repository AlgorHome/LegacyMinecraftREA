# Xbox diagnostic harness plan

Phase 6B planning only, 2026-10-17. This document specifies a future, independently built diagnostic APPX; it does not implement, build, sign, install, deploy or execute one. The diagnostic cases are self-authored and require no Minecraft JARs, game assets, launcher authentication, accounts, ownership checks, gameplay or network connection. LegacyForge production code remains read-only.

The initial runtime is **Java 21**. Java 17, Java 8 and the current family expected to require Java 25 are deferred configurations, each with exact runtime artifacts and a fresh process. Upstream Java requirements establish an expected major, not the Java major or behavior of a package that has not been supplied. Phase 6A records all actual Windows, Xbox and account execution as BLOCKED. The D00–D18 identifiers below align with the Phase 6B validation matrix; harness observations cannot turn those existing game/loader target rows into passed tests.

Use this design with the [diagnostic matrix](DIAGNOSTIC-MATRIX.md), [hardware acceptance rules](HARDWARE-ACCEPTANCE.md), [primary platform references](PLATFORM-REFERENCES.md) and [proposed receipt template](receipt.template.json). Those documents define the initial S21 acceptance path; this file specifies the harness architecture and evidence collection. Native-only control success remains separate from runtime success.

## Package and architecture boundary

Propose a standalone native x64 UWP CoreWindow app with a diagnostic identity such as **AlgorHome.LegacyForge.RuntimeDiagnostics**, its own Application Id, entrypoint, executable, version, display name and app-local storage. The publisher and signing subject must be explicitly chosen for that separate package. It must never use the production identity **AlgorHome.LegacyForge**, overwrite a production APPX, migrate production data or open production profiles. Package identity is part of every receipt.

Use a native C++ host, one owned CoreWindow, packaged runtime/native modules and self-authored Java classes. The native host selects only bundled, hash-listed scenarios. It does not import the production launcher, invoke its build pipeline, execute downloaded processors or select game targets. Reuse of an approved existing GLFW/Mesa artifact is a separately recorded dependency choice; the diagnostic app and Java/JNI fixtures remain independent source.

The baseline manifest should request only capabilities justified by its chosen local diagnostic APIs. Network, broad filesystem access, full trust and microphone access have no purpose in this plan. Do not copy the production capability block. A proposed JIT-related codeGeneration capability or expanded-resource variant requires its own platform review, approved manifest and separate package hash; neither presence nor absence of a source declaration establishes a console grant or JIT result. The owner selects and installs a future approved package locally. No credentials or Device Portal access are inputs to the harness.

D00 records actual package activation, process identity, inventory/hash verification and the effective manifest profile before any runtime result is attempted. A missing prerequisite prevents the affected case from starting; it does not become a successful empty run.

The production [manifest identity and dependencies](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/Package.appxmanifest#L9) are reference evidence, not a diagnostic manifest to copy. Its x64 Windows.Universal/VCLibs declarations do not prove a new package activates on Series X.

## Build prerequisites and present evidence

A separate build workspace would need the following. These are requirements for a future implementation, not steps executed in this phase.

| Requirement | Pinned-source or dossier basis | Remaining qualification |
|---|---|---|
| Native x64 C++ compiler/linker, C++17, UWP API partition, Windows/WinRT headers and libraries | Production [compile/link invocation](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/build.ps1#L406) uses C++17, WINAPI_FAMILY_APP, /MACHINE:X64, windowsapp/runtimeobject, D3D11 and DXGI | Standalone source must compile/link against an explicitly recorded SDK; production flags such as AVX2 are not a diagnostic hardware guarantee |
| CoreWindow application/package tooling and approved signing inputs | [Package/signing stages](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/build.ps1#L1260) identify makeappx/signtool and version-sensitive paths | Do not run production build.ps1: it writes staging/caches/certificates, can stop processes and includes game/loader preparation |
| Exact approved x64 packaged Java 21 runtime, JNI headers and supporting DLLs | [PreloadJvm](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L663) and [runtime-family selection](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/runtime_manager.cpp#L1079) | No packaged JVM was supplied by Phase 6A. A desktop JDK or release file cannot replace the intended UWP runtime |
| Trusted compiler for self-authored Java classes | E19 records existing trusted Adoptium JDK 21 and compiler-only validation of RuntimeProbe.java | Record compiler/header/source/class hashes and class-file targets; this is not runtime validation |
| Exact approved GLFW shim, mouse-support dependency and Mesa set | [GLFW shim build](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/build_glfw.ps1#L60) links the mouse-support import library, gameinput and WinRT libraries | The built shim/import library was absent. Six Mesa DLLs present in source do not establish the full selected dependency closure or successful console loading |
| Output-only platform audio API, and optionally the exact OpenAL module being assessed | D12 is an independent platform render control; D13 assesses a separately identified OpenAL output path | Select SDK-supported output APIs and approved local artifacts during implementation. Do not acquire a game or native binary implicitly |
| Series X Developer Mode and owner-operated installation/results | [E19 execution readiness](../legacy-launcher/EXECUTION-READINESS.md) | Hardware/deployment history is owner-reported; no new diagnostic APPX, configured console access or physical receipt exists |

[E19's curated tooling observations](../legacy-launcher/evidence/execution-readiness.json) recorded VS2022 Build Tools 17.14.37710.0, MSVC 14.44 and SDK 10.0.26100.0, sampled compiler/linker/package tools, headers/libraries, an existing trusted Ghidra JDK 21 and JDK 25 metadata. They did not establish a usable full JDK 17, a successful standalone build/link/sign/deploy, current tool configuration or any installed tool's suitability for every stage. Missing UWP workload registration alone was inconclusive because pinned source directly invokes cl.exe. Recheck those prerequisites before a separately authorized implementation; do not install or configure them as part of this plan.

## Proposed source and fixture layout

The following is a design outline. None of these new implementation files are created by this document.

~~~text
runtime-diagnostics/                       independent workspace
  README.md                               scope, owner procedure, build/receipt identity
  contracts/
    scenario-manifest.schema.json         bounded scenario/configuration allowlist
    diagnostic-receipt.schema.json        typed stage results, identities, attachments
  package/
    Package.appxmanifest                  distinct identity, approved minimal capabilities
    Assets/                               original diagnostic-only assets
    runtime-inventory.json                hashes, roles, CPU, module/patch/SDK provenance
  src/
    app/                                  CoreWindow, owner UI, activation/lifecycle dispatcher
    host/                                 case runner, watchdog, receipt/checkpoint writer
    runtime/                              packaged load, JNI query/create, Java entrypoint
    native/                               original C/JNI exports, callbacks, thread attach
    graphics/                             D3D control, GLFW/Mesa path, readback/present checks
    input/                                controller, owned-window keyboard/pointer, focus
    audio/                                platform output control, optional OpenAL output
    storage/                              app-local roots, bounded filesystem/ZIPFS scenarios
    telemetry/                            resource sampling, fixed error codes, privacy filter
  java/diagnostic/
    RuntimeProbe.java                     reviewed original subset, with provenance retained
    NativeProbe.java                      original JNI round trips and controlled exceptions
    ComputationProbe.java                 original bounded workload and expected checksums
    GraphicsProbe.java                    original JNI bridge; no game or loader dependencies
  fixtures/
    shaders/                              original GLSL/HLSL sources and expected image rules
    audio/                                original PCM description/generated waveform hash
    filesystem/                           deterministic payload/ZIP entry expectations
    input/                                fixed button/key/pointer scripts; no free text
  build/                                  future standalone build and offline packaging definitions
  tests/                                  future host-side receipt/fixture controls
~~~

Java and native package dependencies require an explicit source/license/version ledger. No phase of this design requires copying proprietary launcher code, a Minecraft client JAR, an asset object or a user's files. A full runtime/module inventory binds the approved runtime, patches, shim, Mesa/backend, JNI native, Java classes, shaders and audio fixture to each APPX. The host rejects a missing or changed required artifact rather than silently loading a system or production copy.

The existing [RuntimeProbe.java](../legacy-launcher/tests/probes/RuntimeProbe.java) is the only already prepared original runtime source fixture referenced here. [Its E19 contract](../legacy-launcher/tests/probes/README.md) records compilation with trusted javac --release 8 to two major-version-52 class files, without execution. It covers a fresh app-local child, a bounded thread, file write/read/hash/rename and ZIP-generation/ZIPFS-readback. It does not establish JNI startup, JIT, native loads, ZIPFS write/update, graphics, input, audio or a physical test pass. Incorporating that subset would preserve its hash/history and add new scenarios as separately identified source.

## Case runner and fresh-process discipline

Use one deliberately selected scenario/configuration per app activation. Each run gets a random diagnostic run ID and a monotonic sequence, an exact package/scenario/configuration hash, an app-local owned result directory and a fresh process-instance identifier. The owner sees the scenario and current stage before selecting Start. The host has no general shell, arbitrary DLL/JAR/classpath/path/URL input or remote-control interface.

Proposed state flow:

~~~text
ACTIVATED -> INPUTS_VERIFIED -> READY_FOR_OWNER -> RUNNING -> VERIFYING
          -> RECEIPT_FINALIZED -> AWAIT_OWNER_EXIT -> PROCESS_TERMINATED

Any unreached dependency: BLOCKED
Observed unexpected result: FAILED
Timeout, loss of observation, or unsupported instrumentation: INCONCLUSIVE
PASS: only the exact case's observed acceptance evidence is complete
~~~

A native-only D3D control and a GLFW/Mesa scenario should use separate activations. In particular, the app must not retain a D3D control swapchain while Mesa owns the same CoreWindow. Pinned [App.cpp:812](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/App.cpp#L812) records a swapchain ownership concern in the production path; that source comment motivates a controlled isolation test, not a reproduced diagnostic failure.

A process may attempt at most one JVM creation. A different runtime, requested JNI version, JVM option set or interpreter/JIT mode requires owner termination followed by a fresh app activation. Do not unload/reload a used JVM, retry another initialization version after a failed creation, or infer that DestroyJavaVM permits a second VM. Pinned [one-VM guard](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L54) supports this precaution. The design does not create child desktop processes from UWP.

A second launch request can reactivate an existing suspended UWP process. Accept a fresh-process case only after the owner has actually terminated the old process and the new process-instance marker differs; an activation event alone is insufficient. A process that has already attempted VM creation refuses another runtime/configuration selection.

Before a potentially blocking native/JNI/GPU call, commit a small checkpoint containing the run ID, case/configuration hash and stage. Keep JNI/runtime work off the CoreWindow dispatcher. A watchdog can record timeout/heartbeat loss while it remains schedulable; it cannot promise to cancel a blocked driver/JVM call or recover a wholly hung process. The owner therefore has a stated observation deadline and termination procedure. A checkpoint without a final receipt remains INCONCLUSIVE, not successful. No unsafe thread abort, unbounded wait or automatic repeated JVM launch is proposed.

Timing budgets are authoritative in [DIAGNOSTIC-MATRIX](DIAGNOSTIC-MATRIX.md), configurable only through a hash-bound scenario approved before the run: module10s, JNI query5s, VM creation30s, short JNI computation10s, graphics30s/120frames, generated tone2s within a30s audio case, and input prompts60s per declared peripheral. Lifecycle recovery has its own10s post-resume bound and explicit cycle count. These are proposed diagnostic deadlines, not measured performance expectations or platform guarantees. Suspension and active-run time are tracked separately; pause an owner-wait clock during actual suspension without fabricating a successful run.

## JVM, JNI and generated-code evidence: D01–D05

Separate these observations in the receipt:

1. **D01 module availability:** the intended package-relative JVM and dependent module load result, actual loaded identity/architecture, selected path role and required export lookup outcomes. Import-table presence and a non-null export do not prove invocation.
2. **D02 initialization-version query:** requested numeric/hex JNI version, JNI_GetDefaultJavaVMInitArgs result and precise operation performed before creation. GetEnv requires an existing VM and belongs to the post-creation observations. A query's acceptance does not prove VM creation, execution or a negotiated fallback.
3. **D03 VM creation:** exact requested initialization version/options hash, JNI_CreateJavaVM result, non-null VM/environment, post-creation GetEnv status for the explicitly requested interface and independently recorded environment-interface version. GetVersion reports an interface version, not the Java release or an automatic fallback negotiation. Never label a query result or release file as an accepted running VM.
4. **D04 synthetic Java/JNI execution:** entrypoint reached; bounded expected integer/array/string/callback results; controlled exception reporting; self-reported Java major/architecture compared with the package inventory. This is separate from native initialization success.

The first Java 21 pair is a portable **JNI_VERSION_1_8** control and the production-like **JNI_VERSION_21** request, each in a fresh activation. Fixed [production initialization](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L1336) is source evidence for the latter comparison. Record symbolic labels and exact header-defined numeric values; do not invent JNI_VERSION_17 or assume a Java major maps to a same-number JNI constant. Deferred Java 17/8 cases use constants actually supported by their headers and include a separately approved too-new-request negative control. A rejection observed in that control is not a broad runtime failure.

The original native fixture should export a fixed C ABI/version function, its explicitly named JNI methods and JNI_OnLoad where required. Exercise C-host-to-export, Java-to-native and native-to-Java paths separately. Use known synthetic scalars, fixed UTF-8, bounded arrays and one controlled Java exception. Check thread attachment/detachment and callback completion with a retained class/global reference and a bounded worker. An export existing, JNI_OnLoad returning or a method lookup succeeding cannot substitute for the expected round-trip result. Missing-export/dependency and controlled-exception fixtures are explicitly named negative cases, not attempts to load arbitrary files.

For D05, define a small self-authored arithmetic workload with runtime-supplied synthetic inputs, a bounded warm-up/iteration budget and an independently computed reference result. Use defined integer arithmetic; avoid a C++ reference with signed-overflow undefined behavior. Compare an interpreter control and a candidate compiled configuration in separate activations of the same runtime artifact. The checksum establishes computation correctness only. Faster time, warm-up, imported VirtualAlloc functions or equal checksums cannot prove JIT.

A JIT pass additionally needs trustworthy evidence that the exact self-authored method was compiled, tied to its class/method/source hash and run. Choose a runtime-supported compilation event/diagnostic channel during implementation; retain only the allowlisted method evidence, not a whole property/log dump. If that channel is unavailable or the workload never demonstrably compiles within the bound, report **INCONCLUSIVE_JIT_UNPROVEN**.

W^X is another explicit property. It requires supported observation of relevant code-memory allocation/protection transitions for this approved runtime/workload and evidence of the final executable mapping and permitted write policy. Successful Java execution, a codeGeneration declaration or a compiled-method event alone does not prove W^X. The implementation may need an independently reviewed instrumented runtime variant; if sufficient observation is unavailable, W^X remains Unknown/INCONCLUSIVE. No arbitrary shellcode, self-modifying payload or executable-memory policy bypass is part of the fixture.

## Graphics and the Java bridge: D06–D09

D06 provides a native platform control: create a D3D11 device and CoreWindow swapchain, draw a fixed original pattern, read back owned pixels and record Present/device status and owner-visible outcome. Use a known unorm format and declared comparison rules. The [existing CoreWindow swapchain call](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/ui/auth_screen.h#L103) is a source anchor for the relevant API route, not a diagnostic implementation or outcome.

D07 then assesses the exact approved GLFW shim and Mesa/backend in its own activation. Publish only the harness's CoreWindow through the documented interface chosen for that approved shim; record the selected backend and module identities rather than assuming WGL, EGL or D3D12 was used because its DLL was packaged. Request a declared context/profile, query what was actually created, compile/link original vertex/fragment shaders, upload fixed geometry and draw into a small owned framebuffer. Use a deterministic RGBA8 image with blending, multisampling, dithering and color-space conversions controlled; hash the readback and compare specified interior samples with an explicitly chosen tolerance. A shader compile/link result, a loaded OpenGL DLL or an empty window is insufficient.

After framebuffer verification, render the matching pattern to the owned window and call the selected present path for a bounded frame sequence. Record readback correctness, swap/present results, presented-frame counter if available and the owner's visible-pattern confirmation separately. A shim counter only counts its own event; it does not establish GPU completion or visible display. Preserve device-removed/context-loss results. An optional owner image attachment must show only the diagnostic surface and be reviewed before export.

D08 compares raw GL capability/extension observations with shim APIs and a small required-function fixture. Do not demand an extension string merely because a feature became core; compare each defined query according to its contract. Pinned [glfwExtensionSupported returns false](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L3979) and [glfwGetProcAddress routing](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L3987) make this a distinct interface test. A discrepancy remains an observed failed interface criterion even if a basic frame displays; no production shim fix is made by this plan.

D09 invokes the same bounded graphics fixture from self-authored Java through the original JNI bridge. It binds class/native/shim/Mesa/shader hashes and repeats computation/readback/present assertions. This proves only that exact Java/JNI bridge. It cannot certify LWJGL's Java bindings, an absent loader, Minecraft rendering or every catalog version; those artifacts are deliberately not required by the diagnostic harness.

## Input and audio: D10–D13

D10 uses the same selected GameInput/controller route as the supplied shim where practicable, while retaining a direct platform observation as a control. The [GameInput creation](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L1465) and [gamepad reading](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L1579) are narrow source anchors. A fixed on-screen script asks for each required button, axis neutral/end point, disconnect/reconnect and focus transition. Record normalized values/counters, stale-release behavior and which mapping/hat interfaces were actually exercised. Pinned [empty hats](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L4068), mapping-return and null-Win32-window stubs are limitations to measure separately, not proof of complete input support.

D11 accepts a small displayed key set and pointer movement/click/wheel inside the harness window. Do not collect arbitrary text, key histories outside that script or global cursor data. Quantize positions relative to the owned client surface. Test focus/capture loss and reconnection; verify held-state release rather than merely noting that callbacks exist. No HWND-dependent consumer is declared supported when the [shim's Win32 handle accessor returns null](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L4123).

If the owner has no supported keyboard or pointer for D11, record those peripheral subcases BLOCKED and preserve that limitation in the acceptance result. Controller success cannot certify keyboard/pointer capability; consult the hardware acceptance rules for a partial result rather than silently omitting a peripheral.

D12 renders a short, low-level original PCM tone through an independently selected UWP platform output API. Confirm output graph/device initialization, submitted/completed buffers, bounded timing/underrun counters and owner-heard output separately. Use an owner volume confirmation and a visible stop control; start muted until the owner elects to hear the test. Do not record or capture audio, enumerate personal endpoint names into receipts, create capture nodes or request microphone capability.

D13 sends the identical synthetic PCM through the exact separately approved OpenAL output module. No capture API is called. Record initialization/context/source/buffer/start/stop results, module identity and owner-heard output. Platform audio success does not automatically pass OpenAL, nor do OpenAL callbacks prove audible output. Owner-controlled device loss/default-output changes require bounded notification/reopen tests. If the route cannot expose switching/latency evidence, record the unavailable measurement rather than inventing it. The output-only fixtures are sufficient for this phase; no game, headset microphone or account is required.

## Storage, lifecycle and resource behavior: D14–D18

D14 obtains the host's own app-local test root through the package's storage API and passes only that owned root to Java. Create a fresh run-specific child and refuse pre-existing/symlink/reparse-point destinations; hash bounded original payloads and retain relative role names, never user paths. Test C++ and Java read/write/hash/rename outcomes separately. Use a declared small allocation/file budget and bounded ZIP entries; verify traversal/absolute-entry rejection with synthetic names. Do not touch launcher/game/user directories, exhaust the console disk or implement implicit cleanup of another run.

D15 starts with the existing RuntimeProbe ZIP-generation/ZIPFS-readback subset. ZIPFS create/update/rename/locking and explicit failure variants require separately implemented fixture cases and their own acceptance rules. A successful readback cannot pass those unwritten paths. Preserve runtime patch identities and module/options hashes; an unpatched baseline and an approved patched variant are different configurations.

D16 registers CoreWindow/application lifecycle transitions and uses owner-triggered suspension, resume and close after an on-screen ready checkpoint. [Existing lifecycle handlers](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/App.cpp#L116) motivate the probes; their source presence is not a physical test. Flush small local checkpoints within a bounded suspension-deferral budget. On resume, verify the same synthetic state and the relevant Java worker, input, graphics and audio recovery. Do not infer that suspension recreates a destroyed JVM, and do not attempt another VM after resume.

D17 samples app memory usage/limit, CPU and available GPU timings before/after each bounded workload, outside a debugger. [ReadAppMemoryBudget](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/common/launcher_common.cpp#L313) demonstrates a source route using MemoryManager and notes thread/apartment failures. Zero/unavailable values must be distinguished from a measured zero. Record package capability profile and actual limit; do not substitute a historical generic Xbox limit or desktop working-set figure. Resource headroom and supported measurement APIs remain device observations.

D18 ends the process through the owner's ordinary close/termination route, then starts a fresh activation with a distinct process-instance marker. Confirm prior-run synthetic state/receipt integrity, no stale held input/context/audio state and a new VM lifecycle. The app must not treat DestroyJavaVM success or a second Java entrypoint in the original process as a cold restart. Reset/cleanup is a separately selected action confined to the harness's own run directories.

## Receipts and outcome semantics

Design a dedicated diagnostic receipt schema that can be referenced by the broader matrix receipts; do not silently reuse Phase 6A game-target criteria. Every result should contain:

- Schema/run/process-instance IDs, D-case ID, UTC timestamps and monotonic stage durations; explicit source/scenario/configuration hashes and tool/build identities.
- Diagnostic package identity/version/APPX SHA256; manifest capability-profile hash; console model/OS build; debugger state and observer role.
- Exact JVM/native/patch/shim/Mesa/backend/class/shader/audio fixture inventory hashes; requested JNI value, query/create results, environment-interface value and self-reported Java major in separate typed fields.
- Stage attempts/outcomes, fixed error codes or HRESULT/JNI/GL/AL values, expected versus observed synthetic results, counts and defined measurement units.
- Required owner visual/audio/input/lifecycle confirmations as individual observed/absent fields, without implying automated verification.
- Confined relative attachment paths and SHA256, including only sanitized small receipts, bounded render evidence and original fixture output. Finalize atomically or explicitly mark an interrupted receipt; hashes provide integrity, not proof that an observer's claim is true.

Use PLANNED before execution, BLOCKED for unmet prerequisites, FAILED for an observed criterion failure and INCONCLUSIVE for missing/ambiguous evidence or timeout. NOT_APPLICABLE cannot satisfy a required gate. PASS belongs to one exact case/configuration whose stated observations were actually obtained. A negative case can pass its rejection criterion while the associated positive case remains untested. Unreached stages remain null/NOT_RUN, not false zero or PASS; NOT_RUN is a stage marker, not an alternative case-status enum. A case result cannot automatically certify a runtime family, all 56 game/loader targets or gameplay.

The export allowlist excludes credentials, tokens, device codes, account/user names, device serials, endpoint names, absolute storage paths, arbitrary environment/property dumps, raw command lines and unrestricted exception/driver logs. Store numeric error/status codes and fixed failure enums; review attachments locally before export. Input is restricted to the original test script; audio has no capture path. No exporter contacts a service. Hashes and structural receipt checks do not certify truth or privacy, so owner review remains explicit.

## Implementation exit conditions and uncertainty ledger

A future implementation is ready for owner consideration only after independent source review, host-only schema/fixture controls, a reproducible standalone build, artifact/license inventory, a separately signed package with the correct distinct identity and a reviewable install/run/receipt procedure. Successful compilation is one checkpoint. It cannot replace owner deployment approval or hardware results.

The first hardware sequence starts with the approved Java 21 package, native/platform controls and isolated JNI-version activations. Advance only when the previous case's evidence exists; an unrelated control may still run after a failure if its independence is documented. Java 17, Java 8 and current/Java 25 remain explicitly deferred scope with no completion claim or dropped compatibility requirement.

| Claim | Evidence already available | Evidence still required |
|---|---|---|
| Production source loads a packaged JVM and fixes JNI initialization to version 21 | Pinned source anchors and Phase 6A static dossier | Exact diagnostic runtime load/query/create/body observations on Series X |
| One original Java storage/thread subset compiles | E19 compiler-only receipt and original source | Diagnostic integration plus actual Java/ZIPFS outcomes |
| Relevant build components were found on the host | E19 bounded tool/file metadata | Future standalone compile/link/sign/activation and dependency validation |
| Context, draw/present, input, audio and lifecycle routes can be specified independently of a game | This original harness design | Implemented fixtures and measured owner hardware receipts |
| Java 21 runtime can JIT under its actual package policy with observed W^X | No physical or compiled-method/memory-policy evidence | Exact approved runtime/package, trusted compilation evidence and supported memory-policy observations |
| Console diagnostics prove game/loader compatibility | No such implication is made | Separate future game-specific work outside this account-free diagnostic scope |

This phase ends with a testable design and explicit prerequisites. It reports no harness implementation, executable artifact, approved deployment, physical PASS or change to production authentication/entitlement behavior.

