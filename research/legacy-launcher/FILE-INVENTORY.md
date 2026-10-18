# File inventory

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

**Confirmed [E04]:** inventory covered the supplied `.tlauncher` tree recursively, including launcher, game, runtime and log directory counts. It did not follow an installer execution or inventory arbitrary user directories. Game saves, account/profile values and log contents were excluded from the publishable inventory.

| Relative directory/file group | Files | Bytes |
|---|---:|---:|
| `legacy.properties` | 1 | 96 |
| `logs` | 4 | 2,284,766 |
| `legacy/Minecraft/tl.args` | 1 | 125 |
| `legacy/Minecraft/TL.exe` | 1 | 409,088 |
| `legacy/Minecraft/tl.properties` | 1 | 1,880 |
| `legacy/Minecraft/unins000.dat` | 1 | 141,107 |
| `legacy/Minecraft/unins000.exe` | 1 | 3,593,603 |
| `legacy/Minecraft/game` | 4,688 | 588,291,591 |
| `legacy/Minecraft/jre` | 774 | 315,398,146 |
| `legacy/Minecraft/launcher` | 74 | 47,507,825 |

```text
.tlauncher/
  legacy.properties                  bootstrap-level settings (values excluded)
  logs/                              historical logs (raw content excluded)
  legacy/Minecraft/
    TL.exe                           x86 Windows wrapper
    tl.args                          bootstrap arguments and settings path
    tl.properties                    launcher preferences (values excluded)
    unins000.exe, unins000.dat        installation bookkeeping
    launcher/
      bootstrap.jar                  outer Spring Boot ZIP with nested JARs
      launcher.jar                   installed application
      libraries/                     launcher dependencies
    jre/
      release, bin/, lib/, legal/     Java 17 launcher runtime
      java-runtime-delta/windows-x64/java-runtime-delta/
                                     Java 21 game runtime
    game/
      versions/1.21.11/               metadata, client, backup, extracted natives
      libraries/                     version libraries and native JARs
      assets/indexes/29.json
      assets/objects/<prefix>/<hash>
      tlauncher_profiles.json         not copied or read for token values
      logs/                          historical only
```

**Confirmed:** launcher.jar contains 1,329 ZIP entries and 1,112 classes. bootstrap.jar contains 116 outer entries and 70 outer classes, plus nested application/dependency JARs; outer counts do not measure nested classes. Its nested libraries include FlatLaf, Gson, JNA, Commons, DBus transports and bootstrap/bridge/common/utils components. Names/version strings describe packaged dependencies, not proof every component loads on Windows. [E02]

**Confirmed:** a game client and cache are already present, not merely launcher components. The selected client JAR is 31,152,600 bytes and matches version metadata SHA-1; its `.bak` has the same SHA-256. Asset index 29 lists 4,591 objects, all present and SHA-1-matching. Of 107 version-metadata library download entries, 75 files are present and all 75 hashes match; the 32 absent entries identify macOS/Linux artifacts. This is a bounded check against local metadata, not authenticated upstream revalidation or a complete launch-readiness verdict. [E04]

**Confirmed:** download/install methods also exist, so this populated installation supports on-demand component acquisition. **Confirmed continuation [E11]:** original installer payload inventory and hashes now identify its launcher/bootstrap and bundled runtime/dependency content.431 installed non-game files match installer payload records; game-cache files are absent from inspected destination declarations. Exact later acquisition/update chronology remains Unknown. See INSTALLER-CONTENTS.

Complete relevant executable/JAR paths and sizes are in `evidence/relevant-files.csv`; selected executable/JAR/native hashes are in PROVENANCE. Static dependency metadata is in `evidence/static-summary.json`. No game contents are included.
