import pytest
from .lemmatization import DictionaryLemmatizer

def test_dictionary_lemmatizer_basic():
    lemmatizer = DictionaryLemmatizer()
    word = "living"
    pos = "VERB"
    result = "live"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_empty():
    lemmatizer = DictionaryLemmatizer()
    word = ""
    pos = ""
    result = ""
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_empty_word():
    lemmatizer = DictionaryLemmatizer()
    word = ""
    pos = "NOUN"
    result = ""
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_empty_pos():
    lemmatizer = DictionaryLemmatizer()
    word = "Butterfly"
    pos = ""
    result = "butterfly"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_unexisting_pos():
    lemmatizer = DictionaryLemmatizer()
    word = "Butterfly"
    pos = "DOG"
    result = "butterfly"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_number():
    lemmatizer = DictionaryLemmatizer()
    word = 3
    pos = "NUM"
    result = "3"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_POS_number():
    lemmatizer = DictionaryLemmatizer()
    word = 3
    pos = 9
    result = "3"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_lowercase_pos():
    lemmatizer = DictionaryLemmatizer()
    word = "purchases"
    pos = "verb"
    result = "purchase"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_None():
    lemmatizer = DictionaryLemmatizer()
    word = None
    pos = "verb"
    result = ""
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_multiword():
    lemmatizer = DictionaryLemmatizer()
    word = "this is a multiword string"
    pos = "NOUN"
    result = "this is a multiword string"
    assert lemmatizer.lemmatize(word, pos) == result

def test_dictionary_lemmatizer_noun():
    lemmatizer = DictionaryLemmatizer()
    word = "cats"
    pos = "NOUN"
    result = "cat"
    assert lemmatizer.lemmatize(word, pos) == result
