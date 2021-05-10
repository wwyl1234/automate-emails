# automate-emails
A collection of code that automates emails every 2nd Sunday on my machine, that reads a very specfic Google sheet and generates an email based on the email template.

## Pre Setup that is needed
You would need a gmail account that has enabled insecure apps to access the account to send emails.
You would also need to create a service account and its credientials to read the google sheet.
You would need a google sheet.

To run this script automatically on your machine on start (based on MAC):

1) You would need to make sure to set the program (Python launcher or set up a cron job) you would want to run the file cli.py.

2) You would also need to install the local package. 
```
cd /path/of/automate-emails
python3 -m pip install -e .
```

## Setup
You need the following files for the script to run (needs to be in the same directory as cli.py):
1) the service accounts' credentials in a json file
2) config file called "config"

* The config file looks like something like this:
```
[Env Variables]
sheet_id = <google_sheet_id>
token = <filepath_of_credentials_of_service_account_as_json_file>
email_template = <filepath_of_email_template>
worksheet_index = <int of the worksheet index>
```

3) The email template. Currently, the program looks for 'ECG_email_template'. The email template takes on the form as
```
SENDER
<sender_email>
RECIPIENTS
<recipient1_email>
<recipient2_email>
.
.
.
<recipientN_email>
SUBJECT
<subject>
BODY
<body>
```
can add substitution in the template by adding curly brackets over keywords like '{date}'.


Here is an example of a email template file.
```
SENDER
test1@test.com
RECIPIENTS
test2@test.com
test3@test.com
SUBJECT
This is test email number {email_num}.
BODY
Hello testers,
How are you doing? 
Please give me your results by {date}.
Cheers,
test1
```


4) You can use the cli to call the program:
```python3 cli.py -h
usage: cli.py [-h] [--config CONFIG] [--email_template EMAIL_TEMPLATE]
              [--worksheet_index WORKSHEET_INDEX] [--sheet_id SHEET_ID]
              [--token TOKEN]

Sends email based on dates from Google sheet.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       The absolute or relative filepath of the config file

required arguments on cli or in config file:
  --email_template EMAIL_TEMPLATE
                        The absolute or relative filepath of the email
                        template
  --worksheet_index WORKSHEET_INDEX
                        The worksheet index (0 means the first worksheet)
  --sheet_id SHEET_ID   The Google's sheet id
  --token TOKEN         The absolute or relative filepath of the credientials
                        in a json file
```


### TODOs
* Investigate the docs for using google sheet api from google (right now using gspread module instead of following their docs
* Can explore sending emails on different email service providers like Outlook and so forth

### Notes
* It looks like one cannot use the gmail api without the gsuite account. No free option except for using the less secure way via smtp. 

### Testing
To run tests, activate the virtual environment and run pytest in the directory where cli.py is located at. It should look something like this.
```
(env) Winnies-MacBook-Air:automate-emails winnielam$ pytest
================================================================= test session starts =================================================================
platform darwin -- Python 3.6.1, pytest-4.4.2, py-1.8.0, pluggy-0.11.0
rootdir: /Users/winnielam/projects/automate-emails
collected 20 items                                                                                                                                    

tests/test_email.py .......                                                                                                                     [ 35%]
tests/test_worksheet.py .............                                                                                                           [100%]

============================================================== 20 passed in 0.15 seconds ==============================================================

```

## Credits
Winnie Lam