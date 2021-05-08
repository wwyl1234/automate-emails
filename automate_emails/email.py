"""
This module contains class Email.
"""

from email.mime.text import MIMEText

class Email():
    """
    The Email class.
    """

    def __init__(self):
        """
        The constructor.
        """

        self.sender = ""
        self.recipients = []
        self.subject = ""
        self.body = ""

    def get_mime_text_object(self):
        """
        Returns MIMEText object of the email.
        """

        msg = MIMEText(self.body)
        msg["Subject"]= self.subject
        msg["From"] = self.sender
        if not self.recipients:
            msg["To"] = ""
        msg["To"] = ", ".join(self.recipients)
        return msg

    def load_email_template(self, email_template_file, keywords):
        """
        Loads the email template file and substitues keywords.

        email_template_file : str filename of email template
        keywords: dict where keys are keywords in email template and values
            are the words to replace the keywords
        """

        sender_flag = False
        recipients_flag = False
        subject_flag = False
        body_flag = False
        with open(email_template_file, "r") as infile:
            content = infile.read().splitlines()
            for line in content:
                if line.startswith("SENDER"):
                    sender_flag = True
                    recipients_flag = False
                    subject_flag = False
                    body_flag = False
                    continue
                if line.startswith("RECIPIENTS"):
                    sender_flag = False
                    recipients_flag = True
                    subject_flag = False
                    body_flag = False
                    continue
                if line.startswith("SUBJECT"):
                    sender_flag = False
                    recipients_flag = False
                    subject_flag = True
                    body_flag = False
                    continue
                if line.startswith("BODY"):
                    sender_flag = False
                    recipients_flag = False
                    subject_flag = False
                    body_flag = True
                    continue
                if sender_flag:
                    self.sender = line.strip()
                if recipients_flag:
                    self.recipients.append(line.strip())
                if subject_flag:
                    self.subject += line.strip() #subject should be in one line
                if body_flag:
                    self.body += line.strip() + "\n"

        for key, value in keywords.items():
            self.subject = self.subject.replace("{" + str(key) + "}", str(value))
            self.body = self.body.replace("{" + str(key) + "}", str(value))
