# Owner-operated read-only diagnostic evidence intake

2026-10-17. Retrieval authorization only; no console actions were performed by
Codex. Originals folder is currently empty. Collection and correlation are pending
owner retrieval, not UNAVAILABLE unless the owner actually observes that limit.
This collection is separate from the unsigned 0.1.3.0 MTA experiment. Installed
version remains owner-reported 0.1.2.0; do not update or launch any version.

1. In the existing authenticated Portal, inspect the exact diagnostic package row.
   Match Name AlgorHome.LegacyForge.RuntimeDiagnostics, Publisher
   CN=LegacyForgeDiagnostics, Version0.1.2.0, x64, App classification. Copy its actual
   PackageFullName and package-relative ID if visible; do not construct them.
   If details truncate the name, inspect the matching record from the existing
   read-only GET /api/app/packagemanager/packages interface on the same Portal
   origin, only if already accessible without additional tools or permission
   changes. Do not retain/share whole inventory or RegisteredUsers/SIDs.
   If neither route exposes the identifier, mark identification UNAVAILABLE and
   stop any collection path that requires guessing the app-data container.
2. If existing Portal file explorer exposes this exact diagnostic's LocalAppData,
   select its LocalState/Phase6B1Receipts only. Record original remote filenames,
   timestamps (and timezone if known), and sizes before download. Do not infer
   source timestamps from the PC download creation time. Do not browse production
   LegacyForge, other apps or account/configuration folders.
3. Download existing D00-<run UUID>.json files and their corresponding temporary
   files into originals/. Keep all relevant diagnostic D00 versions, because an
   update can retain old LocalState. Do not edit, rename, delete or upload files
   on the console. Distinguish no directory, empty directory, access denied and
   unavailable file-explorer support. Stop an unsupported path; do not enable
   sharing, use extra tools or change permissions/settings.
4. Existing activation/error records may be copied only where the Portal supports
   filtering to this exact diagnostic. Preserve the incident timestamp, package,
   version if provided, HRESULT/exit/exception code, failing module and stage.
   Do not start logging, ETW, a debugger, reproduction or a broad export. If the
   existing UI cannot isolate the diagnostic, mark that path UNAVAILABLE and stop.
   Do not copy cookies, credentials, account IDs or unrelated events.
5. Keep original downloaded files private under originals/. Provide their local
   paths to Codex for SHA256 inventory and sanitized derivative copies. Original
   diagnostic records will not be uploaded or committed automatically. Raw files
   with personal fields need not be pasted into chat.

After files arrive, hash each original before parsing and preserve those bytes;
record remote listing separately. Create derivatives under sanitized/ with personal
account, console/device, machine, network/address and user-path identifiers redacted.
Retain technical package identity/version, D00 case, run/process UUIDs, timestamps,
stages, error codes and package role hashes needed for correlation. If a technical
field embeds a personal value, use a consistent placeholder and record the
correlation limit. Sanitation requires field-by-field review, not a blanket claim
that an automatic regex removes all personal data. Hash sanitized copies separately
and record source-to-copy mapping without storing secrets in the mapping.

Correlate package_version + run_id + process_instance_id + event time/stage with
the approved artifact's role hashes. A timestamp or current registration alone
cannot assign an old receipt to 0.1.2.0. Empty/partial/tmp records are not PASS.
No receipt is not proof the executable never started. Keep prior 0.1.1.0 error
0x87E10006 separate from owner-attributed 0.1.2.0 apparent crash/0x8027025B.

Current evidence state:
- Registration: PASS, owner-reported for 0.1.2.0.
- Activation: reported failure/apparent brief startup; existing log not collected.
- D00 rendering: UNKNOWN; brief appearance is not proof.
- Native-control execution: UNKNOWN.
- Receipt persistence: UNKNOWN.
- Exact PackageFullName / receipt listing / activation records: PENDING OWNER.
- Local originals received: zero at preparation time.

No new launch, install/update/repair/uninstall, storage clearing, trust/configuration
change or Java/JNI/Minecraft/production operation is included. STOP after analysis.
