# nltk_util.py

import nltk
from nltk.corpus import gutenberg

from collections import Counter
import re

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

# Function to get a long text in English
def get_long_text():
    long_text = gutenberg.raw('bryant-stories.txt') + gutenberg.raw('austen-persuasion.txt') + gutenberg.raw('melville-moby_dick.txt')
    return long_text
