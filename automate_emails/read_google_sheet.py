"""
This module contains functions to load the google sheet data and manipulate the data.
"""

from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# reference:
# https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/


MONTH_MAP = {"january" : 1, "february" : 2, "march" : 3, "april" : 4, "may" : 5, "june" : 6,
"july" : 7, "august" : 8, "september" : 9, "october" : 10, "november" : 11, "december" : 12}

def load_google_sheet_data(sheet_id, token_json):
    """
    Returns the data in the google sheet (list of dict objects) and columns names (list).
    """

    # define the scope
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(token_json, scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open_by_key(sheet_id)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    # Assume the spreadsheet has 3 columns and the first row contains the columns names
    column_names = [
        sheet_instance.cell(1, 1).value,
        sheet_instance.cell(1, 2).value,
        sheet_instance.cell(1, 3).value
    ]

    # get all the records of the data (list of dict objects where dict represents a row entry)
    records_data = sheet_instance.get_all_records()

    return records_data, column_names


def next_meeting(data, column_names, initial_date):
    """
    Returns the row of data in a dict form for the next meeting when given the data
    from the google sheet, column names and the initial date.

    The google sheet has its first column of dates.
    """

    if not data or data == [{}] or not column_names or not initial_date:
        return {}

    date_col_name = column_names[0]

    for row in data:
        date_in_row = row[date_col_name]
        # date_in_row looks like something like "April 1 ,2021"
        date_list = date_in_row.replace(",", "").split()
        # change to ints
        month_int = MONTH_MAP[date_list[0].lower()]
        # the datetime objects takes the parameters of year, month, day
        cur_date = date(int(date_list[2]), month_int, int(date_list[1]))

        # compare with initial date and this date
        if initial_date < cur_date :
            return row

    # Means you need to update spreadsheet
    return {}
