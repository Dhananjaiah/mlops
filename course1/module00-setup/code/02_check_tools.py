"""
Quick Tool Check

This script demonstrates checking for required tools programmatically.
It's a simpler version of verify_setup.py for learning purposes.
"""

import subprocess
import sys


def run_command(command):
    """
    Run a shell command and return the output.
    
    Args:
        command: List of command parts (e.g., ['python', '--version'])
        
    Returns:
        tuple: (success: bool, output: str)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return False, str(e)


def check_tool(tool_name, command):
    """Check if a tool is available."""
    print(f"\n🔍 Checking {tool_name}...")
    success, output = run_command(command)
    
    if success:
        print(f"✅ {tool_name} found!")
        print(f"   {output}")
        return True
    else:
        print(f"❌ {tool_name} not found")
        print(f"   Please install {tool_name}")
        return False


def main():
    """Main function to check all tools."""
    print("="*60)
    print("🛠️  TOOL AVAILABILITY CHECK")
    print("="*60)
    
    tools = [
        ("Python", ['python', '--version']),
        ("Git", ['git', '--version']),
        ("Docker", ['docker', '--version']),
    ]
    
    results = []
    for tool_name, command in tools:
        result = check_tool(tool_name, command)
        results.append((tool_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    all_ok = all(ok for _, ok in results)
    
    for tool_name, ok in results:
        status = "✅" if ok else "❌"
        print(f"{status} {tool_name}")
    
    if all_ok:
        print("\n🎉 All required tools are available!")
    else:
        print("\n⚠️  Some tools are missing. Please install them.")
    
    print("="*60)


if __name__ == "__main__":
    main()
