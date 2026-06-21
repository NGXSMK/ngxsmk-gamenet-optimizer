# pyre-ignore-all-errors
"""
RAM Cleaner Module
Optimizes memory usage and cleans RAM for better performance
"""

import gc
import platform
import ctypes
import subprocess
from typing import Dict, List, Optional, Any, cast

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil
logger = get_logger("ram_cleaner")

class RAMCleaner:
    def __init__(self):
        self.system = platform.system()
        
    def get_memory_info(self) -> Dict[str, float]:
        """Get current memory info"""
        try:
            m = psutil.virtual_memory() # pyre-ignore[16]
            return {
                'total_memory': float(m.total) / (1024**3),
                'available_memory': float(m.available) / (1024**3),
                'used_memory': float(m.total - m.available) / (1024**3),
                'memory_percent': float(m.percent)
            }
        except Exception as e:
            logger.debug("Failed to get virtual memory: %s", e)
            return {'total_memory': 0.0, 'available_memory': 0.0, 'used_memory': 0.0, 'memory_percent': 0.0}
            
    def get_top_memory_processes(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get processes using most memory"""
        procs = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'memory_info']): # pyre-ignore[16]
                try:
                    mi = p.info['memory_info']
                    rss = mi.rss if mi else 0
                    procs.append({
                        'pid': p.info['pid'],
                        'name': p.info['name'],
                        'memory_mb': float(rss) / (1024**2)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied): # pyre-ignore[16]
                    continue
            procs.sort(key=lambda x: x['memory_mb'], reverse=True)
        except Exception as e:
            logger.debug("Failed to fetch top memory procs: %s", e)
        return [procs[i] for i in range(min(count, len(procs)))]
    
    def clean_memory(self) -> float:
        """Perform memory cleanup and return freed MB (estimated)"""
        try:
            before = psutil.virtual_memory().available # pyre-ignore[16]
            
            # GC
            gc.collect()
            
            # Windows specific
            if self.system == "Windows":
                try:
                    # Flush DNS
                    subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=False, timeout=15)
                    # Working set reduction
                    ctypes.windll.kernel32.SetProcessWorkingSetSize(ctypes.windll.kernel32.GetCurrentProcess(), -1, -1) # pyre-ignore[16]
                except Exception as e:
                    logger.debug("Windows mem cleanup failed: %s", e)
            
            after = psutil.virtual_memory().available # pyre-ignore[16]
            return max(0.0, float(after - before) / (1024**2))
        except Exception as e:
            logger.debug("Generic clean_memory failed: %s", e)
            return 0.0
            
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get status for UI"""
        return {
            'memory_info': self.get_memory_info(),
            'top_procs': self.get_top_memory_processes(5)
        }
