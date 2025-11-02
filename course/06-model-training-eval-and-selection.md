# Module 06: Model Training, Evaluation & Selection

## 🎯 Goals

- Structure **training scripts** for reproducibility
- Implement **cross-validation** and hyperparameter tuning
- Calculate comprehensive **evaluation metrics** (accuracy, precision, recall, F1, AUC-ROC)
- Detect and mitigate **bias** in models
- Compare models systematically and **select the best**
- Create **evaluation reports** with visualizations

---

## 📖 Key Terms

- **Cross-validation**: Technique to assess model performance on different data splits (k-fold)
- **Hyperparameter tuning**: Optimizing model parameters not learned during training
- **Grid search**: Exhaustive search over parameter combinations
- **Random search**: Random sampling of parameter space (more efficient for large spaces)
- **Bias**: Systematic errors in predictions favoring certain groups
- **Fairness metrics**: Demographic parity, equal opportunity, equalized odds
- **Model selection**: Choosing best model based on validation metrics and business requirements

---

## 🎓 Lessons with Transcript

### What We're Doing in This Module

**Welcome to Model Training, Evaluation & Selection!** This is where we move beyond basic model training to systematic, robust evaluation that catches issues before production. We're learning to validate models thoroughly and select winners based on multiple criteria.

### Lesson 1: Cross-Validation - Beyond Single Train-Test Split

**Transcript:**
"When you split data 80-20 for train-test, you're making one random choice that affects your results. What if that particular split happened to give you easy test examples? Your model looks great, but it's actually overfit to that split. Cross-validation solves this by using multiple splits. In 5-fold CV, you split data into 5 parts, train on 4, test on 1, and repeat 5 times with different test folds. You get 5 accuracy scores that you can average and compute standard deviation. This gives you a robust estimate of model performance. If standard deviation is high, your model is unstable. If all 5 scores are good, you have confidence it generalizes."

**What you're learning:** Why cross-validation provides more reliable performance estimates than single splits.

### Lesson 2: Hyperparameter Tuning - Grid vs Random Search

**Transcript:**
"Models have parameters they learn - like weights in neural networks. But they also have hyperparameters you set - learning rate, regularization strength, tree depth. These dramatically affect performance. Grid search tries every combination: learning_rate=[0.01, 0.1, 1.0] times regularization=[0.1, 1.0, 10.0] gives 9 combinations. This is exhaustive but expensive. Random search instead samples random combinations, maybe trying 20 random points. Research shows random search often finds better models faster because it explores the space more broadly. The key is to log every trial to MLflow so you can analyze what worked."

**What you're learning:** How to systematically search hyperparameter space and when to use each approach.

### Lesson 3: Business-Aware Model Selection

**Transcript:**
"Highest accuracy doesn't always mean best model. Imagine a fraud detection model. Model A has 95% accuracy but only catches 60% of fraud. Model B has 93% accuracy but catches 80% of fraud. Which is better? Depends on your business goal. If false positives cost little (just extra checks) but false negatives cost huge (fraud losses), you want high recall - Model B. Model selection must consider business metrics, not just statistical metrics. Also consider inference latency, model size, interpretability requirements. A slightly less accurate model that's 10x faster might be better for real-time serving."

**What you're learning:** How to select models based on business requirements beyond just accuracy.

### Lesson 4: Bias and Fairness Evaluation

**Transcript:**
"Your model might perform well overall but unfairly disadvantage certain groups. A loan approval model might have 90% accuracy but reject 70% of minority applicants while accepting 70% of majority applicants - that's demographic disparity. Fairness metrics like demographic parity check if outcomes are equal across groups. Equal opportunity checks if true positive rates are equal. These aren't just ethical concerns - they're legal requirements in many domains. Use libraries like Fairlearn to compute fairness metrics alongside accuracy. If bias is detected, you may need to rebalance training data, adjust decision thresholds per group, or use debiasing algorithms."

**What you're learning:** How to detect and measure bias in model predictions across demographic groups.

### Lesson 5: Systematic Model Selection Process

