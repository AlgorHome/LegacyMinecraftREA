# D06-FMT01 separately gated Xbox acceptance plan

**PREPARATION ONLY. No signing, installation, launch, retrieval or cleanup is authorized here.**
Approved-for-review unsigned source `bbe3a42c422e4328d5f98c07a9370fa948d0cbbf`;
artifact `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-180047-9ad3700d\NativeCapabilities.unsigned.appx`;
unsigned SHA256 `24dc6835408f9a5d38d1ab56ec82dfd550cf0dc183e495defa836299d77dd03d`. Never submit this unsigned package as if already signed/approved.

## Gate0 — registration preservation choice

Inventory/read-only actions need their own approved scope. Current intended identity is
AlgorHome.LegacyForge.NativeDiagnostics / CN=LegacyForgeDiagnostics /0.2.1.0 /x64 /App.
Later installation is an update of HW010.2.0.0 and may retain LocalState. Preserve archived
HW01/D00 packages, receipts, photos and exact source refs; do not uninstall, clear storage
or touch RuntimeDiagnostics/production LegacyForge. If HW01 must remain installed for
side-by-side reproducibility, stop and approve a distinct package implementation first;
NativeFormatDiagnostics is the documented alternative, with new receipt identity bindings.
No restoration/downgrade or uninstall is automatic.

## Gate1 — local signing and static verification (separate approval)

Rehash unsigned artifact immediately before signing; stop on mismatch. Use one fresh copy,
only the nominated diagnostic certificate; preserve original. Verify certificate metadata,
CMS/content integrity, package digests/blockmap and all original payload bytes. Record signed
path/SHA256/signer. Retain standard Windows chain-trust outcome separately; never import
trust or bypass rejection automatically. No installation implied by signing approval.

## Gate2 — owner installation-only (separate approval)

Use only the later approved signed SHA256 through the owner's existing authenticated Portal.
Read exact current diagnostic identity/version and confirm not running. Confirm App
classification and installed Microsoft.VCLibs.140.00 x64 satisfies the unchanged manifest;
do not assume framework status or upload the UWPDesktop alternative/fallback unnecessarily.
Disable launch-after-install and stop if that cannot be ensured. One update attempt only;
record status/HRESULT/full package identity and0.2.1.0 registration. Preserve LocalState.
Certificate/dependency/registration/version errors mean STOP; no retry, repair, trust change,
framework installation, uninstall or launch. Signing approval does not authorize this stage.

## Gate3 — one D06-FMT01 launch (separate approval)

Confirm package/version/source/signed artifact match gate2 and no extra launch occurred.
Owner launches exactly once using empty arguments (or exact D06-FMT01 if supported).
Observe for at most30s without reactivation. Case decision deadline10s is observational;
no claim that a blocked driver or file call is cancelled. Photograph exact displayed case,
version, reason/status, run UUID, creation HRESULT/level and persistence text. No dialog
interaction is necessary for query acceptance. A close/suspend event is independently noted;
manual termination or any additional activation/cleanup needs its own scope.
On timeout/crash/failure stop; preserve existing evidence, no automatic relaunch.

## Gate4 — diagnostic-only read-only receipt retrieval (separate approval)

Identify the exact0.2.1.0 PackageFullName from owner inventory without guessing suffixes.
Access only that package's LocalAppData/LocalState/NativeCapabilityReceipts. List filenames,
timestamps/sizes; retrieve D06-FMT01-<fresh run UUID>.json and same-run .json.tmp if present.
Do not overwrite, clear or delete remote files; do not collect D00/other-app data or broad logs.
Preserve downloaded original bytes and photo, calculate local SHA256, sanitize only separate
copies if necessary. Correlate photo run UUID with JSON/filename and receipt/build/version.
Clock/file timestamps are supporting observations, not trusted proof of device provenance.

Use RECEIPT-SCHEMA.json and source tools/receipt_contract.py to validate structure/semantics.
Rehash six members **from the exact approved pinned package independently**, not using
receipt claims as the expected hashes. BUILD-EVIDENCE.json pins all six unsigned values;
Gate1 must establish equality to signed payload. Check source/build IDs and production/
frozen D00/HW01 refs, distinct process/run UUIDs, normal terminal sequence4 and checkpoint
BEFORE_FORMAT_QUERY. Unexpected/missing binding is INCONCLUSIVE until resolved; never PASS.

