# pyre-ignore-all-errors
"""
DNS Switcher Module
Switch DNS servers on all active network adapters for gaming-optimized latency.
"""

import subprocess
import platform
import re
from typing import Dict, List, Any, Optional

from .compat import get_logger # type: ignore
logger = get_logger("dns_switcher")

DNS_PRESETS: Dict[str, Dict[str, str]] = {
    'cloudflare': {'primary': '1.1.1.1',   'secondary': '1.0.0.1',   'label': 'Cloudflare (1.1.1.1)'},
    'google':     {'primary': '8.8.8.8',   'secondary': '8.8.4.4',   'label': 'Google (8.8.8.8)'},
    'opendns':    {'primary': '208.67.222.222', 'secondary': '208.67.220.220', 'label': 'OpenDNS'},
    'quad9':      {'primary': '9.9.9.9',   'secondary': '149.112.112.112', 'label': 'Quad9 (9.9.9.9)'},
}

class DNSSwitcher:
    def __init__(self):
        self.system = platform.system()
        self.current_preset: Optional[str] = None
        self._original_dns: Dict[str, List[str]] = {}  # adapter -> [dns list]

    def _get_active_adapters(self) -> List[str]:
        """Get names of active (up) network adapters."""
        adapters = []
        try:
            out = subprocess.run(
                ['netsh', 'interface', 'show', 'interface'],
                capture_output=True, text=True, timeout=10
            ).stdout
            for line in out.splitlines():
                if 'Connected' in line or 'Enabled' in line:
                    # Last token is the adapter name
                    parts = line.split()
                    if len(parts) >= 4:
                        adapters.append(' '.join(parts[3:]))
        except Exception as e:
            logger.debug("Failed to list adapters: %s", e)
        return adapters

    def _get_current_dns(self, adapter: str) -> List[str]:
        """Get the current DNS servers for an adapter."""
        dns_list = []
        try:
            out = subprocess.run(
                ['netsh', 'interface', 'ip', 'show', 'dns', f'name={adapter}'],
                capture_output=True, text=True, timeout=10
            ).stdout
            for line in out.splitlines():
                m = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', line)
                if m:
                    dns_list.append(m.group(1))
        except Exception as e:
            logger.debug("Failed to get DNS for %s: %s", adapter, e)
        return dns_list

    def switch_dns(self, preset: str = 'cloudflare', custom_primary: str = '',
                   custom_secondary: str = '') -> Dict[str, Any]:
        """Switch DNS on all active adapters to a preset or custom servers."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}

        if preset == 'custom':
            primary = custom_primary.strip()
            secondary = custom_secondary.strip()
            label = f'Custom ({primary})'
        elif preset in DNS_PRESETS:
            primary = DNS_PRESETS[preset]['primary']
            secondary = DNS_PRESETS[preset]['secondary']
            label = DNS_PRESETS[preset]['label']
        else:
            return {'success': False, 'error': f'Unknown preset: {preset}'}

        adapters = self._get_active_adapters()
        if not adapters:
            # Fallback: try common adapter names
            adapters = ['Wi-Fi', 'Ethernet', 'Local Area Connection']

        changed = []
        errors = []
        for adapter in adapters:
            try:
                # Save original DNS before overwriting
                if adapter not in self._original_dns:
                    self._original_dns[adapter] = self._get_current_dns(adapter)

                subprocess.run(
                    ['netsh', 'interface', 'ip', 'set', 'dns', f'name={adapter}',
                     'source=static', f'address={primary}', 'validate=no'],
                    capture_output=True, check=False, timeout=10
                )
                if secondary:
                    subprocess.run(
                        ['netsh', 'interface', 'ip', 'add', 'dns', f'name={adapter}',
                         f'address={secondary}', 'index=2', 'validate=no'],
                        capture_output=True, check=False, timeout=10
                    )
                changed.append(adapter)
            except Exception as e:
                errors.append(f"{adapter}: {e}")
                logger.debug("DNS switch failed on %s: %s", adapter, e)

        self.current_preset = preset
        return {
            'success': len(changed) > 0,
            'preset': label,
            'primary': primary,
            'secondary': secondary,
            'adapters_changed': changed,
            'errors': errors
        }

    def restore_dns(self) -> Dict[str, Any]:
        """Restore original DNS settings (DHCP) on all adapters."""
        if self.system != 'Windows':
            return {'success': False, 'error': 'Windows only'}
        restored = []
        for adapter, original in self._original_dns.items():
            try:
                subprocess.run(
                    ['netsh', 'interface', 'ip', 'set', 'dns', f'name={adapter}',
                     'source=dhcp'],
                    capture_output=True, check=False, timeout=10
                )
                restored.append(adapter)
            except Exception as e:
                logger.debug("DNS restore failed on %s: %s", adapter, e)
        self._original_dns.clear()
        self.current_preset = None
        return {'success': True, 'restored_adapters': restored}

    def get_status(self) -> Dict[str, Any]:
        """Get current DNS status."""
        presets_list = [
            {'key': k, 'label': v['label'], 'primary': v['primary']}
            for k, v in DNS_PRESETS.items()
        ]
        return {
            'current_preset': self.current_preset,
            'is_custom': self.current_preset is not None,
            'available_presets': presets_list,
        }
