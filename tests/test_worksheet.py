"""
Tests for Worksheet class.
"""

import pytest
import datetime
from automate_emails import worksheet

@pytest.fixture
def empty_worksheet(scope="class"):
    """
    Test data of empty worksheet.
    """

    return worksheet.Worksheet()

@pytest.fixture
def one_row_worksheet(scope="class"):
    """
    Test data of one row worksheet.
    """

    return worksheet.Worksheet(
        [{"Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}],
        0)

@pytest.fixture
def multi_rows_worksheet(scope="class"):
    """
    Test data of multirows worksheet.
    """

    return worksheet.Worksheet(
        [{"Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"},
        {"Date": "May 3 ,2021", "Activity": "Play Games!!", "Leader": "RandomPerson2"},
        {"Date": "May 4 ,2021", "Activity": "Play Games!!!", "Leader": "RandomPerson3"}],
        0)

@pytest.fixture
def multi_rows_worksheet_not_in_order(scope="class"):
    """
    Test data of multirows workeet that is not in order by date.
    """

    return worksheet.Worksheet(
        [{"Date": "May 3 ,2021", "Activity": "Play Games!!", "Leader": "RandomPerson2"},
        {"Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"},
        {"Date": "May 4 ,2021", "Activity": "Play Games!!!", "Leader": "RandomPerson3"}],
        0)

@pytest.fixture
def no_date_col_name_worksheet(scope="class"):
    """
    Test data has no column name called 'Date'.
    """

    return worksheet.Worksheet(
        [{"Blah": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}],
        0)

@pytest.fixture
def date_in_fifth_col_worksheet(scope="class"):
    """
    Test data where 5th column's name is called 'Date'.
    """

    return worksheet.Worksheet(
        [{"Game" : "Escape Room",
        "Co-leader" : "Somebody1",
        "Activity": "Play Games!",
        "Leader": "RandomPerson1",
        "Date": "May 2 ,2021"}],
        0)

@pytest.fixture
def date_trailing_left_spaces_worksheet(scope="class"):
    """
    Test data where the column name has trailing left spaces with 'Date'.
    """

    return worksheet.Worksheet(
        [{"    Date": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}],
        0)

@pytest.fixture
def date_trailing_right_spaces_worksheet(scope="class"):
    """
    Test data where the column name has trailing right spaces with 'Date'.
    """

    return worksheet.Worksheet(
        [{"Date    ": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}],
        0)

@pytest.fixture
def date_spaces_both_sides_worksheet(scope="class"):
    """
    Test data where the column names has spaces both sides of 'Date'.
    """

    return worksheet.Worksheet(
        [{"    Date    ": "May 2 ,2021", "Activity": "Play Games!", "Leader": "RandomPerson1"}],
        0)

class TestWorksheet():
    """
    The class that tests the class Worksheet.
    """

    def test_next_meeting_empty(self, empty_worksheet):
        """
        Test case for next_meeting when Worksheet is empty.
        """

        assert empty_worksheet.next_meeting(None) == {}
        assert empty_worksheet.next_meeting(datetime.date(2021, 5, 2)) == {}


    def test_next_meeting_one_row_typical(self, one_row_worksheet):
        """
        Test case for next_meeting when one row of data has a date after initial_date.
        """

        initial_date = datetime.date(2021, 5, 1)
        actual_result = one_row_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 2 ,2021"
        assert actual_result.get("Activity") == "Play Games!"
        assert actual_result.get("Leader") == "RandomPerson1"


    def test_next_meeting_one_row_date_expired(self, one_row_worksheet):
        """
        Test case for next_meeting when one row of data does not have a date after intial_date.
        """

        initial_date = datetime.date(2021, 5, 3)
        actual_result = one_row_worksheet.next_meeting(initial_date)
        assert actual_result == {}


    def test_next_meeting_one_row_same(self, one_row_worksheet):
        """
        Test case for next_meeting when one row of data has the same date as initial_date.
        """

        initial_date = datetime.date(2021, 5, 2)
        actual_result = one_row_worksheet.next_meeting(initial_date)
        assert actual_result == {}

    def test_next_meeting_multi_rows_typical(self, multi_rows_worksheet):
        """
        Test case for next_meeting when multi rows of data has a date after initial_date.
        """

        initial_date = datetime.date(2021, 5, 1)
        actual_result = multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 2 ,2021"
        assert actual_result.get("Activity") == "Play Games!"
        assert actual_result.get("Leader") == "RandomPerson1"

        initial_date = datetime.date(2021, 5, 2)
        actual_result = multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 3 ,2021"
        assert actual_result.get("Activity") == "Play Games!!"
        assert actual_result.get("Leader") == "RandomPerson2"

        initial_date = datetime.date(2021, 5, 3)
        actual_result = multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 4 ,2021"
        assert actual_result.get("Activity") == "Play Games!!!"
        assert actual_result.get("Leader") == "RandomPerson3"

    def test_next_meeting_multi_rows_date_expired(self, multi_rows_worksheet):
        """
        Test case for next_meeting when multi rows of data does not have a date after initial_date.
        """

        initial_date = datetime.date(2021, 5, 10)
        actual_result = multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result == {}

        initial_date = datetime.date(2022, 1, 1)
        actual_result = multi_rows_worksheet.next_meeting(initial_date)
        assert actual_result == {}

    def test_next_meeting_multi_rows_not_in_order(self, multi_rows_worksheet_not_in_order):
        """
        Test case for next_meeting when multi rows of data is not in order and has dates
        after initial_date.
        """

        initial_date = datetime.date(2021, 5, 1)
        actual_result = multi_rows_worksheet_not_in_order.next_meeting(initial_date)
        assert actual_result.get("Date") == "May 2 ,2021"
        assert actual_result.get("Activity") == "Play Games!"
        assert actual_result.get("Leader") == "RandomPerson1"

    def test_get_date_column_index_no_date(self, no_date_col_name_worksheet):
        """
        Test case for get_date_column_index when no column names are called 'Date'.
        """

        actual_result = no_date_col_name_worksheet.get_date_column_index()
        assert actual_result == -1

    def test_get_date_column_index_first_col(self, one_row_worksheet):
        """
        Test case for get_date_column_index when first column name is 'Date'.
        """

        actual_result = one_row_worksheet.get_date_column_index()
        assert actual_result == 0

    def test_get_date_column_index_fifth_col(self, date_in_fifth_col_worksheet):
        """
        Test case for get_date_column_index when fifth column name is 'Date'.
        """

        actual_result = date_in_fifth_col_worksheet.get_date_column_index()
        assert actual_result == 4

    def test_get_date_column_index_left_trailing_spaces(self, date_trailing_left_spaces_worksheet):
        """
        Test case for get_date_column_index when column name
        has left trailing spaces with 'Date'.
        """

        actual_result = date_trailing_left_spaces_worksheet.get_date_column_index()
        assert actual_result == 0

    def test_get_date_column_index_right_trailing_spaces(self, date_trailing_right_spaces_worksheet):
        """
        Test case for get_date_column_index when column name
        has right trailing spaces with 'Date'.
        """

        actual_result = date_trailing_right_spaces_worksheet.get_date_column_index()
        assert actual_result == 0

    def test_get_date_column_index_dates_spaces_both_sides(self, date_spaces_both_sides_worksheet):
        """
        Test case for get_date_column_index when column name
        has left and right trailing spaces with 'Date'.
        """

        actual_result = date_spaces_both_sides_worksheet.get_date_column_index()
        assert actual_result == 0
