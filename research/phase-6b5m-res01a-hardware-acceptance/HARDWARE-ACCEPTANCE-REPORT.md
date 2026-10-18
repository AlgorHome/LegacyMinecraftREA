# Phase6B.5m — D06-RES01a final Xbox hardware acceptance

**PASS — D06-RES01a only.** All case requirements are met by the original terminal
receipt, exact-run original photograph and independently pinned0.2.2.0 payload evidence.
No signing, rebuild, installation, launch, device-data retrieval or application-state change
occurred in this local verification review. Production and accepted D00/HW01/FMT01 evidence
remain untouched. This is not graphics rendering or Minecraft acceptance.

## Original evidence preserved unchanged

Receipt `C:\Users\arinze\Desktop\D06-RES01a-7A897A91-DE14-4A33-82AE-4737F5575C6D.json`; SHA256 **10081860917f805a82f366d0e2e9ddccb11a07deb330e16643bda68e55227fe9** matches the independent owner
pin10081860917f805a82f366d0e2e9ddccb11a07deb330e16643bda68e55227fe9.
Original JPEG `C:\Users\arinze\Downloads\IMG_5563.JPG`; SHA256 **d62d1121b060179d27790454fc9165e26cc6fe4abfba7ab9c08c0723e740aee8**,
1623686 bytes. Photo was visually inspected locally. Both originals copied byte-for-byte to
`C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5m-res01a-hardware-acceptance\originals`.
No original was edited, resaved, redacted or overwritten. No legible unrelated personal/network
identifier appears in the supplied diagnostic display. Originals remain outside Git.

HARDWARE-VERIFICATION.json contains the per-role comparisons, full native observations,
photo binding and numeric resource checks. The prepared offline receipt verifier checked
pinned schema v3/semantic oracle without native-target loading; visual association was
then independently established from the original JPEG. Its intermediate automated output
intentionally leaves photo association pending; this final manual review resolves it.

## Source/build, identity, run and terminal checks — PASS

| Property | Verified |
|---|---|
| Schema | legacyforge-native-capability-receipt-v3; validated against approved package schema, not a receipt-supplied schema |
| Case/version | D06-RES01a /0.2.2.0 |
| Source |4457142ff1fd9e01371eb446612c70162ce93357 |
| Build |20261017-183031-15ba7835; matches packaged sourceCommit/compiledSourceCommit/buildId |
| Production reference | d1453434ceefe73bef5aff497194e09f39dde7e1 |
| D00 reference |553c6554f40f1372b0ea09f6badbbb98e133a9ab |
| HW01 reference | a3f72874241914f6048d4ca9ec4fc0edc978625d |
| FMT01 reference | bbe3a42c422e4328d5f98c07a9370fa948d0cbbf |
| Package identity | AlgorHome.LegacyForge.NativeDiagnostics /CN=LegacyForgeDiagnostics /x64 /application Id App; expected_package_identity=true |
| Run UUID |7A897A91-DE14-4A33-82AE-4737F5575C6D; exact filename/JSON/photo match |
| Process UUID |12DB5ECA-0A71-4310-BB19-E8E1B64FA742; valid and distinct from run |
| Terminal result | PASS /FINAL /terminal=true |
| Reason | RGBA8_TEXTURE_CREATED_DESCRIPTOR_MATCH |
| Sequence/checkpoint |4 /BEFORE_CREATE_TEXTURE; consistent with STARTED1 -> BEFORE_CREATE_DEVICE2 -> BEFORE_CREATE_TEXTURE3 -> FINAL4 |
| Timing |62ms elapsed,10000ms deadline; below deadline |
| Recorded UTC |2026-10-17T23:43:07.619Z; Chicago18:43:07.619 CDT, conversion only |
| Java/gameplay/all-D06 |false /false /false |

UUID syntax/identity, duplicate-key rejection, root/field restrictions, returned HRESULT
signed values and complete descriptor semantics were checked. Original final retrieval
establishes this run's saved receipt; receipt_persistence_result=VERIFY_BY_RETRIEVAL is
not a self-prediction of future storage. Fresh case/version/run/build distinguish retained
FMT01/HW01 LocalState. Earlier physical checkpoint versions were not provided and are not
reconstructed merely from sequence4. Console clock synchronization, remote mtime listing,
PackageFullName, console classification and current OS build were not collected anew.

## Independent package/payload evidence — PASS

