import argparse
import random

from tr import tr

class MonoalphabeticCipher:
    """
    This class represents the Monoalphabetic Substitution Cipher system.
    It provides methods to cipher and decipher content using a random key.
    """
    
    def __init__(self):
        """
        Constructor method that initializes the class with a random key.
        """
        self.__key = self.__generate_random_key()

    def __generate_random_key(self):
        """
        Private method that generates a random key for the cipher.

        :return: a random key as a string
        """
        # Create a list of all uppercase and lowercase letters
        chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        
        # Shuffle the list to create a random key
        random.shuffle(chars)
        
        # Return the key as a string
        return ''.join(chars)
        
    def cipher_content(self, content):
        """
        Public method that ciphers the given content using the random key.

        :param content: the content to be ciphered as a string
        :return: the ciphered content as a string
        """
        # Cipher the content using the random key
        ciphered_content = tr(content, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', self.__key)
        return ciphered_content
    
    def decipher_content(self, ciphered_content):
        """
        Public method that deciphers the given ciphered content using the random key.

        :param ciphered_content: the ciphered content to be deciphered as a string
        :return: the deciphered content as a string
        """
        # Decipher the ciphered content using the random key
        deciphered_content = tr(ciphered_content, self.__key, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        return deciphered_content

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Monoalphabetic Substitution Cipher')
    
    # Add a positional argument for the filename
    parser.add_argument('--filename', type=str, help='the name of the file to cipher')
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Get the filename from the command line arguments
    filename = args.filename
    
    # Read the content of the file
    with open(filename, 'r') as file:
        content = file.read()
    
    # Create an instance of the MonoalphabeticCipher class
    cipher = MonoalphabeticCipher()

    # Cipher the content
    ciphered_content = cipher.cipher_content(content)
    
    # Print the ciphered content
    print('Ciphered content:')
    print(ciphered_content)
    
    # Decipher the ciphered content
    deciphered_content = cipher.decipher_content(ciphered_content)
    
    # Print the deciphered content
    print('Deciphered content:')
    print(deciphered_content)
