# Baseline preservation

**PASS.** All175 original frozen pins and all679 previously preserved files verified against their prior hashes. Expanded before/after snapshot covers694 pre-existing project/evidence files, including the entire Phase6C.0 dossier and previous source/artifacts. No mismatch or missing original.

Additional candidate preservation:490 existing Java21 files independently hashed on initial inspection and rehashed after all read-only analysis, all unchanged. This does not establish those files' provenance before inspection. Full hashes in LOCAL-RUNTIME-INVENTORY.json; project pins in BASELINE-HASHES.json.

Source HEAD before/after `deb44072dd8e3ef2c936307b0a6788c6a95fad6b`; branch `research/phase6b5x-d06-srv03`; Git status empty/clean. Production baseline d1453434ceefe73bef5aff497194e09f39dde7e1 and accepted diagnostics through SRV02 remain unchanged. SRV03 source deb44072dd8e3ef2c936307b0a6788c6a95fad6b and unsigned APPXf0c9aff93c7fe05d202d9460d0f6f8643b3facfe674ce1543055a9027e1bc3e6 preserved, unsigned/not hardware-tested. No branch switch, checkout, commit, reset or source edit.

Phase6C.0 SOURCE-COMPARISON-HASHES.json remains byte-identical; all9 recorded production Git blobs freshly match their recorded hashes. Six upstream-match flags remain supported by preserved prior upstream hash observations; no fresh Bandit download performed. This is still a release-blocking provenance/permission review item, not a finding of infringement or a grant.

Phase6A documents, accepted receipts/photographs/reports, original packages and local runtime files were not rewritten. Only this new qualification dossier was written. Public metadata/specifications/licenses and a HEAD-only alternative URL resolution were read. No runtime archive body, Bandit bundle, game file, source archive or signing material obtained. No Java/JNI call, target loading/execution, compilation/signing/installation, Xbox Device Portal, account operation or certificate/trust configuration change.

Read-only PE parser and existing Microsoft dumpbin export inspection read files without loading Java. Get-AuthenticodeSignature observed selected-file signature trust; no certificate was created/imported/exported or trust settings changed. Those host observations do not claim Xbox trust/loader acceptance.

Final verification UTC: 2026-10-18T04:22:13.044765+00:00. Byte preservation is the claim; filesystem access timestamps and historic console clocks are not used as evidence of runtime compatibility.
