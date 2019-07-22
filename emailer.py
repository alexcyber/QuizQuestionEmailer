# emailer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

'''
Creates an emailer class that can be used to send an email. 
'''
class emailer:

    def __init__(self, username, password, sEmailAddr, rEmailAddr, subject, body, url, logging):
        self.username = username
        self.password = password
        self.sEmailAddr = sEmailAddr
        self.rEmailAddr = rEmailAddr
        self.logging = logging

        if self.logging:
            print("In emailer.__init__().  Before MIMEMultipart()")

        #creates email
        msg = MIMEMultipart()
        msg['From'] = sEmailAddr
        msg['Subject'] = subject

        '''
        Code added for website plugin
        '''
        questionAnswerSplit = body.split('Answer')
        questionAnswerSplit[0] = questionAnswerSplit[0] + "\nFor the answer and (if available) explanation, visit:\n" + \
                     f"http://www.alexcyber.com/answers/{url}.html"

        questionAnswerSplit[0] = questionAnswerSplit[0] + "\n\nFor support, send an email to alex@alexcyber.com"
        msg.attach(MIMEText(questionAnswerSplit[0],'plain'))
        #msg.attach(MIMEText(body, 'plain'))
        self.email = msg.as_string()

        if logging:
            print("In emailer.__init__().  Finished __init__")


    def sendEmail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
        except:
            print('Something went wrong with connecting to mail server...')
        #Next, log in to the server
        server.login(self.username, self.password)  # jbsycbipzoochgrl
        server.sendmail(self.sEmailAddr, self.rEmailAddr, self.email)
        server.quit()



