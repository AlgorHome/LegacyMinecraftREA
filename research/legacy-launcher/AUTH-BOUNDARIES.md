# Authentication and licensing boundaries

Research date: 2026-10-17 (America/Chicago). Static evidence only unless explicitly marked historical.

## Installed launcher's architecture

**Confirmed [E03]:** `MinecraftOAuthAuthenticate.authenticate` contains the sequence Microsoft authorization-code OAuth → Xbox Live → XSTS → Minecraft services token → GameOwnershipValidator → Minecraft profile/conversion. Constants identify login.live.com OAuth endpoints, user.auth.xboxlive.com, xsts.auth.xboxlive.com, api.minecraftservices.com authentication/login_with_xbox, entitlements/license and minecraft/profile. These are recovered implementation endpoints, not verified current service contracts or captured traffic.

**Confirmed:** GameOwnershipValidator sends a Bearer-authorized entitlement request, rejects empty item lists and requires both `product_minecraft` and `game_minecraft` entries in this inspected implementation. PlainUser/PlainAuth and other account-provider classes also exist; a launcher-local identity is not proof of Microsoft authentication or Java ownership. Third-party modes are not an implementation pattern for bypassing ownership.

**Confirmed:** ProfileManager persists account/profile sets through Gson with temporary output and Files.move. MinecraftUserJsonizer payload types include Microsoft and Minecraft token objects. Token values and actual profile contents were not inspected. **Unknown:** encryption/protection at rest, renewal lifecycle in every provider, and full redaction coverage. Do not call this secure-vault storage without additional evidence.

## Downloading versus launching

**Confirmed:** catalog/library/asset/runtime acquisition is structurally separate from the Microsoft authentication flow. Public metadata/artifact acquisition can be an installation-preparation activity without collecting a user's Microsoft credentials. That does not authorize copying restricted game content to a research repository or demonstrate legitimate unauthenticated gameplay. [E03/E10]

**Inferred:** maintain distinct states for local launcher profile, Microsoft sign-in, Minecraft services authorization, ownership validation, and game profile. A downloaded client JAR or Xbox console sign-in is insufficient evidence of Java entitlement. No ownership or online-session check was bypassed or tested here.

## Preserve LegacyForge's existing boundaries

**Confirmed [E07]:** [MC.Xbox/auth/minecraft_auth.cpp:391](https://github.com/AlgorHome/LegacyForge/blob/d1453434ceefe73bef5aff497194e09f39dde7e1/MC.Xbox/auth/minecraft_auth.cpp#L391) sequences XBL/XSTS/Minecraft authentication, then entitlement and profile retrieval. `EnsureMinecraftEntitlement` at line 332 accepts recognized `game_minecraft` or `product_minecraft` items; do not silently copy the installed launcher's different both-item predicate. Present service compatibility was not authenticated or tested.

**Confirmed:** refresh tokens use Windows PasswordVault/PasswordCredential in minecraft_auth.cpp:17–61. Local sessions are separate in App.cpp:515–554; launcher_ui.cpp:1083 and 1108 block Play/Repair without the existing ownership boundary. `common/launch_diagnostics.h:9–15` redacts both token argument syntaxes; minecraft_launch.cpp uses that helper when logging game args. This narrow helper does not prove all possible JVM/user-supplied text is redacted.

**Proposed:** retain those checks and storage. Any account changes require separate scope. Use synthetic credentials for future tests and keep access/refresh tokens, device codes, personal UUID/name/account records and raw authentication logs out of research artifacts. No authentication was performed in this investigation.

## Continuation: persistence, refresh and service support

E12 traces raw token-string getters into JSON payload fields, Gson serialization and normal Java file output. Application-level JSON serialization is Confirmed for the traced path; actual saved contents, OS protection/ACLs and account values were not inspected. Refresh repeats the ownership/profile chain after token refresh. E13 confirms the original archived launcher also contains the Microsoft/XBL/XSTS/Minecraft/ownership/profile flow. Neither provider architecture grants permission to bypass ownership.

Official [authorization-code](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow) and [device-flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code) documents establish generic Microsoft identity contracts; [XSTS guidance](https://learn.microsoft.com/en-us/gaming/gdk/docs/services/fundamentals/s2s-auth-calls/service-authentication/security-tokens/live-security-tokens?view=gdk-2604) describes relying-party-specific Xbox tokens. They do not authorize every Minecraft relying party/client. No authoritative public Minecraft launcher API contract was established for the observed service endpoints; registration/scopes/current service permission and live ownership remain Unknown/BLOCKED. No account or token test was run.
