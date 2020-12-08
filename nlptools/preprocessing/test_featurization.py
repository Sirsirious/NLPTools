from pytest import raises
from ..core.structures import Document, Sentence
import os
from nlptools.preprocessing.featurization import *

EXAMPLE_DOCUMENT="This is an example document made out of many sentences. This is the second sentence. This is the third sentence. Finally, another sentence with another another is. Very good to have some interesting sentences, isn't it? Adding another sentence can be tedious, but it is necessary. And, finally, another one! Should I continue? Maybe it is important that I keep adding sentences for testing. Good that you feel it amazing!"

def test_gtf_document():
    document = Document(EXAMPLE_DOCUMENT)
    case = global_term_frequency(document)
    assert isinstance(case, dict)
    assert len(case) > 0

def test_gtf_sentence():
    sent = "This is an example document made out of many sentences"
    case = term_frequency(Sentence(0, len(sent), sent))
    assert isinstance(case, dict)
    assert len(case) > 0

def test_bowfeaturizer():
    document = Document(EXAMPLE_DOCUMENT)
    bow = Bow()
    bow.fit(document)
    numpy_data = bow.transform(document)
    assert numpy_data.shape == (len(document),len(bow.word_indexes))

def test_bowfeaturizer_fit_transform():
    document = Document(EXAMPLE_DOCUMENT)
    bow = Bow()
    numpy_data = bow.fit_transform(document)
    assert numpy_data.shape == (len(document),len(bow.word_indexes))
    another = "This is another sentence used to test the bow vectorizer."
    new_data = bow.transform(another)
    assert new_data.shape == (len(bow.word_indexes),)

def test_transform_before_fit():
    data = Document("This is a very simple document.")
    bow = Bow()
    raises(AttributeError, bow.transform, data)

def test_raises_fit():
    data = {'dict':'fake'}
    bow = Bow()
    raises(TypeError,bow.fit,data)

def test_tf_idf_single():
    document = Document(EXAMPLE_DOCUMENT)
    tfidf = Tfidf(lower_case = True)
    tfidf.fit(document)
    test_sentence = "This is good, actually, it is amazing! Please, give me more!"
    array = tfidf.transform(Sentence(0, len(test_sentence), test_sentence))
    print(array)
    assert array.shape == (len(tfidf.word_indexes),)

def test_tf_idf_full_doc():
    document = Document(EXAMPLE_DOCUMENT)
    tfidf = Tfidf(lower_case = True)
    matrix = tfidf.fit_transform(document)
    print(matrix)
    assert matrix.shape == (len(document), len(tfidf.word_indexes))

def test_fit_none():
    doc = None
    tfidf = Tfidf()
    raises(TypeError, tfidf.fit_transform, doc)

def test_save_tfidf():
    file = os.path.join(os.path.dirname(__file__), "../../test_cases/tfidf_test.p")
    document = Document(EXAMPLE_DOCUMENT)
    tfidf = Tfidf(lower_case = True)
    tfidf.fit(document)
    tfidf.save_to_file(file)

def test_load_file():
    file = os.path.join(os.path.dirname(__file__), "../../test_cases/tfidf_test.p")
    test_save_tfidf()
    tfidf = Tfidf()
    tfidf.load_from_file(file)
    sentence = "This is good, actually, it is amazing! Please, give me more!"
    array = tfidf.transform(Sentence(0, len(sentence), sentence))
    assert array.shape == (len(tfidf.word_indexes),)
