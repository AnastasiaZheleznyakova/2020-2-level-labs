import math
import re

"""
Language detection using n-grams
"""


# 4
def tokenize_by_sentence(text: str) -> tuple:
    """
    Splits a text into sentences, sentences into tokens, tokens into letters
    Tokens are framed with '_'
    :param text: a text
    :return: a tuple of sentence with tuples of tokens split into letters
    e.g.
    text = 'She is happy. He is happy.'
    -->  (
         (('_', 's', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
         (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_'))
         )
    """
    if not isinstance(text, str) or not text:
        return ()
    sentences = re.split(r"[.!?]+", text.lower())
    sentences = [sentence for sentence in sentences if sentence]
    if not sentences:
        return ()
    result = tuple(
        tuple(
            ('_',) + tuple(letter for letter in word) + ('_',)
            for word in re.sub(r"[^a-zA-Z\s]", "", sentence).split()
        )
        for sentence in sentences if re.sub(r"[^a-zA-Z\s]", "", sentence).split()
    )


    return result


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if isinstance(letter, str) and len(letter) == 1:
            if letter not in self.storage:
                self.storage[letter] = len(self.storage)
            return 0
        else:
            return 1

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter in self.storage:
            return self.storage[letter]
        else:
            return -1

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if isinstance(corpus, tuple):
            for sentence in corpus:
                for token in sentence:
                    for letter in token:
                        result = self._put_letter(letter)
                        if result != 0:
                            return 1
            return 0
        else:
            return 1


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if isinstance(storage, LetterStorage):
        error = storage.update(corpus)
        if not error:
            result = tuple(
                tuple(
                    tuple(
                        storage.get_id_by_letter(letter)
                        for letter in word
                    )
                    for word in sentence
                )
                for sentence in corpus
            )
            return result
        else:
            return ()
    else:
        return ()



# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if isinstance(encoded_text, tuple):
            list_n_grams = []
            for sentence in encoded_text:
                n_grams_sentence = []
                for token in sentence:
                    n_grams_token = []
                    for ind in range(len(token) - self.size + 1):
                        n_grams_token.append(tuple(token[ind:ind + self.size]))
                    n_grams_sentence.append(tuple(n_grams_token))
                list_n_grams.append(tuple(n_grams_sentence))
            self.n_grams = tuple(list_n_grams)
            return 0
        else:
            return 1

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if self.n_grams:
            for sentence in self.n_grams:
                for word in sentence:
                    for n_gram in word:
                        self.n_gram_frequencies[n_gram] = self.n_gram_frequencies.get(n_gram, 0) + 1
            return 0
        else:
            return 1

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if self.n_gram_frequencies:
            for n_gram in self.n_gram_frequencies:
                arr = [self.n_gram_frequencies[other_n_gram]
                       for other_n_gram in self.n_gram_frequencies
                       if n_gram[:self.size - 1] == other_n_gram[:self.size - 1]]
                probability = self.n_gram_frequencies[n_gram] / sum(arr)
                self.n_gram_log_probabilities[n_gram] = math.log(probability)
            return 0
        else:
            return 1

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if self.n_gram_frequencies and isinstance(k, int) and k >= 0:
            return tuple(sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)[:k])
        else:
            return ()



# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        pass

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        pass

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        pass

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        pass


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        pass

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        pass
