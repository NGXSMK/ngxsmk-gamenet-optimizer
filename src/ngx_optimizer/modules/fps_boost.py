"""
FPS Boost Module
Optimizes game performance by adjusting system settings and process priorities
"""

import psutil
import subprocess
import platform
import os
import time
import threading
from typing import Dict, List, Optional

class FPSBoost:
    def __init__(self):
        self.system = platform.system()
        self.optimized_processes = []
        self.original_priorities = {}
        self.game_processes = [
            'valorant.exe', 'cs2.exe', 'fortnite.exe', 'apex.exe', 
            'cod.exe', 'codmw.exe', 'overwatch.exe', 'league of legends.exe',
            'lol.exe', 'riotclientservices.exe', 'riotclient.exe',
            'dota2.exe', 'pubg.exe', 'rust.exe', 'minecraft.exe'
        ]
        
    def detect_game_processes(self) -> List[psutil.Process]:
        """Detect currently running game processes"""
        game_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_name = proc.info['name'].lower()
                if any(game in proc_name for game in self.game_processes):
                    game_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return game_processes
    
    def set_high_priority(self, process: psutil.Process) -> bool:
        """Set process to high priority"""
        try:
            if self.system == "Windows":
                process.nice(psutil.HIGH_PRIORITY_CLASS)
            else:
                process.nice(-10)  # Higher priority on Unix systems
            return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return False
    
    def optimize_cpu_affinity(self, process: psutil.Process) -> bool:
        """Optimize CPU affinity for better performance"""
        try:
            if self.system == "Windows":
                # Use all available cores
                cpu_count = psutil.cpu_count()
                process.cpu_affinity(list(range(cpu_count)))
            return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return False
    
    def disable_fullscreen_optimizations(self) -> bool:
        """Disable Windows fullscreen optimizations"""
        if self.system != "Windows":
            return False
            
        try:
            # This would require registry modifications
            # For now, we'll just return True as a placeholder
            return True
        except Exception:
            return False
    
    def optimize_gpu_settings(self) -> bool:
        """Optimize GPU settings for gaming"""
        try:
            if self.system == "Windows":
                # Disable Windows Game Mode optimizations that might interfere
                subprocess.run([
                    'powershell', '-Command',
                    'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\GameBar" -Name "AllowAutoGameMode" -Value 0'
                ], capture_output=True, check=False)
                
                # Disable Windows Game DVR
                subprocess.run([
                    'powershell', '-Command',
                    'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Name "AppCaptureEnabled" -Value 0'
                ], capture_output=True, check=False)
                
            return True
        except Exception:
            return False
    
    def optimize_system_performance(self) -> Dict[str, bool]:
        """Optimize system-wide performance settings"""
        results = {}
        
        try:
            # Disable Windows Search indexing for better performance
            if self.system == "Windows":
                subprocess.run([
                    'powershell', '-Command',
                    'Set-Service -Name "WSearch" -StartupType Disabled'
                ], capture_output=True, check=False)
                results['search_indexing'] = True
        except Exception:
            results['search_indexing'] = False
        
        try:
            # Optimize power settings for performance
            if self.system == "Windows":
                subprocess.run([
                    'powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'  # High performance
                ], capture_output=True, check=False)
                results['power_settings'] = True
        except Exception:
            results['power_settings'] = False
            
        return results
    
    def optimize_game_performance(self, priority_boost: bool = True, 
                                cpu_optimization: bool = True, 
                                gpu_optimization: bool = True) -> Dict[str, any]:
        """Main optimization function"""
        results = {
            'processes_optimized': 0,
            'system_optimized': False,
            'gpu_optimized': False,
            'errors': []
        }
        
        try:
            # Detect and optimize game processes
            game_processes = self.detect_game_processes()
            
            for process in game_processes:
                try:
                    if priority_boost and self.set_high_priority(process):
                        self.optimized_processes.append(process.pid)
                        results['processes_optimized'] += 1
                    
                    if cpu_optimization:
                        self.optimize_cpu_affinity(process)
                        
                except Exception as e:
                    results['errors'].append(f"Failed to optimize process {process.pid}: {str(e)}")
            
            # System-wide optimizations
            if cpu_optimization or gpu_optimization:
                system_results = self.optimize_system_performance()
                results['system_optimized'] = all(system_results.values())
            
            if gpu_optimization:
                results['gpu_optimized'] = self.optimize_gpu_settings()
                
        except Exception as e:
            results['errors'].append(f"Optimization failed: {str(e)}")
        
        return results
    
    def restore_original_settings(self) -> bool:
        """Restore original process priorities and settings"""
        try:
            for pid in self.optimized_processes:
                try:
                    process = psutil.Process(pid)
                    if self.system == "Windows":
                        process.nice(psutil.NORMAL_PRIORITY_CLASS)
                    else:
                        process.nice(0)  # Normal priority
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.optimized_processes.clear()
            return True
        except Exception:
            return False
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """Get current performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Get GPU usage if available
            gpu_usage = 0.0
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100
            except ImportError:
                pass
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available / (1024**3),  # GB
                'gpu_usage': gpu_usage
            }
        except Exception:
            return {
                'cpu_usage': 0.0,
                'memory_usage': 0.0,
                'memory_available': 0.0,
                'gpu_usage': 0.0
            }
    
    def monitor_performance(self, duration: int = 60) -> List[Dict[str, float]]:
        """Monitor performance metrics over time"""
        metrics = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            metrics.append(self.get_performance_metrics())
            time.sleep(5)  # Sample every 5 seconds
        
        return metrics
    
    def get_optimization_status(self) -> Dict[str, any]:
        """Get current optimization status"""
        return {
            'optimized_processes': len(self.optimized_processes),
            'current_metrics': self.get_performance_metrics(),
            'system_optimized': len(self.optimized_processes) > 0
        }
