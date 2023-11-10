import itertools
import pandas as pd
from collections import Counter

from src.ciphers.ngram_analyzer import NgramAnalyzer
from src.util.nltk_util import Language, language_type
from src.util.text_util import TextUtil


class MonoalphabeticCipherBreaker:
    """
    This class represents a Monoalphabetic Substitution Cipher breaker.
    It provides methods to break the cipher using n-gram frequency analysis.
    """

    def __init__(self, ciphered_content: str, language: Language) -> None:
        """
        Constructor method that initializes the class with the ciphered content.

        :param ciphered_content: the ciphered content as a string
        """
        # Initialize instance variables
        self._ciphered_content = ciphered_content
        self._language = language
        self._language_name = language.name
        self._ciphered_content_ngrams = NgramAnalyzer(text=ciphered_content, text_name=f"{self._language_name}_ciphered")
        self._language_ngrams = NgramAnalyzer(language=language, text_name=self._language_name)

        # Text utility instance
        self._util_text = TextUtil()

        # Convert the unigrams, bigrams, and trigrams into Pandas DataFrames
        self._df_ciphered_unigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.unigrams)
        self._df_ciphered_bigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.bigrams)
        self._df_ciphered_trigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.trigrams)
        self._df_language_unigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.unigrams)
        self._df_language_bigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.bigrams)
        self._df_language_trigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.trigrams)

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
        path_root = f"results/{self._language_name}/ngrams"
        self._util_text.write_dataframe_to_csv(filename=f"{path_root}/df_ciphered_unigrams.csv", dataframe=self._df_ciphered_unigrams)
        self._util_text.write_dataframe_to_csv(filename=f"{path_root}/df_ciphered_biigrams.csv", dataframe=self._df_ciphered_bigrams)
        self._util_text.write_dataframe_to_csv(filename=f"{path_root}/df_ciphered_trigrams.csv", dataframe=self._df_ciphered_trigrams)
        self._util_text.write_dataframe_to_csv(filename=f"{path_root}/df_language_unigrams.csv", dataframe=self._df_language_unigrams)
        self._util_text.write_dataframe_to_csv(filename=f"{path_root}/df_language_biigrams.csv", dataframe=self._df_language_bigrams)
        self._util_text.write_dataframe_to_csv(filename=f"{path_root}/df_language_trigrams.csv", dataframe=self._df_language_trigrams)

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

    def perform_replacement(self, replacements):
        """
        Apply replacements to the ciphered content.

        :param replacements: the replacement dictionary
        :return: the deciphered content
        """
        # Apply the replacements to the ciphered content
        translation_table = str.maketrans(replacements)
        ciphered_content = self._ciphered_content.translate(translation_table)
        return ciphered_content

    def break_cipher(self) -> None:
        """
        Breaks the cipher and saves deciphered content to files.
        """
        # Get the most frequent trigrams, bigrams, and unigrams from the language and ciphered content
        top_trigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_trigrams, num_top=3)
        top_trigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_trigrams, num_top=3)

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

            # Check if all the words in top_trigrams_language appear in ciphered_content
            if all(word in ciphered_content for word in top_trigrams_language.values()):
                # Save the result
                self._util_text.write_text_to_file(filename=f"results/{self._language_name}/possible_decoders/decoder_{num_decoder}.txt", content=ciphered_content)

    def color_text(self, text: str, color_code: str) -> str:
        """
        Colors the given text with the specified color code.

        :param text: the text to color as a string
        :param color_code: the color code as a string
        :return: the colored text as a string
        """
        return f'\033[{color_code}m{text}\033[0m'

    def break_cipher_manually(self, ciphered_content: str = None) -> str:
        """
        Breaks the cipher manually by allowing the user to provide replacement suggestions.

        :param ciphered_content: the ciphered content to be manually broken as a string (optional)
        :return: the deciphered content as a string
        """
        # Use the attribute value if ciphered_content is not provided
        if ciphered_content is None:
            ciphered_content = self._ciphered_content

        # Initialize the replacement dictionary
        replacement_dict = {}

        # Populate the replacement dictionary with initial differences
        for i, char in enumerate(ciphered_content):
            if i < len(self._ciphered_content) and char != self._ciphered_content[i]:
                replacement_dict[self._ciphered_content[i]] = char

        while True:
            # Highlight the differences in blue
            highlighted_content = ""
            for i, char in enumerate(ciphered_content):
                if i < len(self._ciphered_content) and char != self._ciphered_content[i]:
                    highlighted_content += self.color_text(char, '94')
                else:
                    highlighted_content += char

            # Print the current ciphered content with differences highlighted
            print(f"\n{highlighted_content}")

            # Get the user's replacement suggestion
            user_input = input("\nEnter the string you want to replace and the new value (e.g. 'A B'), or type 'done' to finish: ")
            if user_input.lower() == 'done':
                self._util_text.write_json_to_file(filename="decoder.json", data=replacement_dict)
                break

            try:
                # Parse the old and new strings from the user input
                old_string, new_string = user_input.split()

                # Apply the replacement suggestion to the ciphered content
                old_string_letters = list(old_string)
                new_string_letters = list(new_string)

                temp_deciphered_content = ciphered_content
                for num in range(0, len(old_string_letters)):
                    temp_deciphered_content = temp_deciphered_content.replace(old_string_letters[num], self.color_text(new_string_letters[num], '91'))

                # Print the deciphered text with the current suggestion
                print("\nDeciphered text with current suggestion:")
                print(temp_deciphered_content)
                print()

                # Ask the user if they want to apply the suggestion
                apply_suggestion = input("\nDo you want to apply this suggestion? (yes/no): ")
                if apply_suggestion.lower() == 'yes':
                    # Apply the replacement suggestion to a copy of the ciphered content
                    replacements = {}
                    old_string_letters = list(old_string)
                    new_string_letters = list(new_string)
                    for num in range(0, len(old_string_letters)):
                        replacements[old_string_letters[num]] = new_string_letters[num]

                    # Apply the replacements to the ciphered content
                    translation_table = str.maketrans(replacements)
                    temp_deciphered_content = ciphered_content.translate(translation_table)

                    # Update the replacement dictionary
                    for i, old_char in enumerate(old_string):
                        if i < len(new_string):
                            replacement_dict[old_char] = new_string[i]

                    # Update the original ciphered content with the applied changes
                    ciphered_content = temp_deciphered_content

            except ValueError:
                # Handle invalid input
                print("\nInvalid input. Please enter the string you want to replace and the new value separated by a space.")
                continue

        return ciphered_content

