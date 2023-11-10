import re
from collections import Counter
from enum import Enum

import nltk
from nltk.corpus import gutenberg


class Language(Enum):
    eng = 1
    spa = 2

def language_type(value):
    """
    Converts a string into a Language enum member.

    :param value: The string representation of the Language enum.
    :return: The corresponding Language enum member.
    :raises: KeyError if an invalid Language value is provided.
    """
    try:
        return Language[value]
    except KeyError:
        raise ValueError(f"Invalid Language value: {value}")

def download_resource(resource):
    """
    Downloads the specified NLTK resource if not already available.

    :param resource: The name of the NLTK resource.
    """
    try:
        nltk.data.find(resource_name=resource, paths='~/nltk_data')
    except LookupError:
        nltk.download(resource)

def download_required_resources():
    """
    Downloads the required NLTK resources for the script.
    """
    download_resource('gutenberg')

def calculate_ngram_freq(text, ngram_type):
    """
    Calculates the frequency distribution of n-grams in the given text.

    :param text: The input text.
    :param ngram_type: The type of n-gram ("unigrams", "bigrams", or "trigrams").
    :return: A Counter object representing the frequency distribution of n-grams.
    """
    if ngram_type == "unigrams":
        ngrams_list = [letter.lower() for letter in text]
    elif ngram_type == "bigrams":
        ngrams_list = list(ngrams(2, text))
    elif ngram_type == "trigrams":
        ngrams_list = list(ngrams(3, text))

    # Calculate the frequency distribution using the Counter class
    freq_dist = Counter(ngrams_list)
    return freq_dist

def ngrams(n, text):
    """
    Generates n-grams from the given text.

    :param n: The size of the n-grams.
    :param text: The input text.
    :yield: The generated n-grams.
    """
    for i in range(len(text) - n + 1):
        if not re.search(r'\s', text[i:i+n]):
            yield text[i:i+n]

def get_long_text(language):
    """
    Retrieves a long text in the specified language.

    :param language: The target language (Language enum).
    :return: The concatenated long text.
    :raises: ValueError if an invalid language is specified.
    """
    if language == Language.eng:
        long_text = gutenberg.raw('bryant-stories.txt') + gutenberg.raw('austen-persuasion.txt') + gutenberg.raw('melville-moby_dick.txt')
    elif language == Language.spa:
        long_text = gutenberg.raw('don_quijote.txt') + gutenberg.raw('cosas_nuevas.txt')
    else:
        raise ValueError("Invalid language specified")
    return long_text
