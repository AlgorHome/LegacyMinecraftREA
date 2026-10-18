# LegacyForge Launcher

**Minecraft Java. Reforged for Xbox.**

LegacyForge Launcher is an experimental Minecraft Java Edition launcher intended for Xbox Series X|S Developer Mode. This repository contains a UWP launcher, graphics/input compatibility code, and mod-loader integration.

## Project identity

- App name: **LegacyForge Launcher**
- UWP package identity: `AlgorHome.LegacyForge`
- UWP publisher: `CN=AlgorHome`
- Application executable: `LegacyForge.exe`
- Built package: `output/LegacyForge_<version>.appx`

## Launcher UI V2

The new QR-free account UI is being developed on a feature branch. See [UI V2 specification and Xbox test checklist](docs/UI-V2.md). The working Microsoft authentication and Minecraft launch logic remain unchanged.

## Build

On Windows, install Visual Studio C++ build tools, a suitable Windows SDK, the required JDKs, and Git. From the repository root:

```powershell
.\scripts\setup.ps1
.\build.ps1
```

The scripts prepare runtime dependencies and generate a signed UWP package. This rename has not been verified with a clean Windows build or an Xbox hardware test.

## Project origins and dependencies

This work is based on or integrates prior Minecraft launcher/compatibility work, including the [JavaUWP / Bandit Launcher project](https://github.com/veroxsity/JavaUWP). Some internal class names, mod IDs, bundled assets, service URLs, and code identifiers still reflect upstream components; those identifiers are not equivalent to the public-facing LegacyForge name. Third-party code and binaries retain their respective licenses and attribution requirements.

LegacyForge does not configure BanditVault telemetry by default. To enable a separately operated endpoint, see [privacy and data flows](docs/PRIVACY.md).\n\nMinecraft and Mojang game assets are not included. See [third-party components](docs/THIRD-PARTY.md) and [architecture](docs/ARCHITECTURE.md).
