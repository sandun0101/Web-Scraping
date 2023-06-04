import csv
import os
from datetime import datetime


def list_to_csv(data):
    """
    Write a list of lists to a CSV file.

    This function takes a list of lists containing data and writes it to a CSV file. Each inner list represents a row
    in the CSV file, and the elements within the inner lists are written as columns. The CSV file is saved with a
    new file name that includes a timestamp.

    Args:
        data (list): A list of lists containing the data to be written to the CSV file.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    directory = r"C:\Users\Sandun Wijethunga\Documents\Workspace\Upwork\Web Scraping Projects\Amazon Customer Reviews"
    filename = f"amazon_reviews_{timestamp}.csv"
    csv_file_path = os.path.join(directory, filename)

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Star Rating", "Review"])
        writer.writerows(data)
    print("CSV file saved.")
