# pyre-ignore-all-errors
"""
Startup Manager Module
Manage Windows auto-startup registry entry for the optimizer.
"""

import platform
import sys
import os
from typing import Dict, Any

from .compat import get_logger # type: ignore
logger = get_logger("startup_manager")

STARTUP_KEY   = r"Software\Microsoft\Windows\CurrentVersion\Run"
STARTUP_NAME  = "NGXSMK_GameNet_Optimizer"

class StartupManager:
    def __init__(self):
        self.system = platform.system()

    def _get_exe_path(self) -> str:
        """Return the path of the running executable or script."""
        if getattr(sys, 'frozen', False):
            return f'"{sys.executable}"'
        # Running as a script — wrap with python
        script = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'api.py')
        )
        return f'"{sys.executable}" "{script}"'

    def is_enabled(self) -> bool:
        """Check if startup entry exists."""
        if self.system != 'Windows':
            return False
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, STARTUP_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.debug("Startup check failed: %s", e)
            return False

    def enable(self) -> Dict[str, Any]:
        """Add optimizer to Windows startup."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        try:
            import winreg
            exe_path = self._get_exe_path()
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, STARTUP_NAME, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            logger.info("Startup entry added: %s", exe_path)
            return {'success': True, 'path': exe_path}
        except Exception as e:
            logger.error("Failed to enable startup: %s", e)
            return {'success': False, 'error': str(e)}

    def disable(self) -> Dict[str, Any]:
        """Remove optimizer from Windows startup."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, STARTUP_NAME)
            winreg.CloseKey(key)
            logger.info("Startup entry removed.")
            return {'success': True}
        except FileNotFoundError:
            return {'success': True, 'note': 'Entry was not present'}
        except Exception as e:
            logger.error("Failed to disable startup: %s", e)
            return {'success': False, 'error': str(e)}

    def get_status(self) -> Dict[str, Any]:
        enabled = self.is_enabled()
        return {
            'enabled': enabled,
            'startup_name': STARTUP_NAME,
        }
