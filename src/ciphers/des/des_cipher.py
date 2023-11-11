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

        # Table of Position of 64 bits at initial level: Initial Permutation Table
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
        self._round_keys_binary, self._round_keys_hex = self.des_helper.generate_keys(self._key)

    def _process_block(self, block, round_keys_binary, round_keys_hex):
        """
        Processes a block using the DES algorithm for encryption.

        :param block: The input block to be processed (64 bits)
        :param round_keys_binary: List of round keys in binary format
        :param round_keys_hex: List of round keys in hexadecimal format
        :return: The encrypted block as a hexadecimal string
        """
        # Split the block into left and right halves
        left, right = block[0:32], block[32:64]

        # Iterate through 16 rounds
        for round_num in range(16):
            # Expansion D-box: Expanding the 32 bits data into 48 bits
            right_expanded = self.des_helper.permute(right, self.expansion_d_box_table)

            # XOR RoundKey[i] and right_expanded
            xor_result = self.des_helper.xor(right_expanded, round_keys_binary[round_num])

            # S-boxes: Substituting the value from s-box table
            sbox_result = ""
            for sbox_index in range(8):
                row = self.des_helper.bin_to_dec(int(xor_result[sbox_index * 6] + xor_result[sbox_index * 6 + 5]))
                col = self.des_helper.bin_to_dec(int(xor_result[sbox_index * 6 + 1:sbox_index * 6 + 5]))
                val = self.s_box_table[sbox_index][row][col]
                sbox_result += self.des_helper.dec_to_bin(val)

            # Straight Permutation: Rearranging the bits
            sbox_result = self.des_helper.permute(sbox_result, self.straight_permutation_table)

            # XOR left and sbox_result
            xor_left_result = self.des_helper.xor(left, sbox_result)
            left = xor_left_result

            # Swapper
            if round_num != 15:
                left, right = right, left

            print("Round", round_num + 1, ":", self.des_helper.bin_to_hex(left), self.des_helper.bin_to_hex(right),
                  round_keys_hex[round_num])

        # Combination
        combined_result = left + right

        # Final Permutation: Rearranging bits to get ciphertext
        ciphertext = self.des_helper.permute(combined_result, self.final_permutation_table)
        ciphertext = self.des_helper.bin_to_hex(ciphertext)
        return ciphertext

    def cipher(self, plaintext_hex: str) -> str:
        """
        Encrypts the given plaintext using DES algorithm.

        :param plaintext_hex: The input plaintext as a hexadecimal string
        :return: The encrypted ciphertext as a binary string
        """
        round_keys_binary = self._round_keys_binary
        round_keys_hex = self._round_keys_hex
        plaintext_binary = self.des_helper.hex_to_bin(plaintext_hex)

        # Initial Permutation
        initial_permutation_result = self.des_helper.permute(plaintext_binary, self.initial_permutation_table)
        print("After initial permutation:", self.des_helper.bin_to_hex(initial_permutation_result))

        # Process block using common logic
        ciphertext = self._process_block(initial_permutation_result, round_keys_binary, round_keys_hex)

        return ciphertext

    def decipher(self, cipher_text: str) -> str:
        """
        Decrypts the given ciphertext using DES algorithm.

        :param cipher_text: The input ciphertext as a hexadecimal string
        :return: The decrypted plaintext as a binary string
        """
        round_keys_binary_reverse = self._round_keys_binary[::-1]
        round_keys_hex_reverse = self._round_keys_hex[::-1]
        ciphertext_binary = self.des_helper.hex_to_bin(cipher_text)

        # Initial Permutation
        initial_permutation_result = self.des_helper.permute(ciphertext_binary, self.initial_permutation_table)
        print("After initial permutation:", self.des_helper.bin_to_hex(initial_permutation_result))

        # Process block using common logic
        plaintext = self._process_block(initial_permutation_result, round_keys_binary_reverse, round_keys_hex_reverse)

        return plaintext


# Main -------
des = DesCipher()
pt = "123456ABCD132536"

print("Encryption")
cipher_text = des.cipher(pt)
print("Cipher Text: ", cipher_text)

print("Decryption")
text = des.decipher(cipher_text)
print("Plain Text: ", text)
