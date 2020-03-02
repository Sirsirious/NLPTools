import pytest

from word_utils import inflect_noun_singular

def test_inflect_noun_simple():
    cases = ['cars','houses','books','birds','pencils']
    expected = ['car', 'house', 'book','bird','pencil']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_1rule():
    cases = ['kisses','wishes','matches','foxes','quizzes']
    expected = ['kiss', 'wish', 'match','fox','quiz']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_2rule():
    cases = ['boys','holidays','keys','guys']
    expected = ['boy', 'holiday', 'key','guy']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_3rule():
    cases = ['parties','ladies','stories','nannies', 'cities']
    expected = ['party','lady','story','nanny', 'city']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_4rule():
    cases = ['lives','leaves','thieves','wives']
    expected = ['life','leaf','thief','wife']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_5rule():
    cases = ['tomatoes','potatoes','echoes','heroes']
    expected = ['tomato','potato','echo','hero']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_irergular1():
    cases = ['men','women','children','feet','teeth','geese','mice']
    expected = ['man','woman','child','foot','tooth','goose','mouse']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_noun_irergular2():
    cases = ['fish','sheep','deer','moose','aircraft']
    expected = ['fish','sheep','deer','moose','aircraft']
    obtained = [inflect_noun_singular(word) for word in cases]
    assert expected == obtained

def test_inflect_empty():
    cases = ''
    expected = ''
    assert inflect_noun_singular(cases) == expected

def test_inflect_num():
    cases = 3
    expected = '3'
    assert inflect_noun_singular(cases) == expected
