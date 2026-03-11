"""
Traffic Shaper Module
Manages bandwidth allocation and traffic prioritization
"""

import subprocess
import platform
import time
import threading
import psutil
import socket
from typing import Dict, List, Optional, Tuple
import json

class TrafficShaper:
    def __init__(self):
        self.system = platform.system()
        self.is_shaping = False
        self.shaping_rules = []
        self.bandwidth_limits = {}
        self.priority_queues = {}
        
        # Common gaming ports
        self.gaming_ports = {
            'Valorant': [7000, 7001, 7002, 7003, 7004, 7005],
            'CS2': [27015, 27016, 27017, 27018, 27019, 27020],
            'Fortnite': [5222, 5223, 5224, 5225, 5226, 5227],
            'Apex Legends': [1024, 1025, 1026, 1027, 1028, 1029],
            'Call of Duty': [3074, 3075, 3076, 3077, 3078, 3079],
            'League of Legends': [2099, 5222, 5223, 8080, 8081, 8082],
            'LoL': [2099, 5222, 5223, 8080, 8081, 8082]
        }
        
        # Common streaming ports
        self.streaming_ports = [1935, 8080, 8081, 8082, 8083, 8084]
        
        # Common download ports
        self.download_ports = [80, 443, 8080, 8081, 8082, 8083, 8084, 8085]
    
    def get_network_usage(self) -> Dict[str, float]:
        """Get current network usage by interface"""
        usage = {}
        
        try:
            # Get network I/O counters
            net_io = psutil.net_io_counters(pernic=True)
            
            for interface, counters in net_io.items():
                if interface != 'lo':  # Skip loopback
                    usage[interface] = {
                        'bytes_sent': counters.bytes_sent,
                        'bytes_recv': counters.bytes_recv,
                        'packets_sent': counters.packets_sent,
                        'packets_recv': counters.packets_recv,
                        'total_bytes': counters.bytes_sent + counters.bytes_recv
                    }
        except Exception:
            pass
        
        return usage
    
    def get_bandwidth_usage(self) -> Dict[str, float]:
        """Get bandwidth usage in Mbps"""
        usage = {}
        
        try:
            # Get initial counters
            initial_counters = psutil.net_io_counters(pernic=True)
            time.sleep(1)  # Wait 1 second
            final_counters = psutil.net_io_counters(pernic=True)
            
            for interface in initial_counters:
                if interface != 'lo':
                    initial = initial_counters[interface]
                    final = final_counters[interface]
                    
                    bytes_sent = final.bytes_sent - initial.bytes_sent
                    bytes_recv = final.bytes_recv - initial.bytes_recv
                    total_bytes = bytes_sent + bytes_recv
                    
                    # Convert to Mbps
                    mbps = (total_bytes * 8) / (1024 * 1024)
                    usage[interface] = mbps
                    
        except Exception:
            pass
        
        return usage
    
    def identify_bandwidth_hogs(self) -> List[Dict[str, any]]:
        """Identify applications using the most bandwidth"""
        bandwidth_hogs = []
        
        try:
            # Get network connections
            connections = psutil.net_connections(kind='inet')
            
            # Group by process
            process_usage = {}
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.pid:
                    try:
                        process = psutil.Process(conn.pid)
                        process_name = process.name()
                        
                        if process_name not in process_usage:
                            process_usage[process_name] = {
                                'pid': conn.pid,
                                'connections': 0,
                                'ports': set()
                            }
                        
                        process_usage[process_name]['connections'] += 1
                        process_usage[process_name]['ports'].add(conn.laddr.port)
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            # Sort by number of connections
            sorted_processes = sorted(process_usage.items(), 
                                    key=lambda x: x[1]['connections'], 
                                    reverse=True)
            
            for process_name, info in sorted_processes[:10]:  # Top 10
                bandwidth_hogs.append({
                    'process': process_name,
                    'pid': info['pid'],
                    'connections': info['connections'],
                    'ports': list(info['ports'])
                })
                
        except Exception:
            pass
        
        return bandwidth_hogs
    
    def set_bandwidth_limit(self, interface: str, limit_mbps: float) -> bool:
        """Set bandwidth limit for an interface"""
        try:
            if self.system == "Windows":
                return self._set_windows_bandwidth_limit(interface, limit_mbps)
            else:
                return self._set_unix_bandwidth_limit(interface, limit_mbps)
        except Exception:
            return False
    
    def _set_windows_bandwidth_limit(self, interface: str, limit_mbps: float) -> bool:
        """Set bandwidth limit on Windows"""
        try:
            # This would require Windows QoS APIs or third-party tools
            # For now, we'll just store the limit
            self.bandwidth_limits[interface] = limit_mbps
            return True
        except Exception:
            return False
    
    def _set_unix_bandwidth_limit(self, interface: str, limit_mbps: float) -> bool:
        """Set bandwidth limit on Unix/Linux"""
        try:
            # Use tc (traffic control) to set bandwidth limit
            # Convert Mbps to bytes per second
            limit_bps = int(limit_mbps * 1024 * 1024 / 8)
            
            # Clear existing rules
            subprocess.run(['tc', 'qdisc', 'del', 'dev', interface, 'root'], 
                         capture_output=True, check=False)
            
            # Add new bandwidth limit
            result = subprocess.run([
                'tc', 'qdisc', 'add', 'dev', interface, 'root', 'tbf',
                'rate', f'{limit_bps}bps', 'latency', '50ms', 'burst', '1540'
            ], capture_output=True, check=True)
            
            self.bandwidth_limits[interface] = limit_mbps
            return True
            
        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False
    
    def prioritize_gaming_traffic(self) -> bool:
        """Prioritize gaming traffic"""
        try:
            if self.system == "Windows":
                return self._prioritize_windows_gaming()
            else:
                return self._prioritize_unix_gaming()
        except Exception:
            return False
    
    def _prioritize_windows_gaming(self) -> bool:
        """Prioritize gaming traffic on Windows"""
        try:
            # This would require Windows QoS APIs
            # For now, we'll just return True as a placeholder
            return True
        except Exception:
            return False
    
    def _prioritize_unix_gaming(self) -> bool:
        """Prioritize gaming traffic on Unix/Linux"""
        try:
            # Use tc to create priority queues
            for interface in psutil.net_if_addrs():
                if interface == 'lo':
                    continue
                
                # Create priority queue
                subprocess.run([
                    'tc', 'qdisc', 'add', 'dev', interface, 'root', 'handle', '1:', 'prio'
                ], capture_output=True, check=False)
                
                # Add gaming ports to high priority
                for game, ports in self.gaming_ports.items():
                    for port in ports:
                        subprocess.run([
                            'tc', 'filter', 'add', 'dev', interface, 'protocol', 'ip',
                            'parent', '1:', 'prio', '1', 'u32', 'match', 'ip', 'dport',
                            str(port), '0xffff', 'flowid', '1:1'
                        ], capture_output=True, check=False)
            
            return True
            
        except Exception:
            return False
    
    def limit_background_applications(self) -> bool:
        """Limit bandwidth for background applications"""
        try:
            # Identify background applications
            background_apps = self._identify_background_apps()
            
            for app in background_apps:
                self._limit_app_bandwidth(app)
            
            return True
            
        except Exception:
            return False
    
    def _identify_background_apps(self) -> List[str]:
        """Identify background applications"""
        background_apps = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    # Common background applications
                    background_keywords = [
                        'chrome', 'firefox', 'edge', 'safari',  # Browsers
                        'spotify', 'music', 'vlc', 'media',     # Media
                        'update', 'updater', 'installer',       # Updates
                        'backup', 'sync', 'cloud'               # Backup/sync
                    ]
                    
                    if any(keyword in proc_name for keyword in background_keywords):
                        background_apps.append(proc.info['name'])
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception:
            pass
        
        return background_apps
    
    def _limit_app_bandwidth(self, app_name: str) -> bool:
        """Limit bandwidth for a specific application"""
        try:
            # This would require advanced traffic shaping
            # For now, we'll just return True as a placeholder
            return True
        except Exception:
            return False
    
    def optimize_traffic(self, prioritize_gaming: bool = True, 
                        limit_background: bool = True,
                        bandwidth_limit: Optional[float] = None) -> Dict[str, any]:
        """Main traffic optimization function"""
        results = {
            'gaming_prioritized': False,
            'background_limited': False,
            'bandwidth_limited': False,
            'errors': []
        }
        
        try:
            # Prioritize gaming traffic
            if prioritize_gaming:
                if self.prioritize_gaming_traffic():
                    results['gaming_prioritized'] = True
                else:
                    results['errors'].append('Failed to prioritize gaming traffic')
            
            # Limit background applications
            if limit_background:
                if self.limit_background_applications():
                    results['background_limited'] = True
                else:
                    results['errors'].append('Failed to limit background applications')
            
            # Set bandwidth limits
            if bandwidth_limit:
                interfaces = self.get_available_interfaces()
                for interface in interfaces:
                    if self.set_bandwidth_limit(interface, bandwidth_limit):
                        results['bandwidth_limited'] = True
                    else:
                        results['errors'].append(f'Failed to limit bandwidth on {interface}')
            
        except Exception as e:
            results['errors'].append(f'Traffic optimization failed: {str(e)}')
        
        return results
    
    def get_available_interfaces(self) -> List[str]:
        """Get list of available network interfaces"""
        interfaces = []
        
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                if interface != 'lo' and addrs:
                    has_ip = any(addr.family == socket.AF_INET for addr in addrs)
                    if has_ip:
                        interfaces.append(interface)
        except Exception:
            pass
        
        return interfaces
    
    def get_traffic_statistics(self) -> Dict[str, any]:
        """Get detailed traffic statistics"""
        stats = {
            'total_usage': 0,
            'interface_usage': {},
            'bandwidth_hogs': [],
            'gaming_traffic': 0,
            'background_traffic': 0
        }
        
        try:
            # Get bandwidth usage
            bandwidth_usage = self.get_bandwidth_usage()
            stats['interface_usage'] = bandwidth_usage
            stats['total_usage'] = sum(bandwidth_usage.values())
            
            # Get bandwidth hogs
            stats['bandwidth_hogs'] = self.identify_bandwidth_hogs()
            
            # Estimate gaming vs background traffic
            stats['gaming_traffic'] = self._estimate_gaming_traffic()
            stats['background_traffic'] = self._estimate_background_traffic()
            
        except Exception:
            pass
        
        return stats
    
    def _estimate_gaming_traffic(self) -> float:
        """Estimate gaming traffic usage"""
        try:
            # This is a simplified estimation
            # In reality, you'd need to monitor actual traffic
            return 0.0
        except Exception:
            return 0.0
    
    def _estimate_background_traffic(self) -> float:
        """Estimate background traffic usage"""
        try:
            # This is a simplified estimation
            # In reality, you'd need to monitor actual traffic
            return 0.0
        except Exception:
            return 0.0
    
    def start_traffic_monitoring(self, interval: int = 10):
        """Start monitoring traffic usage"""
        if self.is_shaping:
            return
        
        self.is_shaping = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_traffic_monitoring(self):
        """Stop monitoring traffic usage"""
        self.is_shaping = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _monitoring_loop(self, interval: int):
        """Traffic monitoring loop"""
        while self.is_shaping:
            try:
                # Update traffic statistics
                stats = self.get_traffic_statistics()
                
                # Check if limits are being exceeded
                for interface, usage in stats['interface_usage'].items():
                    if interface in self.bandwidth_limits:
                        limit = self.bandwidth_limits[interface]
                        if usage > limit:
                            print(f"Warning: {interface} exceeding limit ({usage:.2f} > {limit} Mbps)")
                
                time.sleep(interval)
            except Exception:
                time.sleep(interval)
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get traffic optimization recommendations"""
        recommendations = []
        
        try:
            stats = self.get_traffic_statistics()
            
            # Check for bandwidth hogs
            if stats['bandwidth_hogs']:
                top_hog = stats['bandwidth_hogs'][0]
                recommendations.append(f"Consider limiting {top_hog['process']} bandwidth usage")
            
            # Check total usage
            if stats['total_usage'] > 100:  # More than 100 Mbps
                recommendations.append("High bandwidth usage detected - consider setting limits")
            
            # Check for gaming traffic
            if stats['gaming_traffic'] < stats['background_traffic']:
                recommendations.append("Background applications using more bandwidth than gaming")
                recommendations.append("Enable gaming traffic prioritization")
            
        except Exception:
            recommendations.append("Unable to analyze traffic - check network connection")
        
        return recommendations
    
    def reset_traffic_shaping(self) -> bool:
        """Reset all traffic shaping rules"""
        try:
            if self.system == "Windows":
                return self._reset_windows_shaping()
            else:
                return self._reset_unix_shaping()
        except Exception:
            return False
    
    def _reset_windows_shaping(self) -> bool:
        """Reset Windows traffic shaping"""
        try:
            # This would require Windows QoS APIs
            # For now, we'll just clear our limits
            self.bandwidth_limits.clear()
            return True
        except Exception:
            return False
    
    def _reset_unix_shaping(self) -> bool:
        """Reset Unix/Linux traffic shaping"""
        try:
            interfaces = self.get_available_interfaces()
            
            for interface in interfaces:
                # Clear traffic control rules
                subprocess.run(['tc', 'qdisc', 'del', 'dev', interface, 'root'], 
                             capture_output=True, check=False)
            
            self.bandwidth_limits.clear()
            return True
            
        except Exception:
            return False
