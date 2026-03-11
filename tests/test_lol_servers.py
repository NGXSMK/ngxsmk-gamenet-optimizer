#!/usr/bin/env python3
"""
Test script for League of Legends server latency
Tests all major LoL servers including Singapore
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from modules.lol_optimizer import LoLOptimizer
    
    def test_lol_servers():
        """Test League of Legends server latency"""
        print("🎮 League of Legends Server Latency Test")
        print("=" * 50)
        
        lol_optimizer = LoLOptimizer()
        
        print("Testing server latencies...")
        latencies = lol_optimizer.get_lol_server_latency()
        
        print("\n📊 Server Latency Results:")
        print("-" * 30)
        
        for region, latency in latencies.items():
            if latency < 999:
                status = "✅ Good" if latency < 50 else "⚠️  Fair" if latency < 100 else "❌ Poor"
                print(f"{region:4}: {latency:6.1f}ms {status}")
            else:
                print(f"{region:4}: {'Unable to reach':>15} ❌")
        
        # Find best server
        best_server = lol_optimizer.get_best_lol_server()
        print(f"\n🏆 Best Server: {best_server}")
        
        # Performance metrics
        print("\n📈 LoL Performance Metrics:")
        print("-" * 30)
        metrics = lol_optimizer.get_lol_performance_metrics()
        print(f"Processes Running: {metrics['processes_running']}")
        print(f"Memory Usage: {metrics['total_memory_mb']:.1f} MB")
        print(f"CPU Usage: {metrics['cpu_usage']:.1f}%")
        print(f"Network Connections: {metrics['network_connections']}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        print("-" * 30)
        recommendations = lol_optimizer.get_lol_optimization_recommendations()
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec}")
    
    if __name__ == "__main__":
        test_lol_servers()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
