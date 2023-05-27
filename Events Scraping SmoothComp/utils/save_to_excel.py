import pandas as pd


def save_to_excel(event_data, excel_file):
    # Create a DataFrame from the event_data dictionary
    df = pd.DataFrame(event_data)

    # Save the DataFrame to an Excel file
    excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name='Events')

    # Get the workbook and worksheet objects
    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Events']

    # Modify the worksheet to display email addresses in a single cell
    email_cell_format = workbook.add_format({'text_wrap': True})
    worksheet.set_column('G:G', None, email_cell_format)

    # Save and close the Excel file
    excel_writer._save()
    print("Operation Completed..")

