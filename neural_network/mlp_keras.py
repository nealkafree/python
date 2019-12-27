#!/usr/bin/python

# Example of 3-layer neural network (original code: https://github.com/makeyourownneuralnetwork/makeyourownneuralnetwork)
# Dataset: MNIST (full version)
# Original MNIST dataset: http://yann.lecun.com/exdb/mnist/, full dataset in CSV: https://pjreddie.com/projects/mnist-in-csv/

from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils import to_categorical

import numpy
from numpy import genfromtxt


def load_data_from_cloud():
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    print('Training set size:', train_images.shape)
    print('Test set size:', test_images.shape)

    train_images = train_images.reshape((60000, 28 * 28))
    train_images = train_images.astype('float32') / 255
    test_images = test_images.reshape((10000, 28 * 28))
    test_images = test_images.astype('float32') / 255

    print('Training set size (updated):', train_images.shape)
    print('Test set size (updated):', test_images.shape)

    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    print('Training labels shape:', train_labels.shape)
    print('Test labels shape:', test_labels.shape)

    return train_images, train_labels, test_images, test_labels


def load_data_from_file(filename):
    data = genfromtxt(filename, delimiter=',')
    labels = to_categorical(data[:, 0])
    data = data[:, 1:]
    return (numpy.asfarray(data) / 255.0 * 0.99) + 0.01, labels


def train_full():
    # Load full version of the dataset
    train_images, train_labels, test_images, test_labels = load_data_from_cloud()

    network = models.Sequential()
    network.add(layers.Dense(784, activation='sigmoid', input_shape=(28 * 28,)))
    network.add(layers.Dense(200, activation='sigmoid', input_shape=(28 * 28,)))
    network.add(layers.Dense(10, activation='sigmoid'))
    network.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

    network.fit(train_images, train_labels, epochs=7, batch_size=50, shuffle=True)

    test_loss, test_acc = network.evaluate(test_images, test_labels)
    print('test_acc:', test_acc, 'test_loss', test_loss)


def train_short():
    # Load short version of the dataset
    trainfile = 'mnist_dataset/mnist_train_100.csv'
    testfile = 'mnist_dataset/mnist_test_10.csv'
    train_images, train_labels = load_data_from_file(trainfile)
    test_images, test_labels = load_data_from_file(testfile)

    network = models.Sequential()
    network.add(layers.Dense(784, activation='sigmoid', input_shape=(28 * 28,)))
    network.add(layers.Dense(200, activation='sigmoid', input_shape=(28 * 28,)))
    network.add(layers.Dense(10, activation='sigmoid'))
    network.compile(optimizer='adam',
                    loss='mean_squared_error',
                    metrics=['accuracy'])

    network.fit(train_images, train_labels, epochs=5, batch_size=1)

    test_loss, test_acc = network.evaluate(test_images, test_labels)
    print('test_acc:', test_acc, 'test_loss', test_loss)


if __name__ == '__main__':
    train_full()

    # train_short()
