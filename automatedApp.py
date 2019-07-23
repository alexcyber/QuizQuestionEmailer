#!/usr/bin/python36
'''
This python script is used to automate sending out an email and creating a corresponding answer html webpage.

Select this script when running from a task scheduler like cron
'''


import app
from randomProblem import randomProblem
from datetime import datetime
from pytz import timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def sendEmail(emailTxt):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
    except:
        print('Something went wrong with connecting to mail server...')
    # Next, log in to the server
    server.login(app.conf['emailUsername'], app.conf['emailPassword'])
    server.sendmail(app.conf['emailAddress'], app.conf['emailAddress'], emailTxt)
    server.quit()

try:
    cont = True

    # define date format
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # define eastern timezone
    eastern = timezone('US/Eastern')
    # naive datetime
    naive_dt = datetime.now()
    # localized datetime
    loc_dt = datetime.now(eastern)

    #Creates randomProblem Object
    problemQ = randomProblem(app.conf['questionPool'], 1, app.conf['logging'])
    currentProblemNum = app.conf["sequenceNumber"]  # pulls sequence number from config.txt
    problemQ.returnProblem(currentProblemNum)  # rewrites problem object
    try:
        cont = app.sendEmail(cont, problemQ)
        app.editconfig("sequenceNumber", currentProblemNum + 1)  # sequence number goes up one

    # if no errors, sends email, sequenceNum++ in config, and printing to log that an email was sent
    except IndexError:
        sendEmail("Daily CCNA Question failed. \n  Ran out of problems to send (IndexError)")
        print(f'{naive_dt.strftime(fmt)}\tRan out of problems to send (IndexError).')
        print(f'{naive_dt.strftime(fmt)}\tSent email to {app.conf["emailAddress"]}\n')
        cont = False
    else:
        # print datestamp if all succeeded
        print(f'{naive_dt.strftime(fmt)}\t Sent email\n')
except Exception as e:
    sendEmail("Daily CCNA Question failed.\n  General failure")
    print(f'{naive_dt.strftime(fmt)}\tRan out of problems to send (IndexError).  Sent Email')
    print(f'{naive_dt.strftime(fmt)}\t{e} \n')

