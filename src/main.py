import argparse
import os

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

# Define file paths as constants
RESULTS_PATH = f"results/{language}"
IMAGES_PATH = "results/images"

# Main
# Text utility instance
text_util = TextUtil()

# Read the content of the sample file
logger.info(f"Reading text from: {filename}")
sample_text = text_util.read_file(filename=filename)

# Instance of the MonoalphabeticCipher class
logger.info("Running Monoalphabetic cipher")
monoalphabetic_cipher = MonoalphabeticCipher()

# Cipher and decipher the text
logger.debug("Running Monoalphabetic cipher - Ciphering")
ciphered_content_mono = monoalphabetic_cipher.cipher_content(content=sample_text)
text_util.write_text_to_file(filename=os.path.join(RESULTS_PATH, "mono_ciphered.txt"), content=ciphered_content_mono)

logger.debug("Running Monoalphabetic cipher - Deciphering")
deciphered_content_mono = monoalphabetic_cipher.decipher_content(ciphered_content=ciphered_content_mono)
text_util.write_text_to_file(filename=os.path.join(RESULTS_PATH, "mono_deciphered.txt"), content=deciphered_content_mono)

# Instance of the PolyalphabeticCipher class
logger.info("Running PolyalphabeticCipher cipher")
polyalphabetic_cipher = PolyalphabeticCipher()

# Cipher and decipher the text
logger.debug("Running PolyalphabeticCipher cipher - Ciphering")
ciphered_content_poly = polyalphabetic_cipher.cipher_content(content=sample_text)
text_util.write_text_to_file(filename=os.path.join(RESULTS_PATH, "poly_ciphered.txt"), content=ciphered_content_poly)

logger.debug("Running PolyalphabeticCipher cipher - Deciphering")
deciphered_content_poly = polyalphabetic_cipher.decipher_content(ciphered_content=ciphered_content_poly)
text_util.write_text_to_file(filename=os.path.join(RESULTS_PATH, "poly_deciphered.txt"), content=deciphered_content_poly)

# Instance of the DesCipher class
logger.info("Running DesCipher cipher")
des_cipher = DesCipher()

# Cipher and decipher the text
logger.debug("Running DesCipher cipher - Ciphering")
ciphered_content_des = des_cipher.cipher_content(content=sample_text)
text_util.write_text_to_file(filename=os.path.join(RESULTS_PATH, "des_ciphered.txt"), content=ciphered_content_des)

logger.debug("Running DesCipher cipher - Deciphering")
deciphered_content_des = des_cipher.decipher_content(ciphered_content=ciphered_content_des)
text_util.write_text_to_file(filename=os.path.join(RESULTS_PATH, "des_deciphered.txt"), content=deciphered_content_des)

# Cipher and decipher the image
logger.debug("Running DesCipher image cipher - Deciphering")
image_bit_map, image_dimensions = text_util.extract_image_hex_bitmap_and_dimensions(image_path="test_files/test_img.jpg")
ciphered_img_des = des_cipher.cipher_hex_img(content=image_bit_map)
text_util.write_image_from_hex(filename=os.path.join(IMAGES_PATH, "des_ciphered.jpg"), hex_bitmap=ciphered_img_des, image_size=image_dimensions)
deciphered_img_des = des_cipher.decipher_hex_img(ciphered_content=ciphered_img_des)
text_util.write_image_from_hex(filename=os.path.join(IMAGES_PATH, "des_deciphered.jpg"), hex_bitmap=deciphered_img_des, image_size=image_dimensions)
