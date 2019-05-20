import nltk.lm
import nltk.lm.preprocessing
from nltk.util import bigrams


def train_ngrams(n, training_corpus, model, gamma):
    train, vocab = nltk.lm.preprocessing.padded_everygram_pipeline(n, training_corpus)

    lp = model(gamma=gamma, order=n)

    lp.fit(train, vocab)

    return lp


def train_ngrams_kn(n, training_corpus, model, smoothing):
    train, vocab = nltk.lm.preprocessing.padded_everygram_pipeline(n, training_corpus)

    lp = model(order=n)

    lp.fit(train, vocab)

    return lp


def get_words(path):
    with open(path) as file:
        list_sent = nltk.tokenize.sent_tokenize(file.read())
        list_sent = [nltk.tokenize.word_tokenize(sent) for sent in list_sent]
        return list_sent


def entropy_preprocess(word_list):
    word_list = [list(bigrams(nltk.lm.preprocessing.pad_both_ends(sent, n=2))) for sent in word_list]
    bigrams_list = []
    for sent in word_list:
        for bigramm in sent:
            bigrams_list.append(bigramm)
    return bigrams_list


# words = [[token.get_value() for token in sent if token.get_group() == 'word']
#         for sent in CorpusTokenizer.tokenize('.', 'test')]
words = get_words('test')
training_part = words[0:round(len(words) * 0.8)]
validating_part = words[round(len(words) * 0.8): round(len(words) * 0.9)]
testing_part = words[round(len(words) * 0.9):]

validating = entropy_preprocess(validating_part)
testing = entropy_preprocess(testing_part)
training = entropy_preprocess(training_part)

test ='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
test = [nltk.tokenize.word_tokenize(sent) for sent in nltk.tokenize.sent_tokenize(test)]
test = entropy_preprocess(test)

res = train_ngrams(2, training_part, nltk.lm.Lidstone, 0.01)
print(test)
print(testing)
print(res.entropy(test))
print(res.entropy(testing))
