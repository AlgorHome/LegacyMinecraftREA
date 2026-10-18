# Phase 5E.3 — Large installed-mod grid stability

**Draft: Windows compilation and Xbox Series X hardware stress tests pending.**

This targeted increment clamps the installed-mod grid selection and viewport to the current number of JARs, including disabled JARs. It handles empty collections, stale selections after mod removal, and scroll offsets that are beyond the end after the list shrinks. The same normalizer runs on entry and after list updates. No file formats, mod toggle/removal logic, download logic, entitlement checks, or authentication behavior were changed.

This is *not* a claim of proven large-library performance or memory stability. Hardware stress testing is required.

## Xbox stress test
1. Create or import a **disposable** profile with many mod entries (e.g. 50-100 test JARs; do not rely on them for actual gameplay).
2. Rapidly scroll to the end and back with D-pad and shoulder paging; selected card stays visible and input responsive.
3. Disable/re-enable entries near the final row, including an odd number of mods.
4. Remove the final entries via two-X confirmation and confirm no crash, blank/offscreen selection or stale scroll.
5. Remove all remaining entries in a test profile, then reopen and confirm empty state and action bar navigation.
6. Restart repeatedly; switch between small and large profiles; verify dependency warnings, R3 inspection, browsing, and sign-in.
7. Record approximate profile size, test duration and any UI stalls or memory-related failures.
