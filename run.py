#!/usr/bin/env python3
"""
RUN.PY - ALPHA SELFBOT LAUNCHER
Run this file to start the bot with everything needed
No additional setup required - just run once!
"""

import os
import sys
import subprocess
import platform

def print_startup_banner():
    """Print startup banner"""
    banner = """
    
    ███████████████████████████████████████████████████████████████████████████████
    █                                                                             █
    █    ╔═══════════════════════════════════════════════════════════════════╗  █
    █    ║                                                                   ║  █
    █    ║               🚀 ALPHA SELFBOT LAUNCHER 🚀                      ║  █
    █    ║                                                                   ║  █
    █    ║              Starting NUKE • SPAM • MASSBAN Bot...              ║  █
    █    ║                                                                   ║  █
    █    ╚═══════════════════════════════════════════════════════════════════╝  █
    █                                                                             █
    ███████████████████████████████████████████████████████████████████████████████
    """
    print(banner)

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("\n❌ ERROR: .env file not found!")
        print("\n📋 Creating .env.example for you...")
        print("\nSteps:")
        print("1. Copy .env.example to .env")
        print("2. Add your DISCORD_TOKEN")
        print("3. Add your OWNER_ID")
        print("4. Run this script again\n")
        sys.exit(1)
    
    # Check if .env has required values
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_bot_token_here' in content or 'your_discord_id_here' in content:
            print("\n❌ ERROR: .env file not properly configured!")
            print("\n📋 Please update .env with:")
            print("   - DISCORD_TOKEN=your_actual_token")
            print("   - OWNER_ID=your_actual_id\n")
            sys.exit(1)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['discord', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️  Missing packages detected!")
        print(f"\n📦 Installing: {', '.join(missing_packages)}...\n")
        
        cmd = [sys.executable, '-m', 'pip', 'install'] + missing_packages
        subprocess.check_call(cmd)
        print("\n✓ Packages installed!\n")

def start_bot():
    """Start the bot"""
    print("\n✓ All checks passed!")
    print("✓ Starting ALPHA SELFBOT...\n")
    print("="*80)
    
    try:
        # Run main.py
        if platform.system() == "Windows":
            subprocess.call([sys.executable, 'main.py'])
        else:
            subprocess.call([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n\n✓ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print_startup_banner()
    
    print("\n⏳ Checking environment...")
    check_env_file()
    
    print("✓ .env file found!")
    
    print("\n⏳ Checking dependencies...")
    check_dependencies()
    
    print("\n" + "="*80)
    print("ALPHA SELFBOT READY TO LAUNCH")
    print("="*80)
    
    start_bot()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n✓ Launcher stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
