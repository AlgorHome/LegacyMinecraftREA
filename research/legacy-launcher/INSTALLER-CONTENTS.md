# Archived installer contents and installed comparison

Research continuation: 2026-10-17. No target code executed; all behavioral tests below remain BLOCKED unless a specific result is supplied.

## Verified nonexecuting recovery [E11]

The installer SHA256 remains `a7c997ba3c3e91c048f80f96f08754948428f6d3fe4001bab79c4ae09d06c5e0`. Independent Python standard-library inspection recovered the Inno Unicode data-format marker `6.1.0` at file offsets 751888 and 115841256. The marker is a storage-format identifier, not proof of the exact installer compiler release.

The valid metadata block starts at 115841320: stored 999,527 bytes, decoded 5,085,511 bytes, header and 244 chunk CRC32 checks validated. Decoded SHA256: `b1c3a29ec0144f6b4613d0ba5d64f05c9693ec32d04000ffb7c21c20714927c3`. The second checked block starts at 116840856, stored 10,884 bytes, decoded 56,980 bytes; its 770 location descriptors each occupy 74 bytes.

The single solid data chunk begins at 1202688 and uses LZMA2 with a 2,097,152-byte dictionary. Decoding produced 432,715,852 bytes. SHA256 of the filtered solid stream is `98f38fa6ec39b19762aa2d4106f5c9e95e71258cc479f17056979dcd0ccc76dc`. All 770 payload records match their declared SHA1 after reversing the applicable x86 instruction-storage transform. Of these, 622 already match before transforming; 148 need the inverse transform. No installer, JAR, EXE or DLL was run. Only two original JARs and the installed nested bootstrap application JAR were materialized locally for static inspection, outside the publication folder.

The decoder is a bounded inspector for this exact format/artifact, not a general installer extractor. Format mechanics were checked against [innoextract stream/data sources](https://github.com/dscharrer/innoextract/tree/master/src); code was not taken from the proprietary launcher. CRC/SHA1 consistency establishes internal decoding correctness, not upstream publisher authenticity.

## Original versus installed identity

| Artifact | Installer payload | Installed snapshot | Conclusion |
|---|---|---|---|
| launcher.jar | 5,441,684 bytes; 1.159.2+legacy; SHA256 5f1f1b8ef187c5fcea69830d4dec87c84447a6c134c314fe5a840340e4ee5e6c | 5,496,812 bytes; 1.169.4+legacy; SHA256 364b9add9a3b0e74e553439b3f0e33a573bb5d28667adc028180d509b0459eec | Confirmed different payloads |
| bootstrap.jar | 9,612,033 bytes; 1.32.2+legacy; SHA256 df2d2516e905cdc87a68ec456f881664a5b158ba810934251d7b70a740679588 | 11,026,138 bytes; 1.40.3+legacy; SHA256 09ba7517c8a9b30780ff9a6de230b8905247835ae0da914d66991e2b3b4b6c4e | Confirmed different payloads |
| Native/runtime/dependencies | 770 decoded records; declarations include root JRE and jre/x86 | 431 installed non-game files have SHA1 equal to an installer record, including the wrapper | Confirmed shared content; not a complete historical update chain |
| Minecraft client/assets | No game-cache destination in the inspected installer destination declarations | 1.21.11 client, libraries/assets and Java 21 runtime exist | Inferred later on-demand installation; installer itself is a launcher/runtime distribution |

Original launcher metadata declares `ru.turikhay.tlauncher.TLauncher` and 34 library descriptors. Its older namespace alone does not identify another similarly named product. Original bootstrap contains 5,275 ZIP entries; launcher 1,422. Both have now been examined separately from installed copies. [E11/E13]

**Confirmed wrapper configuration:** TL.exe contains `jre;x86` at file offset 408392, `-Xmx128m -Dtlauncher.bootstrap.restartExec=TL.exe` at 408404, `launcher\bootstrap.jar` at 408456 and `_JAVA_OPTIONS=-Dtlauncher.launch4j=true` at 408484. Alongside the earlier native CreateProcessA call, this establishes declared native-wrapper/bootstrap linkage. Actual command-line expansion and resulting runtime process remain unexecuted. [E06/E11]

**Unknown historical facts:** exact update/download timestamps and intermediate builds, whether an external/manual replacement occurred, original acquisition event and independently authenticated publisher signature/hash. Decoding the installer cannot reconstruct events that were not recorded. Current publisher pages corroborate product naming and research-only source availability, not the archived artifact's authenticity.

Machine evidence: `evidence/installer-payload-summary.json`; local decoder commands in EVIDENCE-INDEX. Destination strings are retained as declarations; their order was not promoted into a formally parsed file-table/path-to-record mapping. Content matches use hashes independently of that order.
