import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt

from src.util.logger import setup_logging


# Set up the logging configuration
logger = setup_logging()


class GraphUtil:
    """
    This class provides utility methods for creating bar graphs from CSV files.
    """

    def create_bar_graph(self, csv_file_path: str, output_folder: str) -> None:
        """
        Create a bar graph from a CSV file and save it as an image.

        :param csv_file_path: The path to the CSV file as a string.
        :param output_folder: The path to the output folder as a string.
        :return: None
        """
        try:
            # Load only the first 100 rows of the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path, nrows=20)

            # Assuming your CSV file has columns like "ngram" and "frequency"
            # Replace these column names with the actual column names in your CSV file
            category_column = "ngram"
            value_column = "frequency"

            # Plotting the bar graph
            plt.bar(df[category_column], df[value_column])

            # Adding labels and title
            plt.xlabel("Ngrams")
            plt.ylabel("Frequency")
            plt.title(f"Bar Graph from {os.path.basename(csv_file_path)} (First 20 rows)")

            # Rotate x-axis labels for better readability if needed
            plt.xticks(rotation=45)

            # Save the plot as an image in the specified output folder
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(csv_file_path))[0]}_bar_graph.png")
            plt.savefig(output_image_path)
            
            logger.info(f"Bar graph created and saved at: {output_image_path}")

        except Exception as e:
            logger.error(f"Error creating bar graph: {e}")

        finally:
            # Clear the plot to release resources
            plt.clf()


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create bar graphs from CSV files in a folder.")
    parser.add_argument("--folder_path", help="Path to the folder containing CSV files", required=True)
    args = parser.parse_args()

    folder_path = args.folder_path

    # Check if the folder path is valid
    if not os.path.isdir(folder_path):
        logger.error(f"Error: {folder_path} is not a valid directory.")
        exit()

    # Get a list of all CSV files in the specified folder
    csv_files = [file_name for file_name in os.listdir(folder_path) if file_name.endswith(".csv")]

    # Create bar graphs for each CSV file in the folder
    graph_util = GraphUtil()
    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        graph_util.create_bar_graph(csv_file_path, folder_path)
