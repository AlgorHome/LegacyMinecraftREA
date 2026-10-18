# JVM and native runtime analysis

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

## Separate launcher Java from game Java

| Layer | Confirmed observation | Evidence |
|---|---|---|
| Native entry wrapper | TL.exe is x86 PE GUI; Launch4j/javaw strings and CreateProcessA call | E05/E06 |
| Installed launcher | 1.169.4+legacy metadata requires Java 11 or newer | E02 |
| Bundled launcher runtime | Azul Zulu 17.0.3, x86-64 Windows, JavaFX modules | E01/E05 |
| Selected game metadata | 1.21.11 requires java-runtime-delta, Java major 21 | E04 |
| Additional installed runtime | jre/java-runtime-delta/windows-x64/java-runtime-delta/release says 21.0.7; native java/jvm files are x86-64 | E04/E05 |

**Unknown:** actual selected executable and flags in a captured live launch; two installed runtimes and metadata are not proof of the active process path. The Java 21 release fields do not identify a vendor; PE VersionInfo separately reports CompanyName Microsoft and ProductName OpenJDK Platform21.0.7. That is an embedded metadata claim, not independent publisher provenance.

## Desktop launch construction

**Confirmed [E03/E04]:** JavaManager chooses local/recommended/custom configurations and remote component manifests. JavaRuntimeLocal maps platform to executable path. MinecraftLauncher constructs the classpath with CompleteVersion.getClassPath and checks file existence; it extracts selected native libraries to a writable directory. Metadata/argument construction supplies `-Djava.library.path`, JNA/LWJGL extraction locations, `-cp`, main class, launcher identity, heap/encoding options and game placeholders. The inspected game placeholders include username, UUID, access token, clientId and XUID; no values were collected.

`launchMinecraft` invokes JavaProcessLauncher.createProcess and ProcessBuilder.start. TL.exe separately has a native CreateProcessA call. These are desktop process assumptions; they are not LegacyForge's startup contract.

## Native and operating-system dependencies

**Confirmed [E04/E05]:** the installed native directory contains x86-64 glfw.dll, lwjgl.dll, lwjgl_opengl.dll, lwjgl_stb.dll, jemalloc.dll, OpenAL.dll and a JNA dispatch DLL. Metadata names LWJGL 3.3.3 components, including additional freetype/tinyfd native archives. An extracted directory snapshot is not an exhaustive dynamic-load inventory.

Static imports show:

- GLFW: USER32/GDI32/SHELL32/KERNEL32; CreateWindowExW and LoadLibrary/GetProcAddress paths.
- JVMs: Windows kernel/user/security/network/timer APIs plus VCRUNTIME140, VCRUNTIME140_1 and CRT API sets; VirtualProtect, process creation and dynamic loading.
- LWJGL components: dynamic loader and symbol lookup APIs; lack of a direct OpenGL DLL import does not prove OpenGL absence.
- OpenAL: WINMM, USER32, OLE32 and dynamic-loading APIs.

The first parser covered standard imports. Continuation E14 expands this to291 PE observations with standard/delay imports, named exports, archive-native inspection and a candidate dependency graph; runtime dynamic resolution, reachability and Xbox API certification remain unverified. No import-list-only conclusion claims every imported desktop API is unavailable on UWP.

**Confirmed historical evidence [E09]:** existing game log lines report LWJGL 3.3.3+5 and OpenAL initialization. They predate this analysis and were not reproduced; they establish recorded messages, not a new verified play session.

## Implications for LegacyForge

**Confirmed [E07]:** PreloadJvm loads packaged modules; RunEmbeddedMinecraft resolves JNI_CreateJavaVM. The project already patches Java filesystem/ZIPFS behavior and routes LWJGL/JNA paths, uses its GLFW shim and selects an OpenGL DLL. It also prevents starting a second JVM in the same launcher process, reflecting lifecycle limits.

**Confirmed source discrepancy:** ResolveJavaRuntimeInfo allows Java 17/8 families, while RunEmbeddedMinecraft assigns JNI_VERSION_21 unconditionally. **Unknown impact:** no older-runtime startup was run. Validate the invocation contract and runtime version per target before proposing a fix. Do not assume newer JNI invocation versions are accepted by an older runtime.

**Unknown:** complete Java/JNI/native ABI compatibility, graphics profile/extension support, audio/input behavior, resource pressure, suspend/resume and every loader's runtime effects on Xbox. See compatibility matrix and staged roadmap; desktop library downloads alone cannot resolve them.

## Archived build classfile baseline [E13]

Static ZIP inspection finds classfile major52 (Java 8-era format) in all 964 archived launcher-namespace classes and 183 archived bootstrap-namespace classes. The archived bootstrap manifest selects ru.turikhay.tlauncher.bootstrap. BootstrapStarter. Classfile format establishes a bytecode baseline, not a proof that all runtime/library/API requirements are Java 8-only. Keep this distinct from installed launcher 11+ metadata, bundled Java 17, and selected game's Java 21 requirement.
