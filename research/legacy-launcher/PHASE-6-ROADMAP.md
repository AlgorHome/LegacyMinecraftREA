# Phase 6 engineering roadmap

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

These are independent implementation proposals, not production changes made by Phase 6A. Preserve current entitlement checks, Credential Locker storage, local-session boundaries, mods behavior and established Xbox adaptation.

| Priority / proposal | Existing code to extend | Concrete acceptance evidence |
|---|---|---|
| P0: target/runtime readiness record | ResolveJavaRuntimeInfo, ResolveVersionInfo, RunEmbeddedMinecraft, target catalog | Version/loader, runtime identity/major, supported JNI invocation, native hashes/ABI, graphics provider and explicit Unknown/Unsupported/Validated state |
| P0: resolve Java/JNI agreement | Fixed JNI_VERSION_21 assignment versus java17/legacy families | Independent synthetic invocation tests for exact packaged runtime; supported version chosen/negotiated, no false success; explicit failure with runtime identity |
| P1: deterministic metadata rule contract | Test-LibraryAllowed and Convert-ArgumentArrayToList | Fixtures for ordered allow/disallow, OS/arch/version/features, conditional string/array args, unsupported conditions and loader module options |
| P1: repair receipts | EnsureRuntimeDownloads and PrepareTargetNativeDir | Manifest hash + target, checked/reused/downloaded counts, mismatch/retry/cancellation results, promotion result and native/runtime readiness; no token values |
| P1: exact native/graphics validation | Existing GLFW shim, Mesa packaging, Java/native patches | Exact module versions/imports, JNI exports, minimal window/context/shader/presentation/input/audio probes |
| P2: version discovery UX | Existing build-generated target manifests/catalog | Distinguish upstream availability, downloaded state, experimental target and hardware-validated support; no automatic enablement from catalog presence |
| P2: loader-specific support expansion | Existing Fabric/Forge/NeoForge providers; missing 1.12.2 provider boundary | Reproducible processor/classpath/main/options output; explicit per-target unsupported outcomes; no reuse of proprietary launcher implementation |

Evidence motivating proposals: E03/E04 establish version-driven requirements; E07 establishes existing services and narrower gaps; E08 establishes platform contracts and remaining requirements. Any implementation should describe the permitted behavior independently, with synthetic fixtures and official metadata contracts, without copying proprietary code/resources.

## Future execution gates, requiring separate authorization

1. Verify package activation and actual console/OS/package identity.
2. Validate the selected JVM primitive and supported JNI invocation version in isolation.
3. Run a minimal synthetic Java entrypoint, filesystem/threading and error propagation.
4. Validate packaged JNI/native symbol loading and selected module identity.
5. Create the required graphics context, verify capabilities, draw/present a synthetic frame.
6. Exercise input/audio and suspend/resume within measured memory/resources.
7. Validate an owned authenticated game launch for one exact target/loader; redact receipts.
8. Expand only after recording exact versions, results, limitations and regressions.

These gates are proposed validation design, not tests performed in this research pass. Existing Phase 5F.2 hardware testing reported by the user remains relevant context but cannot be extrapolated to all catalog targets. Download completion alone must never become a gameplay feasibility claim.

## Continuation and full-scope execution handoff

Installer decoding and original-build comparison are now completed statically. Update/download/profile/inheritance traces and native graphs are expanded. Preserve all 56 targets and use the prepared Windows/Xbox procedures and receipt template; no infrastructure-dependent test is passed. Include extension-query/Win32-handle/gamepad-mapping consumers in graphics/input validation. Do not install or execute archived code until a disposable environment is approved; the owner explicitly retained static-only authorization. No scope reduction or production/authentication/entitlement change is proposed by this research handoff.

Final preparation adds complete public metadata plans for all56 rows, an embedded-key signed response fixture, corrected prerequisite receipts and an original Java8-compatible probe source. The `current` targets' official metadata requires Java25; actual packaged runtime identity and JNI behavior must be tested. Extend the standalone fixture only within separately approved diagnostic integration; it does not supply native/graphics/input/audio checks. The first independently implementable changes remain runtime/JNI readiness records, deterministic metadata contracts and structured repair receipts, followed by exact native/graphics validation. No production change was made to implement them during Phase6A.
