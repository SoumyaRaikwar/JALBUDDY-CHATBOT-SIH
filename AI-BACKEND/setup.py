#!/usr/bin/env python3
"""
Setup script for JalBuddy AI Backend
Creates virtual environment and installs dependencies
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run shell command and handle errors"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main setup function"""
    print("🚀 Setting up JalBuddy AI Backend...")
    
    # Get current directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Backend directory: {backend_dir}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Create virtual environment
    venv_path = os.path.join(backend_dir, "venv")
    
    if os.path.exists(venv_path):
        print("🔄 Virtual environment already exists, removing...")
        if platform.system() == "Windows":
            run_command(f"rmdir /s /q {venv_path}")
        else:
            run_command(f"rm -rf {venv_path}")
    
    print("🏗️ Creating virtual environment...")
    if not run_command(f"python3 -m venv venv", cwd=backend_dir):
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Determine activation script path
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    # Upgrade pip
    print("⬆️ Upgrading pip...")
    if not run_command(f"{pip_path} install --upgrade pip", cwd=backend_dir):
        print("⚠️ Failed to upgrade pip, continuing...")
    
    # Install requirements
    requirements_file = os.path.join(backend_dir, "requirements.txt")
    if os.path.exists(requirements_file):
        print("📦 Installing dependencies...")
        if not run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir):
            print("❌ Failed to install some dependencies")
            print("🔧 Trying with reduced requirements...")
            
            # Create minimal requirements for testing
            minimal_reqs = [
                "fastapi==0.104.1",
                "uvicorn[standard]==0.24.0", 
                "pydantic==2.5.0",
                "pydantic-settings==2.1.0",
                "python-multipart==0.0.6",
                "python-dotenv==1.0.0"
            ]
            
            for req in minimal_reqs:
                run_command(f"{pip_path} install {req}", cwd=backend_dir)
    else:
        print("⚠️ requirements.txt not found")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    
    if platform.system() == "Windows":
        print("1. Activate virtual environment: venv\\Scripts\\activate")
    else:
        print("1. Activate virtual environment: source venv/bin/activate")
    
    print("2. Run the server: python main.py")
    print("3. Visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
