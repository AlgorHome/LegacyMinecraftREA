# NativeCapabilities - D06-SRV03 only

Separate native-only UWP diagnostic, NativeDiagnostics 0.2.5.0, existing diagnostic
identity CN=LegacyForgeDiagnostics, x64 App Id App, MTA startup, zero capabilities.
A future owner-approved update replaces registered 0.2.4.0 and may retain stale
LocalState. Accepted packages/evidence and production LegacyForge remain separate.

One HARDWARE 11_0/BGRA device, one fixed 1x1 RGBA8 texture and one explicit SRV,
using accepted descriptors and S_OK/nonnull/GetDesc checks. Then exactly one
ID3D11DeviceChild::GetDevice on the SRV with nonnull output storage. It returns
void, not HRESULT. Require nonnull ID3D11Device, query original and returned device
once each for IID_IUnknown; require S_OK and nonnull before canonical equality.
No GetResource call or previous case dispatch in this single-case build.

Scoped ownership: temporary IUnknown references, returned device reference, SRV,
texture, context, original device. Failure outputs are also scoped. Record only
identity equality, not raw addresses; markers do not prove driver leak freedom.

No pipeline binding, sampling, texel initialization/reads, shaders, draw/clear/copy/
map/readback, render target, swapchain/presentation, WARP, retries or Java/JNI/Minecraft.

Build from a clean committed checkout with existing MSVC 14.44.35207 UWP store CRT,
Windows SDK 10.0.26100.0 C++/WinRT, PowerShell 7 and Python standard library:

```powershell
pwsh -NoProfile -File .\diagnostics\NativeCapabilities\build.ps1
```

Build creates a fresh ignored unsigned x64 APPX only. Nine unsafe preprocessor
configurations must reject; no target executable is run by any verifier.

Receipt v6 binds case, source/build, frozen baselines, package identity, distinct
process/run UUIDs, six payload hashes, device/texture/SRV HRESULTs and descriptors,
GetDevice output, two QI HRESULTs/nonnull flags, canonical equality, release order,
app-memory samples, deadline and terminal result. Sequence: STARTED1,
BEFORE_CREATE_DEVICE2, BEFORE_CREATE_TEXTURE3, BEFORE_CREATE_SRV4,
BEFORE_GET_DEVICE5, FINAL6. LocalState/NativeCapabilityReceipts/D06-SRV03-<run>.json.

PASS requires hardware-only successful prerequisites and matching descriptors,
nonnull GetDevice output, S_OK/nonnull canonical identities, equality, scoped
cleanup and memory/deadline compliance. Failed/null/mismatched outputs are FAILED;
prerequisite/persistence unavailable is BLOCKED; late/native exception attribution
or timeout can be INCONCLUSIVE as specified by reason; NOT EXECUTED is distinct.
Formal hardware acceptance additionally requires retrieved terminal bytes, pinned
payload verification and exact run/photo association. Synthetic fixtures are not
hardware results. Receipt write cap128KiB, lock wait100ms, 10s observation deadline,
256MiB preflight headroom, max64MiB sampled growth. Startup hash/write precedes timer.
No cancellation of blocked native/GPU/file calls or hard driver time bound claimed.

API contract: https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicechild-getdevice
Signing, installation, one launch, retrieval, acceptance and cleanup each gated.
