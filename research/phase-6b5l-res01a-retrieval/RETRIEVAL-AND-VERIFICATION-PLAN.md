# Phase6B.5l — D06-RES01a read-only receipt retrieval preparation

**Visible PASS: OWNER-REPORTED. Receipt PASS: NOT VERIFIED. Formal acceptance: PENDING.**
Owner reports NativeDiagnostics0.2.2.0/D06-RES01a activation and visible PASS, no errors.
Run UUID was not captured; no photograph supplied. No further launch is authorized.
Do not reconstruct a run ID, assume a photograph exists or claim a correlated receipt.
Historical build evidence remains unchanged; its NOT EXECUTED field describes that build phase.

## Local preservation/preparation completed

Approved signed APPX SHA256 ead7016c94e551fac43e2b622b323354bfa4506fe507f44bf5e98f112b8f0c3f
and unsigned SHA256526c7fe24950a1084e592c2df3d020c82aa1d15cd330b4b7fd5612e82191d7e8
were reverified. All107 frozen pins and total118 prior original/evidence files match.
All6 role members were rehashed directly from pinned unsigned APPX and compared with
signed member bytes and original build pins. EXPECTED-PAYLOADS.json records exact paths,
source4457142ff1fd9e01371eb446612c70162ce93357/build20261017-183031-15ba7835 and hashes.
No signing, installed-app/source/LocalState/console/trust change or target execution occurred.

## Owner-operated read-only collection

1. Use the existing authenticated Device Portal without changing settings. Do not click
   Launch, Restart, Install, Update, Repair, Uninstall or clear storage.
2. Locate only AlgorHome.LegacyForge.NativeDiagnostics0.2.2.0, x64. Record exact
   PackageFullName if displayed; do not guess its publisher suffix. If identity/version
   cannot be established, stop that collection path and report UNKNOWN/UNAVAILABLE.
3. Open the Portal file explorer for that exact diagnostic package's LocalAppData.
   The app-relative directory is **LocalState/NativeCapabilityReceipts**.
   Some UI roots already start at LocalState; use NativeCapabilityReceipts beneath it.
   Do not browse other apps, production LegacyForge, accounts or broad logs.
4. List only D06-RES01a-*.json and corresponding .json.tmp candidates. Record filenames,
   displayed timestamps and sizes. Leave prior D06-FMT01/HW01 receipts untouched.
   Missing/inaccessible directory is UNAVAILABLE/BLOCKED for collection, not proof no file exists.
5. With no captured run UUID, use the diagnostic-specific listing to identify candidate(s).
   Do not select solely by newest timestamp: console clock accuracy is unknown. If several
   RES01a candidates exist, return their minimal listing first to resolve ambiguity.
6. Download the original D06-RES01a-<UUID>.json through an existing read-only download
   action; same-run .json.tmp may be preserved separately if present. No remote edits,
   rename/delete or directory creation. If the Portal lacks a read-only download path,
   stop and report UNAVAILABLE; no workaround tool or additional permissions.
7. Save the file locally with its original filename and bytes. Do not open/save through an
   editor, normalize whitespace, or substitute copy-pasted text. Record local path and compute:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\path\D06-RES01a-<UUID>.json'
```

   Return exact local path, hash and the diagnostic-only listing metadata. Do not share
   credentials/account/device/network identifiers. An already-existing photo may be supplied
   if available; do not relaunch or change the console to obtain one.
8. Stop after download. No retry/activation/cleanup. If a receipt is absent, preserve that
   observation and await review; visible PASS alone does not establish formal acceptance.

## Prepared local verification, awaiting original

verify_original_receipt.py has been syntax-checked only; it has not consumed a receipt.
It will preserve a byte-identical copy in a hash-named private originals directory, compute
SHA256, reject duplicate JSON fields, validate pinned schema v3 and case semantics,
verify source/build/identity/filename/run/process IDs and independently hash all6 archive
members again. Optional independent owner SHA256 is compared if supplied. It never loads
native target code, accesses Xbox or edits input bytes. Verification results go to a new
local evidence file, not frozen evidence or console storage.

| Role | Pinned unsigned member SHA256 |
|---|---|
| executable_sha256 /NativeCapabilities.exe | `cb08435285c6dad6f0eba7b0be955f4243d52d29bf575cacfcef4aa6facfbd67` |
| manifest_sha256 /AppxManifest.xml | `82f0b634c4343a5272af9f873d1accc528970407da0dce1913deeb1704ccc3c0` |
| build_inputs_sha256 /native-inputs.json | `d7fcb2e1ac04e3013a37dcca473ea24e402ce165de1f7460efbd7924de9b8a1e` |
| policy_sha256 /profiles/D06-RES01a.json | `ec8a12dda98ecfbcaac14ff647c329867d7e386aebcf4d6d0d4e48812348c0e2` |
| schema_sha256 /contracts/native-receipt.schema.json | `cd2ba13e2da44ead0cb3f421d88138596cca6541e86105daed7e892883029180` |
| inventory_sha256 /native-inventory.json | `d5abc15a2bd38f06d749fd371855302b74861eebc8f46ddab0d03e9bdf42fbe4` |

For a PASS receipt, verify hardware driver HARDWARE1/BGRA32/no fallback, S_OK device,
level11_0/45056, nonnull device/context and non-software adapter (classification HRESULTs
S_OK). Texture call must be attempted, S_OK0 and nonnull; GetDesc called and every field
matches both requested fixed descriptor and independently pinned policy:
width1,height1,mip_levels1,array_size1,format28,sample_count1,sample_quality0,usage0,
bind_flags8,cpu_access_flags0,misc_flags0. S_FALSE is never successful allocation.
No GetDesc HRESULT is invented; it is a void metadata method, not a content read.

Check texture_reference_released/test_resources_released true; before/after memory
available, >=256MiB before headroom, <=64MiB observed growth. FINAL/PASS/terminal true,
reason RGBA8_TEXTURE_CREATED_DESCRIPTOR_MATCH, sequence4/checkpoint BEFORE_CREATE_TEXTURE,
elapsed<10000ms. Verify current-run original final persistence by retrieved bytes, not
only UI saved text or a .tmp/nonterminal checkpoint. Release flags do not prove every
driver allocation freed; sampled memory is not peak/leak testing, and no blocked-call
cancellation is claimed. Receipt UTC and remote mtime are not trusted clocks.

## Separate evidence/result fields

| Field | Current state |
|---|---|
| Activation | PASS, owner-reported |
| Visible status | PASS, owner-reported |
| JSON/schema/native outcome | NOT VERIFIED; original awaited |
| Persistence | UNKNOWN until original retrieval |
| Run UUID /photo | Not captured /not supplied |
| Association of visible run to receipt | UNESTABLISHED; do not invent |
| Formal hardware acceptance | PENDING; cannot mark PASS now |

A later structurally valid/source-bound PASS receipt establishes a receipt-level result,
not automatically the missing photograph/visible-run association. Final review must state
provenance limits and apply the existing acceptance plan; if an attribution criterion
remains unresolved, report INCONCLUSIVE rather than inventing it. No automatic formal PASS
is emitted by the prepared verifier. Do not request a relaunch to fill an evidence gap.

No texture content, SRV/RTV, rendering, presentation, OpenGL, LWJGL, Java/JNI or Minecraft
capability is established by current owner-visible PASS or by this preparation phase.
