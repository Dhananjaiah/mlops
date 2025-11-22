"""
Hello MLOps!

A simple introductory script to welcome you to the course.
This demonstrates basic Python and introduces key concepts.
"""

import sys
from datetime import datetime


def print_banner():
    """Print a welcome banner."""
    print("="*60)
    print(" " * 15 + "🚀 WELCOME TO MLOPS! 🚀")
    print("="*60)


def print_environment_info():
    """Print information about the Python environment."""
    print("\n📊 Your Environment Information:")
    print(f"   Python Version: {sys.version}")
    print(f"   Platform: {sys.platform}")
    print(f"   Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def explain_mlops():
    """Explain what MLOps is in simple terms."""
    print("\n🤔 What is MLOps?")
    print("-" * 60)
    print("""
MLOps is the practice of bringing DevOps principles to Machine Learning.

Think of it as:
  🏗️  Building reliable ML systems (not just models)
  🔄  Automating repetitive tasks
  📊  Monitoring what happens in production
  🔧  Making updates safely and quickly
  📚  Keeping track of everything

Without MLOps:
  ❌ "Works on my machine" problems
  ❌ Can't reproduce results
  ❌ Broken models in production
  ❌ Manual, error-prone processes

With MLOps:
  ✅ Reproducible experiments
  ✅ Automated pipelines
  ✅ Monitored production systems
  ✅ Fast, safe deployments
    """)


def show_course_path():
    """Show the learning path."""
    print("\n📚 Your Learning Path:")
    print("-" * 60)
    
    modules = [
        ("Module 00", "Setup and Overview", "30 min", "← You are here"),
        ("Module 01", "MLOps Foundations", "1 hour", ""),
        ("Module 02", "Environment & Packaging", "1.5 hours", ""),
        ("Module 03", "Data Versioning", "2 hours", ""),
        ("Module 04", "Experiment Tracking", "2 hours", ""),
        ("Module 05", "Pipelines & Orchestration", "2.5 hours", ""),
        ("Module 06", "Model Training", "2 hours", ""),
        ("Module 07", "Model Registry", "1.5 hours", ""),
        ("Module 08", "Serving & APIs", "2 hours", ""),
    ]
    
    for num, name, duration, note in modules:
        print(f"  {num}: {name:<30} {duration:<15} {note}")


def show_tools():
    """Show the tools we'll use."""
    print("\n🛠️  Tools You'll Master:")
    print("-" * 60)
    
    tools = [
        ("Git", "Version control for code"),
        ("DVC", "Version control for data"),
        ("MLflow", "Experiment tracking and model registry"),
        ("Airflow", "Pipeline orchestration"),
        ("Docker", "Containerization"),
        ("FastAPI", "API serving"),
        ("Prometheus", "Monitoring metrics"),
        ("Grafana", "Visualization dashboards"),
    ]
    
    for tool, description in tools:
        print(f"  • {tool:<15} - {description}")


def show_next_steps():
    """Show what to do next."""
    print("\n🎯 Next Steps:")
    print("-" * 60)
    print("""
  1. Verify your setup:
     → python verify_setup.py

  2. Read the complete transcript:
     → cat ../transcript.md

  3. Explore the code examples:
     → ls -la
     → python 02_check_tools.py

  4. Complete the exercises:
     → cd ../exercises
     → cat exercise01.md

  5. Move to Module 01:
     → cd ../../module01-foundations
     → cat README.md
    """)


def main():
    """Main function."""
    print_banner()
    print_environment_info()
    explain_mlops()
    show_course_path()
    show_tools()
    show_next_steps()
    
    print("\n" + "="*60)
    print("  🎓 Ready to transform how you deploy ML? Let's go!")
    print("="*60)
    print()


if __name__ == "__main__":
    main()
