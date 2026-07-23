# ML System Design Framework

## 🎯 Objective
This lecture teaches a structured 7-step framework for designing real-world ML systems, using Netflix's churn prediction problem as a running case study to show how a business goal becomes a deployable ML solution.

---

## 📚 Concepts Covered
- Translating a business problem into an ML problem
- Identifying the correct ML problem type (classification, regression, clustering, etc.)
- Establishing a baseline before building a model
- Data collection strategy and data architecture
- Choosing the right ML and business metrics
- Online vs batch vs hybrid prediction deployment
- Validating assumptions and avoiding common pitfalls
- End-to-end system architecture and MLOps
- Iterative model development workflow
- Production monitoring considerations

---

## 🧠 Concept Explanations

### Business Problem to ML Problem
- **Definition:** The process of converting a vague business goal into a well-defined, measurable ML task.
- **Why it matters:** A poorly framed problem leads to a model that technically works but doesn't solve the actual business need.
- **Simple explanation:** Instead of just saying "reduce churn," you define it as "predict the probability a user cancels their subscription."
- **Example:** Netflix reframes "reduce churn" into a binary classification task with churn (yes/no) as the target variable.

### Type of Problem
- **Definition:** Categorizing the task as supervised, unsupervised, or reinforcement learning, and further into classification, regression, clustering, etc.
- **Why it matters:** The problem type determines which algorithms, data labels, and evaluation metrics are appropriate.
- **Simple explanation:** Ask "do I have labeled outcomes?" and "am I predicting a category or a number?" to narrow down the type.
- **Example:** Churn prediction is supervised binary classification, since past churn labels exist and the output is yes/no.

### Baseline (Current Solution)
- **Definition:** A simple existing benchmark (rule-based, statistical, or basic ML) used to measure whether a new model actually improves things.
- **Why it matters:** Without a baseline, it's impossible to prove that a complex ML model adds real value.
- **Simple explanation:** Start simple — like "flag users inactive for 30+ days" — before building anything advanced.

### Getting Data
- **Definition:** Identifying what signals to collect (watch time, failed searches, incomplete viewing, recommendation clicks) and how they flow through systems like OLTP databases, data warehouses, and event logs.
- **Why it matters:** Good features come from thoughtful data collection, not just whatever is easiest to grab.
- **Simple explanation:** Real-time data (OLTP) captures current activity, while data warehouses hold historical patterns for deeper analysis.

### Metrics to Measure
- **Definition:** A combination of ML metrics (precision, recall, F1, AUC-ROC) and business metrics (churn rate, ROI, customer lifetime value).
- **Why it matters:** High model accuracy alone doesn't guarantee business impact — both angles must be tracked together.
- **Simple explanation:** Precision tells you how many flagged churners were correct; recall tells you how many actual churners you caught.

### Online vs Batch Prediction
- **Definition:** Batch prediction scores all users on a schedule (e.g., daily), while online prediction scores a single user instantly in real time.
- **Why it matters:** Choosing the wrong deployment style leads to unnecessary cost or unacceptable delay.
- **Simple explanation:** Batch is like mailing a monthly report; online is like getting an instant reply while chatting.
- **Example:** Netflix uses a hybrid model — daily batch scores for email campaigns and real-time online scoring for in-app offers.

### Assumption Validation & Pitfalls
- **Definition:** Checking assumptions (data representativeness, feature availability at prediction time, future resembling past) before trusting a model.
- **Why it matters:** Unvalidated assumptions cause silent failures like data leakage, selection bias, or class imbalance in production.
- **Simple explanation:** Always ask "could this assumption break, and what happens if it does?"

---

## 📌 Key Points
- Always translate business goals into a measurable ML target variable before modeling.
- Supervised classification needs labeled historical data; unsupervised methods don't.
- Baselines define the minimum bar a new model must beat to justify its cost.
- Combine ML metrics (precision/recall/F1) with business metrics (ROI, churn rate) for full evaluation.
- Batch prediction suits scheduled bulk scoring; online prediction suits instant, per-user decisions.
- Data leakage, selection bias, and class imbalance are the most common pitfalls to guard against.
- A full ML system includes data pipelines, feature stores, model training, serving, and monitoring — not just the model itself.
- Production systems need continuous monitoring for performance drift, data quality, and business impact.

---

## 🌍 Real-World Applications
- Subscription platforms (Netflix, Spotify) predicting and preventing customer churn
- E-commerce fraud detection using anomaly detection frameworks
- Recommendation systems personalizing content based on engagement features
- Retention campaign optimization using ROI-driven business metrics

---

## 🔗 Related Topics
- **Previous:** Data science tool setup (Anaconda, Jupyter, Colab) and foundational EDA/feature engineering skills
- **Next:** Model building techniques (logistic regression, random forest, XGBoost) and MLOps deployment practices

---

## ✅ Summary
This lecture introduces a repeatable 7-step framework for designing ML systems: translate the business problem, identify the ML problem type, set a baseline, plan data collection, define metrics, choose a deployment strategy, and validate assumptions. Using Netflix's churn prediction as an example, it shows how a business goal like "reduce churn" becomes a supervised classification task measured by precision, recall, and ROI. The lecture also emphasizes production concerns like batch vs online serving, common pitfalls like data leakage, and continuous monitoring after deployment.