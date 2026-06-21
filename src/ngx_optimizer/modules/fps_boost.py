# pyre-ignore-all-errors
"""
FPS Boost Module
Optimizes game performance by adjusting system settings and process priorities
"""

import subprocess
import platform
import time
import threading
from typing import Dict, List, Optional, Any, cast

from .compat import get_psutil, get_logger # type: ignore
psutil = get_psutil()
globals()['psutil'] = psutil

logger = get_logger("fps_boost")

class FPSBoost:
    # Class-level constants for better maintainability
    DEFAULT_GAME_PROCESSES = [
        'valorant.exe', 'cs2.exe', 'fortnite.exe', 'apex.exe', 
        'league of legends.exe', 'lol.exe', 'riotclient.exe',
        'dota2.exe', 'pubg.exe', 'rust.exe', 'minecraft.exe'
    ]

    def __init__(self):
        self.system = platform.system()
        self._lock = threading.Lock()
        self.optimized_processes: List[int] = []
        self.game_processes = self.DEFAULT_GAME_PROCESSES
        
    def detect_game_processes(self) -> List[Any]:
        """Detect currently running game processes"""
        game_procs = []
        try:
            for proc in psutil.process_iter(['pid', 'name']): # pyre-ignore[16]
                try:
                    name = str(proc.info.get('name', '')).lower()
                    if any(game in name for game in self.game_processes):
                        game_procs.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied): # pyre-ignore[16]
                    continue
        except Exception as e:
            logger.debug("Failed to detect game procs: %s", e)
        return game_procs
    
    def set_high_priority(self, process: Any) -> bool:
        """Set process to high priority"""
        try:
            if self.system == "Windows":
                process.nice(psutil.HIGH_PRIORITY_CLASS) # pyre-ignore[16]
            else:
                process.nice(-10)
            return True
        except (psutil.AccessDenied, psutil.NoSuchProcess): # pyre-ignore[16]
            return False
    
    def optimize_cpu_affinity(self, process: Any) -> bool:
        """Optimize CPU affinity"""
        try:
            if self.system == "Windows":
                count = psutil.cpu_count() or 1 # pyre-ignore[16]
                process.cpu_affinity(list(range(count))) # pyre-ignore[16]
            return True
        except (psutil.AccessDenied, psutil.NoSuchProcess): # pyre-ignore[16]
            return False
    
    def optimize_gpu_settings(self) -> bool:
        """Optimize GPU settings"""
        if self.system != "Windows": return True
        try:
            subprocess.run(['powershell', '-Command', 'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\GameBar" -Name "AllowAutoGameMode" -Value 0'], capture_output=True, check=False, timeout=15)
            subprocess.run(['powershell', '-Command', 'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Name "AppCaptureEnabled" -Value 0'], capture_output=True, check=False, timeout=15)
            return True
        except Exception as e:
            logger.debug("GPU optim settings fail: %s", e)
            return False
    
    def optimize_system_performance(self) -> Dict[str, bool]:
        """Optimize system-wide performance settings"""
        res = {'power': False}
        try:
            if self.system == "Windows":
                subprocess.run(['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'], capture_output=True, check=False, timeout=15)
                res['power'] = True
        except Exception as e:
            logger.debug("System perf optimization fail: %s", e)
        return res
    
    def optimize_game_performance(self, priority_boost: bool = True, cpu_optimization: bool = True, gpu_optimization: bool = True) -> Dict[str, Any]:
        """Main optimization function"""
        results: Dict[str, Any] = {'processes_optimized': 0, 'system_optimized': False, 'gpu_optimized': False, 'errors': []}
        try:
            procs = self.detect_game_processes()
            for p in procs:
                try:
                    if priority_boost and self.set_high_priority(p):
                        with self._lock:
                            if p.pid not in self.optimized_processes:
                                self.optimized_processes.append(p.pid)
                        results['processes_optimized'] += 1
                    if cpu_optimization: self.optimize_cpu_affinity(p)
                except Exception as e:
                    results['errors'].append(str(e))
            
            if gpu_optimization: results['gpu_optimized'] = self.optimize_gpu_settings()
            results['system_optimized'] = all(self.optimize_system_performance().values())
        except Exception as e:
            results['errors'].append(str(e))
        return results
    
    def restore_original_settings(self) -> bool:
        """Restore original process priorities"""
        try:
            with self._lock:
                current_pids = self.optimized_processes.copy()
            
            for pid in current_pids:
                try:
                    p = psutil.Process(pid) # pyre-ignore[16]
                    p.nice(psutil.NORMAL_PRIORITY_CLASS if self.system == "Windows" else 0) # pyre-ignore[16]
                except (psutil.NoSuchProcess, psutil.AccessDenied): # pyre-ignore[16]
                    continue
            
            with self._lock:
                self.optimized_processes.clear()
            return True
        except Exception as e:
            logger.debug("Restore optim settings fail: %s", e)
            return False
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        try:
            cpu = psutil.cpu_percent(interval=None) # pyre-ignore[16]
            mem = psutil.virtual_memory() # pyre-ignore[16]
            return {
                'cpu_usage': float(cpu),
                'memory_usage': float(mem.percent),
                'memory_available': float(mem.available) / (1024**3)
            }
        except Exception as e:
            logger.debug("FPS get perf metrics fail: %s", e)
            return {'cpu_usage': 0.0, 'memory_usage': 0.0, 'memory_available': 0.0}
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization status"""
        details = []
        with self._lock:
            count = len(self.optimized_processes)
            is_optimized = count > 0
            
            # Fetch names for the optimized PIDs
            for pid in self.optimized_processes:
                try:
                    p = psutil.Process(pid)
                    details.append({'pid': pid, 'name': p.name()})
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
        return {
            'optimized_processes': count,
            'optimized_details': details,
            'current_metrics': self.get_performance_metrics(),
            'system_optimized': is_optimized
        }
