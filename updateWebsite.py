

'''
This class will update nginx files on a remote linux server to create weburls for answers.
init(self, url, username, publickey, rootWebDirectory, question)
    Question refers to toString of randomProblem or a formated string containing full question, and answer
example website page
    Question:
    You are working with an enterprise router connecting out to two Internet Service Providers (ISPs). The router has a single link to each ISP. What type of topology is described by this scenario?
    a. Single Multihomed
    b. Single Homed
    c. Dual Homed
    d. Dual Mulithomed
    Answer:
    a. Single Multihomed
First run through will create webpages at a local level to provide faster turnaround
    These html files will be stored in webpages folder for organization.  Two inits will be used for
    organization.
init(self, url
'''

import subprocess

class updateWebsite:

    #def __init__(self, url, username, publickey, rootWebDirectory, question):
    def __init__(self, folder, url, problem):
        self.url = url
        self.problem = problem
        self.folder = folder

    #creates html file for webpages/{url} using template at webpageTemplate.html
    def createHTMLPage(self, template):

        #check to see if HTML page is already created
        '''
        create html file at location webpages/*unique url*.  Overwrites if needed
            Uses template located at webpageTemplate.html and replaces:
                text "Question Here" with question and choices
                text "Answer Here" with answer and reason (if one)
        '''

        htmlAnswer = open(f"{self.folder}/{self.url}.html", 'w')
        htmlTemplate = open(template, "r")
        problemSplit = self.problem.split("\n")
        problemSplit.pop(0)
        for i,line in enumerate(problemSplit):
            try:
                if "Answer:" in problemSplit[i-1]:
                    boldAnswer = problemSplit[i].split()
                    boldAnswer.pop(0)
                    boldAnswer = ' '.join(boldAnswer)
                    boldAnswer = f"<b>{boldAnswer}</b>\n"
                    problemSplit[i] = boldAnswer
                else:
                    problemSplit[i] = "\n<br>" + line
            except IndexError:
                print("Expected error.  Please Ignore")
            except:
                print("Something went wrong splitting adding html tags to text")
        self.problem = ''.join(problemSplit)
        problemSplit = self.problem.split("Answer:")
        for line in htmlTemplate:
                if "{Question Here}" in line:
                    htmlAnswer.write(problemSplit[0])
                elif "{Answer Here}" in line:
                    try:
                        htmlAnswer.write(problemSplit[1])
                    except:
                        print("WARNING: No answer to this question")
                else:
                    htmlAnswer.write(line)

#    def upload(self, remoteHost, user, lFileLocation, rFileLocation, keyFileLocation):
#        keyFile = open(keyFileLocation, "r")
#        p = subprocess.Popen(["pscp", "-i",
#                              r"C:\Users\mmoli\.ssh\mailbotAmazon.ppk",
#                              "C:\\Users\\mmoli\\OneDrive\\Documents\\Programming Projects\\Python\\Projects\\Daily CCNA Question\webpages\\test.html",
#                              "ec2-user@ec2-18-219-217-61.us-east-2.compute.amazonaws.com:/home/ec2-user/mailbotAnswers/webpages/test.html"],
#                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#        print(p.communicate())