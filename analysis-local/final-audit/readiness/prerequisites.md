# Runtime readiness audit

Observed 2026-10-17. This is a prerequisite check, not execution evidence. No archived launcher, game, bundled JVM, VM, or Xbox package was executed. No feature, service, boot, permission, trust-store, or installed-software changes were made. The pinned evidence checkout remains read-only at `d1453434ceefe73bef5aff497194e09f39dde7e1`.

## What is actually available

| Prerequisite | Observed result | Meaning |
|---|---|---|
| Windows edition | Windows 11 Pro, x64, version 10.0.26300, build 26300 | An edition/build observation; it does not establish an available isolated guest. |
| Active hypervisor | `HypervisorPresent=true` | A hypervisor is reported. The concurrently false CPU virtualization flags may be masked by it and do not establish an unsupported host. |
| Hyper-V PowerShell | `Get-VM` command present; inventory denied for insufficient permission | No VM names, states, ownership, or usable guest could be established. No permissions were changed. |
| Optional-feature state | Sandbox, Hyper-V, and Virtual Machine Platform reads require elevation | State remains unknown. None was enabled or disabled. |
| Windows Sandbox | `C:\Windows\System32\WindowsSandbox.exe` absent | No launchable Sandbox was established at the standard path. |
| Alternative VM tools | Standard VirtualBox/VMware executable paths absent | Limited path checks, not proof that every possible hypervisor is absent. |
| Workspace guest artifacts | No `.wsb`, `.vmcx`, `.vmrs`, `.vhd`, `.vhdx`, `.vmdk`, `.ova`, `.ovf`, or `.iso` | No supplied disposable guest or ISO. The existing `offline.wsb.example` is a template and was not launched. |
| Visual Studio Build Tools | 2022 version 17.14.37710.0; VC x86/x64 component present | Compiler/linker files exist. No source build or link test was run. |
| SDK | 10.0.26100.0; x64 MakeAppx/MakePri/SignTool; required sampled headers/libs present | Build/package tools exist. SDK presence does not prove a complete package can build. |
| UWP workload | No `Microsoft.VisualStudio.Workload.Universal` registration returned | Not sufficient by itself to call this a blocker: the pinned script directly invokes `cl.exe`, and sampled C++/WinRT/Windows libraries exist. |
| JDK | Adoptium 25.0.4.1 in standard vendor roots; existing trusted Ghidra JDK21.0.12.1 outside them, with `java.exe`, `javac.exe`, `jar.exe`, and `lib/src.zip` | JDK21 is available. Release-file metadata reports Adoptium21.0.12.1+1-LTS/x86_64. LegacyForge build path/configuration compatibility remains unverified. No full build-compatible JDK17 was established; a target-bundled desktop Java17 runtime is insufficient. |
| Deployable package | No APPX/APPXBUNDLE/MSIX/MSIXBUNDLE in the supplied workspace | No exact package can currently be handed to the owner from these artifacts. |
| Runtime files | Six Mesa DLLs in pinned source; no packaged JVM/launcher executable | The Mesa source inventory is not a complete staged/deployed package. |
| Xbox | Hardware/Developer Mode/prior deployment are owner-reported; no remote address/access | Physical tests require owner action and actual returned evidence. |

The recursive workspace inventory observed 563 files at its collection time. Other agents share the workspace, so this count is only a snapshot. Neither the launcher workspace's private account stores nor unrelated user directories were searched.

## Minimal reviewable Windows environment plan

1. The owner supplies or prepares a disposable Windows 11 VM with a fresh local test account and an offline baseline checkpoint. Use a full VM for repeatable snapshot-based installer/update/recovery tests; an approved Windows Sandbox can cover disposable smoke tests when installed and available. The present audit cannot establish VM availability because enumeration is permission-denied.
2. Keep host home directories, clipboard, credentials, printers, camera/microphone, and writable host shares disconnected. Copy only the fixed-hash installer/research inputs through a dedicated read-only transfer surface, then copy working inputs onto the guest's disposable disk. Use a narrowly scoped, separately reviewed result-export route. A guest must never receive the host's existing `.tlauncher` profile or personal credentials.
3. Record the guest OS/build, hypervisor, isolation controls, installer SHA256, approved actions, and network mode before execution. The owner's execution approval must identify the actual isolated guest and target artifacts; there is no confirmed isolated target to approve or run yet.
4. Run W01-W03 offline first. Preserve guest-only file inventories and sanitized process identities. For W04-W10, obtain the separately approved guest network/test mode, use pinned public artifacts, and perform interruptions/corruption/full-volume tests exclusively on synthetic guest copies.
5. Preserve every W01-W12 row. Real authentication remains an owner-operated flow with outcome-only receipts; no credentials, tokens, device codes, account identifiers, or raw authentication traffic are returned. W11 gameplay and W12 authentication are not implied by successful downloads.

