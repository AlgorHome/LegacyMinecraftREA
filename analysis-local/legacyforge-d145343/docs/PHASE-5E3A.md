# Phase 5E.3a — Immediate newly created profile rename feedback

**Draft: Windows build and Xbox Series X validation pending.**

- After creating a mod profile, the Profiles grid selects its card by stable profile ID, not the former tile index.
- When the Xbox keyboard submits a profile rename, LegacyForge saves the name, reloads profile cards, restores the selected profile by ID, and refreshes the visible detail title and active-profile name.
- Existing profile targets, mod files, identity accounts, authentication and entitlement checks are unchanged.

## Xbox validation
1. Create a new mod profile and confirm its card becomes selected.
2. Open it immediately, press Y, enter a new name and submit with Enter/keyboard confirmation.
3. Confirm the detail heading changes immediately, without navigating away.
4. Close details: card shows the new name immediately; reenter and verify.
5. Restart, confirm the name persists; rename an older existing profile and verify.
6. Check Y activate, A inspect, X remove, mod browsing and sign-in.
