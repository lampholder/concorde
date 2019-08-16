#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cli tool to register a Matrix user with a password generated (securely)
from their username"""
import argparse

from concorde.integrations import Matrix
from concorde.exceptions import UserRegistrationFailed

parser = argparse.ArgumentParser(description='Register matrix users with a Matrix homeserver')
parser.add_argument('--homeserver', required=True)
parser.add_argument('--homeserver-secret', required=True)
parser.add_argument('--passgen-secret', required=True)
parser.add_argument('usernames', nargs='+')
args = parser.parse_args()

homeserver_secret = args.homeserver_secret
passgen_secret = args.passgen_secret
usernames = args.usernames

matrix = Matrix(args.homeserver)

for username in args.usernames:
    try:
        print username, matrix.create_account(args.homeserver_secret, username, args.passgen_secret)
    except UserRegistrationFailed as exception:
        print username, False, exception.response_code, exception.message
