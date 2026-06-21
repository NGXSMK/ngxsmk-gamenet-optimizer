# NGXSMK GameNet Optimizer 2.3.1

## What's New

- **install.bat** — New auto-installer: download one file, double-click, it downloads the right EXE for your system and launches it. No dependencies needed.
- **Windows Setup Installer** — Professional InnoSetup-based `NGXSMK_GameNet_Optimizer_Setup.exe` with Start Menu shortcut, desktop shortcut, and uninstall support.
- **EXE Metadata** — Embedded VERSIONINFO resource (company name, description, version) and assembly manifest to reduce SmartScreen warning severity.
- **Updated Build Pipeline** — Release workflow now builds x64 EXE, x86 EXE, and Setup.exe, then attaches all three to the release.

## Bug Fixes

- Installer scripts no longer require Python, Node.js, or npm — they download pre-built EXEs from GitHub releases.
- Download buttons on website now link directly to release asset files.

## How to Download

| File | Description |
|------|-------------|
| `install.bat` | Auto-downloader — detects your architecture, downloads + runs |
| `NGXSMK_GameNet_Optimizer_Setup.exe` | Professional installer with shortcuts and uninstall |
| `NGXSMK_GameNet_Optimizer_x64.exe` | Portable EXE for 64-bit Windows |
| `NGXSMK_GameNet_Optimizer_x86.exe` | Portable EXE for 32-bit Windows |