if __name__ == "__main__":
    import argparse

    # Create an instance of the TextUtil class
    util_text = TextUtil()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Break a monoalphabetic cipher.")
    parser.add_argument("--filename", help="Path to the file containing the ciphered text.", required=True)
    parser.add_argument("--hack_by_file", help="Path to the JSON file containing the replacements.")
    parser.add_argument("--current_decoding_file", help="Path to file with current decoding.")
    parser.add_argument("--language", help="Language for the text (eng or spa).", required=True, type=language_type, choices=list(Language))
    args = parser.parse_args()

    # Read the content of the file specified by the command line argument
    ciphered_text = util_text.read_file(filename=args.filename)

    # Create an instance of the MonoalphabeticCipherBreaker class
    cipher_breaker = MonoalphabeticCipherBreaker(ciphered_content=ciphered_text, language=args.language)

    # Store n-grams
    cipher_breaker.store_ngrams()

    # Break the cipher
    cipher_breaker.break_cipher()

    # Check if the --hack_by_file option was used
    if args.hack_by_file:
        # Read the JSON file containing the replacements
        replacements = util_text.read_json_from_file(filename=args.hack_by_file)
        # Perform the replacements and get the deciphered content
        deciphered_content = cipher_breaker.perform_replacement(replacements=replacements)
    else:
        if args.current_decoding_file:
            current_decoding_file = args.current_decoding_file
        else:
            # Ask the user for the path of the content to send to break_cipher_manually
            current_decoding_file = input(
                "Enter the path of the file to use for manual decryption, or press Enter to start from scratch: ")

        # Use the user input as the argument to break_cipher_manually if it is not empty, otherwise use ciphered_text
        if current_decoding_file:
            manual_ciphered_text = util_text.read_file(filename=current_decoding_file)
        else:
            manual_ciphered_text = ciphered_text

        # Allow the user to break the cipher manually
        deciphered_content = cipher_breaker.break_cipher_manually(ciphered_content=manual_ciphered_text)

    # Save the deciphered content to a file
    util_text.write_text_to_file(filename="mono_hacked.txt", content=deciphered_content)
