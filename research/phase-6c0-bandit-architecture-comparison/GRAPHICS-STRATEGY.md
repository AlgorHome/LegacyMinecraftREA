# Graphics strategy: D3D11 controls and Mesa/D3D12

## Correct the backend narrative

UPSTREAM_DOCUMENTED: PATCHING164-174 describes a GLFW UWP/EGL replacement and CoreWindow input. UPSTREAM_SOURCE_OBSERVED: [glfw_uwp.cpp2154-2161](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/glfw_shim/glfw_uwp.cpp#L2154) actually calls the WGL backend from a function still named CreateEglContext. [wgl_backend.h65-142](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/glfw_shim/wgl_backend.h#L65) loads the Mesa-related DLL set, resolves WGL functions and uses the CoreWindow bridge; [swap/procedure routes](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/glfw_shim/glfw_uwp.cpp#L3952) branch to WGL. EGL types/fallback-shaped branches remain in source, but their presence does not establish an operational alternative runtime.

The selected code path labels its Mesa runtime as D3D12. [mesa-runtime/README](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/mesa-runtime/README.md) requires opengl32, libgallium_wgl, dxil, spirv_to_dxil and z-1; vulkan_dzn is copied when present. Those binary names are not a verified binary SBOM. Source comment version26.1.3 and claimed MesaTestApp experience are upstream assertions, not an independently checked compiler/driver release or performance result.

General platform fact: [Mesa's D3D12 driver](https://docs.mesa3d.org/drivers/d3d12.html) maps desktop GL to D3D12. INFERENCE: it is the intended implementation behind this selected runtime path. D3D12 is therefore a dependency of that route, not proof every conceivable Minecraft/UWP renderer must use it. D3D11 hardware success neither proves nor disproves D3D12, WGL, EGL or OpenGL functionality. The inspected production GLFW/WGL files are already byte-identical to upstream, so a migration proposal based solely on those names is redundant.

## What is still missing

| Boundary | Evidence | Uncertainty / next oracle |
| --- | --- | --- |
| D3D11 hardware/resources | VERIFIED_LOCAL accepted native receipts through SRV02 | No shader, content, binding, frame or present evidence |
| D3D12 device | UNKNOWN for approved separate diagnostic | Actual S_OK/nonnull ID3D12Device, nonsoftware adapter, feature support and cleanup |
| Native bridge/library closure | UPSTREAM_SOURCE_OBSERVED WGL export/load contracts | Reviewed exact runtime provenance, legal redistribution, imports/exports, UWP load behavior |
| Context/window | UPSTREAM_SOURCE_OBSERVED CoreWindow/WGL path; EGL documentation drifts | Actual context/version/profile/extensions, correct owner thread; exclusive surface ownership |
| Translation/binding | DLL set suggests compiler/translation components (INFERENCE) | Shader compile/link statuses, resource-binding correctness, deterministic pixels |
| Presentation | UPSTREAM_SOURCE_OBSERVED swap/frame counter | A known visual pattern plus independently recorded present results; counter alone insufficient |
| Memory/recovery | Native receipts sampled small allocations | Larger GPU budgets, context loss, suspend/focus and driver recovery UNKNOWN |

A launch-screen swapchain can conflict with game backend ownership: production App.cpp812 documents that concern. Treat it as a specific source-observed risk, not a reproduced fault. Use one backend/window owner in any later original fixture; do not embed D3D11 and Mesa simultaneous presentation in a first test. Driver/runtime calls may block beyond any observation deadline.

UPSTREAM_SOURCE_OBSERVED and independently source-checked locally: [glfwExtensionSupported3979](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/glfw_shim/glfw_uwp.cpp#L3979) returns false, while [glfwGetWin32Window4123](https://github.com/veroxsity/JavaUWP/blob/ba42117784ce201eb10ab5220ee25382e76cec1f/glfw_shim/glfw_uwp.cpp#L4123) returns null. These are concrete shim limitations, not proof that the underlying GL driver lacks every extension or that all native window consumers work. Shader/resource-binding coverage and mods that assume a real desktop HWND need separate contract tests. No generic GLFW/LWJGL parity is inferred.

## Value of continuing D3D11

Accepted native receipts prove installation/activation, manifest/framework handling, hardware adapter selection, metadata queries, scoped resource ownership, LocalState evidence and fine-grained negative-vs-unknown semantics. These remain reusable diagnostic practices whichever final backend is chosen. They do not provide an OpenGL implementation or LWJGL/GLFW contract.

SRV03 has already been implemented unsigned/static-only. Its owning-device identity question is narrow; hardware acceptance would strengthen COM ownership evidence, but it is not a dependency of proving a JVM or basic D3D12 availability. Do not rebuild it as unimplemented or claim its current source is hardware-passed. Further SRV getters have lower strategic information gain than testing JVM viability or native D3D12.

## Proposed order

First review Java runtime provenance and conduct the J0/J1/J2 sequence under later gates. Independently plan a small **N12** original D3D12 hardware device-creation control: no queue/shaders/resources/swapchain, one actual call with nonnull output, no software fallback. Microsoft documents [D3D12CreateDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-d3d12createdevice): null output can return S_FALSE for validation only; that must not satisfy actual creation.

If N12 passes and a legal independently sourced Mesa build is established, investigate its native-library/context contract. Only then propose a single-frame original presentation/pixel oracle, followed by Java/JNI graphics. Choosing native D3D11 versus D3D12 for an intermediate presentation control depends on which uncertainty it resolves; no broad full backend rewrite is recommended.

This phase fetched no graphics binaries, ran no GPU operations, changed no capabilities and copied no shim/backend implementation.
