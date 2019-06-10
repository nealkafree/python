import re

import nltk
import math
import sklearn

from nltk.classify.scikitlearn import SklearnClassifier

BoW_dictionary = ["###"]
Bow_3symb_dictionary = ["###"]


def read_file(path):
    with open(path, encoding="UTF-8") as file:
        return file.read().split("\n")


def prepare_eval_simple(dataset):
    return_data = []
    for text in dataset:
        features = simple_tokens_feature(text, 200)
        features.update(add_parameters(text))
        return_data.append(features)
    return return_data


def prepare_data_simple(dataset, scores):
    return_data = []
    for text, score in zip(dataset, scores):
        features = simple_tokens_feature(text, 200)
        features.update(add_parameters(text))
        return_data.append((features, score))
    return return_data


def prepare_data_bow(dataset, scores):
    return_data = []
    for text, score in zip(dataset, scores):
        features = bow_features(text)
        features.update(add_parameters(text))
        return_data.append((features, score))
    return return_data


def prepare_data_bow_3symb(dataset, scores):
    return_data = []
    for text, score in zip(dataset, scores):
        features = bow_3symb_features(text)
        features.update(add_parameters(text))
        return_data.append((features, score))
    return return_data


def prepare_bow_dictionary(dataset):
    for text in dataset:
        text = nltk.tokenize.word_tokenize(text)
        for token in text:
            if token not in BoW_dictionary:
                BoW_dictionary.append(token)


def prepare_bow_symb_dictionary(dataset, n):
    reg = '.{' + str(n) + '}'
    dictionary = []
    for text in dataset:
        text_dict = re.findall(reg, text)
        for token in text_dict:
            if token not in dictionary:
                dictionary.append(token)

    return dictionary


def simple_tokens_feature(text, max_len):
    text = nltk.tokenize.word_tokenize(text)
    features = {i: "" for i in range(max_len)}
    i = 0
    for token in text:
        if i >= max_len:
            break
        features[i] = token
        i += 1
    return features


def last_symbol_feature(text):
    if len(text) > 0:
        return text[-1]
    else:
        return ""


def punkt_feature(text):
    c = 0
    for symbol in text:
        if symbol in {".", "!", "?"}:
            c += 1
    return c


def open_brackets_feature(text):
    c = 0
    for symbol in text:
        if symbol == "(":
            c += 1
    return c


def close_brackets_feature(text):
    c = 0
    for symbol in text:
        if symbol == ")":
            c += 1
    return c


def capital_feature(text):
    c = 0
    for symbol in text:
        if symbol.isupper():
            c += 1
    return c


def add_parameters(text):
    parameters = {"last": last_symbol_feature(text), "punkt": punkt_feature(text), "open": open_brackets_feature(text),
                  "close": close_brackets_feature(text), "capital": capital_feature(text)}
    return parameters


def bow_features(text):
    features = {i: 0 for i in range(len(BoW_dictionary))}
    text = nltk.tokenize.word_tokenize(text)
    for token in text:
        i = 0
        while i < len(BoW_dictionary):
            if token == BoW_dictionary[i]:
                break
            i += 1
        if not i == 0 and i in features:
            features[i] += 1
    return features


def bow_3symb_features(text):
    features = {str(i): 0 for i in range(len(Bow_3symb_dictionary))}
    text = re.findall('...', text)
    for token in text:
        i = 0
        while i < len(Bow_3symb_dictionary):
            if token == Bow_3symb_dictionary[i]:
                break
            i += 1
        if not i == 0 and i in features:
            features[str(i)] += 1
    return features


dataset = read_file("data/texts_train.txt")
scores = read_file("data/scores_train.txt")
evaluate = read_file("data/dataset_40757_1.txt")

dataset = prepare_data_simple(dataset, scores)
evaluate = prepare_eval_simple(evaluate)
print("start training...")
classifier = SklearnClassifier(sklearn.svm.LinearSVC(max_iter=10000))
classifier.train(dataset)
print("start evaluating...")
with open("data/answer.txt", 'a', encoding="UTF-8") as file:
    for eval_set in evaluate:
        file.write(classifier.classify(eval_set) + '\n')

# max_dif = 0
# aver_dif = 0
# for test in test_set:
#     score = classifier.classify(test[0])
#     abs = math.fabs(int(score) - int(test[1]))
#     print(str(score) + " : " + str(test[1]) + ' | ' + str(abs) + "    " + str(test[0]))
#     if abs > max_dif:
#         max_dif = abs
#     aver_dif += abs
# print(max_dif)
# print(aver_dif / len(test_set))
