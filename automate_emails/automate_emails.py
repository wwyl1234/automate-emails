"""
This module contains functions that retrivie data from files and send emails.
"""

import smtplib
import getpass
import configparser
from email.mime.text import MIMEText
from datetime import date
from automate_emails import read_google_sheet


# Reference:
# https://medium.com/lyfepedia/sending-emails-with-gmail-api-and-python-49474e32c81f
# https://stackoverflow.com/questions/37201250/sending-email-via-gmail-python


def get_zoom_info(filename):
    "Get zoom info from file with filename."

    zoom_info = ""
    with open(filename, 'r') as infile:
        for line in infile:
            zoom_info += line
    return zoom_info


def get_recipients(filename):
    "Get recipients from file with filename where recipients are separated by a new line."

    recipients = []
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            recipients.append(line)
    return recipients


def send_mail(recipients, zoom_info, sheet_id, token_json):
    """Sends the email via gmail with the given recipients, zoom info, sheet_id, token_json.
    """

    server = smtplib.SMTP("smtp.gmail.com", 587)

    user = input("Username:")
    password = getpass.getpass("Password for " + user + ":")

    server.starttls()
    server.login(user, password)

    data, column_names = read_google_sheet.load_google_sheet_data(
        sheet_id,
        token_json
        )
    today = date.today()
    next_meeting = read_google_sheet.next_meeting(data, column_names, today)

    # need to get the next date of meeting
    meeting_date = next_meeting[column_names[0]]
    passage = next_meeting[column_names[1]]
    leader = next_meeting[column_names[2]]

    body = """
    Hello, everyone!
    
    Just a reminder there is ECG next Sunday ({date}) at 2 pm on Zoom: 

    {zoom_info}

    The passage is {passage} and will be led by {leader}.

    Cheers,
    Winnie Lam's bot 
    """.format(date=meeting_date, zoom_info=zoom_info, passage=passage, leader=leader)

    msg = MIMEText(body)
    sender = user
    msg['Subject']= "ECG next Sunday"
    msg['From'] = user
    msg['To'] = ", ".join(recipients)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()


def main():
    """The main function."""

    print("Loading files and environment variables...")

    today = date.today()
    recipients_list = get_recipients("recipients_list")
    loaded_zoom_info = get_zoom_info("zoom_info")

    config_file_content = ""
    with open("config") as f:
        config_file_content = f.read()

    config_parser = configparser.RawConfigParser()
    config_parser.read_string(config_file_content)

    sheet_id = config_parser.get("Env Variables", "sheet_id")
    token_json = config_parser.get("Env Variables", "token_json")

    print("Checking to see if today is the second Sunday...")
    # only send email if it is the second sunday
    # sunday is 6
    if today.weekday() == 6 and  8 <= today.day <= 14 :
        print("Attemping to send email...")
        send_mail(
            recipients_list,
            loaded_zoom_info,
            sheet_id,
            token_json
            )


if __name__ == "__main__":
    main()
