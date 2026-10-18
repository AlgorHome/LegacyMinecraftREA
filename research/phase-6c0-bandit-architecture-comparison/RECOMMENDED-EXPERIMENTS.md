# Prioritized experiments - proposals only

No experiment implemented, rebuilt, signed or executed in Phase6C.0. Names below are proposal IDs, not existing result claims. State of SRV03 remains the separately built unsigned artifact.

## Common independent gates

For every candidate involving software: **G0** owner approves read-only input/provenance/license/dependency inventory (separate download approval if any needed); **G1** owner approves diagnostic-only source plus unsigned build/static review; **G2** separately approve signing one pinned copy; **G3** separately approve one owner installation/update with auto launch disabled; **G4** separately approve one hardware launch; **G5** separately approve diagnostic-only existing receipt/photo retrieval; **G6** separately approve offline formal acceptance. Cleanup always separately approved. A gate does not authorize the next one. No automatic retry, dependency install, trust change, production update or game execution.

Each build has its own allowed case and original fixtures, source/runtime/policy/member hashes, package identity and distinct run/process UUIDs. Persist native STARTED/control evidence before unsafe DLL/JNI/driver work, then relevant checkpoint, terminal result and explicit retrieval-based persistence. A timeout cannot cancel a blocked native call. Missing infrastructure/artifact approval is BLOCKED, never PASS. Negative-control success applies only to its named negative oracle.

## J0 - reviewed Java21 package-native loading (first executable probe proposed)

- Question: can the exact approved x64 Java21 DLL dependency chain load under the diagnostic UWP policy? Expected: original native control, per-module path/hash/load status/export presence/Win32 error, sanitized import graph, before/after memory and terminal receipt; no VM.
- PASS: every mandatory approved dependency loads from intended package location and invocation exports resolve. FAILED: attempted mandatory load/export fails. BLOCKED: candidate/license/signature/dependency provenance or package prerequisite missing. INCONCLUSIVE: crash/hang or incomplete attributable final receipt. Load success does not mean Java runs.
- Dependencies: separate reviewed runtime source/build/license, own package identity/native control, approved native framework. No Bandit image/patches and no Minecraft or auth.
- Complexity: medium (native harness small; runtime closure uncertain). Comes before VM creation to isolate loader failure. DLL loading runs initialization code, so G4 explicit approval remains essential. All G0-G6 and cleanup gates apply.

## J1 - JNI invocation-version query (small intermediate discriminator)

- Question: does this runtime accept the production-equivalent JNI21 initialization contract, compared with a separately approved JNI1_8 control? One request configuration per build/cold activation; never silent fallback.
- Evidence: exact request/runtime/export/hash, raw JNI return, post-call args, options digest, no VM created.
- PASS: intended positive query returns JNI_OK with valid documented data; a designed negative variant is scored only against its predeclared rejection. FAILED: positive query fails or data violates contract. BLOCKED: J0/runtime/input gate unmet. INCONCLUSIVE: hang/exception/missing bound receipt.
- Complexity: low-medium, depends on J0; independent JNI specification/runtime license only. Before J2 when the request-version discrepancy needs isolation; does not retire the actual VM risk. G0-G6 and cleanup separately gated.

## J2 - one real embedded VM and original Java result (largest near-term risk retirement)

- Question: can this package start Java21 and execute one original pure-Java method on Series X? Interpreter-only first to separate VM execution from JIT requirements. No auth/game code or other native library. One VM per fresh process, no retry/recreation.
- Expected evidence: native control checkpoint, exact runtime/fixture/member/options hashes, JNI_OK and nonnull VM/JNIEnv, GetVersion, Java version/vendor, deterministic small checksum/value, exception state, bounded memory/time, terminal receipt and photo run association. Bounded heap/direct memory chosen during G1, not inherited from game launch settings.
- PASS: correct fixture result with valid VM/version/no unexpected exception and independent pins/terminal persistence. FAILED: completed VM or fixture returns error/wrong result/wrong runtime. BLOCKED: reviewed runtime or J0/J1 dependencies unavailable. INCONCLUSIVE: hang/crash/unretrievable final evidence. Interpreter PASS cannot be promoted to JIT PASS.
- Complexity: medium-high because native runtime can fail process-wide. Most useful functional test after J0/J1; G0-G6 and cleanup each separate. Do not relax D00's native-only gate; use a new Java diagnostic identity.

## N12 - one native hardware D3D12 device control (parallel second track)

