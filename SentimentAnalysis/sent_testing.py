import nltk


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


dataset = read_file("data/dataset_40757_1.txt")
scores = read_file("data/scores_train.txt")
feature_set = prepare_data(dataset, scores)
print(feature_set[0])
train_set = feature_set[0:round(len(feature_set) * 0.8)]
test_set = feature_set[round(len(feature_set) * 0.8):]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))