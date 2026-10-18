# License and provenance

## Exact selected image

VERIFIED local NOTICE and legal/java.base/LICENSE, ADDITIONAL_LICENSE_INFO and ASSEMBLY_EXCEPTION. The selected21.0.12.1+1 image declares GPLv2 with Classpath Exception; designated files/components and bundled independent components retain their own terms.243 legal files were inventoried and hashed. SOURCE-INVENTORY.json pins inspected principal legal files, and LOCAL-RUNTIME-INVENTORY.json pins every notice and component file.

The exception permits specified combinations with independent modules; it is not permission to erase notices or disregard changes to the runtime itself. Future redistribution must retain applicable licenses/copyright/exception and component notices, identify modifications, and satisfy corresponding-source/source-offer/access duties as applicable to the chosen distribution method. Merely pointing to a changing upstream homepage is not a complete redistribution plan. No runtime modification or redistribution has occurred here.

DOCUMENTED matching publisher source asset: [OpenJDK21U-jdk-sources_21.0.12.1_1.tar.gz](https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk-sources_21.0.12.1_1.tar.gz),115,126,841 bytes per release metadata; checksum/signature sidecars advertised. Not downloaded or inspected. Existing lib/src.zip is not assumed to contain all native sources/build scripts required for a chosen redistribution route. The release source/build identifiers in local release were read but not independently rebuilt or authenticated against source archives.

Microsoft CRT/UCRT files are independently signed Microsoft components, not automatically GPL-covered by OpenJDK's license. Their exact packaging/redistribution rights and app-local-versus-framework choice need review before any new package. Per-component notices apply to data/code such as zlib, Unicode, ICU, ASM and other legal-tree entries. No blanket Temurin license is inferred for everything in bin.

## Provenance chain

| Link | Status |
| --- | --- |
| Official publisher release/version/ZIP/checksum/signature URLs | DOCUMENTED, captured public metadata |
| Local release declares matching version/vendor/arch | VERIFIED local text; not self-authenticating provenance |
| Local image exact files and hashes | VERIFIED490-file manifest |
| JVM/Java/JLI Authenticode | VERIFIED Windows status Valid, Eclipse Foundation signer |
| Selected CRT Authenticode | VERIFIED Windows status Valid, Microsoft signer |
| Full official ZIP checksum locally calculated | BLOCKED: ZIP not available in inspected locations; none downloaded |
| Detached archive signature/public key fingerprint | BLOCKED: archive/signature not obtained; trusted publisher key identity not yet pinned |
| Local member equality with official complete archive | BLOCKED pending archive or independently authenticated publisher member manifest |
| Full runtime/dependency notice/redistribution plan | UNKNOWN until exact proposed package contents reviewed |
| Xbox load/runtime/JIT suitability | UNKNOWN; no execution |

Published ZIP SHA256 `f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e` cannot be compared with jvm.dll's unrelated hash or a concatenation of extracted files. Authenticode on six files does not authenticate unsigned lib/modules/configuration or establish the entire installation's download history. Private hash inventory ensures preservation from this review onward, not origin before review. No compromised/tampered-file allegation is supported by those gaps.

## Bandit separation and existing release blocker

No Bandit source, binaries, Java bundle, custom module patch or release was fetched/copied/executed in Phase6C.1. Pure JNI experiments must be independently authored from primary specifications. Official JDK files here are candidate inputs, not approved changes to production.

Phase6C.0 found six sampled production files byte-identical to pinned Bandit. That preserved finding remains a **release-blocking provenance/permission review item**, separate from qualification of this official JDK and independent fixtures. Establish authorship, existing grants and applicable notices before redistribution; do not infer infringement or permission from equal hashes. Do not alter matching files in this phase. The custom Bandit license does not automatically govern independently licensed OpenJDK components, nor does an OpenJDK license grant rights to Bandit adaptations.
