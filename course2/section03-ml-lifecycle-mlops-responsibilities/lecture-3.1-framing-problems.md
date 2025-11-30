# Lecture 3.1 – Business Problem → ML Problem (Framing Correctly)

---

## The Most Important Skill

Here's something that took me years to learn:

**The hardest part of ML isn't building models. It's knowing what to build.**

I've seen brilliant data scientists build perfect models that no one uses. Why? Because they solved the wrong problem.

In this lecture, I'll teach you how to frame problems correctly—how to go from "the business has a problem" to "here's what the model should predict."

---

## A Tale of Two Projects

### Project 1: The Failed Success

A retail company wanted to "use AI to increase sales."

The data science team built a recommendation system. It achieved 95% accuracy in predicting what products users would click on.

The model went live. Clicks went up. Sales stayed flat.

Why? Users clicked on recommendations out of curiosity, not purchase intent. The model optimized for the wrong thing.

### Project 2: The Successful Failure

Same company, different approach.

They reframed the problem: "Predict which customers are likely to make a purchase in the next 7 days."

The model "only" achieved 72% accuracy. But when they targeted these customers with promotions, sales increased 15%.

The "worse" model delivered more value.

---

## The Framing Process

Here's my process for framing ML problems:

### Step 1: Start with the Business Outcome

Ask: "What does success look like for the business?"

Bad starting point:
- "We need an ML model"
- "Let's predict something"
- "I want to use deep learning"

Good starting point:
- "We need to reduce customer churn by 10%"
- "We want to increase conversion rate"
- "We need to detect fraud before it costs us money"

### Step 2: Define the Decision

Ask: "What action will someone take based on this prediction?"

No action = no value.

Examples:
- If we predict churn → Call the customer to retain them
- If we predict fraud → Block the transaction
- If we predict demand → Order more inventory

If no one will act on the prediction, don't build the model.

### Step 3: Define the Prediction Target

Ask: "What exactly should the model output?"

Be specific:
- Not "predict churn" → "predict probability of churn in next 30 days"
- Not "predict fraud" → "classify transaction as fraud/not fraud"
- Not "predict sales" → "predict units sold per product per store per day"

### Step 4: Consider the Timeline

Ask: "When do we need the prediction, and about what time frame?"

- How far ahead do we need to predict?
- How often do we need predictions?
- How quickly after requesting?

Example:
- Predict churn 30 days ahead (so we have time to intervene)
- Update predictions weekly
- Response time: can be batch (not real-time)

### Step 5: Define Success Metrics

Ask: "How will we measure if this is working?"

Two types of metrics:
1. **Model metrics**: Accuracy, precision, recall, AUC
2. **Business metrics**: Revenue, cost savings, conversion rate

The business metric is what matters.

---

## Common Framing Patterns

### Classification: Yes or No

"Should we do X for this customer/transaction/item?"

Examples:
- Will this customer churn? (yes/no)
- Is this transaction fraud? (yes/no)
- Will this patient be readmitted? (yes/no)

When to use:
- Discrete outcomes
- Binary decisions
- Filtering or flagging

### Regression: How Much

"How much X will happen?"

Examples:
- How much will this customer spend next month?
- What will be the demand for this product?
- How long will this delivery take?

When to use:
- Continuous outcomes
- Quantitative predictions
- Planning and resource allocation

### Ranking: What Order

"What should we show first?"

Examples:
- Which products should we recommend?
- Which leads should sales call first?
- Which documents are most relevant?

When to use:
- Ordered lists
- Limited attention/resources
- Relative importance matters more than absolute

### Clustering: What Group

"What groups exist in this data?"

Examples:
- What customer segments do we have?
- What types of user behavior patterns exist?
- What are the different failure modes?

When to use:
- Discovery and exploration
- No predefined labels
- Understanding structure

---

## The Churn Example

Let's frame our course project: Customer Churn Prediction.

