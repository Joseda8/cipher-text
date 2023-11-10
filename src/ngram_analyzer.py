from util.cache_data import cache_data
from util.nltk_util import download_required_resources, calculate_ngram_freq, get_long_text, Language

# Download NLTK required resources
download_required_resources()

# NgramAnalyzer class
class NgramAnalyzer:
    def __init__(self, text_name, language=Language.eng, text=None, cache=True):

        if text is None:
            text = get_long_text(language=language)

        # Generate bigrams, trigrams, and single letters
        self.unigrams = cache_data(calculate_ngram_freq, f"{text_name}_unigram_freq", cache, text, "unigrams")
        self.bigrams = cache_data(calculate_ngram_freq, f"{text_name}_bigram_freq", cache, text, "bigrams")
        self.trigrams = cache_data(calculate_ngram_freq, f"{text_name}_trigram_freq", cache, text, "trigrams")
