# Lecture 6.1 – Problems with "One Big Notebook"

---

## The Notebook Trap

Jupyter notebooks are wonderful for exploration. They're interactive, visual, and great for sharing ideas.

But they become a trap when you try to use them for production ML.

Let me show you why.

---

## The Symptoms

You know you have a notebook problem when:

- **Cell order matters**: Run cells out of order and everything breaks
- **Hidden state**: Variables exist from deleted cells
- **3000+ lines**: The notebook is massive and unnavigable
- **Copy-paste everywhere**: Same code in multiple notebooks
- **"final_v2_REAL.ipynb"**: Version control through file names
- **"It worked yesterday"**: Can't reproduce results

---

## Why Notebooks Are Tempting

Notebooks feel productive because:

- **Immediate feedback**: Run a cell, see results
- **Inline visualization**: Plots right there
- **Narrative flow**: Markdown between code
- **Easy sharing**: Send the .ipynb file

This is perfect for:
- Data exploration
- Prototyping ideas
- Teaching/presentations
- One-off analyses

---

## Why Notebooks Fail in Production

### Problem 1: Hidden State

```python
# Cell 1
data = load_data()

# Cell 2
data = data.dropna()

# Cell 3 (you deleted Cell 2 later)
# But data still has the dropna applied!
print(data.shape)  # Works... until you restart
```

When you restart and run all, Cell 3 breaks.

### Problem 2: No Modularity

Everything in one file. No functions. No imports from other files.

```python
# 3000 lines of:
df = pd.read_csv(...)
df['new_col'] = ...
# 100 more transformations
model = RandomForest()
model.fit(X, y)
# etc.
```

Impossible to:
- Test individual pieces
- Reuse code
- Debug issues
- Understand the flow

### Problem 3: No Versioning (Really)

Git can track notebooks, but:
- Notebooks are JSON—diffs are ugly
- Output cells clutter history
- Cell execution count changes every run
- Merge conflicts are nightmares

### Problem 4: Can't Be Scheduled

You can't reliably run a notebook on a schedule:
- Dependencies unclear
- Configuration hardcoded
- No clean entry point
- No error handling

### Problem 5: Testing Is Impossible

How do you write tests for a notebook?
- No functions to test
- State depends on cell order
- Side effects everywhere

---

## A Horror Story

Let me tell you about "The Notebook."

A data scientist built a churn model over six months. The notebook grew to 4,500 lines. It had everything:
- Data loading
- 20 experiments
- Visualizations
- Final model training
- Evaluation
- Some prediction code

When asked to deploy it:

**Day 1**: Try to run top to bottom. Fails at line 200. Missing variable.

**Day 2**: Variable was defined in a deleted cell. Reconstruct it.

**Day 3**: Works locally. Try to run on server. Different pandas version. DataFrame method doesn't exist.

**Day 4**: Fix pandas version. Now sklearn is wrong version.

**Day 5**: All versions fixed. Still fails. A file path is hardcoded to `/Users/john/Desktop/data.csv`.

**Week 2**: Extract code into functions. Realize many experiments left dead code.

**Week 3**: Write tests. Find three bugs in the feature engineering.

**Week 4**: Finally deployable. The data scientist has already moved to another project.

**Total time**: 4 weeks to make 1 notebook production-ready.

---

## The Professional Approach

Instead of notebooks for production:

```
Exploration (Notebook)          Production (Scripts)
────────────────────────────────────────────────────────
Quick experiments               Modular code
Visual debugging                Unit tests
Narrative                       Documentation
One-off                         Repeatable
Interactive                     Automated
```

### The Workflow

1. **Explore in notebook**: Try ideas, visualize, experiment
2. **Identify what works**: What needs to run repeatedly?
3. **Extract to modules**: Move working code to `.py` files
4. **Add tests**: Verify the logic
5. **Create pipeline**: Automate execution
6. **Keep notebook for exploration**: New experiments still in notebooks

---

## What Should Stay in Notebooks

Notebooks are still great for:

- Initial data exploration
- Visualizing results
- Prototyping new features
- Documentation with code examples
- Training/teaching materials
- Quick ad-hoc analyses

The key: **Notebooks for exploration, scripts for production.**

---

## Notebook Best Practices (If You Must)

If you have to use notebooks in production:

### 1. Clear and Linear

- Number your cells
- Run all from scratch before committing
- Clear outputs before committing

### 2. Short and Focused

- One purpose per notebook
- < 200 lines
- Split into multiple notebooks

### 3. Import Don't Define

```python
# Good: Import from modules
from src.features import build_features
from src.models import train_model

# Bad: Define everything in notebook
def build_features(df):
    # 100 lines...
```

### 4. Configuration at Top

```python
# Configuration
DATA_PATH = "data/raw/customers.csv"
MODEL_PARAMS = {"n_estimators": 100}
OUTPUT_PATH = "models/"

# Then use these variables below
```

### 5. Use nbconvert for Execution

```bash
# Run notebook as script
jupyter nbconvert --to notebook --execute notebook.ipynb

# Convert to Python
jupyter nbconvert --to python notebook.ipynb
```

---

## Recap

Notebooks fail in production because:
- Hidden state
- No modularity  
- Version control issues
- Can't be scheduled
- Can't be tested

The solution:
- Use notebooks for exploration
- Extract production code to modules
- Write tests
- Automate with scripts/pipelines

---

## What's Next

Let's look at how to properly structure experiments for reproducibility.

---

**Next Lecture**: [6.2 – Structuring Experiments (Folders, Scripts, Configs)](lecture-6.2-structuring-experiments.md)
