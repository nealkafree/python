import nltk.lm.preprocessing as prep
from nltk.util import bigrams


def freq(text):
    freq_dict = {}
    for word in text:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict


def bigr_freq(text):
    freq_dict = {}
    for sent in text:
        bigr = bigrams(sent)
        for first, second in bigr:
            if first in freq_dict:
                d = freq_dict[first]
                if second in d:
                    d[second] += 1
                else:
                    d[second] = 1
            else:
                d = {second: 1}
                freq_dict[first] = d
    return freq_dict


def perp(text):
    bigr = bigrams(text.split())
    probab = 1
    for first, second in bigr:
        d = bigram_dict[first]
        if second in d:
            p = d[second] / freq_dict[first]
        else:
            p = 0
        print(p)
        probab *= p
    return pow(probab, -(1 / 4))


with open('train_corpus', encoding='UTF-8') as file:
    text = []
    for line in file.readlines():
        text.append(line.strip().split(' '))

    # test_text = []
    # for line in file2.readlines():
    #     test_text.append(line.split(' '))

    freq_dict = freq(prep.flatten(text))
    bigram_dict = bigr_freq(text)

    print(bigram_dict)

    # for sent in test_text:
    #     key = bigrams(sent)
    #     probab = 1
    #     for first, second in key:
    #         d = bigram_dict[first]
    #         if second in d:
    #             p = d[second] / freq_dict[first]
    #         else:
    #             p = 0
    #         probab *= p
    #     print(probab)
    print(perp('<s> Георгий любит малину </s>'))
