# pyre-ignore-all-errors
"""
League of Legends Specific Optimizer
Specialized optimizations for League of Legends
"""

import subprocess
import platform
import gc
from typing import Dict, List, Any

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil
logger = get_logger("lol_optimizer")

class LoLOptimizer:
    def __init__(self):
        self.system = platform.system()
        self.lol_processes = ['league of legends.exe', 'lol.exe', 'riotclient.exe', 'leagueclient.exe']
        
    def detect_lol_processes(self) -> List[Any]:
        """Detect League of Legends related processes"""
        procs = []
        try:
            for proc in psutil.process_iter(['pid', 'name']): # pyre-ignore[16]
                try:
                    name = str(proc.info.get('name', '')).lower()
                    if any(p in name for p in self.lol_processes):
                        procs.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied): # pyre-ignore[16]
                    continue
        except Exception as e:
            logger.debug("Failed to detect lol processes: %s", e)
        return procs
    
    def optimize_lol_performance(self) -> Dict[str, Any]:
        """Optimize League of Legends performance"""
        res: Dict[str, Any] = {'processes_optimized': 0, 'priority_set': False, 'errors': []}
        try:
            procs = self.detect_lol_processes()
            for p in procs:
                try:
                    p.nice(psutil.HIGH_PRIORITY_CLASS if self.system == "Windows" else -10) # pyre-ignore[16]
                    res['processes_optimized'] += 1
                    res['priority_set'] = True
                except (psutil.AccessDenied, psutil.NoSuchProcess): # pyre-ignore[16]
                    continue
            if self.system == "Windows":
                subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=False, timeout=15)
            gc.collect()
        except Exception as e:
            res['errors'].append(str(e))
        return res
    
    def get_lol_performance_metrics(self) -> Dict[str, float]:
        """Get performance metrics for LoL"""
        try:
            procs = self.detect_lol_processes()
            if not procs:
                return {'running': 0.0, 'mem_mb': 0.0}
            mem = sum(p.memory_info().rss for p in procs) / (1024 * 1024)
            return {'running': float(len(procs)), 'mem_mb': mem}
        except Exception as e:
            logger.debug("Failed to get lol network metrics: %s", e)
            return {'running': 0.0, 'mem_mb': 0.0}
    
    def get_lol_server_latency(self) -> Dict[str, float]:
        """Test latency to LoL servers"""
        servers = {'NA': '104.160.131.1', 'EUW': '104.160.141.3', 'KR': '104.160.156.1'}
        lats: Dict[str, float] = {}
        for reg, srv in servers.items():
            try:
                cmd = ['ping', '-n' if self.system == "Windows" else '-c', '2', srv]
                pr = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                lats[reg] = self._parse_ping(pr.stdout) if pr.returncode == 0 else 999.0
            except Exception as e:
                logger.debug("Latency test for %s failed: %s", reg, e)
                lats[reg] = 999.0
        return lats
    
    def _parse_ping(self, out: str) -> float:
        """Simple ping output parser"""
        for line in out.split('\n'):
            if 'time=' in line or 'time<' in line:
                try:
                    p = line.split('time' + ('=' if 'time=' in line else '<'))[1].split()[0].replace('ms', '')
                    return float(p)
                except (IndexError, ValueError):
                    pass
        return 999.0
