# Precision, Recall & F1 Score

## 🎯 Objective

Learn how to evaluate classification models using **Precision, Recall, and F1 Score**.  
The lecture focuses on choosing the right metric based on the cost of False Positives and False Negatives, especially for imbalanced and multiclass datasets.

---

## 📚 Concepts Covered

- Classification Metrics
- Precision
- Recall
- Precision-Recall Trade-off
- F1 Score
- Harmonic Mean
- False Positive and False Negative Costs
- Accuracy on Imbalanced Datasets
- Binary Classification Metrics
- Multiclass Classification Metrics
- Macro Average
- Weighted Average
- Micro Average
- Per-Class Metrics
- `classification_report()`

---

## 🧠 Concept Explanations

### Precision

- **Definition:** Measures how many predicted positive samples are actually positive.
- **Why it matters:** Useful when **False Positives are more costly**.
- **Simple explanation:** "When the model says positive, how often is it correct?"
- **Formula:** `Precision = TP / (TP + FP)`
- **Example:** In spam detection, high precision reduces legitimate emails being incorrectly marked as spam.

### Recall

- **Definition:** Measures how many actual positive samples are correctly identified.
- **Why it matters:** Useful when **False Negatives are more dangerous**.
- **Simple explanation:** "Of all actual positives, how many did the model find?"
- **Formula:** `Recall = TP / (TP + FN)`
- **Example:** In cancer detection, high recall helps minimize missed cancer cases.

### Precision-Recall Trade-off

- **Definition:** Precision and recall often move in opposite directions.
- **Why it matters:** Improving one can reduce the other depending on the model's decision threshold.
- **Simple explanation:** Increasing the number of detected positives may increase recall but can also create more False Positives and reduce precision.
- **Key idea:** Both metrics cannot always be maximized simultaneously.

### F1 Score

- **Definition:** Harmonic mean of Precision and Recall.
- **Why it matters:** Useful when both Precision and Recall are important.
- **Simple explanation:** It rewards models that maintain a good balance between the two metrics.
- **Formula:** `F1 = 2 × (Precision × Recall) / (Precision + Recall)`

### Harmonic Mean

- **Definition:** A type of average that gives more importance to low values.
- **Why it matters:** Prevents a model from receiving a high F1 Score when either Precision or Recall is very low.
- **Example:** Precision = 60% and Recall = 100% gives an F1 Score of 75%, rather than an arithmetic average of 80%.

### Multiclass Classification Metrics

- **Definition:** Metrics calculated separately for each class when there are more than two classes.
- **Why it matters:** A single overall score may hide poor performance on individual classes.
- **Example:** A Dog/Cat/Rabbit classifier calculates Precision, Recall, and F1 Score for each class.

### Macro Average

- **Definition:** Calculates the metric for every class and then takes their simple average.
- **Why it matters:** Gives every class equal importance.
- **Best used when:** Classes have similar numbers of samples.

### Weighted Average

- **Definition:** Calculates metrics for each class and weights them according to class frequency.
- **Why it matters:** Accounts for differences in class sizes.
- **Best used when:** Classes are imbalanced.

### Classification Report

- **Definition:** Scikit-learn's `classification_report()` displays Precision, Recall, F1 Score, and support for each class.
- **Why it matters:** Provides a quick overall view of classification performance.
- **Example:** `classification_report(y_test, y_pred)`

---

## 📌 Key Points

- **Precision → Focus on False Positives.**
- **Recall → Focus on False Negatives.**
- Use Recall when missing a positive case is more dangerous.
- Use Precision when incorrectly predicting a positive case is more costly.
- F1 Score balances Precision and Recall.
- F1 Score uses the **harmonic mean**, so a very low Precision or Recall lowers the score.
- Accuracy can be misleading for highly imbalanced datasets.
- In multiclass classification, calculate metrics for each class.
- **Macro average** treats all classes equally.
- **Weighted average** accounts for class frequency.
- There is no universally "best" classification metric; the correct choice depends on the problem and business consequences.

---

## 🌍 Real-World Applications

- **Cancer detection:** Prioritize Recall to reduce missed cancer cases.
- **Spam detection:** Prioritize Precision to avoid legitimate emails being marked as spam.
- **Fraud detection:** Use Recall when missing fraudulent transactions is costly.
- **Security systems:** High Recall can help detect rare but important threats.
- **Multiclass classification:** Evaluate individual classes in applications such as image and digit recognition.

---

## 🔗 Related Topics

- **Previous:** Accuracy & Confusion Matrix
- **Next:** Multiclass Classification Metrics
- **Related:** Confusion Matrix, TP, TN, FP, FN, Imbalanced Data, Classification Algorithms

---

## ✅ Summary

Precision measures the correctness of positive predictions, while Recall measures how many actual positives were detected.  
The choice between them depends on whether False Positives or False Negatives are more costly.  
F1 Score combines Precision and Recall using the harmonic mean.  
For multiclass problems, metrics can be calculated per class and aggregated using Macro or Weighted averages.  
The most appropriate metric depends on the dataset, model objective, and real-world consequences of errors.