The existing `docs/research/legacy-launcher/tests/offline.wsb.example` disables networking, clipboard, audio/video input, printers, and vGPU, and has no automatic target command. It is not a substitute for enabling/installing a supported Sandbox or for the owner's execution approval. A vGPU-disabled guest cannot establish Xbox graphics/performance behavior.

## Minimal reviewable LegacyForge package plan

The shortest path is for the owner to provide the exact approved Phase 5F.2 package and dependencies they already deployed, together with its package identity/version and fixed hashes. It must still be correlated to the pinned source; the owner's earlier success does not independently pass new Phase 6A tests or all catalog targets.

If a new package is needed, use a separate build checkout at exactly `d1453434ceefe73bef5aff497194e09f39dde7e1`; do not build in the read-only evidence checkout. The current `build.ps1` creates staging/cache/output files, can stop processes, generates a development signing certificate when absent, runs Java tools, fetches/generates dependencies through subordinate scripts, and signs an APPX. It is not a harmless read-only prerequisite check.

Before a separate build, supply or explicitly approve the required JDK/dependency acquisition and signing environment. The pinned build resolves an exact JDK 21 (`build.ps1:75`), may package an exact JDK 17 when available, and needs a sufficiently new JDK for newer targets. The existing Ghidra JDK21 satisfies an availability observation; whether its path must be explicitly configured and its vendor/source layout can build the pinned patches is unverified. JDK25 does not replace the explicit JDK21 requirement. The full 56-row catalog must be staged and reviewed; absent old-runtime/provider support must remain an explicit unresolved result. Do not omit rows to make the build appear complete.

Use the pinned script's reviewed parameters, including `-SkipStopAppProcesses` to avoid unrelated process termination in the separate build environment. `-KeepStaging` preserves the staged files for hashing. `-StrictTargets` makes recorded skipped target-build failures fatal; it does not manufacture unsupported provider implementations. Do not invent package versions or reuse a production signing private key without owner control. Keep diagnostic additions separate, identified and approved, if the owner chooses synthetic probes; no new diagnostic package is present or represented as built here.

For an eventual package, collect:

- APPX SHA256, package identity/version/architecture, dependency identities and signing verification result.
- Exact packaged `jvm.dll`/runtime release metadata and hashes, GLFW/mouse shims, Mesa/native module hashes, and their dependency identities.
- Exact 56-row catalog, manifests, patch/mod artifacts, and per-row build results. Build checks only establish staging; they do not pass gameplay.
- The source commit and any separately approved diagnostic delta, without modifying production authentication or entitlement checks.

## Xbox execution and evidence plan

The owner uses their already-established manual Developer Mode deployment route. This audit has no console address or remote session and performs no device discovery, connection, sign-in, or deployment.

All X01-X13 gates remain required: package activation, actual resource budget, four runtime-family/JNI checks, filesystem/ZIPFS, native load, graphics, input/focus/reconnect, audio/device loss, suspend/resume/relaunch, download/repair under existing account gates, legitimate owned gameplay, all 56 catalog rows, and Phase 5F.2 UI regressions. Synthetic probes must have their own exact approved package identity and receipt; desktop/static results cannot pass them.

The owner records only allowlisted results from `tests/result.template.json`: test/target IDs, source/package/runtime/module hashes, console OS/build, observed error/HRESULT, counters, measured timing/resource values, and a brief sanitized symptom. Owner-only authentication/entitlement/profile checks return outcomes without account identifiers or secrets. Until those actual observations arrive, each dynamic or physical gate is **BLOCKED**, and the number of dynamic/physical tests passed by this audit is **zero**.

## Inputs still required

1. A confirmed isolated Windows guest and explicit archived-target execution approval for that guest.
2. An exact approved signed LegacyForge APPX/dependency set, or an explicitly approved separate build environment with the missing runtime/dependency/signing inputs.
3. Owner execution of the complete Series X and account checks with sanitized receipts.

More agents cannot substitute for these unavailable execution surfaces or create historical publisher/update provenance. This audit identifies them concretely without labeling pending tests as successful.

## Bounded public package check

The root audit's unauthenticated public GitHub check returned zero workflow runs for the exact pinned commit and zero repository public releases. This is bounded to those public API responses: it does not exclude owner-held APPX files, private/expired workflow artifacts, other commits, unpublished builds, or other distribution channels. No exact package was thereby obtained.
