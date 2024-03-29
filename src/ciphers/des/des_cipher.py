from typing import List

from src.ciphers.des import const
from src.ciphers.des.des_cipher_helper import DesCipherHelper

class DesCipher:
    """
    This class represents the Data Encryption Standard (DES) algorithm.
    It provides methods for key generation, encryption, and helper functions.
    """

    def __init__(self) -> None:
        """
        Constructor method that initializes the DES object with predefined tables.
        """
        # Instance of DesCipherHelper
        self.des_helper = DesCipherHelper()

        # Table of Position of 64 bits at the initial level: Initial Permutation Table
        self.initial_permutation_table = const.initial_permutation_table

        # Expansion D-box Table
        self.expansion_d_box_table = const.expansion_d_box_table

        # Straight Permutation Table
        self.straight_permutation_table = const.straight_permutation_table

        # S-box Table
        self.s_box_table = const.s_box_table

        # Final Permutation Table
        self.final_permutation_table = const.final_permutation_table

        # Generate keys
        self._seed = self.des_helper._generate_seed()
        self._key = self.des_helper._generate_random_key(self._seed)
        self._round_keys_binary = self.des_helper.generate_keys(self._key)

    def _process_block(self, block_hex: str, round_keys_binary: List[str]) -> str:
        """
        Processes a block using the DES algorithm for encryption.

        :param block: The input block to be processed (64 bits)
        :param round_keys_binary: List of round keys in binary format
        :return: The encrypted block as a hexadecimal string
        """
        # Convert input to binary
        block_bin = self.des_helper.hex_to_bin(block_hex)

        # Initial Permutation
        initial_permutation_result = self.des_helper.permute(block_bin, self.initial_permutation_table)

        # Split the block into left and right halves
        left, right = initial_permutation_result[0:32], initial_permutation_result[32:64]

        # Iterate through 16 rounds
        for round_num in range(16):
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = self.des_helper.permute(right, self.expansion_d_box_table)

            # XOR and expansion
            xor_result = self.des_helper.xor(right_expanded, round_keys_binary[round_num])

            # S-boxes: Substituting the value from s-box table
            sbox_result = "".join(
                self.des_helper.dec_to_bin(self.s_box_table[i][self.des_helper.bin_to_dec(xor_result[i * 6] + xor_result[i * 6 + 5])][
                    self.des_helper.bin_to_dec(xor_result[i * 6 + 1:i * 6 + 5])]
                )
                for i in range(8)
            )

            # Straight Permutation: Rearranging the bits
            sbox_result = self.des_helper.permute(sbox_result, self.straight_permutation_table)

            # XOR left and sbox_result
            left = self.des_helper.xor(left, sbox_result)

            # Swapper
            if round_num != 15:
                left, right = right, left

        # Combination
        combined_result = left + right

        # Final Permutation: Rearranging bits to get text
        text = self.des_helper.permute(combined_result, self.final_permutation_table)
        text = self.des_helper.bin_to_hex(text)
        return text

    def cipher_block(self, plaintext_hex: str) -> str:
        """
        Encrypts the given plaintext using the DES algorithm.

        :param plaintext_hex: The input plaintext as a hexadecimal string
        :return: The encrypted ciphertext as a binary string
        """
        # Use regular keys
        round_keys_binary = self._round_keys_binary
        # Process block
        ciphertext = self._process_block(plaintext_hex, round_keys_binary)
        return ciphertext

    def decipher_block(self, cipher_text: str) -> str:
        """
        Decrypts the given ciphertext using the DES algorithm.

        :param cipher_text: The input ciphertext as a hexadecimal string
        :return: The decrypted plaintext as a binary string
        """
        # Use reverse keys
        round_keys_binary_reverse = self._round_keys_binary[::-1]
        # Process block
        plaintext = self._process_block(cipher_text, round_keys_binary_reverse)
        return plaintext
    
    def cipher_content(self, content: str) -> str:
        """
        Encrypts the given plaintext using the DES algorithm.

        :param content: The input plaintext as a regular string
        :return: The encrypted ciphertext as a binary string
        """
        # Convert the input string to hexadecimal
        hex_string = self.des_helper.text_to_hex(content)
        hex_blocks = self.des_helper.hex_to_64_bits_blocks(hex_string)

        # Call cipher_block to perform encryption
        ciphertext = "".join(self.cipher_block(hex_string) for hex_string in hex_blocks)
        return ciphertext

    def decipher_content(self, ciphered_content: str) -> str:
        """
        Decrypts the given ciphertext using the DES algorithm.

        :param ciphered_content: The input ciphertext as a hexadecimal string
        :return: The decrypted plaintext as a regular string
        """
        # Get hex blocks of 64 bits
        hex_blocks = self.des_helper.hex_to_64_bits_blocks(ciphered_content)

        # Call decipher_block to perform decryption
        hex_text = "".join(self.decipher_block(hex_string) for hex_string in hex_blocks)

        # Convert hexadecimal code to text
        deciphered_text = self.des_helper.hex_to_text(hex_text)
        return deciphered_text

    def cipher_hex_img(self, content: str) -> str:
        """
        Encrypts the given hex image using DES algorithm.

        :param content: The image as a hexadecimal string
        :return: The encrypted ciphertext as a binary string
        """
        # Convert the input string to hexadecimal
        hex_blocks = self.des_helper.hex_to_64_bits_blocks(content)

        # Call cipher_block to perform encryption
        ciphertext = "".join(self.cipher_block(hex_string) for hex_string in hex_blocks)

        return ciphertext

    def decipher_hex_img(self, ciphered_content: str) -> str:
        """
        Decrypts the given ciphertext using DES algorithm.

        :param ciphered_content: The input ciphertext as a hexadecimal string
        :return: The decrypted text as a hexadecimal image
        """
        # Get hex blocks of 64 bits
        hex_blocks = self.des_helper.hex_to_64_bits_blocks(ciphered_content)

        # Call decipher_block to perform decryption
        hex_text = "".join(self.decipher_block(hex_string) for hex_string in hex_blocks)

        return hex_text
