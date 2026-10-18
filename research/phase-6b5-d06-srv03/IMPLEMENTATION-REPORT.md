# Phase 6B.5x - D06-SRV03 implementation

Source implementation, unsigned x64 compilation, packaging and static verification complete. **PASS_STATIC_ONLY; hardware NOT EXECUTED.**

## Source and artifact

- Research branch: `research/phase6b5x-d06-srv03`.
- Source commit: `deb44072dd8e3ef2c936307b0a6788c6a95fad6b`.
- Accepted parent: `c81d0f48286513f7a7579a1d2d786cca4f5e60e2`. Existing accepted branch/commits and artifacts preserved.
- Build ID: `20261017-194936-1a6bc299`.
- Unsigned APPX: `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-194936-1a6bc299\NativeCapabilities.unsigned.appx`.
- SHA-256: `f0c9aff93c7fe05d202d9460d0f6f8643b3facfe674ce1543055a9027e1bc3e6`.

Manifest: AlgorHome.LegacyForge.NativeDiagnostics, CN=LegacyForgeDiagnostics, 0.2.5.0, x64, Application Id App, LegacyForgeNativeDiagnostics.App. MTA startup unchanged; zero declared capabilities. Host validation establishes intended UWP App shape; console classification and compatibility remain later hardware checks. No new dependency or bundled framework. Microsoft.VCLibs.140.00 min14.0.0.0 and Windows.Universal min10.0.17763.0/MaxVersionTested10.0.26100.0 unchanged.

A later approved install uses the same diagnostic identity and updates registered 0.2.4.0, potentially retaining stale LocalState. It does not install side by side with 0.2.4.0. The accepted artifact/evidence and original source commit remain preserved for reproducibility; keeping both diagnostic versions installed concurrently would require a separately reviewed identity change. D00 and production identities remain separate.

## Runtime changes compared with accepted SRV02

SOURCE-DIFF.patch contains the complete exact diff; all changed paths are under diagnostics/NativeCapabilities. No production source or accepted evidence edit.

1. Replace the backing-resource GetResource query with a single SRV GetDevice query and ID3D11Device owned output. No GetResource call remains.
2. Compare original device versus returned device canonical IID_IUnknown outputs, instead of original texture versus returned resource. Require S_OK and nonnull from each before equality. Failed QI or null cannot produce PASS.
3. Scope temporary identities before returned device, SRV, texture, context/original device. Retain failure/timeout checks and scoped unwinding. Use device-specific fields/reasons/release markers.
4. Change case/UI/profile/native inventory/activation allowlist to D06-SRV03, compile definition LFN_CASE_D06_SRV03=1, and explicitly reject prior SRV02 macro along with earlier cases. Nine unsafe configurations rejected.
5. Manifest and runtime identity assertion increment version to0.2.5.0. Existing MTA, UWP entry point, driver selection, texture/SRV descriptors, no initial data, graphics exclusions and memory/deadline/write controls unchanged.
6. Receipt schema increments v5 to v6, identifies owning-device query, adds frozen_srv02_reference_commit, changes predecessor to BEFORE_GET_DEVICE. Existing run/process identity, six package hashes, atomic persistence and terminal ownership retained. No fabricated GetDevice HRESULT or pointer-address properties.
7. Update build/package/static tooling and README for the single case; extend offline positive/negative contract fixtures. Source/build strings and generated metadata change with the new commit/build ID; these are expected provenance changes.

Device path: one HARDWARE 11_0/BGRA D3D11CreateDevice, no retry/fallback; adapter nonsoftware classification required. One1x1 RGBA8 DEFAULT/SHADER_RESOURCE texture, no initial data, all11 GetDesc fields checked. One explicit Texture2D SRV, mip0/count1, all4 GetDesc fields checked. Then one ID3D11DeviceChild::GetDevice call. No extra GPU allocation or content operation added.

