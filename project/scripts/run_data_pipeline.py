"""
Complete Data Engineering Pipeline

This script runs the entire data engineering pipeline from start to finish.
Perfect for beginners to see the complete workflow!

What this does:
1. Loads raw data
2. Performs EDA (Exploratory Data Analysis)
3. Cleans the data
4. Engineers features
5. Preprocesses for ML
6. Trains a simple model
7. Evaluates performance

All with detailed explanations and comments!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

print("="*80)
print("🚀 DATA ENGINEERING PIPELINE FOR BEGINNERS")
print("="*80)
print()

# ============================================================================
# STEP 1: LOAD RAW DATA
# ============================================================================

print("📂 STEP 1: Loading Raw Data")
print("-" * 80)

try:
    df = pd.read_csv('data/raw/customers.csv')
    print(f"✅ Data loaded successfully!")
    print(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n📋 Columns: {', '.join(df.columns)}")
except FileNotFoundError:
    print("❌ Error: data/raw/customers.csv not found!")
    print("💡 Run: python scripts/00_generate_sample_data.py first")
    exit(1)

# ============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================

print("\n" + "="*80)
print("🔍 STEP 2: Exploratory Data Analysis (EDA)")
print("-" * 80)

# 2.1 Basic information
print("\n📊 Dataset Info:")
print(f"  - Total rows: {df.shape[0]:,}")
print(f"  - Total columns: {df.shape[1]}")
print(f"  - Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 2.2 Data types
print("\n📝 Data Types:")
for dtype in df.dtypes.unique():
    cols = df.select_dtypes(include=[dtype]).columns.tolist()
    print(f"  - {dtype}: {len(cols)} columns")

# 2.3 Missing values
print("\n❓ Missing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': missing.index,
    'Missing': missing.values,
    'Percentage': missing_pct.values
})
missing_df = missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False)
if len(missing_df) > 0:
    print(missing_df.to_string(index=False))
else:
    print("  ✅ No missing values!")

# 2.4 Target variable distribution
print("\n🎯 Target Variable Distribution (churned):")
churn_counts = df['churned'].value_counts()
churn_pct = df['churned'].value_counts(normalize=True) * 100
print(f"  - Not Churned (0): {churn_counts[0]:,} ({churn_pct[0]:.1f}%)")
print(f"  - Churned (1): {churn_counts[1]:,} ({churn_pct[1]:.1f}%)")

# 2.5 Save visualizations
print("\n📊 Creating visualizations...")

# Missing data heatmap
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Plot 1: Missing data
if missing.sum() > 0:
    axes[0, 0].bar(range(len(missing[missing > 0])), missing[missing > 0].values)
    axes[0, 0].set_xticks(range(len(missing[missing > 0])))
    axes[0, 0].set_xticklabels(missing[missing > 0].index, rotation=45, ha='right')
    axes[0, 0].set_title('Missing Values by Column')
    axes[0, 0].set_ylabel('Count')
else:
    axes[0, 0].text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
    axes[0, 0].set_title('Missing Values by Column')

# Plot 2: Age distribution
axes[0, 1].hist(df['age'].dropna(), bins=30, edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Age Distribution')
axes[0, 1].set_xlabel('Age')
axes[0, 1].set_ylabel('Frequency')

# Plot 3: Churn distribution
churn_counts.plot(kind='bar', ax=axes[1, 0], color=['green', 'red'], alpha=0.7)
axes[1, 0].set_title('Churn Distribution')
axes[1, 0].set_xlabel('Churned (0=No, 1=Yes)')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_xticklabels(['Not Churned', 'Churned'], rotation=0)

# Plot 4: Subscription type distribution
df['subscription_type'].value_counts().plot(kind='bar', ax=axes[1, 1], alpha=0.7)
axes[1, 1].set_title('Subscription Type Distribution')
axes[1, 1].set_xlabel('Subscription Type')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('outputs/01_eda_overview.png', dpi=100, bbox_inches='tight')
print("  ✅ Saved: outputs/01_eda_overview.png")

# ============================================================================
# STEP 3: DATA CLEANING
# ============================================================================

print("\n" + "="*80)
print("🧹 STEP 3: Data Cleaning")
print("-" * 80)

df_clean = df.copy()
initial_rows = len(df_clean)

# 3.1 Remove duplicates
duplicates = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()
print(f"✅ Removed {duplicates} duplicate rows")

# 3.2 Handle outliers in age
age_before = len(df_clean)
df_clean = df_clean[(df_clean['age'] >= 18) & (df_clean['age'] <= 100)]
age_removed = age_before - len(df_clean)
print(f"✅ Removed {age_removed} rows with invalid ages")

# 3.3 Handle negative support tickets
tickets_before = len(df_clean)
df_clean = df_clean[df_clean['support_tickets'] >= 0]
tickets_removed = tickets_before - len(df_clean)
print(f"✅ Removed {tickets_removed} rows with negative support tickets")

# 3.4 Convert date columns
df_clean['signup_date'] = pd.to_datetime(df_clean['signup_date'])
df_clean['last_login'] = pd.to_datetime(df_clean['last_login'])
print("✅ Converted date columns to datetime")

final_rows = len(df_clean)
print(f"\n📊 Cleaning summary: {initial_rows:,} → {final_rows:,} rows ({initial_rows - final_rows} removed)")

# Save cleaned data
df_clean.to_csv('data/processed/customers_cleaned.csv', index=False)
print("💾 Saved: data/processed/customers_cleaned.csv")

# ============================================================================
# STEP 4: FEATURE ENGINEERING
# ============================================================================

print("\n" + "="*80)
print("⚙️ STEP 4: Feature Engineering")
print("-" * 80)

df_features = df_clean.copy()

# 4.1 Date-based features
print("📅 Creating date-based features...")
df_features['signup_year'] = df_features['signup_date'].dt.year
df_features['signup_month'] = df_features['signup_date'].dt.month
df_features['signup_day_of_week'] = df_features['signup_date'].dt.dayofweek

# Days since last login
df_features['days_since_last_login'] = (
    pd.Timestamp.now() - df_features['last_login']
).dt.days

print("  ✅ Created: signup_year, signup_month, signup_day_of_week, days_since_last_login")

# 4.2 Ratio features
print("\n📐 Creating ratio features...")
df_features['login_frequency'] = df_features['login_count'] / (df_features['days_as_customer'] + 1)
df_features['spend_per_day'] = df_features['total_spent'] / (df_features['days_as_customer'] + 1)
df_features['spend_per_login'] = df_features['total_spent'] / (df_features['login_count'] + 1)
print("  ✅ Created: login_frequency, spend_per_day, spend_per_login")

# 4.3 Binning features
print("\n📊 Creating binned features...")
df_features['age_group'] = pd.cut(
    df_features['age'],
    bins=[0, 25, 35, 45, 55, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '55+']
)

df_features['tenure_group'] = pd.cut(
    df_features['days_as_customer'],
    bins=[0, 90, 180, 365, 730, np.inf],
    labels=['0-3mo', '3-6mo', '6-12mo', '1-2yr', '2yr+']
)
print("  ✅ Created: age_group, tenure_group")

# 4.4 Engagement score
print("\n🎯 Creating engagement score...")
df_features['engagement_score'] = (
    (df_features['login_count'] / df_features['login_count'].max()) * 0.4 +
    (df_features['avg_session_duration'] / df_features['avg_session_duration'].max()) * 0.3 +
    (1 - df_features['days_since_last_login'] / df_features['days_since_last_login'].max()) * 0.3
)
print("  ✅ Created: engagement_score")

print(f"\n📊 Features added: {df_features.shape[1] - df_clean.shape[1]} new columns")

# Save with features
df_features.to_csv('data/processed/customers_with_features.csv', index=False)
print("💾 Saved: data/processed/customers_with_features.csv")

# ============================================================================
# STEP 5: DATA PREPROCESSING FOR ML
# ============================================================================

print("\n" + "="*80)
print("🔧 STEP 5: Data Preprocessing for Machine Learning")
print("-" * 80)

# 5.1 Select features for modeling
print("📋 Selecting features for modeling...")

# Features to use (only numeric features for simplicity)
feature_cols = [
    'age', 'income', 'days_as_customer', 'login_count',
    'avg_session_duration', 'support_tickets', 'total_spent',
    'monthly_charge', 'days_since_last_login', 'login_frequency',
    'spend_per_day', 'spend_per_login', 'engagement_score'
]

# Add one-hot encoded categorical features
df_encoded = pd.get_dummies(
    df_features,
    columns=['gender', 'subscription_type', 'age_group', 'tenure_group'],
    prefix=['gender', 'sub', 'age_grp', 'tenure']
)

# Get all feature columns (numeric + encoded)
all_feature_cols = [col for col in df_encoded.columns if col not in [
    'customer_id', 'country', 'signup_date', 'last_login', 'churned'
]]

X = df_encoded[all_feature_cols]
y = df_encoded['churned']

print(f"  ✅ Selected {len(all_feature_cols)} features")

# 5.2 Split data
print("\n✂️ Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"  ✅ Training set: {X_train.shape[0]:,} samples")
print(f"  ✅ Test set: {X_test.shape[0]:,} samples")
print(f"  ✅ Churn rate (train): {y_train.mean():.1%}")
print(f"  ✅ Churn rate (test): {y_test.mean():.1%}")

# 5.3 Handle missing values
print("\n💧 Handling missing values...")
imputer = SimpleImputer(strategy='median')
imputer.fit(X_train)

X_train_imputed = pd.DataFrame(
    imputer.transform(X_train),
    columns=X_train.columns,
    index=X_train.index
)

X_test_imputed = pd.DataFrame(
    imputer.transform(X_test),
    columns=X_test.columns,
    index=X_test.index
)

print("  ✅ Missing values imputed with median")

# 5.4 Scale features
print("\n📏 Scaling features...")
scaler = StandardScaler()
scaler.fit(X_train_imputed)

X_train_scaled = pd.DataFrame(
    scaler.transform(X_train_imputed),
    columns=X_train_imputed.columns,
    index=X_train_imputed.index
)

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test_imputed),
    columns=X_test_imputed.columns,
    index=X_test_imputed.index
)

print("  ✅ Features standardized (mean=0, std=1)")

# Save preprocessing artifacts
joblib.dump(imputer, 'models/imputer.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("\n💾 Saved preprocessing artifacts:")
print("  - models/imputer.pkl")
print("  - models/scaler.pkl")

# ============================================================================
# STEP 6: TRAIN MODEL
# ============================================================================

print("\n" + "="*80)
print("🤖 STEP 6: Training Machine Learning Model")
print("-" * 80)

print("🏗️ Building Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=20,
    min_samples_leaf=10,
    random_state=42,
    n_jobs=-1
)

print("🚀 Training model...")
model.fit(X_train_scaled, y_train)
print("  ✅ Model trained successfully!")

# Save model
joblib.dump(model, 'models/churn_model.pkl')
print("💾 Saved: models/churn_model.pkl")

# ============================================================================
# STEP 7: EVALUATE MODEL
# ============================================================================

print("\n" + "="*80)
print("📊 STEP 7: Model Evaluation")
print("-" * 80)

# Make predictions
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)
y_test_proba = model.predict_proba(X_test_scaled)[:, 1]

# Calculate metrics
def print_metrics(y_true, y_pred, dataset_name):
    print(f"\n{dataset_name}:")
    print(f"  Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"  Recall:    {recall_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"  F1-Score:  {f1_score(y_true, y_pred, zero_division=0):.4f}")

print("📈 Performance Metrics:")
print_metrics(y_train, y_train_pred, "Training Set")
print_metrics(y_test, y_test_pred, "Test Set")

# Detailed report
print("\n📋 Detailed Classification Report (Test Set):")
print(classification_report(y_test, y_test_pred, target_names=['Not Churned', 'Churned']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix (Test Set)')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig('outputs/02_confusion_matrix.png', dpi=100, bbox_inches='tight')
print("\n💾 Saved: outputs/02_confusion_matrix.png")

# Feature Importance
feature_importance = pd.DataFrame({
    'feature': X_train_scaled.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🔝 Top 15 Most Important Features:")
print(feature_importance.head(15).to_string(index=False))

# Plot feature importance
plt.figure(figsize=(10, 8))
top_features = feature_importance.head(15)
plt.barh(range(len(top_features)), top_features['importance'].values)
plt.yticks(range(len(top_features)), top_features['feature'].values)
plt.xlabel('Importance')
plt.title('Top 15 Feature Importances')
plt.tight_layout()
plt.savefig('outputs/03_feature_importance.png', dpi=100, bbox_inches='tight')
print("💾 Saved: outputs/03_feature_importance.png")

# ============================================================================
# STEP 8: SAVE RESULTS
# ============================================================================

print("\n" + "="*80)
print("💾 STEP 8: Saving Results")
print("-" * 80)

# Save experiment results
results = {
    'timestamp': datetime.now().isoformat(),
    'model_type': 'RandomForestClassifier',
    'n_features': len(all_feature_cols),
    'n_train_samples': len(X_train),
    'n_test_samples': len(X_test),
    'train_churn_rate': float(y_train.mean()),
    'test_churn_rate': float(y_test.mean()),
    'metrics': {
        'train': {
            'accuracy': float(accuracy_score(y_train, y_train_pred)),
            'precision': float(precision_score(y_train, y_train_pred, zero_division=0)),
            'recall': float(recall_score(y_train, y_train_pred, zero_division=0)),
            'f1': float(f1_score(y_train, y_train_pred, zero_division=0))
        },
        'test': {
            'accuracy': float(accuracy_score(y_test, y_test_pred)),
            'precision': float(precision_score(y_test, y_test_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_test_pred, zero_division=0)),
            'f1': float(f1_score(y_test, y_test_pred, zero_division=0))
        }
    },
    'top_features': feature_importance.head(10).to_dict('records')
}

with open('outputs/experiment_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("✅ Saved: outputs/experiment_results.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("🎉 PIPELINE COMPLETE!")
print("="*80)

print("\n📊 Summary:")
print(f"  - Raw data: {initial_rows:,} rows")
print(f"  - Cleaned data: {final_rows:,} rows")
print(f"  - Features created: {len(all_feature_cols)}")
print(f"  - Train samples: {len(X_train):,}")
print(f"  - Test samples: {len(X_test):,}")

print("\n📈 Model Performance (Test Set):")
test_metrics = results['metrics']['test']
print(f"  - Accuracy:  {test_metrics['accuracy']:.1%}")
print(f"  - Precision: {test_metrics['precision']:.1%}")
print(f"  - Recall:    {test_metrics['recall']:.1%}")
print(f"  - F1-Score:  {test_metrics['f1']:.4f}")

print("\n📁 Output Files:")
print("  - data/processed/customers_cleaned.csv")
print("  - data/processed/customers_with_features.csv")
print("  - models/churn_model.pkl")
print("  - models/imputer.pkl")
print("  - models/scaler.pkl")
print("  - outputs/01_eda_overview.png")
print("  - outputs/02_confusion_matrix.png")
print("  - outputs/03_feature_importance.png")
print("  - outputs/experiment_results.json")

print("\n🎓 Congratulations! You've completed your first data engineering pipeline!")
print("\n📚 Next Steps:")
print("  1. Review the visualizations in outputs/")
print("  2. Explore experiment_results.json")
print("  3. Try modifying features and rerunning")
print("  4. Move on to Module 01: MLOps Foundations")

print("\n" + "="*80)
