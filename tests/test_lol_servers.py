import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(PROJECT_ROOT, "src"))

try:
    from ngx_optimizer.modules.lol_optimizer import LoLOptimizer # type: ignore
    
    def test_lol_servers():
        """Test League of Legends server latency"""
        print("League of Legends Server Latency Test")
        print("=" * 50)
        
        lol_optimizer = LoLOptimizer()
        
        print("Testing server latencies...")
        latencies = lol_optimizer.get_lol_server_latency()
        
        print("\nServer Latency Results:")
        print("-" * 30)
        
        for region, latency in latencies.items():
            if latency < 999:
                if latency < 50:
                    status = "[OK] Good"
                elif latency < 100:
                    status = "[WARN] Fair"
                else:
                    status = "[POOR] Poor"
                print(f"{region:4}: {latency:6.1f}ms {status}")
            else:
                print(f"{region:4}: {'Unable to reach':>15} [FAIL]")
        
        # Performance metrics
        print("\nLoL Performance Metrics:")
        print("-" * 30)
        metrics = lol_optimizer.get_lol_performance_metrics()
        print(f"Processes Running: {metrics['running']}")
        print(f"Memory Usage: {metrics['mem_mb']:.1f} MB")
        
    if __name__ == "__main__":
        test_lol_servers()
        
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("Make sure you're running from the project directory")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Error: {e}")
    sys.exit(1)
