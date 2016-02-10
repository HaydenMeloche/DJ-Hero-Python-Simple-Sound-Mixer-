#*******************************************************************************************************************
import pygame, sys
from pygame.locals import *
from time import sleep #used for delay
from os import path #used for checking if a file exists
from random import shuffle #used for shuffling file
# set up pygame
pygame.init()
# set up the window
windowSurface = pygame.display.set_mode((1000, 750), 0, 32)
pygame.display.set_caption('Teacher Quiz')
img = pygame.image.load('quiz_back.bmp')
# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE2 = (75, 100, 255)
RED1 = (255, 75, 75)

col1 = BLUE
col2 = BLUE
col3 = BLUE
col4 = BLUE
col5 = BLUE
col6 = BLUE
col7 = RED

a = 2
b = 2
c = 2

FontA=pygame.font.SysFont("Times New Roman",75)
FontB=pygame.font.SysFont("Times New Roman",30)

tutorial_image1 = pygame.image.load('Tutorial 1.bmp')
tutorial_image2 = pygame.image.load('Tutorial 2.bmp')
tutorial_image3 = pygame.image.load('Tutorial 3.bmp')
tutorial_image4 = pygame.image.load('Tutorial 4.bmp')
tutorial_image5 = pygame.image.load('Tutorial 5.bmp')


#----------------Initialization and imports end and functions start below----------
def ExportQuiz (fileName,multiList): #takes a 2d array and outputs it into a txt file
  file = open(fileName + ".txt","w")
  file.write(str(multiList[0][0])+ ",")
  file.write(str(multiList[0][1])+",")
  file.write(str(multiList[0][2])+"\n")
  for i in range (1,multiList[0][0]+1):
    file.write ("~\n")
    for j in range (0,5):
      file.write("*"+multiList[i][j]+"\n")
    file.write(str(multiList[i][5])+"\n")
  file.write ("~\n")
  file.close()

def ShuffleFile (fileName): #imports a text file shuffles its contents then saves it as a new file
  f = open(fileName) #opens the text file
  lines = f.readlines() #reads in the text file line by line
  f.close() #closes text file

  amountQuestions =int((lines[0][0]))#amount of question in the txt file
  order = [[i] for i in range(amountQuestions)] #creates list from 0 to the amount of questions minus 1
  order = [int(i[0]) for i in order] #changes all the values from string to integer
  shuffle(order) #shuffles the order. Now this is the new shuffled order of the questions
  fourRange = [[i] for i in range(4)] #creates a list from one to 3
  fourRange = [int(i[0]) for i in fourRange] #changes the list from string to integer

  newLines = [0 for i in range(len(lines))] #creates a new list that will be added to

  newLines[0] = lines[0]
  for i in range(0,amountQuestions): #for each of the questions
    shuffle(fourRange) #shuffles the order of the answers. ex: a,b,c,d might become b,d,c,a
    newLines[i*7+1] = "~\n"
    newLines[i*7+2] = lines[order[i]*7+2] #outputs the question
    newCorrect = int(lines[order[i]*7+7])-1 #inputs the correct answer
    for y in range(0,4):
      newLines[i*7+3+y] = lines[fourRange[y]+order[i]*7+3] #outputs shuffled answers

    for y in range(0,4):
      if (newCorrect == fourRange[y]): #checks to see what is the new correct answer
        newLines[i*7+7] = str(y+1)+"\n" #outputs it
  newLines[-1] = "~\n"
  with open(fileName[:-4] + "Shuffled.txt", 'w') as f: ################change to make new file with shuffled name
    f.writelines(newLines)

def FileCheck (fileName): #check if a file is correct for import
  if not path.exists(fileName): #check if the file exists
    return "File does not exist, remember there has to be a .txt at the end"

  tempQuizFile = open(fileName) #opens the text file
  lines = tempQuizFile.readlines() #reads in the text file into a list called 'lines'
  tempQuizFile.close() #close the file now that all the info is stored
  if not lines[0][0].isdigit(): #check if the first character on the first line is a number
    return "First character on line one must be a number"
  if not lines[0][2].isdigit(): #check if the second character on the first line is a number
    return "Second character on line one must be a number"
  if not lines[0][4:-1].isdigit(): #check if the third character on the first line is a number
    return "Third character on line one must be a number"
  amountQuestions = int((lines[0][0])) #reads in first number in the text file that is the amount of questions
  correctAmountLines = (amountQuestions-1)*7+9 #formula for calculating how many lines based on how many questions
  if len(lines) > correctAmountLines: #checks if there is too many lines
    return "Too many lines in the file"
  elif len(lines) < correctAmountLines: #checks if there is too few lines
    return "Too few lines in the file"

  for i in range (0,amountQuestions): #for every question
    if not ( (lines[i*7+1])[0] == "~" ): #format check
      return "Error first character on line " + str(i*7+2) + " should be a '~'"
    for j in range (0,5): #format check
      if not ( (lines[i*7+2+j])[0] == "*" ):
        return "Error first character on line " + str(i*7+3+j) + " should be a '*'"

    if not ((lines[i*7+7])[0].isdigit() ): #checks to make sure that there is a number value for the anwser for every question
      return "Error on line " + str(i*7+8) + " should be a number"

  return "" #no errors in the file