- Question: does native D3D12 device creation succeed on this Series X OS/package classification independently of Java/Mesa?
- Expected: approved adapter classification, one actual D3D12CreateDevice call with nonnull output, requested minimum feature level, HRESULT, returned device flag, scoped cleanup, budget and final receipt. No queues/resources/shaders/swapchain; no WARP/fallback or device-creation loop. S_FALSE/null-output validation is not actual device creation.
- PASS: S_OK plus nonnull device and independently classified nonsoftware adapter, bounded receipt/release. FAILED: actual call/required hardware check negative. BLOCKED: platform API/framework/preflight unavailable. INCONCLUSIVE: native call never returns or evidence incomplete.
- Dependencies: accepted native activation/evidence pattern, official SDK/system D3D12; no Bandit/Mesa binary, game or account. Complexity low-medium with existing Windows tools; can follow G1-G3 preparation while Java runtime legal inputs are pending. G4 remains separately approved, no new console work now. G0-G6/cleanup apply.

## M0/M1 - independent Mesa/window-context boundary

- M0 is read-only artifact provenance/build recipe/import/export/license review, not DLL execution. Exact Mesa build plus DXIL/SPIRV/zlib companions must have independent source provenance; no assumption the public Bandit bundle is cleared. Missing source/build/SBOM/license closure => BLOCKED, inconsistent claimed inputs => FAILED, partial unresolved evidence => INCONCLUSIVE, complete reviewed inventory => PASS inventory only.
- M1 question: can that exact reviewed backend create/current/release a native context with a known version/profile on the app's CoreWindow? Use the candidate's actual WGL or EGL contract; do not copy Bandit's bridge/casts or assume prose establishes EGL. Expected module hashes, context API errors, actual GL vendor/renderer/version/extensions/current-thread observations and cleanup receipt; no draw/present in first context case.
- M1 PASS: intended context/profile and hardware backend confirmed, current on the intended thread, clean bounded result. FAILED: completed context/profile requirement violated. BLOCKED: N12/candidate/window contract unapproved or absent. INCONCLUSIVE: incomplete/hung/software renderer not independently attributable. No context-only rendering certification.
- Complexity high for independently reproducible UWP runtime, very high if Mesa must be built from scratch on limited PC resources. Follow N12 and M0, not a prerequisite to J2. Own exact licenses apply; all G0-G6 and cleanup gates required for M1.

## P1 - minimal native presentation (after backend choice)

- Question: can one backend own the window and display one original known pattern? Choose D3D11/D3D12/GL according to the unresolved boundary; do not combine backends or run an unrelated renderer during the test.
- Evidence: window/context/device identity, original shader/data hashes if used, explicit GPU errors/status, known-pixel oracle/readback where approved, bounded successful presents and owner photograph. Define any new resource/shader/readback operations explicitly during G1; none authorized here.
- PASS: predefined pixel/visual/present criteria all match. FAILED: completed wrong pixels/presentation/device error. BLOCKED: required native/context/license/window prerequisite absent. INCONCLUSIVE: no attributable frames or unreliable oracle. API success or a dialog is insufficient.
- Complexity medium-high, later than J2/N12 and corresponding context gate. No Minecraft assets; independently authored fixtures and licensed SDK/backend only. G0-G6 plus cleanup each apply.

## SRV03 - optional completion of existing narrow case

- Question: SRV owning-device canonical COM identity; not a prerequisite of J0/J2/N12. Source/unsigned build already exists at deb44072dd8e3ef2c936307b0a6788c6a95fad6b, version0.2.5.0. No source/build work authorized anew here.
- Expected/criteria: existing separately gated HARDWARE-ACCEPTANCE-PLAN.md under phase-6b5-d06-srv03 (S_OK/nonnull QIs/canonical equality/cleanup/memory/receipt). PASS only that identity; FAILED completed mismatch; BLOCKED missing prerequisite/receipt; INCONCLUSIVE timeout/attribution gap.
- Complexity low incremental implementation cost because built, but still requires signing, installation replacing0.2.4.0, one launch/retrieval/acceptance gates and owner attention. Its information value is low for global Java/graphics feasibility unless a resource/device-association defect is suspected. Existing original-fixture/native SDK scope; no Bandit reuse. Keep it preserved, optional rather than automatic next priority.

## Later questions deliberately retained

Real JIT compilation evidence, JNI callbacks/thread attachment, Java storage/ZIPFS, controller/focus/reconnect, low-volume PCM/OpenAL, context loss/lifecycle and a controlled Java-to-graphics bridge each need distinct fixtures and gates. No56-target sweep, loader or Minecraft gameplay experiment until these core feasibility boundaries and legitimate target/account requirements are separately reviewed.
