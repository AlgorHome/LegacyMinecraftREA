# Phase 5E.3b — Local identity display synchronization

**Draft: Windows compilation and Xbox hardware validation pending.**

The Home page previously initialized the displayed local identity only when the main menu was opened. Changing the saved identity through Accounts did not refresh the existing Home display in the same session.

The main-menu Accounts loop now synchronizes `homePlayerName` with the saved local selection after create, rename, selection or deletion operations and after loading the Accounts page. Cursor movement alone does not change the active account. If all local identities are removed, Home shows `Local Launcher`.

This is a **display synchronization fix**, not a Microsoft sign-in or Minecraft ownership change. Local identities remain launcher-only UI metadata and do not unlock Play/Repair.

## Xbox validation
1. Enter Local Launcher Mode and note the Home identity.
2. Create a new local identity in Accounts; return Home and confirm the displayed identity changes immediately.
3. Create or select a second identity; confirm Home reflects the active selection without relaunching.
4. Move the account cursor without selecting; Home must still display the active identity.
5. Rename the active identity and delete it; confirm Home updates or uses the neutral fallback when none remain.
6. Restart, verify the persisted active local identity; check Microsoft sign-in remains unaffected and Play/Repair still require entitlement.
