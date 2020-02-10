import string, sys
import re


class DummySentencizer:
    """
    The DummySentencizer is a simple way of sentencizing. It is based on default punctuation characters and uses a special token for splitting.

    Attributes
    ----------
    raw : str
        The raw text string passed as input to be sentencized.
    sentences : list of str
        The list of sentences after sentencizing.

    """

    def __init__(self, input_text, split_characters=['.','?','!',':'], delimiter_token='<SPLIT>'):
        """
        Parameters
        ----------
        input_text : str
            Text to be sentencized. Initialization immediately sentencizes the input text based on the input parameters.
        split_characters : list of str, optional
            List of characters to use as sentence splitter. Default to dot, question mark, exclamation mark and colon.
        delimiter_token : str, optional
            Token to be used to split text. Defaults to '<SPLIT>'. Can be changed if the token word is reserved.

        """

        self.sentences = []
        self.raw = str(input_text)
        self._split_characters=split_characters
        self._delimiter_token=delimiter_token
        self._index=0
        self._sentencize()

    def _sentencize(self):
        work_sentence = self.raw
        for character in self._split_characters:
            work_sentence = work_sentence.replace(character, character+""+self._delimiter_token)
        self.sentences = [x.strip() for x in work_sentence.split(self._delimiter_token) if x !='']

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.sentences):
            result = self.sentences[self._index]
            self._index+=1
            return result
        raise StopIteration

class DummyTokenizer:
    """
    The DummyTokenizer is a simple way of tokenizing. It is based on whitespaces and hyphens and uses a special token for splitting.
    It also does some processing to separate punctuation marks from words.

    Attributes
    ----------
    raw : str
        The raw text string passed as input to be tokenized.
    tokens : list of str
        The list of tokens after tokenization.

    """
    def __init__(self, sentence, token_boundaries=[' ', '-'], punctuations=string.punctuation, delimiter_token='<SPLIT>'):
        """
        Parameters
        ----------
        input_text : str
            Text to be tokenized. Initialization immediately tokenizes the input text based on the input parameters.
        token_boundaries : list of str, optional
            List of characters to use as token splitters. Default to whitespaces and hyphens.
        punctuation: str or list of str, optional
            Punctuation characters used for preprocessing punctuation marks from words. Defaults to string library punctuation attribute.
        delimiter_token : str, optional
            Token to be used to split text. Defaults to '<SPLIT>'. Can be changed if the token word is reserved.

        """
        self.tokens = []
        self.raw = str(sentence)
        self._token_boundaries = token_boundaries
        self._delimiter_token = delimiter_token
        self._punctuations = punctuations
        self._index = 0
        self._tokenize()

    def _tokenize(self):
        work_sentence = self.raw
        for punctuation in self._punctuations:
            work_sentence = work_sentence.replace(punctuation, " "+punctuation+" ")
        for delimiter in self._token_boundaries:
            work_sentence = work_sentence.replace(delimiter, self._delimiter_token)
        self.tokens = [x.strip() for x in work_sentence.split(self._delimiter_token) if x != '']

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.tokens):
            result = self.tokens[self._index]
            self._index+=1
            return result
        raise StopIteration
