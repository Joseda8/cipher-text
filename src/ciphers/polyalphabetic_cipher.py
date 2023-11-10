import random
import string

from tr import tr


class PolyalphabeticCipher:
    """
    This class represents the Polyalphabetic Substitution Cipher system.
    It provides methods to cipher and decipher content using a set of random keys.
    """

    def __init__(self, num_mappings=5) -> None:
        """
        Constructor method that initializes the class with a set of random keys.

        :param num_mappings: the number of substitution mappings to use
        """
        self._num_mappings = num_mappings
        self._seed = self._generate_seed()
        self._keys = [self._generate_random_key() for _ in range(num_mappings)]

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
        Ciphers the given content using the set of random keys.

        :param content: the content to be ciphered as a string
        :return: the ciphered content as a string
        """
        # Cipher the content using the set of random keys
        ciphered_content = ""
        for i, char in enumerate(content):
            key = self._keys[i % self._num_mappings]
            ciphered_content += tr(self._seed, key, char)
        return ciphered_content

    def decipher_content(self, ciphered_content: str) -> str:
        """
        Deciphers the given ciphered content using the set of random keys.

        :param ciphered_content: the ciphered content to be deciphered as a string
        :return: the deciphered content as a string
        """
        # Decipher the ciphered content using the set of random keys
        deciphered_content = ""
        for i, char in enumerate(ciphered_content):
            key = self._keys[i % self._num_mappings]
            deciphered_content += tr(key, self._seed, char)
        return deciphered_content
