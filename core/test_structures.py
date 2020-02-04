import pytest

from .structures import Document, sentencize, tokenize

def test_Document_Token_Sentence():
    """
    This test is design to assure that the main structures, Document, Sentence and Token are working as expected. Also, tokenization and
    sentencizing is tested through built-in processes. It is also designed to test the functionality of useful magic functions.
    """
    document = Document('All human beings are born free and equal in dignity and rights.')
    assert document.raw == ('All human beings are born free and equal in dignity and rights.')
    assert document.sentences[0] == 'All human beings are born free and equal in dignity and rights.'
    assert document[0] == 'All human beings are born free and equal in dignity and rights.'
    assert len(document.sentences) == 1
    document = Document('All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.')
    assert len(document.sentences) == 2
    assert document.sentences[0] == 'All human beings are born free and equal in dignity and rights.'
    assert len(document.sentences[0].tokens) == 15
    assert document.sentences[1] == 'They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.'
    assert document.sentences[0].next_sentence == document.sentences[1]
    assert document.sentences[1].previous_sentence == document.sentences[0]
    assert document.sentences[0].tokens[0] == '<SOS>'
    assert document[0][0] == '<SOS>'
    assert document.sentences[0].tokens[1] == 'All'
    assert document.sentences[0].tokens[-2] == '.'
    document = Document('The number of pi is usually summarized to 3.14 for the sake of simplicity. The greek letter pi was adopted by William Jones in 1706. Nice, right?')
    assert len(document.sentences) == 3
    assert document.sentences[2] == "Nice, right?"
    assert len(document.sentences[0].tokens) == 17

def test_sentencize():
    """
    This test is designed to verify the direct functioning of the sentencize function with some use cases.
    """
    text = 'All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood...'
    assert len(sentencize(text)) == 2
    text = 'The number of pi is usually summarized to 3.14 for the sake of simplicity. The greek letter pi was adopted by William Jones in 1706. Nice, right? All human beings are born free and equal in dignity and rights. .15 ... okay. All human beings are born free and equal in dignity and rights. ok . a'
    assert len(sentencize(text)) == 9

def test_tokenize():
    """
    This test is designed to verify the direct functioning of the tokenize function with some use cases. It is also designed to test internal functioning of Token creation.
    """
    sentence = 'The number of pi is usually summarized to 3.14 for the sake of simplicity.'
    tokens = tokenize(sentence)
    assert len(tokens) == 17
    assert tokens[-2].next_token.EOS==True
    assert tokens[1].previous_token.SOS==True
    assert tokens[3].next_token==tokens[4]
    assert tokens[4].previous_token == tokens[3]
    assert tokens[-2]=='.'
