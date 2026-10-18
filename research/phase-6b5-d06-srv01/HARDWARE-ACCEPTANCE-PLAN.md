# D06-SRV01 hardware acceptance plan — separately gated

Current hardware status **NOT EXECUTED**. Source `e3cd2e0fbed5725980d5cc36ac8cb6535d7fa4e8`;
build 20261017-185632-1c4c5a9c; unsigned path `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-185632-1c4c5a9c\NativeCapabilities.unsigned.appx`;
SHA256 **e70fd6c9ef76ff17a06a9ad605c6c88e5eb412240446b6bbfcf17d1b8897c693**. Preparation only; no target or signing action authorized.

## Gate1 — local signing/static integrity

Separate explicit approval for one fresh copy, exact source/unsigned hash and nominated
certificate. Rehash first; check certificate public metadata/nonexportable key availability;
preserve unsigned original. Sign once using SHA256. Verify CMS, APPX digest, original member
bytes/blockmap and expected signing metadata; record signed path/hash/signer. Standard
Windows chain trust reported separately; no trust repair/import/bypass or dependency install.
No signing approval implies installation, launch or future gate approval.

## Gate2 — owner installation-only update

Separate explicit approval naming signed artifact/hash. Existing authenticated Portal only,
no automatic remote settings changes. Confirm exact current NativeDiagnostics0.2.2.0 identity
and Not running.0.2.3.0 replaces that registration and may retain old RES01a/FMT01/HW01 receipts.
If installed RES01a must remain runnable side-by-side, stop for a distinct identity/build
approval. Preserve accepted artifacts and LocalState; do not uninstall/downgrade/clear data.

Rehash exact signed APPX immediately before submission. Upload only that artifact. Leave
framework uploads empty if installed Microsoft.VCLibs.140.00 x64 UWP satisfies unchanged
manifest; no UWPDesktop/fallback/certificate/PFX upload. Disable auto-launch; stop before
submission if that cannot be guaranteed. Exactly one update attempt, await final result.

Verify Name AlgorHome.LegacyForge.NativeDiagnostics, Publisher CN=LegacyForgeDiagnostics,
Version0.2.3.0, x64, App classification; capture PackageFullName only if actually displayed.
Stop on certificate/dependency/registration/identity/version/classification error or ambiguous
outcome; no retry/repair/trust or framework install/configuration change. Stop after registration.
No launch, receipt retrieval or cleanup under this gate.

## Gate3 — one owner-operated SRV01 launch

Separate explicit approval. Confirm registered artifact/version and no unexpected activation.
One launch using empty or exact D06-SRV01 argument. Observe at most30s;10s case decision
deadline cannot cancel a blocked GPU/GetDesc/COM-release/file call. No second launch.

Record activation/platform UI, case/version/status/reason, device HRESULT/feature, persistence
message and exact run UUID. Photograph only diagnostic display, without unrelated personal
identifiers. Both resource HRESULTs/descriptors/release order are confirmed from downloaded
JSON, not assumed from generic device-HRESULT UI. No dialog interaction necessary; platform
UI is not app-owned rendering. On timeout/crash/error stop and preserve evidence. No automatic
retry, repair, termination or cleanup; record any owner-close/suspend as separate observation.

## Gate4 — scoped read-only original receipt/photo verification

Separate explicit approval. Identify exact0.2.3.0 package inventory, then access only its
LocalAppData/LocalState/NativeCapabilityReceipts. List fresh D06-SRV01-<run UUID>.json and
same-run .json.tmp, record timestamps/sizes; preserve downloaded originals/photo unchanged
and compute SHA256 locally. No remote file modifications, unrelated apps/accounts or broad logs.
If path/download unavailable, stop collection and mark evidence BLOCKED/INCONCLUSIVE, no bypass.

Use pinned RECEIPT-SCHEMA.json v4 and independent receipt_contract.py semantic oracle.
Rehash six members directly from exact pinned unsigned APPX; Gate1 must establish equality
with signed member bytes. Never use receipt self-reported values as independent expected pins.

