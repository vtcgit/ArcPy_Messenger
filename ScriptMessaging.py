__author__ = 'Brian Farrell'
__date_created__ = '1/17/14'


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import mimetypes
from email.message import Message
import sys
import os
import getpass
import traceback
import StringIO
from inspect import currentframe, getframeinfo

class Messenger:
    def __init__(self, username, password, application_name, recipients=[]):
        #set up email to/from information
        """
        This constructor sets the information needed to send an email and the computer information (neither of which
        should change during program execution).
        It also overrides the system exception handler to force it to send an email before handling the exception
        as normal.
        NOTE: overriding must be done in each thread of a threaded program.
        @param username: The username of the gmail account.
        @param password: The password of the gmail account.
        @param recipients: String list of email addresses to send to. Will send a copy to self.
        """
        self.fromaddr = username
        recipients.append(self.fromaddr)
        self.to = recipients
        self.uname = self.fromaddr
        self.pwd = password
        self.application_name = application_name

        #Store the computer and user name
        self.computername = os.environ['COMPUTERNAME']
        self.computeruser = getpass.getuser()

        self.__override_exception_handler()


    def __override_exception_handler(self):
        """
        This method sends an email when the script encounters an unexpected error. Then it returns control to the normal
        error handling exception.
        NOTE: This will not work in threaded programs.

        """

        def myexcepthook(exctype, value, tb):
            frame = tb
            while frame.tb_next is not None:
                frame = frame.tb_next
            msg = self.__build_message("An unhandled exception occurred", etype=exctype, evalue=value, etb=tb, stackframe=frame)
            self.__send_email(msg)
            sys.__excepthook__(exctype, value, traceback)
        sys.excepthook = myexcepthook


    def __build_message(self, message, exception=None, etype=None, evalue=None, etb=None, stackframe=None):
        """

        @param message: A human friendly message that you want emailed.
        @param exception: The exception object relevant to this message.
        @param etype: The type of the exception.
        @param evalue: The value of the exception.
        @param etb: The exception traceback object.
        @param stackframe: The stackframe from where you should get line number and file names.
        @return: A MIMEMultipart, with a plain text body, ready for attachements.
        """
        #Collect exception information
        if exception:
            etype, evalue, etb = sys.exc_info()
        output = StringIO.StringIO()
        traceback.print_exception(etype, evalue, etb, file=output)

        #Collect the line number and file name where this method was called
        lineno = "Unknown"
        filename = "Unknown"
        if stackframe is not None:
            lineno = getframeinfo(stackframe).lineno
            filepath = getframeinfo(stackframe).filename.split('/')
            filename = filepath[len(filepath) - 1]

        body_text = "\r\n".join([
            message,
            "File: " + filename,
            "Line: " + str(lineno),
            "Computer Name: " + self.computername,
            "Computer User: " + self.computeruser,
            "Error Information: " + output.getvalue()
            ])

        msg = MIMEMultipart()
        msg['Subject'] = "[" + self.application_name + "] Python Script Message"

        body = MIMEMultipart('alternative')
        body_content = MIMEText(body_text, 'plain')
        body.attach(body_content)
        msg.attach(body)
        return msg

    def __send_email(self, msg):
        """

        @param msg: The message to be put in the body of the email.
        """
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.uname,self.pwd)
        composed = msg.as_string()
        server.sendmail(self.fromaddr, self.to, composed)
        server.quit()

    @staticmethod
    def __add_attachments(msg, attachments):
        """

        @param message: The MIMEMultipart message.
        @param attachments: A list of strings; the filepaths to all email attachments.
        """
        for attachment_path in attachments:
            ctype, encoding = mimetypes.guess_type(attachment_path)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(attachment_path)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(attachment_path, 'rb')
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(attachment_path, 'rb')
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(attachment_path, 'rb')
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(attachment)

            head, tail = os.path.split(attachment_path)
            attachment.add_header('Content-Disposition', 'attachment', filename=tail)
            msg.attach(attachment)

    def email_error(self, message, exception, attachments=None):
        """

        @param message: The message to be put in the body of the email.
        @param exception: The exception object (if none, use email_message).
        """
        msg = self.__build_message(message, exception=exception, stackframe=currentframe().f_back)
        if(attachments):
            self.__add_attachments(msg, attachments)
        self.__send_email(msg)

    def email_message(self, message, attachments=None):
        """

        @param message: The message to be put in the body of the email.
        @param attachments: A list of strings; the filepaths to all email attachments.
        """
        msg = self.__build_message(message, stackframe=currentframe().f_back)
        if(attachments):
            self.__add_attachments(msg, attachments)
        self.__send_email(msg)