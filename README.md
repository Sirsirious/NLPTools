[![Build Status](https://travis-ci.com/Sirsirious/NLPTools.svg?branch=master)](https://travis-ci.com/Sirsirious/NLPTools)
[![codecov](https://codecov.io/gh/Sirsirious/NLPTools/branch/master/graph/badge.svg?token=YKCP2INQIR)](https://codecov.io/gh/Sirsirious/NLPTools)

# [nlptools] Python NLP Tools
> A straightforward Natural Language Processing Toolbox

NLP Tools is a set of tools written in python that covers the most common NLP tasks with an easy and clear to understand style of code. 

It is being developed together with a Series of Articles about NLP by the main author in Medium. You can find the articles at 
[tfduque.medium.com](tfduque.medium.com)

## Installation

Installing with pip

```sh
pip install nlpytools
```

## Usage example
### Tokenization
* Using the tokenizer:
```python
from nlptools.core.structures import tokenize

tokenize("This is a sentence")
```
```sh
[<SOS>, this, is, a, sentence, <EOS>]
```

* Using sentence/document format:
```python
from nlptools.core.structures import Document
doc = Document("This is a sentence. This is another sentence.")

for sentence in doc:
    print(sentence, sentence.tokens)
```
```sh
This is a sentence. [<SOS>, This, is, a, sentence, ., <EOS>]
This is another sentence. [<SOS>, This, is, another, sentence, ., <EOS>]
```
### Normalization
These are the currently available normalization steps:
```python
pre_tokenization_functions = {'simplify_punctuation': simplify_punctuation,
                                  'normalize_whitespace': normalize_whitespace}
post_tokenization_functions = {'normalize_contractions': normalize_contractions,
                               'spell_correction': spell_correction,
                               'remove_stopwords': remove_stopwords}
```
Usage:
```python
from nlptools.preprocessing.normalization import Normalizer
normalizer = Normalizer(pre_tokenization_steps=['simplify_punctuation', 'normalize_whitespace'],
                        post_tokenization_steps=['normalize_contractions', 'spell_correction'])
norm.normalize_string("This is a nnormalized sentence!!!!         Yeah,,!!") # one can also use normalize_document
```
```sh
'This is a normalized sentence! Yeah,!'
```
### Stemming:
```python
from nlptools.preprocessing.stemming import PorterStemmer
from nlptools.core.structures import tokenize
stemmer = PorterStemmer()
tokens = tokenize("The words in this sentence will be stemmed.")
stemmed_tokens = [stemmer.stem(token) for token in tokens]
```
```sh
['<sos>', 'the', 'word', 'in', 'thi', 'sent', 'will', 'be', 'stem', '.', '<eos>']
```

### Lemmatizing and Tagging
First: tagging
```python
from nlptools.preprocessing.tagging import MLTagger
tagger = MLTagger()
tag_pairs = tagger.tag("Tag this sentence")
for tag in tag_pairs:
     print(tag, tag.PoS)
```
```python
<SOS> None
Tag NNP
this DT
sentence NN
<EOS> None
```
Every token carries its own Part of Speech in the PoS attribute after the tagging.

Then, after tagging, we can do Lemmatization
```python
from nlptools.preprocessing.tagging import MLTagger
tagger = MLTagger(force_ud=True) # Force UD format to use compatible tags
tag_pairs = tagger.tag("The cars are running")
lemmatized_words = [lemmatizer.lemmatize(word, word.PoS) for word in tag_pairs.tokens]
print(" ".join(lemmatized_words[1:-1]))
```
```sh
the car are run
```
### Featurization
```python
from nlptools.preprocessing.featurization import Tfidf
tfidf = Tfidf()
tfidf.fit(["The first sentence", "The second sentence", "The third sentence", "First, second, third."])
tfidf.transform(["The first sentence", "The second sentence", "The third sentence", "First, second, third."]) #or just go with fit_transform
```
```sh
matrix([[0.30543024, 0.        , 0.        , 0.        , 0.        ,
         0.07438118, 0.        , 0.07438118],
        [0.        , 0.30543024, 0.        , 0.        , 0.        ,
```
_For more examples and usage, please refer to the [medium series](https://tfduque.medium.com/dissecting-natural-language-processing-layer-by-layer-an-introductory-overview-d11cfff4f329)._

## Release History

* 0.1.0
    * Pypi release

## Meta

Tiago Duque – [medium website](tfduque.medium.com)

Distributed under the MIT license. See ``LICENSE`` for more information.

[Check me at github](https://github.com/Sirsirious)

[Check me at Linkedin](https://www.linkedin.com/in/tfduque/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Write understandable code!!!
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request
