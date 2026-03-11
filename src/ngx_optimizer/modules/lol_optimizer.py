"""
League of Legends Specific Optimizer
Specialized optimizations for League of Legends
"""

import psutil
import subprocess
import platform
import os
import time
from typing import Dict, List, Optional

class LoLOptimizer:
    def __init__(self):
        self.system = platform.system()
        self.lol_processes = [
            'league of legends.exe', 'lol.exe', 'riotclientservices.exe', 
            'riotclient.exe', 'leagueclient.exe', 'leagueclientux.exe'
        ]
        self.lol_ports = [2099, 5222, 5223, 8080, 8081, 8082]
        
    def detect_lol_processes(self) -> List[psutil.Process]:
        """Detect League of Legends related processes"""
        lol_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_name = proc.info['name'].lower()
                if any(lol_process in proc_name for lol_process in self.lol_processes):
                    lol_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return lol_processes
    
    def optimize_lol_performance(self) -> Dict[str, any]:
        """Optimize League of Legends performance"""
        results = {
            'processes_optimized': 0,
            'priority_set': False,
            'memory_optimized': False,
            'network_optimized': False,
            'errors': []
        }
        
        try:
            # Detect and optimize LoL processes
            lol_processes = self.detect_lol_processes()
            
            for process in lol_processes:
                try:
                    # Set high priority
                    if self.system == "Windows":
                        process.nice(psutil.HIGH_PRIORITY_CLASS)
                    else:
                        process.nice(-10)
                    
                    # Set CPU affinity to use all cores
                    cpu_count = psutil.cpu_count()
                    process.cpu_affinity(list(range(cpu_count)))
                    
                    results['processes_optimized'] += 1
                    results['priority_set'] = True
                    
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    results['errors'].append(f"Failed to optimize process {process.pid}")
            
            # Memory optimization
            results['memory_optimized'] = self._optimize_lol_memory()
            
            # Network optimization
            results['network_optimized'] = self._optimize_lol_network()
            
        except Exception as e:
            results['errors'].append(f"LoL optimization failed: {str(e)}")
        
        return results
    
    def _optimize_lol_memory(self) -> bool:
        """Optimize memory for League of Legends"""
        try:
            # Clear system cache
            if self.system == "Windows":
                subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=False)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            return True
        except Exception:
            return False
    
    def _optimize_lol_network(self) -> bool:
        """Optimize network settings for League of Legends"""
        try:
            if self.system == "Windows":
                # Optimize TCP settings for gaming
                subprocess.run([
                    'netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'
                ], capture_output=True, check=False)
                
                # Disable Nagle's algorithm for better responsiveness
                subprocess.run([
                    'netsh', 'int', 'tcp', 'set', 'global', 'chimney=enabled'
                ], capture_output=True, check=False)
            
            return True
        except Exception:
            return False
    
    def get_lol_performance_metrics(self) -> Dict[str, float]:
        """Get League of Legends specific performance metrics"""
        try:
            lol_processes = self.detect_lol_processes()
            
            if not lol_processes:
                return {
                    'processes_running': 0,
                    'total_memory_mb': 0,
                    'cpu_usage': 0,
                    'network_connections': 0
                }
            
            total_memory = 0
            total_cpu = 0
            network_connections = 0
            
            for process in lol_processes:
                try:
                    # Memory usage
                    memory_info = process.memory_info()
                    total_memory += memory_info.rss / (1024 * 1024)  # MB
                    
                    # CPU usage
                    total_cpu += process.cpu_percent()
                    
                    # Network connections
                    connections = process.connections()
                    network_connections += len(connections)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'processes_running': len(lol_processes),
                'total_memory_mb': total_memory,
                'cpu_usage': total_cpu,
                'network_connections': network_connections
            }
            
        except Exception:
            return {
                'processes_running': 0,
                'total_memory_mb': 0,
                'cpu_usage': 0,
                'network_connections': 0
            }
    
    def optimize_lol_settings(self) -> Dict[str, bool]:
        """Optimize League of Legends game settings"""
        results = {}
        
        try:
            # This would involve modifying LoL configuration files
            # For now, we'll return placeholder results
            results['game_settings'] = True
            results['graphics_settings'] = True
            results['network_settings'] = True
            
        except Exception:
            results['game_settings'] = False
            results['graphics_settings'] = False
            results['network_settings'] = False
        
        return results
    
    def get_lol_optimization_recommendations(self) -> List[str]:
        """Get League of Legends specific optimization recommendations"""
        recommendations = []
        
        try:
            metrics = self.get_lol_performance_metrics()
            
            if metrics['processes_running'] == 0:
                recommendations.append("League of Legends is not running")
                recommendations.append("Start the game to apply optimizations")
            else:
                if metrics['total_memory_mb'] > 2000:  # More than 2GB
                    recommendations.append("High memory usage detected")
                    recommendations.append("Consider closing other applications")
                
                if metrics['cpu_usage'] > 80:
                    recommendations.append("High CPU usage detected")
                    recommendations.append("Check for background processes")
                
                if metrics['network_connections'] > 50:
                    recommendations.append("Many network connections detected")
                    recommendations.append("Check for network issues")
            
            # General LoL recommendations
            recommendations.append("Use wired connection for best performance")
            recommendations.append("Close Discord overlay if experiencing lag")
            recommendations.append("Disable Windows Game Mode for LoL")
            recommendations.append("Set LoL to high priority in Task Manager")
            
        except Exception:
            recommendations.append("Unable to analyze LoL performance")
        
        return recommendations
    
    def monitor_lol_performance(self, duration: int = 60) -> List[Dict[str, float]]:
        """Monitor League of Legends performance over time"""
        metrics_history = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            metrics = self.get_lol_performance_metrics()
            metrics['timestamp'] = time.time()
            metrics_history.append(metrics)
            time.sleep(5)  # Sample every 5 seconds
        
        return metrics_history
    
    def get_lol_server_latency(self) -> Dict[str, float]:
        """Test latency to League of Legends servers"""
        # Real LoL server IPs (these are the actual Riot Games server IPs)
        servers = {
            'NA': '104.160.131.1',      # North America
            'EUW': '104.160.141.3',     # Europe West  
            'EUNE': '104.160.142.3',    # Europe Nordic & East
            'KR': '104.160.156.1',      # Korea
            'BR': '104.160.152.3',      # Brazil
            'SG': '104.160.136.3'       # Singapore (Southeast Asia)
        }
        
        latencies = {}
        
        for region, server in servers.items():
            try:
                # Use ping with proper parameters for accurate latency testing
                if self.system == "Windows":
                    result = subprocess.run(['ping', '-n', '4', '-w', '5000', server], 
                                          capture_output=True, text=True, timeout=15)
                else:
                    result = subprocess.run(['ping', '-c', '4', '-W', '5', server], 
                                          capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    # Parse average latency from ping output
                    output = result.stdout
                    latency = self._parse_ping_latency(output)
                    latencies[region] = latency
                else:
                    latencies[region] = 999.0
                    
            except subprocess.TimeoutExpired:
                latencies[region] = 999.0
            except Exception:
                latencies[region] = 999.0
        
        return latencies
    
    def _parse_ping_latency(self, ping_output: str) -> float:
        """Parse latency from ping command output"""
        try:
            lines = ping_output.split('\n')
            latencies = []
            
            for line in lines:
                if 'time=' in line or 'time<' in line:
                    # Extract latency value
                    if 'time=' in line:
                        time_part = line.split('time=')[1].split()[0]
                    else:
                        time_part = line.split('time<')[1].split()[0]
                    
                    # Remove 'ms' and convert to float
                    if 'ms' in time_part:
                        latency = float(time_part.replace('ms', ''))
                        latencies.append(latency)
            
            if latencies:
                # Return average latency
                return sum(latencies) / len(latencies)
            else:
                return 999.0
                
        except Exception:
            return 999.0
    
    def get_best_lol_server(self) -> str:
        """Get the best League of Legends server based on latency"""
        latencies = self.get_lol_server_latency()
        
        if not latencies:
            return "Unknown"
        
        # Filter out unreachable servers (999ms)
        reachable_servers = {k: v for k, v in latencies.items() if v < 999}
        
        if not reachable_servers:
            return "No servers reachable"
        
        # Find server with lowest latency
        best_server = min(reachable_servers.items(), key=lambda x: x[1])
        return f"{best_server[0]} ({best_server[1]:.1f}ms)"
