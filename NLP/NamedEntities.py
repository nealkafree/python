# скушать текст
# побить на наборы признаков
import nltk

PUNCT = {'.', '!', '?'}
PUNCTFULL = {'.', '!', '?', '...', ',', '-', ':'}


def read_file(path):
    with open(path, encoding="UTF-8") as file:
        return nltk.tokenize.word_tokenize(file.read())


def prepare_dictionary(path):
    with open(path, encoding="UTF-8") as file:
        return file.read().split("\n")


def prepare_data(text):
    data = []
    text.append("#")
    i = 0
    while i < len(text) - 1:
        features = {}
        features["word"] = text[i]
        features["previous"] = True if i > 0 and text[i - 1] in PUNCT else False
        features["next"] = True if i < len(text) - 2 and text[i + 1] == '.' else False
        if text[i][0].isupper():
            if text[i][1:].islower():
                features["capital"] = "firstUpper"
            elif text[i][1:].isupper():
                features["capital"] = "allUpper"
            else:
                features["capital"] = "unknown"
        else:
            if text[i].islower():
                features["capital"] = "allLower"
            else:
                features["capital"] = "unknown"
        if text[i].upper() in DICT:
            features["inDict"] = True
        else:
            features["inDict"] = False
        data.append((features, "unkn"))
        i += 1
    return data


tokens = read_file("test")
print("tokens are ready")
DICT = set(prepare_dictionary("tuzov.words.txt"))
print("dictionary are ready")
dataset = prepare_data(tokens)
print("data are ready")
for feature in dataset:
    if ((feature[0]["previous"] and feature[0]["capital"] != "firstUpper") or feature[0]["capital"] != "allLower") and \
            feature[0]["word"] not in PUNCTFULL:
        print(feature[0])