Unsigned APPX was rehashed against526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8.
Signed APPX was rehashed against ead7016c94e551fac43e2b622b323354bfa4506fe507f44bf5e98f112b8f0c3f.
Exact paths are retained in the Phase6B.5i BUILD-EVIDENCE.json and Phase6B.5j
SIGNING-VERIFICATION.json. Each member below was freshly hashed directly from unsigned
ZIP bytes, then matched against independently pinned build evidence and receipt values.
Signed payload bytes match the original unsigned members.

| Member | Independently computed SHA256 | Match |
|---|---|---|
| NativeCapabilities.exe | `cb08435285c6dad6f0eba7b0be955f4243d52d29bf575cacfcef4aa6facfbd67` | PASS |
| AppxManifest.xml | `82f0b634c4343a5272af9f873d1accc528970407da0dce1913deeb1704ccc3c0` | PASS |
| native-inputs.json | `d7fcb2e1ac04e3013a37dcca473ea24e402ce165de1f7460efbd7924de9b8a1e` | PASS |
| profiles/D06-RES01a.json | `ec8a12dda98ecfbcaac14ff647c329867d7e386aebcf4d6d0d4e48812348c0e2` | PASS |
| contracts/native-receipt.schema.json | `cd2ba13e2da44ead0cb3f421d88138596cca6541e86105daed7e892883029180` | PASS |
| native-inventory.json | `d5abc15a2bd38f06d749fd371855302b74861eebc8f46ddab0d03e9bdf42fbe4` | PASS |

Full signed payload preservation, beyond the six roles:12 original members except the
expected Content_Types changes are byte-identical, including AppxBlockMap.xml. No removal;
only AppxSignature.p7x and AppxMetadata/CodeIntegrity.cat plus their two content-type
declarations added. ZIP CRC/duplicate-name and11-file blockmap64KiB/whole-file hash/size
checks pass. No signing metadata was modified. Earlier signature-integrity evidence remains
pinned by the unchanged signed archive hash; this review performed no re-sign/trust change.
Normal Windows chain finding remains CERT_E_UNTRUSTEDROOT, separately from package integrity.

## Device, texture and every descriptor field — PASS

Requested driver HARDWARE1; creation flags32/BGRA_SUPPORT; fallback=false. Device creation
S_OK0x00000000, signed0; selected/requested feature11_0/45056; device/context returned=true.
Adapter GetAdapter and GetDesc1 both S_OK; adapter_flags0, adapter_software_flag=false.
This meets API-reported hardware classification, not independent GPU-vendor identity.

Texture attempted=true; CreateTexture2D HRESULT S_OK0x00000000/signed0;
texture_returned=true. Nonnull output pointer supplied, initial_data_supplied=false.
S_FALSE/parameter-validation-only result is explicitly excluded. GetDesc called=true;
all11 fields compared independently with the fixed approved descriptor/policy:

| Field | Required | Requested | Returned |
|---|---|---|---|
| width | 1 | 1 | 1 |
| height | 1 | 1 | 1 |
| mip_levels | 1 | 1 | 1 |
| array_size | 1 | 1 | 1 |
| format | 28 | 28 | 28 |
| sample_count | 1 | 1 | 1 |
| sample_quality | 0 | 0 | 0 |
| usage | 0 | 0 | 0 |
| bind_flags | 8 | 8 | 8 |
| cpu_access_flags | 0 | 0 | 0 |
| misc_flags | 0 | 0 | 0 |

Format28 is DXGI_FORMAT_R8G8B8A8_UNORM; usage0 DEFAULT; bind_flags8 SHADER_RESOURCE.
Descriptors match independently, not merely because descriptors_match=true. GetDesc is
void: no texture-GetDesc HRESULT is fabricated. The existing get_desc_hresult field is
adapter GetDesc1, not texture GetDesc. Only metadata was inspected; undefined texel content
was neither initialized nor read. No shader-resource view or shader work was performed.

## Release, memory, deadline and persistence — PASS

texture_reference_released=true and test_resources_released=true; pinned source has scoped
texture release before context/device release and handles unexpected nonnull failure output.
Before usage4,927,488 bytes; limit1,073,741,824; available=true; headroom1,068,814,336
(>=268,435,456). After-release usage9,994,240, same available limit. Observed growth
5,066,752 bytes (~4.83MiB), within67,108,864 allowance. Elapsed62ms<10000ms.
No deadline/late-PASS/observer-won indication appears in this final receipt.

