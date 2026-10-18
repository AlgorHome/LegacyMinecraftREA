# Phase 5E.1 — Storage safety on failed mod removal

**Draft: build and Xbox tests pending.**

Fixes a data-integrity edge case in `RemoveProfileModAndUnusedDependencies`: if deletion of the selected JAR fails, the operation now stops immediately. It does **not** delete installation metadata or remove unused dependencies. The existing UI can correctly report "Could not remove" and retains the selected mod.

Successful deletions still follow the prior metadata and unused-dependency cleanup path. This is not a transactional filesystem implementation: interrupted operations, power loss, failed dependent-file deletion, backups, and large-mod stress tests still need broader Phase 5E coverage.

## Xbox acceptance

1. Verify the known-good profile and enabled/disabled mod state persist after restarting the launcher.
2. Remove a disposable enabled mod with the existing two-X confirmation, then restart and confirm removal.
3. Remove a disposable disabled mod with the same confirmation and confirm consistent metadata.
4. Simulate a deletion failure if practical in a controlled test environment; confirm the JAR, its metadata, and dependencies stay in place and the UI says removal failed.
5. Verify profile isolation, known-dependency warnings, R3 inspection, Modrinth browsing, and sign-in.
6. Check that failures are logged and no unrelated mods are removed.

No Minecraft authentication or ownership/Play behavior changes.
