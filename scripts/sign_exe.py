"""
Sign the built EXE with a code signing certificate to bypass SmartScreen.

Prerequisites:
  - A code signing certificate (EV or standard) installed on your system
  - Windows SDK (signtool.exe) or Windows Kit

Usage:
  python scripts/sign_exe.py [path_to_exe] [optional_cert_sha1]

If no paths given, signs dist/NGXSMK_GameNet_Optimizer_Advanced.exe by default.
"""

import os
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent

def find_signtool():
    candidates = [
        r'C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe',
        r'C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe',
        r'C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe',
        r'C:\Program Files (x86)\Microsoft SDKs\ClickOnce\SignTool.exe',
        r'C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\signtool.exe',
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c

    # Try PATH
    try:
        result = subprocess.run(['where', 'signtool'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip().splitlines()[0]
    except Exception:
        pass
    return None

def sign_exe(exe_path: str, cert_hash: str = None):
    signtool = find_signtool()
    if not signtool:
        print("[ERROR] signtool.exe not found. Install Windows SDK or Windows Kit.")
        print("  Download: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/")
        return False

    if not os.path.isfile(exe_path):
        print(f"[ERROR] File not found: {exe_path}")
        return False

    cmd = [signtool, 'sign', '/fd', 'SHA256', '/td', 'SHA256', '/as']
    if cert_hash:
        cmd.extend(['/sha1', cert_hash])
    else:
        cmd.append('/a')  # Auto-select best cert

    cmd.append(exe_path)

    print(f"Signing: {exe_path}")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("[OK] EXE signed successfully!")
            return True
        else:
            print(f"[ERROR] Signing failed (code {result.returncode})")
            print(f"  stdout: {result.stdout}")
            print(f"  stderr: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("[ERROR] Signing timed out")
        return False

def main():
    exe_path = sys.argv[1] if len(sys.argv) > 1 else str(PROJECT_ROOT / 'dist' / 'NGXSMK_GameNet_Optimizer_Advanced.exe')
    cert_hash = sys.argv[2] if len(sys.argv) > 2 else None
    success = sign_exe(exe_path, cert_hash)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
