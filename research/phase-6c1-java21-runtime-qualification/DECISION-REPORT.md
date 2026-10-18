# Phase6C.1 decision

**Recommend Eclipse Temurin HotSpot JDK21.0.12.1+1-LTS, Windows x64, as the exact first candidate. J0 readiness remains BLOCKED.**

## What is qualified

VERIFIED existing local image identity,490-file hash inventory,127 x64 PE headers, native import/delay/export/forwarder metadata, local JNI constants and six selected Valid Authenticode observations. DOCUMENTED publisher release matches this version/build and advertises ZIP205,073,461 bytes with SHA256 `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e` and a detached signature. GPLv2+CPE and per-component notice obligations were reviewed from existing candidate files. This is substantial static qualification, not a fully authenticated archive/image or UWP success.

## What remains missing

1. Official complete archive or authenticated member mapping against the extracted tree; detached signature and trusted publisher-key verification. Local PE signatures do not cover unsigned module/configuration bytes.
2. Final explicit J0 package/CRT/framework allowlist and reviewed known risks. Static imports alone cannot close target API sets, ordinal/dynamic loading or DllMain behavior.
3. Separately approved source/build and all later executable gates. No test source or Java fixture was implemented.

The most concrete UWP risks are desktop kernel/UI/registry/power imports, JLI dialog dependencies if unnecessarily loaded, local API-set/CRT forwarding and delayed/dynamic native libraries, package-layout discovery, executable-memory assumptions and VM shutdown/thread/memory behavior. None is a proven fatal incompatibility; no security or import-stubbing workaround proposed.

## Next approval

Authorize only exact official ZIP/checksum/signature/build metadata/public-key qualification and safe member comparison, or supply a local original archive. No install or code execution necessary. Then review the exact module/CRT policy before a separate J0 diagnostic implementation approval. J1/J2 remain independently gated; exports/queries cannot be promoted to Java execution.

Existing source/accepted packages are unchanged. The six identical-file Bandit overlap finding is preserved as a separate **release-blocking provenance/permission review**, without assuming infringement, authorship or grants. No Bandit implementation or binaries used. No runtime downloaded, loaded or executed; no compilation/signing/installation/Xbox/authentication/trust action.
