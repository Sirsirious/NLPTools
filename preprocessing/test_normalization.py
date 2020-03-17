import pytest

from .normalization import Normalizer

def test_spell_correction():
    normalizer = Normalizer()
    cases = ['i ate a bsnana', 'okaaaaay my friind', 'this is goood']
    expected = ['i ate a banana', 'okay my friend', 'this is good']
    for case_num in range(len(cases)):
        assert normalizer.spell_correction(cases[case_num])==expected[case_num]

def test_spell_correction_empty_wrong_format():
    normalizer = Normalizer()
    cases = ['', None, 1]
    expected = ['', '', '1']
    for case_num in range(len(cases)):
        assert normalizer.spell_correction(cases[case_num])==expected[case_num]

""" This test takes too long
def test_spell_correction_no_spaces():
    normalizer = Normalizer()
    cases = ['iforgottoaddspaceswhenwriting']
    expected = ['iforgotoadspaceswhenwriting']
    for case_num in range(len(cases)):
        assert normalizer.spell_correction(cases[case_num])==expected[case_num]
"""

def test_simplify_punctuation():
    normalizer = Normalizer()
    cases = ['.','...','!!!!','!?','???????????','....']
    expected = ['.','...','!','!?','?','...']
    for case_num in range(len(cases)):
        assert normalizer.simplify_punctuation(cases[case_num])==expected[case_num]

def test_simplify_punctuation_wrong_format():
    normalizer = Normalizer()
    cases = ['', None, 1]
    expected = ['', '', '1']
    for case_num in range(len(cases)):
        assert normalizer.simplify_punctuation(cases[case_num])==expected[case_num]
