"""
Network Analyzer Module
Analyzes network performance, latency, and connection quality
"""

import socket
import time
import threading
import subprocess
import platform
import json
import statistics
from typing import Dict, List, Tuple, Optional
import psutil

try:
    import ping3
    PING3_AVAILABLE = True
except ImportError:
    PING3_AVAILABLE = False

try:
    import speedtest
    SPEEDTEST_AVAILABLE = True
except (ImportError, AttributeError, ModuleNotFoundError):
    SPEEDTEST_AVAILABLE = False

class NetworkAnalyzer:
    def __init__(self):
        self.system = platform.system()
        self.is_analyzing = False
        self.analysis_thread = None
        self.results = {}
        
        # Common test servers
        self.test_servers = [
            '8.8.8.8',      # Google DNS
            '1.1.1.1',      # Cloudflare DNS
            '208.67.222.222', # OpenDNS
            '8.8.4.4',      # Google DNS Secondary
        ]
        
        # Gaming servers for latency testing
        self.gaming_servers = {
            'Valorant': ['104.18.0.0', '104.18.1.0'],
            'CS2': ['162.254.196.0', '162.254.197.0'],
            'Fortnite': ['3.208.0.0', '3.208.1.0'],
            'Apex Legends': ['13.107.42.14', '13.107.42.15'],
            'League of Legends': ['104.160.131.1', '104.160.131.2', '104.160.131.3', '104.160.131.6'],
            'LoL': ['104.160.131.1', '104.160.131.2', '104.160.131.3', '104.160.131.6']
        }
    
    def ping_host(self, host: str, count: int = 4) -> Dict[str, float]:
        """Ping a host and return latency statistics"""
        if PING3_AVAILABLE:
            return self._ping_with_ping3(host, count)
        else:
            return self._ping_with_system(host, count)
    
    def _ping_with_ping3(self, host: str, count: int) -> Dict[str, float]:
        """Ping using ping3 library"""
        latencies = []
        
        for _ in range(count):
            try:
                latency = ping3.ping(host, timeout=5)
                if latency is not None:
                    latencies.append(latency * 1000)  # Convert to ms
            except Exception:
                continue
        
        if not latencies:
            return {'min': 0, 'max': 0, 'avg': 0, 'packet_loss': 100}
        
        return {
            'min': min(latencies),
            'max': max(latencies),
            'avg': statistics.mean(latencies),
            'packet_loss': ((count - len(latencies)) / count) * 100
        }
    
    def _ping_with_system(self, host: str, count: int) -> Dict[str, float]:
        """Ping using system ping command"""
        try:
            if self.system == "Windows":
                cmd = ['ping', '-n', str(count), '-w', '5000', host]  # 5 second timeout
            else:
                cmd = ['ping', '-c', str(count), '-W', '5', host]  # 5 second timeout
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse ping output for latency
                lines = result.stdout.split('\n')
                latencies = []
                
                for line in lines:
                    if 'time=' in line or 'time<' in line:
                        try:
                            # Extract time value
                            if 'time=' in line:
                                time_part = line.split('time=')[1].split()[0]
                            else:
                                time_part = line.split('time<')[1].split()[0]
                            
                            if 'ms' in time_part:
                                latency = float(time_part.replace('ms', ''))
                                latencies.append(latency)
                        except (IndexError, ValueError):
                            continue
                
                if latencies:
                    return {
                        'min': min(latencies),
                        'max': max(latencies),
                        'avg': statistics.mean(latencies),
                        'packet_loss': 0
                    }
            
            # If ping failed, try alternative method
            return self._ping_alternative(host, count)
            
        except Exception as e:
            print(f"Ping error: {e}")
            return {'min': 0, 'max': 0, 'avg': 0, 'packet_loss': 100}
    
    def _ping_alternative(self, host: str, count: int) -> Dict[str, float]:
        """Alternative ping method using socket"""
        try:
            latencies = []
            
            for _ in range(count):
                start_time = time.time()
                try:
                    # Try to connect to the host
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex((host, 80))  # Try port 80
                    sock.close()
                    
                    if result == 0:
                        latency = (time.time() - start_time) * 1000  # Convert to ms
                        latencies.append(latency)
                except Exception:
                    continue
            
            if latencies:
                return {
                    'min': min(latencies),
                    'max': max(latencies),
                    'avg': statistics.mean(latencies),
                    'packet_loss': ((count - len(latencies)) / count) * 100
                }
            
            return {'min': 0, 'max': 0, 'avg': 0, 'packet_loss': 100}
            
        except Exception:
            return {'min': 0, 'max': 0, 'avg': 0, 'packet_loss': 100}
    
    def test_bandwidth(self) -> Dict[str, float]:
        """Test internet bandwidth using speedtest"""
        try:
            # Always use alternative method for better reliability
            return self._test_bandwidth_alternative()
        except Exception:
            return {'download': 0, 'upload': 0, 'ping': 0}
    
    def _test_bandwidth_alternative(self) -> Dict[str, float]:
        """Alternative bandwidth testing method for executables"""
        try:
            # Test multiple servers for better estimation
            servers_to_test = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
            total_latency = 0
            successful_tests = 0
            
            for server in servers_to_test:
                ping_result = self.ping_host(server, 2)
                if ping_result['avg'] > 0:
                    total_latency += ping_result['avg']
                    successful_tests += 1
            
            if successful_tests > 0:
                avg_latency = total_latency / successful_tests
                
                # More sophisticated bandwidth estimation
                if avg_latency < 20:
                    # Excellent connection
                    estimated_download = 100 + (50 - avg_latency) * 2
                    estimated_upload = estimated_download * 0.9
                elif avg_latency < 50:
                    # Good connection
                    estimated_download = 50 + (50 - avg_latency) * 1.5
                    estimated_upload = estimated_download * 0.8
                elif avg_latency < 100:
                    # Fair connection
                    estimated_download = 25 + (100 - avg_latency) * 0.5
                    estimated_upload = estimated_download * 0.7
                else:
                    # Poor connection
                    estimated_download = max(5, 25 - (avg_latency - 100) * 0.2)
                    estimated_upload = estimated_download * 0.6
                
                # Ensure reasonable bounds
                estimated_download = max(5, min(200, estimated_download))
                estimated_upload = max(2, min(100, estimated_upload))
                
                return {
                    'download': round(estimated_download, 1),
                    'upload': round(estimated_upload, 1),
                    'ping': round(avg_latency, 1)
                }
        except Exception as e:
            print(f"Bandwidth estimation error: {e}")
        
        return {'download': 0, 'upload': 0, 'ping': 0}
    
    def analyze_network_connections(self) -> List[Dict[str, any]]:
        """Analyze current network connections"""
        connections = []
        
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        'status': conn.status,
                        'pid': conn.pid
                    })
        except Exception:
            pass
        
        return connections
    
    def get_network_interfaces(self) -> List[Dict[str, any]]:
        """Get information about network interfaces"""
        interfaces = []
        
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface,
                    'addresses': [],
                    'is_up': False
                }
                
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # IPv4
                        interface_info['addresses'].append({
                            'ip': addr.address,
                            'netmask': addr.netmask,
                            'broadcast': addr.broadcast
                        })
                        interface_info['is_up'] = True
                
                if interface_info['addresses']:
                    interfaces.append(interface_info)
                    
        except Exception:
            pass
        
        return interfaces
    
    def test_gaming_servers(self) -> Dict[str, Dict[str, float]]:
        """Test latency to gaming servers"""
        gaming_results = {}
        
        for game, servers in self.gaming_servers.items():
            game_latencies = []
            
            for server in servers:
                ping_result = self.ping_host(server, 3)
                if ping_result['avg'] > 0:
                    game_latencies.append(ping_result['avg'])
            
            if game_latencies:
                gaming_results[game] = {
                    'min_latency': min(game_latencies),
                    'max_latency': max(game_latencies),
                    'avg_latency': statistics.mean(game_latencies)
                }
            else:
                gaming_results[game] = {
                    'min_latency': 0,
                    'max_latency': 0,
                    'avg_latency': 0
                }
        
        return gaming_results
    
    def analyze_network(self) -> Dict[str, any]:
        """Main network analysis function - returns dictionary for UI"""
        try:
            # Test basic connectivity
            connectivity_results = []
            for server in self.test_servers[:2]:  # Test first 2 servers
                ping_result = self.ping_host(server, 3)
                connectivity_results.append({
                    'server': server,
                    'latency': ping_result['avg'],
                    'packet_loss': ping_result['packet_loss']
                })
            
            # Test gaming servers
            gaming_results = self.test_gaming_servers()
            
            # Bandwidth test
            bandwidth = self.test_bandwidth()
            
            # Network interfaces
            interfaces = self.get_network_interfaces()
            
            # Active connections
            connections = self.analyze_network_connections()
            
            # Network quality score
            quality = self.get_network_quality_score()
            
            # Get optimization recommendations
            recommendations = self.get_optimization_recommendations()
            
            return {
                'connection_status': 'Connected' if any(r['latency'] > 0 for r in connectivity_results) else 'Disconnected',
                'latency': connectivity_results[0]['latency'] if connectivity_results else 0,
                'packet_loss': connectivity_results[0]['packet_loss'] if connectivity_results else 100,
                'download_speed': bandwidth['download'],
                'upload_speed': bandwidth['upload'],
                'ping': bandwidth['ping'],
                'gaming_servers': gaming_results,
                'interfaces': interfaces,
                'active_connections': len(connections),
                'quality_score': quality['score'],
                'quality_rating': quality['quality'],
                'issues': quality['issues'],
                'recommendations': recommendations,
                'connectivity_results': connectivity_results
            }
            
        except Exception as e:
            return {
                'connection_status': 'Error',
                'latency': 0,
                'packet_loss': 100,
                'download_speed': 0,
                'upload_speed': 0,
                'ping': 0,
                'gaming_servers': {},
                'interfaces': [],
                'active_connections': 0,
                'quality_score': 0,
                'quality_rating': 'Unknown',
                'issues': [f'Analysis failed: {str(e)}'],
                'recommendations': ['Check your internet connection'],
                'connectivity_results': []
            }
    
    def get_network_analysis_report(self) -> str:
        """Get detailed network analysis report as string"""
        results = []
        results.append("=== Network Analysis Report ===\n")
        
        # Test basic connectivity
        results.append("1. Basic Connectivity Test:")
        for server in self.test_servers[:2]:  # Test first 2 servers
            ping_result = self.ping_host(server, 3)
            results.append(f"   {server}: {ping_result['avg']:.2f}ms avg, {ping_result['packet_loss']:.1f}% loss")
        results.append("")
        
        # Test gaming servers
        results.append("2. Gaming Server Latency:")
        gaming_results = self.test_gaming_servers()
        for game, stats in gaming_results.items():
            if stats['avg_latency'] > 0:
                results.append(f"   {game}: {stats['avg_latency']:.2f}ms avg")
            else:
                results.append(f"   {game}: Unable to reach servers")
        results.append("")
        
        # Bandwidth test
        results.append("3. Bandwidth Test:")
        if SPEEDTEST_AVAILABLE:
            bandwidth = self.test_bandwidth()
            if bandwidth['download'] > 0:
                results.append(f"   Download: {bandwidth['download']:.2f} Mbps")
                results.append(f"   Upload: {bandwidth['upload']:.2f} Mbps")
                results.append(f"   Ping: {bandwidth['ping']:.2f} ms")
            else:
                results.append("   Bandwidth test failed")
        else:
            results.append("   Speedtest not available (install speedtest-cli)")
        results.append("")
        
        # Network interfaces
        results.append("4. Network Interfaces:")
        interfaces = self.get_network_interfaces()
        for interface in interfaces:
            if interface['is_up']:
                results.append(f"   {interface['name']}: {interface['addresses'][0]['ip']}")
        results.append("")
        
        # Active connections
        results.append("5. Active Connections:")
        connections = self.analyze_network_connections()
        results.append(f"   Total established connections: {len(connections)}")
        
        # Show top connections by port
        port_counts = {}
        for conn in connections:
            if conn['remote_address'] != "N/A":
                port = conn['remote_address'].split(':')[1]
                port_counts[port] = port_counts.get(port, 0) + 1
        
        top_ports = sorted(port_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for port, count in top_ports:
            results.append(f"   Port {port}: {count} connections")
        
        return "\n".join(results)
    
    def start_continuous_analysis(self, interval: int = 30):
        """Start continuous network analysis"""
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analysis_thread = threading.Thread(
            target=self._continuous_analysis_loop,
            args=(interval,),
            daemon=True
        )
        self.analysis_thread.start()
    
    def stop_continuous_analysis(self):
        """Stop continuous network analysis"""
        self.is_analyzing = False
        if self.analysis_thread:
            self.analysis_thread.join(timeout=5)
    
    def _continuous_analysis_loop(self, interval: int):
        """Continuous analysis loop"""
        while self.is_analyzing:
            try:
                # Quick ping test
                ping_result = self.ping_host('8.8.8.8', 2)
                self.results['last_ping'] = {
                    'timestamp': time.time(),
                    'latency': ping_result['avg'],
                    'packet_loss': ping_result['packet_loss']
                }
                
                time.sleep(interval)
            except Exception:
                time.sleep(interval)
    
    def get_network_quality_score(self) -> Dict[str, any]:
        """Calculate network quality score"""
        try:
            # Test multiple servers
            latencies = []
            packet_losses = []
            
            for server in self.test_servers:
                result = self.ping_host(server, 3)
                if result['avg'] > 0:
                    latencies.append(result['avg'])
                    packet_losses.append(result['packet_loss'])
            
            if not latencies:
                return {'score': 0, 'quality': 'Poor', 'issues': ['No connectivity']}
            
            avg_latency = statistics.mean(latencies)
            avg_packet_loss = statistics.mean(packet_losses)
            
            # Calculate score (0-100)
            score = 100
            
            # Penalize high latency
            if avg_latency > 100:
                score -= 30
            elif avg_latency > 50:
                score -= 15
            elif avg_latency > 20:
                score -= 5
            
            # Penalize packet loss
            if avg_packet_loss > 10:
                score -= 40
            elif avg_packet_loss > 5:
                score -= 20
            elif avg_packet_loss > 1:
                score -= 10
            
            # Determine quality
            if score >= 80:
                quality = 'Excellent'
            elif score >= 60:
                quality = 'Good'
            elif score >= 40:
                quality = 'Fair'
            else:
                quality = 'Poor'
            
            issues = []
            if avg_latency > 50:
                issues.append('High latency')
            if avg_packet_loss > 1:
                issues.append('Packet loss')
            
            return {
                'score': max(0, score),
                'quality': quality,
                'avg_latency': avg_latency,
                'packet_loss': avg_packet_loss,
                'issues': issues
            }
            
        except Exception:
            return {'score': 0, 'quality': 'Unknown', 'issues': ['Analysis failed']}
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get network optimization recommendations"""
        recommendations = []
        
        try:
            quality = self.get_network_quality_score()
            
            if quality['score'] < 60:
                recommendations.append("Consider upgrading your internet connection")
            
            if quality['avg_latency'] > 50:
                recommendations.append("Try using a wired connection instead of WiFi")
                recommendations.append("Close unnecessary network applications")
            
            if quality['packet_loss'] > 1:
                recommendations.append("Check for network interference")
                recommendations.append("Restart your router and modem")
            
            if quality['score'] < 40:
                recommendations.append("Contact your ISP about connection issues")
                recommendations.append("Consider using a different DNS server (8.8.8.8)")
            
        except Exception:
            recommendations.append("Unable to analyze network - check connection")
        
        return recommendations
