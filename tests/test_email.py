"""
Tests for Email class.
"""

import pytest
from automate_emails import email

@pytest.fixture
def empty_email(scope="class"):
    """
    Test data of empty email.
    """

    return email.Email()

@pytest.fixture
def one_recipient_email(scope="class"):
    """
    Test data of one recipient email.
    """

    new_email = email.Email()
    new_email.sender = "test1@test.com"
    new_email.recipients = ["test2@test.com"]
    new_email.subject = "Test simple test case"
    new_email.body = "Hello, it is me!\n"
    return new_email

@pytest.fixture
def many_recipients_email(scope="class"):
    """
    Test data of many recipients email.
    """

    new_email = email.Email()
    new_email.sender = "test1@test.com"
    new_email.recipients = [f"""test{i}@test.com""" for i in range(2, 17)]
    new_email.subject = "Test many recipients test case"
    new_email.body = "Hello, it is me!\n"
    return new_email


class TestEmail():
    """
    The class that tests the class Email.
    """

    def test_constructor_empty_email(self, empty_email):
        """
        Test case for constructor.
        """

        assert empty_email.sender == ""
        assert empty_email.recipients == []
        assert empty_email.subject == ""
        assert empty_email.body == ""

    def test_get_mime_text_object_empty_email(self, empty_email):
        """
        Test case for get_mime_text_object when email is empty.
        """

        actual_result = empty_email.get_mime_text_object()
        assert actual_result["Subject"] == ""
        assert actual_result["From"] == ""
        assert actual_result["To"] == ""
        assert actual_result._payload == ""

    def test_get_mime_text_object_one_recipient_email(self, one_recipient_email):
        """
        Test case for get_mime_text_object when email has one recipient.
        """

        actual_result = one_recipient_email.get_mime_text_object()
        assert actual_result["Subject"] == "Test simple test case"
        assert actual_result["From"] == "test1@test.com"
        assert actual_result["To"] == "test2@test.com"
        assert actual_result._payload == "Hello, it is me!\n"

    def test_get_mime_text_object_many_recipients_email(self, many_recipients_email):
        """
        Test case for get_mime_text_object when email has many recipients.
        """

        actual_result = many_recipients_email.get_mime_text_object()
        assert actual_result["Subject"] == "Test many recipients test case"
        assert actual_result["From"] == "test1@test.com"
        assert actual_result["To"] == ", ".join([f"""test{i}@test.com""" for i in range(2, 17)])
        assert actual_result._payload == "Hello, it is me!\n"

    def test_load_email_template_simple(self, empty_email):
        """
        Test case for load_email_template when template has one recipients.
        """

        empty_email.load_email_template("tests/test_simple_email_template", {})
        assert empty_email.sender == "test1@test.com"
        assert empty_email.recipients == ["test2@test.com"]
        assert empty_email.subject == "Test simple test case"
        assert empty_email.body == "Hello, it is me!\n"

    def test_load_email_template_many_recipients(self, empty_email):
        """
        Test case for load_email_template when template has many recipients.
        """

        empty_email.load_email_template("tests/test_many_recipients_template", {})
        assert empty_email.sender == "test1@test.com"
        assert empty_email.recipients == [f"""test{i}@test.com""" for i in range(2, 17)]
        assert empty_email.subject == "Test many recipients test case"
        assert empty_email.body == "Hello, it is me!\n"

    def test_load_email_template_substitution(self, empty_email):
        """
        Test case for load_email_template when template has substitution fields.
        """

        num1 = 1
        num2 = 2
        num3 = 3
        date = "May 4, 2021"
        time = "2 pm"
        secret_location = "The Bubbles"
        empty_email.load_email_template(
            "tests/test_substitution_template",
            {
                "num1": num1,
                "num2": num2,
                "num3": num3,
                "date": date,
                "time": time,
                "secret_location" : secret_location
            })
        assert empty_email.sender == "test1@test.com"
        assert empty_email.recipients == ["test2@test.com"]
        assert empty_email.subject == f"Test substitution {num1} {num2} {num3} test case"
        assert empty_email.body == \
            f"Dear test2,\nHello, it is me! Lets meet on {date} at {time} at {secret_location}.\n" \
                + "Cheers,\ntest1\n"
