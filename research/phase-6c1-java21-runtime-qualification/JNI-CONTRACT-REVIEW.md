# JNI21 contract review - no calls implemented

Primary specification: [Java21 Invocation API](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/invocation.html), [JNI functions/version](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/functions.html), [types](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/types.html). These specify embedding contracts, not Xbox runtime approval.

VERIFIED local include/jni.h: JNI_VERSION_21=0x00150000; JNI_VERSION_1_8=0x00010008. Return definitions include JNI_OK0, JNI_ERR-1, JNI_EVERSION-3, JNI_ENOMEM-4, JNI_EEXIST-5. No JNI_VERSION_17 constant is invented. Headers' presence establishes definitions, not whether the local JVM accepts a request.

VERIFIED actual jvm.dll named exports (offline PE parser and independent Microsoft dumpbin agree):

- JNI_GetDefaultJavaVMInitArgs: version/configuration query; no JavaVM required.
- JNI_GetCreatedJavaVMs: VM enumeration contract; discovery is not VM creation.
- JNI_CreateJavaVM: actual VM creation/initialization entry.

DestroyJavaVM, AttachCurrentThread, DetachCurrentThread, GetEnv and AttachCurrentThreadAsDaemon are JavaVM-table operations, not three more required DLL export names. JNI_OnLoad is a native-library hook, not a substitute for JNI_CreateJavaVM. None was called here.

| Stage | Establishes if successful | Does not establish |
| --- | --- | --- |
| Static PE export inspection | Named export metadata exists in pinned bytes | DLL loads, code initializes or any query works |
| J0 load-only plus export address lookup | Selected package-native load and expected export resolution | JNI version acceptance, live VM, Java/JIT or game |
| J1 JNI_GetDefaultJavaVMInitArgs | Declared request profile returns documented status/data | Live VM/bytecode execution or correct future JVM options |
| J2 JNI_CreateJavaVM | JNI_OK with nonnull VM/JNIEnv | Correct fixture, exception-free run or cleanup by itself |
| J2 original bytecode return | Correct known value on identified runtime, with no unexpected exception | JIT, all modules/natives, loaders or Minecraft |
| J2 shutdown observation | Declared cleanup stage result if actually returned | Automatic restartability, complete OS/driver reclamation |

Plan one production-equivalent JNI21 query profile per cold activation; JNI1_8 is a separately approved compatibility control, never a silent retry after failure. Record numeric request/response and returned argument structure, exact runtime and profile hashes. A designed rejection can PASS its negative oracle only, not the positive version gate. No production JNI_VERSION_21 change proposed.

Actual Java proof requires an attributed JNI_OK VM/JNIEnv, observed runtime version, original class/bytecode hash, verified deterministic method result, explicit exception checks and durable final evidence. Use the JNIEnv only on its owning thread. Release local references and separately record VM teardown; one VM per fresh process. DestroyJavaVM may block; neither native watchdog nor an extra thread can safely cancel it. No speculative unload/recreate workaround.

Initial J2 proposes -Xint only as a Java-method JIT control. Do not infer JIT from speed, export availability or even the correct checksum. Later JIT proof needs a real compilation witness; it is outside J0-J2 initial acceptance.
