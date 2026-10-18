> **Phase 6B.1a:** The default configuration is now **D00Only**. See
> [D00-only build and safety contract](docs/D00-ONLY.md).
> Earlier Java21 instructions describe the retained Java21Smoke configuration;
> they do not authorize JNI execution and do not apply to the D00-only package.
> Historical build/status evidence below refers to f77bd4c, not the new artifact.

# Separate diagnostic build

This original build compiles diagnostic sources and Java21 fixture classes, statically inspects outputs, and optionally creates an **unsigned** APPX. It never runs the built app, VM or class files, signs a package, creates certificates, deploys, downloads dependencies or changes the production launcher.

From this folder, after source review:

```powershell
.\build.ps1 -JavaHome21 'C:\explicit\approved\jdk21' -Package
```

Required existing tools are MSVC 14.44.35207 x64 (including UWP `lib/x64/store`), Windows SDK 10.0.26100.0, C++/WinRT headers, explicit trusted x64 JDK21 compiler/JNI headers, and Python standard library. Parameters `-MsvcRoot`, `-SdkRoot`, `-SdkVersion` and `-Python` select reviewed installed paths without installing anything. Missing tools fail. No script from the production build is sourced.

Each invocation creates a unique ignored `out/<timestamp-guid>/` with objects, local compiler logs, package staging, tool/source/artifact/license hashes and numeric tool exit codes in `build-receipt.json`. Logs may contain local paths and remain local. The receipt sanitizes the user's home prefix in tool paths. The package includes original generated PNG assets, synthetic classes, fixed profiles and hash inventories. `static-verification.json` distinguishes static checks from execution. `-Package` uses the existing MakeAppx tool without signing. The resulting APPX needs a separately reviewed signing/deployment procedure and VCLibs framework dependency; it is not an executable test receipt or evidence of console certification.

Default builds package **no Java runtime**. `runtime-inventory.json` says `available:false`; static verification reports `BLOCKED_RUNTIME_NOT_SUPPLIED`, and a future smoke invocation records status `BLOCKED` with reason `APPROVED_RUNTIME_NOT_SUPPLIED`. Compiler/header availability does not authorize copying its desktop runtime. No network, authentication, broad filesystem, microphone, full trust or code-generation capability is declared.

An optional runtime can only be included when both `-RuntimeRoot` and `-RuntimeInventory` are explicitly supplied. This is a future input contract, not approval to choose a runtime now. The JSON uses the template's camelCase fields and requires `available:true`, `approvedForDiagnosticPackaging:true`, `expectedJavaMajor:21`, `architecture:"x64"`. Each `files` record requires canonical forward-slash `path` relative to RuntimeRoot, exact lowercase `sha256`, fixed role, reviewed `sourceId`, relative `licensePath` and exact `licenseSha256`. Inventory coverage must equal every source file; symlinks/junctions, traversal, unlisted files, mismatches and non-x64 DLLs fail. Include the runtime `release` and license files as inventory entries too. Package paths are `Runtime/<path>`.

`loadOrder` must equal the template's six runtime-relative paths in order. The build generates `fixtureFiles` for `Fixtures/classes/diagnostic/JniSmoke.class`; RuntimeRoot does not supply fixtures. Each copied runtime file is checked again in the finished package. These checks establish bounded identity and provenance records, not JVM/native compatibility or a grant of redistribution rights. Review source/URL, license and package-policy requirements before admitting any runtime/native artifacts.

`tools/verify_artifacts.py` performs only standard-library static file/PE/classfile/XML/hash checks and original PNG generation. It does not load DLLs or invoke a JVM. The checks reject unexpected capabilities and identity/entrypoint/architecture changes; they cannot establish API availability, graphical behavior, dependency satisfaction, package activation or hardware success.
