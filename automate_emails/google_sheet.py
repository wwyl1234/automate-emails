"""
This module contains functions to load the google sheet data and manipulate the data.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from automate_emails import worksheet

# reference:
# https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/


class GoogleSheet():
    """
    The GoogleSheet class that represents a Google sheet.
    """

    def __init__(self):
        self.sheet_id = ""
        self.worksheets = []

    def load(self, sheet_id, token_json):
        """
        Loads the data

        sheet_id : str that represents the Google sheet's id
        token_json : str that represents the filename of the json file containing the credentials
        """

        self.sheet_id = sheet_id
        # define the scope
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(token_json, scope)
        # authorize the clientsheet
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id)
        worksheets = sheet.worksheets()

        for index, model_worksheet in enumerate(worksheets):
            cur_worksheet = worksheet.Worksheet(model_worksheet.get_all_records(), index)
            self.worksheets.append(cur_worksheet)
