__author__ = 'Brian Farrell'
__date_created__ = '1/30/14'

import __credentials, ScriptMessaging
import os

messenger = ScriptMessaging.Messenger(__credentials.username, __credentials.password, "Test Case", __credentials.recipients)

# Test Handled Exception
m = []

messenger.email_message("Sample message, no attachments")
messenger.email_message("Sample message, with attachments", [os.path.join(os.curdir, 'README.md')])

try:
    m[0] = 1
except (Exception) as e:
    messenger.email_error("Sample handled error, no attachments", e)

try:
    m[0] = 1
except (Exception) as e:
    messenger.email_error("Sample handled error, with attachments", e, [os.path.join(os.curdir, 'README.md')])

print("Test complete")