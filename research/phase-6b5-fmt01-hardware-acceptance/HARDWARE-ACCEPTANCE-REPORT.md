# Phase 6B.5 — D06-FMT01 Xbox hardware acceptance

**PASS — D06-FMT01 RGBA8 support query only.** Review2026-10-17,
America/Chicago. All formal case acceptance checks pass against the supplied original
receipt, matching photograph and independently pinned0.2.1.0 package. No signing,
installation, update, launch, console access or application/source change occurred.

## Preserved evidence and provenance

Original receipt: `C:\Users\arinze\Desktop\D06-FMT01-D10A4D4B-45B4-4E67-972F-5B7A13675204.json`.
Receipt SHA256 independently recomputed and matched the owner pin:
**453d84192d19a698513513742468dae8509c74973ecd9645fe08266cb1184893** (2735 bytes).
Original photograph: `C:\Users\arinze\AppData\Local\Temp\codex-clipboard-bc68cd2c-bddb-42f5-a0a8-2c7b83f911be.png`.
Photo SHA256: **9a4c59da1a878a699aa9936081bd69cf5e21214923ae529ce7c59a919abafa68** (2239950 bytes).
Byte-identical copies, with originals untouched, are under:
`C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5-fmt01-hardware-acceptance\originals`.
Neither image nor JSON was edited. No legible unrelated personal/account/network
identifier appears in the diagnostic display. Original copies remain outside Git.

HARDWARE-VERIFICATION.json records every independent payload comparison and key
assertion. verify_hardware_receipt.py performs only local byte/schema/oracle checks;
it never loads the diagnostic executable or accesses a device. It uses the reviewed
offline receipt validator whose source is checked against the pinned Git commit.

Xbox Series X origin/retrieval are owner-attested, supported by the photograph;
this is not cryptographically attested device telemetry. The receipt itself is unsigned.
Source/build identity is established by independently hashing the pinned APPX members,
not by trusting receipt hashes alone. No Portal package listing, exact PackageFullName,
console classification, remote file size/mtime listing or OS build was collected anew.
The owner-supplied photo has an exact run ID but no visible capture time.

## Identity, terminal sequence and persistence

| Field | Verified evidence |
|---|---|
| Schema | legacyforge-native-capability-receipt-v2; validated against schema bytes independently hashed from approved unsigned APPX |
| Case | D06-FMT01 |
| Source | bbe3a42c422e4328d5f98c07a9370fa948d0cbbf |
| Build |20261017-180047-9ad3700d; compiledSourceCommit and sourceCommit match packaged native-inputs |
| Production reference | d1453434ceefe73bef5aff497194e09f39dde7e1 |
| Frozen D00 source |553c6554f40f1372b0ea09f6badbbb98e133a9ab |
| Frozen HW01 source | a3f72874241914f6048d4ca9ec4fc0edc978625d |
| Package | AlgorHome.LegacyForge.NativeDiagnostics / CN=LegacyForgeDiagnostics /0.2.1.0 /x64 /application Id App |
| Expected identity | true; pinned manifest/source guard consistent |
| Run UUID | D10A4D4B-45B4-4E67-972F-5B7A13675204; exact receipt filename and photo match |
| Process UUID | F55B2698-AF7B-4D48-A176-9B8DDCC6AA28; valid and distinct from run UUID |
| Terminal | PASS / FINAL /true |
| Reason | RGBA8_REQUIRED_FORMAT_SUPPORT_CONFIRMED |
| Sequence/checkpoint |4 /BEFORE_FORMAT_QUERY; consistent with STARTED1 -> BEFORE_CREATE_DEVICE2 -> BEFORE_FORMAT_QUERY3 -> FINAL4 |
| Elapsed/deadline |63ms /10000ms; within policy |
| Recorded UTC |2026-10-17T23:15:01.858Z |
| Chicago conversion |2026-10-17 18:15:01.858 CDT; conversion only, not clock verification |
| Persistence | Original final file retrieved; photo says saved; receipt marks VERIFY_BY_RETRIEVAL |

