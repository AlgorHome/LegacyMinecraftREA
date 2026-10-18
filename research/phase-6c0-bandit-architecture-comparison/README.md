# Phase 6C.0 - Bandit/JavaUWP feasibility comparison

**Recommendation: prioritize an independently designed Java21 feasibility sequence, with a small native D3D12 control as the second track. Preserve D3D11 acceptance; pause further SRV identity increments unless they answer a named dependency question. Do not adopt Bandit code or binaries.** This is a research decision, not implementation or execution approval.

Bandit / JavaUWP by [veroxsity / BanditVault](https://github.com/veroxsity/JavaUWP) at `ba42117784ce201eb10ab5220ee25382e76cec1f` documents in-process Java, packaged runtimes, loader adapters and Mesa-based graphics. [Pinned architecture](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/docs/ARCHITECTURE.md) and [source inventory](UPSTREAM-SOURCE-INVENTORY.md) separate documentation from observed source contracts. Its current shader/window path uses WGL over a Mesa D3D12-labeled runtime, not simply the EGL narrative in older prose.

LegacyForge already contains those broad boundaries at production pin `d1453434ceefe73bef5aff497194e09f39dde7e1`. Six of nine sampled files, including GLFW/WGL, Forge/NeoForge/dispatch and authentication, are byte-identical to upstream. SOURCE-COMPARISON-HASHES.json records this existing overlap; no upstream file was imported. This is evidence of a shared source surface, not a judgment about origin, authorization or rights. Review provenance/permissions before redistribution.

Accepted local Xbox evidence proves D00 activation, D3D11 hardware device, RGBA8 format query, one texture, one SRV, and backing-resource COM identity, with receipt/photo attribution. It does not prove a JVM, JNI, JIT, GL context, presentation, shaders, input/audio/lifecycle or Minecraft. Details in [architecture comparison](ARCHITECTURE-COMPARISON.md).

## State correction

The supplied mission's statement that SRV03 is unimplemented is stale. The immediately preceding authorized phase produced unsigned source `deb44072dd8e3ef2c936307b0a6788c6a95fad6b`, branch research/phase6b5x-d06-srv03, SHA-256 `f0c9aff93c7fe05d202d9460d0f6f8643b3facfe674ce1543055a9027e1bc3e6`. It is implemented/build-static-pass, unsigned, NOT hardware-tested. Preserved unchanged; no branch switch or rebuild. This research does not approve its signing or execution.

## Evidence vocabulary

VERIFIED_LOCAL: independently supported local artifact/source checks; hardware claims only where accepted receipt/photo evidence exists. UPSTREAM_DOCUMENTED: official text claim. UPSTREAM_SOURCE_OBSERVED: inspected version-pinned contract, not execution. INFERENCE: interpretation/proposal. UNKNOWN: missing or insufficient evidence. Confidence applies to the named narrow fact, not global Xbox compatibility.

## Dossier

- [Sources](UPSTREAM-SOURCE-INVENTORY.md), [component matrix](ARCHITECTURE-COMPARISON.md), [JVM](JVM-FEASIBILITY.md), [graphics](GRAPHICS-STRATEGY.md).
- [Licenses and research separation](LEGAL-AND-LICENSE-RISKS.md), [gaps](GAP-AND-RISK-REGISTER.md), [experiments](RECOMMENDED-EXPERIMENTS.md), [decision](DECISION-REPORT.md), [preservation](BASELINE-PRESERVATION.md).

Only this new analytical dossier was written. No source change, implementation, branch checkout, build, signing, installation, Xbox access, authentication, runtime execution or game download. No credentials or copied Bandit implementation are included.
