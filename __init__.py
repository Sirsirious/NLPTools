import sys

from .core.structures import Document
from .preprocessing.tagging import MLTagger
from .preprocessing.stemming import PorterStemmer

def process(raw_document, pipeline = ['sentencize','pos','stemming']):
    document = raw_document
    if 'sentencize' in pipeline:
        document = Document(document)
    if 'pos' in pipeline:
        tagger = MLTagger()
        if isinstance(document, Document):
            sentences = [tagger.tag(sentence) for sentence in document]
            document.sentences = sentences
        else:
            document = tagger.tag(document)
    if 'stemming' in pipeline:
        stemmer = PorterStemmer()
        if isinstance(document, Document):
            for sentence in document.sentences:
                for token_idx in range(len(sentence)):
                    sentence[token_idx].repr = stemmer.stem(sentence[token_idx])
        else:
            for token_idx in range(len(document)):
                document[token_idx] = stemmer.stem(sentence[token_idx])
    return document
