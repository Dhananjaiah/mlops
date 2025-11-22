"""
Module 01: Basic ML Workflow

This script demonstrates a simple but complete ML workflow.
It shows all the steps from data to predictions.

Key concepts demonstrated:
- Data preparation
- Model training
- Model evaluation
- Making predictions
- Tracking what we did
"""

import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def setup_directories():
    """Create necessary directories for our workflow."""
    dirs = ['data', 'models', 'metrics', 'predictions']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Created directories: " + ", ".join(dirs))


def generate_sample_data(n_samples=1000):
    """
    Generate sample customer data for churn prediction.
    
    In a real project, this would be replaced with actual data loading.
    """
    print(f"\n📊 Generating {n_samples} sample records...")
    
    np.random.seed(42)  # For reproducibility
    
    # Generate features
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 70, n_samples),
        'tenure_months': np.random.randint(1, 72, n_samples),
        'monthly_charges': np.random.uniform(20, 120, n_samples),
        'total_charges': np.random.uniform(100, 5000, n_samples),
        'num_products': np.random.randint(1, 5, n_samples),
        'has_support_tickets': np.random.randint(0, 2, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate target (churn) based on features
    # Customers are more likely to churn if:
    # - They have support tickets
    # - They have low tenure
    # - They have high charges
    churn_probability = (
        (df['has_support_tickets'] * 0.3) +
        (df['tenure_months'] < 12) * 0.3 +
        (df['monthly_charges'] > 80) * 0.2
    )
    df['churned'] = (np.random.random(n_samples) < churn_probability).astype(int)
    
    # Save raw data
    df.to_csv('data/customers.csv', index=False)
    print(f"✅ Generated data with {df['churned'].sum()} churned customers")
    print(f"   Churn rate: {df['churned'].mean():.1%}")
    
    return df


def prepare_features(df):
    """
    Prepare features for model training.
    
    This step:
    - Selects relevant features
    - Handles missing values (if any)
    - Creates derived features
    """
    print("\n🔧 Preparing features...")
    
    # Select feature columns
    feature_cols = [
        'age', 'tenure_months', 'monthly_charges',
        'total_charges', 'num_products', 'has_support_tickets'
    ]
    
    X = df[feature_cols]
    y = df['churned']
    
    # Create a derived feature: average charge per month
    X['avg_charge_per_month'] = X['total_charges'] / (X['tenure_months'] + 1)
    
    print(f"✅ Prepared {len(X.columns)} features:")
    for col in X.columns:
        print(f"   - {col}")
    
    return X, y


def split_data(X, y, test_size=0.2):
    """Split data into train and test sets."""
    print(f"\n✂️  Splitting data (test_size={test_size})...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    print(f"✅ Train set: {len(X_train)} samples")
    print(f"✅ Test set: {len(X_test)} samples")
    print(f"   Train churn rate: {y_train.mean():.1%}")
    print(f"   Test churn rate: {y_test.mean():.1%}")
    
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """Train a Random Forest classifier."""
    print("\n🤖 Training Random Forest model...")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    print("✅ Model trained successfully!")
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance."""
    print("\n📊 Evaluating model...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print("\n📋 Detailed Classification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Not Churned', 'Churned'],
        digits=4
    ))
    
    return accuracy, y_pred


def save_artifacts(model, accuracy, feature_names):
    """
    Save all artifacts from this run.
    
    This is a key MLOps practice: track everything!
    """
    print("\n💾 Saving artifacts...")
    
    # Save model
    import joblib
    model_path = 'models/churn_model.pkl'
    joblib.dump(model, model_path)
    print(f"✅ Saved model: {model_path}")
    
    # Save metrics
    metrics = {
        'accuracy': float(accuracy),
        'timestamp': datetime.now().isoformat(),
        'model_type': 'RandomForestClassifier',
        'n_features': len(feature_names),
        'feature_names': feature_names
    }
    
    metrics_path = 'metrics/run_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Saved metrics: {metrics_path}")
    
    # Save run info
    run_info = {
        'run_id': f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'status': 'success',
        'model_path': model_path,
        'metrics_path': metrics_path,
    }
    
    run_info_path = 'metrics/run_info.json'
    with open(run_info_path, 'w') as f:
        json.dump(run_info, f, indent=2)
    print(f"✅ Saved run info: {run_info_path}")


def demonstrate_predictions(model, X_test):
    """Show how to make predictions on new data."""
    print("\n🔮 Making predictions on new data...")
    
    # Take first 5 samples
    sample_data = X_test.head(5)
    predictions = model.predict(sample_data)
    probabilities = model.predict_proba(sample_data)
    
    print("\nSample Predictions:")
    print("-" * 60)
    for i, (idx, row) in enumerate(sample_data.iterrows()):
        pred = "WILL CHURN" if predictions[i] == 1 else "will not churn"
        prob = probabilities[i][1] * 100
        print(f"Customer {i+1}:")
        print(f"  Age: {row['age']}, Tenure: {row['tenure_months']} months")
        print(f"  Prediction: {pred} (probability: {prob:.1f}%)")
        print()


def main():
    """Main workflow function."""
    print("="*60)
    print(" " * 10 + "🚀 ML WORKFLOW DEMONSTRATION")
    print("="*60)
    
    # Step 1: Setup
    setup_directories()
    
    # Step 2: Generate/Load Data
    df = generate_sample_data(n_samples=1000)
    
    # Step 3: Prepare Features
    X, y = prepare_features(df)
    
    # Step 4: Split Data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Step 5: Train Model
    model = train_model(X_train, y_train)
    
    # Step 6: Evaluate Model
    accuracy, y_pred = evaluate_model(model, X_test, y_test)
    
    # Step 7: Save Everything
    save_artifacts(model, accuracy, list(X.columns))
    
    # Step 8: Demonstrate Predictions
    demonstrate_predictions(model, X_test)
    
    # Summary
    print("\n" + "="*60)
    print("✅ WORKFLOW COMPLETE!")
    print("="*60)
    print("\n📚 Key Takeaways:")
    print("  1. ML workflow has many steps, not just training")
    print("  2. Every step produces artifacts (data, model, metrics)")
    print("  3. Tracking artifacts enables reproducibility")
    print("  4. This is just the beginning - MLOps adds much more!")
    print("\n🔍 Generated files:")
    print("  - data/customers.csv      (raw data)")
    print("  - models/churn_model.pkl  (trained model)")
    print("  - metrics/run_metrics.json (performance metrics)")
    print("  - metrics/run_info.json    (run information)")
    print("\n📖 Next: Check out 02_artifact_tracking.py")
    print("="*60)


if __name__ == "__main__":
    main()
