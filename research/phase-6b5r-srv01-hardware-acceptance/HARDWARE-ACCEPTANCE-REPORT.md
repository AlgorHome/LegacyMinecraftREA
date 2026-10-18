# Phase6B.5r — D06-SRV01 final Xbox hardware acceptance

**PASS — D06-SRV01 only.** Review2026-10-17, America/Chicago. All declared case
criteria pass for the supplied original final receipt, exact-run photograph and
independently pinned0.2.3.0 payloads. No target execution, signing/rebuild/install,
console access/data retrieval or application-state change occurred during review.

## Preserved originals and SHA256

Original receipt: `C:\Users\arinze\Desktop\D06-SRV01-DDCAC652-19A4-451E-8AD9-EB191AC45A23.json` (3626 bytes).
SHA256 **5a989a129e49658d42dcc61abc364b8a614feb7a7006ed897394a4c178f51d9b** independently recomputed and matched owner's pin
5a989a129e49658d42dcc61abc364b8a614feb7a7006ed897394a4c178f51d9b.
Original photo: `C:\Users\arinze\Desktop\IMG_5564.JPG` (1462549 bytes).
SHA256 **9dec20778c9add96fb54d18ea84fa4bb2d316b89435ae588fe37ae92eddac8e1** independently computed. No separate owner photo-hash pin
was supplied; original and preserved-copy hashes match each other byte-for-byte.
Both unchanged originals copied to `C:\Users\arinze\Desktop\ReverseLegacyCraft\analysis-local\phase6b5r-srv01-hardware-acceptance\originals`.
No editing/resaving/redaction of originals; private evidence remains outside Git.
No unrelated personal/account/network information is legible in the diagnostic display.

HARDWARE-VERIFICATION.json records the full receipt, independent payload comparisons,
preservation/resource checks and photo association. Analysis imports only the pinned
original offline Python schema/oracle; no native target or graphics DLL loaded. Validator
source hash and all original compiled source hashes match native-inputs.json from the
approved unsigned archive. Duplicate JSON keys, unknown fields and invalid UUID/typed
values are rejected by the pinned v4 contract and semantic oracle.

## Source/build, identity and terminal evidence — PASS

| Field | Independently checked value |
|---|---|
| Receipt schema | legacyforge-native-capability-receipt-v4; approved package schema bytes also match research dossier |
| Case | D06-SRV01 |
| Source | e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8 |
| Build |20261017-185632-1c4c5a9c; packaged sourceCommit/compiledSourceCommit/buildId match |
| Production baseline | d1453434ceefe73bef5aff497194e09f39dde7e1 |
| D00 reference |553c6554f40f1372b0ea09f6badbbb98e133a9ab |
| HW01 reference | a3f72874241914f6048d4ca9ec4fc0edc978625d |
| FMT01 reference | bbe3a42c422e4328d5f98c07a9370fa948d0cbbf |
| RES01a reference |4457142ff1fd9e01371eb446612c70162ce93357 |
| Package metadata | AlgorHome.LegacyForge.NativeDiagnostics /CN=LegacyForgeDiagnostics /0.2.3.0 /x64 /application Id App |
| Expected identity |true, consistent with pinned manifest and runtime identity guard |
| Run UUID | DDCAC652-19A4-451E-8AD9-EB191AC45A23, matches original filename/JSON/photo |
| Process UUID | DB9268D0-C2FA-412C-ACF3-5E1FB4B77B17, valid and distinct from run |
| Status/reason | PASS /RGBA8_SRV_CREATED_DESCRIPTOR_MATCH |
| Stage/terminal/sequence | FINAL /true /5 |
| Last checkpoint | BEFORE_CREATE_SRV |
| Elapsed/deadline |78ms /10000ms |
| Recorded UTC |2026-10-18T00:11:25.203Z |
| Chicago conversion |2026-10-17 19:11:25.203 CDT; conversion only, no clock attestation |
| Java/gameplay/all-D06 flags |false /false /false |

Sequence is consistent with STARTED1 -> BEFORE_CREATE_DEVICE2 -> BEFORE_CREATE_TEXTURE3
-> BEFORE_CREATE_SRV4 -> FINAL5. Earlier overwritten checkpoint bytes are not supplied;
sequence consistency does not independently reconstruct every historical flush. Package
identity is source-bound and owner-correlated; no fresh Portal registration log,
PackageFullName, console classification or OS build was retrieved. Application Id App
is not independent confirmation of the console's App/Game classification field.

## Independent unsigned and signed payload verification — PASS

