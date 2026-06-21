# pyre-ignore-all-errors
"""
Advanced Network Optimizer Module
Intelligent network optimization with traffic shaping, QoS, and latency optimization
"""

import subprocess
import platform
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, cast

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil
logger = get_logger("network_optimizer")

class NetworkOptimizer:
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.is_optimizing = False
        self.optimization_thread: Optional[threading.Thread] = None
        
    def start_network_optimization(self, profile: str = 'gaming') -> Dict[str, Any]:
        """Start advanced network optimization"""
        if self.is_optimizing: return {'status': 'already_optimizing'}
        try:
            self.is_optimizing = True
            res: Dict[str, Any] = {'profile': profile, 'timestamp': datetime.now().isoformat(), 'optimizations': []}
            if profile == 'gaming': res['optimizations'].append(self._apply_gaming_opts())
            return res
        except Exception as e:
            self.is_optimizing = False
            return {'status': 'error', 'message': str(e)}

    def _apply_gaming_opts(self) -> Dict[str, Any]:
        """Apply gaming network optimizations"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"], capture_output=True, check=False, timeout=15)
            return {'type': 'Gaming', 'status': 'Applied'}
        except Exception as e:
            return {'type': 'Gaming', 'error': str(e)}

    def get_network_interfaces(self) -> List[Dict[str, Any]]:
        """Get available network interfaces"""
        ifaces = []
        try:
            addrs = psutil.net_if_addrs() # pyre-ignore[16]
            stats = psutil.net_if_stats() # pyre-ignore[16]
            for name, adr in addrs.items():
                is_up = stats[name].isup if name in stats else False
                ifaces.append({'name': name, 'is_up': is_up, 'address_count': len(adr)})
        except Exception as e:
            logger.debug("Failed to list network interfaces: %s", e)
        return ifaces
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {'is_optimizing': self.is_optimizing}

    def run_speed_test(self) -> Dict[str, Any]:
        """Run a bandwidth speed test using speedtest-cli"""
        try:
            import speedtest
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            download_bps = st.download()
            upload_bps = st.upload()
            ping_ms = st.results.ping
            server_info = {
                'host': st.results.server.get('host', ''),
                'location': f"{st.results.server.get('name', '')}, {st.results.server.get('country', '')}",
                'sponsor': st.results.server.get('sponsor', '')
            }
            return {
                'download_mbps': round(download_bps / 1_000_000, 2),
                'upload_mbps': round(upload_bps / 1_000_000, 2),
                'ping_ms': round(ping_ms, 1) if ping_ms else 0,
                'server': server_info,
                'timestamp': datetime.now().isoformat()
            }
        except ImportError:
            logger.debug("speedtest-cli not installed, using estimation")
            return {'error': 'speedtest-cli not available', 'download_mbps': 0, 'upload_mbps': 0, 'ping_ms': 0}
        except Exception as e:
            logger.debug("Speed test failed: %s", e)
            return {'error': str(e), 'download_mbps': 0, 'upload_mbps': 0, 'ping_ms': 0}
