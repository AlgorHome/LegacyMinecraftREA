# D06-RES01a hardware acceptance plan — separate approvals required

Current state: **NOT EXECUTED**. Source `4457142ff1fd9e01371eb446612c70162ce93357`;
build 20261017-183031-15ba7835; unsigned artifact `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-183031-15ba7835\NativeCapabilities.unsigned.appx`;
SHA256 **526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8**. This document authorizes no signing or device action.

## Gate1 — local signing only

Separate explicit approval naming exact unsigned source/hash and nominated diagnostic
certificate. Rehash first, confirm certificate subject/publisher/validity/EKU/key usage/
nonexportable key availability, preserve original and sign exactly one fresh copy with SHA256.
Verify CMS, APPX digest, every original payload byte and blockmap; record signed hash/path.
Report normal chain trust separately, retain any CERT_E_UNTRUSTEDROOT; no automatic trust
change, dependency install or repair. Signing approval does not authorize installation.

## Gate2 — owner installation-only update

Separate explicit approval naming signed hash/path and expected0.2.2.0 identity.
Owner uses existing authenticated Portal; no automatic remote configuration changes.
Confirm exact current NativeDiagnostics0.2.1.0 registration and Not running. This update
replaces that executable/registration; LocalState may retain stale HW01/FMT01 receipts.
If independent installed0.2.1.0 reproducibility is required, stop for a distinct-package
proposal rather than updating. Preserve all archived packages, receipts/photos/reports.

Rehash exact signed copy immediately before submission. Upload only that APPX, leaving
dependencies empty if existing Microsoft.VCLibs.140.00 x64 UWP satisfies the unchanged
manifest. Do not upload UWPDesktop/fallback/framework/certificates unnecessarily. Disable
auto-launch; if it cannot be guaranteed disabled, stop before submission. One attempt only.

Record final status/HRESULT and registered Name AlgorHome.LegacyForge.NativeDiagnostics,
Publisher CN=LegacyForgeDiagnostics, Version0.2.2.0, x64, App classification and exact full
name if displayed. Classification/full-name cannot be derived by inventing a suffix from
another package. Stop on any certificate/dependency/registration/identity/version error;
no retry, repair, uninstall, data clearance, framework or trust change. No launch yet.

## Gate3 — one owner-operated RES01a launch

Separate approval for exactly one activation of the verified registered0.2.2.0 artifact.
Use empty launch arguments, or exact D06-RES01a if supported; no alternate cases.
One-shot probe starts automatically. Observe at most30s, no repeated launch or interaction
needed.10s watchdog is an observation/terminal-decision deadline; cannot cancel driver,
GetDesc, COM-release or file calls. Do not infer cleanup after hang/crash.

Record activation, platform UI visibility, overall reason, device HRESULT/feature, saved/
pending receipt status and exact run UUID. Photograph only diagnostic display, excluding
personal/device/network data. Texture HRESULT/descriptors are verified in downloaded JSON,
not assumed from generic device-HRESULT UI. A dialog is not app rendering/presentation.
On timeout/crash/error stop, preserve evidence, no automatic relaunch or repair.
Manual termination/cleanup is not implicitly approved by this plan.

## Gate4 — scoped read-only receipt retrieval and formal review

Separate approval. Identify exact0.2.2.0 package via owner read-only inventory, then access
only its LocalAppData/LocalState/NativeCapabilityReceipts. Record filenames/timestamps/sizes;
retrieve fresh D06-RES01a-<run UUID>.json and same-run .json.tmp if present. No remote
writes/deletes, unrelated apps, accounts, broad logs or credentials. Preserve original bytes
and calculate local SHA256; sanitize separate copies only when necessary.

Use pinned RECEIPT-SCHEMA.json (schema v3) plus tools/receipt_contract.py semantic oracle.
Recompute six role hashes directly from this pinned unsigned APPX (then establish signed
payload equality at Gate1); never use receipt-provided hashes as independent expected values.

| Role /member | Pinned SHA256 |
|---|---|
| executable_sha256 /NativeCapabilities.exe | `cb08435285c6dad6f0eba7b0be955f4243d52d29bf575cacfcef4aa6facfbd67` |
| manifest_sha256 /AppxManifest.xml | `82f0b634c4343a5272af9f873d1accc528970407da0dce1913deeb1704ccc3c0` |
| build_inputs_sha256 /native-inputs.json | `d7fcb2e1ac04e3013a37dcca473ea24e402ce165de1f7460efbd7924de9b8a1e` |
| policy_sha256 /profiles/D06-RES01a.json | `ec8a12dda98ecfbcaac14ff647c329867d7e386aebcf4d6d0d4e48812348c0e2` |
| schema_sha256 /contracts/native-receipt.schema.json | `cd2ba13e2da44ead0cb3f421d88138596cca6541e86105daed7e892883029180` |
| inventory_sha256 /native-inventory.json | `d5abc15a2bd38f06d749fd371855302b74861eebc8f46ddab0d03e9bdf42fbe4` |

