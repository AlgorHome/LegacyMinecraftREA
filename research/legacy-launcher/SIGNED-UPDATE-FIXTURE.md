# Public signed-update metadata fixture [E20]

An independently implemented verifier accepted a current public metadata response against the public key embedded in both supplied bootstrap versions. This closes **fixture availability** for the signed-update test. **Actual launcher/updater acceptance, update application, recovery, and Windows/Xbox execution remain untested/BLOCKED.**

The compact evidence is [evidence/signed-update-fixture.json](evidence/signed-update-fixture.json). Fetched metadata, decoded metadata, extracted key bytes, and the analyst verifier remain local under `analysis-local/final-audit/signed-update/`; none is included in this publication folder.

## Exact fixture and trust anchor

The URL was derived from shipped resources and bytecode, without guessing a domain: installed `HostsV1.BOOTSTRAP` contains `bootstrap.llaun.ch` and `bootstrap.legacylauncher.ru`; `META-INF/bootstrap-meta.json` supplies `shortBrand=legacy`; `UpdateMeta$1.lambda$fetchUpdateMeta$0` constructs `https://%s/%s/bootstrap.json.mgz.signed`.

One bounded, unauthenticated HTTPS read of [the exact metadata endpoint](https://bootstrap.llaun.ch/legacy/bootstrap.json.mgz.signed) completed on **2026-10-17 at 06:55:04 UTC** with HTTP 200. Redirects, cookies, authentication, private/device endpoints, and downloads of referenced executable artifacts were excluded. DNS results were checked for public routability without retaining their address values.

| Identity | Bytes | SHA-256 |
|---|---:|---|
| Signed metadata response | 72,164 | `9081bab55e8c8ba72ff3c63a1c2cbb85ba523bd2ef357b94e272ba913cf5c52c` |
| Signed payload after signature prefix | 71,908 | `7f90a5642b01ccc77bfa79acde3229e36ce874219de77636a2ae637ca494e827` |
| Embedded public key, DER SubjectPublicKeyInfo | 294 | `4fd4703ee5c9f4339bfc5e7ea7aa36eb0ffa6e6f6915df0ec5563ac0835a294c` |
| Decoded metadata JSON | 316,400 | `22155baa1562d52a04574b80a4e668c3fe017bbd5e81529e12c1b95db359159f` |

The installed key is `net/legacylauncher/bootstrap/transport/public.der` within `BOOT-INF/lib/bootstrap-1.40.3-plain.jar`. The archived bootstrap's `public.der` is byte-identical. The enclosing installed bootstrap SHA-256 is `09ba7517c8a9b30780ff9a6de230b8905247835ae0da914d66991e2b3b4b6c4e`; the archived bootstrap SHA-256 is `df2d2516e905cdc87a68ec456f881664a5b158ba810934251d7b70a740679588`.

## Independently checked framing and algorithm

The first **256 bytes** are an RSA signature. The remaining payload begins with the five-byte marker `gzip:` and then gzip-compressed JSON. The signature scheme is **RSASSA-PKCS1-v1_5 with SHA-1**, applied to the UTF-8 bytes of the **lowercase hexadecimal SHA-256 digest of the complete payload**, including its marker. The key is RSA-2048 with public exponent 65537.

The analyst verifier uses Python's standard library for bounded ASN.1 parsing, modular exponentiation, SHA-256/SHA-1, and strict PKCS#1 encoded-message comparison. It does not call the launcher's verifier or execute a supplied JAR/EXE/DLL. Its result for these exact bytes was **VALID**. A local one-bit payload change and a local one-bit signature change were both rejected; altered data was never sent to a service or supplied to the launcher. Bounded decompression also produced syntactically valid JSON.

The traced static anchors are `HostsV1.<clinit>` offsets 6/11; `UpdateMeta$1.fetchUpdateMeta` offset 22 and `lambda$fetchUpdateMeta$0` offset 3; `SignedStream.readSignature` offsets 9/25, `validateSignature` offsets 18/37/43/52 and `verify` offset 0; `ChecksumStream.<init>` offset 6; and `Sha256Sign.toString`'s radix-16 conversion at offset 40. Class hashes are retained in E20's compact evidence.

## Limits

The fetch was capped at 1 MiB, decompression at 4 MiB, and the network operation at a 15-second socket timeout. Only this metadata URL was fetched; no launcher update or referenced binary was downloaded or installed.

A matching signature establishes correspondence to the **embedded trust anchor**. It does not independently establish the installer's publisher identity, archival authenticity, historical acquisition/update chain, present key ownership, or the behavior of the actual Java updater. The negative controls validate the independent checker for these modifications; they do not substitute for malformed-input, tamper, interrupted-update, rollback, or recovery tests inside an approved guest. W09's infrastructure and actual-updater execution requirements remain open.
