import json
import os
import re
import string
import warnings

import pkg_resources
from symspellpy.symspellpy import SymSpell, Verbosity

from ..core.structures import sentencize, tokenize, Sentence, Document, untokenize

contractions_file = os.path.join(os.path.dirname(__file__),
                                 "../preloaded/dictionaries/contractions/english_contractions.json")
stopwords_file = os.path.join(os.path.dirname(__file__), "../preloaded/lists/words/english_stopwords.txt")


#### Pre-tokenization functions ####

def simplify_punctuation(text):
    """
    This function simplifies doubled or more complex punctuation. The exception is '...'.
    """
    if text is None:
        return ''
    corrected = str(text)
    corrected = re.sub(r'([!?,;])\1+', r'\1', corrected)
    corrected = re.sub(r'\.{2,}', r'...', corrected)
    return corrected


def normalize_whitespace(input_string):
    """
    This function normalizes whitespaces, removing duplicates.
    """
    if input_string is None:
        return ''
    corrected = str(input_string)
    corrected = re.sub(r"//t", r"\t", corrected)
    corrected = re.sub(r"( )\1+", r"\1", corrected)
    corrected = re.sub(r"(\n)\1+", r"\1", corrected)
    corrected = re.sub(r"(\r)\1+", r"\1", corrected)
    corrected = re.sub(r"(\t)\1+", r"\1", corrected)
    return corrected.strip(" ")


#### Post-tokenization functions ####

def normalize_contractions(token_list):
    """
    This function normalizes english contractions.
    """
    contractions = json.loads(open(contractions_file, 'r').read())
    new_token_list = []
    for word_pos in range(1, len(token_list[:-1])):
        word_token = token_list[word_pos]
        word = word_token.get()
        first_upper = False
        if word[0].isupper():
            first_upper = True
        if word.lower() in contractions:
            replacement = contractions[word.lower()]
            if first_upper:
                replacement = replacement[0].upper() + replacement[1:]
            replacement_tokens = replacement.split()
            if len(replacement_tokens) > 1:
                new_token_list.append(replacement_tokens[0])
                new_token_list.append(replacement_tokens[1])
            else:
                new_token_list.append(replacement_tokens[0])
        else:
            new_token_list.append(word_token.get())
    tokens = tokenize(" ".join(new_token_list).strip(" "))
    return tokens


def remove_stopwords(token_list):
    """
    This function does simple stopword removal over a token List. The token is actually not removed, but its representation blanked.
    Uses https://www.ranks.nl/stopwords stopword list.
    """
    stopwords = [line.replace('\n', '') for line in open(stopwords_file, 'r').readlines()]
    for word_pos in range(1, len(token_list[:-1])):
        word_token = token_list[word_pos]
        word = word_token.get()
        if word in stopwords:
            word_token.repr = ""
            token_list[word_pos] = word_token
    return token_list


def spell_correction(token_list):
    """
    This function does very simple spell correction normalization using pyspellchecker module. It works over a tokenized sentence and only the token representations are changed.
    """
    # Spell checker config
    spellchecker = SysmspellSingleton()
    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.TOP  # TOP, CLOSEST, ALL
    # End of Spell checker config
    for word_pos in range(1, len(token_list[:-1])):
        word_token = token_list[word_pos]
        word = word_token.get()
        if not '\n' in word and word not in string.punctuation and not is_numeric(word) and not (
                word.lower() in spellchecker.words.keys()):
            suggestions = spellchecker.lookup(word.lower(), suggestion_verbosity, max_edit_distance_lookup)
            # Checks first uppercase to conserve the case.
            upperfirst = word[0].isupper()
            # Checks for correction suggestions.
            if len(suggestions) > 0:
                correction = suggestions[0].term
                replacement = correction
            # We call our _reduce_exaggerations function if no suggestion is found. Maybe there are repeated chars.
            else:
                replacement = _reduce_exaggerations(word)
            # Takes the case back to the word.
            if upperfirst:
                replacement = replacement[0].upper() + replacement[1:]
            word_token.repr = replacement
            token_list[word_pos] = word_token
    return token_list


def _reduce_exaggerations(text):
    """
    Auxiliary function to help with exxagerated words.
    Examples:
        woooooords -> words
        yaaaaaaaaaaaaaaay -> yay
    """
    correction = str(text)
    # TODO work on complexity reduction.
    return re.sub(r'([\w])\1+', r'\1', correction)


def is_numeric(text):
    for char in text:
        if not (char in "0123456789" or char in ",%.$"):
            return False
    return True


