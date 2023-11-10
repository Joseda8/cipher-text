from src.util.cache_data import cache_data
from src.util.nltk_util import download_required_resources, calculate_ngram_freq, get_long_text, Language

# Download NLTK required resources
download_required_resources()


class NgramAnalyzer:
    """
    This class represents an Ngram Analyzer that generates unigrams, bigrams, and trigrams frequency distributions.
    """

    def __init__(self, text_name, language=Language.eng, text=None, cache=True):
        """
        Initializes the NgramAnalyzer instance.

        :param text_name: A name identifier for the text.
        :param language: The language for which to analyze n-grams (default is Language.eng).
        :param text: The input text for analysis (default is None, in which case a long text is used).
        :param cache: Flag indicating whether to use caching for calculated n-grams (default is True).
        """
        if text is None:
            text = get_long_text(language=language)

        # Generate bigrams, trigrams, and single letters
        self.unigrams = cache_data(calculate_ngram_freq, f"{text_name}_unigram_freq", cache, text, "unigrams")
        self.bigrams = cache_data(calculate_ngram_freq, f"{text_name}_bigram_freq", cache, text, "bigrams")
        self.trigrams = cache_data(calculate_ngram_freq, f"{text_name}_trigram_freq", cache, text, "trigrams")