Unsigned archive SHA256 reverified:
e70fd6c9ef76ff17a06a9ad605c6c88e5eb412240446b6bbfcf17d1b8897c693.
Signed archive SHA256 reverified:
da28a5c22cb27b913b2bf296155c9d9bc5745e37ff3b2af88832f7661e042724.
Paths are pinned in Phase6B.5n BUILD-EVIDENCE.json and Phase6B.5o SIGNING-VERIFICATION.json.
Six required members were freshly hashed **directly from the approved unsigned APPX**,
matched against independently pinned build evidence and receipt, then byte-compared
with signed members. Receipt values were not used as the independent expected hashes.

| Member | Independent SHA256 | Match |
|---|---|---|
| NativeCapabilities.exe | `ae5bf1529880c252d61d53e407dae1a11d3ebc6c1a62e52d41f1945b07b50fe4` | PASS |
| AppxManifest.xml | `459fe8541f08cb06e60636b84b30c3e2268959acf0680034b325dc0e942d3d16` | PASS |
| native-inputs.json | `707abd3ab6bebe12d4c536c923f2a86d155f4d3171d13a6fa5fb2eb4c8c19d4c` | PASS |
| profiles/D06-SRV01.json | `8e174475104f0519a7756d46240ac3a767d05659748486bf55d9267f8ab63542` | PASS |
| contracts/native-receipt.schema.json | `322358b6bb95467165fa97d8f5e48035bd06e9f025b0f109c9ec17300732b228` | PASS |
| native-inventory.json | `53be6683824eeba3b764e9bb7f36fdb523faebbffe82e8f356cc3386f1de5e24` | PASS |

Entire original payload preserved:12 original members other than expected Content_Types
changes byte-identical, including blockmap. No removed member; only AppxSignature.p7x,
AppxMetadata/CodeIntegrity.cat and their two corresponding content-type declarations added.
ZIP CRC/duplicate names pass; all11 blockmap members verified for file size,64KiB block
hashes, optional whole-file hash and local-header size. Existing signing integrity evidence
remains pinned by exact signed archive bytes; no new signing or trust operation performed.
Prior Windows CERT_E_UNTRUSTEDROOT finding remains separate from package integrity.

## Device, texture and view observations — PASS

HARDWARE driver1 requested, BGRA_SUPPORT32, no software fallback. Device HRESULT S_OK0,
nonnull device/context, requested/selected feature level11_0/45056. Adapter GetAdapter and
GetDesc1 S_OK0; adapter flags0/SOFTWARE false. Meets API-reported hardware classification;
it does not independently identify a GPU vendor/model or attest physical hardware origin.

Texture creation S_OK0, texture_attempted/texture_returned true; initial_data_supplied false,
nonnull_output_pointer true; texture GetDesc called, descriptors_match true. Every field
was independently checked against fixed expected values and approved policy, not just
against the receipt's comparison flag:

| Texture field | Required | Requested | Returned |
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

Format28=R8G8B8A8_UNORM, usage0=DEFAULT, bind8=SHADER_RESOURCE.
SRV creation S_OK0, srv_attempted/srv_returned true, nonnull output storage;
srv_get_desc_called/srv_descriptors_match true. Exact explicit view fields:

| SRV field | Required | Requested | Returned |
|---|---|---|---|
| format | 28 | 28 | 28 |
| view_dimension | 4 | 4 | 4 |
| most_detailed_mip | 0 | 0 | 0 |
| mip_levels | 1 | 1 | 1 |

view_dimension4=TEXTURE2D. GetDesc methods return void: no resource-GetDesc HRESULT is
invented. Receipt get_desc_hresult is adapter GetDesc1. Wrong dimension/inactive-union
path was not taken; all active fields match. Three creation HRESULTs have correct signed0
values, not parameter-validation-only S_FALSE. Pointer validity is boolean, no raw addresses.
No pipeline binding, shader execution or undefined texel-content read occurred in this case.

## Release, memory and timing — PASS within stated policy

srv_reference_released=true; srv_released_before_texture=true;
texture_reference_released=true; test_resources_released=true. Source review confirms
SRV scope exits while caller owns texture, then texture/context/device scopes complete.
These are owned-reference release/order markers, not measured GPU driver deallocation.

Before memory4,956,160 bytes, limit1,073,741,824, available=true;
headroom1,068,785,664 bytes>=268,435,456 required. After release9,687,040 bytes,
same available limit; observed growth4,730,880 bytes (~4.51MiB)<=67,108,864 allowance.
Elapsed78ms<10000ms; final sequence/checkpoint indicates no timeout/late-PASS result.
Elapsed is the recorded monotonic snapshot, not an independent per-API latency benchmark.
No peak, leak, repetition, pressure or full driver-memory reclamation claim.
Watchdog cannot cancel blocked GPU/GetDesc/release/file operations; no such cancellation tested.

## Exact photograph and final persistence — PASS

