"""Helper functions for the poetry.py program.
"""

from typing import List
from typing import Tuple
from typing import Dict
import re

from poetry_constants import (
    CLEAN_POEM, WORD_PHONEMES, LINE_PRONUNCIATION, POEM_PRONUNCIATION,
    PRONOUNCING_DICTIONARY)


# ===================== Helper Functions =====================


def clean_word(s: str) -> str:
    """Return a new string based on s in which all letters have been converted
    to uppercase and whitespace and punctuation characters have been stripped
    from both ends. Inner punctuation and whitespace is left untouched.

    >>> clean_word('Birthday!!!')
    'BIRTHDAY'
    >>> clean_word('  "Quoted?"\\n\\n\\n')
    'QUOTED'
    """

    punctuation = """!"'`@$%^&_-+={}|\\/,;:.-?)([]<>*#\n\t\r """
    result = s.upper().strip(punctuation)
    return result



def clean_poem(raw_poem: str) -> CLEAN_POEM:
    r"""Return the non-blank, non-empty lines of poem, with whitespace removed
    from the beginning and end of each line and all words capitalized.
    
    >>> clean_poem('The first line leads off,\n\n\nWith a gap before the next.\n    Then the poem ends.\n')
    [['THE', 'FIRST', 'LINE', 'LEADS', 'OFF'], ['WITH', 'A', 'GAP', 'BEFORE', 'THE', 'NEXT'], ['THEN', 'THE', 'POEM', 'ENDS']]
    """
    temp = re.split('\\n+', raw_poem)
    if temp[-1] == '':
        del(temp[-1])

    result = []
    temp_result = []
    for sentences in temp:
        temp_result = []
        words = re.split(' ', sentences)
        for word in words:
            temp_word = clean_word(word)
            if temp_word != '':
                temp_result.append(temp_word)
        result.append(temp_result)

    return result
    pass


def extract_phonemes(
        cleaned_poem: CLEAN_POEM,
        word_to_phonemes: PRONOUNCING_DICTIONARY) -> POEM_PRONUNCIATION:
    """Return a list where each inner list contains the phonemes for the
    corresponding line of poem_lines.

    >>> word_to_phonemes = {'YES': ['Y', 'EH1', 'S'], 'NO': ['N', 'OW1']}
    >>> extract_phonemes([['YES'], ['NO', 'YES']], word_to_phonemes)
    [[['Y', 'EH1', 'S']], [['N', 'OW1'], ['Y', 'EH1', 'S']]]
    """
    result = []
    for line in cleaned_poem:
        temp_result = []
        for word in line:
            temp_result.append(word_to_phonemes[word])
        result.append(temp_result)

    return result
    pass


def phonemes_to_str(poem_pronunciation: POEM_PRONUNCIATION) -> str:
    """Return a string containing all the phonemes in each word in each line in
    poem_pronunciation. The phonemes are separated by spaces, the words are
    separated by ' | ', and the lines are separated by '\n'.

    >>> phonemes_to_str([[['Y', 'EH1', 'S']], [['N', 'OW1'], ['Y', 'EH1', 'S']]])
    'Y EH1 S\\nN OW1 | Y EH1 S'
    """
    str_result = ''
    for lines in poem_pronunciation:
        for word in lines:
            for prounce in word:
                str_result += prounce
                if prounce != word[-1]:
                    str_result += ' '
            if word != lines[-1]:
                str_result += ' | '
        if lines != a[-1]:
            str_result += '\\\\n'
    
    return str_result
    pass


def get_rhyme_scheme(poem_pronunciation: POEM_PRONUNCIATION) -> List[str]:
    """Return a list of last syllables from the poem described by
    poem_pronunction.

    Precondition: poem_pronunciation is not empty and each PHONEMES list
    contains at least one vowel phoneme.

    >>> get_rhyme_scheme([[['IH0', 'N']], [['S', 'IH0', 'N']]])
    ['A', 'A']
    """
    Rhyme = {}
    number = 65
    result = []
    for lines in poem_pronunciation:
        last_word = lines[-1]
        last_rhyme = last_word[-1]
        if last_rhyme not in Rhyme:
            Rhyme[last_rhyme] = chr(number)
            number += 1
        result.append(Rhyme[last_rhyme])
    return result
    pass

def count_syllables(Line: LINE_PRONUNCIATION) -> int:
    count = 0
    for word in Line:
        count += len(word)

    return count

def get_num_syllables(poem_pronunciation: POEM_PRONUNCIATION) -> List[int]:
    """Return a list of the number of syllables in each poem_pronunciation
    line.
    """
    result = []
    for lines in poem_pronunciation:
        result.append(count_syllables(lines))

    return result
    pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
