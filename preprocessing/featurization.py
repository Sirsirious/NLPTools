import numpy as np
import math
import string
import pickle
from functools import reduce
from ..core.structures import Document, Sentence, Token

class AbstractFeaturizer():
    """
    Abstract class for turning text into features.
    Attributes
    ----------
    ignore_tokens: list of str
        List of tokens to ignore in Featurization computing. E.g.: <SOS> and <EOS> tokens (default).
    ignore_punctuation: boolean
        Whether to ignore punctiation as features. Defaults to True. Uses string.punctuation.
    lower_case: boolean
        Whether to turn all text to lowercase or keep case. Default to false (keeps case).
    word_indexes: dict of int
        A dictionary with the index of each word fit into the featurizer. This is used to compose the feature vector.
    """

    def __init__(self, ignore_tokens=["<SOS>","<EOS>"], ignore_punctuation=True, lower_case = False):
        self.ignore_tokens = ignore_tokens
        if ignore_punctuation:
            self.ignore_tokens+=[char for char in string.punctuation]
        self.lower_case=lower_case
        self.word_indexes={}
        self.index_to_word={}

    def fit(self, data):
        """
        Fits the data into the Featurizer.
        Abstract class only implements the exceptions.
        Exceptions
        ----------
        TypeError
            Related to data type. Expects Document or list of strings.
        """

        if not (isinstance(data, Document) or isinstance(data, list)):
            raise(TypeError("Could not fit data because it is of wrong type. Type {} found. Please, insert it as a Document or list of strings".format(type(data))))

    def transform(self, data):
        """
        Transforms the data passed as input.
        Abstract class only implements the exceptions.
        Exceptions
        ----------
        TypeError
            Related to data type. Expects Document, Sentence, list of strings or string.
        AttributeError
            Related to the vocabulary lenght. Happens if fit with empty data or not fit.
        """
        if not (isinstance(data, Document) or isinstance(data, Sentence) or isinstance(data, str) or isinstance(data, list)):
            raise(TypeError("Could not transform data because it is of wrong type. Type {} found. Please, insert it as a Document, list of strings, Sentence or string.".format(type(data))))
        if len(self.word_indexes) == 0:
            raise(AttributeError("Vocabulary length is zero. Maybe you forgot to fit the Featurizer?"))

    def fit_transform(self, data):
        """
        Fits and then transforms the data passed as input.
        """
        self.fit(data)
        return self.transform(data)

    def _transform_document():
        pass

    def _transform_sentence():
        pass

    def save_to_file(self, filename):
        """
        Saves the current status of the Featurizer to a pickled file. Useful for deploying.
        """
        if not filename.endswith(".p"):
            filename+=".p"
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
        print("{} saved successfully as a pickeld file. You can load it using 'load_from_file' function.")

    def load_from_file(self, filename):
        """
        Loads a pickled featurizer, updating the current featurizer to match the saved data.
        """
        with open(filename, 'rb') as f:
            tmp_dict = pickle.load(f)
        self.__dict__.update(tmp_dict)

class Bow(AbstractFeaturizer):
    """
    Bag of Words implementation for featurization. Based on AbstractFeaturizer class.
    """

    def __init__(self, ignore_tokens=["<SOS>","<EOS>"], ignore_punctuation=True, lower_case = False):
        super().__init__(ignore_tokens, ignore_punctuation, lower_case)

    def fit(self, data):
        """
        Fits the data into the Featurizer.
        Arguments
        ---------
        data: Document or list of string.
            The data to fit the featurizer.
        Exceptions
        ----------
        TypeError
            Related to data type. Expects Document or list of strings.
        """
        super(Bow, self).fit(data)
        document_words = list(set(global_term_frequency(data, self.ignore_tokens, self.lower_case).keys()))
        for word_position in range(len(document_words)):
            word = document_words[word_position]
            self.word_indexes[word] = word_position

    def transform(self, data):
        """
        Transforms the data passed as input into a Bag of Words vector/matrix, depending on the input.
        Arguments
        ---------
        data: Document, Sentence, list of string or string.
            The data to fit the featurizer.
        Exceptions
        ----------
        TypeError
            Related to data type. Expects Document, Sentence, list of strings or string.
        AttributeError
            Related to the vocabulary lenght. Happens if fit with empty data or not fit.
        """
        super(Bow, self).transform(data)
        if isinstance(data, Document) or isinstance(data, list):
            return self._transform_document(data)
        elif isinstance(data, Sentence) or isinstance(data, str):
            return self._transform_sentence(data)

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
            tokens = [token.get().lower() if self.lower_case else token.get() for token in data.tokens if token not in self.ignore_tokens]
        else:
            tokens = [token.lower() if self.lower_case else token for token in data.split()]
        word_array = np.zeros(len(self.word_indexes))
        for token in tokens:
            # Dismisses out of vocabulary tokens
            if token in self.word_indexes:
                token_index = self.word_indexes[token]
                word_array[token_index]+=1
        return word_array


