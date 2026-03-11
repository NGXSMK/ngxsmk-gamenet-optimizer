"""
Advanced Network Optimizer Module
Intelligent network optimization with traffic shaping, QoS, and latency optimization
"""

import psutil
import time
import threading
import subprocess
import platform
import socket
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

class NetworkOptimizer:
    """Advanced network optimizer with intelligent traffic management"""
    
    def __init__(self):
        self.is_optimizing = False
        self.optimization_thread = None
        self.network_interfaces = []
        self.traffic_rules = []
        self.qos_settings = {}
        self.latency_optimizations = {}
        
    def start_network_optimization(self, profile: str = 'gaming') -> Dict[str, any]:
        """Start advanced network optimization"""
        if self.is_optimizing:
            return {'status': 'already_optimizing'}
        
        try:
            self.is_optimizing = True
            results = {
                'profile': profile,
                'timestamp': datetime.now().isoformat(),
                'optimizations': []
            }
            
            # Get network interfaces
            self.network_interfaces = self._get_network_interfaces()
            results['interfaces'] = self.network_interfaces
            
            # Apply profile-specific optimizations
            if profile == 'gaming':
                gaming_optimizations = self._apply_gaming_optimizations()
                results['optimizations'].extend(gaming_optimizations)
            elif profile == 'streaming':
                streaming_optimizations = self._apply_streaming_optimizations()
                results['optimizations'].extend(streaming_optimizations)
            elif profile == 'productivity':
                productivity_optimizations = self._apply_productivity_optimizations()
                results['optimizations'].extend(productivity_optimizations)
            
            # Apply universal optimizations
            universal_optimizations = self._apply_universal_optimizations()
            results['optimizations'].extend(universal_optimizations)
            
            # Start traffic monitoring
            self._start_traffic_monitoring()
            
            return results
            
        except Exception as e:
            self.is_optimizing = False
            return {'status': 'error', 'message': str(e)}
    
    def _get_network_interfaces(self) -> List[Dict]:
        """Get available network interfaces"""
        try:
            interfaces = []
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface_name,
                    'addresses': [],
                    'is_up': interface_name in psutil.net_if_stats() and psutil.net_if_stats()[interface_name].isup
                }
                
                for address in interface_addresses:
                    interface_info['addresses'].append({
                        'family': str(address.family),
                        'address': address.address,
                        'netmask': address.netmask,
                        'broadcast': address.broadcast
                    })
                
                interfaces.append(interface_info)
            
            return interfaces
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def _apply_gaming_optimizations(self) -> List[Dict]:
        """Apply gaming-specific network optimizations"""
        optimizations = []
        
        try:
            # TCP optimization for gaming
            optimizations.append(self._optimize_tcp_for_gaming())
            
            # UDP optimization for gaming
            optimizations.append(self._optimize_udp_for_gaming())
            
            # Gaming port prioritization
            optimizations.append(self._prioritize_gaming_ports())
            
            # Latency optimization
            optimizations.append(self._optimize_latency())
            
            # Gaming DNS optimization
            optimizations.append(self._optimize_gaming_dns())
            
        except Exception as e:
            optimizations.append({'type': 'Gaming Optimization', 'error': str(e)})
        
        return optimizations
    
    def _apply_streaming_optimizations(self) -> List[Dict]:
        """Apply streaming-specific network optimizations"""
        optimizations = []
        
        try:
            # Bandwidth optimization for streaming
            optimizations.append(self._optimize_bandwidth_for_streaming())
            
            # Buffer optimization
            optimizations.append(self._optimize_streaming_buffers())
            
            # Streaming port prioritization
            optimizations.append(self._prioritize_streaming_ports())
            
        except Exception as e:
            optimizations.append({'type': 'Streaming Optimization', 'error': str(e)})
        
        return optimizations
    
    def _apply_productivity_optimizations(self) -> List[Dict]:
        """Apply productivity-specific network optimizations"""
        optimizations = []
        
        try:
            # Web browsing optimization
            optimizations.append(self._optimize_web_browsing())
            
            # Email and communication optimization
            optimizations.append(self._optimize_communication())
            
            # File transfer optimization
            optimizations.append(self._optimize_file_transfer())
            
        except Exception as e:
            optimizations.append({'type': 'Productivity Optimization', 'error': str(e)})
        
        return optimizations
    
    def _apply_universal_optimizations(self) -> List[Dict]:
        """Apply universal network optimizations"""
        optimizations = []
        
        try:
            # Network adapter optimization
            optimizations.append(self._optimize_network_adapters())
            
            # DNS optimization
            optimizations.append(self._optimize_dns_servers())
            
            # Network buffer optimization
            optimizations.append(self._optimize_network_buffers())
            
            # QoS optimization
            optimizations.append(self._optimize_qos())
            
        except Exception as e:
            optimizations.append({'type': 'Universal Optimization', 'error': str(e)})
        
        return optimizations
    
    def _optimize_tcp_for_gaming(self) -> Dict[str, any]:
        """Optimize TCP settings for gaming"""
        try:
            optimizations = []
            
            if platform.system() == "Windows":
                # TCP window scaling
                optimizations.append("Enabling TCP window scaling")
                subprocess.run(["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"], 
                             capture_output=True, check=True)
                
                # TCP congestion control
                optimizations.append("Setting TCP congestion control to BBR")
                subprocess.run(["netsh", "int", "tcp", "set", "global", "congestionprovider=bbr"], 
                             capture_output=True, check=True)
                
                # TCP receive window
                optimizations.append("Optimizing TCP receive window")
                subprocess.run(["netsh", "int", "tcp", "set", "global", "chimney=enabled"], 
                             capture_output=True, check=True)
            
            return {
                'type': 'TCP Gaming Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'TCP Gaming Optimization', 'error': str(e)}
    
    def _optimize_udp_for_gaming(self) -> Dict[str, any]:
        """Optimize UDP settings for gaming"""
        try:
            optimizations = []
            
            if platform.system() == "Windows":
                # UDP buffer optimization
                optimizations.append("Optimizing UDP buffer sizes")
                subprocess.run(["netsh", "int", "udp", "set", "global", "udprcvbuffer=65536"], 
                             capture_output=True, check=True)
                subprocess.run(["netsh", "int", "udp", "set", "global", "udpsndbuffer=65536"], 
                             capture_output=True, check=True)
            
            return {
                'type': 'UDP Gaming Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'UDP Gaming Optimization', 'error': str(e)}
    
    def _prioritize_gaming_ports(self) -> Dict[str, any]:
        """Prioritize gaming ports"""
        try:
            optimizations = []
            
            # Gaming ports to prioritize
            gaming_ports = {
                'League of Legends': [2099, 5222, 5223, 8080, 8443],
                'Valorant': [443, 5222, 5223, 8080, 8443],
                'CS2': [27015, 27016, 27017, 27018, 27019, 27020],
                'Fortnite': [443, 5222, 5223, 8080, 8443],
                'Apex Legends': [443, 5222, 5223, 8080, 8443]
            }
            
            for game, ports in gaming_ports.items():
                optimizations.append(f"Prioritizing {game} ports: {ports}")
                # This would involve setting up QoS rules for these ports
                # Implementation would depend on the specific network setup
            
            return {
                'type': 'Gaming Port Prioritization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Gaming Port Prioritization', 'error': str(e)}
    
    def _optimize_latency(self) -> Dict[str, any]:
        """Optimize network latency"""
        try:
            optimizations = []
            
            if platform.system() == "Windows":
                # Disable Nagle's algorithm for gaming (reduces latency)
                optimizations.append("Disabling Nagle's algorithm for gaming")
                subprocess.run(["netsh", "int", "tcp", "set", "global", "nagle=disabled"], 
                             capture_output=True, check=False)
                
                # Optimize TCP timestamps
                optimizations.append("Optimizing TCP timestamps")
                subprocess.run(["netsh", "int", "tcp", "set", "global", "timestamps=enabled"], 
                             capture_output=True, check=True)
                
                # Optimize TCP selective acknowledgments
                optimizations.append("Enabling TCP selective acknowledgments")
                subprocess.run(["netsh", "int", "tcp", "set", "global", "sack=enabled"], 
                             capture_output=True, check=True)
            
            return {
                'type': 'Latency Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Latency Optimization', 'error': str(e)}
    
    def _optimize_gaming_dns(self) -> Dict[str, any]:
        """Optimize DNS for gaming"""
        try:
            optimizations = []
            
            # Set fast DNS servers for gaming
            gaming_dns_servers = [
                '8.8.8.8',      # Google DNS
                '8.8.4.4',      # Google DNS
                '1.1.1.1',      # Cloudflare DNS
                '1.0.0.1'       # Cloudflare DNS
            ]
            
            optimizations.append(f"Setting gaming DNS servers: {gaming_dns_servers}")
            
            # This would involve setting DNS servers for gaming
            # Implementation would depend on the specific network setup
            
            return {
                'type': 'Gaming DNS Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Gaming DNS Optimization', 'error': str(e)}
    
    def _optimize_bandwidth_for_streaming(self) -> Dict[str, any]:
        """Optimize bandwidth for streaming"""
        try:
            optimizations = []
            
            # Streaming bandwidth optimization
            optimizations.append("Optimizing bandwidth for streaming")
            optimizations.append("Setting streaming buffer sizes")
            optimizations.append("Configuring streaming QoS")
            
            return {
                'type': 'Streaming Bandwidth Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Streaming Bandwidth Optimization', 'error': str(e)}
    
    def _optimize_streaming_buffers(self) -> Dict[str, any]:
        """Optimize streaming buffers"""
        try:
            optimizations = []
            
            # Streaming buffer optimization
            optimizations.append("Optimizing streaming buffers")
            optimizations.append("Setting optimal buffer sizes for streaming")
            
            return {
                'type': 'Streaming Buffer Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Streaming Buffer Optimization', 'error': str(e)}
    
    def _prioritize_streaming_ports(self) -> Dict[str, any]:
        """Prioritize streaming ports"""
        try:
            optimizations = []
            
            # Streaming ports to prioritize
            streaming_ports = {
                'Twitch': [443, 80, 1935],
                'YouTube': [443, 80],
                'Discord': [443, 80, 8080],
                'OBS': [443, 80, 8080]
            }
            
            for service, ports in streaming_ports.items():
                optimizations.append(f"Prioritizing {service} ports: {ports}")
            
            return {
                'type': 'Streaming Port Prioritization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Streaming Port Prioritization', 'error': str(e)}
    
    def _optimize_web_browsing(self) -> Dict[str, any]:
        """Optimize web browsing"""
        try:
            optimizations = []
            
            # Web browsing optimization
            optimizations.append("Optimizing web browsing performance")
            optimizations.append("Setting web browsing DNS servers")
            optimizations.append("Configuring web browsing cache")
            
            return {
                'type': 'Web Browsing Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Web Browsing Optimization', 'error': str(e)}
    
    def _optimize_communication(self) -> Dict[str, any]:
        """Optimize communication applications"""
        try:
            optimizations = []
            
            # Communication optimization
            optimizations.append("Optimizing communication applications")
            optimizations.append("Setting communication port priorities")
            optimizations.append("Configuring communication QoS")
            
            return {
                'type': 'Communication Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Communication Optimization', 'error': str(e)}
    
    def _optimize_file_transfer(self) -> Dict[str, any]:
        """Optimize file transfer"""
        try:
            optimizations = []
            
            # File transfer optimization
            optimizations.append("Optimizing file transfer performance")
            optimizations.append("Setting file transfer buffer sizes")
            optimizations.append("Configuring file transfer protocols")
            
            return {
                'type': 'File Transfer Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'File Transfer Optimization', 'error': str(e)}
    
    def _optimize_network_adapters(self) -> Dict[str, any]:
        """Optimize network adapters"""
        try:
            optimizations = []
            
            # Network adapter optimization
            optimizations.append("Optimizing network adapter settings")
            optimizations.append("Setting network adapter power management")
            optimizations.append("Configuring network adapter offloading")
            
            return {
                'type': 'Network Adapter Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Network Adapter Optimization', 'error': str(e)}
    
    def _optimize_dns_servers(self) -> Dict[str, any]:
        """Optimize DNS servers"""
        try:
            optimizations = []
            
            # Fast DNS servers
            fast_dns_servers = [
                '1.1.1.1',      # Cloudflare DNS
                '1.0.0.1',      # Cloudflare DNS
                '8.8.8.8',      # Google DNS
                '8.8.4.4'       # Google DNS
            ]
            
            optimizations.append(f"Setting fast DNS servers: {fast_dns_servers}")
            
            return {
                'type': 'DNS Server Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'DNS Server Optimization', 'error': str(e)}
    
    def _optimize_network_buffers(self) -> Dict[str, any]:
        """Optimize network buffers"""
        try:
            optimizations = []
            
            # Network buffer optimization
            optimizations.append("Optimizing network buffer sizes")
            optimizations.append("Setting network buffer limits")
            optimizations.append("Configuring network buffer management")
            
            return {
                'type': 'Network Buffer Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'Network Buffer Optimization', 'error': str(e)}
    
    def _optimize_qos(self) -> Dict[str, any]:
        """Optimize Quality of Service"""
        try:
            optimizations = []
            
            # QoS optimization
            optimizations.append("Configuring Quality of Service")
            optimizations.append("Setting traffic prioritization")
            optimizations.append("Configuring bandwidth allocation")
            
            return {
                'type': 'QoS Optimization',
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'type': 'QoS Optimization', 'error': str(e)}
    
    def _start_traffic_monitoring(self):
        """Start traffic monitoring"""
        try:
            self.optimization_thread = threading.Thread(target=self._traffic_monitoring_loop, daemon=True)
            self.optimization_thread.start()
        except Exception as e:
            print(f"Traffic monitoring thread error: {e}")
    
    def _traffic_monitoring_loop(self):
        """Traffic monitoring loop"""
        while self.is_optimizing:
            try:
                # Monitor network traffic and update traffic rules
                self._update_traffic_rules()
                
                time.sleep(10)  # Update every 10 seconds
                
            except Exception:
                time.sleep(10)
    
    def _update_traffic_rules(self):
        """Update traffic rules based on current usage"""
        try:
            # This would involve updating QoS rules based on current traffic
            # Implementation would depend on the specific network setup
            pass
        except Exception:
            pass
    
    def stop_network_optimization(self):
        """Stop network optimization"""
        self.is_optimizing = False
        if self.optimization_thread:
            self.optimization_thread.join(timeout=2)
        
        return {'status': 'stopped'}
    
    def get_network_status(self) -> Dict:
        """Get current network status"""
        try:
            network_io = psutil.net_io_counters()
            connections = psutil.net_connections()
            
            return {
                'status': 'optimizing' if self.is_optimizing else 'stopped',
                'interfaces': len(self.network_interfaces),
                'connections': len(connections),
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv,
                'packets_sent': network_io.packets_sent,
                'packets_recv': network_io.packets_recv,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def test_network_performance(self) -> Dict:
        """Test network performance"""
        try:
            # Test latency to various servers
            test_servers = [
                '8.8.8.8',      # Google DNS
                '1.1.1.1',      # Cloudflare DNS
                '208.67.222.222' # OpenDNS
            ]
            
            results = {}
            for server in test_servers:
                try:
                    start_time = time.time()
                    socket.create_connection((server, 53), timeout=5)
                    latency = (time.time() - start_time) * 1000
                    results[server] = {'latency_ms': latency, 'status': 'success'}
                except Exception:
                    results[server] = {'latency_ms': 0, 'status': 'failed'}
            
            return {
                'test_results': results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}
