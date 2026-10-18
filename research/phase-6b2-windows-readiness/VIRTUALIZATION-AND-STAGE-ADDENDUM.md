# Virtualization checks and independent stage reporting

2026-10-17, America/Chicago. D00 execution remains BLOCKED. Only read-only
host queries and documentation were performed; no VM start, feature change,
signing, installation, activation or diagnostic execution occurred.

## Current host results

| Query | Observation |
|---|---|
| Get-ComputerInfo requested fields | WindowsProductName=Windows 10 Pro; WindowsVersion=2009; OsBuildNumber=26300 |
| Win32_OperatingSystem cross-check | Microsoft Windows 11 Pro; 10.0.26300; build26300; 64-bit. Product-name fields disagree; the raw Get-ComputerInfo name is not treated as an OS downgrade. |
| Containers-DisposableClientVM | BLOCKED: operation requires elevation; HRESULT -2147024156 |
| Microsoft-Hyper-V-All | BLOCKED: operation requires elevation; HRESULT -2147024156 |
| Get-VM command | Present, Hyper-V module |
| Get-VM inventory | BLOCKED: permissions unavailable; HRESULT -2146233088; not an empty inventory result |
| CPU | Intel Core i5-9500 @3.00GHz |
| CPU virtualization CIM booleans | VirtualizationFirmwareEnabled=false; SecondLevelAddressTranslationExtensions=false; VMMonitorModeExtensions=false |
| HypervisorPresent | true |

The running session is not elevated. No elevation prompt or new administrative
shell was opened. CPU flags are recorded as reported; with a hypervisor present
they are not sufficient grounds to conclude virtualization is disabled or request
BIOS changes. Microsoft documents that hardware requirement reporting changes
when a hypervisor is detected: [Hyper-V requirements](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements).

Sandbox remains the first candidate to evaluate after owner-elevated feature
results arrive. It has not been confirmed available, and no guest is selected.
If its UWP/graphics/isolation prerequisites cannot be met, assess a full VM;
Hyper-V availability alone does not guarantee a hardware D3D11 path.

## Independent results for a future approved run

| Evidence stage | Acceptance | If hardware rendering is unavailable |
|---|---|---|
| Package registration | Successful package deployment with exact identity/dependency/signature checks | Retain PASS if actually established; registration does not require a claim of rendering success. |
| Process/UWP activation | Evidence attributable to this fresh activation, such as a newly bound receipt or process/activation observation | Retain established evidence; a missing window alone is not proof of failed package registration. |
| Durable receipt persistence | Newly written parseable receipt with correct case, run/source/payload binding; preserve numeric failure reason | A durable terminal failure receipt can establish writing even though D00 overall did not pass. No receipt means persistence unproven. |
| Full native-control identity/hash/resource observation | Existing RunNativeControl acceptance, not inferred from registration alone | BLOCKED/not reached if renderReady is false, because current code skips RunNativeControl. |
| Graphics/UI prerequisite | Actual renderer initialization result; distinct from formal D06 graphics testing | Report prerequisite failure if observed; formal D06 remains NOT EXECUTED/BLOCKED. |
| Overall current D00 | Existing unmodified terminal receipt and acceptance rules | Preserve FAILED/DIAGNOSTIC_UI_UNAVAILABLE if emitted. Do not relabel as full PASS merely because registration/receipt persistence succeeded. |

Source: `phase6b1-diagnostics/diagnostics/RuntimeDiagnostics/src/app.cpp:96-136`
attempts D00 receipt creation before checking renderReady. If false it writes
FAILED/DIAGNOSTIC_UI_UNAVAILABLE instead of calling RunNativeControl. Therefore
useful activation/persistence evidence may survive a renderer failure, but is not
guaranteed. Source, schema, D00-only lock and package remain unchanged.

All execution-stage results above are currently NOT EXECUTED. This addendum
defines reporting distinctions, not new successful tests or weaker acceptance.
