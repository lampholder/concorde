#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cli script for sending a Slack DM to a single Slack user"""

import os
import sys
import time
import argparse

from slackclient import SlackClient

parser = argparse.ArgumentParser(description='Send a DM to a Slack user')
parser.add_argument('--bot-oauth-token')
parser.add_argument('--skip-rate-limit', action='store_true')
parser.add_argument('--slack-id', required=True)
parser.add_argument('--message', required=True)
args = parser.parse_args()

token = (args.bot_oauth_token or
         (os.environ['SLACK_CLIENT_TOKEN']
          if 'SLACK_CLIENT_TOKEN' in os.environ else None))
slack_id = args.slack_id
message = args.message
skip_rate_limit = args.skip_rate_limit

assert token is not None, 'No Slack bot oauth token provided!'

slack = SlackClient(token)

send = slack.api_call('chat.postMessage',
                      channel=slack_id,
                      text=message,
                      as_user=True)

if 'error' in send:
    print >> sys.stderr, 'ERROR:', send['error'],
else:
    print >> sys.stdout, 'SENT',

if not skip_rate_limit:
    # If we're sending a whole bunch of these at once (as we'd usually expect)
    # we're going to want to respect Slack's rate limit of 1 message/second
    print >> sys.stdout, 'Respecting rate limit...',
    time.sleep(1)
    print >> sys.stdout, 'DONE'
