import os
import re
from collections import Counter
from enum import Enum
from typing import Union, List

import nltk
from nltk.util import ngrams

class Language(Enum):
    eng = 1
    spa = 2

def language_type(language_str: str) -> Language:
    """
    Converts a string into a Language enum member.

    :param language_str: The string representation of the Language enum.
    :return: The corresponding Language enum member.
    :raises: ValueError if an invalid Language value is provided.
    """
    try:
        return Language[language_str]
    except KeyError:
        raise ValueError(f"Invalid Language value: {language_str}")

def download_resource(resource: str) -> None:
    """
    Downloads the specified NLTK resource if not already available.

    :param resource: The name of the NLTK resource.
    """
    try:
        nltk.data.find(resource_name=resource, paths="~/nltk_data")
    except LookupError:
        nltk.download(resource)

def download_required_resources() -> None:
    """
    Downloads the required NLTK resources for the script.
    """
    download_resource("gutenberg")

def calculate_ngram_freq(text: str, ngram_type: str) -> Counter:
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

def ngrams(n: int, text: str) -> List[str]:
    """
    Generates n-grams from the given text.

    :param n: The size of the n-grams.
    :param text: The input text.
    :return: The generated n-grams.
    """
    for start_index in range(len(text) - n + 1):
        end_index = start_index + n
        if not re.search(r"\s", text[start_index:end_index]):
            yield text[start_index:end_index]

def get_long_text(language: Language) -> Union[str, None]:
    """
    Retrieves a long text in the specified language.

    :param language: The target language (Language enum).
    :return: The concatenated long text.
    :raises: ValueError if an invalid language is specified.
    """
    try:
        # Define file names based on the specified language
        if language == Language.eng:
            files = ["bryant-stories.txt", "austen-persuasion.txt", "melville-moby_dick.txt"]
        elif language == Language.spa:
            files = ["don_quijote.txt", "cosas_nuevas.txt", "garcia_marques.txt"]
        else:
            raise ValueError("Invalid language specified")

        # Get the NLTK data directory path and set the corpus relative path
        nltk_data_dir = nltk.data.path[0]
        corpus_relative_path = "corpora/gutenberg"
        corpus_root = os.path.join(nltk_data_dir, corpus_relative_path)

        # Initialize an empty string to store the concatenated long text
        long_text = ""

        # Iterate over the selected files for the specified language
        for file_name in files:
            full_path = os.path.join(corpus_root, file_name)

            # Open each file and append its content to the long_text string
            with open(full_path, "r", encoding="utf-8") as file:
                long_text += file.read()

        return long_text

    except ValueError as e:
        raise ValueError("Invalid language specified")
