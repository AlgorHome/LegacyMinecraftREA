# Phase 6A evidence baseline for Phase 6B

Planning date: 2026-10-17, America/Chicago. Approved source: `d1453434ceefe73bef5aff497194e09f39dde7e1`. Confidence describes the narrow evidence claim, not a runtime certification. Phase 6A files remain unchanged; no target executable was run for this plan.

| Finding | Confidence and evidence | Phase 6B consequence |
|---|---|---|
| Archived installer and installed application are different builds | **Confirmed, static.** [PROVENANCE](../legacy-launcher/PROVENANCE.md), [INSTALLER-CONTENTS](../legacy-launcher/INSTALLER-CONTENTS.md), E11: all 770 installer payload records validate. Original launcher/bootstrap are 1.159.2/1.32.2; installed copies are 1.169.4/1.40.3. | Isolated installer tests must record which build actually starts; an updated installed copy cannot substitute for the archived build. Publisher authenticity and intermediate update history remain **Unknown**. |
| Downloads are a metadata-driven content plan | **Confirmed, static/public metadata.** [INSTALLATION-PIPELINE](../legacy-launcher/INSTALLATION-PIPELINE.md), [DOWNLOADS-TO-LEGACYFORGE](../legacy-launcher/DOWNLOADS-TO-LEGACYFORGE.md), E03/E13/E17/E21. `OfficialVersionList.getRawList`, `CompleteVersion.resolve`, library rules, assets and runtime selection feed a desktop Java process. | Reuse the content-contract ideas independently. Do not transplant `ProcessBuilder.start`, desktop Java or standard Windows GLFW into Xbox. |
| Core LegacyForge facilities already exist | **Confirmed, source.** [LEGACYFORGE-GAP-ANALYSIS](../legacy-launcher/LEGACYFORGE-GAP-ANALYSIS.md): `EnsureRuntimeDownloads` (`runtime_manager.cpp:770`), `ResolveJavaRuntimeInfo:1079`, `PrepareTargetNativeDir:1310`, `PreloadJvm` (`minecraft_launch.cpp:663`), `RunEmbeddedMinecraft:1335`; manifest generator `new-download-manifest.ps1:547`. | Diagnose the existing packaged runtime/native boundary before proposing replacements. Production source stays read-only during diagnostic planning and separate harness work. |
| Java/JNI agreement is unresolved | **Confirmed source discrepancy; runtime impact Unknown.** [JVM-RUNTIME](../legacy-launcher/JVM-RUNTIME.md): the host sets `JNI_VERSION_21` (`minecraft_launch.cpp:1353`) while selectable families include Java17/8. | Test API query, VM creation, observed Java major and synthetic Java execution separately, in fresh processes. A query success alone cannot pass the VM gate. |
| Graphics, input and native interfaces have specific limitations | **Confirmed source; consumer impact Inferred/Unknown.** [NATIVE-DEPENDENCIES](../legacy-launcher/NATIVE-DEPENDENCIES.md), E14/E15: 291 native occurrences; GLFW `glfwExtensionSupported:3979` always false; `glfwGetWin32Window:4123` returns null; hats/custom mappings limited. `PollGameInputGamepad:1563`, swap/procedure lookup and `App.cpp:112` lifecycle hooks exist. | Compare real GL capabilities with shim answers; test actual frames, input transitions, audio and lifecycle. Imports and an empty window do not establish compatibility. |
| Metadata coverage is broad, runtime evidence is absent | **Confirmed metadata.** [CATALOG-METADATA-PLANS](../legacy-launcher/CATALOG-METADATA-PLANS.md), E21: 22 Minecraft JSON hashes, 20 Fabric profiles and 34 resolved Forge/NeoForge Maven entries checked; Forge `selected` unresolved. 26.x metadata declares Java25. [PHASE-STATUS](../legacy-launcher/PHASE-STATUS.md): all 25 execution gates and 56 runtime tuples remain BLOCKED. | Start with one Java21 synthetic profile. Expand to Java17/8/current25 only after the first gate; no 56-target sweep and no game launch in initial Phase6B. |
| Historical and cryptographic evidence close narrower questions | **Confirmed recorded messages / independent verification.** [HISTORICAL-CORROBORATION](../legacy-launcher/HISTORICAL-CORROBORATION.md), E18, records newer-build Java21/LWJGL/OpenAL and exit0. [SIGNED-UPDATE-FIXTURE](../legacy-launcher/SIGNED-UPDATE-FIXTURE.md), E20, independently verifies a public response against the embedded key. | Historical logs are not new tests. The positive update fixture is available; actual updater acceptance/rejection/recovery is still untested. Embedded-key correspondence does not authenticate the archived installer publisher. |
| Diagnostics have source preparation, not a deployable harness | **Confirmed preparation; execution Unknown/BLOCKED.** [EXECUTION-READINESS](../legacy-launcher/EXECUTION-READINESS.md), E19; original [RuntimeProbe contract](../legacy-launcher/tests/probes/README.md). Trusted compilation to classfile52 succeeded; no execution occurred. Exact APPX/JVM/shim artifacts and approved guest/console access are absent. | Independently build a separately identified diagnostic package after approval, using approved artifact identities. The Java fixture covers only part of storage/thread/ZIPFS-read testing. |

