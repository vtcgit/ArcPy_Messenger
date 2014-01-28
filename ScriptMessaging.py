__author__ = 'Brian Farrell'
__date_created__ = '1/17/14'


import smtplib
import sys
import os
import getpass
import traceback
import StringIO
from inspect import currentframe, getframeinfo

class Messenger:
    def __init__(self, username, password):
        #set up email to/from information
        """
        This constructor sets the information needed to send an email and the computer information (neither of which
        should change during program execution).
        It also overrides the system exception handler to force it to send an email before handling the exception
        as normal.
        NOTE: overriding must be done in each thread of a threaded program.
        @param username: The username of the gmail account.
        @param password: The password of the gmail account.
        """
        self.fromaddr = username
        self.to = self.fromaddr
        self.uname = self.fromaddr
        self.pwd = password

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
        @return: A string message, intended to go in the body of an email.
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

        msg = "\r\n".join([
            "Subject: Python Script Message",
            message,
            "File: " + filename,
            "Line: " + str(lineno),
            "Computer Name: " + self.computername,
            "Computer User: " + self.computeruser,
            "Error Information: " + output.getvalue()
            ])
        return msg

    def __send_email(self, msg):
        """

        @param msg: The message to be put in the body of the email.
        """
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.uname,self.pwd)
        server.sendmail(self.fromaddr, self.to, msg)
        server.quit()

    def email_error(self, message, exception):
        """

        @param message: The message to be put in the body of the email.
        @param exception: The exception object (if none, use email_message).
        """
        msg = self.__build_message(message, exception=exception, stackframe=currentframe().f_back)
        self.__send_email(msg)

    def email_message(self, message):
        """

        @param message: The message to be put in the body of the email.
        """
        msg = self.__build_message(message, stackframe=currentframe().f_back)
        self.__send_email(msg)