Microsoft documents [GetDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicechild-getdevice) as void with an owned returned reference. Canonical comparison follows [COM identity rules](https://learn.microsoft.com/en-us/windows/win32/com/rules-for-implementing-queryinterface). Source does not invent an HRESULT for void getters.

## Verification results

| Check | Result |
| --- | --- |
| MSVC x64 compile/link | PASS; three native units, no compiler warnings found |
| Unsigned APPX packaging | PASS; fresh unique ignored build directory |
| Manifest, identity, capabilities/dependencies | PASS |
| Native-only source/preprocessed exclusions | PASS |
| Unsafe compiler gate rejections | PASS, all9 rejected before linking |
| Receipt schema/semantic fixtures | PASS:17 valid accepted,65 invalid rejected |
| Archive allowlist/CRC/unique entries | PASS;11 payload files plus block map/content types; no signature |
| Imports/dependencies | PASS static; exact import set equals accepted SRV02 |
| Independent payload and block-map hashes | PASS; six role hashes and all11 block-mapped files |
| Frozen baseline preservation | PASS: original175 and expanded208 preserved files |
| Hardware/native behavior | NOT EXECUTED |

Fixtures cover PASS, S_FALSE/null/failed resource outputs, wrong descriptors/dimensions, null GetDevice output, each failed or S_OK/null QI, unequal identities, timeouts, NOT EXECUTED and RUNNING. Invalid inputs include stale case/version/schema, wrong UUID attribution/sequence, inconsistent HRESULTs/nonnull flags, raw addresses, invented GetDevice/GetResource HRESULTs, memory breaches, wrong predecessor, forged payload pins and duplicate JSON keys. Fixture generation/validation executes Python only, not the diagnostic.

## Reproducible Windows build

Existing prerequisites: PowerShell7; MSVC BuildTools14.44.35207 x64 with UWP store CRT; Windows SDK10.0.26100.0 including C++/WinRT headers, windowsapp/runtimeobject/d3d11/ole32/bcrypt libraries and MakeAppx; Python standard library. No signing certificate or private material needed for this unsigned build. Tool paths/hashes and commands/exit codes in BUILD-RECEIPT.json and BUILD-EVIDENCE.json.

From clean committed checkout of the source commit:

```powershell
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Build rejects a dirty checkout and emits a new unique out directory. Embedded commit/build ID and toolchain metadata affect hashes; rerunning later is not expected to reproduce this exact APPX digest. The pinned artifact is the review/signing input. No signing, installation, execution or downloads occur in the build script.

## Risks and boundaries

SRV03 GetDevice/QI behavior, activation and UI/receipt operation on Xbox have not been tested. Import equality cannot prove complete target loader closure. Platform MessageDialog uses system UI; its appearance would not prove app rendering. Deadline10s bounds result eligibility/observation, not native/GPU/file call completion. Startup hashing and initial receipt precede the deadline. Detached observer cannot cancel a blocked native call; a timed-out worker may remain pending until owner action under a later gate.

Memory samples are not peak/GPU allocation or leak tests. Scoped references and release markers prove code-owned progression only. Receipt flush/replace is best-effort atomic persistence, not power-loss proof. Failure/race recovery is statically reviewed and synthetically validated only. Prior self-signed Windows trust finding remains unchanged; no certificate inspection/signing/trust modification done in this phase.

## Deliverables and next approval

IMPLEMENTATION-REPORT.md, STATIC-SAFETY-REVIEW.md, BUILD-EVIDENCE.json, RECEIPT-SCHEMA.json and HARDWARE-ACCEPTANCE-PLAN.md. Additional BUILD-RECEIPT.json, STATIC-VERIFICATION.json, BASELINE-PRESERVATION.json and SOURCE-DIFF.patch retain review evidence.

Stop reached at unsigned build/static verification. Next approval: local signing and integrity verification of this exact source/artifact. Installation-only update, one launch, receipt retrieval, final acceptance and cleanup remain distinct later approvals. No Xbox access or runtime action performed.
