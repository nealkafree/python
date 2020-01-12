import json
import re
import xml.etree.ElementTree as et
from nltk.tokenize import sent_tokenize, word_tokenize
from rnnmorph.predictor import RNNMorphPredictor

# Файл для решения задачи с частеречными теггерами
# Варианты теггеров:
# 1) HMM теггер
# 2) теггер на наивом байесе
# 3) теггер на перцептроне
# Здесь же будут функции для предобработке xml и подготовке данных
from tqdm import tqdm

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
        return [sent_tokenize(text) for text in json.load(file)]


def return_first_two_sentences(text):
    return text[0:2]


def return_first_and_last_sentences(text):
    return [text[0], text[-1]]


def lose_non_russian_alphabet(text):
    # Удаляет из текста любые символы не являющиеся кириллицей
    return re.sub('[^а-яА-ЯёЁ]', '', text)


def sentence_to_matrix(text):
    predictor = RNNMorphPredictor(language='ru')
    normal_text = []
    for sentence in text:
        words = word_tokenize(sentence)
        words = [lose_non_russian_alphabet(word).lower() for word in words if lose_non_russian_alphabet(word)]
        words = [prediction.normal_form for prediction in predictor.predict(words)]
        normal_text.append(words)
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


# ref = eat_json(REFERATS)
# for text in ref:
#     print(len(text))
#     print(len(sentence_to_matrix(text)))
