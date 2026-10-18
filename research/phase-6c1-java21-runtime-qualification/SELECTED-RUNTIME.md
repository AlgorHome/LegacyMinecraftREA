# Selected candidate - static qualification only

Selection: Eclipse Adoptium, Eclipse Temurin HotSpot **21.0.12.1+1-LTS**, Windows x64 JDK. Overall readiness **BLOCKED** for a future J0, not rejected as definitively incompatible.

## Publisher pin

[Official release](https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.12.1%2B1), published `2026-08-19T12:10:19Z`. Archive: [OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip](https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip);205,073,461 bytes. Publisher-reported SHA256:

`f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e`

Checksum URL: https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip.sha256.txt

Detached-signature URL: https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip.sig

Artifact metadata URL: https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip.json

These are DOCUMENTED expected inputs. No archive, signature, key or source tarball downloaded; no archive hash/signature verification claimed. No exact archive top-level member path can be asserted before approved archive inspection. The extracted directory name is not proof of archive layout.

## Local candidate

`C:\Users\arinze\AppData\Local\LegacyForge\jdks\jdk-21.0.12.1`. VERIFIED local release declares IMPLEMENTOR Eclipse Adoptium, JAVA_RUNTIME_VERSION21.0.12.1+1-LTS, OS_ARCHx86_64, OS_NAMEWindows, Hotspot/JDK, date2026-08-18. Source fields identify adoptium/jdk21u and build source e6ba7dec3d07654074559310376a3ae89da5f4ac. Those fields were hashed, not independently matched to a source build.

Full inventory:490 files/343,823,876 bytes, including243 legal files;127 PE images all x64. No file changed or loaded. Each local hash below is independently computed from bytes and distinct from the publisher's ZIP checksum.

| Local relative file | Bytes | Local SHA256 |
| --- | --- | --- |
| `release` | 1664 | `07117c72ce033949c14878e07fbf2fe23f59a1f8c90a6d1351b5c89099847ce7` |
| `NOTICE` | 2400 | `c02756bcd9fa8191bf0fda4451bc018414dd44ee35bf09922c24377a475e4b5a` |
| `include/jni.h` | 76018 | `99e64ebbe749e6df284f852f11b3c73f6ea97baf15120428f40f887fe0616e61` |
| `include/win32/jni_md.h` | 1510 | `3cacac1e4802ec246ea7c0c6772d4ac40c9f7255d4df095cfffe601137689771` |
| `bin/server/jvm.dll` | 13919872 | `3df13bd73c7dbeef26693cef664b4ede84649720f7a12f0203215a65656d25f4` |
| `bin/java.dll` | 122488 | `9b484b6a703e890292ab3bdb43c81c17eac1eecce585a28205d32ae42c3bc049` |
| `bin/jli.dll` | 89720 | `1e189c727f043e924cb8779b673702ba836faa7c9e752e2743b69cde70a2c1fb` |
| `bin/jimage.dll` | 34424 | `8123408896077c9fcdcb0d5809d5bdf6e96a3e3a1a15bec2dc7432f68b42acf4` |
| `bin/verify.dll` | 54912 | `dd1d4af0d2c1348f29a143c358922be9d071addbf0d103d15910332cf3b74a58` |
| `bin/zip.dll` | 87168 | `a9ae352e10a098403f497ea69442818be1148a737792a21a7d568a4836d2dc06` |
| `bin/net.dll` | 60024 | `da8fe694d71e287cb1c74d478d8854f55d6ea26aba17e58050b772a0a7ef79d8` |
| `bin/nio.dll` | 80504 | `50cddbcea627390ed9dee80da7ca9d1942c4c7b1e3f138276693d487a6dd589c` |
| `bin/vcruntime140.dll` | 119888 | `02c6aa0e6e624411a9f19b0360a7865ab15908e26024510e5c38a9c08362c35a` |
| `bin/vcruntime140_1.dll` | 49640 | `7dd9aa02e271c68ca6d5f18d651d23a15d7259715af43326578f7dde27f37637` |
| `bin/msvcp140.dll` | 575056 | `a4c2229bdc2a2a630acdc095b4d86008e5c3e3bc7773174354f3da4f5beb9cde` |
| `bin/ucrtbase.dll` | 1361448 | `2e5fb14b7bf8540278f3614a12f0226e56a7cc9e64b81cbd976c6fcf2f71cbfb` |
| `lib/modules` | 140891368 | `cbcbf551210912063c7cb8384474d127568ffc8b4eef1ed57572ae7150591ec7` |
| `lib/jvm.cfg` | 29 | `aa9efb969444c1484e29adecab55a122458090616e766b2f1230ef05bc3867e0` |
| `conf/security/java.security` | 73067 | `7eff0eef66774d0c6a07f6c69fae02d8a7dff9b2ef3d7751af9af87a4dda33e6` |
| `legal/java.base/LICENSE` | 19274 | `4b9abebc4338048a7c2dc184e9f800deb349366bdf28eb23c2677a77b4c87726` |
| `legal/java.base/ADDITIONAL_LICENSE_INFO` | 2114 | `a69bce275ba7a3570af6579cb0f55682cd75fedfcd49e0e8e9022270c447c916` |
| `legal/java.base/ASSEMBLY_EXCEPTION` | 1514 | `75292f03bf23d3db7c985aecc191029b93883200721ed23ed34a2e601463df33` |

LOCAL-RUNTIME-INVENTORY.json enumerates every file and native import/export table. SELECTED-RUNTIME.json records selected fields/publisher expectations; LOCAL-SIGNATURE-OBSERVATIONS.json records six selected file signatures. JVM/Java/JLI signers Eclipse Foundation and CRT signers Microsoft returned Valid on this Windows host. This authenticates those signed PE images under host trust policy, not every unsigned module/config/license file or the whole extracted image.

## Readiness boundaries

VERIFIED local identity/PE/hash/export observations; DOCUMENTED official archive/version/license program. UNKNOWN complete archive match, dynamic imports/ordinal/API-set target mapping and package policy. BLOCKED exact package allowlist/CRT-vs-framework decision, provenance closure and future executable approvals. J1/J2 not run; bytecode/JIT/JVM startup wholly unproved on Xbox. No generic desktop runtime automatically becomes a UWP runtime.
