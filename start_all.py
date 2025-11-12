"""
Start All Services
===================
Starts ML service (Flask), Backend (Node.js), and Frontend (Vite)
"""
import subprocess
import sys
import os
import time

def start_service(name, command, cwd):
    """Start a service in a new terminal"""
    print(f"\n🚀 Starting {name}...")
    
    if sys.platform == 'win32':
        # Windows: Start in new PowerShell window
        ps_command = f"cd '{cwd}'; {command}"
        subprocess.Popen(
            ['powershell', '-NoExit', '-Command', ps_command],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        # Linux/Mac: Start in background
        subprocess.Popen(
            command,
            shell=True,
            cwd=cwd
        )
    
    time.sleep(2)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("="*80)
    print("🎯 Flight Fare Prediction - Starting All Services")
    print("="*80)
    
    # Start ML Service (Flask)
    ml_dir = base_dir
    start_service(
        "ML Service (Flask - Port 5001)",
        "python backend\\ml_service.py",
        ml_dir
    )
    
    # Start Backend (Node.js)
    backend_dir = os.path.join(base_dir, 'backend')
    start_service(
        "Backend API (Node.js - Port 4000)",
        "npm start",
        backend_dir
    )
    
    # Start Frontend (Vite)
    frontend_dir = os.path.join(base_dir, 'frontend')
    start_service(
        "Frontend (Vite - Port 5173)",
        "npm run dev",
        frontend_dir
    )
    
    print("\n" + "="*80)
    print("✅ All Services Started!")
    print("="*80)
    print("\n📋 Services Running:")
    print("   🔬 ML Service:  http://localhost:5001")
    print("   🔧 Backend API: http://localhost:4000")
    print("   🌐 Frontend:    http://localhost:5173")
    print("\n💡 Open http://localhost:5173 in your browser")
    print("\n⚠️  Close all terminal windows to stop services")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