| Role | Expected SHA256 |
|---|---|
| executable_sha256 | `eda70661b4f0ec6b7df6e08b81c8e42f7ee2f6f11acc8f3c3be69a5872f43de1` |
| manifest_sha256 | `593fbda9d0dce1ac6b6f12a96e187d5b1c2d0d4aaced9accdadb7cf806807fd0` |
| build_inputs_sha256 | `5cb62bbacce8b7000099f9432c285bbb71b8b3e26fd50876878f1db1a89cc21a` |
| policy_sha256 | `57f849c631ba5fd2de08e6d6eda593eccd81f7cba485212b99f7665b86f0a845` |
| schema_sha256 | `3373265fb3aa787a375e4edc1da54e4807793bf4151d645519d9c45b5cdbb6b7` |
| inventory_sha256 | `37cc66fcd8abd77fce39b6d488ac822e196ced3bf91cb1a7835ec90976d1f1b6` |

## Independent result fields and acceptance

Record each field separately: installation/registration, activation, platform dialog visibility,
hardware creation/classification, exact-format query, flag decoding, cleanup/memory,
receipt persistence, payload/provenance binding and overall case acceptance. UI absence
alone does not establish native failure; a valid independently bound original may still
establish query success. A dialog PASS alone cannot establish durable acceptance.

- **PASS:** All source/build/identity/hash/UUID checks; driver HARDWARE, no fallback;
  creation S_OK0x00000000/level45056, nonnull device+context; adapter SOFTWARE bit false;
  query format28/R8G8B8A8_UNORM, query S_OK, valid raw mask; required0x20/0x200/0x4000
  bits all present, all four booleans consistent; cleanup true; before headroom>=256MiB,
  after observed growth<=64MiB; elapsed<10000ms; FINAL/PASS/terminal true, sequence4,
  reason RGBA8_REQUIRED_FORMAT_SUPPORT_CONFIRMED; independently retrieved original final
  receipt, no unresolved persistence failure, photo/run correlation if available.
- **FAILED:** Valid query missing required support bits (zero is a valid failing mask),
  ordinary failed native HRESULT, hardware/output mismatch, software adapter, native
  exception, or memory-growth policy breach. Preserve exact reason/HRESULT. MIP absent
  alone is never failure. Never interpret invalid output as zero capabilities.
- **BLOCKED:** Required environment/API/policy/receipt prerequisite unavailable, insufficient
  headroom/unavailable memory, or missing approvals. Creation E_ACCESSDENIED/E_NOTIMPL/
  E_NOINTERFACE/DXGI_ERROR_UNSUPPORTED; query E_ACCESSDENIED/E_NOTIMPL/E_NOINTERFACE;
  unavailable classification are the implemented blocking mappings.
- **INCONCLUSIVE:** Timeout/crash/late return, owner close, invalid/sentinel/reserved output,
  unexpected non-S_OK success, inaccessible/missing/partial/nonterminal evidence or
  unresolved independent integrity/provenance discrepancies. Returned INCONCLUSIVE
  details may be empty if observer wins; cannot infer capability absence or cleanup.

JSON marks receipt_persistence_result=VERIFY_BY_RETRIEVAL, intentionally not self-predicted
flush success. A .tmp or nonterminal checkpoint does not meet final acceptance. When final
receipt is inaccessible, record persistence BLOCKED and overall INCONCLUSIVE; do not retry.
Downloaded file proves this retrieval, not future power-loss durability. Receipt is not signed;
owner-provided console context remains an explicit provenance limit.

**Rendering, presentation, texture/shader execution, OpenGL, LWJGL, Java/JNI and Minecraft
remain untested even if D06-FMT01 passes.** Format-support flags are driver reports only.

## Gate5 — cleanup (separate approval)

No implicit cleanup. Only after original evidence is preserved/accepted and owner separately
authorizes exact diagnostic-only removal/storage action. Never remove dependencies, certificates,
accepted D00 or production apps. Preserve earlier LocalState unless explicitly authorized.

Stop after each gate and report outcome; no approval carries forward to a later stage.
