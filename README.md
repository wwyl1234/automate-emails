# automate-emails
A collection of code that automates emails every 2nd Sunday on my machine, that reads a very specfic Google sheet and generates an email based on the next Zoom meeting that should take place.


## Pre Setup that is needed
You would need a gmail account that has enabled insecure apps to access the account to send emails.
You would also need to create a service account and its credientials to read the google sheet.
You would need a google sheet.

To run this script automatically on your machine on start (based on MAC):

1) You would need to make sure to set the program (Python launcher) you would want to run on the file (cli.py)

2) You would also need to install the local package. 

cd /path/of/automate-emails
python3 -m pip install -e .

3) You might need to change the shebang in cli.py so that it runs python3 instead of python2. This might be a python launcher limitation.

## Setup
You need the following files for the script to run (needs to be in the same directory as cli.py):
1) the service accounts' credentials in a json file
2) config file called "config"
3) the list of recipients separated by a newline characters called "recipients_list" 
4) the Zoom information called "zoom_info"


### TODOs
* Investigate how to not use that specific shebang in cli.py (probably need to setup virtual environment)
* Investigate the docs for using google sheet api from google (right now using gspread module instead of following their docs)
* Place the requirements.txt
* Can abstract this further and decouple automate_emails.py
* Add unit tests
* Can explore sending emails on different email service providers like Outlook and so forth
* add an option to store username and password in a config file for sending emails


### Notes
* It looks like one cannot use the gmail api without the gsuite account. No free option except for using the less secure way via smtp. 


## Credits
Winnie Lam