## Artifact identities

Full SHA256 values are intentionally retained for reproducibility; they do not imply publisher trust.

| Artifact | SHA256 |
|---|---|
| Archived installer | `a7c997ba3c3e91c048f80f96f08754948428f6d3fe4001bab79c4ae09d06c5e0` |
| Original launcher1.159.2 | `5f1f1b8ef187c5fcea69830d4dec87c84447a6c134c314fe5a840340e4ee5e6c` |
| Original bootstrap1.32.2 | `df2d2516e905cdc87a68ec456f881664a5b158ba810934251d7b70a740679588` |
| Installed launcher1.169.4 | `364b9add9a3b0e74e553439b3f0e33a573bb5d28667adc028180d509b0459eec` |
| Installed bootstrap1.40.3 | `09ba7517c8a9b30780ff9a6de230b8905247835ae0da914d66991e2b3b4b6c4e` |
| E20 signed metadata response | `9081bab55e8c8ba72ff3c63a1c2cbb85ba523bd2ef357b94e272ba913cf5c52c` |
| Original RuntimeProbe.java | `56a6250ddf494136c6214fab269966ec2c099b60642002a28becd543ec58ddfd` |
| Approved `minecraft_launch.cpp` | `c37eade570d45fbdad0ba876be3347729b1000e579692c1819d059dbf80b5b12` |
| Approved `runtime_manager.cpp` | `fad066071b9c8914350d719fd08e2ea516daa59b6087b83ba45c96bb4787eeaf` |
| Approved `glfw_uwp.cpp` | `0dde9a0c2e0e9b6f028fae5efe9d45a8a81a1e26e330bb72d42cacc3a4ad4d10` |

Source anchors above use paths relative to the approved checkout. [EVIDENCE-INDEX](../legacy-launcher/EVIDENCE-INDEX.md), its JSON evidence and `evidence/SHA256SUMS.txt` bind the wider dossier. A fresh planning check verified the source HEAD/clean state and the three listed source hashes. Dossier checksum validation is recorded in this plan's `planning-validation.json`.

## Refined 1.12.2 interpretation

The catalog's unsupported declaration is confirmed. It should not be expanded into a claim that no Forge code exists: generic Forge dispatch is present, vanilla finalization is unsupported, and the `selected` Forge label is not a resolved release. The separate [1.12.2 assessment](LEGACY-1.12.2-ASSESSMENT.md) distinguishes those facts from unverified old-loader/runtime behavior. Phase6B diagnoses the Java8/native primitives without installing or launching Minecraft.