def keyboardInput(xvar,yvar): #gets keyboard input until and displays it until user presses enter
    totalMessage = "" #all the keys that the user pressed that will later returned
    while True: #infinite loop, exits loop when user hits enter
        for event in pygame.event.get():
            if event.type == KEYDOWN: #if a key is being pressed
                currentKey = event.key #save what key is being pressed to currentKey
                if currentKey == 13: #if the current key is the 'enter key'
                    return totalMessage #exit the loop and return all the keys the user has typed
                else: #if the current key is not the enter key
                    otherKeys = pygame.key.get_pressed() #stores all the other keys , ex: the shift keys
                    if currentKey == 8: #delete key
                        TextC=FontB.render(totalMessage,1,BLUE) #write over the white text with blue to erase
                        windowSurface.blit(TextC,(xvar,yvar))
                        pygame.display.update()
                        totalMessage = totalMessage[:-1] #erase last character
                    else:
                        if not (currentKey == 304 or currentKey == 303): #if the last key pressed is an actual character
                            if otherKeys[K_LSHIFT] or otherKeys[K_RSHIFT]: #if a shift key is pressed
                                currentKey -= 32 #change it from lower-case to capital letter
                            if currentKey <= 256: #fixes crash with keys such as windows button
                                totalMessage += chr(currentKey) #add the latest key to the whole message
                    TextC=FontB.render(totalMessage,1,WHITE) #writes the text the user has typed to the screen
                    windowSurface.blit(TextC,(xvar,yvar))
                    pygame.display.update()

def numberKeyboardInput(xvar,yvar): #equivalent to input() but with pygame
    while True: #infinite loop until the user types in a valid number
        userNum = keyboardInput(xvar,yvar) #get user input
        try:
            int(userNum) #see if the user's input is a number
            return int(userNum) #if yes return the number
        except ValueError:
            pygame.draw.rect(windowSurface, BLUE, (100,200,800,200))
            TextC=FontB.render("Error must be a number",1,WHITE) #writes error to the screen
            windowSurface.blit(TextC,(xvar,yvar))
            pygame.display.update()
            sleep(1) #delay for user to read
            pygame.draw.rect(windowSurface, BLUE, (100,200,800,200))#draws square over error text
            pygame.display.update()

def allAnwsered(multiArray,amount_of_questions_on_quiz): #checks for done button if all of the questions have an answer to them
    for i in range(1,amount_of_questions_on_quiz+1): #for every question
        if multiArray[i][5] == 0: #if the question doesn't have an answer
            return False
    return True #all the questions have an answer to them

def inputFile (fileName): #inputs from a text file to a multi-dimensional array
  file = open(fileName) #opens the txt file with the name passed to the function
  lines = file.readlines() #reads the file line by line and stores it in a list
  numQuestions = int((lines[0][0])) #determines the number of question by using the first line of the text file
  QuestionsData = [[0 for x in xrange(6)]for x in xrange(numQuestions+1)] #initialize list that will later be returned to user
  QuestionsData[0][0] = numQuestions #set the first value in the list to the number of questions
  file.close()

  for i in range(1,numQuestions+1): #for every question
    for j in range(0,5): # retrieve 5 pieces of info: The question, 4 different possible anwsers, and the correct anwser
      QuestionsData[i][j]= (lines[(i-1)*7+2+j])[1:-1] #put the questions and the 4 different possible anwsers into the list
    QuestionsData[i][5]= int(lines[(i-1)*7+3+4]) #put the correct anwser in as an integer
  return QuestionsData #end function return multidimensional list

