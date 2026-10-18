# D06-SRV03 separately gated hardware acceptance plan

Preparation only. Current artifact is unsigned; do not install or launch it.

## Gate 1 - local signing (requires new explicit approval)

Pin source `deb44072dd8e3ef2c936307b0a6788c6a95fad6b` and unsigned APPX `C:\Users\arinze\Desktop\ReverseLegacyCraft\phase6b1-diagnostics\diagnostics\NativeCapabilities\out\20261017-194936-1a6bc299\NativeCapabilities.unsigned.appx`, SHA-256 `f0c9aff93c7fe05d202d9460d0f6f8643b3facfe674ce1543055a9027e1bc3e6`. Reverify source/build, identity, only-case policy, six role hashes and expanded frozen pins. Sign exactly one fresh copy with separately approved diagnostic certificate and SHA-256; preserve original. Verify CMS, APPX digest, unchanged payload, block map and archive. Record signed path/hash; report Windows chain trust independently without modifying trust. No deployment under signing approval.

## Gate 2 - owner installation only (requires new explicit approval)

Owner uses existing authenticated Portal only after approval. Verify approved signed hash immediately before upload. Confirm existing NativeDiagnostics not running. Expected identity AlgorHome.LegacyForge.NativeDiagnostics, publisher CN=LegacyForgeDiagnostics, x64, version0.2.5.0, App Id App; verify intended App console classification. Same identity replaces0.2.4.0 and may retain stale LocalState; no side-by-side registration promised. Preserve all prior receipts and accepted packages. Disable auto launch or stop; upload no extra dependencies when installed Microsoft.VCLibs.140.00 resolves manifest. Submit exactly once; record final status/HRESULT/full identity and PackageFullName if exposed. Stop on any signature/dependency/identity/registration error; no retry, repair, uninstall or trust changes. Stop before activation.

## Gate 3 - one owner launch (requires new explicit approval)

After registration matches, authorize exactly one launch, observe at most30s. Case dispatch automatically starts one SRV03 run; no extra UI test action. Record activation separately from visible status, and photograph complete case/version/reason/run ID and saved-receipt indicator. No second launch or repair after crash, missing UI or timeout.10s internal deadline cannot cancel a blocked driver/COM call. Preserve any failure; request separate scoped evidence retrieval approval.

## Gate 4 - existing receipt retrieval (requires new explicit approval)

Read only this installed package's LocalState/NativeCapabilityReceipts. Retained older case receipts are stale for SRV03 acceptance. Obtain original D06-SRV03-<exact-run-UUID>.json and relevant same-run temporary file only if present/approved; list filename/time/size, preserve original bytes, hash JSON and original photograph locally. No relaunch or unrelated package/log data. If unavailable mark BLOCKED/INCONCLUSIVE, do not assume absent means no execution.

## Gate 5 - offline formal acceptance (requires explicit evidence-analysis approval)

Use pinned schema v6 plus semantic oracle; verify source/build, package0.2.5.0/x64/App, all frozen reference pins, distinct v4 run/process UUIDs, same photo run, expected sequence6/FINAL/terminal and last checkpoint BEFORE_GET_DEVICE. Independent six member hashes must match unsigned approved archive, pre-sign build pins and receipt; signed payload preservation must pass.

Require creation/texture/SRV HRESULT S_OK, nonnull device/context/texture/SRV, nonsoftware adapter/no fallback, expected11_0 and accepted11-field texture/4-field SRV descriptors. Require get_device_called=true, nonnull owning_device_returned, original_device_identity and returned_device_identity QIs both S_OK/nonnull, IID_IUnknown, comparison performed and canonical_identity_equal=true. GetDevice returns void: no fabricated HRESULT field accepted. Require temporary_identity_references_released, returned_device_reference_released, device_references_released_before_srv, srv_reference_released, srv_released_before_texture, texture_reference_released and test_resources_released. Scope review must corroborate those markers.

Memory samples available, initial headroom>=256MiB and observed growth<=64MiB; elapsed<10000ms; no watchdog cancellation claim. PASS reason SRV_OWNING_DEVICE_IDENTITY_CONFIRMED. Original terminal retrieval establishes case persistence within owner provenance; receipt's VERIFY_BY_RETRIEVAL is not self-certification of a future write. Log unverified clocks, replaced intermediate checkpoints, app-generated identity/counters and memory/release telemetry limitations.

Keep registration, activation, visible result, native identity check, final persistence and overall acceptance separate. PASS only all required criteria; FAILED for established negative output/policy violation; BLOCKED for missing required evidence/prerequisite; INCONCLUSIVE for unresolved run attribution/timeout/conflicting evidence. NOT EXECUTED describes stages not performed. Platform dialog is not app rendering proof. No shader/sampling/rendering/presentation/OpenGL/LWJGL/Java/JNI/Minecraft compatibility established.

## Gate 6 - cleanup (requires separate explicit approval)

No implicit uninstall, data clearing, rollback or process termination. Preserve final evidence first. Define the exact diagnostic-only cleanup action in a separate approval; production LegacyForge and D00 remain untouched.
