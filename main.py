from PyPDF2 import PdfReader


class ReadText:

    @staticmethod
    def read_file(file_name):
        with open(file_name, "r") as f:
            return f.read()


class TextProcessing:
    __pre_replace = [
        ('?"', '"'),
        ('!"', '"'),
        ('!', '.'),
        ('?', '.'),
        ('. ..', '.'),
        ('.. .', '.'),
        ('...', '.'),
        ('\n', '')
    ]

    __post_replace = [
        (',', ''),
        (' - ', ' '),
        (' -', '-'),
        ('(', ''),
        (')', ''),
        ('"', ''),
    ]

    text: str = ""

    def __init__(self, out_text):
        self.text = out_text

    def replace_text(self):
        for a, b in self.__pre_replace:
            self.text = self.text.replace(a, b)

        split_text_dot = self.text.split('.')[:-1]

        for a, b in self.__post_replace:
            for i in range(len(split_text_dot)):
                split_text_dot[i] = split_text_dot[i].replace(a, b)

        return [item.split() for item in split_text_dot]


class TextInfo:
    split_text_word: str = ""

    word_count: int = 0
    words_length: dict = {}

    char_word_count: int = 0
    sentences_length: dict = {}

    max_len_word: str = ""
    min_len_word: str = ""

    sentence_count: int = 0

    def __init__(self, out_text):
        self.words_length = {}
        self.sentences_length = {}
        self.split_text_word = out_text
        self.__text_analysis()
        self.__max_min_length_word()

    def __text_analysis(self):
        for i in range(len(self.split_text_word)):
            self.word_count += len(self.split_text_word[i])
            sentence_length = len(self.split_text_word[i])

            if sentence_length not in self.sentences_length:
                self.sentences_length[sentence_length] = 1
            else:
                self.sentences_length[sentence_length] += 1

            for j in self.split_text_word[i]:
                length = len(j)
                if length not in self.words_length:
                    self.words_length[length] = 1
                else:
                    self.words_length[length] += 1
                self.char_word_count += length

        new_word_dict = {}
        for i in sorted(self.words_length):
            new_word_dict[i] = self.words_length[i]
        self.words_length = new_word_dict

        new_sentences_dict = {}
        for i in sorted(self.sentences_length):
            new_sentences_dict[i] = self.sentences_length[i]
        self.sentences_length = new_sentences_dict

        self.sentence_count = len(self.split_text_word)

    def __max_min_length_word(self):
        self.max_len_word = self.split_text_word[0][0]
        self.min_len_word = self.split_text_word[0][0]

        service_parts_text = ReadText.read_file("ChastRech.txt").split('\n')

        for i in range(len(self.split_text_word)):
            for j in range(len(self.split_text_word[i])):
                if len(self.max_len_word) < len(self.split_text_word[i][j]) and\
                        self.split_text_word[i][j] not in service_parts_text:
                    self.max_len_word = self.split_text_word[i][j]
                    continue
                if len(self.min_len_word) > len(self.split_text_word[i][j]) and\
                        self.split_text_word[i][j] not in service_parts_text:
                    self.min_len_word = self.split_text_word[i][j]
                    continue

    def median_length_sentence(self):
        count_sum = 0
        numb_key = 0
        for key, value in self.sentences_length.items():
            count_sum += value
            if count_sum > self.sentence_count // 2:
                numb_key = key
                break
        return numb_key

    def median_length_words(self):
        count_sum = 0
        numb_key = 0
        for key, value in self.words_length.items():
            count_sum += value
            if count_sum > self.word_count // 2:
                numb_key = key
                break
        return numb_key

    def get_info(self):
        print("Кол-во слов - ", self.word_count)
        print(f'Самое длинное слово - {self.max_len_word}')
        print(f'Самое короткое слово - {self.min_len_word}')
        print(f'Количество символов - {self.char_word_count}')
        print(f'Средняя длина слов - {self.char_word_count / self.word_count:.5}')
        print(f'Количество предложений - {self.sentence_count}')
        print(f'Средняя длина предложений - {self.word_count / self.sentence_count:.5}')
        print(f'Медианная длина слов - {self.median_length_words()}')
        print(f'Медианная длина предложений - {self.median_length_sentence()}')

    def get_all_sentence(self):
        for i in range(len(self.split_text_word)):
            print(f"{i+1}){self.split_text_word[i]}")

    def search_words(self):
        char = input('Введите букву для вывода слов или \'-\' для завершения программы: ')[0].lower()
        if char == '-':
            exit()

        found_words = set()
        for word_dict in self.split_text_word:
            for word in word_dict:
                word = word.lower()
                if word.startswith(char):
                    found_words.add(word)

        print(f'Количество найденных слов на букву {char.upper()} - {len(found_words)}')
        for i in found_words:
            print(i)


if __name__ == '__main__':
    text = ReadText.read_file("text.txt")

    split_text_word = TextProcessing(text).replace_text()
    text_info = TextInfo(split_text_word)

    text_info.get_all_sentence()
    # text_info.get_info()
    # text_info.search_words()
    #
    # pdf_doc = PdfReader("test.pdf")
    # count_pages = len(pdf_doc.pages)
    # pdf_text = ""
    # for i in range(count_pages):
    #     page = pdf_doc.pages[i]
    #     pdf_text += f'{page.extract_text()} '
    # split_text_word = TextProcessing(pdf_text).replace_text()
    # text_info = TextInfo(split_text_word)
    #
    # text_info.get_info()
    # text_info.search_words()
