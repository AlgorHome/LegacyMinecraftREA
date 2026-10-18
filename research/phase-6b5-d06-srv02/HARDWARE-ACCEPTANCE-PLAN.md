# D06-SRV02 independently gated hardware plan

**PREPARATION ONLY — hardware NOT EXECUTED.** Source `c81d0f48286513f7a7579a1d2d786cca4f5e60e2`;
build 20261017-192156-1c3f66cf; unsigned APPX `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-192156-1c3f66cf\NativeCapabilities.unsigned.appx`;
SHA256 **88cde899358b6eaade1658802831c5a914b8e637cf1466321b233fa8a2788c31**. No stage below is authorized by source/build approval.

## Gate1 — local signing/integrity only

Separate explicit approval naming source/unsigned hash and nominated certificate. Rehash,
check certificate public properties/nonexportable-key availability; preserve unsigned original,
sign exactly1 fresh copy with SHA256. Verify CMS, APPX digest/payload/blockmap and expected
metadata; record signed hash/path/signer and ordinary chain trust separately. Do not repair/
import trust, install frameworks or assume signing approval authorizes installation.

## Gate2 — owner installation-only update

Separate approval naming signed hash/path. Owner's existing authenticated Portal only;
no settings change. Confirm exact current NativeDiagnostics0.2.3.0 and Not running.
Version0.2.4.0 replaces that registration, may retain old SRV01/RES01a/FMT01/HW01 receipts.
If accepted installed SRV01 must remain independently runnable, stop for a distinct package
identity/build proposal first. Preserve LocalState/receipts and archived accepted packages.

Rehash signed package immediately before submission. Upload only approved APPX; leave
framework uploads empty if existing Microsoft.VCLibs.140.00 x64 UWP satisfies unchanged
manifest. No UWPDesktop/fallback/certificate/PFX/extra package upload. Disable auto-launch;
if no-launch cannot be guaranteed, STOP before submitting. Exactly1 attempt, wait for final
status. Verify AlgorHome.LegacyForge.NativeDiagnostics /CN=LegacyForgeDiagnostics /0.2.4.0 /
x64 /App classification; record actual PackageFullName if displayed, no inferred suffix.
Stop on signature/dependency/registration/identity/version failure or ambiguous outcome;
no retry, repair, uninstall, storage clearance or trust/configuration change. No launch.

## Gate3 — one owner-operated Xbox launch

Separate explicit approval for1 D06-SRV02 activation. Confirm exact registered/signed
artifact and no unexpected launch. Empty/exact-case argument only. Observe<=30s;10s
case deadline cannot cancel GPU/GetResource/QueryInterface/Release/file calls. No retry.
Record activation/status/reason/device HRESULT/feature/persistence message and exact run
UUID; photograph diagnostic display without unrelated personal data. Getter/QI results
come from JSON, not inferred from generic device-HRESULT UI. No interaction necessary.
On crash/hang/failure stop and preserve observation. No automatic termination/repair/cleanup.

## Gate4 — diagnostic-only read-only original retrieval

Separate explicit approval for retrieval. Identify exact0.2.4.0 package, then inspect only
its LocalAppData/LocalState/NativeCapabilityReceipts. Record filenames/sizes/timestamps;
download fresh D06-SRV02-<run UUID>.json and same-run .json.tmp if present, preserve originals/
photo unchanged and compute local SHA256. No remote edits/deletes, unrelated apps/data,
accounts/credentials or broad logs. Missing Portal path/read-only download: mark UNAVAILABLE,
stop that path; no workaround, permission change or relaunch. Retrieval is not formal acceptance.

## Gate5 — offline formal hardware acceptance

Separate explicit approval for local evidence review. Use pinned receipt v5 and semantic
oracle; independently rehash6 members directly from exact approved unsigned archive, compare
with build pins/receipt; Gate1 establishes signed member preservation. Do not use receipt's
own hashes as independent expected values. Verify exact source/build/version/identity and
all frozen refs; UUIDs valid/distinct, filename/photo match, final persistence and sequence.

| Role /member | Pinned unsigned member SHA256 |
|---|---|
| executable_sha256 /NativeCapabilities.exe | `4e9e8a5563c8b4eaa0aff8d36695c03b29af7a127d5437997b4e579bbdd749b2` |
| manifest_sha256 /AppxManifest.xml | `cb09200058bafb97974ff366231fb4eca0829abc264e5aeb218bc4e4c6140550` |
| build_inputs_sha256 /native-inputs.json | `f6eb65349dd42b8192415b3147405d86093bc84f392180bcfe8199acc60c18d9` |
| policy_sha256 /profiles/D06-SRV02.json | `d81e3edf4de37d1fa699ac6af207f84d429a9391215d1b593e36d314017b4594` |
| schema_sha256 /contracts/native-receipt.schema.json | `4ab9dfbbf345704a846945d1c6609952b937f80949409c91fdf549be1cf71d36` |
| inventory_sha256 /native-inventory.json | `b30d732ac7093e8b54ad188658072de50aa3eb2a6bcabb69115f6dd6c96bcb54` |

