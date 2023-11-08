from cache_data import cache_data
from nltk_util import download_required_resources, calculate_ngram_freq, get_long_text

# Download required resources
download_required_resources()

# NgramAnalyzer class
class NgramAnalyzer:
    def __init__(self, text_name="default", text=None, cache=True):

        if text is None:
            text = get_long_text()

        # Generate bigrams, trigrams, and single letters
        self.unigrams = cache_data(calculate_ngram_freq, f"{text_name}_unigram_freq", cache, text, "unigrams")
        self.bigrams = cache_data(calculate_ngram_freq, f"{text_name}_bigram_freq", cache, text, "bigrams")
        self.trigrams = cache_data(calculate_ngram_freq, f"{text_name}_trigram_freq", cache, text, "trigrams")
