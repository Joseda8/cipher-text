class TextUtil:
    """
    This class represents a general utility class for text file operations.
    It provides methods to read content from and write content to a text file, and perform other text file operations.
    """

    def write_text_to_file(self, filename: str, content: str) -> None:
        """
        Writes the provided content to the specified text file.

        :param filename: the name of the file to be written as a string
        :param content: the content to be written to the file as a string
        :return: None
        """
        with open(filename, 'w') as file:
            file.write(content)

    def read_file(self, filename: str) -> str:
        """
        Reads the content from the specified text file.

        :param filename: the name of the file to be read as a string
        :return: the content of the file as a string
        """
        with open(filename, 'r') as file:
            content = file.read()
        return content
