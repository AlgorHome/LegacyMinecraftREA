# Phase 6B.5w - D06-SRV02 Xbox hardware acceptance

**Determination: PASS_D06_SRV02_ONLY.** Visible PASS, schema-bound receipt PASS and formal case acceptance PASS are recorded separately. No FAILED, BLOCKED or INCONCLUSIVE required case criterion remains. This result applies to the owner's one supplied run and the pinned build only.

## Original evidence and preservation

Original receipt: `C:\Users\arinze\Desktop\D06-SRV02-8A125555-353C-4C3D-AD19-D8849FD138A8.json`

SHA-256: `307dde1773ff9f5aba5b44862c7e9ef1c4179d97035161d873d832364a6e0436`; matches owner-provided pin.

Original photograph: `C:\Users\arinze\Desktop\IMG_5565.JPG`

SHA-256: `6f71797139b62009b9a353877b0db42aa1091211cb028edd79a03ade28293f18`; independently calculated locally (no prior owner photo hash was supplied). Original 4032x3024 photograph was viewed; the displayed preview was resized. Original bytes were not edited, recompressed or sanitized in place.

Run: `8A125555-353C-4C3D-AD19-D8849FD138A8`; process instance `31218D4A-0751-426A-9239-DC244FF507B2`. Both valid distinct v4 UUIDs; filename agrees with run. Photo visibly shows D06-SRV02, package 0.2.4.0, PASS, SRV_BACKING_RESOURCE_IDENTITY_CONFIRMED, hardware request/no fallback, device HRESULT 0x00000000, feature 0x0000B000, saved-receipt message and the exact same full run ID.

All 175 frozen baseline pins and 199 total preserved signing/evidence files were rehashed unchanged. Original photo and JSON rehashed unchanged after analysis. Approved checkout remains clean at c81d0f48286513f7a7579a1d2d786cca4f5e60e2. Source comparisons with that commit account only for Git CRLF/LF checkout normalization. No source or accepted report edited, no application executed, no console data retrieved, no install/sign/build/trust action.

## Identity and pinned build

Source `c81d0f48286513f7a7579a1d2d786cca4f5e60e2`; build `20261017-192156-1c3f66cf`. Receipt source and build agree with the packaged native-inputs sourceCommit/compiledSourceCommit/buildId and independent BUILD-EVIDENCE.json. Schema v5 is byte-identical to the pinned RECEIPT-SCHEMA.json and validates with the commit-pinned offline structure and semantic oracle, including duplicate-key rejection and closed property sets.

Package: AlgorHome.LegacyForge.NativeDiagnostics, CN=LegacyForgeDiagnostics, 0.2.4.0, x64, Application Id App, expected_package_identity=true. Production comparison and frozen D00/HW01/FMT01/RES01a/SRV01 source references agree with the schema/source pins. PackageFullName and actual console classification were not independently inventoried in this review; no new Portal access was made.

Unsigned SHA-256: `88cde899358b6eaade1658802831c5a914b8e637cf1466321b233fa8a2788c31`.

Signed SHA-256: `a77e31a5922bca35a09084dbe885b5d13ed1207571f66458644d5ac7ee8738d5`.

Directly recomputed hashes from the unsigned archive match both the pre-sign BUILD-EVIDENCE pins and all six receipt roles. Signed archive members are byte-identical for these roles:

| Receipt role | Member | Independent SHA-256 |
| --- | --- | --- |
| executable_sha256 | NativeCapabilities.exe | `4e9e8a5563c8b4eaa0aff8d36695c03b29af7a127d5437997b4e579bbdd749b2` |
| manifest_sha256 | AppxManifest.xml | `cb09200058bafb97974ff366231fb4eca0829abc264e5aeb218bc4e4c6140550` |
| build_inputs_sha256 | native-inputs.json | `f6eb65349dd42b8192415b3147405d86093bc84f392180bcfe8199acc60c18d9` |
| policy_sha256 | profiles/D06-SRV02.json | `d81e3edf4de37d1fa699ac6af207f84d429a9391215d1b593e36d314017b4594` |
| schema_sha256 | contracts/native-receipt.schema.json | `4ab9dfbbf345704a846945d1c6609952b937f80949409c91fdf549be1cf71d36` |
| inventory_sha256 | native-inventory.json | `b30d732ac7093e8b54ad188658072de50aa3eb2a6bcabb69115f6dd6c96bcb54` |