Bind source/build IDs, package/version, production/frozen D00/HW01/FMT01 references and
process/run UUIDs. Expected normal sequence4, last checkpoint BEFORE_CREATE_TEXTURE,
terminal=true/stage FINAL. Correlate filename and photograph with exact fresh run UUID;
old HW01/FMT01 LocalState is not new evidence. UTC/mtime may be supporting chronology,
not trusted hardware/clock provenance. Raw JSON/photo are not hardware-attested signatures.

Required descriptor (both requested and returned): width1, height1, mip_levels1,
array_size1, format28, sample_count1, sample_quality0, usage0, bind_flags8,
cpu_access_flags0, misc_flags0. All11 fields must match exactly; no padding comparison.
No GetDesc HRESULT exists because the API returns void. Pointer validity is a boolean,
not a proof of reading content. Null initial data means undefined texture contents; no
initialization/readback/content validation is authorized or implied by this case.

| Independent result | Evidence to record |
|---|---|
| Registration | Exact package identity/version and owner final installation status; retain missing Portal fields as UNKNOWN |
| Activation /UI | One run observed, photo or error; platform UI absent does not by itself prove texture failure |
| Hardware/device | Requested HARDWARE1, no fallback, BGRA32, creation S_OK0, level45056, device/context true |
| Adapter classification | GetAdapter/GetDesc1 S_OK, adapter SOFTWARE false |
| Allocation | texture_attempted true, texture_hresult S_OK0, texture_returned true; S_FALSE never counts |
| Descriptor | get_desc_called true, both exact fixed descriptors, descriptors_match true |
| Release/resource policy | texture_reference_released and test_resources_released true, available before/after memory within policy, elapsed<10s |
| Persistence | Retrieved original final bytes and current-run binding, not only UI saved text or .tmp |
| Overall | Apply strict criteria below; no broader graphics/runtime inference |

- **PASS:** All independent fields/bindings above; reason RGBA8_TEXTURE_CREATED_DESCRIPTOR_MATCH,
  correct six hashes/source/build, expected identity, FINAL/terminal/PASS, sequence4;
  no unresolved final persistence error; headroom>=268435456bytes, observed growth<=67108864bytes,
  elapsed<10000ms; original final retrieval/photo/run association. Scoped-reference release is
  not evidence that every driver allocation is freed. No peak/leak/repetition guarantee.
- **FAILED:** S_OK with null texture, S_FALSE/non-S_OK success, ordinary negative HRESULT,
  descriptor mismatch, software adapter/wrong device outputs, native exception or excess
  observed memory growth. An error-only or crash receipt cannot establish cleanup.
- **BLOCKED:** Required environment/API/policy/memory/classification/receipt prerequisite
  unavailable or missing approval. E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED
  map to BLOCKED for device/texture API. Missing before memory or<256MiB headroom also blocks.
- **INCONCLUSIVE:** Timeout/late return/owner close/observer failure, missing/unreadable/
  temporary/nonterminal receipt or unresolved provenance/schema/hash mismatch. Do not claim
  PASS from photo alone. Observer may save empty details without returned driver results.
- **NOT EXECUTED:** No authorized run/original receipt. Build/synthetic-test success never
  changes hardware status to PASS. RUNNING is only an intermediate checkpoint.

Writer uses VERIFY_BY_RETRIEVAL because bytes cannot predict their own future flush.
Original retrieval proves this final file exists, not future power-loss durability. Missing
final file: persistence BLOCKED, overall INCONCLUSIVE; retain .tmp/checkpoints, no retry.
Startup hash/writer and underlying OS I/O calls are not hard-time-bounded; no cancellation claim.

## Gate5 — cleanup

Separate approval after originals/reports are preserved. Name exact diagnostic-only operation;
no implicit uninstall, downgrade, LocalState clearance, framework removal, certificate change
or touching accepted D00/production LegacyForge. Stop after each stage and report separately.

Even future RES01a PASS establishes only one allocation/GetDesc/release path. Texture content,
initialization, SRV/RTV, rendering, presentation, OpenGL, LWJGL, Java/JNI and Minecraft remain
untested. No next graphics test is included in this authorization.
