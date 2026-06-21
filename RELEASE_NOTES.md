# NGXSMK GameNet Optimizer 2.3.1

## What's New

- **App Icon** — Custom icon (`icon.ico`) now embedded in all EXEs and the Setup installer. The icon appears on the EXE file, Start Menu shortcut, and desktop shortcut.
- **Windows Setup Installer** — Professional InnoSetup-based `NGXSMK_GameNet_Optimizer_Setup.exe` with Start Menu shortcut, desktop shortcut, and uninstall support.
- **EXE Metadata** — Embedded VERSIONINFO resource (company name, description, version) and assembly manifest to reduce SmartScreen warning severity.
- **Updated Build Pipeline** — Release workflow builds x64 EXE, x86 EXE, and Setup.exe, then attaches all three to the release.

## Bug Fixes

- **EXE crash when installed to Program Files** — All application data files (`config.json`, `profiles.json`, `learning_data.json`, `optimizer.log`) now write to `%APPDATA%\NGXSMK GameNet Optimizer\` instead of the install directory. This fixes the `PermissionError` that occurred when running from `C:\Program Files\`.
- **Website download links** — Download buttons now serve EXEs directly from the Pages site (fetched from latest release).
- **InnoSetup build** — Fixed missing file references that caused installer compile failures.

## How to Download

| File | Description |
|------|-------------|
| `NGXSMK_GameNet_Optimizer_Setup.exe` | Professional installer with shortcuts and uninstall |
| `NGXSMK_GameNet_Optimizer_x64.exe` | Portable EXE for 64-bit Windows |
| `NGXSMK_GameNet_Optimizer_x86.exe` | Portable EXE for 32-bit Windows |

> **Note:** If Windows SmartScreen blocks the download, right-click the file → **Properties** → check **Unblock** → OK.
