import pytest

from .tokenization import DummySentencizer, DummyTokenizer

def test_dummysentencizer():
    sentences = DummySentencizer('All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.')
    assert sentences.sentences == ['All human beings are born free and equal in dignity and rights.','They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.']
    sentences = DummySentencizer('What is a tokenizer, a reader may ask? It is a NLP preprocessing task!')
    assert sentences.sentences == ['What is a tokenizer, a reader may ask?','It is a NLP preprocessing task!']
    sentences = DummySentencizer('This is a sentence without any punctuation mark')
    assert sentences.sentences == ['This is a sentence without any punctuation mark']
    sentences = DummySentencizer('This is a sentence: this is another sentence. A third sentence, oh my! Four? I dont believe it!',)
    assert sentences.sentences == ['This is a sentence:','this is another sentence.','A third sentence, oh my!','Four?','I dont believe it!']
    sentences = DummySentencizer('')
    assert sentences.sentences == []
    sentences = DummySentencizer(4)
    assert sentences.sentences == ['4']
    sentences = DummySentencizer('...')
    assert sentences.sentences == ['.','.','.']

def test_dummytokenizer():
    tokens = DummyTokenizer('All human beings are born free and equal in dignity and rights.')
    assert tokens.tokens == ['All','human', 'beings', 'are', 'born', 'free', 'and', 'equal', 'in', 'dignity', 'and', 'rights', '.']
    tokens = DummyTokenizer('...')
    assert tokens.tokens == ['.','.','.']
    tokens = DummyTokenizer(19.3)
    assert tokens.tokens == ['19','.','3']
    tokens = DummyTokenizer('')
    assert tokens.tokens == []
    tokens = DummyTokenizer(4)
    assert tokens.tokens == ['4']
