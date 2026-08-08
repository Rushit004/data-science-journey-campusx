# Classification Metrics: Accuracy Score & Confusion Matrix

## 🎯 Objective

Learn how to evaluate classification models using **accuracy, confusion matrices, and error types**.  
The lecture also explains why accuracy can be misleading on imbalanced datasets and introduces better metrics such as precision, recall, and F1-score.

---

## 📚 Concepts Covered

- Classification Metrics
- Accuracy Score
- Binary Classification
- Multiclass Classification
- Confusion Matrix
- True Positive (TP)
- True Negative (TN)
- False Positive (FP)
- False Negative (FN)
- Type I and Type II Errors
- Accuracy Paradox
- Imbalanced Datasets
- Precision, Recall, F1-Score, and ROC-AUC

---

## 🧠 Concept Explanations

### Classification Metrics

- **Definition:** Measures used to evaluate how well a classification model performs.
- **Why it matters:** Model accuracy alone may not represent real-world performance.
- **Simple explanation:** Compare the model's predictions with the actual labels and calculate meaningful performance measures.

### Accuracy Score

- **Definition:** Proportion of total predictions that are correct.
- **Why it matters:** Useful when classes are reasonably balanced and errors have similar importance.
- **Simple explanation:** Out of all predictions, how many did the model get right?
- **Formula:** `Accuracy = (TP + TN) / (TP + TN + FP + FN)`

### Confusion Matrix

- **Definition:** A table comparing actual classes with predicted classes.
- **Why it matters:** Shows exactly what kinds of mistakes the classifier makes.
- **Simple explanation:** Instead of only saying whether a prediction is correct, it tells us *how* it was correct or incorrect.

### TP, TN, FP, FN

- **TP:** Positive class correctly predicted as positive.
- **TN:** Negative class correctly predicted as negative.
- **FP:** Negative class incorrectly predicted as positive; also called a **Type I Error**.
- **FN:** Positive class incorrectly predicted as negative; also called a **Type II Error**.
- **Example:** In disease detection, FN means a diseased patient was incorrectly classified as healthy.

### Multiclass Confusion Matrix

- **Definition:** Confusion matrix used when there are more than two classes.
- **Why it matters:** Shows correct and incorrect predictions for every class.
- **Example:** Digit classification with classes `0–9` produces a `10 × 10` confusion matrix.

### Imbalanced Dataset

- **Definition:** A dataset where one class contains significantly more samples than another.
- **Why it matters:** Accuracy can become highly misleading.
- **Simple explanation:** A model can predict the majority class almost every time and still achieve very high accuracy.
- **Example:** If 99.999% of passengers are non-terrorists, always predicting "not terrorist" gives extremely high accuracy but fails at detecting terrorists.

### Better Classification Metrics

- **Precision:** Of predicted positives, how many were actually positive?
- **Recall:** Of actual positives, how many did the model identify?
- **F1-Score:** Harmonic mean of precision and recall.
- **ROC-AUC:** Measures the model's overall ability to distinguish between classes.

---

## 📌 Key Points

- Accuracy is not always a reliable classification metric.
- Always inspect the **confusion matrix** to understand model errors.
- **FP = Type I Error**, while **FN = Type II Error**.
- Accuracy can be misleading when classes are highly imbalanced.
- Use **precision, recall, and F1-score** when the cost of different errors matters.
- For multiclass problems, the confusion matrix expands to one row and column per class.
- Choose evaluation metrics based on the actual problem, not just the highest score.

---

## 🌍 Real-World Applications

- **Fraud detection:** Identify fraudulent transactions.
- **Disease diagnosis:** Detect patients with a disease.
- **Spam detection:** Separate spam from legitimate emails.
- **Manufacturing:** Detect defective products.
- **Security systems:** Identify rare but important events such as threats.

---

## 🔗 Related Topics

- **Previous:** Classification Basics and Model Prediction
- **Next:** Precision, Recall & F1-Score
- **Related:** Binary Classification, Multiclass Classification, Model Evaluation, Imbalanced Data

---

## ✅ Summary

Classification metrics help determine how effectively a classification model performs.  
Accuracy measures the proportion of correct predictions but can fail on imbalanced datasets.  
A confusion matrix provides a detailed view of TP, TN, FP, and FN predictions.  
Different errors have different consequences, so metric selection should match the problem.  
Precision, recall, and F1-score provide better evaluation when accuracy alone is insufficient.