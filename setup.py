"""
PBSC-Ignite Platform Setup Script
Automated setup for the AI-Powered Career Readiness Platform
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step_num, text):
    """Print formatted step"""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 70)

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    if description:
        print(f"  ➤ {description}")
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
        
        if result.stdout:
            print(f"    {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"    ❌ Error: {e}")
        if e.stderr:
            print(f"    {e.stderr.strip()}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"  Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("  ✅ Python version is compatible (3.8+)")
        return True
    else:
        print("  ❌ Python 3.8 or higher is required")
        return False

def check_mongodb():
    """Check if MongoDB is running"""
    print_step(2, "Checking MongoDB")
    
    try:
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        load_dotenv()
        
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        
        print(f"  ✅ MongoDB is running at {mongo_uri}")
        client.close()
        return True
    except Exception as e:
        print(f"  ❌ MongoDB connection failed: {str(e)}")
        print(f"\n  Please ensure MongoDB is installed and running:")
        print(f"    • Windows: Download from https://www.mongodb.com/try/download/community")
        print(f"    • Start service: net start MongoDB")
        print(f"    • Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas")
        return False

def check_redis():
    """Check if Redis is running (optional)"""
    print_step(3, "Checking Redis (Optional)")
    
    try:
        import redis
        from dotenv import load_dotenv
        
        load_dotenv()
        
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        
        r = redis.Redis(host=redis_host, port=redis_port, socket_timeout=5)
        r.ping()
        
        print(f"  ✅ Redis is running at {redis_host}:{redis_port}")
        print(f"  ✅ Caching features will be enabled")
        return True
    except Exception as e:
        print(f"  ⚠️  Redis not available: {str(e)}")
        print(f"  ℹ️  The application will work without Redis, but caching will be disabled")
        print(f"\n  To enable caching:")
        print(f"    • Windows: Download from https://github.com/microsoftarchive/redis/releases")
        print(f"    • Or use Redis Cloud: https://redis.com/try-free/")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print_step(4, "Installing Dependencies")
    
    if not os.path.exists("requirements.txt"):
        print("  ❌ requirements.txt not found")
        return False
    
    print("  Installing packages from requirements.txt...")
    print("  This may take several minutes...\n")
    
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )
    
    if success:
        print("\n  ✅ Dependencies installed successfully")
    else:
        print("\n  ❌ Failed to install some dependencies")
        print("  Try running manually: pip install -r requirements.txt")
    
    return success

def setup_environment():
    """Setup environment variables"""
    print_step(5, "Setting Up Environment")
    
    if os.path.exists(".env"):
        print("  ✅ .env file already exists")
        
        response = input("\n  Do you want to keep existing .env file? (y/n): ").lower()
        if response == 'y':
            print("  Keeping existing .env file")
            return True
        else:
            print("  Creating backup of existing .env...")
            os.rename(".env", ".env.backup")
            print("  ✅ Backup created: .env.backup")
    
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("  ✅ Created .env from .env.example")
        print("\n  ⚠️  IMPORTANT: Edit .env file and add your API keys:")
        print("     • GROQ_API_KEY")
        print("     • PERPLEXITY_API_KEY")
        print("     • AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY (for Bedrock)")
        print("     • UNIPILE_API_KEY (for LinkedIn integration)")
        return True
    else:
        print("  ❌ .env.example not found")
        return False

def initialize_database():
    """Initialize MongoDB database"""
    print_step(6, "Initializing Database")
    
    response = input("\n  Initialize database collections and indexes? (y/n): ").lower()
    
    if response != 'y':
        print("  Skipping database initialization")
        return True
    
    try:
        print("\n  Running database initialization...")
        success = run_command(
            f"{sys.executable} init_db.py init",
            "Creating collections and indexes"
        )
        
        if success:
            print("  ✅ Database initialized successfully")
        else:
            print("  ❌ Database initialization failed")
            print("  You can run it manually later: python init_db.py init")
        
        return success
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def create_directories():
    """Create necessary directories"""
    print_step(7, "Creating Required Directories")
    
    directories = [
        "app/Static/uploads",
        "app/Static/cache",
        "logs",
        "instance"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("\n  ✅ Directories created")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete! 🎉")
    
    print("Next Steps:")
    print("\n1. Configure API Keys:")
    print("   • Edit the .env file")
    print("   • Add your API keys for AI services")
    print("   • Update MongoDB URI if not using localhost")
    
    print("\n2. Start the Application:")
    print("   python run.py")
    
    print("\n3. Access the Platform:")
    print("   Open your browser and go to: http://localhost:5000")
    
    print("\n4. Optional - Check Database:")
    print("   python init_db.py check")
    
    print("\n" + "=" * 70)
    print("\nFor more information, see README.md")
    print("=" * 70 + "\n")

def main():
    """Main setup function"""
    print_header("PBSC-Ignite Platform - Automated Setup")
    
    print("This script will:")
    print("  ✓ Check system requirements")
    print("  ✓ Install dependencies")
    print("  ✓ Setup environment configuration")
    print("  ✓ Initialize database")
    print("  ✓ Prepare the application to run")
    
    response = input("\nContinue with setup? (y/n): ").lower()
    
    if response != 'y':
        print("\nSetup cancelled.")
        return
    
    # Run setup steps
    steps_passed = 0
    total_steps = 7
    
    if check_python_version():
        steps_passed += 1
    else:
        print("\n❌ Setup failed: Incompatible Python version")
        return
    
    if check_mongodb():
        steps_passed += 1
    else:
        print("\n⚠️  Warning: MongoDB not running")
        print("The application requires MongoDB. Please install and start it.")
    
    if check_redis():
        steps_passed += 1
    else:
        steps_passed += 1  # Redis is optional
    
    if install_dependencies():
        steps_passed += 1
    else:
        print("\n❌ Setup failed: Could not install dependencies")
        return
    
    if setup_environment():
        steps_passed += 1
    
    if create_directories():
        steps_passed += 1
    
    if initialize_database():
        steps_passed += 1
    
    # Print summary
    print(f"\n{'=' * 70}")
    print(f"Setup Progress: {steps_passed}/{total_steps} steps completed")
    print("=" * 70)
    
    if steps_passed >= total_steps - 1:  # Allow for Redis being optional
        print_next_steps()
    else:
        print("\n⚠️  Setup completed with some warnings.")
        print("Please review the messages above and fix any issues.")

if __name__ == "__main__":
    main()
