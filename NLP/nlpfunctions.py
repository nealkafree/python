import json
import math
import re
import xml.etree.ElementTree as et
from multiprocessing import Pool

from nltk.tokenize import sent_tokenize, word_tokenize
from pymystem3 import Mystem
# from rnnmorph.predictor import RNNMorphPredictor
from tqdm import tqdm
import numpy as np

POS_TAGS = {'NOUN': 'S', 'ADJF': 'A', 'ADJS': 'A', 'COMP': 'A', 'VERB': 'V', 'INFN': 'V', 'PRTF': 'V',
            'GRND': 'V', 'ADVB': 'ADV', 'PRED': 'ADV', 'PRCL': 'ADV', 'INTJ': 'ADV', 'PREP': 'PR'}
LINK_TYPES = {'3', '4', '5', '1', '2'}
BANNED = {"PNCT", "UNKN", "LATN", "NUMB", "SYMB"}

DICTIONARY = 'dict.opcorpora.xml'
CORPUS = 'annot.opcorpora.no_ambig.xml'
REFERATS = 'example_texts.json'


def eat_dictionary(path):
    # Возвращает словарь в формате {форма_тег:лемма}. Пример: {стола_S:стол}
    tree = et.parse(path)
    root = tree.getroot()

    links = {}
    for link in root.iter('link'):
        at = link.attrib
        if at['type'] in LINK_TYPES:
            links[at['to']] = at['from']

    lem_dict = {}
    for lemma in root.iter('lemma'):
        lem_dict[lemma.attrib['id']] = lemma[0].attrib['t'].replace('ё', 'е')

    form_dict = {}
    for lemma in root.iter('lemma'):
        lemma_id = lemma.attrib['id']

        tag = lemma[0][0].attrib['v']
        if tag in POS_TAGS:
            tag = POS_TAGS[tag]

        lem = lem_dict[links[lemma_id]] if lemma_id in links else lem_dict[lemma_id]

        for form in lemma:
            form_dict[form.attrib['t'].replace('ё', 'е') + '_' + tag] = lem
    return form_dict


def eat_corpus(path):
    # Возвращает список предложений, которые являются списками кортежей (слово, тег)
    tree = et.parse(path)
    root = tree.getroot()
    text = []
    for sentence in root.iter('sentence'):
        res_sentence = []
        for token in sentence[1]:
            l_elem = token[0][0][0]
            word = token.attrib['text'].lower()
            tag = l_elem[0].attrib['v']
            if tag not in BANNED:
                if tag in POS_TAGS:
                    tag = POS_TAGS[tag]
                res_sentence.append((word, tag))
        if res_sentence:
            text.append(res_sentence)
    return text


def prepare_sentence(text):
    sentence = text.split()
    sentence = [word.strip('.,!?') for word in sentence]
    return sentence


def eat_json(path):
    with open(path, encoding='UTF-8') as file:
        return json.load(file)


def return_first_two_sentences(text):
    return text[0:2]


def return_first_and_last_sentences(text):
    return [text[0], text[-1]]


def lose_non_russian_alphabet(text):
    # Удаляет из текста любые символы не являющиеся кириллицей
    return re.sub('[^а-яА-ЯёЁ]', '', text)


def sentence_to_matrix(text):
    normal_text = normalize_text(text)
    M = []
    for sentence, i in zip(normal_text, range(len(text))):
        m = []
        for sent, j in zip(normal_text, range(len(text))):
            if i == j:
                m.append(0)
            else:
                m.append(jakkar(sentence, sent))
        n = sum(m)
        if n:
            m = [i / n for i in m]
        else:
            m = [1 / len(m) for _ in m]
        # m = [0.85 * i + 0.15 / len(m) for i in m]
        M.append(m)
    return M


def jakkar(sent1, sent2):
    a = set(sent1)
    b = set(sent2)
    c = a.intersection(b)
    t = len(a) + len(b) - len(c)
    return len(c) / t if t else 0


def expression_scores(normalized_texts, scores, min_freq):
    # Превращает коллекцию текстов в {слово: оценка экспрессивности}
    # оценка экспрессивности = S / n
    # S = сумма расстояний всех оценок текстов, в которых встречается слово до 5.5
    # n = количество текстов в которых встречается слово
    expression_dictionary = {}
    for text, score in zip(normalized_texts, scores):
        for sentence in text.split('.'):
            words = sentence.split(' ')
            words = appoint_denial(words)
            for word in words:
                count_expression(word, expression_dictionary, score)
    result_dict = {}
    for word, cort in expression_dictionary.items():
        if cort[1] > min_freq:
            result_dict[word] = cort[0] / cort[1]
    return result_dict