class Tfidf(AbstractFeaturizer):
    """
    TF-IDF implementation for featurization. Based on AbstractFeaturizer class.
    Attributes:
    -----------
    idf_dict: dict of int.
        Dictionary containing the idf score for each word (available after fitting).
    num_documents: int.
        Number of documents used to fit the featurizer (important feature for score calculation).
    """

    def __init__(self, ignore_tokens=["<SOS>","<EOS>"], ignore_punctuation=True, lower_case=False):
        super().__init__(ignore_tokens, ignore_punctuation, lower_case)
        self.idf_dict = {}
        self.num_documents = 0

    def fit(self, data):
        """
        Fits the data into the Featurizer.
        Arguments
        ---------
        data: Document or list of string.
            The data to fit the featurizer.
        Exceptions
        ----------
        TypeError
            Related to data type. Expects Document or list of strings.
        """
        super(Tfidf, self).fit(data)
        self.num_documents = len(data) if isinstance(data, list) else len(data.sentences)
        word_freq_per_document = self._compute_global_tf(data)
        self._compute_idf(word_freq_per_document)
        document_words = list(set(global_term_frequency(data, self.ignore_tokens, self.lower_case)))
        for word_position in range(len(document_words)):
            word = document_words[word_position]
            self.word_indexes[word] = word_position
            self.index_to_word[word_position] = word

    def transform(self, data):
        """
        Transforms the data passed as input into a tdf-idf vector/matrix, depending on the input.
        Arguments
        ---------
        data: Document, Sentence, list of string or string.
            The data to fit the featurizer.
        Exceptions
        ----------
        TypeError
            Related to data type. Expects Document, Sentence, list of strings or string.
        AttributeError
            Related to the vocabulary lenght. Happens if fit with empty data or not fit.
        """
        super(Tfidf, self).transform(data)
        if isinstance(data, Document) or isinstance(data, list):
            return self._transform_document(data)
        elif isinstance(data, Sentence) or isinstance(data, str):
            return self._transform_sentence(data)

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
            tokens = [token.get().lower() if self.lower_case else token.get() for token in data.tokens if token not in self.ignore_tokens]
        else:
            tokens = [token.lower() if self.lower_case else token for token in data.split()]
        word_array = np.zeros(len(self.word_indexes))
        sentence_tf_idf = self._compute_sentence_tf_idf(data)
        for token in tokens:
            # Dismisses out of vocabulary tokens
            if token in self.word_indexes:
                token_index = self.word_indexes[token]
                word_array[token_index] = sentence_tf_idf[token]
        return word_array

    def _compute_global_tf(self, data):
        """
        Computes global term frequency from data.
        """
        word_freq_per_document = {}
        if isinstance(data, Document):
            list_of_sentences = data.sentences
        else:
            list_of_sentences = data
        for sentence in list_of_sentences:
            words_in_sent = set()
            document_frequency = term_frequency(sentence, self.ignore_tokens, self.lower_case)
            for word in document_frequency:
                if not word in words_in_sent:
                    word_freq_per_document[word] = word_freq_per_document.get(word, 0)+1
                    words_in_sent.add(word)
        return word_freq_per_document

    def explain(self, tf_idf_array, summary=False):
        explained_results = {}
        if len(tf_idf_array.shape)>1:
            for sent_id, sent_scores in enumerate(tf_idf_array):
                explained_results[sent_id]={}
                for word_idx, idf in enumerate(sent_scores):
                    if summary:
                        if idf == 0.0:
                            continue
                    word = self.index_to_word[word_idx]
                    explained_results[sent_id][word]=idf
        else:
            explained_results[0]={}
            for word_idx, idf in enumerate(tf_idf_array):
                if summary:
                    if idf == 0.0:
                        continue
                word = self.index_to_word[word_idx]
                explained_results[0][word]=idf
        return explained_results


    def _compute_idf(self, word_freq_per_document):
        """
        Computes sentence(document) idf.
        """
        for word, frequency in word_freq_per_document.items():
            idf = math.log(float(1 + self.num_documents) / (1 + frequency))
            self.idf_dict[word]=idf

    def _compute_sentence_tf_idf(self, sentence):
        """
        Computes the tf_idf for a single sentence(document).
        """
        sentence_tf_idf = {}
        document_frequency = term_frequency(sentence, self.ignore_tokens, self.lower_case)
        total_words = sum(document_frequency.values())
        averaged_frequency = {k:(float(v)/total_words) for k,v in document_frequency.items()}
        for term, tf in averaged_frequency.items():
            # Out of vocabulary words are simply zeroed. They are going to be removed later either way.
            sentence_tf_idf[term] = tf*self.idf_dict.get(term, 0)
        return sentence_tf_idf


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

