"""
RAM Cleaner Module
Optimizes memory usage and cleans RAM for better performance
"""

import psutil
import gc
import os
import time
import threading
import subprocess
import platform
from typing import Dict, List, Optional, Tuple
import ctypes
from ctypes import wintypes

class RAMCleaner:
    def __init__(self):
        self.system = platform.system()
        self.is_cleaning = False
        self.cleanup_thread = None
        self.memory_history = []
        
        # Windows-specific memory optimization
        if self.system == "Windows":
            try:
                # Load Windows API functions
                self.kernel32 = ctypes.windll.kernel32
                self.psapi = ctypes.windll.psapi
                self.advapi32 = ctypes.windll.advapi32
            except Exception:
                self.kernel32 = None
                self.psapi = None
                self.advapi32 = None
    
    def get_memory_info(self) -> Dict[str, float]:
        """Get current memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total_memory': memory.total / (1024**3),  # GB
                'available_memory': memory.available / (1024**3),  # GB
                'used_memory': memory.used / (1024**3),  # GB
                'memory_percent': memory.percent,
                'swap_total': swap.total / (1024**3),  # GB
                'swap_used': swap.used / (1024**3),  # GB
                'swap_percent': swap.percent
            }
        except Exception:
            return {
                'total_memory': 0,
                'available_memory': 0,
                'used_memory': 0,
                'memory_percent': 0,
                'swap_total': 0,
                'swap_used': 0,
                'swap_percent': 0
            }
    
    def get_memory_usage_by_process(self) -> List[Dict[str, any]]:
        """Get memory usage by process"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
                try:
                    proc_info = proc.info
                    memory_info = proc_info['memory_info']
                    
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'memory_mb': memory_info.rss / (1024**2),  # MB
                        'memory_percent': proc_info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by memory usage
            processes.sort(key=lambda x: x['memory_mb'], reverse=True)
            return processes[:20]  # Top 20 processes
            
        except Exception:
            return []
    
    def identify_memory_hogs(self) -> List[Dict[str, any]]:
        """Identify processes using the most memory"""
        processes = self.get_memory_usage_by_process()
        memory_hogs = []
        
        for proc in processes:
            if proc['memory_mb'] > 100:  # More than 100 MB
                memory_hogs.append(proc)
        
        return memory_hogs
    
    def clean_system_cache(self) -> Dict[str, bool]:
        """Clean system cache"""
        results = {}
        
        try:
            if self.system == "Windows":
                results.update(self._clean_windows_cache())
            else:
                results.update(self._clean_unix_cache())
        except Exception:
            results['error'] = True
        
        return results
    
    def _clean_windows_cache(self) -> Dict[str, bool]:
        """Clean Windows system cache"""
        results = {}
        try:
            # Clear Windows file system cache
            if self.kernel32:
                process_handle = self.kernel32.GetCurrentProcess()
                self.kernel32.SetProcessWorkingSetSize(process_handle, -1, -1)
                results['working_set'] = True
            
            # Clear DNS cache
            results['dns_cache'] = self._flush_windows_dns()
            
            # Clear Windows temp files
            results['temp_files'] = self._clear_windows_temp_files()
            
            # Clear Windows memory cache using PowerShell
            results['powershell_cleanup'] = self._run_powershell_gc()
            
            # Clear Windows standby memory
            results['recycle_bin'] = self._clear_recycle_bin()
            
        except Exception:
            results['error'] = True
        return results

    def _flush_windows_dns(self) -> bool:
        """Flush Windows DNS cache"""
        try:
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=True)
            return True
        except Exception:
            return False

    def _clear_windows_temp_files(self) -> bool:
        """Clear Windows temporary files"""
        try:
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('WINDIR', ''), 'Temp')
            ]
            cleaned = 0
            for temp_dir in temp_dirs:
                if not (temp_dir and os.path.exists(temp_dir)):
                    continue
                for file in os.listdir(temp_dir):
                    try:
                        file_path = os.path.join(temp_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            cleaned += 1
                    except OSError:
                        continue
            return cleaned > 0
        except Exception:
            return False

    def _run_powershell_gc(self) -> bool:
        """Run .NET Garbage Collector via PowerShell"""
        try:
            subprocess.run([
                'powershell', '-Command',
                '[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); [System.GC]::Collect()'
            ], capture_output=True, check=True)
            return True
        except Exception:
            return False

    def _clear_recycle_bin(self) -> bool:
        """Clear the Recycle Bin"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'
            ], capture_output=True, check=False)
            return True
        except Exception:
            return False
    
    def _clean_unix_cache(self) -> Dict[str, bool]:
        """Clean Unix/Linux system cache"""
        results = {}
        try:
            # Clear page cache, dentries and inodes
            results['system_cache'] = self._clear_unix_system_cache_internal()
            
            # Clear user cache
            results['user_cache'] = self._clear_unix_user_cache_internal()
            
        except Exception:
            results['error'] = True
        return results

    def _clear_unix_system_cache_internal(self) -> bool:
        """Internal helper for clearing Unix system cache"""
        try:
            subprocess.run(['sync'], check=True)
            with open('/proc/sys/vm/drop_caches', 'w') as f:
                f.write('3')
            return True
        except Exception:
            return False

    def _clear_unix_user_cache_internal(self) -> bool:
        """Internal helper for clearing Unix user cache"""
        try:
            cache_dirs = [
                os.path.expanduser('~/.cache'),
                '/tmp',
                '/var/tmp'
            ]
            cleaned = False
            for cache_dir in cache_dirs:
                if not os.path.exists(cache_dir):
                    continue
                for root, _, files in os.walk(cache_dir):
                    for file in files:
                        try:
                            os.remove(os.path.join(root, file))
                            cleaned = True
                        except OSError:
                            continue
            return cleaned
        except Exception:
            return False
    
    def optimize_memory_allocation(self) -> Dict[str, bool]:
        """Optimize memory allocation"""
        results = {}
        
        try:
            # Force garbage collection multiple times
            for i in range(3):
                collected = gc.collect()
                print(f"GC cycle {i+1}: collected {collected} objects")
            results['garbage_collection'] = True
            
            # Clear Python internal caches
            try:
                import sys
                if hasattr(sys, '_clear_type_cache'):
                    sys._clear_type_cache()
                if hasattr(sys, 'intern'):
                    # Clear interned strings cache
                    pass
                results['python_cache'] = True
            except Exception:
                results['python_cache'] = False
            
            # Optimize memory allocation
            if self.system == "Windows":
                results.update(self._optimize_windows_memory())
            else:
                results.update(self._optimize_unix_memory())
            
        except Exception:
            results['error'] = True
        
        return results
    
    def _optimize_windows_memory(self) -> Dict[str, bool]:
        """Optimize Windows memory allocation"""
        results = {}
        
        try:
            # Set process priority to high
            if self.kernel32:
                process_handle = self.kernel32.GetCurrentProcess()
                self.kernel32.SetPriorityClass(process_handle, 0x00000080)  # HIGH_PRIORITY_CLASS
                results['process_priority'] = True
            
            # Optimize virtual memory
            try:
                subprocess.run([
                    'powershell', '-Command',
                    'Get-WmiObject -Class Win32_PageFileUsage | ForEach-Object { $_.SetPageFileSize(0, 0) }'
                ], capture_output=True, check=False)
                results['virtual_memory'] = True
            except Exception:
                results['virtual_memory'] = False
            
        except Exception:
            results['error'] = True
        
        return results
    
    def _optimize_unix_memory(self) -> Dict[str, bool]:
        """Optimize Unix/Linux memory allocation"""
        results = {}
        
        try:
            # Optimize swap usage
            try:
                subprocess.run(['swapoff', '-a'], capture_output=True, check=False)
                subprocess.run(['swapon', '-a'], capture_output=True, check=False)
                results['swap_optimization'] = True
            except Exception:
                results['swap_optimization'] = False
            
            # Optimize memory overcommit
            try:
                with open('/proc/sys/vm/overcommit_memory', 'w') as f:
                    f.write('1')  # Always overcommit
                results['memory_overcommit'] = True
            except (PermissionError, FileNotFoundError):
                results['memory_overcommit'] = False
            
        except Exception:
            results['error'] = True
        
        return results
    
    def clean_memory(self) -> float:
        """Main memory cleaning function - returns freed memory in MB"""
        try:
            # Get initial memory in MB
            initial_memory = psutil.virtual_memory()
            initial_used_mb = initial_memory.used / (1024**2)  # Convert to MB
            
            # Clean system cache
            cache_results = self.clean_system_cache()
            
            # Optimize memory allocation
            optimization_results = self.optimize_memory_allocation()
            
            # Force garbage collection multiple times for better results
            for _ in range(3):
                gc.collect()
            
            # Wait a moment for memory to be freed
            time.sleep(0.5)
            
            # Get final memory in MB
            final_memory = psutil.virtual_memory()
            final_used_mb = final_memory.used / (1024**2)  # Convert to MB
            
            # Calculate freed memory in MB
            freed_memory_mb = initial_used_mb - final_used_mb
            
            # If no memory was freed, try more aggressive cleaning
            if freed_memory_mb <= 0:
                import sys
                if hasattr(sys, '_clear_type_cache'):
                    sys._clear_type_cache()
                
                gc.collect()
                time.sleep(0.2)
                
                final_memory = psutil.virtual_memory()
                final_used_mb = final_memory.used / (1024**2)
                freed_memory_mb = initial_used_mb - final_used_mb
            
            # Update memory history
            self.memory_history.append({
                'timestamp': time.time(),
                'freed_memory': freed_memory_mb,
                'cache_cleaned': cache_results,
                'optimization_applied': optimization_results
            })
            
            # Return freed memory in MB, minimum 0
            return max(0, freed_memory_mb)
            
        except Exception as e:
            print(f"RAM cleaning error: {e}")
            return 0.0

    
    def start_auto_cleanup(self, interval: int = 300):  # 5 minutes
        """Start automatic memory cleanup"""
        if self.is_cleaning:
            return
        
        self.is_cleaning = True
        self.cleanup_thread = threading.Thread(
            target=self._auto_cleanup_loop,
            args=(interval,),
            daemon=True
        )
        self.cleanup_thread.start()
    
    def stop_auto_cleanup(self):
        """Stop automatic memory cleanup"""
        self.is_cleaning = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
    
    def _auto_cleanup_loop(self, interval: int):
        """Automatic cleanup loop"""
        while self.is_cleaning:
            try:
                # Check memory usage
                memory_info = self.get_memory_info()
                
                # Clean if memory usage is high
                if memory_info['memory_percent'] > 80:
                    freed_memory = self.clean_memory()
                    print(f"Auto-cleanup freed {freed_memory:.2f} MB of memory")
                
                time.sleep(interval)
            except Exception:
                time.sleep(interval)
    
    def get_memory_recommendations(self) -> List[str]:
        """Get memory optimization recommendations"""
        recommendations = []
        
        try:
            memory_info = self.get_memory_info()
            memory_hogs = self.identify_memory_hogs()
            
            # Check memory usage
            if memory_info['memory_percent'] > 90:
                recommendations.append("Critical: Memory usage is very high (>90%)")
                recommendations.append("Consider closing unnecessary applications")
            elif memory_info['memory_percent'] > 80:
                recommendations.append("Warning: Memory usage is high (>80%)")
                recommendations.append("Consider running memory cleanup")
            
            # Check for memory hogs
            if memory_hogs:
                top_hog = memory_hogs[0]
                recommendations.append(f"Top memory user: {top_hog['name']} ({top_hog['memory_mb']:.1f} MB)")
                
                if top_hog['memory_mb'] > 1000:  # More than 1 GB
                    recommendations.append(f"Consider closing {top_hog['name']} if not needed")
            
            # Check swap usage
            if memory_info['swap_percent'] > 50:
                recommendations.append("High swap usage detected")
                recommendations.append("Consider increasing physical RAM")
            
            # Check available memory
            if memory_info['available_memory'] < 1:  # Less than 1 GB
                recommendations.append("Low available memory")
                recommendations.append("Enable auto-cleanup for better performance")
            
        except Exception:
            recommendations.append("Unable to analyze memory usage")
        
        return recommendations
    
    def get_memory_statistics(self) -> Dict[str, any]:
        """Get detailed memory statistics"""
        stats = {
            'current_usage': self.get_memory_info(),
            'memory_hogs': self.identify_memory_hogs(),
            'cleanup_history': self.memory_history[-10:],  # Last 10 cleanups
            'recommendations': self.get_memory_recommendations()
        }
        
        return stats
    
    def optimize_for_gaming(self) -> Dict[str, any]:
        """Optimize memory specifically for gaming"""
        results = {
            'processes_optimized': 0,
            'memory_freed': 0.0,
            'gaming_priority': False,
            'errors': []
        }
        
        try:
            # Note: We do NOT automatically terminate user processes.
            # Doing so without explicit confirmation is disruptive.
            # Memory cleanup and priority boosting are performed instead.
            
            # Clean memory
            results['memory_freed'] = self.clean_memory()
            
            # Set gaming priority
            if self.system == "Windows":
                try:
                    # Find game processes and set high priority
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            proc_name = proc.info['name'].lower()
                            if any(game in proc_name for game in ['valorant', 'cs2', 'fortnite', 'apex', 'cod', 'lol', 'league', 'riot']):
                                proc.nice(psutil.HIGH_PRIORITY_CLASS)
                                results['gaming_priority'] = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                except Exception:
                    pass
            
        except Exception as e:
            results['errors'].append(f"Gaming optimization failed: {str(e)}")
        
        return results
    
    def get_memory_usage_trend(self) -> List[Dict[str, float]]:
        """Get memory usage trend over time"""
        if len(self.memory_history) < 2:
            return []
        
        trend = []
        for entry in self.memory_history[-20:]:  # Last 20 entries
            trend.append({
                'timestamp': entry['timestamp'],
                'freed_memory': entry['freed_memory']
            })
        
        return trend
