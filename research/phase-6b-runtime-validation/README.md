# Proposed Phase 6B — Runtime Feasibility and Diagnostic Validation

Status: **PLAN FOR REVIEW, NOT IMPLEMENTED OR EXECUTED.** Date: 2026-10-17, America/Chicago. Source baseline is LegacyForge `d1453434ceefe73bef5aff497194e09f39dde7e1`. No production source, authentication or entitlement change is proposed for this stage. Approval of this document has not been assumed.

Read the concise [Phase6A evidence summary](PHASE-6A-EVIDENCE-SUMMARY.md) first. The plan answers whether an independently built Xbox UWP package can exercise the required runtime primitives. A positive result establishes only the tested synthetic package/runtime/backend combination; it does not establish Minecraft gameplay, ownership or all-version support.

## Work packages and approval gates

| Stage | Proposed work | Exit evidence |
|---|---|---|
| B0 — Freeze inputs | Approve separate source workspace, runtime/native provenance, package identity, manifest, signing control and exact test scope. Hash inputs and retain licenses. | Reviewed artifact manifest; clean approved-source baseline; no unknown executable acquisition. Missing inputs remain BLOCKED. |
| B1 — Independent harness implementation | After explicit approval, implement original native UWP shell, synthetic Java/JNI fixtures, native/graphics/input/audio/storage/lifecycle probes and receipt export. Build locally in a separate workspace. | Source/build hashes, compile/package checks, reviewed dependency graph and permissions. A build is not a runtime pass. |
| B2 — Isolated Windows qualification | After execution approval for the named guest and hashes, qualify the harness and separately exercise archived installer/update behavior. | [Windows receipts](WINDOWS-EXECUTION-PLAN.md); recorded controlled failures. No archived execution on the host. |
| B3 — Minimal Series X acceptance | Owner deploys reviewed diagnostic package and executes the small offline smoke sequence. | [Hardware acceptance](HARDWARE-ACCEPTANCE.md), structured observations and hash-bound evidence. No Minecraft account, assets, client, loader or gameplay required. |
| B4 — Evidence review | Separate baseline/native/runtime/graphics compatibility verdicts; identify minimum independently implementable production proposal. | [Uncertainty matrix](DIAGNOSTIC-MATRIX.md), unresolved issues and package-specific recommendation. Production implementation requires another explicit approval. |

The archived-launcher Windows track is independent of the ownership-free Xbox track. A missing archived-launcher sandbox does not justify executing it on the host and does not prevent planning or later approved construction of the self-authored diagnostic harness.

## Proposed implementation layout

The following is a future standalone diagnostic workspace/repository, **not files created by this planning task**. Keep it outside the read-only production checkout and use a separate package identity and app-local store.

```text
LegacyForge.RuntimeDiagnostics/
  README.md
  package/
    Package.appxmanifest                 # independent x64 identity, reviewed capabilities
    Assets/                              # original diagnostic visuals only
  native/
    App.{h,cpp}                          # CoreWindow lifecycle, case selection, UI
    Runner.{h,cpp}                       # bounded states, watchdog, fresh-process policy
    probes/
      PackageLoad.cpp  JniInvocation.cpp  JitObservation.cpp
      D3DControl.cpp   GlBridge.cpp       Input.cpp
      Audio.cpp       Storage.cpp        Lifecycle.cpp
    synthetic-jni/                       # original JNI_OnLoad/roundtrip fixture DLL
    receipts/                            # allowlisted serializer and atomic checkpointing
  java/src/                              # original deterministic Java fixtures
  fixtures/                              # generated PCM, shaders, small ZIP/data fixtures
  profiles/
    native-control.json
    java21-smoke.json
    java17-followup.json                  # deferred
    java8-followup.json                   # deferred; no 1.12.2 game/provider claim
    java25-followup.json                  # deferred
  schemas/receipt.schema.json
  tools/
    build-diagnostics.ps1                 # explicit input paths, no automatic downloads
    hash-inputs.ps1
    validate-receipts.py
  provenance/inputs.template.json         # approved source/URL/license/hash per dependency
  out/                                   # ignored local packages, classes, symbols, receipts
  local-inputs/                          # ignored approved runtimes/native artifacts
```

No third-party proprietary binaries, signing private keys, runtime archives, Minecraft client/assets or recovered code enter Git. Package approved redistributable dependencies only when provenance/license and intended execution are explicitly approved; store them outside tracked sources and retain their hashes. Do not copy the launcher's proprietary implementation or keys.

## Build requirements and current availability

Use native x64 C++ UWP/CoreWindow with a pinned Windows SDK and reviewed VCLibs framework dependency. Avoid introducing a WinUI3/desktop-process model or requiring a full production build. E19 observed VS2022 Build Tools17.14.37710, MSVC14.44 and SDK10.0.26100 with sampled compiler/linker/packaging/WinRT files; complete UWP build/link/signing remains unverified. Do not auto-install workloads.

