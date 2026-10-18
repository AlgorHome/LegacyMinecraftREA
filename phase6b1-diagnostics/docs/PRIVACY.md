# LegacyForge privacy and data flows

LegacyForge Launcher is an experimental Xbox UWP Minecraft Java launcher maintained under the AlgorHome repository. This document describes the current source behavior; it is not a substitute for verifying a compiled release.

## Microsoft and Minecraft sign-in

The launcher uses Microsoft's device-code sign-in flow, exchanges tokens through Xbox Live/XSTS/Minecraft Services, and checks Minecraft Java Edition ownership. The player's username, UUID, and access token are used to launch the game. A refresh token may persist in Windows Credential Locker.

The existing authentication implementation may still use a third-party public Microsoft application registration. The consent-screen application name should be independently verified before shipping a public release.

## LegacyForge telemetry

The inherited telemetry client remains in the source code, but **there is no default telemetry destination** in LegacyForge. Automatic event uploads and the remote compatibility-feed refresh are disabled unless an operator deliberately configures an endpoint.

To configure an independently controlled telemetry endpoint, set `LEGACYFORGE_TELEMETRY_ENDPOINT` in the application environment or supply a URL in `LocalState\telemetry\\endpoint.txt`. An endpoint may receive session/crash information only when the user grants telemetry consent; check the telemetry implementation and any server privacy policy before enabling. The compatibility feed requests `/v1/compat` from the configured endpoint even when telemetry consent is off, so configuring an endpoint enables that outbound request.

Locally stored telemetry state can include consent, an installation identifier, queued crash events, and compatibility-feed cache in `LocalState\telemetry`. See `MC.Xbox/telemetry/` for exact behavior.

LegacyForge does **not** use `telemetry.banditvault.co.uk` by default. We have not replaced it with an AlgorHome server.

## Remote file manager and mouse relay

The launcher provides optional local-network HTTP functionality. It is not intended for exposure to the public internet. Use it on a trusted network and stop it when not needed.

## Dependencies and project history

Minecraft/Microsoft, Modrinth, and other accessed external services have their own policies. Portions of the compatibility layer and application were adapted from [JavaUWP / Bandit Launcher](https://github.com/veroxsity/JavaUWP); names in internal APIs, Java packages, filesystem folders, and compatibility metadata may retain upstream identifiers.

The upstream project's privacy and developer contact details do not constitute LegacyForge's support contacts or privacy guarantees. For project questions, use [repository issues](https://github.com/AlgorHome/LegacyForge/issues).
