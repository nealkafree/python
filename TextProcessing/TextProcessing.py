def len_syl_to_len_symb(corpus):
    accumulator = 0
    corp_len = 0
    vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
    for text in corpus.texts:
        for sentence in text:
            for token in [token.value for token in sentence if token.group == "word"]:
                vow = 0
                for ch in token:
                    if ch in vowels:
                        vow += 1
                accumulator += vow / len(token)
                corp_len += 1
    return accumulator / corp_len


def average_len(corpus):
    accumulator = 0
    corp_len = 0
    vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
    for text in corpus.texts:
        for sentence in text:
            for token in [token.value for token in sentence if token.group == "word"]:
                vow = 0
                for ch in token:
                    if ch in vowels:
                        vow += 1
                accumulator += vow
                corp_len += 1
    return accumulator / corp_len


def average_sent_len(corpus):
    accumulator = 0
    corp_len = 0
    for text in corpus.texts:
        for sentence in text:
            accumulator += len([token.value for token in sentence if token.group == "word"])
            corp_len += 1
    return accumulator / corp_len


def printTokens(corpus):
    for text in corpus.texts:
        for sentence in text:
            for token in sentence:
                print(token)
    print()
    print("{END SNT}")
    print()


def getMetrics(corpus):
    metrics = TextMetrics()
    vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
    for sentence in corpus:
        for token in [token.value for token in sentence if token.group == "word"]:
            for ch in token:
                if ch in vowels:
                    metrics.vowelsCount += 1
            metrics.wordCount += 1
            metrics.charactersCount += len(token)
        metrics.sentencesCount += 1

    metrics.countHighLevelMetrics()
    return metrics


class TextMetrics:

    def __init__(self):
        self.name = ""
        self.vowelsCount = 0
        self.wordCount = 0
        self.sentencesCount = 0
        self.charactersCount = 0

        self.FRE = None
        self.FKRA = None
        self.ARI = None

    def countHighLevelMetrics(self):
        self.FKRA = 0.39 * self.wordCount / self.sentencesCount \
                    + 11.8 * self.vowelsCount / self.wordCount - 10.59
        self.ARI = 4.71 * self.charactersCount / self.wordCount \
                   + 0.5 * self.wordCount / self.sentencesCount - 21.43
        self.FRE = 206.835 - 1.3 * (self.wordCount / self.sentencesCount) - 60.1 * (self.vowelsCount / self.wordCount)
