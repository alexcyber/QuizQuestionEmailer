'''

Creator: alpha
Date Created: 6.26.19

Purpose:  This application is designed to send a daily email that contains a Cisco test question
  to a list of email addresses.  Questions will be stored in a CSV with following sections:
  Question, A, B, C, D, E, correctAnswer, reason, url ending
  Emails will be stored in a csv as well with the following sections:
  email, name, correct answered, responded



main parts:
app: Interface to add, or remove a question.  Also can send out an email instantly
randomQuestion: returns one question from questionpool.csv, randomizes abcd answers
emailer: send username, password, sender, reciever(list),



Ideas:
- Question answers randomizer (yes)
- Select which topics to focus on (probably not gonna happen)
- Select type of test you are practicing on (probably not gonna happen)
- Packet tracer labs (nope)
- Contest an answer (yes)
- Email their answer back to get answer (nope, new route)
- link to answer? (the 'new route' mentioned above)
- Request a multiple questions a day (would like to implement)
- backup question pool (?)
- Statistics of usage (cool to have, probably gonna implement at the webserver level)

'''


import csv
import fileinput
import sys
from emailer import emailer
from updateWebsite import updateWebsite
from randomProblem import randomProblem
import re


# Creates and takes user input for Main Menu
def mainMenu():
    cont = True
    choices = ['e', 's', 'g', 'v', 'q']
    while cont:
        user_input =input("Enter one of the following: \n" +
                          "'e' to run emailing service to all users with a random question \n" +
                          "'s' to run email services to all users with a specific question \n" +
                          "'g' to generate an email within interface \n" +
                          "'v' to verify all html answers\n" +
                          "'q' to quit\n")
        for achoice in choices:
            if user_input == achoice:
                return user_input
        else:
            print('Not a valid answer, try again \n')


# sends an email to all emails in emailpool.csv
def sendEmail(cont, problemQ):
    emailList = [] # list for rEmailAddr in emailer()

    #adds emails from emailpool.csv to  emailList[]
    with open(conf['emailPool']) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        # selects the numbered question that was selected beforehand
        for row in csvReader:
            emailList.append(row[0])

    if conf['logging']:
        print("In app.sendEmail.  Made it to right before email call")

    url = problemQ.getURL()
    # sets randomQ to the string output of the file
    problemQ = str(problemQ)
    web = updateWebsite(conf['webpageFolderLocation'], url, problemQ)
    web.createHTMLPage(conf['webpageTemplate'], conf['motd'], conf['footnote'])

    email = emailer(conf['emailUsername'], conf['emailPassword'], conf['emailAddress'],
                    emailList, "Daily CCNA Question", problemQ, url, conf['websiteRootDirectory'], conf['logging'])

    if conf['logging']:
        print("In app.sendEmail.  Made it to right before emailer.sendEmail()")

    email.sendEmail()
    return cont

def generateProblem():
    print()
    randomQ = randomProblem(conf['questionPool'], 1, conf['logging'])
    return randomQ

def verifyHTMLanswers():
    problemList = []
    urlList = []
    problem = randomProblem(conf['questionPool'], 1, conf['logging'])
    for i in range(problem.file_len()):
        if i == 0:
            continue
        print(i)
        currentProblem = problem.returnProblem(i)
        currentProblem = str(problem)
        url = problem.getURL()
        web = updateWebsite(conf['webpageFolderLocation'], url, currentProblem)
        web.createHTMLPage(conf['webpageTemplate'], conf['motd'], conf['footnote'])
    return


#Loads config.txt files into a conf dictionary
def loadconfig():
    f = open("config.txt", "r")
    value = ""
    for line in f:
        # removes blank lines
        if not re.match(r'^\s*$', line):
            line = line.split("=")  # splits lines from config.txt from key to entry
            if line[0] in ['emailPool', 'questionPool',
                           'websiteRootDirectory', 'webpageFolderLocation', 'webpageTemplate', 'motd', 'footnote',
                           'emailUsername', 'emailPassword', 'emailAddress',
                           'logging', 'sequenceNumber']:
                conf[line[0]] = '='.join(line[1:]).strip()
            else:
                print(f"Warning: config file contained '{line[0]}' key.\n" +
                      "This is not a recognized key\n")

    # sets conf['logging'] to a boolean
    try:
        if conf['logging'] != "":
            conf['logging'] = eval(conf['logging'])
    except:
        print("no logging found")
    conf["sequenceNumber"] = int(conf["sequenceNumber"])
    f.close()

def editconfig(key, newEntry):
    for line in fileinput.input('config.txt', inplace=True):
        # Whatever is written to stdout or with print replaces
        # the current line
        if line.startswith(key):
            print(f'{key}={newEntry}')
        else:
            sys.stdout.write(line)


conf = {}
loadconfig()