def filenamePromtMenu(): #a menu that returns a valid file-name
    windowSurface.blit(img,(0,0))
    TextB=FontB.render("Please type the file name",1,BLUE)
    pygame.draw.rect(windowSurface, BLUE, (100,200,800,200))
    windowSurface.blit(TextB,(35,75))
    pygame.display.update()

    user_file_name = keyboardInput(200,200) #gets a file name from the user

    while True: #infinite loop until user has selected a valid file
        errorCode = FileCheck(user_file_name) #runs the code that checks for error and stores the first error it finds in errorCode
        if not errorCode == "": #if there is an error
            windowSurface.blit(img,(0,0))
            pygame.display.update()
            sleep(0.25) #adds slight delay before shows error, show user that the program has run.
            TextB=FontB.render("Error occurred with the file-name '" + user_file_name +  "'",1,RED) #outputs error code
            pygame.draw.rect(windowSurface, BLUE, (100,200,800,200))
            windowSurface.blit(TextB,(35,75))
            TextB=FontB.render(errorCode,1,RED)
            windowSurface.blit(TextB,(35,115))
            pygame.display.update()
            user_file_name = keyboardInput(200,200)
        else:
             return user_file_name #if it is a valid file-name return the file

def create_edit_teacher (quizFile): #both the create and edit buttons on the teachers main screen
    col0 = BLUE
    col1 = BLUE
    col2 = BLUE
    col3 = BLUE
    col4 = BLUE
    SlideNumber = 1
    b = 2
    a = 2
    c = 2

    windowSurface.blit(img,(0,0))
    pygame.draw.rect(windowSurface, BLUE, (100,200,800,200))
    TextA=FontB.render('How Many Questions Do You Want',1,BLUE)
    windowSurface.blit(TextA,(100,150))
    TextD=FontB.render('Click',1,WHITE)
    windowSurface.blit(TextD,(300,200))
    pygame.display.update()

    if quizFile == "": #if there was no file-name passed to the function, aka create mode
        while c == 2:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                        if mx > 99 and mx < 901 and my > 199 and my < 401:
                            pygame.draw.rect(windowSurface, BLUE, (100,200,800,200))
                            pygame.display.update()
                            amount_of_slides = numberKeyboardInput(200,200)
                            c = 1
        MainQuiz = [[0 for x in xrange(6)]for x in xrange(amount_of_slides+1)]
        MainQuiz[0][0] = amount_of_slides
        ######################################MAIN TEACHER QUESTIONS###########################################################################
        for i in range(1,amount_of_slides+1): #for every question
            MainQuiz[i][0] = "Write" #set the question for every question to "write" by default
            for j in range(1,5):
                MainQuiz[i][j] = "" #set all the possible answers to nothing by default

    else: #there was a file-name passed to the program, aka edit mode
        MainQuiz = inputFile(quizFile) #input the information from the file name given
        amount_of_slides = MainQuiz [0][0] #stores the amount of questions

    def graphics (): #the main graphics for the teacher edit and create
        windowSurface.fill(BLACK)
        windowSurface.blit(img,(0,0))
        pygame.draw.line(windowSurface, BLACK, (60, 60), (120, 60), 4)
        pygame.draw.rect(windowSurface, col0, (25,50,950,100))
        pygame.draw.rect(windowSurface, col1, (200,175,650,100))
        pygame.draw.rect(windowSurface, col2, (200,300,650,100))
        pygame.draw.rect(windowSurface, col3, (200,425,650,100))
        pygame.draw.rect(windowSurface, col4, (200,550,650,100))

        if MainQuiz[SlideNumber][5] == 1: #decision structure to select which answer to draw the selected green box around
            pygame.draw.rect (windowSurface, GREEN,(50,660,65,70))
        elif MainQuiz[SlideNumber][5] == 2:
            pygame.draw.rect (windowSurface, GREEN,(200,660,65,70))
        elif MainQuiz[SlideNumber][5] == 3:
            pygame.draw.rect (windowSurface, GREEN,(350,660,65,70))
        elif MainQuiz[SlideNumber][5] == 4:
            pygame.draw.rect (windowSurface, GREEN,(500,660,65,70))

        TextA=FontA.render('a',1,BLUE)
        windowSurface.blit(TextA,(160,178))

        TextA=FontA.render('b',1,BLUE)
        windowSurface.blit(TextA,(160,303))

        TextA=FontA.render('c',1,BLUE)
        windowSurface.blit(TextA,(160,428))

        TextA=FontA.render('d',1,BLUE)
        windowSurface.blit(TextA,(160,553))

        TextA=FontA.render('A',1,BLUE)
        windowSurface.blit(TextA,(50,650))

        TextA=FontA.render('B',1,BLUE)
        windowSurface.blit(TextA,(200,650))

        TextA=FontA.render('C',1,BLUE)
        windowSurface.blit(TextA,(350,650))

        TextA=FontA.render('D',1,BLUE)
        windowSurface.blit(TextA,(500,650))

        TextB=FontB.render('Answer for Question',1,BLUE)
        windowSurface.blit(TextB,(650,660))

        TextB=FontB.render(MainQuiz[SlideNumber][0],1,WHITE) #question
        windowSurface.blit(TextB,(35,75))

        TextB=FontB.render(MainQuiz[SlideNumber][1],1,WHITE) #answer a
        windowSurface.blit(TextB,(215,200))

        TextB = FontB.render(MainQuiz[SlideNumber][2],1,WHITE) #answer b
        windowSurface.blit(TextB,(215,325))

        TextB=FontB.render(MainQuiz[SlideNumber][3],1,WHITE) #answer c
        windowSurface.blit(TextB,(215,450))

        TextB=FontB.render(MainQuiz[SlideNumber][4],1,WHITE) #answer d
        windowSurface.blit(TextB,(215,575))

        if SlideNumber < amount_of_slides: #if it isn't the last slide then draw the forward arrow
            pygame.draw.rect(windowSurface, BLUE, (875,365, 75,75))
            pygame.draw.lines(windowSurface, BLUE, False, [(950,440), (999,402), (950,365)], 30)
            pygame.draw.rect(windowSurface, BLUE, (950,380, 40,46))
        if SlideNumber != 1: #if it isn't the first slide then draw the back arrow
            pygame.draw.rect(windowSurface, BLUE, (50,365, 75,75))
            pygame.draw.lines(windowSurface, BLUE, False, [(50,440), (1,402), (50,365)], 30)
            pygame.draw.rect(windowSurface, BLUE, (10,380, 40,46))
        if SlideNumber == amount_of_slides and allAnwsered(MainQuiz,amount_of_slides): #if it is the last slide and all questions have an anwser add the done option
            pygame.draw.rect (windowSurface, GREEN, (900,700,90,30))
            TextA=FontB.render('DONE',1,BLUE)
            windowSurface.blit(TextA,(900,700))

        pygame.display.update()

    while 2==a:
        b=2
        graphics ()
        while b==2:
            for event in pygame.event.get():
                mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                if mx > 24 and my >49 and mx < 976 and my < 151:
                    col0 = BLUE2
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE
                    graphics ()
                elif mx > 199 and my >174 and mx < 851 and my < 276:
                    col0 = BLUE
                    col1 = BLUE2
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE
                    graphics ()
                elif mx > 199 and my >299 and mx < 851 and my < 401:
                    col0 = BLUE
                    col1 = BLUE
                    col2 = BLUE2
                    col3 = BLUE
                    col4 = BLUE
                    graphics ()
                elif mx > 199 and my >424 and mx < 851 and my < 526:
                    col0 = BLUE
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE2
                    col4 = BLUE
                    graphics ()
                elif mx > 199 and my >549 and mx < 851 and my < 651:
                    col0 = BLUE
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE2
                    graphics ()
                else:
                    col0 = BLUE
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE
                    graphics ()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                        if mx > 24 and my >49 and mx < 976 and my < 151:
                            pygame.draw.rect(windowSurface, BLUE, (25,50,950,100))
                            pygame.display.update()
                            MainQuiz[SlideNumber][0] = keyboardInput(35,75)
                            graphics ()
                            #Question
                        elif mx > 199 and my >174 and mx < 851 and my < 276:
                            pygame.draw.rect(windowSurface, BLUE, (200,175,650,100))
                            pygame.display.update()
                            MainQuiz[SlideNumber][1] = keyboardInput(215,200)
                            graphics ()
                            #A
                        elif mx > 199 and my >299 and mx < 851 and my < 401:
                            pygame.draw.rect(windowSurface, BLUE, (200,300,650,100))
                            pygame.display.update()
                            MainQuiz[SlideNumber][2] = keyboardInput(215,325)
                            graphics ()
                            #B
                        elif mx > 199 and my >424 and mx < 851 and my < 526:
                            pygame.draw.rect(windowSurface, BLUE, (200,425,650,100))
                            pygame.display.update()
                            MainQuiz[SlideNumber][3] = keyboardInput(215,450)
                            graphics ()
                            #C
                        elif mx > 199 and my >549 and mx < 851 and my < 651:
                            pygame.draw.rect(windowSurface, BLUE, (200,550,650,100))
                            pygame.display.update()
                            MainQuiz[SlideNumber][4] = keyboardInput(215,575)
                            graphics ()
                            #D
                        elif mx > 0 and my >364 and mx < 126 and my < 441:
                            b = 1
                            if SlideNumber > 1:
                                SlideNumber = SlideNumber - 1
                                pygame.draw.rect(windowSurface, GREEN, (50,365, 75,75))
                                pygame.draw.lines(windowSurface, GREEN, False, [(50,440), (1,402), (50,365)], 30)
                                pygame.draw.rect(windowSurface, GREEN, (10,380, 40,46))

                        elif mx > 874 and my >364 and mx < 1000 and my < 441:
                            b = 1
                            if SlideNumber < amount_of_slides:
                                SlideNumber = SlideNumber + 1
                                pygame.draw.rect(windowSurface, GREEN, (875,365, 75,75))
                                pygame.draw.lines(windowSurface, GREEN, False, [(950,440), (999,402), (950,365)], 30)
                                pygame.draw.rect(windowSurface, GREEN, (950,380, 40,46))

                        elif mx > 49 and mx < 126 and my > 649 and my < 751:
                            MainQuiz[SlideNumber][5] = 1
                            graphics ()
                        elif mx > 199 and mx < 276 and my > 649 and my < 751:
                            MainQuiz[SlideNumber][5] = 2
                            graphics ()
                        elif mx > 349 and mx < 426 and my > 649 and my < 751:
                            MainQuiz[SlideNumber][5] = 3
                            graphics ()
                        elif mx > 499 and mx < 576 and my > 649 and my < 751:
                            MainQuiz[SlideNumber][5] = 4
                            graphics ()
                        elif mx > 899 and mx < 991 and my > 699 and my < 731:
                            if SlideNumber == amount_of_slides and allAnwsered(MainQuiz,amount_of_slides): #done button
                                if quizFile != "":
                                    ExportQuiz(quizFile[:-4],MainQuiz)
                                    a = 1
                                    b = 1
                                elif quizFile == "":
                                    windowSurface.blit(img,(0,0))
                                    TextA=FontB.render('Please click then write the file-name',1,BLUE)
                                    pygame.draw.rect(windowSurface, BLUE, (200,300,600,100))
                                    windowSurface.blit(TextA,(100,200))
                                    pygame.display.update()
                                    file_saving = keyboardInput(200,325)
                                    ExportQuiz(file_saving,MainQuiz)
                                    a = 1
                                    b = 1
                        else:
                            col0 = BLUE
                            col1 = BLUE
                            col2 = BLUE
                            col3 = BLUE
                            col4 = BLUE

                    pygame.display.update()

