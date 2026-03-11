import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from ngx_optimizer.app import NetworkOptimizerApp # type: ignore

def main():
    try:
        app = NetworkOptimizerApp()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
