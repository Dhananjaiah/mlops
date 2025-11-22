"""
Module 00: Environment Verification Script

This script checks if your development environment is properly set up.
It verifies Python version, required packages, and Docker installation.

Run this script to ensure you're ready to start the course!
"""

import sys
import subprocess
import importlib
from typing import Tuple, List


def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.11 or higher."""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version_str} - OK")
        return True, version_str
    else:
        print(f"❌ Python {version_str} - Need Python 3.11 or higher")
        return False, version_str


def check_docker() -> Tuple[bool, str]:
    """Check if Docker is installed and running."""
    print("\n🔍 Checking Docker...")
    
    try:
        # Check Docker version
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        
        # Check if Docker daemon is running
        subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            check=True
        )
        
        print(f"✅ Docker is installed and running")
        print(f"   Version: {version}")
        return True, version
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not running")
        print("   Please install Docker Desktop from docker.com")
        return False, "Not found"


def check_git() -> Tuple[bool, str]:
    """Check if Git is installed."""
    print("\n🔍 Checking Git...")
    
    try:
        result = subprocess.run(
            ['git', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✅ {version}")
        return True, version
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed")
        return False, "Not found"


def check_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        return True, version
    except ImportError:
        return False, "Not installed"


def check_dependencies() -> List[Tuple[str, bool, str]]:
    """Check if all required dependencies are installed."""
    print("\n🔍 Checking required dependencies...")
    
    required_packages = [
        ('mlflow', 'mlflow'),
        ('dvc', 'dvc'),
        ('fastapi', 'fastapi'),
        ('scikit-learn', 'sklearn'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
    ]
    
    results = []
    all_ok = True
    
    for package_name, import_name in required_packages:
        is_installed, version = check_package(package_name, import_name)
        results.append((package_name, is_installed, version))
        
        if is_installed:
            print(f"✅ {package_name}: {version}")
        else:
            print(f"❌ {package_name}: Not installed")
            all_ok = False
    
    return results


def print_summary(python_ok: bool, docker_ok: bool, git_ok: bool, deps_ok: bool):
    """Print a summary of the verification."""
    print("\n" + "="*60)
    print("📊 SETUP VERIFICATION SUMMARY")
    print("="*60)
    
    checks = [
        ("Python 3.11+", python_ok),
        ("Docker", docker_ok),
        ("Git", git_ok),
        ("Dependencies", deps_ok),
    ]
    
    all_ok = all(ok for _, ok in checks)
    
    for check_name, ok in checks:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{check_name:.<40} {status}")
    
    print("="*60)
    
    if all_ok:
        print("\n🎉 All checks passed! You're ready to start learning.")
        print("\n📚 Next steps:")
        print("   1. Read module00-setup/transcript.md")
        print("   2. Run the example scripts in code/")
        print("   3. Move to module01-foundations/")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Tips:")
        print("   - Check the troubleshooting section in transcript.md")
        print("   - Ensure virtual environment is activated")
        print("   - Run: pip install -r requirements.txt")


def main():
    """Main verification function."""
    print("="*60)
    print("🚀 MLOps COURSE - ENVIRONMENT VERIFICATION")
    print("="*60)
    print()
    
    # Check Python
    python_ok, python_version = check_python_version()
    
    # Check Docker
    docker_ok, docker_version = check_docker()
    
    # Check Git
    git_ok, git_version = check_git()
    
    # Check dependencies
    dep_results = check_dependencies()
    deps_ok = all(ok for _, ok, _ in dep_results)
    
    # Print summary
    print_summary(python_ok, docker_ok, git_ok, deps_ok)
    
    # Return exit code
    if python_ok and docker_ok and git_ok and deps_ok:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
