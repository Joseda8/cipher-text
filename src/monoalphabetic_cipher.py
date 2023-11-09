import itertools
import pandas as pd
from collections import Counter

from ngram_analyzer import NgramAnalyzer
from util.text_util import TextUtil


class MonoalphabeticCipherBreaker:
    """
    This class represents a Monoalphabetic Substitution Cipher breaker.
    It provides methods to break the cipher using n-gram frequency analysis.
    """
    
    def __init__(self, ciphered_content: str) -> None:
        """
        Constructor method that initializes the class with the ciphered content.
        
        :param ciphered_content: the ciphered content as a string
        """
        # Initialize instance variables
        self._ciphered_content = ciphered_content
        self._ciphered_content_ngrams = NgramAnalyzer(text=ciphered_content, text_name="ciphered")
        self._language_ngrams = NgramAnalyzer()

        # Text utility instance
        self._util_text = TextUtil()

        # Convert the unigrams, bigrams, and trigrams into Pandas DataFrames
        self._df_ciphered_unigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.unigrams)
        self._df_ciphered_bigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.bigrams)
        self._df_ciphered_trigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.trigrams)
        self._df_language_unigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.unigrams)
        self._df_language_bigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.bigrams)
        self._df_language_trigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.trigrams)

    def _get_most_frequent_chars(self, df_ngrams, num_top) -> dict:
        """
        Gets the most frequent characters from the given DataFrame of n-grams.

        :param df_ngrams: the DataFrame of n-grams as a pandas DataFrame
        :param num_top: the number of most frequent n-grams to return as an int
        :return: the most frequent characters as a dictionary
        """
        # Get the top n-grams from the DataFrame
        df_top = df_ngrams.head(num_top).to_dict()["ngram"]
        return df_top

    def _get_decoder(self, ngrams_language, ngrams_ciphered) -> list:
        """
        Gets a decoder by pairing the language n-grams with the ciphered n-grams.

        :param ngrams_language: the language n-grams as a dictionary
        :param ngrams_ciphered: the ciphered n-grams as a dictionary
        :return: the decoder as a list of tuples
        """
        # Pair the language n-grams with the ciphered n-grams
        decoder = [(cipher_value, language_value) for cipher_value, language_value in zip(ngrams_ciphered, ngrams_language)]
        return decoder

    def _get_possible_decoders(self, ngrams_language, ngrams_ciphered) -> list:
        """
        Gets all possible decoders by generating all permutations of the language n-grams.

        :param ngrams_language: the language n-grams as a dictionary
        :param ngrams_ciphered: the ciphered n-grams as a dictionary
        :return: the possible decoders as a list of lists of tuples
        """
        # Convert the n-grams dictionaries to lists
        ngrams_language_values = list(ngrams_language.values())
        ngrams_ciphered_values = list(ngrams_ciphered.values())

        # Generate all permutations of the language n-grams
        perms = list(itertools.permutations(ngrams_language_values))

        # Pair each permutation with the ciphered n-grams
        possible_decoders = [[(cipher, lang) for cipher, lang in zip(ngrams_ciphered_values, perm)] for perm in perms]
        return possible_decoders

    def break_cipher(self) -> str:
        """
        Breaks the cipher and returns the deciphered content.

        :return: the deciphered content as a string
        """
        # Get the most frequent trigrams, bigrams, and unigrams from the language and ciphered content
        top_trigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_trigrams, num_top=3)
        top_trigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_trigrams, num_top=3)
        top_bigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_bigrams, num_top=3)
        top_bigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_bigrams, num_top=3)
        top_unigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_unigrams, num_top=5)
        top_unigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_unigrams, num_top=5)

        # Generate all possible decoders for the trigrams
        decoders_trigrams = self._get_possible_decoders(top_trigrams_language, top_trigrams_ciphered)

        for num_decoder, decoder in enumerate(decoders_trigrams):
            ciphered_content = self._ciphered_content
            replacements = {}

            # Generate replacement dictionary for each pair of ciphered and language values
            for cipher_value, lang_value in decoder:
                cipher_value_letters = list(cipher_value)
                lang_value_letters = list(lang_value)

                for num in range(0, len(cipher_value_letters)):
                    replacements[cipher_value_letters[num]] = lang_value_letters[num]

            # Apply the replacements to the ciphered content
            translation_table = str.maketrans(replacements)
            ciphered_content = ciphered_content.translate(translation_table)

            # Print and save the result
            print(ciphered_content)
            self._util_text.write_text_to_file(filename=f"decoder_{num_decoder}.txt", content=ciphered_content)

        return deciphered_content

    def color_text(self, text: str, color_code: str) -> str:
        """
        Colors the given text with the specified color code.

        :param text: the text to color as a string
        :param color_code: the color code as a string
        :return: the colored text as a string
        """
        return f'\033[{color_code}m{text}\033[0m'

    def break_cipher_manually(self) -> str:
        """
        Breaks the cipher manually by allowing the user to provide replacement suggestions.

        :return: the deciphered content as a string
        """
        replacement_dict = {}

        while True:
            # Print the current ciphered content
            print(f"\n{self._ciphered_content}")

            # Get the user's replacement suggestion
            user_input = input("\nEnter the string you want to replace and the new value (e.g. 'A B'), or type 'done' to finish: ")
            if user_input.lower() == 'done':
                break

            try:
                # Parse the old and new strings from the user input
                old_string, new_string = user_input.split()

                # Apply the replacement suggestion to the ciphered content
                temp_deciphered_content = self._ciphered_content.replace(old_string, self.color_text(new_string, '91'))

                # Print the deciphered text with the current suggestion
                print("\nDeciphered text with current suggestion:")
                print(temp_deciphered_content)
                print()

                # Ask the user if they want to apply the suggestion
                apply_suggestion = input("\nDo you want to apply this suggestion? (yes/no): ")
                if apply_suggestion.lower() == 'yes':
                    # Apply the replacement suggestion to a copy of the ciphered content
                    temp_deciphered_content = self._ciphered_content.replace(old_string, new_string)

                    # Highlight the replaced segment in blue
                    highlighted_content = temp_deciphered_content.replace(new_string, self.color_text(new_string, '94'))

                    # Print the applied suggestion
                    print("\nApplied suggestion:")
                    print(highlighted_content)
                    print()

                    # Update the original ciphered content with the applied changes
                    self._ciphered_content = temp_deciphered_content

            except ValueError:
                # Handle invalid input
                print("\nInvalid input. Please enter the string you want to replace and the new value separated by a space.")
                continue

        return self._ciphered_content

    def _ngram_to_dataframe(self, ngram: Counter) -> pd.DataFrame:
        """
        Converts the given n-gram Counter object to a Pandas DataFrame.

        :param ngram: the n-gram Counter object
        :return: the n-gram DataFrame
        """
        # Convert the n-gram Counter object to a DataFrame
        df_ngram = pd.DataFrame(ngram.items(), columns=['ngram', 'frequency'])

        # Sort the DataFrame by frequency in descending order
        df_ngram = df_ngram.sort_values(by='frequency', ascending=False)

        # Reset the index of the sorted DataFrame
        df_ngram = df_ngram.reset_index(drop=True)

        return df_ngram

    def store_ngrams(self) -> None:
        """
        Stores the n-grams data to CSV files.
        """
        # Store the n-grams DataFrames to CSV files
        self._df_ciphered_unigrams.to_csv("df_ciphered_unigrams.csv", sep=',', index=False)
        self._df_ciphered_bigrams.to_csv("df_ciphered_bigrams.csv", sep=',', index=False)
        self._df_ciphered_trigrams.to_csv("df_ciphered_trigrams.csv", sep=',', index=False)
        self._df_language_unigrams.to_csv("df_language_unigrams.csv", sep=',', index=False)
        self._df_language_bigrams.to_csv("df_language_bigrams.csv", sep=',', index=False)
        self._df_language_trigrams.to_csv("df_language_trigrams.csv", sep=',', index=False)


if __name__ == "__main__":
    # Create an instance of the TextUtil class
    util_text = TextUtil()

    # Read the content of the sample file
    sample_text = util_text.read_file(filename="mono_ciphered.txt")

    # Create an instance of the MonoalphabeticCipherBreaker class
    cipher_breaker = MonoalphabeticCipherBreaker(ciphered_content=sample_text)

    # Store n-grams
    cipher_breaker.store_ngrams()

    # Break the cipher and get the deciphered content
    deciphered_content = cipher_breaker.break_cipher()

    # Allow the user to break the cipher manually
    deciphered_content = cipher_breaker.break_cipher_manually()

    # Save the deciphered content to a file
    util_text.write_text_to_file(filename="mono_hacked.txt", content=deciphered_content)
