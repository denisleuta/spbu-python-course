# Comparison of the results of the K-Nearest Neighbors (KNN) model using the scikit-learn library and its own implementation
1. Accuracy:
- Native implementation of KNN: 0.9474 (94.74%)
- KNN from the sklearn library: 0.9591 (95.91%)
## Conclusion: The model implemented using the scikit-learn library shows slightly higher accuracy compared to our own implementation. The difference of 1.17% may be due to optimizations implemented in the scikit-learn library, such as a more efficient implementation of the algorithm and additional parameters that can improve the results.

2. Confusion Matrix:
- Own implementation:
[[40  3]
 [ 3 68]]
- KNN from sklearn:
[[57  7]
 [ 0 107]]

## Conclusion:

- True Positives (TP): The sklearn model has more True Positives for both classes (107 vs. 68 for Class 1 and 57 vs. 40 for class 0), which confirms its higher accuracy.
- False Positives (FP): In the implementation using scikit-learn, the number of false positive classifications (7 vs. 3) has increased. This means that the model is more mistaken, considering benign tumors to be malignant.
- False Negatives (FN): The sklearn model made no errors in class 1 classification (FN=0), while our implementation made 3 errors (FN=3).
In general, the sklearn model copes much better with the classification of malignant tumors (class 1), since it did not miss a single case. However, it copes somewhat worse with the classification of benign tumors (class 0), which manifests itself in a greater number of false positives (7 instead of 3).

3. Precision, Recall, and F1-Score:
## Own implementation:
- Precision for class 0: 0.93, for Class 1: 0.96
- Recall for class 0: 0.93, for class 1: 0.96
- F1-Score for class 0: 0.93, for Class 1: 0.96
## KNN from sklearn:
- Precision for class 0: 1.00, for class 1: 0.94
- Recall for class 0: 0.89, for class 1: 1.00
- F1-Score for class 0: 0.94, for Class 1: 0.97

## Conclusion:

- The precision for class 0 in the sklearn model is 1.00, which indicates that the model classifies benign tumors extremely accurately without making false positive errors. While our implementation has a precision of 0.93, which indicates a greater number of false positives.
- The recall for class 1 in the sklearn model is 1.00, which means that all malignant tumors have been correctly classified as malignant. In our implementation, recall for this class is slightly lower (0.96).
F1-Score for class 1 in sklearn is 0.97, which is slightly higher compared to our model (0.96).

4. General conclusion:
- Sklearn KNN showed slightly better accuracy (95.91% vs. 94.74%), as well as significantly better completeness performance (recall) for class 1. The model from sklearn did not allow false negatives (FN = 0), which is extremely important in a medical task where skipping a malignant tumor can have serious consequences.
- However, the sklearn model has large false positives (FP = 7) for benign tumors, which increases the number of false positives.
- Our own implementation showed good classification quality with minimal errors, but was inferior to the model from sklearn in terms of accuracy and efficiency of data processing.

5. Recommendations:
- If it is more important to minimize false positives and improve the accuracy of classification of benign tumors, you can give preference to your own implementation, which has fewer false positive results.
- If the priority is to minimize the omission of malignant tumors, then the sklearn model is preferable, since it more accurately detects malignant tumors without errors.