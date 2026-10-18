> **Phase 6B.1a:** The default configuration is now **D00Only**. See
> [D00-only build and safety contract](D00-ONLY.md).
> Earlier Java21 instructions describe the retained Java21Smoke configuration;
> they do not authorize JNI execution and do not apply to the D00-only package.
> Historical build/status evidence below refers to f77bd4c, not the new artifact.

# Reproducible Windows build and separate APPX requirements

Run from this isolated checkout, never from the production launcher workspace.
The build invokes trusted compiler/static packaging tools only. It does not run
the diagnostic EXE, Java fixture or native JVM, and does not install, sign,
register, activate or deploy a package. It has no dependency downloads.

## Prerequisites

- Windows x64 with PowerShell7, Python3.12+ (standard library only).
- Existing Visual Studio2022 Build Tools C++ toolset. Defaults pin MSVC
  `14.44.35207`; supply `-MsvcRoot` to an explicitly reviewed equivalent.
- Windows SDK `10.0.26100.0`: WinRT/C++WinRT/UCRT headers, x64 libraries,
  MakeAppx and related packaging components. Supply `-SdkRoot` and
  `-SdkVersion` explicitly if changing the reviewed SDK.
- A trusted **Java21 x64 compiler JDK**, supplied explicitly as `-JavaHome21`,
  including `javac`, `include/jni.h` and `include/win32/jni_md.h`. Its runtime is
  **not** copied into the APPX or executed. The compiler produces the original
  fixture with `--release 21` (classfile major65).

The native build uses C++17, `/MD`, `WINAPI_FAMILY_APP`, x64 UWP store libraries
before ordinary toolset libraries, and `/APPCONTAINER`. It links the Windows
runtime, D3D11/DXGI, Direct2D/DWrite and BCrypt for status UI, package storage,
hashes and measurements. UI dependencies are not graphics capability tests.

## Build commands

Compilation only, after confirming the trusted tool paths:

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration Java21Smoke -JavaHome21 '<trusted-installed-java21-jdk>'
```

Build and create an **unsigned**, separately identified APPX:

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration Java21Smoke -JavaHome21 '<trusted-installed-java21-jdk>' -Package
```

Optional `-Python '<trusted-python.exe>'`, `-MsvcRoot`, `-SdkRoot` and
`-SdkVersion` select already installed tools. No install/repair is automatic.
Every run uses a new ignored `out/<timestamp>-<id>/` directory; it does not
recursively clean another build or stop running apps. Compiler diagnostics stay
in local logs; do not publish raw logs without review because paths can appear.

Output includes objects, package staging, compiled original fixture, original
generated tile assets, static import inspection, input hashes, static verifier
results, build receipt and (with `-Package`) `RuntimeDiagnostics.unsigned.appx`.
`build-receipt.json` and `static-verification.json` explicitly distinguish build
success from target execution. A compile/package success is not activation,
runtime support, signing or Xbox validation.

## Default package and runtime-bearing variant

Default package has `runtime-inventory.json` with `available:false`. This is
intentional: D00 can be reviewed/built independently; S21 must remain BLOCKED
when run without approved runtime inputs. Do not silently copy a desktop JDK,
the installed legacy launcher's Java or another package's files.

For a future explicitly approved Java21 package:

```powershell
pwsh -NoProfile -File .\diagnostics\RuntimeDiagnostics\build.ps1 `
  -Configuration Java21Smoke -JavaHome21 '<trusted-installed-java21-jdk>' -Package `
  -RuntimeRoot '<owner-approved-java21-runtime-root>' `
  -RuntimeInventory '<reviewed-inventory.json>'
```

Both runtime parameters are required together. Populate the contract from
`runtime-inventory.template.json`: exact Java21/x64 identity; explicit packaging
approval; fixed load order; every included file's runtime-relative path, SHA256,
role, source identifier and license path/hash. Include the runtime release and
license files in that inventory. The verifier rejects links/path escapes,
unlisted files, absent licenses, changed bytes, wrong architecture and wrong Java
major. It does not prove the runtime is UWP-compatible or that a license assertion
is legally sufficient; provenance/license review remains an owner requirement.

The build copies only the approved inventoried files, regenerates the fixture
hash, and verifies the staged package. Nothing is fetched or executed. Runtime
load order follows a fixed package layout for this diagnostic experiment and
is recorded, not generalized into support for arbitrary JVM distributions.

## APPX and signing requirements

The manifest specifies x64 `AlgorHome.LegacyForge.RuntimeDiagnostics`, publisher
`CN=LegacyForgeDiagnostics`, its own Application Id and executable, UWP partial
trust and a VCLibs framework dependency. It declares no networking, microphone,
broad-filesystem, full-trust, expanded-resource or code-generation capability.
The app-local store is therefore separate from production by package identity.

The owner must supply a valid development signing certificate whose subject
matches the manifest publisher, required trusted framework dependencies, and
separate authorization to sign/install/activate on a specified Series X.
This build creates no certificate/private key, changes no trust store and invokes
no signing/deployment command. Changing publisher/capabilities creates a new
reviewed manifest/package identity; do not reuse the production identity or key
implicitly. An unsigned APPX is a review/build artifact, not a deployable success.

Actual JIT/code-generation behavior, capabilities and runtime policies remain
unproven. This initial smoke does not attempt a JIT feasibility claim or add a
capability to make initialization succeed. Signing, approved-runtime integration
and all execution remain separate pending gates.
