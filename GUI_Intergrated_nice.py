from FSE_Classes import soundSample
from UsersSolo import playBack
from Tkinter import*
from PIL import Image, ImageTk
import pyaudio
import pygame
from pygame.locals import *
import os
from array import array

class mainScreen (object):
    def __init__(self):
        self.listOfKeys = {} #a dictionary of all keys that are bound. Each item in the dictionary has a value of a soundSample object
        self.drumLoop = 2 #the default drum loop
        self.textLabel = StringVar() #the text label on the top of the tk window
        self.keyLabel = StringVar()
        self.radioButtonValue = "Piano"
        self.listOfLetters= []
        self.radioButton = StringVar()
        self.restored = False

        self.radioButton.set("Piano")

        self.choices = ["Guitar","Piano"]

        self.updateTextKeys()

        pygame.init #start pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=100) #start the pygame mixer

    def setText(self, text): #takes a string and updates the text at the top of the screen
        self.textLabel.set(text)

    def updateTextKeys(self):
        self.listOfLetters.sort() #sorts all the letters
        if len(self.listOfKeys) == 0:#if there isnt any bound keys
            self.keyLabel.set("Bound Keys: None")
        else: #there is bound keys
            listOfBoundKeys = "" # a string to hold all the keys

            for i in self.listOfLetters: #for every item in the list of letters
                listOfBoundKeys += i + " " #add the current current item in the list to the string with a space

            self.keyLabel.set("Bound Keys: " + listOfBoundKeys) #update the second text box

    def bindKey (self,letter): #takes a key that has not yet been bound and initializes it to a soundSample object
        if len(letter) > 0: #if there is a key in the textbox for
            if not letter in self.listOfKeys: #if the key has not been bound yet
                self.listOfKeys[letter] = soundSample(5000,1024,44100*2,letter) #create a new object for the key
                self.setText(letter + " key has been bound") #tell the user that the key has been bound
                self.listOfLetters.append(letter)
                self.updateTextKeys()
        else:
            self.setText( "please enter one key for the sound to be bound to")

    def playLoop(self,): #starts live playback using recorded audio samples
        solo = playBack(self.listOfKeys,str(self.radioButtonValue),self.drumLoop) #create a new object using the dictionary of bound keys
        print self.radioButtonValue
        solo.userSolo() #starts the playback

    def recordButton(self,letter):

        if self.keyErrorCheck(letter): #if the key has been bound
            self.listOfKeys[letter].record() #record audio
            self.resetButton(letter) #reset the speed back to normal
            self.setText("Done Recording ") #tell the user that recording has stopped
        else:
            self.setText("Key must be bound first") #tell the user that the key is invalid

    def speedUpButton(self,letter):
        if self.keyErrorCheck(letter): #if the key has been bound

            if self.listOfKeys[letter].rate < self.listOfKeys[letter].originalRate: #if the speed is slowed down
                self.listOfKeys[letter].speedOrSlow(20000*2) #then speed up by a little bit
            else: #otherwise the speed is either normal or speed up
                self.listOfKeys[letter].speedOrSlow(80000*2) #speed up by a lot

            self.listOfKeys[letter].export()
            self.setText("Current speed is: " + str(self.listOfKeys[letter].rateRelative))

    def slowDownButton(self,letter): #slows down the speed of the audio
        if self.keyErrorCheck(letter): #if  the key is bound
            if self.listOfKeys[letter].rate > self.listOfKeys[letter].originalRate: #if the speed is speed up
                self.listOfKeys[letter].speedOrSlow(-80000*2) # slow down a lot
            else: #if the speed is normal or slow
                self.listOfKeys[letter].speedOrSlow(-20000*2) # slow down a bit
            self.listOfKeys[letter].export() #export the slowed down audio
            self.setText("Current speed is: " + str(self.listOfKeys[letter].rateRelative)) #tell the user how fast the speed is

    def resetButton(self,letter): #resets the speed
        if self.keyErrorCheck(letter): #if the key is bound
            self.listOfKeys[letter].restoreRate() #then reset the speed back to normal
            self.listOfKeys[letter].export() #export the modified.
            self.setText("Speed is now normal")

    def playButton(self,letter): #play the exported audio of the current letter
        if self.keyErrorCheck(letter):
            self.listOfKeys[letter].play() #play the recorded audio

    def toggleBeat(self): #toggles the beat in the background
        if pygame.mixer.music.get_busy(): #if the beat is playing
            pygame.mixer.music.stop() #stop the beat
        else: #otherwise the beat is not playing start the beat
            pygame.mixer.music.load('Drum_loops/'+str(self.drumLoop)+'.wav') #start the music
            pygame.mixer.music.play(-1) #-1 means loop infitenetly
            pygame.mixer.music.set_volume(0.3)

    def changeBeat(self):
        if pygame.mixer.music.get_busy():#if the music is playing
            pygame.mixer.music.stop() #stop the music
        #cycles through the drum loops
        self.drumLoop += 1
        if self.drumLoop > 5:
            self.drumLoop = 1

        pygame.mixer.music.load('Drum_loops/'+str(self.drumLoop)+'.wav') #plays the updated
        pygame.mixer.music.play(-1) #-1 means loop infitenetly
        pygame.mixer.music.set_volume(0.3)

    def keyErrorCheck(self,letter):
        if letter in self.listOfKeys: #if the letter is in the dictionary then tell the user then that means it is bound
            return True
        else: #otherwise the key is not in the dictionary and thus is not bound
            self.setText( letter+" must be bound first") #update the text at the top to tell the user the problem
            return False

    def restoreKeys (self): #restores the keys from exported file
        if self.restored:
            self.setText("The keys have ALREADY been restored")
        else:
            for fileName in os.listdir(os.getcwd()+"/userSamples"): #for every file in the userSamples folder
                if fileName.endswith(".wav") and fileName[1] == ".": #if the file is a wav and is one letter long
                    self.listOfKeys[fileName[0]] = soundSample(5000,1024,44100*2,fileName[0]) #then initialize the object with the letter of the wav file
                    self.listOfLetters.append(fileName[0])

                    textFile = open(os.getcwd()+"/keyConfig/"+fileName[0]+".txt",'r') #open the text file using the letter of the found file
                    listText = textFile.readlines() # read in a text file to a list
                    arrayText = array("h") #creates an array
                    for i in listText: #for every item in listText
                        arrayText.append(int(i)) #add the current item in listText to the array

                    self.listOfKeys[fileName[0]].recordedAudio = arrayText #take the array file and store it to the soundObject
                    self.updateTextKeys()
                    self.setText("The keys have been restored")
                    self.restored = True


    def deleteFolder (self): #deletes the contents of the folder
        for fileName in os.listdir(os.getcwd()+"\userSamples"): #for every file in userSamples
            os.remove(os.getcwd()+"\userSamples/"+fileName) #delete the current file in userSamples
        for fileName in os.listdir(os.getcwd()+"\keyConfig"): #for every file in keyConfig
            os.remove(os.getcwd()+"\keyConfig/"+fileName) #delete the current file

        self.listOfKeys = {} #remove all the contents of the dictionary listOfKeys
        self.listOfLetters = []
        self.setText("Samples have been cleared") #tell the user that the text has been updated
        self.updateTextKeys() #update that the keys are no longer bound



