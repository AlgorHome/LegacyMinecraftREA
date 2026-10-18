# Completion audit closure addendum

Closure snapshot: 2026-10-17T06:52:41.7255837Z. This addendum supersedes only the findings listed below; **actual Windows/Xbox/account tests remain BLOCKED**.

The parent corrected W09 to require a genuine publisher-signed positive fixture, W10/W11 to record actual desktop graphics/native providers, the unresolved `1.12.2 Forge selected` blocker and the missing diagnostic-package prerequisites. Those current plan changes were independently read and confirmed.

The auditor changed only `docs/research/legacy-launcher/tools/verify-test-receipts.py`: malformed X12 targets now reject cleanly; predecessor JVM/native/manifest/loader identities and Java major must match the summary; digest letter case is accepted; the loader inventory hash is allowlisted and checked. The tool explicitly says that aggregate 56-target/four-runtime coverage and manual privacy review remain separate.

## Synthetic checker validation

All execution here used `python -B` and independently written validator controls. No launcher, installer, bundled runtime, game, Windows guest, Xbox or account was executed.

The baseline reproduced six checker issues across 27 controls. The corrected checker satisfied **31 of 31 synthetic controls**, including a linked-format positive control, a desktop-provider positive control, case-independent hashes, malformed target rejection, wrong commit/hardware/isolation/time rejection, attachment confinement/hash checks, unsupported/unknown target rejection, missing predecessors and package/tuple/JVM/native/manifest/loader/Java-major mismatches. A CLI check also accepted the BLOCKED template and an explicitly synthetic linked receipt as structurally valid.

These are checker-control results, **zero target tests passed**. Synthetic fixtures remain solely under `analysis-local/final-audit/completion/validator-controls/` and must never be submitted as actual observations. The final checker SHA256 is `8ae33dca3eb3b63742e977e972e6795183edaac6d2bfd55325c04b8783f2d255`.

## Finding closures

- **C01 OPEN_ENVIRONMENT:** No configured approved Windows guest, actual owner console receipts, exact package or account execution evidence supplied. Every actual behavioral outcome remains BLOCKED.
- **C02 CLOSED_DOCUMENTATION_CORRECTION:** W09 JSON now matches prose: retained genuine publisher-signed positive fixture plus corrupted/truncated copies. Missing trusted positive fixture remains a named blocker.
- **C03 CLOSED_DOCUMENTATION_CORRECTION:** W10/W11 now require desktop native_inventory_sha256, graphics_provider_sha256 and loader_inventory_sha256 instead of mandatory Mesa/GLFW hashes.
- **C04 CLOSED_FOR_SINGLE_TARGET_FORMAT_AND_REFERENCE_CHECKING:** X12 now checks one exact approved tuple, supported resolved provider, expected Java major, required passing X01-X11/X13 predecessors and consistent package/tuple/JVM/native/manifest/loader identities. All56-target/four-runtime aggregate coverage and truth of observations are still separate.
- **C05 MITIGATED_MANUAL_REVIEW_REQUIRED:** Nested primary sections now reject unknown fields. Tool docstring explicitly disclaims privacy certification; arbitrary freeform values and attachment content still need owner/manual redaction review.
- **C06 CLOSED_DOCUMENTATION_CORRECTION:** Legacy Forge-selected target explicitly records EXACT_LOADER_VERSION_UNRESOLVED_IN_APPROVED_SOURCE and UNSUPPORTED_PROVIDER; X12 rejects a PASS for it.
- **C07 OPEN_ARTIFACT_PREREQUISITE_NOW_EXPLICIT:** APPROVED_DIAGNOSTIC_PACKAGE_NOT_SUPPLIED is explicit for X03-X08 and every target plan. No diagnostic package or real probe outcome is fabricated.
- **C08 OPEN_FINAL_PUBLICATION_HYGIENE:** tools/__pycache__ was still present at closure snapshot; root notified to exclude/remove generated own cache and regenerate hashes. This auditor used python -B for all checker execution.

The complete control outputs are `validator-controls-baseline.json` and `validator-controls-patched.json`; reproduction source is `validator_control_checks.py`. `completion-audit-closure.json` binds these results and current plan identity.

All 25 gates and 56 catalog rows remain present. Missing environments, exact packages, diagnostic probes, genuine publisher fixture, owner hardware/account outcomes and unrecorded historical facts remain the actual completion boundary. Validator success cannot establish an observation's truth, privacy clearance or aggregate runtime support.

## Subsequent closure observations

At 2026-10-17T06:58:46.9597759Z, root E20's genuine public signed positive fixture was available. Its local SHA256 matched the parent evidence record, which reports independent static signature verification VALID. This closes the missing-positive-fixture prerequisite; actual launcher acceptance/rejection in W09 remains BLOCKED. Root also moved generated Python cache out of publication, and a later read-only check confirmed its absence. These observations supersede the earlier C02/C08 snapshot wording above.

E21 now independently covers all 56 upstream plans: 22 Mojang version JSON documents matched catalog SHA1, 20 exact Fabric profiles were found, 34 resolved Forge/NeoForge coordinates appeared in the public Maven indexes, one source-selected loader remains unresolved and vanilla needs no loader coordinate. No binary was downloaded or target executed.

The serialized target-plan-only runtime crosscheck records Java 25 as the upstream-based expectation for 12 current-runtime rows and adds URL/SHA1/SHA256 references to all 56 rows. Fifty-one expected labels match vanilla's declared major; five select a higher major; none select a lower one. Packaged runtime/JNI/loader/hardware compatibility remains unobserved and every row stays BLOCKED. See catalog-runtime-crosscheck.json for all rows and before/after plan hashes.

