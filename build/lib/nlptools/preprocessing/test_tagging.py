import pytest

from .tagging import MLTagger

def test_penn_crf():
    tagger = MLTagger()
    sentence1 = "This is a sentence with a total of 11 words."
    sentence2 = "This expects at least 7 tags."
    assert len(tagger.tag(sentence1).tokens)-2 == 11
    assert len(tagger.tag(sentence2).tokens)-2 == 7
    tagged_sentence = tagger.tag(sentence1)
    for token_idx in range(1,len(tagged_sentence)-1):
        assert tagged_sentence.tokens[token_idx].PoS != None
    tagged_sentence = tagger.tag(sentence2)
    for token_idx in range(1,len(tagged_sentence)-1):
        assert tagged_sentence.tokens[token_idx].PoS != None

def test_ud_crf():
    tagger = MLTagger(model='ud_crf')
    sentence1 = "This is a sentence with a total of 11 words."
    sentence2 = "This expects at least 7 tags."
    assert len(tagger.tag(sentence1).tokens)-2 == 11
    assert len(tagger.tag(sentence2).tokens)-2 == 7
    tagged_sentence = tagger.tag(sentence1)
    for token_idx in range(1,len(tagged_sentence)-1):
        assert tagged_sentence.tokens[token_idx].PoS != None
    tagged_sentence = tagger.tag(sentence2)
    for token_idx in range(1,len(tagged_sentence)-1):
        assert tagged_sentence.tokens[token_idx].PoS != None
