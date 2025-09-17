#!/usr/bin/env python3
"""
Install missing dependencies for JalBuddy AI Backend
"""

import subprocess
import sys

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("📦 Installing missing dependencies...")
    
    missing_deps = [
        "sqlalchemy==2.0.23",
        "alembic==1.13.1"
    ]
    
    for dep in missing_deps:
        install_package(dep)
    
    print("🎉 Dependencies installed!")
    print("📋 Now try: python main.py")

if __name__ == "__main__":
    main()