# A Singleton class to ensure that the dictionary is loaded to memory only once (reduces load time A LOT).
class SysmspellSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            ##Symspell configuration
            max_edit_distance_dictionary = 3
            prefix_length = 4
            spellchecker = SymSpell(max_edit_distance_dictionary, prefix_length)
            dictionary_path = pkg_resources.resource_filename(
                "symspellpy", "frequency_dictionary_en_82_765.txt")
            bigram_path = pkg_resources.resource_filename(
                "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
            spellchecker.load_dictionary(dictionary_path, term_index=0, count_index=1)
            spellchecker.load_bigram_dictionary(dictionary_path, term_index=0, count_index=2)
            cls._instance = spellchecker
        return cls._instance


class Normalizer:
    """
    The basic Normalizer object. It houses many different normalizer methods for different inputs.
    The normalization steps are defined in the instantiation and defaults to 'simplify_punctuation', 'normalize_whitespace', 'normalize_contractions', 'spell_correction'.
    Other functions are available in the class attribute normalization_functions.
    -----------------
    Class Attributes:
    -----------------
    normalization_functions: dict of function
        Offer name based access to the available normalization functions.
    """

    pre_tokenization_functions = {'simplify_punctuation': simplify_punctuation,
                                  'normalize_whitespace': normalize_whitespace}
    post_tokenization_functions = {'normalize_contractions': normalize_contractions,
                                   'spell_correction': spell_correction,
                                   'remove_stopwords': remove_stopwords}

    def __init__(self, pre_tokenization_steps=['simplify_punctuation', 'normalize_whitespace'],
                 post_tokenization_steps=['normalize_contractions', 'spell_correction']):
        """
        -----------
        Attributes:
        -----------
        steps: list of function
            A list of normalization functions - order matters. Default: simplify_punctuation, normalize_whitespace, normalize_contractions, spell_correction.
        """

        self.pre_tokenization_steps = [self.pre_tokenization_functions[step] for step in pre_tokenization_steps]
        self.post_tokenization_steps = [self.post_tokenization_functions[step] for step in post_tokenization_steps]

    def normalize_string(self, input_string):
        """
        Core normalization  function. Does basic normalization over strings. Used by other normalization functions such as normalize_document and normalize_sentence.
        -----------
        Attributes:
        -----------
        input_document: string
            string to be normalized.

        """

        if input_string is None:
            return ''
        normalized_string = str(input_string)
        for pre_tokenization_step in self.pre_tokenization_steps:
            normalized_string = pre_tokenization_step(normalized_string)
        tokens = tokenize(normalized_string)
        for post_tokenization_step in self.post_tokenization_steps:
            tokens = post_tokenization_step(tokens)
        return untokenize(tokens)

    def normalize_document(self, input_document):
        """
        Does basic normalization on Document objects. This should not be used after tagging since it loses all tags.
        -----------
        Attributes:
        -----------
        input_document: Document
            Document to be normalized.
        """

        warnings.warn(
            "This function can imply in data loss and reverts all lemmatization and pos tagging process. It is recomended that any text is normalized prior to tokenization.")
        if not isinstance(input_document, Document):
            raise TypeError(
                message="Wrong argument provided. Please, ensure that the input is of type core.structures.Document")
        sentences = input_document.sentences
        new_sentences = []
        for sentence in sentences:
            new_sentences.append(self.normalize_string(sentence))
        new_raw_document = " ".join(new_sentences)
        return Document(new_raw_document.strip(" "))

    def normalize_sentence(self, input_sentence):
        """
        Does basic normalization on Sentence objects. Should only be used on standalone sentences, since it breaks relation with parent Document.
        -----------
        Attributes:
        -----------
        input_sentence: Sentence
            The input sentence to be normalized
        """

        warnings.warn(
            "This function can imply in data loss and reverts all lemmatization and pos tagging process. Also, it creates a standalone sentence in relation to parent Document. It is recomended that any text is normalized prior to tokenization.")
        if not isinstance(input_sentence, Sentence):
            raise TypeError(
                message="Wrong argument provided. Please, ensure that the input is of type core.structures.Sentence")
        raw_sentence = input_sentence.get()
        raw_sentence = self.normalize_string(raw_sentence)
        return sentencize(raw_sentence)[0]

    def normalize_raw_document(self, document_path):
        """
        Does basic normalization over a txt document. For use in batch processes.
        -----------
        Attributes:
        -----------
        document_path: str (path)
            Path to the text document to be normalized.
        """

        with open(document_path) as f:
            lines = f.read()
        document_to_normalize = Document(lines)
        normalized_document = self.normalize_document(document_to_normalize)

        return normalized_document.raw