**Transcript:**
"Don't eyeball results and pick a model. Use a systematic process. First, filter models by minimum requirements - must meet accuracy threshold, must meet fairness constraints, must meet latency requirements. Second, rank remaining models by primary business metric - maybe F1 score for balanced classification. Third, consider secondary factors - model complexity, interpretability, maintenance burden. Fourth, validate your top candidate on a held-out test set that wasn't used for selection. Finally, document the decision - why this model, what trade-offs were made, what risks remain. This process is reproducible and auditable."

**What you're learning:** How to implement a structured, defensible model selection process.

### Key Definition - What We're Doing Overall

**In this module, we're professionalizing model evaluation.** We're using cross-validation for robust performance estimates. We're tuning hyperparameters systematically with grid or random search. We're evaluating fairness alongside accuracy to catch bias. We're selecting models based on business requirements, not just statistical metrics. And we're documenting decisions for reproducibility and auditability.

**By the end of this lesson, you should understand:** How to implement cross-validation in scikit-learn, how to use GridSearchCV and RandomizedSearchCV for hyperparameter tuning, how to compute fairness metrics with Fairlearn, and how to select models based on multiple criteria. Rigorous evaluation is what separates research experiments from production-ready models - it's where you catch issues before they affect users.

---

## 🔧 Commands First: Structured Training Script

```bash
# Create modular training script
cat > src/train.py << 'EOF'
import argparse
import json
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import numpy as np

def train_and_evaluate(model_type='rf', n_estimators=100, max_depth=5, random_state=42):
    """Train model with given hyperparameters"""
    
    # Load data
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    
    # Initialize model
    if model_type == 'rf':
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
    elif model_type == 'gb':
        model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    # Train on full training set
    model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='macro'),
        'recall': recall_score(y_test, y_pred, average='macro'),
        'f1': f1_score(y_test, y_pred, average='macro'),
        'cv_mean': cv_mean,
        'cv_std': cv_std,
    }
    
    return model, metrics, (X_test, y_test, y_pred)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-type', type=str, default='rf', choices=['rf', 'gb'])
    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--max-depth', type=int, default=5)
    parser.add_argument('--random-state', type=int, default=42)
    args = parser.parse_args()
    
    mlflow.set_experiment("model-selection")
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("model_type", args.model_type)
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_param("random_state", args.random_state)
        
        # Train
        model, metrics, test_data = train_and_evaluate(
            model_type=args.model_type,
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=args.random_state
        )
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Create classification report
        X_test, y_test, y_pred = test_data
        report = classification_report(y_test, y_pred, output_dict=True)
        with open("classification_report.json", "w") as f:
            json.dump(report, f, indent=2)
        mlflow.log_artifact("classification_report.json")
        
        print(f"Model: {args.model_type}")
        print(f"Test Accuracy: {metrics['accuracy']:.3f}")
        print(f"CV Accuracy: {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")

if __name__ == "__main__":
    main()
EOF

# Run training
python src/train.py --model-type rf --n-estimators 100 --max-depth 5
python src/train.py --model-type gb --n-estimators 150 --max-depth 7
```

**Why**: Modular training script with args allows running multiple experiments easily. Cross-validation gives robust performance estimates.

---

## 🔍 Hyperparameter Tuning with Grid Search

```bash
# Create tuning script
cat > src/tune.py << 'EOF'
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
import json

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 5, 10],
}

mlflow.set_experiment("hyperparameter-tuning")

with mlflow.start_run(run_name="grid_search_rf"):
    # Grid search with CV
    clf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1
    )
    grid_search.fit(X_train, y_train)
    
    # Log best params
    best_params = grid_search.best_params_
    for param, value in best_params.items():
        mlflow.log_param(f"best_{param}", value)
    
    # Log best score
    mlflow.log_metric("best_cv_score", grid_search.best_score_)
    mlflow.log_metric("test_accuracy", grid_search.score(X_test, y_test))
    
    # Log best model
    mlflow.sklearn.log_model(grid_search.best_estimator_, "model")
    
    # Save all CV results
    cv_results = grid_search.cv_results_
    with open("cv_results.json", "w") as f:
        json.dump({k: v.tolist() if hasattr(v, 'tolist') else v for k, v in cv_results.items()}, f)
    mlflow.log_artifact("cv_results.json")
    
    print(f"Best params: {best_params}")
    print(f"Best CV score: {grid_search.best_score_:.3f}")

EOF

python src/tune.py
```

