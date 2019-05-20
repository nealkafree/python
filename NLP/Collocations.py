import nltk
import pymorphy2
from nltk.collocations import *
from nltk.corpus import stopwords


def go():
    with open('test') as file:
        words = nltk.tokenize.word_tokenize(file.read())
        stop = stopwords.words('russian')
        words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop]

        morph = pymorphy2.MorphAnalyzer()
        words = [morph.parse(word)[0].normal_form for word in words]

        bigram = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(5)

        print(set(finder.nbest(bigram.dice, 20)) & set(finder.nbest(bigram.pmi, 20)) & set(
            finder.nbest(bigram.likelihood_ratio, 20)))


if __name__ == "__main__":
    go()