def expression_scores_bigr(normalized_texts, scores, min_freq):
    # Превращает коллекцию текстов в {(слово1, слово2): оценка экспрессивности}
    # оценка экспрессивности = S / n
    # S = сумма расстояний всех оценок текстов, в которых встречается слово до 5.5
    # n = количество текстов в которых встречается слово
    expression_dictionary = {}
    for text, score in zip(normalized_texts, scores):
        for sentence in text.split('.'):
            words = sentence.split(' ')
            words = appoint_denial(words)
            for word1, word2 in zip(words, words[1:]):
                bigr = (word1, word2)
                count_expression(bigr, expression_dictionary, score)
    result_dict = {}
    for word, cort in expression_dictionary.items():
        if cort[1] > min_freq:
            result_dict[word] = cort[0] / cort[1]
    return result_dict


def appoint_denial(words):
    for word in words:
        if word == 'не' and words.index(word) + 1 < len(words):
            words[words.index(word) + 1] = 'не_' + words[words.index(word) + 1]
            words.pop(words.index(word))
    return words


def expression_scores_trigr(normalized_texts, scores, min_freq):
    # Превращает коллекцию текстов в {(слово1, слово2, слово3): оценка экспрессивности}
    # оценка экспрессивности = S / n
    # S = сумма расстояний всех оценок текстов, в которых встречается слово до 5.5
    # n = количество текстов в которых встречается слово
    expression_dictionary = {}
    for text, score in zip(normalized_texts, scores):
        for sentence in text.split('.'):
            words = sentence.split(' ')
            for word1, word2, word3 in zip(words, words[1:], words[2:]):
                trigr = (word1, word2, word3)
                count_expression(trigr, expression_dictionary, score)
    result_dict = {}
    for word, cort in expression_dictionary.items():
        if cort[1] > min_freq:
            result_dict[word] = cort[0] / cort[1]
    return result_dict


def count_expression(key, dictionary, score):
    if key in dictionary:
        dictionary[key] = (dictionary[key][0] + math.fabs(int(score) - 5.5),
                           dictionary[key][1] + 1)
    else:
        dictionary[key] = (math.fabs(int(score) - 5.5), 1)


def normalize_text(*text):
    # Превращает текст в список предложений, являющихся списками нормализованных слов
    text = ''.join(text)
    predictor = Mystem()
    normal_text = []
    for sentence in re.split('[.!?]', text):
        words = [word for word in predictor.lemmatize(sentence) if word.isalpha()]
        if words:
            normal_text.append(words)
    return normal_text


def test_texts_normalize(dataset):
    test_dataset = []
    with Pool(8) as p:
        result = [p.apply_async(normalize_text, text) for text in dataset]
        for text in result:
            text = text.get()
            res_text = []
            for sentence in text:
                res_text.append(' '.join(sentence))
            test_dataset.append('.'.join(res_text) + '\n')
    return test_dataset


def prepare_bow(texts, words_list):
    # Создает массив мешков слов (проверяются только слова из word_list) для текстов из texts
    train_set = []
    for text in texts:
        features = [0 for _ in range(len(words_list))]
        for sentence in text.split('.'):
            for word in sentence.split(' '):
                if word in words_list:
                    features[words_list.index(word)] += 1
        train_set.append(features)
    return train_set


def excl_feature(text):
    c = 0
    for symbol in text:
        if symbol == '!':
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


def read_file(path):
    with open(path, encoding="UTF-8") as file:
        return file.read().split("\n")


def extraction_preprocess(dataset):
    # Затем приписать каждому токену его контекст (+-N) и сопоставить с тренировочными данными
    # А также начинается ли тег с большой буквы
    dataset_prep = []
    for line in dataset:
        words = word_tokenize(line)
        words_prep = []
        i = 1
        words_prep.append((words[0], 0, len(words[0])))
        while i < len(words):
            if words[i] in '.,;!?:»)' or words[i - 1] in '(«' or words[i - 1] == '``':
                words_prep.append((words[i], words_prep[i - 1][1] + words_prep[i - 1][2], len(words[i])))
            elif words[i] == "''":
                words_prep.append((words[i], words_prep[i - 1][1] + words_prep[i - 1][2], len(words[i]) - 1))
            elif words[i] == '``':
                words_prep.append((words[i], words_prep[i - 1][1] + words_prep[i - 1][2] + 1, len(words[i]) - 1))
            else:
                words_prep.append((words[i], words_prep[i - 1][1] + words_prep[i - 1][2] + 1, len(words[i])))
            i += 1
        dataset_prep.append(words_prep)
    return dataset_prep


def prepare_answers(answers):
    pass


def prepare_features(dataset, answers):
    pass


prep = extraction_preprocess(read_file('train_sentences.txt')[0:20])
