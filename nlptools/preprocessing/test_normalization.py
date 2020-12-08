import pytest
from pytest import raises
import os, sys

from .normalization import *
from ..core.structures import Document, Sentence, untokenize

test_case_folder = os.path.join(os.path.dirname(__file__), "../test_cases/")

def test_spell_correction():
    cases = ['i ate a bsnana', 'okaaaaay my friind', 'this is goood', 'yaaaaaaaaaaaaaay']
    expected = ['i ate a banana', 'okay my friend', 'this is good', 'yay']
    for case_num in range(len(cases)):
        tokenized = tokenize(cases[case_num])
        assert untokenize(spell_correction(tokenized))==expected[case_num]

""" This test takes too long
def test_spell_correction_no_spaces():
    normalizer = Normalizer()
    cases = ['iforgottoaddspaceswhenwriting']
    expected = ['iforgotoadspaceswhenwriting']
    for case_num in range(len(cases)):
        assert normalizer.spell_correction(cases[case_num])==expected[case_num]
"""

def test_simplify_punctuation():
    cases = ['.','...','!!!!','!?','???????????','....']
    expected = ['.','...','!','!?','?','...']
    for case_num in range(len(cases)):
        assert simplify_punctuation(cases[case_num])==expected[case_num]

def test_simplify_punctuation_wrong_format():
    cases = ['', None, 1]
    expected = ['', '', '1']
    for case_num in range(len(cases)):
        assert simplify_punctuation(cases[case_num])==expected[case_num]

def test_normalize_contractions():
    cases = ["ain't", "isn't", "you've", "hasnt", "that's his", "i'm"]
    expected = ["are not", "is not", "you have", "has not", "that is his", "I am"]
    for case_num in range(len(cases)):
        tokenized = tokenize(cases[case_num])
        assert untokenize(normalize_contractions(tokenized))==expected[case_num]

def test_normalize_whitespace():
    cases = [" ", "this  is it", "        ", " i am not here", "okay       ", "very      good"]
    expected = ["", "this is it", "", "i am not here", "okay", "very good"]
    for case_num in range(len(cases)):
        assert normalize_whitespace(cases[case_num])==expected[case_num]

def test_remove_stopwords():
    cases = ["this is good", "my cat", "of course it is", "this is really bad"]
    expected = ["good", "cat", "course", "really bad"]
    for case_num in range(len(cases)):
        tokenized = tokenize(cases[case_num])
        assert untokenize(remove_stopwords(tokenized))==expected[case_num]

def test_basic_string_normalization():
    normalizer = Normalizer()
    case = "Thiis is a normalized  sentence. Yaaaaaay!!!!!"
    expected = "This is a normalized sentence. Yay!"
    assert normalizer.normalize_string(case) == expected

def test_document_normalization():
    normalizer = Normalizer()
    doc_string = "Thiis is a not nnormalised string that will become a document. This is the aecond sentence   of the document."
    document = Document(doc_string)
    expected_raw = "This is a not normalised string that will become a document. This is the second sentence of the document."
    document = normalizer.normalize_document(document)
    assert document.raw == expected_raw

def test_wrong_document_normalization():
    normalizer = Normalizer()
    doc_string = "Thiis is a not nnormalised string that will become a document. This is the aecond sentence   of the document."
    raises(TypeError, normalizer.normalize_document, doc_string)

def test_sentence_normalization():
    normalizer = Normalizer()
    doc_string = "Thiis is a not nnormalised string that will become a document."
    sentence = sentencize(doc_string)[0]
    expected_raw = "This is a not normalised string that will become a document."
    sentence = normalizer.normalize_sentence(sentence)
    assert sentence.get() == expected_raw

def test_wrong_sentence_normalization():
    normalizer = Normalizer()
    doc_string = "Thiis is a not nnormalised string that will become a document. This is the aecond sentence   of the document."
    raises(TypeError, normalizer.normalize_document, doc_string)

#TODO fix \n not appearning
def test_raw_document_normalization():
    normalizer=Normalizer()
    case = normalizer.normalize_raw_document(test_case_folder+"test_normalize_document_file.txt")
    expected = open(test_case_folder+"test_normalize_document_expected.txt").read()
    assert case == expected
