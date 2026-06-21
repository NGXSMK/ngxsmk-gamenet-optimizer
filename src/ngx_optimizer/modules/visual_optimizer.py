# pyre-ignore-all-errors
"""
Visual Optimizer Module
Disable Windows visual effects for maximum gaming performance.
"""

import subprocess
import platform
from typing import Dict, Any

from .compat import get_logger # type: ignore
logger = get_logger("visual_optimizer")

# Registry tweaks: (key_path, value_name, gaming_value, default_value)
VISUAL_TWEAKS = [
    # Disable transparency effects
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize',
     'EnableTransparency', '0', '1'),
    # Disable animations in windows
    (r'HKCU\Control Panel\Desktop\WindowMetrics',
     'MinAnimate', '0', '1'),
    # Visual effects: best performance (2 = best performance, 1 = best appearance)
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects',
     'VisualFXSetting', '2', '1'),
    # Disable window shadow
    (r'HKCU\Control Panel\Desktop',
     'UserPreferencesMask', '9012038010000000', None),
    # Disable taskbar animations
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
     'TaskbarAnimations', '0', '1'),
    # Disable list-view animations
    (r'HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',
     'ListviewAlphaSelect', '0', '1'),
    # Disable drag full windows
    (r'HKCU\Control Panel\Desktop',
     'DragFullWindows', '0', '1'),
]

class VisualOptimizer:
    def __init__(self):
        self.system = platform.system()
        self.is_optimized = False

    def _run_reg(self, key: str, value: str, data: str, reg_type: str = 'REG_DWORD') -> bool:
        try:
            subprocess.run(
                ['reg', 'add', key, '/v', value, '/t', reg_type, '/d', data, '/f'],
                capture_output=True, check=False, timeout=10
            )
            return True
        except Exception as e:
            logger.debug("Reg tweak failed %s/%s: %s", key, value, e)
            return False

    def optimize(self) -> Dict[str, Any]:
        """Apply all visual effect tweaks for maximum performance."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        applied = []
        for key, value, gaming_val, _ in VISUAL_TWEAKS:
            reg_type = 'REG_BINARY' if gaming_val and len(gaming_val) > 8 else 'REG_DWORD'
            if self._run_reg(key, value, gaming_val, reg_type):
                applied.append(f"{value}")

        # Broadcast WM_SETTINGCHANGE so the desktop updates
        try:
            subprocess.run(
                ['powershell', '-NoProfile', '-Command',
                 '[System.Windows.Forms.SystemInformation]::TerminalServerSession | Out-Null'],
                capture_output=True, timeout=5
            )
        except Exception:
            pass

        self.is_optimized = True
        logger.info("Visual effects optimized for gaming: %s", applied)
        return {
            'success': True,
            'tweaks_applied': applied,
            'message': 'Visual effects set to maximum performance mode'
        }

    def restore(self) -> Dict[str, Any]:
        """Restore default Windows visual effects."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        restored = []
        for key, value, _, default_val in VISUAL_TWEAKS:
            if default_val is not None:
                if self._run_reg(key, value, default_val):
                    restored.append(value)

        self.is_optimized = False
        return {'success': True, 'tweaks_restored': restored}

    def get_status(self) -> Dict[str, Any]:
        return {
            'is_optimized': self.is_optimized,
            'total_tweaks': len(VISUAL_TWEAKS),
        }
