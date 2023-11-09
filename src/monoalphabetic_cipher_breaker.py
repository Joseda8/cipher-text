import itertools

import pandas as pd
from collections import Counter

from ngram_analyzer import NgramAnalyzer
from util.text_util import TextUtil


class MonoalphabeticCipherBreaker:
    def __init__(self, ciphered_content: str):
        self._ciphered_content = ciphered_content
        self._ciphered_content_ngrams = NgramAnalyzer(text=ciphered_content, text_name="ciphered")
        self._language_ngrams = NgramAnalyzer()

        # Text utilitary instance
        self._util_text = TextUtil()

        # Convert the unigrams, bigrams, and trigrams into Pandas DataFrames
        self._df_ciphered_unigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.unigrams)
        self._df_ciphered_bigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.bigrams)
        self._df_ciphered_trigrams = self._ngram_to_dataframe(ngram=self._ciphered_content_ngrams.trigrams)
        self._df_language_unigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.unigrams)
        self._df_language_bigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.bigrams)
        self._df_language_trigrams = self._ngram_to_dataframe(ngram=self._language_ngrams.trigrams)
        
    def _get_most_frequent_chars(self, df_ngrams, num_top):
        df_top = df_ngrams.head(num_top).to_dict()["ngram"]
        return df_top
    
    def _get_decoder(self, ngrams_language, ngrams_ciphered):
        decoder = []
        for num in range(0, len(ngrams_language)):
            cipher_value = ngrams_ciphered[num]
            languague_value = ngrams_language[num]
            decoder.append((cipher_value, languague_value))
        return decoder

    def _get_possible_decoders(self, ngrams_language, ngrams_ciphered):
        ngrams_language_values = list(ngrams_language.values())
        ngrams_ciphered_values = list(ngrams_ciphered.values())

        # Generate all permutations of ngrams_language_values
        perms = list(itertools.permutations(ngrams_language_values))

        # Generate all possible combinations by pairing each permutation with ngrams_ciphered_values
        possible_decoders = [[(cipher, lang) for cipher, lang in zip(ngrams_ciphered_values, perm)] for perm in perms]
        return possible_decoders

    def break_cipher(self) -> str:
        deciphered_content = ""
        
        top_trigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_trigrams, num_top=3)
        top_trigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_trigrams, num_top=3)
        top_bigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_bigrams, num_top=3)
        top_bigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_bigrams, num_top=3)
        top_unigrams_language = self._get_most_frequent_chars(df_ngrams=self._df_language_unigrams, num_top=5)
        top_unigrams_ciphered = self._get_most_frequent_chars(df_ngrams=self._df_ciphered_unigrams, num_top=5)

        decoders_trigrams = self._get_possible_decoders(top_trigrams_language, top_trigrams_ciphered)

        for num_decoder, decoder in enumerate(decoders_trigrams):
            ciphered_content = self._ciphered_content
            replacements = {}
            for cipher_value, lang_value in decoder:
                cipher_value_letters = list(cipher_value)
                lang_value_letters = list(lang_value)

                for num in range(0, len(cipher_value_letters)):
                    replacements[cipher_value_letters[num]] = lang_value_letters[num]

            translation_table = str.maketrans(replacements)
            ciphered_content = ciphered_content.translate(translation_table)
            print(ciphered_content)
            self._util_text.write_text_to_file(filename=f"decoder_{num_decoder}.txt", content=ciphered_content)
        return deciphered_content

    def color_text(self, text: str, color_code: str) -> str:
        return f'\033[{color_code}m{text}\033[0m'

    def break_cipher_manually(self) -> str:
        replacement_dict = {}
        while True:
            print(f"\n{self._ciphered_content}")
            user_input = input("\nEnter the string you want to replace and the new value (e.g. 'A B'), or type 'done' to finish: ")
            if user_input.lower() == 'done':
                break

            try:
                old_string, new_string = user_input.split()
                
                # Apply the replacement suggestion to the ciphered content
                temp_deciphered_content = self._ciphered_content.replace(old_string, self.color_text(new_string, '91'))

                print("\nDeciphered text with current suggestion:")
                print(temp_deciphered_content)
                print()

                apply_suggestion = input("\nDo you want to apply this suggestion? (yes/no): ")
                if apply_suggestion.lower() == 'yes':
                    # Apply the replacement suggestion to a copy of the ciphered content
                    temp_deciphered_content = self._ciphered_content.replace(old_string, new_string)
                    replacement_dict[old_string] = new_string

                    # Highlight the replaced segment in blue
                    highlighted_content = temp_deciphered_content.replace(new_string, self.color_text(new_string, '94'))

                    print("\nApplied suggestion:")
                    print(highlighted_content)
                    print()

                    # Update the original ciphered content with the applied changes
                    self._ciphered_content = temp_deciphered_content

            except ValueError:
                print("\nInvalid input. Please enter the string you want to replace and the new value separated by a space.")
                continue

        return self._ciphered_content

    def _ngram_to_dataframe(self, ngram: Counter):
        # Convert the ngram into Pandas DataFrames
        df_ngram = pd.DataFrame(ngram.items(), columns=['ngram', 'frequency'])

        # Sort the DataFrame by the "frequency" column in descending order
        df_ngram = df_ngram.sort_values(by='frequency', ascending=False)

        # Reset the index of the sorted DataFrame
        df_ngram = df_ngram.reset_index(drop=True)

        return df_ngram
        
    def store_ngrams(self):
        # Store ngrams in CSV files
        self._df_ciphered_unigrams.to_csv("df_ciphered_unigrams.csv", sep=',', index=False)
        self._df_ciphered_bigrams.to_csv("df_ciphered_bigrams.csv", sep=',', index=False)
        self._df_ciphered_trigrams.to_csv("df_ciphered_trigrams.csv", sep=',', index=False)
        self._df_language_unigrams.to_csv("df_language_unigrams.csv", sep=',', index=False)
        self._df_language_bigrams.to_csv("df_language_bigrams.csv", sep=',', index=False)
        self._df_language_trigrams.to_csv("df_language_trigrams.csv", sep=',', index=False)


if __name__ == "__main__":
    # Text utilitary instance
    util_text = TextUtil()

    # Read the content of the sample file
    sample_text = util_text.read_file(filename="mono_ciphered.txt")

    # Create an instance of the MonoalphabeticCipherBreaker class
    cipher_breaker = MonoalphabeticCipherBreaker(ciphered_content=sample_text)

    # Store ngrams
    cipher_breaker.store_ngrams()

    # Break the cipher and get the deciphered content
    deciphered_content = cipher_breaker.break_cipher()
    deciphered_content = cipher_breaker.break_cipher_manually()

    # Save the deciphered content
    util_text.write_text_to_file(filename="mono_hacked.txt", content=deciphered_content)