Required independent fields:

| Field | Acceptance evidence |
|---|---|
| Registration/activation/UI | Owner final identity/version/status and exact-run image; missing inventory fields UNKNOWN, dialog not app rendering |
| Device/adapter | HARDWARE1/BGRA32/no fallback, S_OK/device/context/11_0, classification S_OK/SOFTWARE false |
| Texture/SRV | S_OK+nonnull and accepted11 texture/4 active SRV descriptors |
| GetResource | get_resource_called true, nonnull output storage and backing_resource_returned true; no getter HRESULT allowed |
| IID queries | identity_interface IID_IUnknown; both attempted, actual HRESULTs S_OK/signed0, both identity outputs nonnull |
| Comparison | identity_comparison_performed and canonical_identity_equal true; no raw addresses, no null/noncanonical comparison |
| Temporary cleanup | temporary_identity_references_released, returned_resource_reference_released, backing_references_released_before_srv true |
| Remaining cleanup | srv_reference_released, srv_released_before_texture, texture_reference_released, test_resources_released true |
| Policy | Before/after samples available, >=256MiB headroom, <=64MiB observed growth, elapsed<10000ms |
| Terminal/persistence | FINAL/terminal true/sequence6, checkpoint BEFORE_GET_RESOURCE, original final bytes retrieved and hashed, matching photo/run |

Fixed texture: width/height/mips/array1, format28, sample1/quality0, usage0, bind8,
CPU/misc0. Fixed SRV: format28/view_dimension4/most_detailed_mip0/mip_levels1.
Normal checkpoint sequence1STARTED/2BEFORE_CREATE_DEVICE/3BEFORE_CREATE_TEXTURE/
4BEFORE_CREATE_SRV/5BEFORE_GET_RESOURCE/6FINAL. UTC/remote mtimes are not trusted clock
attestation. Returned resource/IUnknown pointers remain private; identity comparison boolean
only. GetResource and resource GetDesc are void, no fabricated HRESULTs.

- **PASS:** All fields/source/build/six independent pins and original photo/run/persistence
  criteria pass; reason SRV_BACKING_RESOURCE_IDENTITY_CONFIRMED. This is one narrow backing
  identity test, not hardware attestation or full rendering certification.
- **FAILED:** Null returned resource, either QI non-S_OK/null output, unequal canonical
  identities, bad prerequisite outputs/descriptors, ordinary native error/exception or memory
  growth breach. Two null identity outputs must never compare as successful identity.
- **BLOCKED:** Missing API/policy/classification/memory/receipt prerequisite or missing stage
  approval. Device/texture/SRV E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED
  retain blocking mapping; actual QI failure is case FAILED, not assumed policy unavailability.
- **INCONCLUSIVE:** Deadline/late result/owner close/observer failure; missing/inaccessible/
  temporary/nonterminal/stale/unbound original or unresolved photo/source/hash/persistence
  attribution. Empty timeout details cannot establish resource release. Never relaunch for proof.
- **NOT EXECUTED:** No authorized target evidence. Source/build/synthetic fixtures do not
  establish hardware PASS. RUNNING is intermediate only.

VERIFY_BY_RETRIEVAL intentionally avoids predicting flush success within its own receipt.
Missing final: persistence BLOCKED, overall INCONCLUSIVE; preserve partial originals without
repair/retry. A retrieved final proves that saved file, not future power-loss durability.
Canonical identity is determined using IID_IUnknown, never arbitrary interface pointers.
All acquired references need separate releases even when they refer to the same object.
Markers are owned-reference scope evidence, not direct driver refcount/memory measurements.
Driver/OS calls may block; watchdog cannot cancel. No peak/leak/repetition guarantee.

## Gate6 — optional cleanup

Separate explicit approval after accepted originals/report preserved, naming exact diagnostic-only
operation. No implicit uninstall/downgrade/LocalState clearance/framework/certificate removal or
production/D00/older accepted-evidence change. Stop after every stage and report outcome.

Even future PASS leaves pipeline binding, sampling, texel init/read/content correctness,
shaders, draw/clear/copy/map/readback, rendering/presentation, OpenGL, LWJGL, Java/JNI and
Minecraft untested. No next case or broader sweep included.
