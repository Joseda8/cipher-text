import argparse

from monoalphabetic_cipher import MonoalphabeticCipher
from monoalphabetic_cipher_breaker import MonoalphabeticCipherBreaker
from text_util import TextUtil

from logger import setup_logging


# Set up the logging configuration
logger = setup_logging()


# Parse arguments
parser = argparse.ArgumentParser(description="Cipher and breaker playground")
parser.add_argument("--filename", type=str, help="the name of the file to cipher", required=True)
args = parser.parse_args()

# Extract arguments
filename = args.filename


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
ciphered_content = monoalphabetic_cipher.cipher_content(content=sample_text)
util_text.write_text_to_file(filename="mono_ciphered.txt", content=ciphered_content)

logger.debug("Running Monoalphabetic cipher - Deciphering")
deciphered_content = monoalphabetic_cipher.decipher_content(ciphered_content=ciphered_content)
util_text.write_text_to_file(filename="mono_deciphered.txt", content=deciphered_content)

logger.debug("Running Monoalphabetic cipher - Hacking")
monoalphabetic_cipher_breaker = MonoalphabeticCipherBreaker(ciphered_content=ciphered_content)
hacked_content = monoalphabetic_cipher_breaker.break_cipher()
util_text.write_text_to_file(filename="mono_hacked.txt", content=hacked_content)