Original IMG_5564.JPG visibly shows Native Diagnostics/D06-SRV01/package0.2.3.0/PASS,
reason RGBA8_SRV_CREATED_DESCRIPTOR_MATCH, hardware request/no fallback, device HRESULT0,
feature0xB000, receipt saved message and exact run
**DDCAC652-19A4-451E-8AD9-EB191AC45A23**. Matches original filename and JSON exactly.
Texture/SRV HRESULTs, descriptors and cleanup markers are verified from JSON, not claimed
visible in the generic UI photograph. No reliance on EXIF/device/GPS/camera-clock data.

Retrieved original terminal JSON plus exact-run saved message establishes this final receipt's
persistence. VERIFY_BY_RETRIEVAL intentionally does not predict successful future storage
within its own bytes. Fresh case/version/source/build/UUID distinguish older retained LocalState.
No intermediate .tmp history, remote listing timestamp or power-loss durability was tested.

## Separate result fields and determination

| Field | Result | Limit |
|---|---|---|
| Registration identity | MATCH_SUPPORTED | Owner context + pinned guard/manifest, no new Portal full-name/classification evidence |
| Activation/platform UI | PASS | Exact-run final native receipt and matching original dialog photo |
| Hardware/device/adapter | PASS | S_OK/device/context/11_0/SOFTWARE false, no fallback |
| Texture allocation/descriptor | PASS | S_OK+nonnull, all11 fields match fixed policy |
| SRV allocation/descriptor | PASS | S_OK+nonnull, all4 active fields match fixed policy |
| Owned-reference release order | PASS | View before texture then context/device, source/receipt markers; driver reclamation not proven |
| Memory/deadline | PASS | Available samples within headroom/growth/time policy |
| Source/build/six hashes | PASS | Pinned v4 contract and independently hashed archive members |
| Original photo/run association | PASS | Exact UUID/case/version/reason and saved message |
| Retrieved final persistence | PASS | Original terminal file/hash checked, not merely UI PASS |
| Overall | **PASS_D06_SRV01_ONLY** | One texture/view allocation, metadata inspection and scoped release case |

No FAILED criterion present: no failed HRESULT/null output/descriptor mismatch/software
fallback/memory breach. No required prerequisite/evidence remains BLOCKED. No unresolved
case attribution/schema/hash/time/terminal discrepancy remains INCONCLUSIVE. Provenance and
telemetry limitations below remain limits on interpretation, not missing case criteria.

## Provenance limitations

- Series X origin and receipt retrieval are owner-attested. JSON/photo are not independently
  signed hardware attestations; pinned hashes establish artifact consistency, not unforgeable
  remote execution. Process UUID is application-generated, not a hardware identity.
- Console UTC, remote mtimes and camera capture clock are not independently verified.
  Exact run/photo association is the correlation basis, not presumed accurate timestamps.
- Earlier checkpoint files were replaced; only final retrieved bytes supplied. Crash/hang/
  failure/persistence recovery paths are not experimentally validated by this PASS.
- Scoped release/order markers and sampled memory cannot prove all driver allocations freed,
  leak freedom, peak usage or long-duration stability. Actual driver overhead exceeds nominal4bytes.
- Platform MessageDialog appearance is not app-owned rendering/presentation or input/audio/lifecycle proof.

All141 frozen baseline pins and total152 prior signing-review artifact/evidence files were
rehashed unchanged. Source remains clean at approved commit. No accepted D00/HW01/FMT01/
RES01a baseline, installed app, LocalState, certificate/trust, console or production code changed.

**Still untested:** SRV backing-resource identity query, pipeline resource binding/sampling,
texel initialization/content correctness, shaders, draw/clear/copy/map/readback, rendering/
presentation, OpenGL, LWJGL, Java/JNI and Minecraft. This does not certify allD06.

## Next smallest independent gate — proposal only

Propose **D06-SRV-LINK01**: one inherited ID3D11View::GetResource query on the existing
fixed texture's SRV, require nonnull returned resource and compare canonical IUnknown
identity with the original texture. Record QueryInterface HRESULTs/identity-match boolean
without exposing raw pointers. GetResource returns void and adds an owned reference;
release returned resource and identity references before normal SRV/texture/context/device
cleanup. No new content access, initialization, binding, shader/draw/copy/readback or presentation.
This adds a backing-resource association check without introducing pipeline state changes.

Microsoft supports the getter/reference ownership in
[GetResource](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11view-getresource)
and canonical IUnknown comparison in
[QueryInterface](https://learn.microsoft.com/en-us/windows/win32/api/unknwn/nf-unknwn-iunknown-queryinterface%28refiid_void%29).
It remains a proposed diagnostic, not a hardware result. Separate source/build approval first,
then signing, installation-only, one launch, original receipt retrieval and cleanup approvals.
No next experiment implemented or executed in this acceptance review.
