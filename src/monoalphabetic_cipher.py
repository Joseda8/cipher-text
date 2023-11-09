import random
import string

from tr import tr


class MonoalphabeticCipher:
    """
    This class represents the Monoalphabetic Substitution Cipher system.
    It provides methods to cipher and decipher content using a random key.
    """

    def __init__(self) -> None:
        """
        Constructor method that initializes the class with a random key.
        """
        self._seed = self._generate_seed()
        self._key = self._generate_random_key()

    def _generate_seed(self) -> str:
        """
        Generates a seed for the cipher
        using all the ASCII printable characters.

        :return: a string with the seed for the cipher
        """
        # Create a string of numbers and letters (both lowercase and uppercase)
        chars = string.ascii_letters + string.digits
        return chars

    def _generate_random_key(self) -> str:
        """
        Generates a random key for the cipher.

        :return: a random key as a string
        """
        # Shuffle seed to create a random key
        seed = list(self._seed)
        random.shuffle(seed)
        seed = "".join(seed)
        return seed

    def cipher_content(self, content: str) -> str:
        """
        Ciphers the given content using the random key.

        :param content: the content to be ciphered as a string
        :return: the ciphered content as a string
        """
        # Cipher the content using the random key
        ciphered_content = tr(self._seed, self._key, content)
        return ciphered_content

    def decipher_content(self, ciphered_content: str) -> str:
        """
        Deciphers the given ciphered content using the random key.

        :param ciphered_content: the ciphered content to be deciphered as a string
        :return: the deciphered content as a string
        """
        # Decipher the ciphered content using the random key
        deciphered_content = tr(self._key, self._seed, ciphered_content)
        return deciphered_content
