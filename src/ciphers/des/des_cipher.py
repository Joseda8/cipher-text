import random
import string

from src.ciphers.des import const


class DES:
    """
    This class represents the Data Encryption Standard (DES) algorithm.
    It provides methods for key generation, encryption, and helper functions.
    """

    def __init__(self) -> None:
        """
        Constructor method that initializes the DES object with predefined tables.
        """
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
        self._seed = self._generate_seed()
        self._key = self._generate_random_key()
        self._round_keys_binary, self._round_keys_hex = self.generate_keys(self._key)

    def _generate_seed(self) -> str:
        """
        Generates a seed for the cipher using characters representing 4-bits each.

        :return: a string with the seed for the cipher
        """
        # Create a string of numbers (0-9) and uppercase letters (A-F)
        chars = string.digits + string.ascii_uppercase[:6]

        # Shuffle the characters randomly
        seed = "".join(random.sample(chars, len(chars)))
        return seed

    def _generate_random_key(self) -> str:
        """
        Generates a random key for the cipher.

        :return: a random key as a string
        """
        # Shuffle seed to create a random key
        key = list(self._seed)
        random.shuffle(key)
        key = "".join(key)
        return key

    def hex_to_bin(self, hex_string: str) -> str:
        """
        Converts a hexadecimal string to a binary string.

        :param hex_string: The input hexadecimal string
        :return: The corresponding binary string
        """
        hex_to_bin_mapping = const.hex_to_bin_mapping
        return "".join(hex_to_bin_mapping[char] for char in hex_string)

    def bin_to_hex(self, binary_string: str) -> str:
        """
        Converts a binary string to a hexadecimal string.

        :param binary_string: The input binary string
        :return: The corresponding hexadecimal string
        """
        bin_to_hex_mapping = const.bin_to_hex_mapping
        return "".join(bin_to_hex_mapping[binary_string[i:i + 4]] for i in range(0, len(binary_string), 4))

    def bin_to_dec(self, binary: int) -> int:
        """
        Converts a binary number to a decimal number.

        :param binary: The input binary number
        :return: The corresponding decimal number
        """
        binary_str = str(binary)
        decimal = int(binary_str, 2)
        return decimal

    def dec_to_bin(self, decimal: int) -> str:
        """
        Converts a decimal number to a binary string.

        :param decimal: The input decimal number
        :return: The corresponding binary string
        """
        binary = bin(decimal)[2:]
        return binary.rjust((len(binary) + 3) // 4 * 4, "0")

    def permute(self, key: str, arr: list) -> str:
        """
        Permutes the given key based on the specified arrangement.

        :param key: The input key to be permuted
        :param arr: The arrangement table for permutation
        :return: The permuted key
        """
        return "".join(key[idx - 1] for idx in arr)

    def shift_left(self, key: str, nth_shifts: int) -> str:
        """
        Performs left circular shifts on the given key.

        :param key: The input key for circular shifts
        :param nth_shifts: The number of shifts to perform
        :return: The key after circular shifts
        """
        return key[nth_shifts % len(key):] + key[:nth_shifts % len(key)]

    def xor(self, a: str, b: str) -> str:
        """
        Performs XOR operation between two binary strings.

        :param a: The first binary string
        :param b: The second binary string
        :return: The result of the XOR operation
        """
        return "".join("0" if bit_a == bit_b else "1" for bit_a, bit_b in zip(a, b))

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
            right_expanded = self.permute(right, self.expansion_d_box_table)

            # XOR RoundKey[i] and right_expanded
            xor_result = self.xor(right_expanded, round_keys_binary[round_num])

            # S-boxes: Substituting the value from s-box table
            sbox_result = ""
            for sbox_index in range(8):
                row = self.bin_to_dec(int(xor_result[sbox_index * 6] + xor_result[sbox_index * 6 + 5]))
                col = self.bin_to_dec(int(xor_result[sbox_index * 6 + 1:sbox_index * 6 + 5]))
                val = self.s_box_table[sbox_index][row][col]
                sbox_result += self.dec_to_bin(val)

            # Straight Permutation: Rearranging the bits
            sbox_result = self.permute(sbox_result, self.straight_permutation_table)

            # XOR left and sbox_result
            xor_left_result = self.xor(left, sbox_result)
            left = xor_left_result

            # Swapper
            if round_num != 15:
                left, right = right, left

            print("Round", round_num + 1, ":", self.bin_to_hex(left), self.bin_to_hex(right), round_keys_hex[round_num])

        # Combination
        combined_result = left + right

        # Final Permutation: Rearranging bits to get ciphertext
        ciphertext = self.permute(combined_result, self.final_permutation_table)
        ciphertext = self.bin_to_hex(ciphertext)
        return ciphertext

    def cipher(self, plaintext_hex: str) -> str:
        """
        Encrypts the given plaintext using DES algorithm.

        :param plaintext_hex: The input plaintext as a hexadecimal string
        :return: The encrypted ciphertext as a binary string
        """
        round_keys_binary = self._round_keys_binary
        round_keys_hex = self._round_keys_hex
        plaintext_binary = self.hex_to_bin(plaintext_hex)

        # Initial Permutation
        initial_permutation_result = self.permute(plaintext_binary, self.initial_permutation_table)
        print("After initial permutation:", self.bin_to_hex(initial_permutation_result))

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
        ciphertext_binary = self.hex_to_bin(cipher_text)

        # Initial Permutation
        initial_permutation_result = self.permute(ciphertext_binary, self.initial_permutation_table)
        print("After initial permutation:", self.bin_to_hex(initial_permutation_result))

        # Process block using common logic
        plaintext = self._process_block(initial_permutation_result, round_keys_binary_reverse, round_keys_hex_reverse)

        return plaintext

    def generate_keys(self, key_hex: str) -> tuple:
        """
        Generates round keys for the DES algorithm.

        :param key_hex: The input key as a hexadecimal string
        :return: Tuple containing lists of round keys in binary and hexadecimal
        """
        # Convert the hexadecimal key to binary
        key_binary = self.hex_to_bin(key_hex)

        # Parity bit drop table
        key_parity_permutation = const.key_permutation_table

        # Get 56-bit key from 64-bit using the parity bits
        key_binary = self.permute(key_binary, key_parity_permutation)

        # Number of bit shifts
        shift_table = const.key_shift_table

        # Key Compression Table: Compression of key from 56 bits to 48 bits
        key_comp_permutation = const.key_compression_table

        # Splitting
        left_part = key_binary[0:28]  # rkb for RoundKeys in binary
        right_part = key_binary[28:56]  # rk for RoundKeys in hexadecimal

        round_keys_binary = []
        round_keys_hex = []

        for round_num in range(16):
            # Shifting the bits by nth shifts by checking from the shift table
            left_part = self.shift_left(left_part, shift_table[round_num])
            right_part = self.shift_left(right_part, shift_table[round_num])

            # Combination of left and right string
            combined_str = left_part + right_part

            # Compression of key from 56 to 48 bits
            round_key_binary = self.permute(combined_str, key_comp_permutation)

            round_keys_binary.append(round_key_binary)
            round_keys_hex.append(self.bin_to_hex(round_key_binary))

        return round_keys_binary, round_keys_hex


# Main -------
des = DES()
pt = "123456ABCD132536"

print("Encryption")
cipher_text = des.cipher(pt)
print("Cipher Text: ", cipher_text)

print("Decryption")
text = des.decipher(cipher_text)
print("Plain Text: ", text)