**Why**: Grid search systematically explores hyperparameter space. MLflow logs all configs for comparison.

---

## 📊 Comprehensive Evaluation Metrics

```bash
# Create evaluation script
cat > src/evaluate.py << 'EOF'
import mlflow
import matplotlib.pyplot as plt
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, auc, RocCurveDisplay,
    precision_recall_curve, PrecisionRecallDisplay
)
import numpy as np

def evaluate_model(model, X_test, y_test, run_id):
    """Generate comprehensive evaluation artifacts"""
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
    
    with mlflow.start_run(run_id=run_id):
        # 1. Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.title("Confusion Matrix")
        plt.savefig("confusion_matrix.png")
        mlflow.log_artifact("confusion_matrix.png")
        plt.close()
        
        # 2. ROC Curve (for binary/multiclass)
        if y_proba is not None and len(np.unique(y_test)) == 2:
            fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
            roc_auc = auc(fpr, tpr)
            
            plt.figure()
            plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], 'k--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            plt.savefig("roc_curve.png")
            mlflow.log_artifact("roc_curve.png")
            mlflow.log_metric("auc", roc_auc)
            plt.close()
        
        # 3. Feature Importance (if available)
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            plt.figure()
            plt.bar(range(len(importances)), importances)
            plt.xlabel('Feature Index')
            plt.ylabel('Importance')
            plt.title('Feature Importances')
            plt.savefig("feature_importance.png")
            mlflow.log_artifact("feature_importance.png")
            plt.close()
    
    print("Evaluation artifacts logged to MLflow")

# Example usage
# model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
# evaluate_model(model, X_test, y_test, run_id)
EOF
```

**Why**: Visual artifacts (confusion matrix, ROC curve) help understand model behavior beyond scalar metrics.

---

## ⚖️ Bias Detection and Fairness

```bash
# Install fairness toolkit
pip install fairlearn

# Create bias detection script
cat > src/check_bias.py << 'EOF'
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference
from sklearn.metrics import accuracy_score

# Simulated data with sensitive attribute
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'age': np.random.randint(18, 80, n),
    'income': np.random.randint(20000, 150000, n),
    'gender': np.random.choice(['M', 'F'], n),
    'approved': np.random.choice([0, 1], n)
})

# Add bias: males more likely approved
df.loc[df['gender'] == 'M', 'approved'] = np.random.choice([0, 1], sum(df['gender'] == 'M'), p=[0.3, 0.7])
df.loc[df['gender'] == 'F', 'approved'] = np.random.choice([0, 1], sum(df['gender'] == 'F'), p=[0.6, 0.4])

X = df[['age', 'income']]
y = df['approved']
sensitive = df['gender']

X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
    X, y, sensitive, test_size=0.2, random_state=42
)

# Train model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Check fairness metrics
mf = MetricFrame(
    metrics=accuracy_score,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=s_test
)

print("Accuracy by group:")
print(mf.by_group)
print(f"\nDemographic parity difference: {demographic_parity_difference(y_test, y_pred, sensitive_features=s_test):.3f}")
print("Values close to 0 indicate fairness; large values indicate bias")
EOF

python src/check_bias.py
```

**Why**: Detecting bias early prevents discriminatory models. Fairness metrics quantify disparities across groups.

---

## 🏆 Model Selection Strategy

```bash
# Create selection script
cat > src/select_best_model.py << 'EOF'
import mlflow
import pandas as pd

# Set experiment
mlflow.set_experiment("model-selection")

# Get all runs
runs = mlflow.search_runs(experiment_names=["model-selection"])

# Sort by accuracy
runs_sorted = runs.sort_values('metrics.accuracy', ascending=False)

print("Top 5 models by accuracy:")
print(runs_sorted[['params.model_type', 'params.n_estimators', 'params.max_depth', 
                    'metrics.accuracy', 'metrics.f1', 'metrics.cv_mean']].head())

# Select best based on criteria
best_run = runs_sorted.iloc[0]
print(f"\nBest model:")
print(f"  Run ID: {best_run['run_id']}")
print(f"  Model: {best_run['params.model_type']}")
print(f"  Accuracy: {best_run['metrics.accuracy']:.3f}")
print(f"  F1: {best_run['metrics.f1']:.3f}")

# Promote to registry (covered in Module 07)
# mlflow.register_model(f"runs:/{best_run['run_id']}/model", "IrisClassifier")
EOF

python src/select_best_model.py
```

