# 🎯 Logistic Regression Hyperparameters in Scikit-Learn

A hands-on reference for every hyperparameter exposed by `sklearn.linear_model.LogisticRegression`, paired with an interactive Streamlit app that lets you tune them and watch the decision boundary move in real time.

> 📂 Part of my **DSMP** notes — Machine Learning → Logistic Regression track.

---

## 📑 Table of Contents

- [Why Hyperparameters Matter](#-why-hyperparameters-matter)
- [Interactive Simulator](#-interactive-simulator)
- [All Hyperparameters at a Glance](#-all-hyperparameters-at-a-glance)
- [Deep Dive: Each Hyperparameter](#-deep-dive-each-hyperparameter)
- [The Math Behind It](#-the-math-behind-it)
- [Solver ↔ Penalty Compatibility](#-solver--penalty-compatibility)
- [Understanding C](#-understanding-c)
- [Multiclass Strategies: OvR vs Multinomial](#-multiclass-strategies-ovr-vs-multinomial)
- [Tuning with GridSearchCV](#-tuning-with-gridsearchcv)
- [Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [Key Takeaways](#-key-takeaways)
- [Credits](#-credits)

---

## 🧠 Why Hyperparameters Matter

Hyperparameters are the knobs you set **before** training starts — unlike the model's coefficients (`coef_`, `intercept_`), which are *learned* from data. In Logistic Regression, these knobs mostly control one thing: **how much the model is allowed to trust the training data versus how much it's forced to stay simple** (regularization).

| Goal | Hyperparameters to Focus On |
|---|---|
| Prevent overfitting | `penalty`, `C` |
| Handle large datasets | `solver`, `n_jobs` |
| Multiclass problems | `multi_class`, `solver` |
| Fix convergence issues | `max_iter`, `tol` |
| Handle imbalanced data | `class_weight` |

---

## 🎮 Interactive Simulator

To actually *feel* what these hyperparameters do to a decision boundary, there's a small Streamlit app that trains a live `LogisticRegression` model on a synthetic 2D dataset and re-draws the boundary every time you change a setting.

> **Credit:** This simulator started as a **CampusX** teaching tool (from their 100 Days of ML series). It's been updated here to work with current scikit-learn releases (the original used the now-removed `multi_class` parameter) — full credit for the original concept and app goes to CampusX. 🙏

**What it does:**
- Lets you pick a **Binary** or **Multiclass** synthetic dataset (`make_blobs`)
- Exposes `penalty`, `C`, `solver`, `max_iter`, multiclass strategy (auto / One-vs-Rest), and `l1_ratio` as sidebar controls
- Trains the model, draws the decision region with `contourf`, and reports test accuracy — all in one click

- 🔗 [**Live demo**](https://hyperparameters-tuning.streamlit.app/)
- 📄 **Source code:** [`main.py`](./main.py)

**Run it locally:**
```bash
pip install streamlit scikit-learn matplotlib numpy
streamlit run app.py
```

---

## 📊 All Hyperparameters at a Glance

`LogisticRegression` has 15+ constructor arguments. Here's the full set as commonly taught  

| Hyperparameter | Type | Default | Description |
|---|---|---|---|
| `penalty` | str | `'l2'` | Regularization type: `'l1'`, `'l2'`, `'elasticnet'`, `None` |
| `dual` | bool | `False` | Dual formulation (only for L2 with `liblinear`) |
| `tol` | float | `1e-4` | Tolerance for stopping criteria |
| `C` | float | `1.0` | Inverse of regularization strength |
| `fit_intercept` | bool | `True` | Whether to fit an intercept term |
| `intercept_scaling` | float | `1.0` | Scaling factor for the intercept (liblinear only) |
| `class_weight` | dict/str | `None` | Weights for classes (`'balanced'` for imbalanced data) |
| `random_state` | int | `None` | Random seed for reproducibility |
| `solver` | str | `'lbfgs'` | Optimization algorithm |
| `max_iter` | int | `100` | Maximum iterations |
| `multi_class` | str | `'auto'` | Multiclass strategy *(now deprecated — see below)* |
| `verbose` | int | `0` | Verbosity level |
| `warm_start` | bool | `False` | Reuse the previous solution as a starting point |
| `n_jobs` | int | `None` | Parallel jobs for OvR *(now deprecated — see below)* |
| `l1_ratio` | float | `None` | Elastic-Net mixing parameter |

---

## 🔍 Deep Dive: Each Hyperparameter

### 1. `penalty` — Regularization Type

Specifies the norm used to penalize large coefficients.

| Value | Name | Effect | Use Case |
|---|---|---|---|
| `'l1'` | Lasso | Sparse models (some coefficients become exactly 0) | Feature selection |
| `'l2'` | Ridge | Shrinks all coefficients evenly, none to exactly 0 | General purpose (default) |
| `'elasticnet'` | Elastic Net | Blend of L1 + L2 | When you want both effects |
| `None` | No penalty | No regularization at all | Small datasets, pure interpretability |

### 2. `C` — Inverse Regularization Strength

Controls the trade-off between fitting the training data tightly and keeping the model simple. It's the inverse of regularization strength λ:

$$\lambda = \frac{1}{C}$$

| C Value | Regularization | Effect |
|---|---|---|
| Small (0.001) | Strong | High bias, low variance — underfitting risk |
| Medium (1.0) | Balanced | Default, moderate regularization |
| Large (1000) | Weak | Low bias, high variance — overfitting risk |

### 3. `solver` — Optimization Algorithm

The algorithm used to minimize the log-loss.

| Solver | Full Name | Best For |
|---|---|---|
| `newton-cg` | Newton Conjugate Gradient | Medium datasets, L2/none penalty |
| `lbfgs` | Limited-memory BFGS | Medium datasets, default choice |
| `liblinear` | Library for Linear Classification | Small datasets, L1/L2 |
| `sag` | Stochastic Average Gradient | Large datasets, L2/none |
| `saga` | SAGA variant | Large datasets, all penalty types |

### 4. `max_iter` — Maximum Iterations

The cap on how many iterations the solver gets to converge. If you see a `ConvergenceWarning`, this is usually the first thing to bump — try 1000 or 10000.

### 5. `multi_class` — Multiclass Strategy

| Value | Strategy | Description |
|---|---|---|
| `'auto'` | Automatic | Picks a strategy based on solver + data |
| `'ovr'` | One-vs-Rest | Trains one binary classifier per class |
| `'multinomial'` | Softmax | A single model handling all classes jointly |

### 6. `l1_ratio` — Elastic Net Mixing

Only used when `penalty='elasticnet'`. Controls the blend between L1 and L2:

$$\text{Penalty} = \rho \cdot L1 + (1-\rho) \cdot L2$$

- `ρ = 0` → pure L2 (Ridge)
- `ρ = 1` → pure L1 (Lasso)
- `ρ = 0.5` → equal mix

### 7. `class_weight` — Handling Imbalanced Data

| Value | Effect |
|---|---|
| `None` | All classes weighted equally |
| `'balanced'` | Weights set inversely proportional to class frequency |
| `{0: 1, 1: 10}` | Custom weight per class |

**`'balanced'` formula:**

$$w_j = \frac{n}{k \cdot n_j}$$

where `n` = total samples, `k` = number of classes, `n_j` = samples in class `j`.

---

## 🧮 The Math Behind It

**Sigmoid function** — squashes any real number into a (0, 1) probability:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

**Probability of class 1** given features $x_1, \dots, x_n$:

$$P(y=1 \mid x) = \sigma(\beta^T x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_n x_n)}}$$

**Log-loss (binary cross-entropy)** — the unregularized objective being minimized:

$$J(\beta) = -\frac{1}{n}\sum_{i=1}^{n}\Big[y_i\log(p_i) + (1-y_i)\log(1-p_i)\Big]$$

**Regularized objective** — this is what `penalty` and `C` actually control:

$$\hat{\beta} = \arg\min_{\beta}\Big[J_0(\beta) + \frac{1}{C}\Omega(\beta)\Big]$$

| Regularization | Penalty term $\Omega(\beta)$ | Properties |
|---|---|---|
| L1 (Lasso) | $\sum_j \lvert \beta_j \rvert$ | Sparse, feature selection, non-differentiable at 0 |
| L2 (Ridge) | $\sum_j \beta_j^2$ | Shrinks smoothly, handles multicollinearity, differentiable everywhere |
| Elastic Net | $\rho\sum_j\lvert\beta_j\rvert + (1-\rho)\sum_j\beta_j^2$ | Combines both, good for correlated features, needs `solver='saga'` |

**Gradient descent update (L2 case):**

$$\nabla J_{L2}(\beta) = \frac{1}{n}X^T(\sigma(X\beta)-y) + \frac{1}{C}\beta$$

$$\beta \leftarrow \beta - \eta\Big[\frac{1}{n}X^T(p-y) + \frac{1}{C}\beta\Big]$$

---

## 🔗 Solver ↔ Penalty Compatibility

| Penalty | newton-cg | lbfgs | liblinear | sag | saga |
|---|---|---|---|---|---|
| none | ✅ | ✅ | ✅ | ✅ | ✅ |
| l1 | ❌ | ❌ | ✅ | ❌ | ✅ |
| l2 | ✅ | ✅ | ✅ | ✅ | ✅ |
| elasticnet | ❌ | ❌ | ❌ | ❌ | ✅ |

**Rule of thumb decision path:**

```
Dataset size?
├── Small/Medium
│   ├── Penalty = L1        → liblinear
│   ├── Penalty = L2/none   → lbfgs
│   └── Penalty = ElasticNet → saga
└── Large
    ├── Penalty = L1        → saga
    ├── Penalty = L2/none   → sag or saga
    └── Penalty = ElasticNet → saga
```

| Solver | Type | Speed | Memory | Best For |
|---|---|---|---|---|
| `newton-cg` | 2nd order | Medium | High | Medium data, precise |
| `lbfgs` | Quasi-Newton | Fast | Low | Default choice |
| `liblinear` | Coordinate descent | Fast | Low | Small data, L1/L2 |
| `sag` | Stochastic | Very fast | Low | Large data |
| `saga` | Stochastic | Very fast | Low | Large data, all penalties |

---

## 🎚 Understanding C

| C Value | λ Value | Regularization | Model Behavior |
|---|---|---|---|
| 0.001 | 1000 | Very Strong | Very simple model, high bias |
| 0.01 | 100 | Strong | Simple model |
| 0.1 | 10 | Moderate | Balanced |
| 1.0 | 1 | Default | Standard regularization |
| 10 | 0.1 | Weak | Complex model |
| 100 | 0.01 | Very Weak | Very complex model, high variance |

**Finding the optimal `C`:** cross-validate over a logarithmic range rather than guessing:

```python
C_values = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
```

---

## 🧩 Multiclass Strategies: OvR vs Multinomial

**One-vs-Rest (OvR):** trains `K` binary classifiers, one per class vs. everyone else.

$$\hat{y} = \arg\max_k P_k(y=k \mid x)$$

**Multinomial (Softmax):** a single model that directly outputs a joint probability distribution over all classes.

$$P(y=k \mid x) = \frac{e^{\beta_k^T x}}{\sum_{j=1}^{K} e^{\beta_j^T x}}$$

| Aspect | One-vs-Rest (OvR) | Multinomial |
|---|---|---|
| Number of models | K binary classifiers | 1 multiclass model |
| Probability sum | May not sum to 1 | Always sums to 1 |
| Supported solvers | All | newton-cg, lbfgs, sag, saga |
| Speed | Parallelizable (`n_jobs`) | Single model |
| Recommended for | Many classes, liblinear | True multiclass problems |

---

## 🛠 Tuning with GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# Load and scale data
iris = load_iris()
X, y = iris.data, iris.target
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define parameter grid
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear', 'saga'],
    'max_iter': [100, 500, 1000]
}

# Grid Search with Cross-Validation
clf = LogisticRegression()
grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_scaled, y)

print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best Accuracy: {grid_search.best_score_:.4f}")
```

---

## 🚧 Common Pitfalls & Fixes

**Issue 1 — `ConvergenceWarning`:** solver didn't converge within `max_iter`.

| Solution | Code Change |
|---|---|
| Increase iterations | `max_iter=1000` or higher |
| Scale features | Use `StandardScaler()` |
| Try a different solver | `solver='saga'` |
| Reduce regularization | Increase `C` |

**Issue 2 — Incompatible solver/penalty:**
```python
# Raises ValueError
LogisticRegression(penalty='l1', solver='lbfgs')
```
→ Check the [compatibility table](#-solver--penalty-compatibility), or let scikit-learn auto-select.

**Issue 3 — Imbalanced classes:** model biased toward the majority class.
```python
clf = LogisticRegression(class_weight='balanced')
```

**Issue 4 — Overfitting** (high train accuracy, low test accuracy):

| Approach | Implementation |
|---|---|
| Increase regularization | Decrease `C` (e.g. 0.01) |
| Use L1 penalty | `penalty='l1'` for feature selection |
| Add more data | Collect more samples |
| Reduce features | Feature selection techniques |

---


## ✅ Key Takeaways

1. **`C` is the single most important hyperparameter** — it controls regularization strength (inverse relationship: small `C` = strong regularization).
2. **Solver selection matters** for both compatibility and performance:
   - `saga` supports every penalty type
   - `liblinear` is a solid pick for small datasets with L1
   - `sag` / `saga` are fast on large datasets
3. **Regularization prevents overfitting:**
   - L1 → sparse models / feature selection
   - L2 → general shrinkage (default)
   - Elastic Net → best of both, when features are correlated
4. **Always scale your features** before fitting Logistic Regression — `sag`/`saga` in particular assume comparable feature scales.
5. **Use cross-validation** (`GridSearchCV`) rather than guessing hyperparameters by hand.

---

## 🙏 Credits

- **Concept notes & original Streamlit simulator:** [CampusX](https://github.com/campusx-official) — 100 Days of Machine Learning series. This README compiles and reorganizes those notes for my own DSMP reference; the simulator code is used with credit and is not my original work.
- **Official reference:** [scikit-learn `LogisticRegression` documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)

---

*Notes compiled by Rushit Tholiya — DSMP / Machine Learning.*