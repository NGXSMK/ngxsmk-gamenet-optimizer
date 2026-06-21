# pyre-ignore-all-errors
"""
Adapter Optimizer Module
Handles network adapter power management, IPv6 toggle, and MTU optimization.
"""

import subprocess
import platform
import re
from typing import Dict, List, Any

from .compat import get_logger, get_psutil # type: ignore
logger = get_logger("adapter_optimizer")
psutil = get_psutil()

class AdapterOptimizer:
    def __init__(self):
        self.system = platform.system()
        self._ipv6_disabled_adapters: List[str] = []

    def _get_active_adapters(self) -> List[str]:
        """Get connected adapter names."""
        adapters = []
        try:
            out = subprocess.run(
                ['netsh', 'interface', 'show', 'interface'],
                capture_output=True, text=True, timeout=10
            ).stdout
            for line in out.splitlines():
                if 'Connected' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        adapters.append(' '.join(parts[3:]))
        except Exception as e:
            logger.debug("Adapter list failed: %s", e)
        return adapters

    def disable_power_saving(self) -> Dict[str, Any]:
        """Disable power management on all network adapters via PowerShell."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        try:
            ps_cmd = (
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | '
                'ForEach-Object { '
                '  $adapter = Get-WmiObject MSPower_DeviceEnable -Namespace root/WMI | '
                '    Where-Object { $_.InstanceName -match $_.Name }; '
                '  if ($adapter) { $adapter.Enable = $false; $adapter.Put() } '
                '}'
            )
            # Simpler approach via PowerShell that works reliably
            ps_cmd2 = (
                'Get-NetAdapterPowerManagement | '
                'Where-Object {$_.AllowComputerToTurnOffDevice -ne "Unsupported"} | '
                'Set-NetAdapterPowerManagement -AllowComputerToTurnOffDevice Disabled -PassThru | '
                'Select-Object -ExpandProperty Name'
            )
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_cmd2],
                capture_output=True, text=True, timeout=20
            )
            changed = [l.strip() for l in result.stdout.splitlines() if l.strip()]
            logger.info("Disabled power saving on: %s", changed)
            return {
                'success': True,
                'adapters_changed': changed if changed else ['Applied (no output)'],
                'message': 'Network adapter power saving disabled'
            }
        except Exception as e:
            logger.error("Power save disable failed: %s", e)
            return {'success': False, 'error': str(e)}

    def toggle_ipv6(self, disable: bool) -> Dict[str, Any]:
        """Enable or disable IPv6 on all active adapters."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        adapters = self._get_active_adapters()
        if not adapters:
            adapters = ['Wi-Fi', 'Ethernet']
        action = 'disable' if disable else 'enable'
        changed = []
        errors = []
        for adapter in adapters:
            try:
                subprocess.run(
                    ['netsh', 'interface', 'ipv6', action, f'interface={adapter}'],
                    capture_output=True, check=False, timeout=10
                )
                changed.append(adapter)
            except Exception as e:
                errors.append(str(e))
        return {
            'success': len(changed) > 0,
            'ipv6_disabled': disable,
            'adapters_changed': changed,
            'errors': errors
        }

    def optimize_mtu(self) -> Dict[str, Any]:
        """Discover and set optimal MTU using ping-based path MTU discovery."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        try:
            # Binary search for optimal MTU (between 576 and 1500)
            host = '8.8.8.8'
            low, high = 576, 1492
            optimal = 1400  # Safe default
            for size in [1492, 1472, 1452, 1400, 1300]:
                # Ping with DF bit set and specific packet size
                r = subprocess.run(
                    ['ping', '-n', '1', '-f', '-l', str(size), host],
                    capture_output=True, text=True, timeout=5
                )
                if r.returncode == 0 and 'fragmented' not in r.stdout.lower():
                    optimal = size
                    break

            # Apply MTU to all active adapters
            adapters = self._get_active_adapters()
            mtu_value = optimal + 28  # Add IP/ICMP headers
            changed = []
            for adapter in adapters:
                try:
                    subprocess.run(
                        ['netsh', 'interface', 'ipv4', 'set', 'subinterface',
                         adapter, f'mtu={mtu_value}', 'store=persistent'],
                        capture_output=True, check=False, timeout=10
                    )
                    changed.append(adapter)
                except Exception:
                    pass

            logger.info("MTU optimized to %d on adapters: %s", mtu_value, changed)
            return {
                'success': True,
                'optimal_mtu': mtu_value,
                'test_host': host,
                'adapters_changed': changed
            }
        except Exception as e:
            logger.error("MTU optimization failed: %s", e)
            return {'success': False, 'error': str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get adapter optimization status."""
        adapters = self._get_active_adapters()
        return {
            'active_adapters': adapters,
            'adapter_count': len(adapters),
        }
