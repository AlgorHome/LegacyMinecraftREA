# D06-HW01 final Xbox hardware acceptance — PASS

2026-10-17, America/Chicago. **PASS for D06-HW01 hardware D3D11 device creation
and available adapter classification only. Not all of D06.** Local evidence
analysis/documentation; no additional launch, console access, package/source
change, signing, installation, cleanup or production modification occurred.

## Preserved original evidence

Owner-provided original receipt:
C:/Users/arinze/Desktop/D06-HW01-594ACA53-FC63-4709-9C8B-BE96BEDD84BD.json.
Preserved byte-identically under
C:/Users/arinze/Desktop/ReverseLegacyCraft/analysis-local/phase6b5-hw01-acceptance/originals/.
The original on Desktop was not edited. Independently recomputed SHA256 matches:
**14d609bddfe39019ed4808a23190319895a4b9d4d7117eb072c6f74014a49bc7**.

Supplied photograph copied unchanged as originals/Xbox-D06-HW01-PASS.png in that
private evidence directory. SHA256:
**335a12b5cd31ab42d0a32e131c968b0a9549d0eb0cb1b26b1c83bcbbe9e15eff**.
No legible account/device/network identifier is visible on the diagnostic display;
no synthetic alteration of test text was needed. Originals remain outside Git.

HARDWARE-VERIFICATION.json contains the machine-readable checks. The accompanying
verify_hardware_receipt.py reads local bytes only; it neither imports a target DLL
nor executes the diagnostic. Schema validation uses a local standard-library
validator implementing every keyword actually used by the pinned schema, including
local references/formats/field restrictions and duplicate JSON key rejection.

## Source, case, run and terminal evidence

| Field | Verified observation |
|---|---|
| Schema | legacyforge-native-capability-receipt-v1, matches pinned package |
| Package | AlgorHome.LegacyForge.NativeDiagnostics / CN=LegacyForgeDiagnostics |
| Version/architecture/Application Id | 0.2.0.0 / x64 / App |
| Expected identity | true |
| Source commit | a3f72874241914f6048d4ca9ec4fc0edc978625d |
| Build ID | 20261017-173106-d79a3eae, matches packaged build inputs |
| Production comparison | d1453434ceefe73bef5aff497194e09f39dde7e1 |
| Frozen D00 reference | 553c6554f40f1372b0ea09f6badbbb98e133a9ab |
| Case | D06-HW01 only |
| Run UUID | 594ACA53-FC63-4709-9C8B-BE96BEDD84BD, matches filename and photo |
| Process UUID | FB83C3BE-785B-4D9F-98CF-444025A0C12D, valid and distinct from run |
| Result | PASS / FINAL / terminal true |
| Reason | HARDWARE_DEVICE_CREATED_AND_CLASSIFIED |
| Sequence | 3, consistent with STARTED -> BEFORE_CREATE_DEVICE -> FINAL |
| Last durable checkpoint | BEFORE_CREATE_DEVICE |
| Elapsed/deadline | 94ms /10000ms; not a deadline/late-completion result |
| Recorded UTC | 2026-10-17T22:42:23.639Z |
| Chicago equivalent | 2026-10-17 17:42:23.639 CDT |
| Java/gameplay/full D06 flags | java_jni_enabled=false, minecraft_or_gameplay_tested=false, all_d06_certified=false |

The UUID proves correlation within this supplied evidence set, not a cryptographic
identity of Xbox hardware. Registration/console origin remain owner testimony;
no new Portal inventory or installation-log collection was performed. A valid
native receipt and matching UI provide activation evidence but do not reconstruct
the original installation/launch trigger or prove no other owner action occurred.

## Six independent payload comparisons — PASS

Approved unsigned APPX was rehashed:
79722c961dd677a2c89610599aec2e9537727dead6d66e2e3e8ff522da8b2501.
Approved signed APPX was rehashed:
d4629d1f494f73db7dcb6290bee8c5c9f28375c8630c531e58b3ee95a6f05908.
Each required uncompressed member was hashed afresh from unsigned package bytes,
compared with the receipt and confirmed byte-identical in the pinned signed copy.
Receipt values themselves were never used as the expected oracle.

| Required role | Independently verified SHA256 |
|---|---|
| executable_sha256 | 61ba742e8022c6874af7364c022289157c887da5d6035201f4aa61dba7ca02d0 |
| manifest_sha256 | b107ba9665b0eb35d640cb5f7ff43b96ec2071d341feca0d5bfc3343eb98b7a4 |
| build_inputs_sha256 | 13a52990281afbbbca0c2e83f903216e7dd46791253f5e7154f6a16757d1c03b |
| policy_sha256 | 01561fdb7ff95df0d502659b7ab3c5065a8c9f681c4d5ed38db7053a9f837cac |
| schema_sha256 | db311c43104e3940cd7299a495b3ac2a5a0440cb8b3af06cbb5ba1314a4331e1 |
| inventory_sha256 | 642a0d0826deb138fb61fdbcedf02718e83d0938b3960a00c0c1ffc848354bb4 |

