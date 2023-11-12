import argparse

from src.ciphers import DesCipher, MonoalphabeticCipher, PolyalphabeticCipher
from src.util.logger import setup_logging
from src.util.nltk_util import Language, language_type
from src.util.text_util import TextUtil


# Set up the logging configuration
logger = setup_logging()


# Parse arguments
parser = argparse.ArgumentParser(description="Cipher and breaker playground")
parser.add_argument("--filename", type=str, help="the name of the file to cipher", required=True)
parser.add_argument("--language", help="Language for the text (eng or spa).", required=True, type=language_type, choices=list(Language))
args = parser.parse_args()

# Extract arguments
filename = args.filename
language = args.language.name


# ----------------
# Main
# ----------------

# Text utilitary instance
util_text = TextUtil()

# Read the content of the sample file
logger.info(f"Reading text from: {filename}")
sample_text = util_text.read_file(filename=filename)

# Instance of the MonoalphabeticCipher class
logger.info("Running Monoalphabetic cipher")
monoalphabetic_cipher = MonoalphabeticCipher()

# Cipher, decipher and hack the text
logger.debug("Running Monoalphabetic cipher - Ciphering")
ciphered_content_mono = monoalphabetic_cipher.cipher_content(content=sample_text)
util_text.write_text_to_file(filename=f"results/{language}/mono_ciphered.txt", content=ciphered_content_mono)

logger.debug("Running Monoalphabetic cipher - Deciphering")
deciphered_content_mono = monoalphabetic_cipher.decipher_content(ciphered_content=ciphered_content_mono)
util_text.write_text_to_file(filename=f"results/{language}/mono_deciphered.txt", content=deciphered_content_mono)

# Instance of the PolyalphabeticCipher class
logger.info("Running PolyalphabeticCipher cipher")
polyalphabetic_cipher = PolyalphabeticCipher()

# Cipher, decipher and hack the text
logger.debug("Running PolyalphabeticCipher cipher - Ciphering")
ciphered_content_poly = polyalphabetic_cipher.cipher_content(content=sample_text)
util_text.write_text_to_file(filename=f"results/{language}/poly_ciphered.txt", content=ciphered_content_poly)

logger.debug("Running PolyalphabeticCipher cipher - Deciphering")
deciphered_content_poly = polyalphabetic_cipher.decipher_content(ciphered_content=ciphered_content_poly)
util_text.write_text_to_file(filename=f"results/{language}/poly_deciphered.txt", content=deciphered_content_poly)


# Instance of the DesCipher class
logger.info("Running DesCipher cipher")
des_cipher = DesCipher()

# Cipher, decipher and hack the text
logger.debug("Running DesCipher cipher - Ciphering")
ciphered_content_des = des_cipher.cipher_content(content=sample_text)
util_text.write_text_to_file(filename=f"results/{language}/des_ciphered.txt", content=ciphered_content_des)

logger.debug("Running DesCipher cipher - Deciphering")
deciphered_content_des = des_cipher.decipher_content(ciphered_content=ciphered_content_des)
util_text.write_text_to_file(filename=f"results/{language}/des_deciphered.txt", content=deciphered_content_des)
