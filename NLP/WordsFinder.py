import re


def prepare_dictionary(path):
    with open(path) as file:
        dictionary = {}
        for line in file.readlines():
            words = re.split('[\s,]+', line)
            if 'NOUN' in words and 'nomn' in words and 'sing' in words:
                word = words[0].lower()
                word_set = set()
                for letter in word:
                    add_letter(letter, word_set, 1)
                dictionary[word] = word_set
    return dictionary


def add_letter(letter, word_set, number):
    if letter + str(number) not in word_set:
        word_set.add(letter + str(number))
    else:
        add_letter(letter, word_set, number + 1)


base_word = 'крыжовник'
word_set = set()
for letter in base_word:
    add_letter(letter, word_set, 1)
print(base_word)
print(word_set)
dictionary = prepare_dictionary('dict.opcorpora.txt')
print('словарь готов')
result = set()
for word, set in dictionary.items():
    if set.issubset(word_set):
        result.add(word)
print(result)
