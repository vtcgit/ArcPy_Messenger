__author__ = 'Brian Farrell'
__date_created__ = '1/30/14'

import __credentials, ScriptMessaging
import os

messenger = ScriptMessaging.Messenger(__credentials.username, __credentials.password, "Test Case")

# Test Handled Exception
m = []

messenger.email_message("Sample message", [os.path.join(os.curdir, 'README.md')])

try:
    m[0] = 1
except (Exception) as e:
    messenger.email_error("A handled exception occurred", e)

print("Test complete")