Trusted Ghidra JDK21 can compile the Java8-compatible fixtures; existing JDK25 was observed. Actual approved Xbox-compatible JVM/JDK-derived artifacts, patches, shim builds, dependency provenance and signing identity are still needed. A desktop JRE is not an approved Xbox runtime. Header/API selection and runtime DLL must be recorded separately; classfile52 compatibility alone proves neither Java8 nor JNI execution.

Initial package variants: native control; one reviewed Java21 runtime plus synthetic JNI DLL; and the exact proposed GLFW/Mesa/OpenAL stack where inputs are approved. Do not package four JVMs merely to increase coverage. Keep package-relative module resolution and explicit dependencies; [Microsoft's LoadPackagedLibrary contract](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-loadpackagedlibrary) limits lookup to the package dependency graph.

Baseline manifest has no network, OAuth, microphone capture, broad filesystem or full-trust requirement. A JIT-specific capability/API variant, if required by the selected runtime, gets a separate manifest hash and approval. [Microsoft documents codeGeneration for the FromApp JIT route](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocfromapp); that is a documented API condition, not evidence that the exact runtime or capability will work on Series X. Do not silently add capabilities to obtain a pass.

## Representative smoke set

| Order | Synthetic profile | Why representative | Admission condition |
|---|---|---|---|
| 0 | NATIVE-CONTROL, no JVM | Separates package/CoreWindow/D3D/input/audio/storage issues from JVM issues | Independently reviewed package and owner approval |
| 1 | S21, Java21 + JNI + exact proposed graphics/audio bridge | Represents the runtime family used by the examined 1.21.11 metadata, without downloading/launching that game | Native control passes; approved exact runtime/native inputs |
| 2 | S17, Java17 | Addresses fixed-JNI21 versus older-family uncertainty | S21 reviewed; new package/hash; fresh activation for every invocation configuration |
| 3 | S8, Java8 | Investigates primitives relevant to 1.12.2 provider feasibility | S17 or explicit issue-driven exception reviewed; provider work remains separately blocked |
| Later | S25, Java25/current | 26.x metadata declares Java25 | S21 stable and explicit scope expansion approved |

The first implementation/hardware milestone is profiles0–1 only. S17/S8 are staged followups, not part of an immediate all-family run. These are runtime profiles, not Minecraft target executions; no Fabric/Forge/NeoForge processor or gameplay test belongs to this initial smoke set. All56 catalog rows remain in the Phase6A record but are not Phase6B's initial acceptance population.

## Outputs, verdicts and blockers

Each case maps to one uncertainty in [DIAGNOSTIC-MATRIX](DIAGNOSTIC-MATRIX.md) and emits an allowlisted receipt plus bounded per-stage events, module/package/source/fixture hashes and measurements. A proposed [receipt template](receipt.template.json) has no observed results and is not a validated Phase6A execution receipt. A future schema/validator must be implemented and tested before collecting results. The Phase6B case-status enum is PLANNED, BLOCKED, PASS, FAILED, INCONCLUSIVE or NOT_APPLICABLE; the last cannot satisfy a required gate. NOT_RUN is allowed only as an unreached stage marker, not a second case-status spelling. Phase6A Windows receipts retain their existing FAILED spelling and must never be upgraded from a partial synthetic result.

No configured/approved guest, exact Xbox runtime/native diagnostic package, signing/deployment inputs or new owner console evidence exists in the supplied baseline. Build tooling availability is partial evidence only. JIT, packaged loading, GL extension truth, OpenAL/device routing and lifecycle recovery remain technical unknowns. Keyboard/pointer or audio-device switching can be BLOCKED for absent peripherals; that produces a scoped partial result, never a full required-capability pass.

Approval checkpoints: (1) named separate implementation workspace and dependency/manifest plan; (2) actual build outputs, hashes, signing identity and deployment scope; (3) actual guest/console execution scope, including potentially unsafe artifacts; (4) any later production change. This task creates planning documents/templates only. No download, signing, build, deployment, authentication or target execution is authorized by a sample command or proposed tree.

## Plan documents

- [Evidence summary](PHASE-6A-EVIDENCE-SUMMARY.md)
- [Isolated Windows procedure](WINDOWS-EXECUTION-PLAN.md)
- [Separate Xbox harness](XBOX-DIAGNOSTIC-HARNESS.md)
- [Hardware acceptance without ownership](HARDWARE-ACCEPTANCE.md)
- [Diagnostic-to-uncertainty matrix](DIAGNOSTIC-MATRIX.md)
- [Separate 1.12.2/Forge assessment](LEGACY-1.12.2-ASSESSMENT.md)

Primary platform references and their interpretation limits are in [PLATFORM-REFERENCES](PLATFORM-REFERENCES.md). Phase6A's checksum manifest remains authoritative for that sealed dossier. This folder has its own checksum/validation record.
