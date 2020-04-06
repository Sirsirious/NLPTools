from pytest import raises
from ..core.structures import Document, Sentence
import numpy as np
from .featurization import *

EXAMPLE_DOCUMENT="This is an example document made out of many sentences. This is the second sentence. This is the third sentence. Finally, another sentence with another another. "

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
    bow = BagOfWords()
    bow.fit(document)
    numpy_data = bow.transform(document)
    assert numpy_data.shape == (len(document),bow.vocabulary_lenght)

def test_bowfeaturizer_fit_transform():
    document = Document(EXAMPLE_DOCUMENT)
    bow = BagOfWords()
    numpy_data = bow.fit_transform(document)
    assert numpy_data.shape == (len(document),bow.vocabulary_lenght)
    another = "This is another sentence used to test the bow vectorizer."
    new_data = bow.transform(another)
    assert new_data.shape == (bow.vocabulary_lenght,)
