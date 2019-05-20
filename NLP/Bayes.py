from xml.dom import minidom

import nltk

BANNED = {"PNCT", "UNKN", "LATN", "NUMB", "SYMB"}


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
    return_data = []
    for sentence in text_data:
        i = 0
        while i < len(sentence):
            data_row = {}
            word = sentence[i][0]
            prev_word = sentence[i - 1][0] if i > 0 else ""
            label = sentence[i][1]

            data_row["pres_first"] = get_attr(word, 1)
            data_row["pres_second"] = get_attr(word, 2)
            data_row["pres_third"] = get_attr(word, 3)
            data_row["prev_first"] = get_attr(prev_word, 1)
            data_row["prev_second"] = get_attr(prev_word, 2)
            data_row["prev_third"] = get_attr(prev_word, 3)
            return_data.append((data_row, label))
            i += 1
    return return_data


def get_attr(word, i):
    if len(word) >= i:
        return word[-i]
    else:
        return "*"


data = parse_xml_for_data("annot.opcorpora.no_ambig.xml")
feature_set = prepare_data(data)
train_set = feature_set[0:round(len(feature_set) * 0.8)]
test_set = feature_set[round(len(feature_set) * 0.8):]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