def global_term_frequency(document, ignore_tokens=["<SOS>","<EOS>"], lower_case = False):
    """
    Function to compute a list of terms and their frequency from a document (or set of documents). Used as auxiliary for other methods.
    Arguments:
    ----------
    document: list of string or Document class object.
        The "document" (or set of documents) to compute the global term frequency.
    ignore_tokens: list of str.
        Tokens to ignore in the term frequency computation.
    lower_case: boolean.
        Whether to be case sensitive or not. Defaults to False (case sensitive).
    """
    word_dict = {}
    if isinstance(document, Document):
        list_of_sentences = document.sentences
    else:
        list_of_sentences = document
    sentences_freqs = []
    for sentence in list_of_sentences:
        sentences_freqs.append(term_frequency(sentence, ignore_tokens, lower_case))
    word_dict = reduce_term_frequency(sentences_freqs)
    return word_dict

def term_frequency(sentence, ignore_tokens=["<SOS>","<EOS>"], lower_case = False):
    """
    Computes the term frequency for a single sentence (or document). Used as auxiliary for other methods.
    Arguments:
    ----------
    document: list of string or Document class object.
        The "document" (or set of documents) to compute the global term frequency.
    ignore_tokens: list of str.
        Tokens to ignore in the term frequency computation.
    lower_case: boolean.
        Whether to be case sensitive or not. Defaults to False (case sensitive).
    """
    word_dict = {}
    if isinstance(sentence, Sentence):
        words = [token.get().lower() if lower_case else token.get() for token in sentence.tokens if token not in ignore_tokens]
    else:
        words = [token.lower() if lower_case else token for token in sentence.split() if token not in ignore_tokens]
    for word in words:
        word_dict[word] = word_dict.get(word, 0)+1
    return word_dict

def reduce_term_frequency(list_of_word_dict):
    """
    Reduces a list of dicts to a single dictionary, summing all related values. Used to condense the results from the application of multimple term_frequency over several sentences. Returns a single 'str':int dict.
    Arguments:
    ----------
    list_of_word_dict: list of dict
        List of word dicts, containing pairs in 'str':int format, where the string is the word and the int is the frequency.
    """
    def reducer(accumulator, element):
        for key, value in element.items():
            accumulator[key] = accumulator.get(key, 0) + value
        return accumulator
    total_frequencies = reduce(reducer, list_of_word_dict, {})
    return total_frequencies
