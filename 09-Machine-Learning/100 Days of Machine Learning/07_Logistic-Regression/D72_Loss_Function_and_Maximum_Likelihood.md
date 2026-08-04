# Logistic Regression: From Maximum Likelihood to Binary Cross-Entropy Loss

## 🎯 Objective
This lecture explains why logistic regression needs a real loss function instead of ad-hoc updates, and builds Binary Cross-Entropy step by step from Maximum Likelihood Estimation.

---

## 📚 Concepts Covered
- Limitations of the Perceptron (step function)
- Sigmoid function for probabilistic output
- Why Mean Squared Error fails for classification
- Maximum Likelihood Estimation (MLE)
- Likelihood for classification problems
- Log-Likelihood and numerical stability
- Negative Log-Likelihood
- Deriving Binary Cross-Entropy Loss
- Relationship between BCE, NLL, and Log Loss

---

## 🧠 Concept Explanations

### Perceptron Trick
- Definition: Classifies using a hard step function on `z = w·x + b`.
- Why it matters: The starting point that exposes the need for a probabilistic approach.
- Simple explanation: Outputs only 0 or 1, updates weights only for misclassified points, no sense of confidence.
- Example: A line is randomly pushed toward or away from a misclassified point — with no guarantee of the best boundary.

### Sigmoid Function
- Definition: `σ(z) = 1 / (1 + e^-z)`, squashing any real number into (0, 1).
- Why it matters: Converts a raw linear score into a usable probability.
- Simple explanation: A smooth, differentiable alternative to the step function.
- Example: `σ(z) ≈ 0.7` means the model estimates a 70% chance of class 1.

### Why MSE Fails for Classification
- Definition: MSE measures squared distance between prediction and label.
- Why it matters: Doesn't penalize confident wrong predictions properly, since labels are discrete but outputs are probabilities.
- Simple explanation: Classification needs a loss built around probabilities, not raw error distance.

### Maximum Likelihood Estimation (MLE)
- Definition: Finds the parameters that make the observed data most probable.
- Why it matters: A mathematical way to prove one model is better than another, instead of guessing.
- Simple explanation: Multiply the predicted probability of the *correct* class across all points — higher product means a better model.
- Example: A model assigning higher probabilities to true labels has higher likelihood and wins.

### Log-Likelihood
- Definition: The logarithm of the likelihood, turning a product into a sum.
- Why it matters: Multiplying thousands of small probabilities causes numerical underflow; logs prevent this.
- Simple explanation: `log(a×b) = log(a) + log(b)`, so likelihood becomes a sum of logs — more stable to compute.

### Negative Log-Likelihood (NLL)
- Definition: The negative of log-likelihood (always negative, since probabilities are < 1).
- Why it matters: Optimizers like gradient descent minimize loss, so "maximize likelihood" becomes "minimize NLL."
- Simple explanation: Lower probability assigned to the correct class → higher loss.
- Example: `-log(0.9) ≈ 0.105` (confident & correct) vs `-log(0.1) ≈ 2.303` (confidently wrong).

### Binary Cross-Entropy (BCE) Loss
- Definition: `Loss = -[y·log(ŷ) + (1-y)·log(1-ŷ)]` for each data point.
- Why it matters: One formula that automatically handles both classes.
- Simple explanation: When `y=1`, only `-log(ŷ)` survives; when `y=0`, only `-log(1-ŷ)` survives.
- Example: True label 1, predicted 0.7 → loss ≈ 0.357. True label 0, predicted 0.6 → loss ≈ 0.916.

---

## 📌 Key Points
- Step function → no probabilities, no optimization guarantee.
- Sigmoid gives probabilities, but still needs a real loss function to find the *optimal* boundary.
- MLE = choose the model that makes the observed data most likely.
- Log transform prevents numerical underflow and turns products into sums.
- Negating log-likelihood turns a maximization problem into a minimization problem.
- BCE is convex → gradient descent is guaranteed to find the global minimum.
- Clip predictions near 0 or 1 to avoid `log(0) = -∞`.
- **BCE = Negative Log-Likelihood = Log Loss** — three names, one formula.

---

## 🌍 Real-World Applications
- Spam vs. not-spam email filters
- Medical diagnosis (disease present/absent)
- Credit default / fraud detection
- Output-layer loss for binary classifiers in neural networks

---

## 🔗 Related Topics
- **Previous:** Perceptron algorithm, Sigmoid function fundamentals
- **Next:** Gradient Descent for logistic regression, Softmax & Categorical Cross-Entropy for multiclass problems

---

## ✅ Summary
Logistic regression moves beyond the perceptron's rigid step function by using sigmoid probabilities. Random updates are replaced by Maximum Likelihood Estimation, which mathematically justifies picking the "best" model. Taking the log avoids numerical underflow, and negating it creates a minimization problem suited for gradient descent. Written in terms of the sigmoid output, this negative log-likelihood becomes Binary Cross-Entropy — the standard loss function for binary classification.