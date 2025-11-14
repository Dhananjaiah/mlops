"""
Generate Sample Customer Churn Data

This script creates realistic customer data for practicing data engineering and MLOps.
Perfect for beginners who want to learn with actual data!

What this does:
- Creates 10,000 fake customer records
- Includes realistic features: age, income, usage patterns
- Adds some messiness: missing values, outliers (like real data!)
- Saves to CSV for practice

Libraries used:
- pandas: For creating and saving dataframes
- numpy: For random number generation
- faker: For generating realistic names, emails, etc.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
# This ensures we get the same "random" data every time we run the script
np.random.seed(42)
random.seed(42)

print("🚀 Generating sample customer churn data...")

# ============================================================================
# STEP 1: Define the number of customers
# ============================================================================
n_customers = 10000
print(f"📊 Creating {n_customers} customer records...")

# ============================================================================
# STEP 2: Generate Customer IDs
# ============================================================================
# Simple sequential IDs: CUST_0001, CUST_0002, etc.
customer_ids = [f"CUST_{str(i).zfill(4)}" for i in range(1, n_customers + 1)]

# ============================================================================
# STEP 3: Generate Customer Demographics
# ============================================================================

# Age: Normally distributed around mean=40, with some realistic spread
ages = np.random.normal(loc=40, scale=15, size=n_customers)
ages = np.clip(ages, 18, 80).astype(int)  # Keep between 18-80

# Gender: Roughly 50/50 split
genders = np.random.choice(['M', 'F', 'Other'], size=n_customers, p=[0.48, 0.48, 0.04])

# Income: Log-normal distribution (more lower incomes, fewer high earners)
incomes = np.random.lognormal(mean=10.5, sigma=0.5, size=n_customers)
incomes = np.round(incomes).astype(int)

# Country: Weighted distribution (more US customers)
countries = np.random.choice(
    ['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'India', 'Japan'],
    size=n_customers,
    p=[0.4, 0.15, 0.1, 0.1, 0.08, 0.07, 0.05, 0.05]
)

# ============================================================================
# STEP 4: Generate Account Information
# ============================================================================

# Signup date: Random dates in the last 5 years
start_date = datetime.now() - timedelta(days=5*365)
signup_dates = [
    start_date + timedelta(days=random.randint(0, 5*365))
    for _ in range(n_customers)
]

# Days as customer (calculated from signup date)
days_as_customer = [(datetime.now() - date).days for date in signup_dates]

# Subscription type
subscription_types = np.random.choice(
    ['Basic', 'Standard', 'Premium', 'Enterprise'],
    size=n_customers,
    p=[0.5, 0.3, 0.15, 0.05]
)

# Monthly charges based on subscription type
subscription_charges = {
    'Basic': 9.99,
    'Standard': 19.99,
    'Premium': 39.99,
    'Enterprise': 99.99
}
monthly_charges = [subscription_charges[sub] for sub in subscription_types]

# ============================================================================
# STEP 5: Generate Usage Patterns
# ============================================================================

# Login count: More logins for engaged customers
login_counts = np.random.poisson(lam=50, size=n_customers)

# Last login: Recent for active users, older for inactive
last_login_days_ago = np.random.exponential(scale=30, size=n_customers)
last_login_days_ago = np.clip(last_login_days_ago, 1, 365).astype(int)
last_login_dates = [datetime.now() - timedelta(days=int(days)) for days in last_login_days_ago]

# Session duration: Average time spent per session (in minutes)
avg_session_duration = np.random.gamma(shape=2, scale=15, size=n_customers)
avg_session_duration = np.clip(avg_session_duration, 1, 120)

# Support tickets: Most customers have few, some have many
support_tickets = np.random.negative_binomial(n=1, p=0.7, size=n_customers)

# Total spent: Based on months as customer and monthly charge
months_as_customer = np.array(days_as_customer) / 30
total_spent = months_as_customer * np.array(monthly_charges)
total_spent = total_spent * np.random.uniform(0.8, 1.2, size=n_customers)  # Add some variance

# ============================================================================
# STEP 6: Generate Target Variable (Churned)
# ============================================================================

# Create churn probability based on multiple factors
# This simulates real-world churn patterns

churn_probability = 0.1  # Base 10% churn rate

# Factors that increase churn probability:
churn_scores = np.zeros(n_customers)

# 1. Low engagement (few logins) increases churn
churn_scores += (login_counts < 20) * 0.2

# 2. High support tickets increase churn
churn_scores += (support_tickets > 5) * 0.15

# 3. Long time since last login increases churn
churn_scores += (last_login_days_ago > 60) * 0.25

# 4. Lower tier subscriptions have higher churn
churn_scores += (subscription_types == 'Basic') * 0.1

# 5. Shorter customer tenure has higher churn
churn_scores += (np.array(days_as_customer) < 90) * 0.2

# Convert scores to probabilities and generate actual churn
churn_probabilities = np.clip(churn_scores, 0, 0.8)
churned = np.random.binomial(1, churn_probabilities)

print(f"✅ Churn rate: {churned.mean():.2%}")

# ============================================================================
# STEP 7: Create the DataFrame
# ============================================================================

df = pd.DataFrame({
    'customer_id': customer_ids,
    'age': ages,
    'gender': genders,
    'income': incomes,
    'country': countries,
    'signup_date': signup_dates,
    'days_as_customer': days_as_customer,
    'subscription_type': subscription_types,
    'monthly_charge': monthly_charges,
    'login_count': login_counts,
    'last_login': last_login_dates,
    'avg_session_duration': avg_session_duration,
    'support_tickets': support_tickets,
    'total_spent': total_spent,
    'churned': churned
})

# ============================================================================
# STEP 8: Add Some Realistic Messiness
# ============================================================================

print("🔧 Adding realistic data issues...")

# Add missing values (like real data!)
# 5% missing in income
missing_income_idx = np.random.choice(df.index, size=int(0.05 * n_customers), replace=False)
df.loc[missing_income_idx, 'income'] = np.nan

# 3% missing in last_login
missing_login_idx = np.random.choice(df.index, size=int(0.03 * n_customers), replace=False)
df.loc[missing_login_idx, 'last_login'] = pd.NaT

# 2% missing in avg_session_duration
missing_session_idx = np.random.choice(df.index, size=int(0.02 * n_customers), replace=False)
df.loc[missing_session_idx, 'avg_session_duration'] = np.nan

# Add some duplicate records (1%)
n_duplicates = int(0.01 * n_customers)
duplicate_idx = np.random.choice(df.index, size=n_duplicates, replace=False)
df_duplicates = df.loc[duplicate_idx].copy()
df = pd.concat([df, df_duplicates], ignore_index=True)

# Add some outliers
# Impossible ages
outlier_idx = np.random.choice(df.index, size=5, replace=False)
df.loc[outlier_idx, 'age'] = np.random.choice([150, 200, 5, 10])

# Negative support tickets (data entry errors)
outlier_idx = np.random.choice(df.index, size=3, replace=False)
df.loc[outlier_idx, 'support_tickets'] = -1

print(f"✅ Added messiness:")
print(f"   - Missing values: {df.isnull().sum().sum()} total")
print(f"   - Duplicate rows: {n_duplicates}")
print(f"   - Outliers: 8 records")

# ============================================================================
# STEP 9: Save the Data
# ============================================================================

output_path = 'data/raw/customers.csv'
df.to_csv(output_path, index=False)

print(f"\n✅ Data generated successfully!")
print(f"📁 Saved to: {output_path}")
print(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n📋 Column names:")
for col in df.columns:
    print(f"   - {col}")

# Display sample
print(f"\n👀 First 5 rows:")
print(df.head())

# Summary statistics
print(f"\n📈 Summary statistics:")
print(df.describe())

print("\n🎉 Ready to start your data engineering journey!")
print("\n📚 Next steps:")
print("   1. Run: python scripts/01_eda.py")
print("   2. Explore the data and visualizations")
print("   3. Clean and engineer features")
