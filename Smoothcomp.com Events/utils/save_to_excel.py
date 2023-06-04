import pandas as pd


def save_to_excel(event_data, excel_file):
    """
       Saves event data to an Excel file.

       Args:
           event_data (dict): A dictionary containing the event data.
           excel_file (str): The path of the Excel file to save the data to.
    """
    df = pd.DataFrame(event_data)

    excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name='Events')

    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Events']

    email_cell_format = workbook.add_format({'text_wrap': True})
    worksheet.set_column('G:G', None, email_cell_format)

    excel_writer._save()
    print("Operation Completed..")

