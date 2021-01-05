import pytest

from .stemming import PorterStemmer

def test_porterstemmer():
    stemmer = PorterStemmer()
    #Paper Test Cases
    cases = [('caresses','caress'), ('ponies','poni'), ('ties','ti'), ('caress','caress'), ('cats','cat'),
             ('feed','feed'), ('agreed','agre'), ('plastered','plast'), ('bled','bled'), ('motoring','motor'),
             ('sing','sing'), ('sized','size'), ('hopping','hop'), ('tanned','tan'), ('falling','fall'),
             ('hissing','hiss'), ('fizzed','fizz'), ('failing','fail'), ('filing','file'), ('happy','happi'),
             ('sky','sky'), ('revival','reviv'), ('allowance','allow'), ('inference','infer'),
             ('airliner','airlin'), ('gyroscopic','gyroscop'), ('adjustable','adjust'), ('defensible','defens'),
             ('irritant','irrit'), ('replacement','replac'), ('adjustment','adjust'), ('dependent','depend'),
             ('adoption','adopt'), ('homologou','homolog'), ('communism','commun'), ('activate','activ'),
             ('angulariti','angular'), ('homologous','homolog'), ('effective','effect'),
             ('bowdlerize','bowdler'), ('probate','prob'), ('rate','rate'), ('cease','ceas'),
             ('controll','control'), ('roll','roll')]

    for word, stem in cases:
        assert stemmer.stem(word) == stem
