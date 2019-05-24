from xml.dom import minidom

import nltk

BANNED = {"PNCT", "UNKN", "LATN", "NUMB", "SYMB"}
SYMBOLS = 5


def parse_xml_for_data(path):
    doc = minidom.parse(path)
    node = doc.documentElement

    texts = node.getElementsByTagName("text")
    texts = [text.getElementsByTagName("paragraph") for text in texts]
    texts = [paragraph for paragraphs in texts for paragraph in paragraphs]
    texts = [paragraph.getElementsByTagName("sentence") for paragraph in texts]
    texts = [sentence for sentences in texts for sentence in sentences]

    return_data = []
    for sentence in texts:
        data_sent = []
        tokens = sentence.getElementsByTagName("token")
        for token in tokens:
            lemma = token.getAttribute("text").lower()
            gram = token.getElementsByTagName("tfr")[0].getElementsByTagName("v")[0].getElementsByTagName("l")[
                0].getElementsByTagName("g")[0].getAttribute("v")
            if gram not in BANNED:
                data_sent.append((lemma, gram))
        if len(data_sent) > 0:
            return_data.append(data_sent)
    return return_data


def prepare_data(text_data):
    features = []
    real_data = []
    for sentence in text_data:
        i = 0
        while i < len(sentence):
            data_row = {}
            word = sentence[i][0]
            prev_word = sentence[i - 1][0] if i > 0 else ""
            label = sentence[i][1]

            for j in range(SYMBOLS):
                data_row["pres" + str(j + 1)] = get_attr(word, j + 1)
            for j in range(SYMBOLS):
                data_row["prev" + str(j + 1)] = get_attr(prev_word, j + 1)

            # data_row["pres_first"] = get_attr(word, 1)
            # data_row["pres_second"] = get_attr(word, 2)
            # data_row["pres_third"] = get_attr(word, 3)
            # data_row["prev_first"] = get_attr(prev_word, 1)
            # data_row["prev_second"] = get_attr(prev_word, 2)
            # data_row["prev_third"] = get_attr(prev_word, 3)

            features.append((data_row, label))
            real_data.append(prev_word + " + " + word)
            i += 1
    return features, real_data


def get_attr(word, i):
    if len(word) >= i:
        return word[-i]
    else:
        return "*"


data = parse_xml_for_data("annot.opcorpora.no_ambig.xml")
feature_set, words_set = prepare_data(data)

k = round(len(feature_set) * 0.8)
train_set = feature_set[0:k]
test_set = feature_set[k:]

classifier = nltk.NaiveBayesClassifier.train(train_set)

words_set = words_set[k:]
for test, words in zip(test_set, words_set):
    prediction = classifier.classify(test[0])
    if not prediction == test[1]:
        print(words + " = " + prediction + " : " + test[1])
print()
print(nltk.classify.accuracy(classifier, test_set))
print()
print(classifier.most_informative_features(20))