Fresh archive verification also confirms all 12 original members other than the expected content-types update are byte-identical; all 11 block-mapped payload files, SHA-256 blocks, full-file hash extensions, sizes, local header lengths, ZIP CRCs and unique entry names pass. Only AppxSignature.p7x, CodeIntegrity.cat and their content-type declarations differ as expected. This review did not re-sign. Prior CMS and APPX SIP digest PASS remain preserved evidence; prior normal SignTool chain verification FAILED with CERT_E_UNTRUSTEDROOT (0x800B0109), not silently promoted to successful chain trust.

## Case criteria and results

| Criterion | Result | Evidence |
| --- | --- | --- |
| Registration/identity | MATCH, owner provenance | Runtime identity assertion, pinned manifest and photo version; no fresh Portal inventory |
| Activation | PASS | Photo of current case plus matching terminal receipt |
| Visible test result | PASS | Photo exact reason and run ID |
| Device/hardware selection | PASS | S_OK, device/context nonnull, feature 11_0, HARDWARE=1, BGRA flag32, adapter GetAdapter/GetDesc1 S_OK; flags0, software false, no fallback |
| Texture allocation/descriptor | PASS | S_OK, nonnull, GetDesc called, every field independently equal to fixed policy |
| SRV allocation/descriptor | PASS | S_OK, nonnull, GetDesc called, all four active Texture2D view fields equal to policy |
| Backing resource | PASS | get_resource_called and nonnull returned resource; one source call and single-case activation guard |
| Canonical identity | PASS | Both QI IID_IUnknown S_OK with nonnull identities, comparison performed, equal=true |
| Release ordering | PASS within telemetry limits | Both temporary identity references, returned resource, SRV, texture, context/device scopes; receipt release markers true |
| Memory policy | PASS | Available before/after samples; headroom >=256MiB and growth <=64MiB |
| Deadline | PASS | 62ms elapsed below 10000ms; watchdog_cancels_native_calls=false |
| Terminal receipt | PASS | FINAL, terminal=true, sequence6, reason SRV_BACKING_RESOURCE_IDENTITY_CONFIRMED |
| Persistence | PASS within owner-retrieval provenance | Complete matching original final JSON supplied; photo saved message |
| Overall | **PASS_D06_SRV02_ONLY** | Required case criteria above met |

Fixed texture descriptor: Width=Height=MipLevels=ArraySize=1, Format28 (RGBA8 UNORM), Sample Count1 Quality0, Usage0 DEFAULT, BindFlags8 SHADER_RESOURCE, CPUAccessFlags0, MiscFlags0; no initial data. Requested and returned descriptors each independently compared with these eleven constants.

Fixed SRV descriptor: Format28, ViewDimension4 TEXTURE2D, MostDetailedMip0, MipLevels1. Requested and returned descriptors independently compared, not merely relying on match booleans.

`src/probe.cpp:67` calls GetResource once with owned nonnull output storage. GetResource returns void; no GetResource HRESULT appears in the closed schema or receipt. `probe.cpp:74` and `:82` query __uuidof(IUnknown), require S_OK and nonnull outputs; `:89` compares canonical pointer identities. Scoped com_ptr cleanup releases the two temporary QI references before returned resource, then SRV, texture, context and device. One-call cardinality is established by pinned source and policy, not a separate GPU/API trace or runtime counter. Receipt booleans corroborate the path, not exact hardware trace counts.

