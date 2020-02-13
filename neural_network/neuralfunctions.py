import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))


def j_quadratic(y_pred, y):
    return 0.5 * np.mean((y_pred - y) ** 2)


def j_quadratic_derivative(y, y_pred):
    return (y_pred - y) / len(y)


class Neuron:

    def __init__(self, w1, b1, w2, b2):
        self.w1 = w1
        self.w2 = w2
        self.b1 = b1
        self.b2 = b2
        self.z1 = np.array([[0], [0]])
        self.z2 = np.array([[0]])

    def learn_row(self, x, y):
        y_pred = self.forward_propagation(x)
        self.back_propagation(y, y_pred, x)

    def forward_propagation(self, x):
        self.z1 = self.w1 @ x + self.b1
        a1 = np.array([[np.max(self.z1[0], 0)], sigmoid(self.z1[1])])
        self.z2 = self.w2 @ a1 + self.b2
        a2 = sigmoid(self.z2)
        return a2

    def back_propagation(self, y, y_pred, x):
        del2 = (y_pred - y) * sigmoid_prime(self.z2)
        # self.w2 -= del2
        a_prime = np.array([[1 if self.z1[0] > 0 else 0], sigmoid_prime(self.z1[1])])
        del1 = (self.w2.T @ del2) * a_prime
        print(x[2] * del1[0])
        print(x[2] * del1[1])


w1 = np.array([[0.7, 0.2, 0.7], [0.8, 0.3, 0.6]])
w2 = np.array([[0.2, 0.4]])
b1 = np.array([[0], [0]])
b2 = np.array([[0]])
n = Neuron(w1, b1, w2, b2)
n.learn_row(np.array([[0], [1], [1]]), np.array([[1]]))