Freshness is established within this evidence set by the new FMT01 case/run UUID,
0.2.1.0/source/build binding and matching photo, not by presuming a trustworthy console
clock. It cannot be mistaken for stale0.2.0.0 HW01 LocalState evidence. The final sequence
is consistent with the reviewed writer; earlier physical checkpoint versions were not
provided because the per-run file is replaced. Historical flushes are not independently
reconstructed. Original retrieval proves this final receipt exists, not power-loss durability.
No persistence-error field/result or timing contradiction is present in the supplied final
record; remote file listing, intermediate .tmp/checkpoint history and clock synchronization
remain unverified. These are provenance limits, not unmet case acceptance criteria.

## Six independently verified payload hashes

Approved unsigned APPX:
`C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-180047-9ad3700d\NativeCapabilities.unsigned.appx`.
Fresh archive SHA256: `24dc6835408f9a5d38d1ab56ec82dfd550cf0dc183e495defa836299d77dd03d`.
Signed archive also rehashed: `ae19e5ff93438bcf8a3c9e0d42ad0323908ee83d95231cba9dcd9a319fd5d8ef`.
Each member below was hashed directly from **unsigned archive bytes**. All six match the
pinned build evidence, receipt and signed payload, independently of receipt assertions.

| Packaged member | Independently calculated SHA256 | Match |
|---|---|---|
| NativeCapabilities.exe | `eda70661b4f0ec6b7df6e08b81c8e42f7ee2f6f11acc8f3c3be69a5872f43de1` | PASS |
| AppxManifest.xml | `593fbda9d0dce1ac6b6f12a96e187d5b1c2d0d4aaced9accdadb7cf806807fd0` | PASS |
| native-inputs.json | `5cb62bbacce8b7000099f9432c285bbb71b8b3e26fd50876878f1db1a89cc21a` | PASS |
| profiles/D06-FMT01.json | `57f849c631ba5fd2de08e6d6eda593eccd81f7cba485212b99f7665b86f0a845` | PASS |
| contracts/native-receipt.schema.json | `3373265fb3aa787a375e4edc1da54e4807793bf4151d645519d9c45b5cdbb6b7` | PASS |
| native-inventory.json | `37cc66fcd8abd77fce39b6d488ac822e196ced3bf91cb1a7835ec90976d1f1b6` | PASS |

## Native observations and exact support decoding

Hardware requested via the accepted one-attempt D3D11 path; requested driver value1,
BGRA_SUPPORT creation flags32, no software fallback. Creation HRESULT S_OK0x00000000,
nonnull device and immediate context, selected/requested feature level11_0/45056.
GetAdapter and GetDesc1 both returned S_OK; adapter flags0, SOFTWARE flag false.
This establishes the case's API-reported hardware classification, not an independent
physical GPU identity or certification of every hardware API.

Query attempted=true; exact DXGI_FORMAT_R8G8B8A8_UNORM/value28; HRESULT S_OK0x00000000
(signed0); format_support_valid=true. Raw872346611 = **0x33FEF3F3**.
No reserved bit31. Required mask **0x00004220**; raw & required = required.

| Flag | Bit | Independently decoded | Receipt |
|---|---|---|---|
| TEXTURE2D |0x00000020 | present |true /MATCH |
| SHADER_SAMPLE |0x00000200 | present |true /MATCH |
| RENDER_TARGET |0x00004000 | present |true /MATCH |
| MIP (optional) |0x00001000 | present |true /MATCH |

Other bits are retained in the raw mask; this case does not certify their corresponding
operations. A support bit is a driver-reported capability, not a successful resource,
shader or rendering operation. An unsuccessful HRESULT or invalid output would not
have been interpreted as zero support; this receipt is an actual valid S_OK response.