Memory before: 4,931,584 bytes; after scoped release: 9,887,744 bytes; limit1,073,741,824 bytes. Headroom 1,068,810,240 bytes; growth 4,956,160 bytes (4.72656250 MiB). This is sampled app usage, not peak memory, exact GPU allocation size or leak freedom.

Expected normal checkpoint sequence: STARTED1, BEFORE_CREATE_DEVICE2, BEFORE_CREATE_TEXTURE3, BEFORE_CREATE_SRV4, BEFORE_GET_RESOURCE5, FINAL6. Final sequence and last_durable_checkpoint_stage=BEFORE_GET_RESOURCE agree. Earlier checkpoint files were replaced and were not supplied; their individual historical bytes cannot be independently replayed.

`src/report.cpp` uses current-run UUID filename under LocalState/NativeCapabilityReceipts, 128KiB cap, 100ms lock acquisition, same-path temporary write, flush, close and write-through replacement. Current receipt is smaller than the cap. receipt_persistence_result=VERIFY_BY_RETRIEVAL correctly avoids predicting its own future write. Retrieved complete terminal bytes and photo saved message satisfy this run's persistence criterion; they do not prove power-loss durability or historical checkpoint recovery. Filesystem/driver calls have no guaranteed hard cancellation bound; watchdog cannot cancel a blocked native GPU call.

## Verdict rules

PASS requires all identity/schema/hash, descriptor, S_OK/nonnull, hardware-only, canonical identity, release-marker, memory/deadline, run/photo and final retrieval criteria. FAILED would cover independently established hash/policy mismatch, bad HRESULT/null output, descriptor or identity mismatch, software fallback or memory breach. BLOCKED would cover missing required artifact/schema/build evidence or an unavailable prerequisite. INCONCLUSIVE would cover unresolved attribution, contradictory evidence, timeout or nonterminal/inaccessible final evidence. None of these non-PASS conditions is present for this narrowly scoped supplied run.

## Provenance and telemetry limits

Series X origin, installation and retrieval are owner-attested. Photo/JSON are not signed hardware attestations; hashes prove consistency and subsequent preservation, not unforgeable remote execution. Application UUIDs are not OS process IDs, device IDs or verified hardware identifiers. Receipt identity is application-generated under the reviewed runtime identity check; full installed inventory remains unobserved here.

UTC `2026-10-18T00:37:35.918Z`, host file mtimes and camera clock are unverified. No ordering is inferred across clocks; correlation uses exact run ID. Runtime API flags and release markers are app telemetry supported by source, not an external debugger/reference-count trace. This successful single run does not validate failure handling, crash recovery, long-duration stability, leak freedom, peak memory, hardware stress or all D06 capabilities.

Still untested: texel initialization/content reads, pipeline resource binding/sampling, shader compilation/execution, render-target operations, drawing, clearing, copying, map/readback, app rendering/presentation, OpenGL, LWJGL, Java/JNI, audio, input, lifecycle and Minecraft. The platform dialog is supporting visual evidence, not application rendering proof.

## Next smallest experiment - proposal only

Propose D06-SRV03: query the existing SRV's creating device once with ID3D11DeviceChild::GetDevice, require nonnull, and compare canonical IUnknown identity with the original device using two S_OK/non-null QIs. GetDevice is void (no HRESULT); its returned reference is owned and must be released, along with temporary identities, before normal resource cleanup. This tests device association without new GPU allocations, binding, texel access, shaders or rendering. Microsoft documents the returned-device and reference ownership in [ID3D11DeviceChild::GetDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicechild-getdevice).

Separate approvals required: source/unsigned build first, then signing, installation-only update, one launch, receipt retrieval, formal acceptance and cleanup. No follow-up experiment implemented here.

## Reproduction and output

HARDWARE-VERIFICATION.json records independent evidence hashes, six role checks and memory calculations. SIGNED-PAYLOAD-VERIFICATION.json records archive checks. The retained verify_hardware_evidence.py and verify_signed_payload.py are offline Python verification only; running them does not execute diagnostic binaries or connect to Xbox. Original evidence remains in its supplied locations unchanged.