#---------------------------------------------------------------------------
root=Tk()
root.wm_title("DJ Hero") #set the title of the window to DJ Hero
main = mainScreen() #set main to a mainscreen object

main.setText("Welcome") #set the top text to 'welcome'

top=Frame(root)
secondTop = Frame(root)
side=Frame(root)
secondTop.pack(side = TOP)
top.pack(side=TOP)

def getInstrument():
    main.radioButtonValue = main.radioButton.get()

for txt in main.choices:
    Radiobutton(root,text=txt,padx = 20,variable=main.radioButton,command=getInstrument,value=txt).pack(in_ = secondTop,side = LEFT)


#status bar
Label(textvariable=main.textLabel,bg="black",fg="white").pack(in_=top, fill = X)
Label(textvariable=main.keyLabel,bg="black",fg="white").pack(in_=top, fill = X)

#top commands
Button(text="Record", bg="red",  command=lambda: main.recordButton(bind.get())).pack(in_=top, side=TOP, fill=X,)
Button(text="Play",   bg="green", command=lambda: main.playButton(bind.get())).pack(in_=top, side=LEFT, fill=Y,)

#Bottom Commands
Button(text="Delete Samples",  command=lambda: main.deleteFolder()).pack(side=BOTTOM, fill=X,)
Button(text="Restore Keys",  command=lambda: main.restoreKeys()).pack(side=BOTTOM, fill=X,)
Button(text="Change Beat",  command=lambda: main.changeBeat()).pack(side=BOTTOM, fill=X,)
Button(text="Toggle Beat",  command=lambda: main.toggleBeat()).pack(side=BOTTOM, fill=X,)
Button(text="Reset",  command=lambda:main.resetButton(bind.get())).pack(side=BOTTOM, fill=X,)
Button(text="Slow Down ",  command=lambda:main.slowDownButton(bind.get())).pack(side=BOTTOM, fill=X,)
Button(text="Speed Up ^",  command=lambda:main.speedUpButton(bind.get())).pack(side=BOTTOM, fill=X,)
Button(text="Run",  command=lambda: main.playLoop()).pack(side=BOTTOM, fill=X,)


# bind new keys
bind= Entry(root)
bind.pack(side=RIGHT)
Button(text="Bind NEW Key", command=lambda: main.bindKey(bind.get())).pack(side=RIGHT)

#display image
image = Image.open("DJ Hero.jpg")
image = image.resize((350, 250), Image.ANTIALIAS) #The (250, 250) is (height, width)
photo = ImageTk.PhotoImage(image)
label = Label(image=photo)
label.image = photo # keep a reference!
label.pack(in_=top, )

root.mainloop()



#Sarros Approved