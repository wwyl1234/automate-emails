# automate-emails
A collection of code that automates emails every 2nd Sunday on my machine, that reads a very specfic Google sheet and generates an email based on the email template.


## Pre Setup that is needed
You would need a gmail account that has enabled insecure apps to access the account to send emails.
You would also need to create a service account and its credientials to read the google sheet.
You would need a google sheet.

To run this script automatically on your machine on start (based on MAC):

1) You would need to make sure to set the program (Python launcher) you would want to run the file cli.py.

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
token_json = <filename_of_credentials_of_service_account_as_json_file>
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


4) You need to setup the virtual environment in the same directory as cli.py


### TODOs
* Investigate the docs for using google sheet api from google (right now using gspread module instead of following their docs
* Can explore sending emails on different email service providers like Outlook and so forth
* add an option to store username and password in a config file for sending emails

### Notes
* It looks like one cannot use the gmail api without the gsuite account. No free option except for using the less secure way via smtp. 


### Testing
To run tests, activate the virtual environment and run pytest in the directory where cli.py is located at. It should look something like this.
```
(env) Winnies-MacBook-Air:automate-emails winnielam$ pytest
=========================================== test session starts ===========================================
platform darwin -- Python 3.6.1, pytest-4.4.2, py-1.8.0, pluggy-0.11.0
rootdir: /Users/winnielam/projects/automate-emails
collected 2 items                                                                                         

tests/test_read_google_sheet.py ..                                                                  [100%]

======================================== 2 passed in 0.57 seconds =========================================
(env) Winnies-MacBook-Air:automate-emails winnielam$ pytest
=========================================== test session starts ===========================================
platform darwin -- Python 3.6.1, pytest-4.4.2, py-1.8.0, pluggy-0.11.0
rootdir: /Users/winnielam/projects/automate-emails
collected 2 items                                                                                         

tests/test_read_google_sheet.py ..                                                                  [100%]

======================================== 2 passed in 0.53 seconds =========================================
```

## Credits
Winnie Lam