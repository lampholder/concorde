# coding=utf-8
"""Handles the Slack side of business."""

from slackclient import SlackClient

class Slack(object):
    """Class for messaging the Slack users"""

    def __init__(self, slack_token):
        """Requires the slack bot oauth token"""
        self._slack = SlackClient(slack_token)

    def team(self):
        """Gets team details"""
        return self._slack.api_call('team.info')

    def list_users(self):
        """Lists all the users in the attached team."""
        return self._slack.api_call('users.list')

    def user(self, user_id):
        """Fetch the details for a specific user."""
        return self._slack.api_call('user.info',
                                    user=user_id)

    def direct_message(self, user, message):
        """Send a direct message to the specified user."""
        self._slack.api_call('chat.postMessage',
                             channel=user,
                             text=message,
                             as_user=True)
