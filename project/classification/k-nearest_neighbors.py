import numpy as np
from collections import Counter
from sklearn.datasets import load_breast_cancer  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore
from sklearn.metrics import confusion_matrix, classification_report  # type: ignore


def euclidean_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """
    Calculate the Euclidean distance between two points.

    Args:
        point1 (np.ndarray): The first point.
        point2 (np.ndarray): The second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return np.sqrt(np.sum((point1 - point2) ** 2))


class KNN:
    def __init__(self, k: int = 3):
        """
        Initialize the KNN classifier.

        Args:
            k (int): The number of neighbors to use for classification.
        """
        self.k = k
        self.X_train: np.ndarray = np.empty((0,))
        self.y_train: np.ndarray = np.empty((0,))

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Fit the KNN classifier to the training data.

        Args:
            X_train (np.ndarray): Training feature dataset.
            y_train (np.ndarray): Training labels.
        """
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict the class labels for the provided test data.

        Args:
            X_test (np.ndarray): Test feature dataset.

        Returns:
            np.ndarray: Predicted class labels for the test data.
        """
        predictions = [self._predict(x) for x in X_test]
        return np.array(predictions)

    def _predict(self, x: np.ndarray) -> int:
        """
        Predict the class label for a single test instance.

        Args:
            x (np.ndarray): A single test instance.

        Returns:
            int: Predicted class label for the instance.
        """
        distances = [euclidean_distance(x, x_train) for x_train in self.X_train]

        k_indices = np.argsort(distances)[: self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]

        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def score(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """
        Calculate the accuracy of the classifier on test data.

        Args:
            X_test (np.ndarray): Test feature dataset.
            y_test (np.ndarray): True labels for the test dataset.

        Returns:
            float: Accuracy of the classifier on the test data.
        """
        predictions = self.predict(X_test)
        accuracy = np.mean(predictions == y_test)
        return accuracy


# Load dataset and prepare data
data = load_breast_cancer()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and fit KNN classifier
knn = KNN(k=5)
knn.fit(X_train, y_train)

# Calculate accuracy and print results
accuracy = knn.score(X_test, y_test)
print(f"Accuracy of KNN: {accuracy:.4f}")

y_pred = knn.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