def student_quiz (): #the student quiz that runs when the student client is chosen
    col1 = BLUE
    col2 = BLUE
    col3 = BLUE
    col4 = BLUE
    answer_quiz = [] #holds user answers
    SlideNumber = 1
    b = 2
    a = 2

    user_file_name = filenamePromtMenu()
    MainQuiz = inputFile (user_file_name)

    for counter in range (1, MainQuiz[0][0]+2):
        answer_quiz.insert (counter, 0)

    def graphics2 ():

        windowSurface.fill(BLACK)
        windowSurface.blit(img,(0,0))
        pygame.draw.line(windowSurface, BLACK, (60, 60), (120, 60), 4)
        pygame.draw.rect(windowSurface, BLUE, (25,50,950,100))

        pygame.draw.rect(windowSurface, col1, (200,175,650,100))
        pygame.draw.rect(windowSurface, col2, (200,300,650,100))
        pygame.draw.rect(windowSurface, col3, (200,425,650,100))
        pygame.draw.rect(windowSurface, col4, (200,550,650,100))

        if answer_quiz [SlideNumber] == 1:
            pygame.draw.rect(windowSurface, GREEN, (200,175,650,100))
        elif answer_quiz[SlideNumber] == 2:
            pygame.draw.rect(windowSurface, GREEN, (200,300,650,100))
        elif answer_quiz[SlideNumber] == 3:
            pygame.draw.rect(windowSurface, GREEN, (200,425,650,100))
        elif answer_quiz [SlideNumber]== 4:
            pygame.draw.rect(windowSurface, GREEN, (200,550,650,100))

        TextA=FontA.render('a',1,BLUE)
        windowSurface.blit(TextA,(160,178))

        TextA=FontA.render('b',1,BLUE)
        windowSurface.blit(TextA,(160,303))

        TextA=FontA.render('c',1,BLUE)
        windowSurface.blit(TextA,(160,428))

        TextA=FontA.render('d',1,BLUE)
        windowSurface.blit(TextA,(160,553))

        TextB=FontB.render(MainQuiz[SlideNumber][0],1,WHITE)
        windowSurface.blit(TextB,(35,75))

        TextB=FontB.render(MainQuiz[SlideNumber][1],1,WHITE)
        windowSurface.blit(TextB,(215,200))

        TextB = FontB.render(MainQuiz[SlideNumber][2],1,WHITE)
        windowSurface.blit(TextB,(215,325))

        TextB=FontB.render(MainQuiz[SlideNumber][3],1,WHITE)
        windowSurface.blit(TextB,(215,450))

        TextB=FontB.render(MainQuiz[SlideNumber][4],1,WHITE)
        windowSurface.blit(TextB,(215,575))

        if SlideNumber < MainQuiz[0][0]:
            pygame.draw.rect(windowSurface, BLUE, (875,365, 75,75))
            pygame.draw.lines(windowSurface, BLUE, False, [(950,440), (999,402), (950,365)], 30)
            pygame.draw.rect(windowSurface, BLUE, (950,380, 40,46))
        if SlideNumber == MainQuiz[0][0]:
            pygame.draw.rect (windowSurface, GREEN, (900,700,90,30))
            TextA=FontB.render('DONE',1,BLUE)
            windowSurface.blit(TextA,(900,700))

        if SlideNumber != 1:
            pygame.draw.rect(windowSurface, BLUE, (50,365, 75,75))
            pygame.draw.lines(windowSurface, BLUE, False, [(50,440), (1,402), (50,365)], 30)
            pygame.draw.rect(windowSurface, BLUE, (10,380, 40,46))


        pygame.display.update()

    while 2==a:
        b=2
        graphics2 ()
        while 2==b:

            for event in pygame.event.get():
                mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                if mx > 199 and my >174 and mx < 851 and my < 276:
                    col1 = BLUE2
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE
                    graphics2 ()
                    #A
                elif mx > 199 and my >299 and mx < 851 and my < 401:
                    col1 = BLUE
                    col2 = BLUE2
                    col3 = BLUE
                    col4 = BLUE
                    graphics2 ()
                    #B
                elif mx > 199 and my >424 and mx < 851 and my < 526:
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE2
                    col4 = BLUE
                    graphics2 ()
                    #C
                elif mx > 19 and my >549 and mx < 851 and my < 651:
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE2
                    graphics2 ()
                    #D
                else:
                    col1 = BLUE
                    col2 = BLUE
                    col3 = BLUE
                    col4 = BLUE
                    graphics2 ()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                        if mx > 199 and my >174 and mx < 851 and my < 276:
                            answer_quiz [SlideNumber] = 1
                            col1 = BLUE2
                            col2 = BLUE
                            col3 = BLUE
                            col4 = BLUE
                            graphics2 ()
                            #A
                        elif mx > 199 and my >299 and mx < 851 and my < 401:
                            answer_quiz [SlideNumber] = 2
                            col1 = BLUE
                            col2 = BLUE2
                            col3 = BLUE
                            col4 = BLUE
                            graphics2 ()
                            #B
                        elif mx > 199 and my >424 and mx < 851 and my < 526:
                            answer_quiz [SlideNumber] = 3
                            col1 = BLUE
                            col2 = BLUE
                            col3 = BLUE2
                            col4 = BLUE
                            graphics2 ()
                            #C
                        elif mx > 199 and my >549 and mx < 851 and my < 651:
                            answer_quiz [SlideNumber] =4
                            col1 = BLUE
                            col2 = BLUE
                            col3 = BLUE
                            col4 = BLUE2
                            graphics2 ()
                            #D
                        elif mx > 0 and my >364 and mx < 126 and my < 441:
                            b = 1
                            if SlideNumber > 1:
                                SlideNumber = SlideNumber - 1
                                pygame.draw.rect(windowSurface, GREEN, (50,365, 75,75))
                                pygame.draw.lines(windowSurface, GREEN, False, [(50,440), (1,402), (50,365)], 30)
                                pygame.draw.rect(windowSurface, GREEN, (10,380, 40,46))

                        elif mx > 874 and my >364 and mx < 1000 and my < 441:
                            b = 1
                            if SlideNumber < MainQuiz [0][0]:
                                SlideNumber = SlideNumber + 1
                                pygame.draw.rect(windowSurface, GREEN, (875,365, 75,75))
                                pygame.draw.lines(windowSurface, GREEN, False, [(950,440), (999,402), (950,365)], 30)
                                pygame.draw.rect(windowSurface, GREEN, (950,380, 40,46))
                        elif mx > 899 and mx < 991 and my > 699 and my < 731:
                            if SlideNumber == MainQuiz [0][0]:
                                b=1
                                a=1
                        else:
                            col1 = BLUE
                            col2 = BLUE
                            col3 = BLUE
                            col4 = BLUE
                            graphics2 ()


                        pygame.display.update()

    amount_correct = 0

    for curQuestion in range (1, MainQuiz[0][0]+1):
        if MainQuiz[curQuestion][5] == answer_quiz [curQuestion]:
            amount_correct += 1

    windowSurface.blit(img,(0,0))

    TextB=FontB.render("You got, " + str (amount_correct) + " right",1,BLUE)
    windowSurface.blit(TextB,(35,75))

    TextB=FontB.render("You got, " + str (MainQuiz [0][0] - amount_correct) + " wrong",1,BLUE)
    windowSurface.blit(TextB,(35,115))
    TextB=FontB.render("Click to exit",1,BLUE)
    windowSurface.blit(TextB,(35,155))
    pygame.display.update()

    exit_on = 1
    while exit_on == 1: #loop that waits for user to click confirming they saw their score
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                exit_on = 2

