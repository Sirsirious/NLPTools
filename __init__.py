from nlptools.core import Document
from nlptools.preprocessing.tagging import MLTagger
from nlptools.preprocessing.stemming import PorterStemmer
from nlptools.preprocessing import DictionaryLemmatizer

def process(raw_document, pipeline = ['sentencize','pos','lemmatization']):
    document = raw_document
    if 'sentencize' in pipeline:
        document = Document(document)
    if 'pos' in pipeline:
        tagger = MLTagger(force_ud=True)
        if isinstance(document, Document):
            sentences = [tagger.tag(sentence) for sentence in document]
            document.sentences = sentences
        else:
            document = tagger.tag(document)
    if 'lemmatization' in pipeline:
        lemmatizer = DictionaryLemmatizer()
        if isinstance(document, Document):
            for sentence in document.sentences:
                for token_idx in range(len(sentence)):
                    tag = sentence[token_idx].PoS if 'lemmatization' in pipeline else ''
                    sentence[token_idx].repr = lemmatizer.lemmatize(sentence[token_idx], tag)
        else:
            for token_idx in range(len(document)):
                tag = sentence[token_idx].PoS if 'lemmatization' in pipeline else ''
                document[token_idx] = lemmatizer.lemmatize(sentence[token_idx], sentence[token_idx].PoS)
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
