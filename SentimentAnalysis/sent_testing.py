import nltk
import math
import sklearn
from nltk.classify.scikitlearn import SklearnClassifier


def read_file(path):
    with open(path, encoding="UTF-8") as file:
        return file.read().split("\n")


def prepare_data(dataset, scores):
    return_data = []
    j = 0
    for text, score in zip(dataset, scores):
        features = simple_tokens_feature(text, 200)
        features["last"] = last_symbol_feature(text)
        features["punkt"] = punkt_feature(text)
        features["open"] = open_brackets_feature(text)
        features["close"] = close_brackets_feature(text)
        return_data.append((features, score))
        j += 1
    return return_data


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


dataset = read_file("data/texts_train.txt")
scores = read_file("data/scores_train.txt")
feature_set = prepare_data(dataset, scores)
print(feature_set[0])
test_part = round(len(feature_set) * 0.2)
test_set = feature_set[0:test_part]
train_set = feature_set[test_part:]
classifier = SklearnClassifier(sklearn.svm.LinearSVC(max_iter=10000))
classifier.train(train_set)
max_dif = 0
aver_dif = 0
for test in test_set:
    score = classifier.classify(test[0])
    abs = math.fabs(int(score) - int(test[1]))
    print(str(score) + " : " + str(test[1]) + ' | ' + str(abs) + "    " + str(test[0]))
    if abs > max_dif:
        max_dif = abs
    aver_dif += abs
print(max_dif)
print(aver_dif / len(test_set))
