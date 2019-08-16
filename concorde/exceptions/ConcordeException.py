# coding=utf-8
"""Concorde Exceptions."""

class PasswordAlreadyReset(Exception):
    """The password generated for this username has already been reset."""
    pass

class UserRegistrationFailed(Exception):
    """Failed to register the user with the homeserver."""

    def __init__(self, response_code, message):
        super(UserRegistrationFailed, self).__init__(message)

        self.response_code = response_code
