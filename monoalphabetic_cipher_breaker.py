from ngram_analyzer import NgramAnalyzer
import pandas as pd

class MonoalphabeticCipherBreaker:
    def __init__(self, ciphered_content: str):
        self._ciphered_content = ciphered_content
        self._ngram_analyzer = NgramAnalyzer()
        self._ciphered_content_ngrams = NgramAnalyzer(text=ciphered_content, text_name="ciphered")

    def color_text(self, text: str, color_code: str) -> str:
        return f'\033[{color_code}m{text}\033[0m'

    def break_cipher(self) -> str:
        replacement_dict = {}
        while True:
            print(self._ciphered_content)
            user_input = input("Enter the string you want to replace and the new value (e.g. 'A B'), or type 'done' to finish: ")
            if user_input.lower() == 'done':
                break

            try:
                old_string, new_string = user_input.split()
                
                # Apply the replacement suggestion to the ciphered content
                temp_deciphered_content = self._ciphered_content.replace(old_string, self.color_text(new_string, '91'))

                print("Deciphered text with current suggestion:")
                print(temp_deciphered_content)
                print()

                apply_suggestion = input("Do you want to apply this suggestion? (yes/no): ")
                if apply_suggestion.lower() == 'yes':
                    # Apply the replacement suggestion to a copy of the ciphered content
                    temp_deciphered_content = self._ciphered_content.replace(old_string, new_string)
                    replacement_dict[old_string] = new_string

                    # Highlight the replaced segment in blue
                    highlighted_content = temp_deciphered_content.replace(new_string, self.color_text(new_string, '94'))

                    print("Applied suggestion:")
                    print(highlighted_content)
                    print()

                    # Update the original ciphered content with the applied changes
                    self._ciphered_content = temp_deciphered_content

            except ValueError:
                print("Invalid input. Please enter the string you want to replace and the new value separated by a space.")
                continue

        return self._ciphered_content


    def store_ngrams(self):
        # Get the unigrams, bigrams, and trigrams from the ciphered content and the English language
        ciphered_unigrams = self._ciphered_content_ngrams.unigrams
        ciphered_bigrams = self._ciphered_content_ngrams.bigrams
        ciphered_trigrams = self._ciphered_content_ngrams.trigrams
        english_unigrams = self._ngram_analyzer.unigrams
        english_bigrams = self._ngram_analyzer.bigrams
        english_trigrams = self._ngram_analyzer.trigrams

        # Convert the unigrams, bigrams, and trigrams into Pandas DataFrames
        df_ciphered_unigrams = pd.DataFrame(ciphered_unigrams.items(), columns=['ngram', 'frequency'])
        df_ciphered_bigrams = pd.DataFrame(ciphered_bigrams.items(), columns=['ngram', 'frequency'])
        df_ciphered_trigrams = pd.DataFrame(ciphered_trigrams.items(), columns=['ngram', 'frequency'])
        df_english_unigrams = pd.DataFrame(english_unigrams.items(), columns=['ngram', 'frequency'])
        df_english_bigrams = pd.DataFrame(english_bigrams.items(), columns=['ngram', 'frequency'])
        df_english_trigrams = pd.DataFrame(english_trigrams.items(), columns=['ngram', 'frequency'])

        # Sort the DataFrames by the "frequency" column in descending order
        df_ciphered_unigrams = df_ciphered_unigrams.sort_values(by='frequency', ascending=False)
        df_ciphered_bigrams = df_ciphered_bigrams.sort_values(by='frequency', ascending=False)
        df_ciphered_trigrams = df_ciphered_trigrams.sort_values(by='frequency', ascending=False)
        df_english_unigrams = df_english_unigrams.sort_values(by='frequency', ascending=False)
        df_english_bigrams = df_english_bigrams.sort_values(by='frequency', ascending=False)
        df_english_trigrams = df_english_trigrams.sort_values(by='frequency', ascending=False)

        # Reset the index of the sorted DataFrames
        df_ciphered_unigrams = df_ciphered_unigrams.reset_index(drop=True)
        df_ciphered_bigrams = df_ciphered_bigrams.reset_index(drop=True)
        df_ciphered_trigrams = df_ciphered_trigrams.reset_index(drop=True)
        df_english_unigrams = df_english_unigrams.reset_index(drop=True)
        df_english_bigrams = df_english_bigrams.reset_index(drop=True)
        df_english_trigrams = df_english_trigrams.reset_index(drop=True)

        # Store ngrams in CSV files
        df_ciphered_unigrams.to_csv("df_ciphered_unigrams.csv", sep=',', index=False)
        df_ciphered_bigrams.to_csv("df_ciphered_bigrams.csv", sep=',', index=False)
        df_ciphered_trigrams.to_csv("df_ciphered_trigrams.csv", sep=',', index=False)
        df_english_unigrams.to_csv("df_english_unigrams.csv", sep=',', index=False)
        df_english_bigrams.to_csv("df_english_bigrams.csv", sep=',', index=False)
        df_english_trigrams.to_csv("df_english_trigrams.csv", sep=',', index=False)


if __name__ == "__main__":
    from text_util import TextUtil

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

    # Print the deciphered content
    print(deciphered_content)
