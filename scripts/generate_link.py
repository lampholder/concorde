#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cli tool to generate a secure unique link to the migration tool"""
import hmac
import hashlib
import urllib
import argparse

parser = argparse.ArgumentParser(description='Generate a link to the account claim')
parser.add_argument('--migration-secret', required=True)
parser.add_argument('--link-url', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--display-name')
args = parser.parse_args()

mac = hmac.new(key=args.migration_secret,
               digestmod=hashlib.sha1)

mac.update(args.username)

params = {
    'username': args.username,
    'code': mac.hexdigest()
    }

if args.display_name:
    params['displayName'] = args.display_name

print args.link_url + '?' + urllib.urlencode(params)
