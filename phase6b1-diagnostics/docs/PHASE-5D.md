# Phase 5D — Safer profile mod removal

First increment: Xbox X on an installed mod now requires a second X press on the same selection before removal. The first press displays the filename, warns that unused dependency mods may also be removed, and offers B to cancel. Moving the selection or leaving the grid also cancels the pending removal. The existing dependency cleanup algorithm is unchanged. If removal fails, the status reports the failure instead of claiming success.

**Not yet compiled or hardware-tested.**

## Xbox checks

1. Highlight installed mod and press X once: mod remains present, confirmation text appears.
2. Press B: confirmation cancels, profile details remain open.
3. Press X then change selection: operation cancels; no JAR is removed.
4. Press X twice on the same JAR: mod is removed, unused dependencies handled as before.
5. Restart: removal persists. Recheck mod browsing, profile management, and local mode.

Remaining 5D work: enable/disable, metadata inspection, safe restoration and dependency-aware removal previews.
