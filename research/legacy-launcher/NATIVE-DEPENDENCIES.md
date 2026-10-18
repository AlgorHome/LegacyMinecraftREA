# Native dependency and platform boundary audit

Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.

## Coverage [E14]

All 239 installed target EXE/DLL files and 6 pinned Mesa DLLs were parsed. Recursive ZIP inspection added46 DLL occurrences from native archives (up to two nested JAR levels; 64 MiB per entry). Total 291 PE observations: 260 x86-64, 16 x86 and 15 ARM64. No parser errors were recorded. Duplicate archive/extracted copies are occurrences, not291 distinct runtime-loaded modules.

The audit recorded1,714 standard/delay-import module edges,46 delay-import module occurrences and 56,489 named-export entries across these images. External/system/API-set edges are explicitly unresolved. Candidate matches are by module basename, role and CPU; they do not emulate loader order. Graph metadata is in evidence/native-dependency-graph.json; no DLL contents are published.

Representative import-module sets independently matched GNU objdump for TL.exe, selected GLFW, OpenAL and Java 17 JVM. Eight selected Java classes also matched trusted javap checks, including original process launch, original/installed signature code and profile persistence. These12 analyzer cross-checks passed; they are **not**12 passed target/runtime tests.

## Actual pinned adaptation [E15]

- [MC.Xbox/launch/minecraft_launch.cpp:663](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/minecraft_launch.cpp#L663): packaged runtime preload; JNI_CreateJavaVM at 1335 onward; native path overrides1179–1203.
- [MC.Xbox/launch/runtime_manager.cpp:1079](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/launch/runtime_manager.cpp#L1079): runtime family/patch selection; PrepareTargetNativeDir1310 selects/extracts natives and overlays packaged GLFW.
- [glfw_shim/glfw_uwp.cpp:1563](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/glfw_shim/glfw_uwp.cpp#L1563): PollGameInputGamepad uses GameInput readings; controller-to-GLFW buttons/axes conversion and keyboard/mouse bridges exist.
- GLFW exports at 3952 swap through WGL bridge or EGL; glfwGetProcAddress3987 tries WGL, EGL and packaged OpenGL entrypoints. A working backend requires actual context/function/presentation validation.
- glfwExtensionSupported (line 3979) always returns false; glfwGetWin32Window (line 4123) returns NULL. glfwGetJoystickHats returns no hats and glfwUpdateGamepadMappings returns success without applying supplied mappings. These are **Confirmed interface limitations**, not proof every game/mod fails. Test consumers that use these interfaces.
- [MC.Xbox/App.cpp:112](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/App.cpp#L112): suspension logs/marker/telemetry and resume marker clearing exist. This does not prove game audio/context/resource restoration or safe native/JVM reuse.

Pinned Mesa DLLs are opengl32, libgallium_wgl, dxil, spirv_to_dxil, vulkan_dzn and z-1. The import graph shows app CRT dependencies in several Mesa components; opengl32 imports libgallium_wgl and the latter imports z-1. Presence of vulkan_dzn does not prove the selected Minecraft path uses Vulkan. dxil includes desktop-named imports; import spelling alone does not establish Xbox API compatibility.

## Package and missing runtime artifacts

Package.appxmanifest declares x64 Windows. Universal and VCLibs plus internet/private networking, runFullTrust, broadFileSystemAccess, expandedResources and microphone. No explicit codeGeneration declaration was found in that checked manifest. This is a recorded declaration set, not proof of a capability grant, certification or JIT prohibition. Microsoft's documented UWP JIT route exists; exact modified-runtime memory/API behavior requires validation.

No built APPX/MSIX/LegacyForge executable, packaged JVM or built GLFW shim was present in the pinned checkout inventory. Six Mesa binaries can be audited, but the exact deployed JVM/shim package cannot be hashed or tested from absent files. All catalog runtime tests remain BLOCKED, with the source comparison retained for all 56 rows.

## Remaining load-time unknowns

Static import/export inventories cannot resolve all GetProcAddress targets, generated code, registration via JNI_RegisterNatives, actual dependency search order, device drivers, shader/runtime feature support or lifecycle outcomes. Archive x86/ARM64 natives must not be selected merely because their files exist; the actual Xbox package/native selection is x64. No audit result declares arbitrary Windows DLLs UWP-compatible.

Oracle's [JNI invocation contract](https://docs.oracle.com/en/java/javase/17/docs/specs/jni/invocation.html) makes requested JNI version part of the API contract. The pinned host requests JNI_VERSION_21 while Java 17/legacy runtime selections exist. The discrepancy is confirmed; its exact packaged-runtime response is BLOCKED pending those binaries and an approved isolated/device test. No target JVM was loaded through ctypes, JNI, reflection or another host during this investigation.
