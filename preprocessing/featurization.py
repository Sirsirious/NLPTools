import numpy as np
import string
from functools import reduce
from ..core.structures import Document, Sentence, Token

class AbstractFeaturizer():
    def fit():
        pass

    def transform():
        pass

    def fit_transform():
        pass

    def _transform_document():
        pass

    def _transform_sentence():
        pass

class BagOfWords(AbstractFeaturizer):

    def __init__(self, ignore_tokens=["<SOS>","<EOS>"], ignore_punctuation=True, lower_case = False):
        self.ignore_tokens = ignore_tokens
        if ignore_punctuation:
            self.ignore_tokens+=[char for char in string.punctuation]
        self.lower_case = lower_case
        #TODO implement lowercase
        self.word_indexes = {}
        self.vocabulary_lenght = 0

    def fit(self, data):
        document_words = list(set(global_term_frequency(data, self.ignore_tokens).keys()))
        for word_position in range(len(document_words)):
            word = document_words[word_position]
            self.word_indexes[word] = word_position
        self.vocabulary_lenght = len(document_words)

    def transform(self, data):
        if self.vocabulary_lenght == 0:
            raise(AttributeError("Vocabulary lenght is zero. Maybe you forgot to fit the BoWFeaturizer?"))
        if isinstance(data, Document) or isinstance(data, list):
            return self._transform_document(data)
        elif isinstance(data, Sentence) or isinstance(data, str):
            return self._transform_sentence(data)
        else:
            raise(ValueError("Could not transform data because it is of wrong type. Type <{}> found. Please, insert it as a Document, list of strings, Sentence or string.".format(type(data))))

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)

    def _transform_document(self, data):
        if isinstance(data, Document):
            to_transform = data.sentences
        else:
            to_transform = data
        sentence_arrays = []
        for sentence in data:
            sentence_arrays.append(self._transform_sentence(sentence))
        return np.matrix(sentence_arrays)

    def _transform_sentence(self, data):
        if isinstance(data, Sentence):
            tokens = [token.get() for token in data.tokens if token not in self.ignore_tokens]
        else:
            tokens = data.split()
        word_array = np.zeros(self.vocabulary_lenght)
        for token in tokens:
            #Dismisses out of vocabulary tokens
            if token in self.word_indexes:
                token_index = self.word_indexes[token]
                word_array[token_index]+=1
        return word_array


class TFIDFTransformer(AbstractFeaturizer):
    def fit():
        pass

    def transform():
        pass

    def fit_transform():
        pass

    def _transform_document():
        pass

    def _transform_sentence():
        pass

class Word2VecTransformer(AbstractFeaturizer):
    def fit():
        pass

    def transform():
        pass

    def fit_transform():
        pass

    def _transform_document():
        pass

    def _transform_sentence():
        pass

def global_term_frequency(document, ignore_tokens=["<SOS>","<EOS>"]):
    word_dict = {}
    if isinstance(document, Document):
        list_of_sentences = document.sentences
    else:
        list_of_sentences = document
    sentences_freqs = []
    for sentence in list_of_sentences:
        words = []
        sentences_freqs.append(term_frequency(sentence, ignore_tokens))
    word_dict = reduce_term_frequency(sentences_freqs)
    return word_dict

def term_frequency(sentence, ignore_tokens=["<SOS>","<EOS>"]):
    word_dict = {}
    if isinstance(sentence, Sentence):
        words = [token.get() for token in sentence.tokens if token not in ignore_tokens]
    else:
        words = sentence.split()
    for word in words:
        word_dict[word] = word_dict.get(word, 0)+1
    return word_dict

def reduce_term_frequency(list_of_word_dict):
    def reducer(accumulator, element):
        for key, value in element.items():
            accumulator[key] = accumulator.get(key, 0) + value
        return accumulator
    total_frequencies = reduce(reducer, list_of_word_dict, {})
    return total_frequencies