These are source-bound assertions/sampled observations, not proof every driver allocation
was freed, absence of leaks, peak usage or repeated-run stability. Nominal texel data4bytes
does not limit real driver allocation. Watchdog cannot cancel blocked GPU/GetDesc/release/
file calls. No process/thread termination or stress testing is inferred.

Photo visibly shows Native Diagnostics D06-RES01a/package0.2.2.0/PASS, exact reason,
hardware request/no fallback, device HRESULT0, feature0xB000, saved-receipt message and exact
run UUID7A897A91-DE14-4A33-82AE-4737F5575C6D. Texture HRESULT/pointer/descriptors are checked
from JSON, not claimed visible in this photo. The original terminal file plus that exact-run
saved message satisfies retrieved persistence; no future power-loss durability guarantee.

## Separate evidence fields and formal determination

| Field | Result | Scope |
|---|---|---|
| Registration identity | MATCH_SUPPORTED | Pinned runtime identity guard and owner context; no fresh Portal full-name/classification log |
| Activation | PASS | Exact-run terminal native receipt and visible diagnostic dialog |
| Platform UI visibility | PASS | Original photo inspected; not app-owned graphics presentation |
| Hardware creation/classification | PASS | S_OK/device/context/11_0/non-software adapter, no fallback |
| Texture allocation | PASS | S_OK and nonnull texture, not parameter validation |
| Descriptor inspection | PASS | All11 requested/returned fields exactly match fixed policy |
| Scoped release/memory/deadline | PASS | Both release flags, sampled memory and elapsed policy checks |
| Terminal receipt persistence | PASS | Original file hash verified and matching photo/run saved message |
| Source/build/six hashes | PASS | Independently pinned package members and valid receipt contract |
| Exact photo/run association | PASS | Original IMG_5563.JPG matches filename/JSON UUID |
| Overall | **PASS_D06_RES01A_ONLY** | Current narrow allocation/descriptor/release case |

No FAILED criterion is present: no failed HRESULT/null texture/descriptor mismatch/software
fallback/memory-growth breach. No BLOCKED prerequisite remains for this acceptance review.
No INCONCLUSIVE criterion remains: original final receipt/schema/hash/identity/sequence and
photo/run attribution are resolved. Provenance/telemetry limits below remain practical limits.

## Provenance and telemetry limits

- Owner attests Series X origin and retrieval; JSON/photo are not signed or hardware-attested.
  Pinned payload hashes establish artifact consistency, not an unforgeable remote execution proof.
- Console UTC, remote listing timestamps and camera capture clock/metadata are not independently
  verified. Exact-run matching is the association basis. No EXIF GPS/device identifiers collected.
- Only retrieved final bytes are provided; prior overwritten checkpoints and crash/failure paths
  are not experimentally validated by this PASS.
- Process UUID is an application-generated instance identifier, not a hardware attestation or
  proof of process isolation. Pointer validity is boolean; no pointer addresses were collected.
- Scoped reference release/memory sampling are not proof of complete driver cleanup/leak freedom.
- App dialog visibility is not app-owned rendering/presentation or an input/audio/lifecycle test.

All107 original frozen pins, plus total118 prior artifact/evidence files from the signing
review, were rehashed unchanged. Source checkout remains clean at the approved commit.
No accepted D00/HW01/FMT01 source/artifact/receipt/photo/report changed.

**Still untested:** texture initialization/content correctness, SRV/RTV creation, shaders,
draw/clear/copy/map/readback, app rendering/presentation, OpenGL, LWJGL, Java/JNI and Minecraft.
This PASS does not establish those capabilities or certify allD06.

## Next smallest independently gated experiment — proposal only

Propose D06-SRV01: one shader-resource-view creation on the same fixed1x1 RGBA8 texture,
then view GetDesc/release. Explicit view descriptor: RGBA8, TEXTURE2D, MostDetailedMip0,
MipLevels1; one CreateShaderResourceView with nonnull output storage, S_OK+nonnull view
required; compare returned active descriptor fields. Release view before texture/device.
No binding to a pipeline, texel reads/initialization, shader compilation/execution, draw,
render target, swapchain or presentation. This adds only view creation/metadata inspection
and does not claim sampling/rendering success.

Microsoft API basis:
[CreateShaderResourceView](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createshaderresourceview),
[view GetDesc](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11shaderresourceview-getdesc).
Requires separate source/build approval first, then signing, installation, one launch,
scoped receipt retrieval and cleanup approvals. No next experiment has been implemented.
