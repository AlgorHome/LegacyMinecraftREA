> **Phase 6B.1a:** The default configuration is now **D00Only**. See
> [D00-only build and safety contract](D00-ONLY.md).
> Earlier Java21 instructions describe the retained Java21Smoke configuration;
> they do not authorize JNI execution and do not apply to the D00-only package.
> Historical build/status evidence below refers to f77bd4c, not the new artifact.

# Phase6B.1 compilation and review status

Date: 2026-10-17 (America/Chicago). Isolated review branch:
`research/phase6b1-runtime-diagnostics`, based on
`d1453434ceefe73bef5aff497194e09f39dde7e1`.

| Check | Result | Limit |
|---|---|---|
| Original Java fixture compilation | PASS, classfile65 / Java21 | Class was never run |
| Native app/report/control/JNI compilation | PASS, MSVC14.44.35207 / SDK10.0.26100.0 / x64 | Diagnostic EXE/candidate JVM were never run |
| Native link | PASS, x64 AppContainer, UWP CRT imports | Not activation/API certification |
| Compiler/link warning scan | No C/LNK warnings in final build | Not an exhaustive defect assessment |
| Static source/input/package checks | PASS; current build input hashes match compiled snapshot | Hashes/structure, not runtime behavior |
| MakeAppx | PASS; unsigned diagnostic APPX produced | No certificate, signing, trust-store change or deployment |
| Native D00 activation | NOT EXECUTED | Separate owner execution approval required |
| Java21 JNI smoke | BLOCKED / NOT EXECUTED | No approved native runtime supplied or bundled |
| Signing | BLOCKED | Separate certificate/publisher/trust inputs and authorization needed |
| Xbox/Windows diagnostic execution | NOT EXECUTED | No package registration, EXE/class invocation, Device Portal or hardware contact |

Final build output directory, relative to this project:
`out/20261017-113425-45caeffd/`. Generated files are deliberately ignored by Git.

- Native EXE SHA256:
  `e349811bfa2641c4f880a80108d04eddf575588980c31ab016b07c13471ce349`.
- Java fixture SHA256:
  `33cfb26683923979bf734c1b9a20f90872b958294425e4e993b3839ff3565b50`.
- Unsigned APPX SHA256:
  `930f6844eea2777433886d1d347b6925206d2cfd51fccf4a36b1206ab8cf9f08`.

The unsigned APPX is89,592 bytes and contains the original native program,
synthetic class, generated assets, profiles, inventories and Apache-2.0 license.
It contains no JVM, Minecraft content, proprietary launcher code or credentials.
ZIP CRCs and every staged payload byte were checked without executing anything.
The build procedure is reproducible from the recorded tools/inputs; build IDs,
timestamps and packaging metadata may change artifact bytes on another run.

[COMPILATION-RECEIPT.json](COMPILATION-RECEIPT.json) records actual successful
compiler/static-tool exit codes, tool/source/header/license hashes and explicit
unexecuted/blocked outcomes. Local raw build logs remain outside Git. Earlier
integration failures (Python command selection, Windows macro collisions and
missing WinRT collection definitions) were corrected before this final build.

Native-control persistence and UI, watchdog races/timeout behavior, actual
dependency resolution and the JNI oracle have been source-reviewed and compiled,
but have not been experimentally validated. In particular, compilation and
unsigned packaging cannot satisfy D00 or the Java21 runtime acceptance criterion.
Production runtime/authentication/entitlement files and the sealed Phase6A dossier
were not modified. No signing, push, deployment or execution is claimed.
