#!/usr/bin/env python
"""
English to Kannada Translator - Installation & Setup Script
This script helps set up the translator application with minimal configuration.
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def install_dependencies(requirements_file):
    """Install Python dependencies"""
    print_info(f"Installing dependencies from {requirements_file}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print_success(f"Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print_error(f"Failed to install dependencies from {requirements_file}")
        return False

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required. You have {sys.version}")
        return False
    print_success(f"Python {sys.version.split()[0]} detected")
    return True

def check_microphone():
    """Check if microphone is available"""
    try:
        import pyaudio
        print_success("Microphone support available")
        return True
    except ImportError:
        print_info("PyAudio not detected (required for speech features)")
        return False

def setup_google_cloud():
    """Setup Google Cloud credentials"""
    print_header("Google Cloud Setup")
    
    credentials_path = input("Enter path to Google Cloud credentials JSON file (or press Enter to skip): ").strip()
    
    if credentials_path and os.path.exists(credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        print_success(f"Google Cloud credentials set to: {credentials_path}")
        return True
    elif credentials_path:
        print_error(f"File not found: {credentials_path}")
        return False
    else:
        print_info("Google Cloud setup skipped. Using local translation services.")
        return False

def main():
    """Main setup function"""
    print_header("English to Kannada Translator - Setup")
    
    print("Choose your setup option:\n")
    print("1. Local Setup (No Google Cloud, instant start)")
    print("2. Google Cloud Setup (Professional grade, requires credentials)")
    print("3. Custom Setup")
    print("4. Exit\n")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        setup_local()
    elif choice == "2":
        setup_google_cloud_full()
    elif choice == "3":
        setup_custom()
    elif choice == "4":
        print("Exiting setup...")
        sys.exit(0)
    else:
        print_error("Invalid choice. Please try again.")
        main()

def setup_local():
    """Setup local version"""
    print_header("Setting Up Local Version")
    
    if not check_python_version():
        sys.exit(1)
    
    print_info("Installing dependencies for local translation...")
    if not install_dependencies("requirements_local.txt"):
        print_error("Setup failed!")
        sys.exit(1)
    
    check_microphone()
    
    print_success("✨ Setup complete!")
    print_info("To start the application, run:")
    print(f"  python app_local.py\n")
    print("Then open: http://localhost:5000")

def setup_google_cloud_full():
    """Setup Google Cloud version"""
    print_header("Setting Up Google Cloud Version")
    
    if not check_python_version():
        sys.exit(1)
    
    print_info("Installing dependencies for Google Cloud...")
    if not install_dependencies("requirements.txt"):
        print_error("Setup failed!")
        sys.exit(1)
    
    if setup_google_cloud():
        check_microphone()
        print_success("✨ Setup complete!")
        print_info("To start the application, run:")
        print(f"  python app.py\n")
        print("Then open: http://localhost:5000")
    else:
        print_error("Google Cloud setup incomplete. Please verify credentials and try again.")

def setup_custom():
    """Custom setup"""
    print_header("Custom Setup")
    
    print("1. Install local dependencies")
    print("2. Install Google Cloud dependencies")
    print("3. Install both")
    print("4. Back to main menu\n")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        install_dependencies("requirements_local.txt")
    elif choice == "2":
        install_dependencies("requirements.txt")
        setup_google_cloud()
    elif choice == "3":
        install_dependencies("requirements_local.txt")
        install_dependencies("requirements.txt")
        setup_google_cloud()
    elif choice == "4":
        main()
    else:
        print_error("Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        sys.exit(1)
