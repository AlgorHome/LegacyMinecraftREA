# Phase 6B.3f — owner-operated Xbox framework inventory

**Read-only UI inspection only. Codex has not connected to the console.**
Owner-reported baseline: Dev Home operational, OS/build10.26100.9445, default App.
Required framework installation remains **UNKNOWN** until actual inventory evidence.
Existing signing, signature-integrity and D00-only evidence is preserved unchanged.

## Owner steps

1. Use the already configured Device Portal HTTPS address shown in your own Dev
   Home. Authenticate locally in your browser. Do not change Remote Access or
   security settings, import certificates or bypass a new trust failure. If the
   existing Portal cannot be opened under the current configuration, stop and
   report that limitation; framework presence remains UNKNOWN.
2. On Portal **Home**, inspect **My games & apps**. If this console build instead
   exposes an Apps manager/installed-packages view, use its read-only list/details.
   Microsoft documents Home and package details; exact widgets vary by build.
   Do not click Add/Install, Launch, Stop, Uninstall, Update or configuration actions.
3. If the inventory offers a package-type filter, include framework/system packages
   as well as applications. Record the filter and whether frameworks are actually
   included. Do not assume such a control exists or that an app-only list is complete.
   Expand all pages/loaded results using read-only navigation if applicable.
4. Search the list for **Microsoft.VCLibs.140.00**. Open only a matching entry's
   read-only details, if offered. Distinguish the exact Name from friendly display
   names and from **Microsoft.VCLibs.140.00.UWPDesktop**. Record every matching
   architecture/version; do not update, downgrade or install anything.
5. Copy the five fields below exactly as shown. If PackageFullName is visible, also
   record it. If architecture is visible only as `_x64_` in PackageFullName, label
   it **derived from PackageFullName**, rather than directly displayed. Framework
   status must be explicit; the name, logo or presence of VCLibs is not proof of
   an IsFramework/Framework=true flag. Leave missing fields UNKNOWN.
6. Return the sanitized table and inventory coverage notes. Crop account names,
   user SIDs, console identifiers, private endpoint and authentication details
   out of screenshots. No credentials or browser traffic archive is required.

| Field | Expected identity / what to record |
|---|---|
| Name | Exact Microsoft.VCLibs.140.00; no UWPDesktop suffix |
| Version | Actual installed version, even if different from candidate14.0.33519.0 |
| Architecture | x64, with displayed/derived source noted |
| Publisher | Exact distinguished name; expected CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US |
| Framework | Explicit true/false if visible; otherwise UNKNOWN |
| PackageFullName | Optional exact package full name from details, not a friendly label |
| Inventory coverage | View name, filters, all pages covered, whether framework packages are included |

The diagnostic's manifest floor is14.0.0.0. Export coverage has been verified for
the local14.0.33519.0 candidate only; a different installed version needs its own
suitability assessment. This inventory does not authorize package replacement.

## How results are recorded

- **PRESENT / verified identity:** exact matching package and required properties
  observed. This establishes inventory presence, not successful diagnostic activation.
- **Package observed, suitability incomplete:** exact Name found but architecture,
  publisher, version or Framework flag missing. Keep the missing fields UNKNOWN.
- **UNKNOWN:** name not shown in an app-only/incomplete list, no framework filter,
  failed authentication/trust, permission error, omitted fields or unverified list
  coverage. A zero-result browser search is not confirmed absence.
- **CONFIRMED ABSENT:** only after a successful, complete inventory known to include
  framework packages, without exclusions or missing pages, shows no matching
  standard-UWP x64 package. Record the evidence establishing that coverage.

## If the UI cannot reveal it

Record the exact UI limitation and leave the relevant fields UNKNOWN. The next
controlled read-only gate is an owner-operated authenticated **GET** of the existing
Portal package inventory, if the owner authorizes that route; no Codex connection,
credential capture or write request is proposed:

```text
GET /api/app/packagemanager/packages
```

The documented response includes Name, PackageFullName, Publisher and Version.
It does **not** promise an explicit Framework or Architecture field. Architecture
may be derived from the package full name; Framework stays UNKNOWN unless another
read-only property exposes it. Do not infer complete framework coverage merely
from HTTP200 or an empty response. If this route also cannot establish coverage,
stop for review rather than install an inventory app, change permissions or deploy
the dependency/diagnostic as an inventory probe.

Microsoft references, checked2026-10-17:
[Xbox Portal Home/details](https://learn.microsoft.com/en-us/windows/uwp/xbox-apps/device-portal-xbox),
[documented installed-package GET](https://learn.microsoft.com/en-gb/windows/uwp/debug-test-perf/device-portal-api-core#get-installed-apps).

No signing, installation, launch, certificate-trust change, global app classification
change, console security change, package identity change or production code edit is
part of this procedure. Registration, activation, rendering, receipt writing and
overall D00 remain NOT EXECUTED; local integrity PASS does not become console PASS.
