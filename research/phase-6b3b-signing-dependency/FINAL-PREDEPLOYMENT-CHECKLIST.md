# Final predeployment gates — no automatic next action

| Gate | Required evidence | Current status |
|---|---|---|
| Source/static safety | 4101f7e build, df23adb review, unchanged D00-only configuration and unsigned ecb53b... artifact | PASS, revalidated |
| Owner console observations | Dev Home working; OS10.26100.9445; default App; no changes | RECORDED, owner-reported |
| Installed Xbox framework | Exact Name/Publisher/Version/x64/Framework from authorized owner inventory | UNKNOWN; neither present nor absent assumed |
| Optional upload candidate | Exact original Microsoft standard-UWP APPX, SHA2569c17b5..., verified Microsoft signature, x64 and required exports | STATIC PASS; not permission to install |
| License | Applicable terms retained; owner confirms entitlement/conditions | BLOCKED confirmation |
| Diagnostic key creation | Explicit approval; CN=LegacyForgeDiagnostics, nonexportable local owner key, outside Git | BLOCKED approval; NOT CREATED |
| Signing | Separate approval, pinned input, approved thumbprint, signature verification, unchanged payload, new signed hash | BLOCKED; NOT SIGNED |
| Console/Portal access | Explicit owner authorization; credentials local, verified endpoint | BLOCKED; NOT CONNECTED |
| Package installation/registration | Separate approval for exact signed/dependency hashes; auto-launch off; final identity/deployment success | NOT EXECUTED |
| Activation | Separate approval for one exact diagnostic launch; fresh run observation | NOT EXECUTED |
| Graphics initialization | Record first renderer initialization/display separately; hardware D3D11 criterion unchanged | NOT EXECUTED |
| Durable receipt writing | New bound valid JSON; original hash, persistence result; no stale-file inference | NOT EXECUTED |
| Receipt retrieval | Owner-authorized diagnostic LocalAppData/LocalState/Phase6B1Receipts downloads only | NOT EXECUTED |
| Overall D00 | Existing terminal PASS/D00_ACTIVATED_HASHES_RECORDED, complete approved role hashes, no persistence error | NOT EXECUTED |

Full hashes are in PREPARATION-REPORT.md and READINESS-EVIDENCE.json. Abbreviations
in this table are labels only, never inputs to a hash check.

If hardware graphics initialization fails, existing code can still create a bound
FAILED/DIAGNOSTIC_UI_UNAVAILABLE receipt. Preserve independent registration,
activation and successful receipt-writing observations. Do not turn overall D00
into PASS or claim that the skipped native-control observations were completed.
If receipt creation itself fails, persistence is unproven; preserve numeric errors
and before/after file listings. No S21/JNI, formal D06 or Minecraft test is authorized.

The [owner runbook](../phase-6b3-xbox-readiness/OWNER-DEPLOYMENT-RUNBOOK.md) describes
installation without auto-launch and read-only retrieval using the **exact package
full name**. Do not clear LocalState/uninstall before preserving evidence, alter
shared frameworks, touch production identity/data, or change global App defaults.

The discovery/download of a research candidate is not evidence of console absence.
Do not propose an Xbox dependency installation until its need is established and
the owner approves the exact bytes. No action in this checklist has been performed
beyond source/static preparation and the owner-reported read-only observations.
