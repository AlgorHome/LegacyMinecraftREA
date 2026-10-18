RuntimeDiagnostics was orginally supposed to be in the folder 'phase6b1-diagnostics'.
But it was mistakenly placed here.



> **Phase 6B.1a:** The default configuration is now **D00Only**. See
> [D00-only build and safety contract](docs/D00-ONLY.md).
> Earlier Java21 instructions describe the retained Java21Smoke configuration;
> they do not authorize JNI execution and do not apply to the D00-only package.
> Historical build/status evidence below refers to f77bd4c, not the new artifact.

# LegacyForge Runtime Diagnostics — Phase 6B.1

Separate x64 UWP diagnostic application. Baseline comparison: LegacyForge
`d1453434ceefe73bef5aff497194e09f39dde7e1`. This project does not link or modify
the production launcher, authentication, entitlement handling or release package.

Only two scenarios belong to this implementation:

- **D00**: native package activation, isolated app-local receipt persistence,
  package/executable identities and bounded resource observations. It does not
  validate graphics, audio, input, JIT or Minecraft compatibility.
- **S21 / D03**: one synthetic Java21 JNI initialization/execution attempt, with
  native-load and version-query stages recorded separately. It uses the exact
  `JNI_VERSION_21` request; it does not fix, patch or negotiate the production call.

Java17/8/25, 1.12.2 providers, mod loaders, gameplay and the 56-target matrix are
out of scope. No Minecraft account, client, assets or launcher binaries are used.
Original sources/fixtures are covered by the repository Apache-2.0 license.

## Review and execution boundary

Source/build/package review is authorized. **Do not launch the generated EXE,
load a candidate JVM, install/sign/deploy the APPX or contact a console until the
owner separately approves those exact artifacts and actions.** Build commands
compile/package only; they do not register or activate an application.

The native control is saved independently before Java can be selected. The JVM
runs off the CoreWindow dispatcher. A watchdog can record a deadline, but cannot
cancel an arbitrary blocked driver/JVM call or guarantee progress after a process
crash. Checkpoints and the separate D00 receipt retain the last durable evidence.
There is no thread abort, automatic retry, alternate runtime or second JVM.

## Layout

```text
include/diagnostics.h         shared receipt/probe contract
src/app.cpp                  independent CoreWindow UI and bounded runner
src/report.cpp               sanitized JSON/checkpoints/hashing/resources
src/native_control.cpp       D00 only, no JVM
src/jni_smoke.cpp             fixed Java21 package loader/JNI smoke
java/diagnostic/JniSmoke.java original deterministic Java/native fixture
package/Package.appxmanifest  distinct package identity, minimal permissions
build.ps1                    offline compiler/unsigned-package orchestration
runtime-inventory.template.json approved-runtime metadata contract
tools/                       file/package validation, never target execution
docs/                        architecture, build and owner acceptance notes
out/                         ignored local compiler/package artifacts
```

## Runtime inputs

No native JVM is included in source control or selected automatically from a
desktop JDK. The compiler JDK supplies headers and compiles the original Java
fixture only. Default builds deliberately contain no Java runtime and must
report **BLOCKED** for S21 when eventually run.

An optional runtime package requires an explicitly supplied inventory with x64
Java21 identity, every included file's hash, source and license provenance, and
approval for diagnostic packaging. A license assertion does not itself establish
UWP compatibility or authorize execution. A missing/changed dependency, failed
load or rejected JNI request stays an explicit result; no download or speculative
runtime modification is performed to make it succeed.

## Documentation

- [Build instructions and package requirements](docs/BUILD.md)
- [Architecture, output and timeout contract](docs/ARCHITECTURE.md)
- [Short Series X acceptance checklist](docs/XBOX-ACCEPTANCE.md)
- [Compilation and review status](docs/BUILD-STATUS.md)

The Phase6A/6B research specifications live in the separate research workspace
under `docs/research/legacy-launcher` and
`docs/research/phase-6b-runtime-validation`. The production source call retained
for comparison is `MC.Xbox/launch/minecraft_launch.cpp:1352–1363` at the pinned
commit; line1353 assigns `JNI_VERSION_21` before `JNI_CreateJavaVM`. No runtime
failure is inferred from that source alone.

Review this project's diff from the approved pin on branch
`research/phase6b1-runtime-diagnostics`; all new tracked files must remain under
`diagnostics/RuntimeDiagnostics/`. Generated packages, runtime files, local
reports and signing material must not be committed.
