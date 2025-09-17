#!/usr/bin/env python3
"""
Simple setup script for JalBuddy AI Backend
"""

import os
import sys
import subprocess

def run_cmd(cmd):
    """Run command and return success status"""
    print(f"Running: {cmd}")
    result = os.system(cmd)
    return result == 0

def main():
    print("🚀 JalBuddy AI Backend Setup")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Please run this from the AI-BACKEND directory")
        sys.exit(1)
    
    # Try different venv creation methods
    venv_created = False
    
    # Method 1: python3 -m venv
    if run_cmd("python3 -m venv venv"):
        venv_created = True
        print("✅ Virtual environment created with python3 -m venv")
    
    # Method 2: python -m venv (fallback)
    elif run_cmd("python -m venv venv"):
        venv_created = True
        print("✅ Virtual environment created with python -m venv")
    
    # Method 3: virtualenv (if available)
    elif run_cmd("virtualenv venv"):
        venv_created = True
        print("✅ Virtual environment created with virtualenv")
    
    if not venv_created:
        print("❌ Failed to create virtual environment")
        print("💡 Try installing python3-venv: sudo apt install python3-venv")
        print("💡 Or install virtualenv: pip install virtualenv")
        sys.exit(1)
    
    # Activate and install minimal dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        activate_cmd = "venv\\Scripts\\activate"
    else:  # Unix/Linux
        pip_cmd = "venv/bin/pip"
        activate_cmd = "source venv/bin/activate"
    
    print("📦 Installing minimal dependencies...")
    
    # Install core dependencies one by one
    core_deps = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0"
    ]
    
    for dep in core_deps:
        if run_cmd(f"{pip_cmd} install {dep}"):
            print(f"✅ Installed {dep}")
        else:
            print(f"⚠️ Failed to install {dep}")
    
    print("\n🎉 Setup complete!")
    print(f"📋 To activate: {activate_cmd}")
    print("📋 To run server: python main.py")

if __name__ == "__main__":
    main()
