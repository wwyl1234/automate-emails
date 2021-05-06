"""
Tests for read_google_sheet module.
"""

import datetime
from automate_emails import worksheet


class TestWorksheet():
    """
    The class that tests the class Worksheet.
    """

    one_row_worksheet = worksheet.Worksheet(
        [{"Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}],
        0)
    multi_rows_worksheet = worksheet.Worksheet(
        [{"Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"},
        {"Date": "May 3 ,2021", "Activity": "Play Games!!", "Leader": "RandomPerson2"},
        {"Date": "May 4 ,2021", "Activity": "Play Games!!!", "Leader": "RandomPerson3"}],
        0)

    def test_next_meeting_empty(self):
        """
        Test case for next_meeting when Worksheet is empty.
        """

        empty_worksheet = worksheet.Worksheet()
        assert empty_worksheet.next_meeting(None) == {}
        assert empty_worksheet.next_meeting(datetime.date(2021, 5, 2)) == {}


    def test_next_meeting_one_row_typical(self):
        """
        Test case for next_meeting when one row of data has a date after initial_date.
        """

        initial_date = datetime.date(2021, 5, 1)
        actual_result = self.one_row_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 2 ,2021"
        assert actual_result.get("Activity") == "Play Games!"
        assert actual_result.get("Leader") == "RandomPerson1"


    def test_next_meeting_one_row_date_expired(self):
        """
        Test case for next_meeting when one row of data does not have a date after intial_date.
        """

        initial_date = datetime.date(2021, 5, 3)
        actual_result = self.one_row_worksheet.next_meeting(initial_date)
        assert actual_result == {}


    def test_next_meeting_one_row_same(self):
        """
        Test case for next_meeting when one row of data has the same date as initial_date.
        """

        initial_date = datetime.date(2021, 5, 2)
        actual_result = self.one_row_worksheet.next_meeting(initial_date)
        assert actual_result == {}

    def test_next_meeting_multi_rows_typical(self):
        """
        Test case for next_meeting when multi rows of data has a date after initial_date.
        """

        initial_date = datetime.date(2021, 5, 1)
        actual_result = self.multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 2 ,2021"
        assert actual_result.get("Activity") == "Play Games!"
        assert actual_result.get("Leader") == "RandomPerson1"

        initial_date = datetime.date(2021, 5, 2)
        actual_result = self.multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 3 ,2021"
        assert actual_result.get("Activity") == "Play Games!!"
        assert actual_result.get("Leader") == "RandomPerson2"

        initial_date = datetime.date(2021, 5, 3)
        actual_result = self.multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 4 ,2021"
        assert actual_result.get("Activity") == "Play Games!!!"
        assert actual_result.get("Leader") == "RandomPerson3"

    def test_next_meeting_multi_rows_date_expired(self):
        """
        Test case for next_meeting when multi rows of data does not have a date after initial_date
        """

        initial_date = datetime.date(2021, 5, 10)
        actual_result = self.multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result == {}

        initial_date = datetime.date(2022, 1, 1)
        actual_result = self.multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result == {}
