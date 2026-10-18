# UWP compatibility risk register

A normal Windows x64 JDK is not a certified Xbox UWP runtime. None of these risks was resolved through loading or execution here. VERIFIED refers to local static bytes; DOCUMENTED refers to official API behavior; INFERRED/UNKNOWN remain unproven.

| Risk | Evidence | Consequence / future discriminator |
| --- | --- | --- |
| Package graph search | DOCUMENTED LoadPackagedLibrary accepts package-relative paths, not absolute/..; package dependencies govern lookup | One reviewed package-relative route; no PATH/current-directory/System32 fallback to hide failures |
| Desktop native dependency surface | VERIFIED jvm imports USER32/ADVAPI32/POWRPROF/WINMM and desktop-style kernel/process/registry functions | Some symbols or uses may fail policy/target availability. Static presence does not prove a function executes or guarantee failure; J0 records exact loader error |
| Non-AppContainer native PE | VERIFIED selected JVM/Java/JLI images lack APPCONTAINER flag | Desktop build provenance signal, not a sufficient success/failure rule; do not patch PE flags |
| API-set/CRT forwarding | VERIFIED local API-set helper DLLs and forwarded UCRT functions; system exports/ordinals unresolved | Same filename on host or installed VCLibs framework is not ABI proof on Xbox. Review exact package/dependency scheme |
| Delayed/dynamic initialization | VERIFIED java.dll shell delay imports, other libraries use dynamic loading; function export list is incomplete behavioral closure | J0 success only covers selected loads; J2 can encounter new dependencies. DllMain itself executes during loading |
| JLI preload | VERIFIED jli imports COMCTL32/USER32; direct JNI entry is in JVM DLL | Unnecessary launcher-interface loading may add failure points; do not copy Bandit's preload list as a requirement |
| Core runtime data layout | VERIFIED lib/modules/config/release; modular Windows JDK | VM startup needs correct Java home/data discovery; trimming jmods/tools is not proof lib/modules can be omitted |
| Executable memory/JIT | VERIFIED VirtualAlloc/VirtualProtect imports; actual policy UNKNOWN | -Xint removes Java-method JIT as an initial variable, not a guarantee HotSpot uses no generated stubs/executable memory. No capability/security-policy workaround |
| Memory budget | VERIFIED local image disk size343,823,876 bytes; no runtime measurements | Disk bytes are not resident/committed memory. Native1GB observations from another diagnostic do not establish this package's budget |
| Architecture/ABI | VERIFIED all127 local PEs x64; JNI calling-convention headers available | Necessary, not sufficient: instruction requirements, native exceptions/threads, OS APIs and runtime ABI remain |
| Threading/COM | DOCUMENTED JNIEnv is thread-local; JNI spec recommends dedicated VM-creation thread | New harness must own thread/stack and COM state; no borrowed JNIEnv across workers |
| Shutdown | DOCUMENTED DestroyJavaVM can wait for non-daemon threads | Timeout observer cannot forcibly cancel VM creation/destruction; no DLL unload under a live VM or second VM recreation |
| Java IO/security/module behavior | Existing desktop JDK differs from UWP Java path assumptions | Start pure original bytecode with no game, network/auth or optional module patches; later separate IO/ZIPFS cases |
| Input provenance | Valid selected PE signatures but no original archive comparison | Exact full runtime input qualification still BLOCKED; do not conflate a valid DLL with a verified image |

Primary [LoadPackagedLibrary contract](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-loadpackagedlibrary), [JNI Invocation API21](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/invocation.html), [Java21 -Xint](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html). The no-zero-generated-code conclusion is a conservative INFERENCE: interpreted bytecode is not a promise about every internal VM memory mechanism.

Unknown target API closure is the intended future J0 question, not a demand to prove loading before running a loading test. The blocking preparation items are input provenance, explicit allowlist/CRT policy, reviewed known risks and independent approvals. No broad capabilities, registry/token changes, import stubs, patched JVM or trust changes proposed.
