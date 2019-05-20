import CorpusTokenizer
import TextProcessing
import os

files = os.listdir("Corpus")
metrics = []
for file in files:
    corpus = CorpusTokenizer.tokenize(os.getcwd() + "/Corpus", file)

    metric = TextProcessing.getMetrics(corpus)
    metric.name = file
    metrics.append(metric)

    print(metric.name)
    print("Character count", metric.charactersCount)
    print("Vowels count", metric.vowelsCount)
    print("Words count", metric.wordCount)
    print("Sentences count", metric.sentencesCount, "\n")

    print("FRE", metric.FRE)
    print("FKRA", metric.FKRA)
    print("ARI", metric.ARI, "\n\n")
