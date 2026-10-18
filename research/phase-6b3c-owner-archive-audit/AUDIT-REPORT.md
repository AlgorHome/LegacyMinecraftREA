# Owner dependency archive audit

2026-10-17, America/Chicago. Read-only inspection of all six VCLibs APPX files.

**Required standard-UWP x64 framework: PRESENT; exact SHA256 match.**

Exact matching dependency:

`C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\x64\Microsoft.VCLibs.140.00_14.0.33519.0_x64.appx`

SHA256: `9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283`.

All six manifests have Framework=true and the exact publisher:

`CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US`

| # | Exact Name | Version | ProcessorArchitecture | SHA256 |
|---|---|---|---|---|
| 1 | Microsoft.VCLibs.140.00.UWPDesktop | 14.0.33728.0 | arm64 | 831118f2f5cac8e29284e4ecc23bf4236436ccc2ea4a7c225c4946f8cfd29dd3 |
| 2 | Microsoft.VCLibs.140.00 | 14.0.33519.0 | arm64 | c73d0f55dda331f9dcbefc99ff5a420b62120773d2917387639382aa478533ee |
| 3 | Microsoft.VCLibs.140.00.UWPDesktop | 14.0.33728.0 | x64 | 077a3d1a5d0622bd3004dca85f5e192d6e98ec79b83d4aa06766759ea6c09c3d |
| 4 | Microsoft.VCLibs.140.00 | 14.0.33519.0 | x64 | 9c17b521f9d690a1f504da5108ed6eec5669eb3a8fd1331eef43e40d84e74283 |
| 5 | Microsoft.VCLibs.140.00.UWPDesktop | 14.0.33728.0 | x86 | 596c7175c0b0fa27ed292a44f4681f687720a77e34e007bf6c403d1940e46005 |
| 6 | Microsoft.VCLibs.140.00 | 14.0.33519.0 | x86 | 7ba6ea7bc32cd58b7e0683da588796086accfb74efb7a3e525e9f8014d2ad663 |

Exact paths (same numbered rows):

1. `C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\arm64\Microsoft.VCLibs.140.00.UWPDesktop_14.0.33728.0_arm64.appx`
2. `C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\arm64\Microsoft.VCLibs.140.00_14.0.33519.0_arm64.appx`
3. `C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\x64\Microsoft.VCLibs.140.00.UWPDesktop_14.0.33728.0_x64.appx`
4. `C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\x64\Microsoft.VCLibs.140.00_14.0.33519.0_x64.appx`
5. `C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\x86\Microsoft.VCLibs.140.00.UWPDesktop_14.0.33728.0_x86.appx`
6. `C:\Users\arinze\Desktop\DesktopAppInstaller_Dependencies\x86\Microsoft.VCLibs.140.00_14.0.33519.0_x86.appx`

## Matching-package checks

- ZIP CRCs and all manifest reads: PASS.
- Candidate bytes equal the previously acquired official Microsoft reference byte-for-byte; expected SHA256 matches.
- Microsoft signature: prior SignTool verification PASS (exit0, zero warnings/errors), signer Microsoft Corporation; previous signed package and verification-log hash rechecked. No fresh SignTool, chain or revocation check was run during this no-executable audit.
- CRT exports: freshly parsed PE import/export tables as data. All17 required imports present: MSVCP140_APP8, VCRUNTIME140_APP8, VCRUNTIME140_1_APP1; all three DLLs x64. No module loaded.
- UWPDesktop is a distinct package and is not selected. ARM64/x86 are not selected for the x64 diagnostic.

The correct dependency is available locally. Whether Xbox already has the framework remains UNKNOWN; this audit does not authorize installation. Applicable licensing/approval gates from Phase6B.3b remain unchanged.

Existing diagnostic certificate D6245FB640D520EDED8F8A987B364BCADE01D01D is present; public metadata read only. No private-key handle was opened, certificate changed or package signed. Unsigned diagnostic hash remains `ecb53bb12ac86600df22c5d80608f908f10371787be9aa96e06d53011c8c9558`.

No archive files modified, dependency installed, Xbox contacted, target binary executed or production file changed. Only this separate audit report/evidence was written.

Full machine-readable evidence: [ARCHIVE-AUDIT.json](ARCHIVE-AUDIT.json).
