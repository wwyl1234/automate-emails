"""
A module to contain the Worksheet class.

Assumes the data in the worksheet has its column names in the first row.
The first column is called Date and has information about dates.
"""

from datetime import date

MONTH_MAP = {"january" : 1, "february" : 2, "march" : 3, "april" : 4, "may" : 5, "june" : 6,
"july" : 7, "august" : 8, "september" : 9, "october" : 10, "november" : 11, "december" : 12}

class Worksheet():
    """
    The class that represents a worksheet in Google sheet where the first row has the column names.
    The first column is called Date and has information about dates and is ordered by date.
    """

    def __init__(self, data=None, worksheet_index=None):
        """
        The constructor.

        data : list of dict objects where each dict represents a row with the keys as the
            column names and values as the entry
        worksheet_index  : int represents the worksheet index where 0 is the first worksheet
        """
        if not data or worksheet_index is None:
            # Invalid worksheet or empty
            self.data = []
            self.column_names = []
            self.worksheet_index = None

        else:
            self.data = data
            self.column_names = list(data[0].keys())
            self.worksheet_index = worksheet_index

    def next_meeting(self, initial_date):
        """
        Returns the row of data in a dict form for the next meeting when given the initial date.

        initial_date : datetime.date object represents the date of the initial_date
        """

        if not self.data or self.data == [{}] or not self.column_names or not initial_date:
            return {}

        # Assumes the first column is Date
        date_col_name = self.column_names[0]

        for row in self.data:
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
