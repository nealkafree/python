import os


def tokenize(path, name):
    """Trying to read file"""
    try:
        with open(path + "/" + name) as file:
            text = file.read()
            tokenized_text = []

            """Creating FSM"""
            is_word = False
            word = ""
            sentence = []

            for ch in text:

                """Checking every symbol"""
                if ch.isalpha():
                    word += ch
                    is_word = True
                else:
                    if is_word:
                        sentence.append(Token(word.lower(), "word"))
                        is_word = False
                        word = ""
                    if ch in [".", "!", "?"]:
                        sentence.append(Token(ch, "end_snt"))
                        tokenized_text.append(sentence)
                        sentence = []
                    elif not ch.isspace():
                        sentence.append(Token(ch, "inter_snt"))

            return tokenized_text

    except UnicodeError:
        print("Файл " + name + " не прочитан.")


def print_tokenized_text(tokenized_text):
    for sentence in tokenized_text:
        for token in sentence:
            print(token)
        print()
        print("{END SNT}")
        print()


class Token:

    def __init__(self, value, group):
        self.value = value
        self.group = group

    def __str__(self):
        return self.value + " " + self.group


class CorpusTokens:

    def __init__(self, path):
        """Making path absolute"""
        # if os.path.exists(path):
            # path = os.getcwd() + '/' + path

        """Trying to open directory"""
        try:
            file_list = os.listdir(path)
        except FileNotFoundError:
            print("Директория не найдена")
            return

        """Creating list of tokenized texts"""
        self.texts = []
        for file in file_list:
            self.texts.append(tokenize(path, file))


print("CorpusTokenizer is imported\n")