### Business Problem

"We're losing customers. We want to reduce churn."

### The Decision

"If we know a customer is likely to churn, we can offer them a promotion or have customer success reach out."

### The Prediction

"Predict the probability that a customer will churn in the next 30 days."

Why 30 days?
- Enough time to intervene
- Recent enough to be actionable
- Matches our retention program timeline

### Success Metrics

**Model metrics**:
- Precision at 80%: Of customers we flag, what % actually churn?
- Recall at 70%: Of customers who churn, what % did we catch?

**Business metrics**:
- Reduce churn rate from 5% to 4%
- Cost of retention campaign vs. lifetime value of retained customers

### Data Needed

- Customer demographics
- Usage history
- Support ticket history
- Payment history
- Product usage patterns

### Constraints

- Need predictions by Monday morning for weekly review
- Can handle batch processing (not real-time)
- Must be explainable (stakeholders want to know why)

---

## Questions to Ask Stakeholders

When framing a problem, interview stakeholders:

### About the Problem
1. What problem are you trying to solve?
2. How do you currently solve it (without ML)?
3. What would success look like?
4. How much is this problem costing you?

### About Decisions
5. What will you do with the predictions?
6. Who will use the predictions?
7. How will they use them?
8. What happens if the prediction is wrong?

### About Data
9. What data do you have?
10. How is it collected?
11. How reliable is it?
12. How often is it updated?

### About Constraints
13. How fast do predictions need to be?
14. How often do you need them?
15. Are there any regulatory requirements?
16. What's the budget/timeline?

---

## Red Flags in Problem Framing

Watch out for these:

### "We want to use AI"

Technology looking for a problem. Start with the business need, not the technology.

### "Predict everything"

Too vague. Be specific about what, when, and why.

### "No one will act on it"

If predictions don't change behavior, don't build the model.

### "We don't have data for that"

Check data availability early. No data = no model.

### "100% accuracy required"

Nothing is 100% accurate. Discuss acceptable error rates.

### "We'll figure out the use case later"

Use case should be clear before you start.

---

## From Problem to Requirements

Once framed, document it:

```markdown
# ML Problem Definition: Customer Churn Prediction

## Business Context
- Problem: Losing customers to competitors
- Current process: Manual review of at-risk accounts (limited scale)
- Business impact: Each churned customer costs $X in lost revenue

## Prediction Task
- Target: Probability of churn in next 30 days
- Type: Binary classification (churn / no churn)
- Threshold: Flag customers with >70% churn probability

## Success Metrics
- Model: Precision ≥80%, Recall ≥70%
- Business: Reduce churn rate by 1 percentage point

## Operational Requirements
- Prediction frequency: Weekly (batch)
- Latency: Not time-critical (overnight processing OK)
- Explainability: Required (stakeholders need to understand why)

## Data Sources
- Customer database (demographics)
- Product usage logs (activity)
- Support tickets (complaints)
- Payment history (billing issues)

## Constraints
- Must comply with privacy regulations (no PII in predictions)
- Model must be interpretable (no black box)
- Budget: X hours of data science time
```

---

## Recap

Framing ML problems correctly:

1. **Start with business outcomes** – What does success look like?
2. **Define the decision** – What action will be taken?
3. **Define the prediction** – What exactly will the model output?
4. **Consider timeline** – When and how often?
5. **Define success metrics** – Model AND business metrics

Common patterns:
- Classification (yes/no)
- Regression (how much)
- Ranking (what order)
- Clustering (what group)

Red flags to avoid:
- Solution looking for a problem
- No clear use case
- No available data
- No action tied to predictions

---

## What's Next

Now that you know how to frame ML problems, let's look at the classic ML lifecycle—the steps from raw data to deployed model.

---

**Next Lecture**: [3.2 – The Classic ML Lifecycle (CRISP-DM Style)](lecture-3.2-ml-lifecycle.md)
