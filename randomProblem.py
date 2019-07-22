'''
Creates a random problem object contains the question, randomized choices, and the correct answer
'''

# randomProblem
import csv
import random

class randomProblem:

    #sets filename to csv file located witin folder, start value to account for headers, and if logging is enabled
    def __init__(self, fileName, startvalue, logging):
        self.fileName = fileName
        self.startvalue = startvalue
        self.logging = logging
        self.problem = self.generate()
    '''
    EX:
    Question: 
    You are working with an enterprise router connecting out to two Internet Service Providers (ISPs). The router has a single link to each ISP. What type of topology is described by this scenario?
    a. Single Multihomed
    b. Single Homed
    c. Dual Homed
    d. Dual Mulithomed

    Answer: 
    a. Single Multihomed
    '''
    def __str__(self):
        letter = ['a', 'b', 'c', 'd', 'e'] #letters used to set choice answers
        # format is used as a the concat string that is returned
        format = f'Question: \n'
        # formats question portion
        for line in self.problem[0]:
            format = format + f'{line} \n'
        format = format + "\n"

        #formats choices portion
        for i,choice in enumerate(self.problem[1]):
            format = format + f" {letter[i]}. {choice}\n"
            if choice == self.problem[2]:
                self.problem[2] = f'  {letter[i]}. {self.problem[2]}\n'  # sets answer to include correct letter


        #if there is an answer, add answer clause to toString
        if not self.problem[2] == -1:
            format = format + f'\nAnswer: \n Penis{self.problem[2]}'

        if self.problem[3][0] != "":
            format = format + "\n\nReason: \n"
            for line in self.problem[3]:
                format = format + f'{line} \n'

        return format

    #returns the url portion of the problem specifically
    def getURL(self):
        return self.problem[4]


    # returns len(file)
    def file_len(self):
        with open(self.fileName) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


    # returns a single problem with radomized choices.  returns problem
    def returnProblem(self, number):
        question = []
        choices = []
        answer = -1
        reason = []
        questionsList = []
        url = ""

        if self.logging:
            print(f"In Random Problem.returnProblem(), before opening {self.fileName}")

        with open('questionpool.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            questionsList.extend(csvReader)
        csvDataFile.close()
        # opens CSV file
        with open('questionpool.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            # selects the numbered question that was selected beforehand

            if self.logging:
                print(f"In RandomProblem.returnProblem(), after initial opening of {self.fileName}, before for loop")
                print(f"CSVREADER DATA:\n{csvReader}")

            for i,row in enumerate(csvReader, start=-1):
                # when selected, fills out all lists stated in beginning

                if i == number - 1:
                    if self.logging:
                        print(f"In RandomProblem.returnProblem(), row has been selected")
                        print(i)
                        print(row)
                    # Verifies there is a number in answer slot, sets variable if true, otherwise, left -1
                    if row[6] != "":
                        answer = int(row[6])
                    question = row[0].split("\\\\")
                    for j in range(len(row)):
                        if 0 < j < 6:
                            if not row[j] == '':
                                choices.append(row[j])  # adds nonrandom choices
                            if answer == j:
                                answer = str(row[j])  # sets answer
                    random.shuffle(choices)  # after answer as been set, randomizes the choices

                    reason = row[7].split("\\\\")

                    if self.logging:
                        print('Returned questions details from randomQuestion.randomProblem(...)')
                        for i,choice in enumerate(choices):
                            print(f'choice {i+1}: {choice}')
                        print(f'answer: {answer}\n')

                    #sets var url to url of csv.  Creates a random string if needed
                    if row[8] == "":
                        url = random.randint(10000,100000)
                    else:
                        url = row[8]
                    questionsList[number][8] = url
                    if self.logging:
                        print('Before break in randomProble.returnProblem()')
                    # break
        csvDataFile.close()

        #adds url to problem
        with open('questionpool.csv', 'w', newline='') as csvDataFile:
            csvWriter = csv.writer(csvDataFile)
            csvWriter.writerows(questionsList)
        csvDataFile.close()
        self.problem = [question, choices, answer, reason, url]
        return [question, choices, answer, reason, url]


    def generate(self):
        fileLength = self.file_len()
        questionNumber = random.randint(self.startvalue, fileLength - 1)
        if self.logging:
            print(f"In randomQuestion.generate(...) \n" +
                  f"startvalue = {self.startvalue} \n" +
                  f"filelength = {fileLength} \n" +
                  f"Question Number = {questionNumber} \n")
        return self.returnProblem(questionNumber)