def tutorial():
    SlideNumber = 1
    total_tutorial_length = 5
    g = 2
    n = 2

    def graphics_tutorial ():
        if SlideNumber == 1:
            windowSurface.blit(tutorial_image1,(0,0))
        elif SlideNumber == 2:
            windowSurface.blit(tutorial_image2,(0,0))
        elif SlideNumber == 3:
            windowSurface.blit(tutorial_image3,(0,0))
        elif SlideNumber == 4:
            windowSurface.blit(tutorial_image4,(0,0))
        elif SlideNumber == 5:
            windowSurface.blit(tutorial_image5,(0,0))

        if SlideNumber < total_tutorial_length: #if it isn't the last slide then draw the forward arrow
            pygame.draw.rect(windowSurface, WHITE, (875,365, 75,75))
            pygame.draw.lines(windowSurface, WHITE, False, [(950,440), (999,402), (950,365)], 30)
            pygame.draw.rect(windowSurface, WHITE, (950,380, 40,46))
        if SlideNumber != 1: #if it isn't the first slide then draw the back arrow
            pygame.draw.rect(windowSurface, WHITE, (50,365, 75,75))
            pygame.draw.lines(windowSurface, WHITE, False, [(50,440), (1,402), (50,365)], 30)
            pygame.draw.rect(windowSurface, WHITE, (10,380, 40,46))
        if SlideNumber == total_tutorial_length: #if it is the last slide add the done option
            pygame.draw.rect (windowSurface, GREEN, (900,700,90,30))
            TextA=FontB.render('DONE',1,BLUE)
            windowSurface.blit(TextA,(900,700))
        pygame.display.update()



    graphics_tutorial ()
    while 2==n:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                pygame.display.update()
                mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                if mx > 0 and my >364 and mx < 126 and my < 441:
                    if SlideNumber > 1:
                        SlideNumber -= 1
                        graphics_tutorial ()
                elif mx > 874 and my >364 and mx < 1000 and my < 441:
                    if SlideNumber < total_tutorial_length:
                        SlideNumber += 1
                        graphics_tutorial ()
                elif mx > 899 and mx < 991 and my > 699 and my < 731:
                    if SlideNumber == total_tutorial_length:
                        n = 1

