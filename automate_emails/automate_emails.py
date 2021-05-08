"""
This module contains functions that retrivie data from files and send emails.
"""

import smtplib
import getpass
import configparser
from datetime import date
from automate_emails import google_sheet
from automate_emails import email

# Reference:
# https://medium.com/lyfepedia/sending-emails-with-gmail-api-and-python-49474e32c81f
# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python

def send_mail(email_template_filename, keywords):
    """
    Sends the email via gmail.

    email_template_filename : str that represents the filename of the email template
    keywords : dict where keys are words in the email template to be replaced by the
        corresponding value
    """

    server = smtplib.SMTP("smtp.gmail.com", 587)

    user = input("Username:")
    password = getpass.getpass("Password for " + user + ":")

    server.starttls()
    server.login(user, password)

    new_email = email.Email()
    new_email.load_email_template(email_template_filename, keywords)
    server.sendmail(
        new_email.sender,
        new_email.recipients,
        new_email.get_mime_text_object().as_string())
    server.quit()


def main():
    """
    The main function.
    """

    print("Loading files and environment variables...")

    today = date.today()
    config_file_content = ""
    with open("config") as infile:
        config_file_content = infile.read()

    config_parser = configparser.RawConfigParser()
    config_parser.read_string(config_file_content)
    sheet_id = config_parser.get("Env Variables", "sheet_id")
    token_json = config_parser.get("Env Variables", "token_json")

    sheet = google_sheet.GoogleSheet()
    sheet.load(sheet_id, token_json)
    # This google sheet has only 1 worksheet
    worksheet = sheet.worksheets[0]
    today = date.today()
    next_meeting = worksheet.next_meeting(today)
    keywords = {
        "date" : next_meeting[worksheet.column_names[0]],
        "passage" : next_meeting[worksheet.column_names[1]],
        "leader" : next_meeting[worksheet.column_names[2]]
    }

    print("Checking to see if today is the second Sunday...")
    # only send email if it is the second sunday
    # sunday is 6
    if today.weekday() == 6 and  8 <= today.day <= 14 :
        print("Attemping to send email...")
        send_mail(
            "ECG_email_template",
            keywords
            )

if __name__ == "__main__":
    main()
