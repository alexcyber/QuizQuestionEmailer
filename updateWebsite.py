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

class updateWebsite:

    def __init__(self, folder, url, problem):
        self.url = url
        self.problem = problem
        self.folder = folder

    #creates html file for webpages/{url} using template at webpageTemplate.html
    def createHTMLPage(self, template, motd, footnote):

        #check to see if HTML page is already created
        '''
        create html file at location webpages/*unique url*.  Overwrites if needed
            Uses template specified in config.txt and replaces:
                text {MOTD Here} with motd from config (html encoded)
                text {Question Here} with question and choices from config.txt[questionPool]
                text {Answer Here} with answer and reason (if one) from config.txt[questionPool]
                text {Footnote Here} with footnote from config (html encoded)
        '''

        htmlAnswer = open(f"{self.folder}/{self.url}.html", 'w')
        htmlTemplate = open(template, "r")
        problemSplit = self.problem.split("\n")
        problemSplit.pop(0)
        for i,line in enumerate(problemSplit):
            try:
                if "Answer:" in problemSplit[i-1]:
                    boldAnswer = problemSplit[i].split()
                    #boldAnswer.pop(0)  Unknown reason why I put this here.  Leaving for now
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

        #using the template, creates html page filling in the MOTD, question, answer, footnote
        for line in htmlTemplate:
                if "{MOTD Here}" in line:
                    htmlAnswer.write(motd)
                elif "{Question Here}" in line:
                    htmlAnswer.write(problemSplit[0])
                elif "{Answer Here}" in line:
                    try:
                        htmlAnswer.write(problemSplit[1])
                    except:
                        print("WARNING: No answer to this question")
                elif "{Footnote Here}" in line:
                    htmlAnswer.write(footnote)
                else:
                    htmlAnswer.write(line)
