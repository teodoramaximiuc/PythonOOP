import numpy as np
class LogisticRegressionModel:
    threshold = 0.5
    def __init__ (self, learning_rate=0.01, epochs=1000, threshold=0.5):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0
        self.threshold = threshold
    def sigmoid(self, z):
        return 1/(1+np.exp(-z))
    def predict_all(self, X):
        linear_value = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear_value)
    def predict(self, X):
        predictions = self.predict_all(X)
        return (predictions >= self.threshold).astype(int)
    def train(self, X, y):
        num_samples, num_features = X.shape
        self.weights = np.zeros(num_features)
        self.bias = 0
        for _ in range(self.epochs):
            linear_value = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_value)
            dw = (1/num_samples) * np.dot(X.T, (predictions - y))
            db = (1/num_samples) * np.sum(predictions - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
        return self.weights, self.bias

# X = np.array([[1], [2], [3], [4]])
# y = np.array([0, 0, 1, 1])

# model = LogisticRegressionModel()
# model.train(X, y)
# print(model.predict(np.array([[1.5], [3.5]])))