#!/usr/bin/python3

"""
The cli to run the main program.
"""

import configparser
import argparse
from automate_emails import automate_emails

def load_config_file(config_filepath):
    """
    Load config file.

    config_filepath : str represents the filepath of the config file
    """

    config_file_content = ""
    with open(config_filepath, "r") as infile:
        config_file_content = infile.read()

    config_parser = configparser.RawConfigParser()
    config_parser.read_string(config_file_content)
    email_template = config_parser.get("Env Variables", "email_template")
    sheet_id = config_parser.get("Env Variables", "sheet_id")
    token = config_parser.get("Env Variables", "token")
    worksheet_index = int(config_parser.get("Env Variables", "worksheet_index"))
    return email_template, sheet_id, token, worksheet_index

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sends email based on dates from Google sheet.")
    parser.add_argument(
        "--config",
        type=str,
        default="",
        help="The absolute or relative filepath of the config file")

    # required arguments on cli or in config file
    required_args = parser.add_argument_group('required arguments on cli or in config file')
    required_args.add_argument(
        "--email_template",
        type=str,
        default="",
        help="The absolute or relative filepath of the email template")

    required_args.add_argument(
        "--worksheet_index",
        type=int,
        default=0,
        help="The worksheet index (0 means the first worksheet)")

    required_args.add_argument(
        "--sheet_id",
        type=str,
        default="",
        help="The Google's sheet id")

    required_args.add_argument(
        "--token",
        type=str,
        default="",
        help="The absolute or relative filepath of the credientials in a json file")
    args = parser.parse_args()

    # Take variables from config file if corresponding arguments are not given
    config_email_template = ""
    config_sheet_id = ""
    config_token = ""
    config_worksheet_index = 0
    if args.config:
        config_email_template, config_sheet_id, config_token, config_worksheet_index = \
            load_config_file(args.config)
    if not args.email_template:
        args.email_template = config_email_template
    if not args.token:
        args.token = config_token
    if not args.sheet_id:
        args.sheet_id = config_sheet_id
    if not args.worksheet_index:
        if config_worksheet_index:
            args.worksheet_index = config_sheet_id

    # Validate the arguments
    if args.email_template and args.worksheet_index is not None and args.sheet_id and args.token:
        automate_emails.main(
            args.email_template,
            args.sheet_id,
            args.token,
            args.worksheet_index
        )
    else:
        print("Missing arguments")
