"""Functions for reading the pronouncing dictionary and the poetry forms files
"""
from typing import TextIO
import re
from poetry_constants import (
    # CLEAN_POEM, WORD_PHONEMES, LINE_PRONUNCIATION, POEM_PRONUNCIATION,
    PRONOUNCING_DICTIONARY, POETRY_FORM, POETRY_FORMS)

SAMPLE_POETRY_FORM_FILE = '''Limerick
8 A
8 A
5 B
5 B
8 A

Haiku
5 *
7 * 
5 *
'''
EXPECTED_POETRY_FORMS = {
    'Haiku': ([5, 7, 5], ['*', '*', '*']),
    'Limerick': ([8, 8, 5, 5, 8], ['A', 'A', 'B', 'B', 'A'])
}

SAMPLE_DICTIONARY_FILE = ''';;; Comment line
ABSINTHE  AE1 B S IH0 N TH
HEART  HH AA1 R T
FONDER  F AA1 N D ER0
'''

EXPECTED_DICTIONARY = {
    'ABSINTHE': ['AE1', 'B', 'S', 'IH0', 'N', 'TH'],
    'HEART': ['HH', 'AA1', 'R', 'T', ],
    'FONDER': ['F', 'AA1', 'N', 'D', 'ER0']
}

SAMPLE_POEM_FILE = '''  Is this mic on?

Get off my lawn.
'''


def read_and_trim_whitespace(poem_file: TextIO) -> str:
    """Return a string containing the poem in poem_file, with
     blank lines and leading and trailing whitespace removed.

     >>> poem_file = io.StringIO(SAMPLE_POEM_FILE)
     >>> read_and_trim_whitespace(poem_file)
     'Is this mic on?\\n Get off my lawn.'
     """
    result = ''
    result_lines = poem_file.readlines()
    for line in result_lines:
        if line != '\n':
            result += line
    result = result.strip()
    # result = result.replace('\n', '\\n')
    return result


def read_pronouncing_dictionary(
        pronunciation_file: TextIO) -> PRONOUNCING_DICTIONARY:
    """Read pronunciation_file, which is in the format of the CMU Pronouncing
    Dictionary, and return the pronunciation dictionary.

    >>> dict_file = io.StringIO(SAMPLE_DICTIONARY_FILE)
    >>> result = read_pronouncing_dictionary(dict_file)
    >>> result == EXPECTED_DICTIONARY
    True
    """
    Dic_result = {}
    result_lines = pronunciation_file.readlines()
    for line in result_lines:
        if(line.startswith(";")):
            result_lines.remove(line)
    

    for line in result_lines:
         line_word = re.split(' +', line.strip())
         key = line_word[0]
         del(line_word[0])
         Dic_result[key] = line_word

    return Dic_result

def read_poetry_form_descriptions(poetry_forms_file: TextIO) -> POETRY_FORMS:
    """Return a dictionary of poetry form name to poetry pattern for the poetry
    forms in poetry_forms_file.

    >>> form_file = io.StringIO(SAMPLE_POETRY_FORM_FILE)
    >>> result = read_poetry_form_descriptions(form_file)
    >>> result == EXPECTED_POETRY_FORMS
    True
    """
    value = ()
    list1 = []
    list2 = []
    Dic_result = {}
    key = ''
    for lines in poetry_forms_file.readlines():
        if lines == '\n':
            value = (list1, list2)
            Dic_result[key] = value
            list1 = []
            list2 = []

        if lines[0].isalpha():
            key = lines.strip()

        if lines[0].isdigit():
            num_char = re.split(' +', lines.strip())
            list1.append(int(num_char[0]))
            list2.append(num_char[1])

    value = (list1, list2)
    Dic_result[key] = value
    return Dic_result
