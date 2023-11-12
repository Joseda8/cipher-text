import json
import os
from typing import Union

import pandas as pd
from PIL import Image

class TextUtil:
    """
    This class represents a general utility class for text file operations.
    It provides methods to read content from and write content to a text file, and perform other text file operations.
    """

    def _create_directory_if_not_exists(self, filename: str) -> None:
        """
        Private function to create the directory for the given filename if it doesn"t exist.

        :param filename: the name of the file as a string
        :return: None
        """
        # Extract the directory path from the filename
        directory = os.path.dirname(filename)

        # Create the directory if it doesn"t exist
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def image_to_hex_bitmap_and_dimensions(self, image_path: str) -> tuple:
        """
        Extract the bitmap from an image and return the dimensions.

        :param image_path: The path to the image file.
        :return: A tuple containing a binary string representing the image bitmap and the image dimensions (width, height).
        """
        # Open the image file
        with Image.open(image_path) as img:
            # Get the dimensions of the image
            image_dimensions = img.size

            # Convert the image to grayscale
            img_gray = img.convert("L")

            # Get the pixel values as a flat list
            pixel_values = list(img_gray.getdata())

            # Convert pixel values to a hexadecimal string
            bitmap_hex = "".join(format(pixel, "02X") for pixel in pixel_values)

        return bitmap_hex, image_dimensions
    
    def write_image_from_hex(self, filename: str, hex_bitmap: str, image_size: tuple) -> None:
        """
        Writes an image to the specified file using the provided hexadecimal bitmap.

        :param filename: The name of the file to be written as a string.
        :param hex_bitmap: The hexadecimal string representing the image bitmap.
        :param image_size: The size of the output image (width, height).
        :return: None
        """
        self._create_directory_if_not_exists(filename)

        # Calculate the expected length of hex_bitmap based on the image size
        expected_length = image_size[0] * image_size[1] * 2  # Each pixel is represented by 2 characters

        # Ensure hex_bitmap is not shorter than expected_length
        hex_bitmap = hex_bitmap.ljust(expected_length, "0")[:expected_length]

        # Convert the hexadecimal string back to pixel values
        pixel_values = [int(hex_bitmap[i:i+2], 16) for i in range(0, len(hex_bitmap), 2)]

        # Create an image with the specified size
        img = Image.new("L", image_size)

        # Put the pixel values in the image
        img.putdata(pixel_values)

        # Save the image to the specified file path
        img.save(filename)

    def write_dataframe_to_csv(self, filename: str, dataframe: pd.DataFrame) -> None:
        """
        Saves the provided Pandas DataFrame to the specified CSV file.

        :param filename: the name of the CSV file to be written as a string
        :param dataframe: the Pandas DataFrame to be saved
        :return: None
        """
        self._create_directory_if_not_exists(filename)

        # Save the DataFrame to CSV
        dataframe.to_csv(filename, index=False)

    def read_csv_to_dataframe(self, filename: str) -> Union[pd.DataFrame, None]:
        """
        Reads the data from the specified CSV file into a Pandas DataFrame.

        :param filename: the name of the CSV file to be read as a string
        :return: the Pandas DataFrame containing the data, or None if the file does not exist
        """
        if not os.path.exists(filename):
            return None

        # Read the CSV file into a DataFrame
        dataframe = pd.read_csv(filename)
        return dataframe

    def write_text_to_file(self, filename: str, content: str) -> None:
        """
        Writes the provided content to the specified text file.

        :param filename: the name of the file to be written as a string
        :param content: the content to be written to the file as a string
        :return: None
        """
        self._create_directory_if_not_exists(filename)

        with open(filename, "w") as file:
            file.write(content)

    def write_json_to_file(self, filename: str, data: dict) -> None:
        """
        Writes the provided data to the specified JSON file.

        :param filename: the name of the file to be written as a string
        :param data: the data to be written to the file as a dictionary
        :return: None
        """
        self._create_directory_if_not_exists(filename)

        with open(filename, "w") as file:
            json.dump(data, file)

    def read_file(self, filename: str) -> str:
        """
        Reads the content from the specified text file.

        :param filename: the name of the file to be read as a string
        :return: the content of the file as a string
        """
        with open(filename, "r") as file:
            content = file.read()
        return content

    def read_json_from_file(self, filename: str) -> dict:
        """
        Reads the data from the specified JSON file.

        :param filename: the name of the file to be read as a string
        :return: the data from the file as a dictionary
        """
        with open(filename, "r") as file:
            data = json.load(file)
        return data
