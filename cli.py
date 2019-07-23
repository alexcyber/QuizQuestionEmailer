
import app
from randomProblem import randomProblem

cont = True
while cont:
    uInput = app.mainMenu()
    if uInput == 'e':
        problemQ = app.generateProblem()  # gets a random problem selected and written
        cont = app.sendEmail(cont, problemQ)
        print('sent')
    if uInput == 's':
        problemQ = randomProblem(app.conf['questionPool'], 1, app.conf['logging'])
        userInput = int(input("What is the question number you would like to send? "))
        problemQ.returnProblem(userInput)
        cont = app.sendEmail(cont, problemQ)
        print('sent')
    if uInput == 'g':
        question = app.generateProblem()
        print(question)
    if uInput == 'v':
        app.verifyHTMLanswers()
    if uInput == 'q':
        cont = False
    print('')