| Role /member | Pinned SHA256 |
|---|---|
| executable_sha256 /NativeCapabilities.exe | `ae5bf1529880c252d61d53e407dae1a11d3ebc6c1a62e52d41f1945b07b50fe4` |
| manifest_sha256 /AppxManifest.xml | `459fe8541f08cb06e60636b84b30c3e2268959acf0680034b325dc0e942d3d16` |
| build_inputs_sha256 /native-inputs.json | `707abd3ab6bebe12d4c536c923f2a86d155f4d3171d13a6fa5fb2eb4c8c19d4c` |
| policy_sha256 /profiles/D06-SRV01.json | `8e174475104f0519a7756d46240ac3a767d05659748486bf55d9267f8ab63542` |
| schema_sha256 /contracts/native-receipt.schema.json | `322358b6bb95467165fa97d8f5e48035bd06e9f025b0f109c9ec17300732b228` |
| inventory_sha256 /native-inventory.json | `53be6683824eeba3b764e9bb7f36fdb523faebbffe82e8f356cc3386f1de5e24` |

Verify source/build, package/version, production/frozen D00/HW01/FMT01/RES01a refs and
separate run/process UUIDs. Normal terminal sequence5/checkpoint BEFORE_CREATE_SRV, FINAL/
terminal true. Exact filename/photo UUID association required; older-case LocalState is not
new SRV evidence. Clock/remote mtimes are supporting chronology only, not hardware attestation.

Independent fields to retain:

| Evidence field | Required observations |
|---|---|
| Registration | Owner final install status/identity/version/classification, missing UI fields UNKNOWN |
| Activation/platform UI | Exact run/photo/error, no inference of app rendering |
| Device/adapter | HARDWARE1/BGRA32/no fallback, S_OK/non-null device/context/11_0; classification S_OK and SOFTWARE false |
| Texture | S_OK/non-null, null initial data/non-null output, GetDesc11 fields match fixed descriptor |
| SRV | One explicit requested descriptor, S_OK/non-null view, GetDesc4 active fields match |
| Cleanup | srv_reference_released, srv_released_before_texture, texture_reference_released, test_resources_released true |
| Resource/timing | Memory samples available, >=256MiB before headroom, <=64MiB observed growth, elapsed<10000ms |
| Persistence/binding | Retrieved original final, schema/source/build/six hashes match, no unresolved persistence error |
| Overall | Narrow SRV01 only; apply categories below |

Texture descriptor exact11 fields: width1,height1,mip_levels1,array_size1,format28,
sample_count1,sample_quality0,usage0,bind_flags8,cpu_access_flags0,misc_flags0.
SRV descriptor exact4 active fields: format28,view_dimension4,most_detailed_mip0,mip_levels1.
Wrong view dimension must omit inactive Texture2D members and fail the comparison; no padded
or inactive-union data is meaningful. GetDesc methods return void. No texel access occurs.

- **PASS:** All above fields and independent binding, reason RGBA8_SRV_CREATED_DESCRIPTOR_MATCH,
  FINAL/PASS/terminal true/sequence5; exact original photo/run association and terminal file
  retrieved. Scoped release flags are not proof every driver allocation is freed.
- **FAILED:** Normal negative API error, software/wrong device output, S_OK/null texture or view,
  S_FALSE/non-S_OK success, descriptor mismatch, native exception or memory-growth breach.
  Parameter validation alone never proves allocation; absent data is not zero success.
- **BLOCKED:** Environment/API/policy/classification/memory/receipt prerequisite unavailable,
  insufficient headroom or missing stage approval. Device/texture/SRV E_ACCESSDENIED/E_NOTIMPL/
  E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED are implemented BLOCKED mappings.
- **INCONCLUSIVE:** Deadline/late return/owner close/observer failure, missing/inaccessible/
  partial/nonterminal/stale receipt or unresolved schema/hash/identity/photo attribution.
  Empty observer details do not prove cleanup. No new launch to repair evidence.
- **NOT EXECUTED:** No authorized target run and original evidence. Build/synthetic tests are
  not hardware acceptance. RUNNING is only an intermediate checkpoint.

VERIFY_BY_RETRIEVAL avoids predicting a successful flush inside the receipt bytes. Missing
final file: persistence BLOCKED and overall INCONCLUSIVE, preserve .tmp/checkpoint. No future
power-loss durability, trusted-clock, hardware-attestation, peak-memory or leak proof. Startup
hashing/write and OS/driver calls lack a hard wall-time cancellation guarantee.

## Gate5 — cleanup

Separate explicit approval after originals/report are preserved, naming exact diagnostic-only
operation. No implicit uninstall, downgrade, LocalState clearance, framework/certificate removal,
production/D00/accepted-evidence change. Stop and report after each independently approved gate.

Even a future PASS proves one texture/SRV allocation and metadata/release path only. It does
not establish shader-resource binding/sampling, texture content, shader execution, rendering,
presentation, OpenGL, LWJGL, Java/JNI or Minecraft compatibility. No additional case is included.