**Why**: Systematic model selection based on multiple criteria. Document selection rationale for governance.

---

## 🧪 Mini-Lab (10 min)

**Goal**: Train multiple models, tune hyperparameters, and select the best.

1. **Train models**:
```bash
mkdir -p ~/mlops-lab-06 && cd ~/mlops-lab-06
# Copy train.py from above
python train.py --model-type rf --n-estimators 50 --max-depth 3
python train.py --model-type rf --n-estimators 100 --max-depth 5
python train.py --model-type gb --n-estimators 100 --max-depth 5
```

2. **Compare in MLflow UI**:
```bash
# Open http://localhost:5000
# Navigate to "model-selection" experiment
# Select all runs, click "Compare"
# Sort by accuracy
```

3. **Get best model**:
```bash
python select_best_model.py
```

**Expected output**: Multiple runs logged, comparison table shows best model with metrics.

---

## ❓ Quiz (5 Questions)

1. **Why use cross-validation?**
   - Answer: Provides robust performance estimate, reduces overfitting to single train/test split.

2. **What is the difference between Grid Search and Random Search?**
   - Answer: Grid Search tries all combinations (exhaustive), Random Search samples randomly (faster for large spaces).

3. **Why check for bias in models?**
   - Answer: Biased models can discriminate against protected groups, causing legal/ethical issues.

4. **What metrics should you consider beyond accuracy?**
   - Answer: Precision, recall, F1, AUC-ROC (for imbalanced data), fairness metrics (for sensitive attributes).

5. **How do you select the best model?**
   - Answer: Balance validation metrics, business requirements, inference speed, interpretability, fairness.

---

## ⚠️ Common Mistakes

1. **Only using accuracy** → Misleading for imbalanced datasets.  
   *Fix*: Use precision, recall, F1, AUC-ROC.

2. **Not using cross-validation** → Overfitting to test set.  
   *Fix*: Always do k-fold CV on training data.

3. **Tuning on test set** → Data leakage, overoptimistic metrics.  
   *Fix*: Use separate validation set or CV, test set only for final evaluation.

4. **Ignoring fairness** → Discriminatory models.  
   *Fix*: Check bias metrics with fairlearn or similar tools.

5. **Not logging failed experiments** → Repeat mistakes.  
   *Fix*: Log all runs to MLflow, including failures and reasons.

---

## 🛠️ Troubleshooting

**Issue**: "Grid search takes too long"  
→ **Root cause**: Too many parameter combinations or large dataset.  
→ **Fix**: Use RandomizedSearchCV, reduce param grid, use `n_jobs=-1` for parallel, or sample data.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Slow hyperparameter tuning"

**Issue**: "Model overfits (high train accuracy, low test)"  
→ **Root cause**: Model too complex, insufficient data, or data leakage.  
→ **Fix*: Simplify model (lower max_depth), add regularization, collect more data, check for leakage.  
→ **See**: `/troubleshooting/triage-matrix.md` row "Model overfitting"

---

## 📚 Key Takeaways

- **Structure training scripts** with command-line args for reproducibility
- **Cross-validation** provides robust performance estimates
- **Hyperparameter tuning** (Grid/Random Search) optimizes model performance
- **Log all experiments** to MLflow for systematic comparison
- **Check bias and fairness** to avoid discriminatory models
- **Select models** based on multiple criteria: metrics, speed, interpretability, fairness

---

## 🚀 Next Steps

- **Module 07**: Register models, stage transitions, and governance with MLflow Registry
- **Module 08**: Serve models via FastAPI, KServe, or BentoML
- **Hands-on**: Complete Churn Predictor training with comprehensive evaluation

---

**[← Module 05](05-pipelines-orchestration.md)** | **[Next: Module 07 →](07-model-registry-and-governance.md)**
