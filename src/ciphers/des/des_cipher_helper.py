import random
import string

from src.ciphers.des import const


class DesCipherHelper:
    """
    Helper class for DES (Data Encryption Standard) cipher operations.
    """

    @staticmethod
    def hex_to_bin(hex_string: str) -> str:
        """
        Converts a hexadecimal string to a binary string.

        :param hex_string: The input hexadecimal string
        :return: The corresponding binary string
        """
        hex_to_bin_mapping = const.hex_to_bin_mapping
        return "".join(hex_to_bin_mapping[char] for char in hex_string)

    @staticmethod
    def bin_to_hex(binary_string: str) -> str:
        """
        Converts a binary string to a hexadecimal string.

        :param binary_string: The input binary string
        :return: The corresponding hexadecimal string
        """
        bin_to_hex_mapping = const.bin_to_hex_mapping
        return "".join(bin_to_hex_mapping[binary_string[i:i + 4]] for i in range(0, len(binary_string), 4))

    @staticmethod
    def bin_to_dec(binary: int) -> int:
        """
        Converts a binary number to a decimal number.

        :param binary: The input binary number
        :return: The corresponding decimal number
        """
        binary_str = str(binary)
        decimal = int(binary_str, 2)
        return decimal

    @staticmethod
    def dec_to_bin(decimal: int) -> str:
        """
        Converts a decimal number to a binary string.

        :param decimal: The input decimal number
        :return: The corresponding binary string
        """
        binary = bin(decimal)[2:]
        return binary.rjust((len(binary) + 3) // 4 * 4, "0")

    @staticmethod
    def permute(key: str, arr: list) -> str:
        """
        Permutes the given key based on the specified arrangement.

        :param key: The input key to be permuted
        :param arr: The arrangement table for permutation
        :return: The permuted key
        """
        return "".join(key[idx - 1] for idx in arr)

    @staticmethod
    def shift_left(key: str, nth_shifts: int) -> str:
        """
        Performs left circular shifts on the given key.

        :param key: The input key for circular shifts
        :param nth_shifts: The number of shifts to perform
        :return: The key after circular shifts
        """
        return key[nth_shifts % len(key):] + key[:nth_shifts % len(key)]

    @staticmethod
    def xor(a: str, b: str) -> str:
        """
        Performs XOR operation between two binary strings.

        :param a: The first binary string
        :param b: The second binary string
        :return: The result of the XOR operation
        """
        return "".join("0" if bit_a == bit_b else "1" for bit_a, bit_b in zip(a, b))

    @staticmethod
    def _generate_seed() -> str:
        """
        Generates a seed for the cipher using characters representing 4-bits each.

        :return: a string with the seed for the cipher
        """
        # Create a string of numbers (0-9) and uppercase letters (A-F)
        seed = string.digits + string.ascii_uppercase[:6]
        return seed

    @staticmethod
    def _generate_random_key(seed: str) -> str:
        """
        Generates a random key for the cipher.

        :param seed: The seed for key generation
        :return: a random key as a string
        """
        # Shuffle seed to create a random key
        key = list(seed)
        random.shuffle(key)
        key = "".join(key)
        return key

    @staticmethod
    def generate_keys(key_hex: str) -> tuple:
        """
        Generates round keys for the DES algorithm.

        :param key_hex: The input key as a hexadecimal string
        :return: Tuple containing lists of round keys in binary and hexadecimal
        """
        seed = DesCipherHelper._generate_seed()

        # Convert the hexadecimal key to binary
        key_binary = DesCipherHelper.hex_to_bin(key_hex)

        # Parity bit drop table
        key_parity_permutation = const.key_permutation_table

        # Get 56-bit key from 64-bit using the parity bits
        key_binary = DesCipherHelper.permute(
            key_binary, key_parity_permutation)

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
            left_part = DesCipherHelper.shift_left(
                left_part, shift_table[round_num])
            right_part = DesCipherHelper.shift_left(
                right_part, shift_table[round_num])

            # Combination of left and right string
            combined_str = left_part + right_part

            # Compression of key from 56 to 48 bits
            round_key_binary = DesCipherHelper.permute(
                combined_str, key_comp_permutation)

            round_keys_binary.append(round_key_binary)
            round_keys_hex.append(DesCipherHelper.bin_to_hex(round_key_binary))

        return round_keys_binary, round_keys_hex
