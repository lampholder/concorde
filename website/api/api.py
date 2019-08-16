# -*- coding: utf-8 -*-
"""API to claim pre-registered accounts on a Matrix homeserver - these accounts
have been registered with generated passwords (a function of the username, keyed
on migration secret)."""
import json
import hmac
import hashlib
import yaml

from flask import Flask
from flask import request
from flask_cors import CORS

from matrix_client.errors import MatrixRequestError

from concorde.integrations import Matrix
from concorde.exceptions import PasswordAlreadyReset

app = Flask(__name__)
CORS(app)

config = yaml.load(open('config.yaml', 'r'))

HOMESERVER = config['homeserver']
PASSGEN_SECRET = config['passgen_secret']       # Used to generate passwords from username
MIGRATION_SECRET = config['migration_secret']   # Used to validate user was sent link by us

def response(code, message, error=None):
    """Format a standard API response body"""
    response_object = {
        'response_code': code,
        'message': message
        }
    if error:
        response_object['error'] = error
    return json.dumps(response_object)

SUCCESS = response(200,
                   'Your account has been successfully claimed!')
REQUEST_VALIDATION_FAILED = response(401,
        ('Your request to claim this account could not ' +
                                      'be validated - please contact your community ' +
                                      'administrator.'),
                                     'CODE_VALIDATION_FAILURE')
ALREADY_CLAIMED = response(401,
                           ('This account has already been claimed - ' +
                            'please speak to your community administrator.'),
                           'PASSWORD_ALREADY_RESET')

@app.route('/availability')
def availability():
    """Check we're deployed correctly"""
    return 'I\'m here!'

@app.route('/claim', methods=['POST'])
def claim():
    """Complete claim of a migrated account. Works by using the passgen_secret to try
    and log in as the user with the generated password and change their password to
    the requested new password.
    If we can't log in with the generated password we assume this means they've already
    changed their password successfully."""
    content = request.get_json()
    username = content['username'] if 'username' in content else ''
    code = content['code'] if 'code' in content else ''
    display_name = content['displayName'] if 'displayName' in content else None
    new_password = content['password']

    if not request_is_valid(username, code):
        print 'CONCORDE: INVALID_REQUEST %s (%s) - %s' % (username,
                                                          display_name, code)
        return REQUEST_VALIDATION_FAILED

    matrix = Matrix(HOMESERVER)
    try:
        matrix.claim_account(username, PASSGEN_SECRET, new_password, display_name)
        print 'CONCORDE: SUCCESS %s (%s)' % (username, display_name)
        return SUCCESS
    except PasswordAlreadyReset:
        print 'CONCORDE: ALREADY_CLAIMED %s (%s)' % (username, display_name)
        return ALREADY_CLAIMED
    except MatrixRequestError as exception:
        print 'CONCORDE: GENERIC_FAILURE %s (%s) - %s' % (username,
                                                          display_name,
                                                          exception.code)
        return json.dumps({
            'response_code': exception.code,
            'message': 'This request failed - please try again later.',
            'error': 'GENERIC_FAILURE'
            })

def request_is_valid(username, code):
    """Validate that the code provided has been hashed using the secret shared
    with the link-generation cli script"""
    # Establish the validity of the request:
    if username == '' or code == '':
        return False

    mac = hmac.new(key=MIGRATION_SECRET,
                   digestmod=hashlib.sha1)
    mac.update(username)

    return mac.hexdigest() == code


if __name__ == '__main__':
    app.run()
