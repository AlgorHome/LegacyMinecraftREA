# LegacyForge Phase 6A: Legacy Launcher research

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

Baseline: LegacyForge `d1453434ceefe73bef5aff497194e09f39dde7e1` on `main`, explicitly approved by the user. Source checkout remained clean. Research documents are separate from that checkout and production code.

**Confirmed:** the archived installer and installed launcher are different version identities. The 117,751,681 -byte installer matches the archive's published SHA-1 and MD5 and reports file version `1.159.2.0`. Installed launcher metadata reports `1.169.4+legacy`; bootstrap reports `1.40.3+legacy`. The selected installed game is Minecraft `1.21.11`. The original installer payload is now statically recovered: launcher `1.159.2+legacy`, bootstrap `1.32.2+legacy`, with all 770 payload records hash-validated. Intermediate update history remains **Unknown**. [E01–E04/E11]

**Confirmed:** the installed application uses a native Windows wrapper, a Java bootstrap, Swing UI, version/dependency managers and an external game JVM. The selected game requests Java 21 and uses Windows LWJGL 3.3.3 dependencies. LegacyForge already implements an embedded JVM and its own GLFW/Mesa adaptation. Copying the desktop launcher/startup path would not establish Xbox compatibility. [E02–E07]

Start with [how version downloads transfer to LegacyForge](DOWNLOADS-TO-LEGACYFORGE.md), then [installation pipeline](INSTALLATION-PIPELINE.md), [gap analysis](LEGACYFORGE-GAP-ANALYSIS.md), and [roadmap](PHASE-6-ROADMAP.md).

Final additions include [all 56 upstream metadata plans](CATALOG-METADATA-PLANS.md), [execution readiness](EXECUTION-READINESS.md), an independently verified [signed-update fixture](SIGNED-UPDATE-FIXTURE.md), and an original [source-only runtime probe](tests/probes/README.md). The fixture gap is closed; actual Windows/Xbox/account observations remain pending.

## Documents

- [Provenance](PROVENANCE.md): archive identity, signatures, hashes and restrictions.
- [File inventory](FILE-INVENTORY.md): bounded directory and executable inventory.
- [Architecture](ARCHITECTURE.md): subsystem and dependency maps.
- [Authentication boundaries](AUTH-BOUNDARIES.md): accounts, ownership and token handling.
- [JVM/runtime](JVM-RUNTIME.md): Java selection, classpath and native dependencies.
- [Xbox/UWP compatibility](XBOX-UWP-COMPATIBILITY.md): observed behavior versus platform needs.
- [Evidence index](EVIDENCE-INDEX.md): identifiers, tools, reproducible commands and limitations.
- [Unknown subsystems](UNKNOWN-SUBSYSTEMS.md): unanswered questions and required probes.

## Interpretation and completion boundary

**Confirmed** means artifact bytes, selected method instructions, pinned source, or a cited official document establish the stated narrow fact. **Inferred** means those observations support an explanation without proving runtime behavior. **Unknown** means required evidence is absent. Source presence does not prove execution, endpoint constants do not prove network traffic, and hash agreement does not prove publisher authenticity.

The static research package covers every mission phase. See [full phase status](PHASE-STATUS.md), [installer contents](INSTALLER-CONTENTS.md), [update/recovery](UPDATE-AND-RECOVERY.md), [loader resolution](LOADER-RESOLUTION.md), [native audit](NATIVE-DEPENDENCIES.md), [historical corroboration](HISTORICAL-CORROBORATION.md), [Windows procedures](WINDOWS-SANDBOX-TESTS.md) and [Xbox procedures](XBOX-SERIES-X-TESTS.md). Retained newer-build logs record a download/start/audio/exit sequence; acquisition and intermediate-update events/current service permissions remain unknown. Infrastructure-dependent execution is explicitly BLOCKED. The user's report that Phase 5F.2 was Xbox Series X-tested is retained as user-provided context, not independent validation of all targets.

No target executable, installer, JAR, bundled Java, or game was run. Trusted analysis tools parsed target bytes. No installs, network authentication, production edits, Git commits or pushes were performed. No proprietary binaries, game assets, raw profiles, token values, decompiled listings or raw class pools are in this research folder. Local-only analyst working data lives in `analysis-local/` outside it; do not bulk-publish that directory or the workspace root.
