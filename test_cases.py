__author__ = 'Brian Farrell'
__date_created__ = '1/30/14'

import __credentials, ScriptMessaging
import os

messenger = ScriptMessaging.Messenger(__credentials.username, __credentials.password, "Test Case", __credentials.recipients)

# Test Handled Exception
m = []

# messenger.email_message("Sample message, no attachments")
messenger.email_message("Please find attached the vineyards site report you requested on 03/11/2015 from the Grape & Wine Quality, Eastern U.S. Initiative website.\n\nIf you have any issues with the report, please send an email to cgitsupport@listserv.vt.edu.\n\nSincerely,\nCGIT", "Vineyards Site Report", [os.path.join(os.curdir, 'SamplePDF.pdf')])

# try:
#     m[0] = 1
# except (Exception) as e:
#     messenger.email_error("Sample handled error, no attachments", e)
#
# try:
#     m[0] = 1
# except (Exception) as e:
#     messenger.email_error("Sample handled error, with attachments", e, [os.path.join(os.curdir, 'SamplePDF.pdf')])

print("Test complete")