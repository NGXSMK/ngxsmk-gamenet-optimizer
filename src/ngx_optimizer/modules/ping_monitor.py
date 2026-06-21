# pyre-ignore-all-errors
"""
Ping Monitor Module
Maintains a rolling history of ping measurements to key servers for live charting.
"""

import threading
import time
import subprocess
import platform
import re
import statistics
from typing import Dict, List, Any, Optional
from datetime import datetime

from .compat import get_logger # type: ignore
logger = get_logger("ping_monitor")

MONITOR_TARGETS = {
    '8.8.8.8':        'Google DNS',
    '1.1.1.1':        'Cloudflare',
    '104.160.131.1':  'LoL NA',
    '104.160.141.3':  'LoL EUW',
}

class PingMonitor:
    HISTORY_LEN = 60  # Keep last 60 samples

    def __init__(self):
        self.system = platform.system()
        self._lock = threading.Lock()
        self._history: Dict[str, List[Dict[str, Any]]] = {
            host: [] for host in MONITOR_TARGETS
        }
        self._is_running = False
        self._thread: Optional[threading.Thread] = None

    def start(self, interval: int = 3):
        """Start continuous ping monitoring."""
        if self._is_running:
            return
        self._is_running = True
        self._thread = threading.Thread(
            target=self._loop, args=(interval,), daemon=True
        )
        self._thread.start()

    def stop(self):
        """Stop ping monitoring."""
        self._is_running = False

    def _ping_once(self, host: str) -> float:
        """Ping host once and return latency in ms, or -1 on failure."""
        try:
            flag = '-n' if self.system == 'Windows' else '-c'
            result = subprocess.run(
                ['ping', flag, '1', host],
                capture_output=True, text=True, timeout=3
            )
            if result.returncode != 0:
                return -1.0
            for line in result.stdout.splitlines():
                m = re.search(r'time[=<]([\d.]+)\s*ms', line, re.IGNORECASE)
                if m:
                    return float(m.group(1))
        except Exception:
            pass
        return -1.0

    def _loop(self, interval: int):
        """Main monitoring loop — pings all targets sequentially."""
        while self._is_running:
            ts = datetime.now().isoformat()
            for host in MONITOR_TARGETS:
                latency = self._ping_once(host)
                entry = {
                    'timestamp': ts,
                    'latency': latency,
                    'host': host,
                    'label': MONITOR_TARGETS[host]
                }
                with self._lock:
                    self._history[host].append(entry)
                    if len(self._history[host]) > self.HISTORY_LEN:
                        self._history[host].pop(0)
            time.sleep(interval)

    def get_history(self) -> Dict[str, Any]:
        """Return full ping history for all tracked hosts."""
        with self._lock:
            result = {}
            for host, entries in self._history.items():
                valid = [e['latency'] for e in entries if e['latency'] >= 0]
                result[host] = {
                    'label': MONITOR_TARGETS[host],
                    'history': list(entries),
                    'current': entries[-1]['latency'] if entries else -1,
                    'avg': round(statistics.mean(valid), 1) if valid else -1,
                    'min': round(min(valid), 1) if valid else -1,
                    'max': round(max(valid), 1) if valid else -1,
                }
            return result

    def get_status(self) -> Dict[str, Any]:
        return {
            'is_running': self._is_running,
            'targets': list(MONITOR_TARGETS.values()),
            'history_len': self.HISTORY_LEN,
        }
