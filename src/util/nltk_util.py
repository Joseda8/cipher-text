import nltk
from nltk.corpus import gutenberg

from collections import Counter
from enum import Enum
import re


class Language(Enum):
    eng = 1
    spa = 2

# Function to download a resource if not available
def download_resource(resource):
    try:
        nltk.data.find(resource_name=resource, paths='~/nltk_data')
    except LookupError:
        nltk.download(resource)

# Download required resources
def download_required_resources():
    download_resource('gutenberg')

# Function to calculate n-gram frequencies using the new ngrams function
def calculate_ngram_freq(text, type):
    if type == "unigrams":
        ngrams_list = [letter.lower() for letter in text]
    elif type == "bigrams":
        ngrams_list = list(ngrams(2, text))
    elif type == "trigrams":
        ngrams_list = list(ngrams(3, text))

    # Calculate the frequency distribution using the Counter class
    freq_dist = Counter(ngrams_list)
    return freq_dist

# Function to generate n-grams from text
def ngrams(n, text):
    for i in range(len(text) - n + 1):
        if not re.search(r'\s', text[i:i+n]):
            yield text[i:i+n]

# Function to get a long text in a specified language
def get_long_text(language):
    if language == Language.eng:
        long_text = gutenberg.raw('bryant-stories.txt') + gutenberg.raw('austen-persuasion.txt') + gutenberg.raw('melville-moby_dick.txt')
    elif language == Language.spa:
        long_text = gutenberg.raw('don_quijote.txt') + gutenberg.raw('cosas_nuevas.txt')
    else:
        raise ValueError("Invalid language specified")
    return long_text