def graphics_menu ():
    windowSurface.fill(WHITE)
    windowSurface.blit(img,(0,0))
    pygame.draw.line(windowSurface, WHITE, (60, 60), (120, 60), 4)
    pygame.draw.rect(windowSurface, BLUE, (25,50,950,100))
    pygame.draw.rect(windowSurface, col1, (200,175,650,100))
    pygame.draw.rect(windowSurface, col2, (200,300,650,100))
    pygame.draw.rect(windowSurface, col3, (200,425,650,100))
    pygame.draw.rect(windowSurface, col4, (200,550,650,100))
    pygame.draw.rect(windowSurface, col7, (875,320,100,60))

    TextB = FontB.render("Shuffle",1,WHITE)
    windowSurface.blit(TextB,(880,330))

    TextB=FontA.render("Test Creator 2014",1,WHITE)
    windowSurface.blit(TextB,(200, 57))

    TextB=FontB.render("Create",1,WHITE)
    windowSurface.blit(TextB,(450,190))

    TextB = FontB.render("Edit",1,WHITE)
    windowSurface.blit(TextB,(470,315))

    TextB=FontB.render("Tutorial",1,WHITE)
    windowSurface.blit(TextB,(460,440))

    TextB=FontB.render("Exit",1,WHITE)
    windowSurface.blit(TextB,(485,565))

    pygame.display.update()

