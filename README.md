# Ciphering
## _Playground to experiment with different ciphering algorithms_

This Python project provides a playground for experimenting with various ciphers. It includes implementations for the Data Encryption Standard (DES), Monoalphabetic Cipher, and Polyalphabetic Cipher. Additionally, it demonstrates the use of these ciphers on text and image data for DES.

It also includes a playground to break the Monoalphabetic algorithm.

> Note: Notice that the project contains a `requirements.txt` file that can be used to get all the dependencies required to run this project.


## Usage

Run the main script with the desired options. For example:

```sh
python3 -m src.main --filename test_files/sample.txt --language eng
```

- `--filename`: Specify the name of the file to cipher.
- `--language`: Choose the language for the text (`eng` and `spa` currently supported).

## Results

Ciphered and deciphered content, as well as images, will be saved in the `results` directory.

- **results/eng (or spa)**: Contains text files with ciphered and deciphered content for each cipher.
- **results/images**: Contains ciphered and deciphered images (in the case of the DES cipher).


### Monoalphabetic Cipher Breaker

This Python class, `MonoalphabeticCipherBreaker`, is designed to break a Monoalphabetic Substitution Cipher using n-gram frequency analysis. It employs the use of language and ciphered n-grams to generate possible decoders and attempts to decipher the content.

## Usage

To use this Monoalphabetic Cipher breaker, the class provides a main method that can be executed directly. The script accepts the following command-line arguments:

- `--filename`: Path to the file containing the ciphered text (required).
- `--hack_by_file`: Path to the JSON file containing replacement suggestions.
- `--current_decoding_file`: Path to a file with the current status of decoding (optional).
- `--language`: Language for the text (`eng` and `spa` currently supported) (required).

The class uses n-gram frequency analysis for both the language and ciphered content. It provides methods to store n-gram data and break the cipher using a semi automate approach. The deciphered content can be saved to a file for further analysis or usage.

Here's an example of how to run the script:

```sh
python3 -m src.ciphers.monoalphabetic.monoalphabetic_cipher_breaker --filename results/eng/mono_ciphered.txt --language eng
```
