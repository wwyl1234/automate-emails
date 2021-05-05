"""
Tests for read_google_sheet module.
"""

import datetime
from automate_emails import read_google_sheet

# data, column_names, initial_date

def test_next_meeting_empty():
    """
    Test cases for next_meeting when inputs are empty or None object.
    """

    assert read_google_sheet.next_meeting([{}], [], None) == {}
    assert read_google_sheet.next_meeting([], [], None) == {}
    assert read_google_sheet.next_meeting([{}], None, None) == {}
    assert read_google_sheet.next_meeting([], None, None) == {}
    assert read_google_sheet.next_meeting(None, None, None) == {}


def test_next_meeting_typical():
    """
    Test cases for next_meeting when data has a date after initial_date.
    """

    data_one_row = [{"Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}]
    column_names = ["Date", "Activity", "Leader"]
    initial_date = datetime.date(2021, 5, 1)

    actual_result = read_google_sheet.next_meeting(data_one_row, column_names, initial_date)
    assert actual_result.get("Date") == "May 2 ,2021"
    assert actual_result.get("Activity") == "Play Games!"
    assert actual_result.get("Leader") == "RandomPerson1"
