# Native dependency inventory

VERIFIED by read-only PE parsing of all127 local DLL/EXE images; JNI exports independently cross-checked with existing Microsoft dumpbin /exports. No Java code or DLL entry point executed. Full named imports/exports, delay imports, forwarders, machine/subsystem flags and hashes in LOCAL-RUNTIME-INVENTORY.json. The parser is offline metadata analysis, not a platform loader/emulator.

## Observed roles and paths

Future packaging prefix is only a proposal: runtime/java21/. Preserve the verified relative layout beneath it; no files packaged here.

| Relative role | Observation | Requirement classification |
| --- | --- | --- |
| bin/server/jvm.dll | Exports JNI_CreateJavaVM, JNI_GetDefaultJavaVMInitArgs, JNI_GetCreatedJavaVMs | VERIFIED invocation DLL; planned J0 target, never called here |
| bin/vcruntime140.dll, vcruntime140_1.dll | JVM imports both; files present/signed | VERIFIED direct CRT dependencies; package/framework resolution still reviewed separately |
| bin/api-ms-win-crt-*.dll and bin/ucrtbase.dll | Local API-set forwarders/UCRT images present | VERIFIED files/forwarding metadata; cannot assume Xbox resolves them by desktop rules or that all should be bundled |
| bin/java.dll | Imports161 JVM symbols plus platform/CRT; delay-loads SHELL32 SHGetKnownFolderPath/SHGetFolderPathW | VERIFIED dependency metadata; future VM dynamic-load necessity/order INFERRED until reviewed |
| bin/jli.dll | Imports COMCTL32 InitCommonControlsEx, USER32 dialog APIs and CRT | VERIFIED desktop-launcher interface; not automatically needed for direct JNI embedding. Do not preload merely to imitate Bandit |
| bin/jimage.dll, verify.dll, zip.dll | Present, hashed; verify/zip use JVM, zip also java.dll | VERIFIED files/imports; exact per-fixture dynamic-load order UNKNOWN |
| bin/net.dll, nio.dll | Network/platform/Java imports; net delay-loads Secur32/IPHLPAPI | VERIFIED metadata; not permission to access network, not automatically a required J0 preload |
| bin/msvcp140.dll | Present and signed; not a direct JVM import in inspected table | VERIFIED file, conditional dependency only; no blanket required-library claim |
| lib/modules |140,891,368 bytes existing runtime module image | VERIFIED bytes; INFERRED necessary core data for J2, java.base included in release module list. No jimage tool invoked |
| lib/jvm.cfg, release, conf/security/java.security and conf tree | Present and independently hashed | VERIFIED configuration/identity files; preserve exact candidate when choosing J2 layout |
| include/jni.h and include/win32/jni_md.h | JNI declarations/constants inspected | Future host compile inputs only; not runtime executable dependencies |
| jmods and JDK executables | Existing tool/module inputs in reference JDK | No need established for J0; do not invoke javac/java/jlink or trim/repackage the reference tree in this phase |
| legal tree/NOTICE |243 files + notice retained | Required licensing input for any proposed redistributed subset; do not drop notices during trimming |

| Selected PE | Immediate imported modules | Delay modules | Named exports |
| --- | --- | --- | --- |
| `bin/server/jvm.dll` | 19 | 0 | 4385 |
| `bin/java.dll` | 12 | 1 | 292 |
| `bin/jli.dll` | 10 | 0 | 19 |
| `bin/verify.dll` | 6 | 0 | 1 |
| `bin/zip.dll` | 8 | 0 | 36 |
| `bin/net.dll` | 11 | 2 | 54 |
| `bin/nio.dll` | 10 | 0 | 206 |

## Closure findings

JVM immediate imports include KERNEL32, USER32, ADVAPI32, POWRPROF, WS2_32, WINMM, VERSION, VCRUNTIME140/140_1 and UCRT API sets. Examples needing policy review: CreateProcessA, LoadLibraryA/ExW, GetThreadContext, SuspendThread, VirtualAlloc/VirtualProtect, AdjustTokenPrivileges, registry calls, MessageBoxA and CallNtPowerInformation. Some imports may never be used by a pure fixture; presence alone does not prove a forbidden call runs or that loading fails. Conversely not using a function in Java does not remove eager loader binding requirements.

JVM-STATIC-CLOSURE.json records13 candidate-local nodes via imports/delay imports and43 after conservatively including all named export forwarders, including UCRT and core API-set helpers. These counts are **not** an approved package allowlist or complete target closure. They overapproximate forwarded exports, do not resolve target API-set mappings/ordinal exports, and cannot enumerate runtime GetProcAddress/LoadLibrary paths. External modules remain unresolved against Xbox; mapping them to similarly named host System32 DLLs would not prove console compatibility.

## Framework decision

Microsoft.VCLibs.140.00 x64 UWP was previously owner-observed on the console. That does not prove its exports resolve the exact desktop CRT ABI used here. The candidate contains app-local Microsoft CRT/UCRT images; whether a future J0 should use licensed app-local CRT or a compatible framework must be reviewed and frozen before build. No additional framework has been proved necessary, and none may be downloaded/installed automatically. No system DLL copying, PATH/cwd fallback or LocalState code-loading workaround.

**Complete binary dependency closure: UNKNOWN; target closure and final module/package policy: BLOCKED.** Static analysis has retired the missing-local-bytes question for this image, not the missing-UWP-loader/runtime experiment.
