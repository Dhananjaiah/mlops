"""
Module 01: Reproducibility Demonstration

This script shows why reproducibility matters and how to achieve it.

Key concepts:
- Same code + same data + same random seed = same results
- How small changes affect results
- Why tracking versions is critical
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json
from pathlib import Path


def train_model_reproducible(random_seed=42):
    """
    Train a model with a specific random seed.
    Returns the accuracy and model state.
    """
    # Set random seeds for reproducibility
    np.random.seed(random_seed)
    
    # Generate data (with seed, so it's reproducible)
    n_samples = 500
    X = np.random.randn(n_samples, 10)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_seed
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=5,
        random_state=random_seed
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    return accuracy, model


def demonstrate_reproducibility():
    """Show that same seed gives same results."""
    print("\n" + "="*60)
    print("DEMONSTRATION 1: Perfect Reproducibility")
    print("="*60)
    
    print("\n🔬 Running same model 3 times with SAME seed...")
    
    results = []
    for i in range(3):
        accuracy, model = train_model_reproducible(random_seed=42)
        results.append(accuracy)
        print(f"  Run {i+1}: Accuracy = {accuracy:.6f}")
    
    print(f"\n✅ All runs identical: {len(set(results)) == 1}")
    print(f"   Standard deviation: {np.std(results):.10f}")
    
    print("\n💡 Key Point:")
    print("   Same seed → Same random numbers → Same results")
    print("   This is PERFECT reproducibility!")


def demonstrate_non_reproducibility():
    """Show what happens without fixed seeds."""
    print("\n" + "="*60)
    print("DEMONSTRATION 2: What Happens Without Fixed Seeds")
    print("="*60)
    
    print("\n🔬 Running same model 3 times with DIFFERENT seeds...")
    
    results = []
    for i in range(3):
        accuracy, model = train_model_reproducible(random_seed=i)
        results.append(accuracy)
        print(f"  Run {i+1}: Accuracy = {accuracy:.6f}")
    
    print(f"\n⚠️  Results vary: {len(set(results)) > 1}")
    print(f"   Variation range: {max(results) - min(results):.6f}")
    print(f"   Standard deviation: {np.std(results):.6f}")
    
    print("\n💡 Key Point:")
    print("   Different seeds → Different results")
    print("   Without reproducibility, you can't debug or compare!")


def demonstrate_version_tracking():
    """Show how to track versions for reproducibility."""
    print("\n" + "="*60)
    print("DEMONSTRATION 3: Tracking for Reproducibility")
    print("="*60)
    
    print("\n📝 Creating reproducibility record...")
    
    # Run experiment
    accuracy, model = train_model_reproducible(random_seed=42)
    
    # Create reproducibility record
    record = {
        'experiment_id': 'exp_001',
        'timestamp': '2024-01-15T10:30:00',
        'code': {
            'version': 'commit_abc123',
            'file': 'train.py',
            'function': 'train_model_reproducible'
        },
        'data': {
            'version': 'v1.0',
            'hash': '5f4dcc3b5aa765d61d8327deb882cf99',
            'samples': 500,
            'features': 10
        },
        'environment': {
            'python': '3.11.5',
            'numpy': '1.24.3',
            'scikit-learn': '1.3.0'
        },
        'hyperparameters': {
            'n_estimators': 50,
            'max_depth': 5,
            'random_state': 42
        },
        'results': {
            'accuracy': float(accuracy)
        }
    }
    
    # Save record
    Path('reproducibility').mkdir(exist_ok=True)
    record_path = 'reproducibility/experiment_001.json'
    with open(record_path, 'w') as f:
        json.dump(record, f, indent=2)
    
    print(f"✅ Saved reproducibility record: {record_path}")
    
    print("\n📋 Record contents:")
    for key, value in record.items():
        print(f"  {key}: {value}")
    
    print("\n💡 Key Point:")
    print("   Record EVERYTHING needed to reproduce:")
    print("   - Code version (Git commit)")
    print("   - Data version (hash or DVC)")
    print("   - Environment (Python, packages)")
    print("   - Hyperparameters (all settings)")
    print("   - Random seeds")


def demonstrate_reproduce_from_record():
    """Show how to reproduce an experiment from a record."""
    print("\n" + "="*60)
    print("DEMONSTRATION 4: Reproducing from Record")
    print("="*60)
    
    record_path = 'reproducibility/experiment_001.json'
    
    if not Path(record_path).exists():
        print("⚠️  Run demonstration 3 first")
        return
    
    print(f"\n📂 Loading record: {record_path}")
    with open(record_path, 'r') as f:
        record = json.load(f)
    
    print("✅ Record loaded")
    print(f"\n🔄 Reproducing experiment: {record['experiment_id']}")
    print(f"   Original accuracy: {record['results']['accuracy']:.6f}")
    
    # Reproduce using the saved settings
    random_seed = record['hyperparameters']['random_state']
    accuracy, model = train_model_reproducible(random_seed=random_seed)
    
    print(f"   Reproduced accuracy: {accuracy:.6f}")
    
    # Check if reproduction was successful
    original = record['results']['accuracy']
    diff = abs(accuracy - original)
    
    if diff < 1e-6:
        print(f"\n✅ REPRODUCTION SUCCESSFUL!")
        print(f"   Difference: {diff:.10f} (essentially zero)")
    else:
        print(f"\n❌ REPRODUCTION FAILED")
        print(f"   Difference: {diff:.6f}")
    
    print("\n💡 Key Point:")
    print("   With complete records, anyone can reproduce your work")
    print("   This is essential for:")
    print("   - Debugging issues")
    print("   - Scientific validation")
    print("   - Regulatory compliance")
    print("   - Team collaboration")


def demonstrate_what_breaks_reproducibility():
    """Show common things that break reproducibility."""
    print("\n" + "="*60)
    print("DEMONSTRATION 5: What Breaks Reproducibility?")
    print("="*60)
    
    print("\n⚠️  Common reproducibility killers:")
    
    issues = [
        ("No random seed", "Different results every run"),
        ("Data changes", "Model trained on different data"),
        ("Package updates", "sklearn v1.3 ≠ sklearn v1.4"),
        ("Hardware differences", "CPU vs GPU can give different results"),
        ("Untracked dependencies", "Hidden dependencies not recorded"),
        ("Manual steps", "Forgot what preprocessing was done"),
        ("No version control", "Can't find the exact code used"),
    ]
    
    for issue, consequence in issues:
        print(f"\n  ❌ {issue}")
        print(f"     → {consequence}")
    
    print("\n💡 MLOps Solutions:")
    solutions = [
        ("Fix random seeds", "Set seeds in code"),
        ("Version data", "Use DVC to track data"),
        ("Lock dependencies", "requirements.txt with exact versions"),
        ("Use containers", "Docker ensures same environment"),
        ("Track everything", "MLflow logs all parameters"),
        ("Automate", "Pipelines ensure same steps"),
        ("Use Git", "Track all code changes"),
    ]
    
    for solution, how in solutions:
        print(f"\n  ✅ {solution}")
        print(f"     → {how}")


def main():
    """Main function."""
    print("="*60)
    print(" " * 10 + "🔬 REPRODUCIBILITY DEMONSTRATION")
    print("="*60)
    
    print("\n📚 What you'll learn:")
    print("  - Why reproducibility matters")
    print("  - How to achieve perfect reproducibility")
    print("  - What to track for reproducibility")
    print("  - Common pitfalls and solutions")
    
    # Run demonstrations
    demonstrate_reproducibility()
    demonstrate_non_reproducibility()
    demonstrate_version_tracking()
    demonstrate_reproduce_from_record()
    demonstrate_what_breaks_reproducibility()
    
    # Summary
    print("\n" + "="*60)
    print("✅ REPRODUCIBILITY DEMONSTRATION COMPLETE!")
    print("="*60)
    
    print("\n🎯 Key Takeaways:")
    print("  1. Reproducibility = Same inputs → Same outputs")
    print("  2. Track EVERYTHING: code, data, env, hyperparams")
    print("  3. Use version control for all artifacts")
    print("  4. Fix random seeds for deterministic results")
    print("  5. MLOps tools automate reproducibility tracking")
    
    print("\n📁 Files created:")
    print("  - reproducibility/experiment_001.json")
    print("    (Complete record for reproducing this experiment)")
    
    print("\n🚀 Next Steps:")
    print("  - Review the exercises in ../exercises/")
    print("  - Move to Module 02: Environment & Packaging")
    
    print("="*60)


if __name__ == "__main__":
    main()
