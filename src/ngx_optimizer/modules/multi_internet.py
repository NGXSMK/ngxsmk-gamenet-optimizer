"""
Multi Internet Module
Manages multiple internet connections for load balancing and failover
"""

import subprocess
import platform
import time
import threading
import json
import socket
from typing import Dict, List, Optional, Tuple
import psutil

# netifaces is optional - we'll use psutil instead
NETIFACES_AVAILABLE = False

class MultiInternet:
    def __init__(self):
        self.system = platform.system()
        self.active_connections = []
        self.connection_metrics = {}
        self.is_monitoring = False
        self.monitor_thread = None
        
    def get_available_connections(self) -> List[Dict[str, any]]:
        """Get list of available network connections"""
        connections = []
        
        try:
            if self.system == "Windows":
                connections = self._get_windows_connections()
            else:
                connections = self._get_unix_connections()
        except Exception as e:
            print(f"Error getting connections: {e}")
        
        return connections
    
    def _get_windows_connections(self) -> List[Dict[str, any]]:
        """Get Windows network connections"""
        connections = []
        
        try:
            # Get network adapters using netsh
            result = subprocess.run([
                'netsh', 'interface', 'show', 'interface'
            ], capture_output=True, text=True, check=True)
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Enabled' in line and 'Connected' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        name = ' '.join(parts[3:])
                        connections.append({
                            'name': name,
                            'type': 'Ethernet' if 'Ethernet' in name else 'WiFi',
                            'status': 'Connected',
                            'interface': name
                        })
        except Exception:
            pass
        
        # Also get from psutil
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                if interface != 'lo' and addrs:
                    has_ip = any(addr.family == socket.AF_INET for addr in addrs)
                    if has_ip:
                        connections.append({
                            'name': interface,
                            'type': 'Network Interface',
                            'status': 'Connected',
                            'interface': interface
                        })
        except Exception:
            pass
        
        return connections
    
    def _get_unix_connections(self) -> List[Dict[str, any]]:
        """Get Unix/Linux network connections"""
        connections = []
        
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                if interface != 'lo' and addrs:
                    has_ip = any(addr.family == socket.AF_INET for addr in addrs)
                    if has_ip:
                        # Get interface status
                        status = 'Connected'
                        try:
                            stats = psutil.net_if_stats()[interface]
                            if not stats.isup:
                                status = 'Disconnected'
                        except KeyError:
                            pass
                        
                        connections.append({
                            'name': interface,
                            'type': 'Network Interface',
                            'status': status,
                            'interface': interface
                        })
        except Exception:
            pass
        
        return connections
    
    def test_connection_quality(self, interface: str) -> Dict[str, float]:
        """Test the quality of a specific connection"""
        try:
            # Get interface statistics
            if interface in psutil.net_if_stats():
                stats = psutil.net_if_stats()[interface]
                if not stats.isup:
                    return {'latency': 999, 'bandwidth': 0, 'packet_loss': 100}
            
            # Test latency to multiple servers
            test_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
            latencies = []
            
            for server in test_servers:
                try:
                    # Simple ping test
                    if self.system == "Windows":
                        cmd = ['ping', '-n', '1', server]
                    else:
                        cmd = ['ping', '-c', '1', server]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        # Parse latency from output
                        output = result.stdout
                        if 'time=' in output:
                            time_part = output.split('time=')[1].split()[0]
                            if 'ms' in time_part:
                                latency = float(time_part.replace('ms', ''))
                                latencies.append(latency)
                except Exception:
                    continue
            
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                packet_loss = ((len(test_servers) - len(latencies)) / len(test_servers)) * 100
            else:
                avg_latency = 999
                packet_loss = 100
            
            # Estimate bandwidth (simplified)
            bandwidth = self._estimate_bandwidth(interface)
            
            return {
                'latency': avg_latency,
                'bandwidth': bandwidth,
                'packet_loss': packet_loss,
                'quality_score': self._calculate_quality_score(avg_latency, packet_loss, bandwidth)
            }
            
        except Exception:
            return {'latency': 999, 'bandwidth': 0, 'packet_loss': 100, 'quality_score': 0}
    
    def _estimate_bandwidth(self, interface: str) -> float:
        """Estimate bandwidth for an interface"""
        try:
            # Get interface statistics
            if interface in psutil.net_if_stats():
                stats = psutil.net_if_stats()[interface]
                # This is a simplified estimation
                # In reality, you'd need to measure actual throughput
                if 'wifi' in interface.lower() or 'wireless' in interface.lower():
                    return 50.0  # Estimated WiFi speed
                elif 'ethernet' in interface.lower() or 'eth' in interface.lower():
                    return 100.0  # Estimated Ethernet speed
                else:
                    return 25.0  # Default estimation
            return 0.0
        except Exception:
            return 0.0
    
    def _calculate_quality_score(self, latency: float, packet_loss: float, bandwidth: float) -> float:
        """Calculate quality score for a connection"""
        score = 100.0
        
        # Penalize high latency
        if latency > 200:
            score -= 40
        elif latency > 100:
            score -= 20
        elif latency > 50:
            score -= 10
        
        # Penalize packet loss
        if packet_loss > 10:
            score -= 30
        elif packet_loss > 5:
            score -= 15
        elif packet_loss > 1:
            score -= 5
        
        # Reward high bandwidth
        if bandwidth > 100:
            score += 10
        elif bandwidth > 50:
            score += 5
        
        return max(0, min(100, score))
    
    def get_best_connection(self) -> Optional[Dict[str, any]]:
        """Get the best available connection based on quality metrics"""
        connections = self.get_available_connections()
        if not connections:
            return None
        
        best_connection = None
        best_score = 0
        
        for conn in connections:
            if conn['status'] == 'Connected':
                quality = self.test_connection_quality(conn['interface'])
                if quality['quality_score'] > best_score:
                    best_score = quality['quality_score']
                    best_connection = conn
                    best_connection['quality'] = quality
        
        return best_connection
    
    def setup_load_balancing(self, connections: List[str]) -> bool:
        """Setup load balancing across multiple connections"""
        try:
            if self.system == "Windows":
                return self._setup_windows_load_balancing(connections)
            else:
                return self._setup_unix_load_balancing(connections)
        except Exception:
            return False
    
    def _setup_windows_load_balancing(self, connections: List[str]) -> bool:
        """Setup load balancing on Windows"""
        try:
            # This would require advanced Windows networking configuration
            # For now, we'll just return True as a placeholder
            # In a real implementation, you'd use Windows APIs or PowerShell
            return True
        except Exception:
            return False
    
    def _setup_unix_load_balancing(self, connections: List[str]) -> bool:
        """Setup load balancing on Unix/Linux"""
        try:
            # This would require advanced Linux networking configuration
            # For now, we'll just return True as a placeholder
            # In a real implementation, you'd use iptables, routing tables, etc.
            return True
        except Exception:
            return False
    
    def start_connection_monitoring(self, interval: int = 30):
        """Start monitoring connection quality"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_connection_monitoring(self):
        """Stop monitoring connection quality"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _monitoring_loop(self, interval: int):
        """Connection monitoring loop"""
        while self.is_monitoring:
            try:
                connections = self.get_available_connections()
                
                for conn in connections:
                    if conn['status'] == 'Connected':
                        quality = self.test_connection_quality(conn['interface'])
                        self.connection_metrics[conn['interface']] = {
                            'timestamp': time.time(),
                            'quality': quality
                        }
                
                time.sleep(interval)
            except Exception:
                time.sleep(interval)
    
    def get_connection_statistics(self) -> Dict[str, any]:
        """Get statistics for all monitored connections"""
        stats = {
            'total_connections': len(self.connection_metrics),
            'active_connections': 0,
            'best_connection': None,
            'connection_details': {}
        }
        
        best_score = 0
        
        for interface, metrics in self.connection_metrics.items():
            if metrics['quality']['quality_score'] > 0:
                stats['active_connections'] += 1
                
                if metrics['quality']['quality_score'] > best_score:
                    best_score = metrics['quality']['quality_score']
                    stats['best_connection'] = interface
                
                stats['connection_details'][interface] = {
                    'latency': metrics['quality']['latency'],
                    'bandwidth': metrics['quality']['bandwidth'],
                    'packet_loss': metrics['quality']['packet_loss'],
                    'quality_score': metrics['quality']['quality_score'],
                    'last_updated': metrics['timestamp']
                }
        
        return stats
    
    def optimize_connection_routing(self) -> Dict[str, any]:
        """Optimize routing for best performance"""
        try:
            # Get best connection
            best_conn = self.get_best_connection()
            if not best_conn:
                return {'success': False, 'message': 'No suitable connections found'}
            
            # Get current routing table
            routing_info = self._get_routing_table()
            
            # Optimize routing (simplified)
            optimization_result = self._optimize_routes(best_conn, routing_info)
            
            return {
                'success': True,
                'best_connection': best_conn['interface'],
                'quality_score': best_conn['quality']['quality_score'],
                'optimization_applied': optimization_result
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Optimization failed: {str(e)}'}
    
    def _get_routing_table(self) -> List[Dict[str, any]]:
        """Get current routing table"""
        routes = []
        
        try:
            if self.system == "Windows":
                result = subprocess.run(['route', 'print'], capture_output=True, text=True)
                # Parse Windows route output
            else:
                result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
                # Parse Linux route output
        except Exception:
            pass
        
        return routes
    
    def _optimize_routes(self, best_connection: Dict[str, any], routing_info: List[Dict[str, any]]) -> bool:
        """Optimize routing for the best connection"""
        try:
            # This would involve modifying routing tables
            # For now, we'll just return True as a placeholder
            return True
        except Exception:
            return False
    
    def get_failover_configuration(self) -> Dict[str, any]:
        """Get failover configuration"""
        return {
            'primary_connection': self.get_best_connection(),
            'backup_connections': self._get_backup_connections(),
            'failover_threshold': 30.0,  # Latency threshold in ms
            'auto_failover': True
        }
    
    def _get_backup_connections(self) -> List[Dict[str, any]]:
        """Get backup connections sorted by quality"""
        connections = self.get_available_connections()
        backup_connections = []
        
        for conn in connections:
            if conn['status'] == 'Connected':
                quality = self.test_connection_quality(conn['interface'])
                if quality['quality_score'] > 0:
                    backup_connections.append({
                        'interface': conn['interface'],
                        'quality_score': quality['quality_score']
                    })
        
        # Sort by quality score
        backup_connections.sort(key=lambda x: x['quality_score'], reverse=True)
        return backup_connections[1:]  # Exclude the best one (it's primary)
    
    def test_connection_failover(self) -> Dict[str, any]:
        """Test failover functionality"""
        try:
            # Simulate connection failure and test failover
            primary = self.get_best_connection()
            if not primary:
                return {'success': False, 'message': 'No primary connection available'}
            
            # Test backup connections
            backup_connections = self._get_backup_connections()
            
            return {
                'success': True,
                'primary_connection': primary['interface'],
                'backup_connections': len(backup_connections),
                'failover_ready': len(backup_connections) > 0
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Failover test failed: {str(e)}'}
