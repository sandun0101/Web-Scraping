import csv
import pandas as pd


def save_to_csv(list1, list2, list3, csv_file_path):
    """
       Save data to a CSV file.

       This function takes three lists of data (list1, list2, list3) and saves them to a CSV file at the specified
       file path (csv_file_path). Each list represents a column in the CSV file.

       Args:
           list1 (list): List of values for the first column.
           list2 (list): List of values for the second column.
           list3 (list): List of values for the third column.
           csv_file_path (str): File path for the CSV file.

       """
    merged_list = list(zip(list1, list2, list3))
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['User Name', 'Review', 'Rating'])
        writer.writerows(merged_list)


def save_to_excel(list1, list2, list3, excel_file_path):
    """
        Save data to an Excel file.

        This function takes three lists of data (list1, list2, list3) and saves them to an Excel file at the specified
        file path (excel_file_path). Each list represents a column in the Excel file.

        Args:
            list1 (list): List of values for the first column.
            list2 (list): List of values for the second column.
            list3 (list): List of values for the third column.
            excel_file_path (str): File path for the Excel file.

        """
    data = {'User Name': list1, 'Review': list2, 'Rating': list3}
    df = pd.DataFrame(data)
    df.to_excel(excel_file_path, index=False)
