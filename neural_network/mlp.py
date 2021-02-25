#!/usr/bin/python

# Example of 3-layer neural network (original code: https://github.com/makeyourownneuralnetwork/makeyourownneuralnetwork)
# Dataset: MNIST (short version)
# Original MNIST dataset: http://yann.lecun.com/exdb/mnist/, full dataset in CSV: https://pjreddie.com/projects/mnist-in-csv/

import numpy
import scipy.special  # for the sigmoid (or logistic) function expit()


# neural network class definition
class NeuralNetwork:

    # initialise the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc 
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)  # expit(x) = 1/(1+exp(-x))

    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert_dir inputs proc_list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T  # (inodes, 1)
        targets = numpy.array(targets_list, ndmin=2).T  # (onodes, 1)

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)  # (hnodes, 1)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)  # (hnodes, 1)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)  # (onodes, 1)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)  # (onodes, 1)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs  # (onodes, 1)
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)  # (hnodes, 1)

        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))  # (onodes, hnodes)

        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs))  # (hnodes, inodes)

    # query the neural network
    def query(self, inputs_list):
        # convert_dir inputs proc_list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T  # (inodes, 1)

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)  # (hnodes, 1)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)  # (hnodes, 1)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)  # (onodes, 1)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)  # (onodes, 1)

        return final_outputs


if __name__ == '__main__':

    # number of input, hidden and output nodes
    input_nodes = 784  # number of pixels in 28*28 images
    hidden_nodes = 200
    output_nodes = 10  # number of classes (digits from 0 to 9)

    # learning rate
    learning_rate = 0.2

    # create instance of neural network
    network = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    # load the mnist training groups CSV file into a proc_list
    with open('mnist_dataset/mnist_train_100.csv', 'r') as fin:
        training_data_list = fin.readlines()

    # train the neural network

    # epochs is the number of times the training groups set is used for training
    epochs = 50

    for e in range(epochs):
        # go through all records in the training groups set
        for record in training_data_list:
            # split the record by the ',' commas
            all_values = record.split(',')
            # scale and shift the inputs
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            targets = numpy.zeros(output_nodes) + 0.01
            # all_values[0] is the target label for this record
            targets[int(all_values[0])] = 0.99
            network.train(inputs, targets)

    # load the mnist test groups CSV file into a proc_list
    with open('mnist_dataset/mnist_test_10.csv', 'r') as fin:
        test_data_list = fin.readlines()

    # test the neural network

    # scorecard for how well the network performs, initially empty
    scorecard = []

    # go through all the records in the test groups set
    for record in test_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # correct answer is first value
        correct_label = int(all_values[0])
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # query the network
        outputs = network.query(inputs)
        # the index of the highest value corresponds to the label
        label = numpy.argmax(outputs)
        # append correct or incorrect to proc_list
        if label == correct_label:
            # network's answer matches correct answer, add 1 to scorecard
            scorecard.append(1)
        else:
            # network's answer doesn't match correct answer, add 0 to scorecard
            scorecard.append(0)

    # calculate the performance score, the fraction of correct answers
    scorecard_array = numpy.array(scorecard)
    print('Accuracy =', scorecard_array.sum() / scorecard_array.size)