#------------------Main Program Starts here----------------------#
while True:
    c = 2
    a = 2
    windowSurface.blit(img,(0,0))
    pygame.draw.rect(windowSurface, BLUE, (100,100,800,200))
    TextA=FontA.render('Teacher',1,WHITE)
    windowSurface.blit(TextA,(270, 160))
    pygame.draw.rect(windowSurface, BLUE, (100,400,800,200))
    TextA=FontA.render('Student',1,WHITE)
    windowSurface.blit(TextA,(270, 460))
    pygame.display.update()

    while c == 2:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()  #Keep track of mouse position
                if mx > 99 and mx < 901 and my > 99 and my < 301:
                    while 2==a:
                        b=2
                        graphics_menu ()
                        while 2==b:
                            for event in pygame.event.get():
                                mx,my=pygame.mouse.get_pos()
                                if mx > 199 and my >174 and mx < 851 and my < 276:
                                    col1 = BLUE2
                                    col2 = BLUE
                                    col3 = BLUE
                                    col4 = BLUE
                                    graphics_menu ()
                                    #create button
                                elif mx > 199 and my >299 and mx < 851 and my < 401:
                                    col1 = BLUE
                                    col2 = BLUE2
                                    col3 = BLUE
                                    col4 = BLUE
                                    graphics_menu ()
                                    #edit button
                                elif mx > 199 and my >424 and mx < 851 and my < 526:
                                    col1 = BLUE
                                    col2 = BLUE
                                    col3 = BLUE2
                                    col4 = BLUE
                                    graphics_menu ()
                                    #tutorial button
                                elif mx > 199 and my >549 and mx < 851 and my < 651:
                                    col1 = BLUE
                                    col2 = BLUE
                                    col3 = BLUE
                                    col4 = BLUE2
                                    graphics_menu ()
                                    #quit button
                                elif mx > 874 and mx < 976 and my > 319 and my < 381:
                                    col7 = RED1
                                    graphics_menu ()
                                    #shuffle button
                                else:
                                    col1 = BLUE
                                    col2 = BLUE
                                    col3 = BLUE
                                    col4 = BLUE
                                    col7 = RED

                                    graphics_menu ()
                                if event.type == MOUSEBUTTONDOWN:
                                    if event.button == 1:
                                        mx,my=pygame.mouse.get_pos()  #Keep track of mouse position if clicked
                                        if mx > 199 and my >174 and mx < 851 and my < 276:
                                            col1 = GREEN
                                            col2 = BLUE
                                            col3 = BLUE
                                            col4 = BLUE
                                            graphics_menu ()
                                            #create button
                                            create_edit_teacher ("")
                                        elif mx > 199 and my >299 and mx < 851 and my < 401:
                                            col1 = BLUE
                                            col2 = GREEN
                                            col3 = BLUE
                                            col4 = BLUE
                                            graphics_menu ()
                                            create_edit_teacher (filenamePromtMenu())
                                            #edit button
                                        elif mx > 199 and my >424 and mx < 851 and my < 526:
                                            col1 = BLUE
                                            col2 = BLUE
                                            col3 = GREEN
                                            col4 = BLUE
                                            graphics_menu ()
                                            tutorial()
                                            #tutorial button
                                        elif mx > 199 and my >549 and mx < 851 and my < 651:
                                            col1 = BLUE
                                            col2 = BLUE
                                            col3 = BLUE
                                            col4 = GREEN
                                            graphics_menu ()
                                            pygame.quit()
                                            #quit button
                                        elif mx > 874 and mx < 976 and my > 319 and my < 381:
                                            col7 = BLUE
                                            graphics_menu ()
                                            ShuffleFile (filenamePromtMenu())
                                            #shuffle button
                                        else:
                                            col1 = BLUE
                                            col2 = BLUE
                                            col3 = BLUE
                                            col4 = BLUE
                                            col7 = RED
                                            graphics_menu ()
                elif mx > 99 and mx < 901 and my > 399 and my < 601:
                    student_quiz ()
                    c = 1
