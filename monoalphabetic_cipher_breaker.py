import string
from collections import Counter
import nltk
from nltk.corpus import reuters
from nltk import FreqDist, bigrams

class MonoalphabeticCipherBreaker:
    """
    This class represents a breaker for the Monoalphabetic Substitution Cipher system.
    It uses frequency analysis to attempt to break the cipher and decipher the content.
    """

    def __init__(self, ngram_length: int):
        self.ngram_length = ngram_length
        self.language_ngram_freqs = self.get_language_ngram_freqs()

    def get_language_ngram_freqs(self):
        # Download the reuters corpus if not already present
        nltk.download('reuters')

        # Tokenize the words in the reuters corpus
        words = reuters.words()

        # Compute the bigram frequencies
        ngrams = list(nltk.ngrams(words, self.ngram_length))
        freq_dist = FreqDist(ngrams)

        # Normalize the frequencies to get probabilities
        total_ngrams = sum(freq_dist.values())
        ngram_probs = {ngram: count/total_ngrams for ngram, count in freq_dist.items()}

        return ngram_probs

    def break_cipher(self, ciphered_content: str) -> str:
        # Preprocess the content to remove punctuation and convert to lowercase
        content = ciphered_content.lower()
        content = ''.join([c for c in content if c in string.ascii_lowercase])

        # Count the n-gram frequencies in the ciphered content
        cipher_ngram_freqs = Counter([content[i:i+self.ngram_length] for i in range(len(content)-self.ngram_length+1)])

        # Try to match the n-grams in the ciphered content to the n-grams in the original language
        # This is a simple example and may not be very accurate
        substitutions = {}
        for ngram in cipher_ngram_freqs:
            if ngram in self.language_ngram_freqs:
                substitutions[ngram] = ngram

        # Perform the substitutions to try to decipher the content
        deciphered_content = ''
        for i in range(len(content)-self.ngram_length+1):
            ngram = content[i:i+self.ngram_length]
            if ngram in substitutions:
                deciphered_content += substitutions[ngram]
            else:
                deciphered_content += ngram

        return deciphered_content
