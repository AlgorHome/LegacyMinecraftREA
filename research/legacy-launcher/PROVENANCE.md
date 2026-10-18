# Provenance

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

## Archive and local identity

**Confirmed [E01]:** [Internet Archive item](https://archive.org/details/legacy-launcher-for-minecraft), identifier `legacy-launcher-for-minecraft`, title “Legacy Launcher for Minecraft,” published `2024-02-26 21:00:34` as recorded by the archive. Its creator field claims “Legacy Launcher Team.” The description's independence/safety assertions are uploader claims, not verified provenance or a malware assessment. The archive item exposes no license URL in the inspected metadata.

Source download URL: `https://archive.org/download/legacy-launcher-for-minecraft/LegacyLauncher_Installer_legacy.exe`.

**Confirmed:** local installer `LegacyLauncher_Installer_legacy.exe`, 117,751,681 bytes, SHA-256 `a7c997ba3c3e91c048f80f96f08754948428f6d3fe4001bab79c4ae09d06c5e0`. Local SHA-1 `00bddca8bba387a76d6f18fc942859acf9ff5a60` and MD5 `53eea8664d54198e1989301b12f795da` equal the archive's published values. SHA-256 is locally calculated; the archive metadata did not publish it. These checks bind the local file to the archived item, not to a signed upstream publisher.

Local filesystem creation time was `2026-10-17T05:38:41.2577661Z` (2026-10-17 00:38:41 America/Chicago); last write `05:39:00.5248089Z`. **Inferred:** likely local acquisition on October 17. **Unknown:** exact download event/source chain; timestamps are mutable and no readable Zone. Identifier stream was available. The installer was found in the research workspace during inspection; an initial workspace listing also showed it under the launcher workspace. No agent move/delete operation occurred.

## Separate version identities

| Object | Observation | Status/evidence |
|---|---|---|
| Installer PE version | File `1.159.2.0`; product `rolling`; “Legacy Launcher Stable”; company “Legacy Launcher Team” | Confirmed E01 |
| Installed launcher | `META-INF/launcher-meta.json`: `1.169.4+legacy`, Stable, Java `[11,)` | Confirmed E02 |
| Installed bootstrap | `META-INF/bootstrap-meta.json`: `1.40.3+legacy`; Spring Boot wrapper 2.7.18 | Confirmed E02 |
| Selected installed game | Version JSON and directory `1.21.11`; Java major 21, component `java-runtime-delta` | Confirmed E04 |
| Installer payload comparison | Original launcher 1.159.2/bootstrap 1.32.2 recovered; both differ from installed copies; 431 installed non-game content matches | Confirmed E11; intermediate history Unknown |

The `.tlauncher` directory and old package names do not establish equivalence with another similarly named product.

## Signatures, packaging and architecture

**Confirmed [E01/E05]:** Get-AuthenticodeSignature reports `NotSigned` for the installer and TL.exe. They are x86 PE32 GUI images (subsystem 2). The installed JVM images are x86-64 PE32+; java.exe uses console subsystem 3 and javaw.exe GUI subsystem 2. Wrapper CPU architecture is independent of game CPU architecture. Installer and uninstaller contain Inno Setup data markers. **Confirmed continuation [E11]:** Inno Unicode6.1.0 storage-format blocks and the complete770-record solid payload were decoded without running the installer; every declared content hash validated. Exact compiler release and historical install/update actions remain Unknown. See INSTALLER-CONTENTS.

**Confirmed:** bundled Java 17 java.exe reports Azul Zulu 17, version 17.0.3, Authenticode status `Valid`. Signer subject `Azul Systems, Inc.`, issuer DigiCert SHA2 Assured ID Code Signing CA; thumbprint `2BAACB41471E70059550B6FC7DE2BBC09B09F795`; certificate validity March 20, 2020 to June 18, 2023 UTC; timestamp subject DigiCert Timestamp 2022 - 2. A historical signing certificate's expiry alone does not override the returned Windows validation status. No standalone certificate-chain audit or revocation-policy analysis was performed. See sanitized signatures evidence for exact metadata and Java 21 result.

## Licenses and publication boundary

**Confirmed [E10]:** launcher `LICENSE.txt` references Apache/MIT third-party projects, Minecraft EULA-covered modified content, and CC BY-SA icon packs; bundled JRE includes module legal files and OpenJFX licensing. This is not evidence of a blanket license to reproduce the launcher or its resources. Archive availability and an “open_source_software” collection name do not establish redistribution rights.

The [Minecraft EULA](https://www.minecraft.net/en-us/eula) restricts redistribution of Mojang content. This report records a conservative publication boundary rather than a legal clearance: publish independently written behavior descriptions and curated metadata; retain proprietary artifacts, tokens, assets and reconstructed listings locally. No software was committed or redistributed by this investigation.

## Relevant hashes

Paths beginning `legacy/` are relative to the local launcher workspace; installer path is relative to the research workspace.

| File | Bytes | Format / CPU / subsystem | SHA-256 |
|---|---:|---|---|
| `LegacyLauncher_Installer_legacy.exe` | 117,751,681 | PE32 / x86 / subsystem 2 | `a7c997ba3c3e91c048f80f96f08754948428f6d3fe4001bab79c4ae09d06c5e0` |
| `legacy/Minecraft/TL.exe` | 409,088 | PE32 / x86 / subsystem 2 | `2b11f487e853e952dc677071202cbe25d6800ccaf3f93a3232c5eed715a1c033` |
| `legacy/Minecraft/unins000.exe` | 3,593,603 | PE32 / x86 / subsystem 2 | `46b85011af3c4fb909e6795cb4d87cb72f7814f81bde4507ce1eea4e3bebf781` |
| `legacy/Minecraft/launcher/bootstrap.jar` | 11,026,138 | ZIP/JAR | `09ba7517c8a9b30780ff9a6de230b8905247835ae0da914d66991e2b3b4b6c4e` |
| `legacy/Minecraft/launcher/launcher.jar` | 5,496,812 | ZIP/JAR | `364b9add9a3b0e74e553439b3f0e33a573bb5d28667adc028180d509b0459eec` |
| `legacy/Minecraft/jre/bin/java.exe` | 47,344 | PE32+ / x86_64 / subsystem 3 | `88929241f30cbb0ba439bfab1cd82cf6d092f776e5c73a452f80ed465355adec` |
| `legacy/Minecraft/jre/bin/javaw.exe` | 47,344 | PE32+ / x86_64 / subsystem 2 | `3850d4f443b2a97014a1dcb94db893f0b3396201a8573aa4c4b967ff61528ac6` |
| `legacy/Minecraft/jre/bin/server/jvm.dll` | 12,665,584 | PE32+ / x86_64 / subsystem 2 | `064a55423c55802d3ae7147c4f33d30d79d9b7f4f339c99fcb30c8759d0f8268` |
| `legacy/Minecraft/game/versions/1.21.11/natives/glfw.dll` | 496,128 | PE32+ / x86_64 / subsystem 3 | `affa7e54eb0dedce4a5721c327c1a16035edbbd039cd402e08107d6d2d55eb1a` |
| `legacy/Minecraft/game/versions/1.21.11/natives/jemalloc.dll` | 398,336 | PE32+ / x86_64 / subsystem 2 | `9abf0095066ebab37b78968e11370a8078313e48cb5be8eda01f67623c6a6248` |
| `legacy/Minecraft/game/versions/1.21.11/natives/jna4102832794457777779.dll` | 273,408 | PE32+ / x86_64 / subsystem 2 | `5a7ff949f6d93d86491eb5b26b1cfc60051168a60622650224b89995ac420023` |
| `legacy/Minecraft/game/versions/1.21.11/natives/lwjgl.dll` | 479,232 | PE32+ / x86_64 / subsystem 2 | `a39adf52947fafd954c2a86ce031abb8c59825f7ee50337ac8c41e4280abe82d` |
| `legacy/Minecraft/game/versions/1.21.11/natives/lwjgl_opengl.dll` | 364,032 | PE32+ / x86_64 / subsystem 2 | `fe200dc96ab31237a52facd6345d31f9740ef16dd411e5f9be014eaa30f89fb6` |
| `legacy/Minecraft/game/versions/1.21.11/natives/lwjgl_stb.dll` | 510,464 | PE32+ / x86_64 / subsystem 2 | `de03f38f8c7471b4924aa8bdf8724c181d1a7c20428dbce2ed301877e1d387e4` |
| `legacy/Minecraft/game/versions/1.21.11/natives/OpenAL.dll` | 1,338,368 | PE32+ / x86_64 / subsystem 3 | `0630aa42492f78126da1c4d99769632e03c55b2e63b050efe7e3005e07e3e6fc` |
| `legacy/Minecraft/game/versions/1.21.11/1.21.11.jar` | 31,152,600 | ZIP/JAR | `1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd` |
| `legacy/Minecraft/game/versions/1.21.11/1.21.11.jar.bak` | 31,152,600 | ZIP/JAR | `1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd` |
| `legacy/Minecraft/jre/java-runtime-delta/windows-x64/java-runtime-delta/bin/java.exe` | 39,424 | PE32+ / x86_64 / subsystem 3 | `0afb1170b83c156dfdb7f54bb34c9b058064175c329a5d80b782bcc9dbaa2164` |
| `legacy/Minecraft/jre/java-runtime-delta/windows-x64/java-runtime-delta/bin/server/jvm.dll` | 13,870,080 | PE32+ / x86_64 / subsystem 2 | `8b2da3280a300fc5d183da24cb578fa29d59f26c25ad29fcbdd0cc525a75cf26` |

## Continuation: publisher references and license boundary [E16]

The [publisher source page](https://docs.llaun.ch/en/launcher/source) describes reference/research use and links LegacyLauncher/archive, whose [license](https://raw.githubusercontent.com/LegacyLauncher/archive/master/LICENSE.txt) says All rights reserved. The public [website](https://llaun.ch/en) states downloads were halted after a Mojang complaint and disclaims Mojang/Microsoft affiliation. These documentary observations corroborate naming/restrictions, not historical installer authenticity. No proprietary source was incorporated into LegacyForge; only independently written summaries and analyst metadata are published here.