## Device, classification, cleanup and resources

Requested driver HARDWARE/value1; software fallback false; creation flags32
(BGRA_SUPPORT); requested and selected level45056/0xB000 (11_0). Exact creation
HRESULT0x00000000, signed0. Device/context returned true. GetAdapter/GetDesc1
HRESULT0x00000000; adapter Flags0 and software flag false. These establish the
requested hardware path with the classification exposed by the API. They do not
identify the physical GPU or guarantee all features/performance of the console.

Receipt test_resources_released=true corresponds to reviewed lexical release of
context/device/adapter references on the owning worker. This is scoped COM cleanup,
not proof all driver allocations disappear immediately or a leak/endurance test.

| Memory policy item | Receipt observation / oracle |
|---|---|
| Before app usage | 4,911,104 bytes |
| Reported limit | 1,073,741,824 bytes |
| Before headroom | 1,068,830,720 bytes, exceeds268,435,456 minimum |
| After release app usage | 9,482,240 bytes |
| Observed growth | 4,571,136 bytes, about4.36MiB; below67,108,864 maximum |
| Availability | both snapshots available |

These are observations from the receipt; counter accuracy and driver-internal
memory are not independently measured. They satisfy the fixed policy, not a
universal Series X memory limit or allocation-capacity certification.

## Photo correlation and persistence

The inspected photograph visibly shows Native Diagnostics — D06-HW01, case/package
0.2.0.0, PASS, exact reason, hardware request/no fallback, creation HRESULT0,
feature0x0000B000, receipt saved and run
594ACA53-FC63-4709-9C8B-BE96BEDD84BD. This exact run ID matches receipt and filename;
it is not an inferred timestamp-only association. The image shows the platform
dialog and Close button, not app-owned render/presentation output. UI dismissal
behavior is not tested by a still image.

Serialized receipt_persistence_result is VERIFY_BY_RETRIEVAL. Retrieval of this
valid final original resolves that check for this run; the photograph independently
shows the saved message, whose reviewed source requires a successful terminal
write snapshot. No receipt/role/schema mismatch or persistence warning is present.
This is PASS for normal retrieved-file persistence, not power-loss durability or
all future storage operations. Previous physical checkpoint versions and remote
file timestamps/sizes were not separately supplied; the internal sequence/marker
are consistent but not an independent checkpoint history.

The receipt is not digitally signed; owner-attested Xbox retrieval and photograph
context establish provenance. Console UTC clock and photo capture time are not
authenticated/synchronized. Run-ID correlation is available despite that limit.
No broad logs, personal identifiers, credentials or unrelated files were collected.

## Separate acceptance decisions

| Dimension | Result |
|---|---|
| Installation/registration | consistent owner-installed package context and matching receipt identity; original registration log not independently inspected |
| Native activation | PASS, attributable final native run and photographed UI |
| Platform status UI | PASS for observed display, exact run correlated; no app-rendering capability inference |
| Hardware device creation/classification | PASS, exact oracle above |
| Scoped cleanup/resource policy | PASS within declared observations/limits |
| Durable terminal receipt | PASS for retrieved original and matching saved UI |
| Overall D06-HW01 | PASS, narrow case only |

Outcome rules: **FAILED** if hash/binding/device/feature/software/resource/cleanup
oracle is violated on an exercised supported path. **BLOCKED** if required API,
policy, package or evidence prerequisite is unavailable. **INCONCLUSIVE** for
timeout/interruption, missing final evidence, ambiguous run or incomplete oracles.
**PASS** requires all declared case oracles plus validated original evidence.
**NOT EXECUTED** remains the status for additional capabilities with no approved run.
No such outstanding criterion prevents this D06-HW01 PASS.

## Exclusions and next narrow experiment

Rendering, render-target correctness, presentation, readback, OpenGL, LWJGL,
Java/JNI, Minecraft/gameplay, audio/input and lifecycle stress remain **NOT TESTED**.
The platform's status dialog is not D06 render/present certification. Accepted D00
source/artifact/evidence hashes were rechecked unchanged; production is untouched.

Recommend, for separate design/implementation approval, a narrow **D06-FL01 format
support** variant: call CheckFormatSupport only for DXGI_FORMAT_R8G8B8A8_UNORM on
the reviewed hardware path, record exact HRESULT/bitmask, and test required
TEXTURE2D/RENDER_TARGET bits. No texture allocation, draw, present, adapter sweep,
OpenGL or Java. This is narrower than the full feature-query matrix row and would
prepare the later bounded texture/readback case; it is not implemented here.
Reference: [Microsoft CheckFormatSupport](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-checkformatsupport).

Source/build, signing, owner installation, one run and receipt collection remain
independent approval gates for any next artifact. Stop after this local review.