Cleanup: test_resources_released=true, consistent with pinned scoped COM references.
Before usage4,931,584 bytes, limit1,073,741,824 bytes, headroom1,068,810,240 bytes
(>=256MiB). After release9,904,128 bytes; observed growth4,972,544 bytes (~4.74MiB),
within64MiB allowance. Memory observations available before/after. These observations
do not prove every driver allocation was released, absence of leaks, peak usage,
repeated-run stability, memory pressure behavior or blocked-call cancellation.

## Separate acceptance results

| Evidence field | Result | Practical limit |
|---|---|---|
| Installed package identity | MATCH_SUPPORTED | Owner context + receipt identity and pinned runtime guard; no new Portal registration log/full-name/classification capture |
| Activation | PASS | Matching run produced terminal native receipt and visible platform dialog; launch trigger not independently reconstructed |
| Platform dialog visibility | PASS | Photo shows FMT01/version0.2.1.0/PASS/reason/S_OK/11_0/saved message and exact run ID; mask/query HRESULT are verified from JSON, not displayed in photo |
| Hardware creation/classification | PASS | Correct hardware request, S_OK device/context, level11_0, SOFTWARE false |
| RGBA8 format support query | PASS | S_OK, exact format28, valid mask, all three required support bits |
| Scoped cleanup/resource policy | PASS | Source-bound release marker; observed memory and deadline within policy, with limits above |
| Final receipt persistence | PASS | Original retrieved bytes verified, matching new FMT01 run and saved UI message |
| Source/build/payload binding | PASS | Schema, IDs, sequence and six independent archive-member hashes |
| Overall | **PASS_D06_FMT01_ONLY** | No broader graphics/runtime certification |

FAILED criteria would include missing required bits in a valid S_OK mask, non-policy native
errors, software adapter/output mismatch, exception or memory-growth breach. None occurred.
BLOCKED criteria would include unavailable prerequisite/API/policy/classification, memory
headroom/receipt prerequisites or missing original evidence. None block this case review.
INCONCLUSIVE criteria would include timeout/late completion, malformed/nonterminal/stale
receipt, invalid mask, photo/run mismatch, unresolved payload/source discrepancy or
inaccessible final persistence. None occurred. Provenance limits remain explicitly recorded.

All84 prior source/artifact/evidence files frozen by the signing review were rehashed and
unchanged. No changes to accepted D00/HW01 packages/reports/photos, production LegacyForge,
source checkout, certificates/trust, installed applications, LocalState or console settings.
Prior Windows signing trust finding remains historical: CMS/APPX integrity PASS;
SignTool /pa CERT_E_UNTRUSTEDROOT. This review did not re-sign or change trust.

**Not tested:** actual texture/buffer or graphics-view creation, shader execution,
app rendering, presentation, readback, OpenGL, LWJGL, Java/JNI or Minecraft. Platform
MessageDialog appearance does not certify an app-owned graphics pipeline. Audio,
input, lifecycle stress and all-D06 certification remain outside this case.

## Next smallest separately gated graphics experiment

Propose **D06-RES01a — single RGBA8 texture creation/release**, a deliberately smaller
precursor to the matrix's multi-resource/readback D06-RES01, not its full implementation.
Use the established hardware-only device path, then one CreateTexture2D call:1x1 RGBA8,
one mip, array1, sample count1/quality0, D3D11_USAGE_DEFAULT, SHADER_RESOURCE bind flag,
CPUAccessFlags0, MiscFlags0, no initial data. Require S_OK and a nonnull texture; inspect
GetDesc against the fixed descriptor, release references and record memory/receipt results.
The nominal texel payload is4bytes; actual driver allocation overhead is not bounded to4bytes.
No reads of uninitialized contents, resource views, shaders, draw/clear/copy/map/readback,
swapchain, presentation or retry loop. A null output pointer with S_FALSE would only validate
parameters; it must not be claimed as successful texture allocation.

Microsoft references:
[CreateTexture2D](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createtexture2d),
[D3D11_TEXTURE2D_DESC](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ns-d3d11-d3d11_texture2d_desc).
This is a proposal only. Source/build, signing, installation, one launch, scoped retrieval
and cleanup each require their own explicit approval. No next experiment was implemented.
