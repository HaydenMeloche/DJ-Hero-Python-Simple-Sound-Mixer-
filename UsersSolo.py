import pygame,sys
from pygame.locals import *

class playBack(object):

    def __init__(self,soundDictionary,folderName,drumNumber):

        windowSurface = pygame.display.set_mode((100, 100), 0, 32) #needs screen for keyboard input

        self.userSounds = {}
        self.drumNumber = drumNumber #the drum loop to be played in the background
        self.folderName = folderName #the folder name of the instruments of the top row keys

        for i in soundDictionary: #for every bound letter
            self.userSounds[i]=pygame.mixer.Sound('userSamples/'+i+'.wav') #add a item to the dictionairy with a pygame sound object value

        self.instrumentList = [] #
        for i in range (10):
            curSound = pygame.mixer.Sound(folderName+'/'+str(i)+'.wav')
            self.instrumentList.append(curSound)

    def is_Int(self,text): #determines if a string is also an integer, returns true or false
        try:
            int(text)
            return True
        except ValueError:
            return False

    def userSolo(self):

        pygame.mixer.music.load('Drum_loops/'+str(self.drumNumber)+'.wav') #backtrack selection
        pygame.mixer.music.play(-1) #-1 means loop infitenetly

        while True: #infinite loop, exits loop when user hits enter
            for event in pygame.event.get():
                if event.type == KEYDOWN: #if a key is being pressed
                    currentKey = event.key #save what key is being pressed to currentKey

                    otherKeys = pygame.key.get_pressed() #stores all the other keys , ex: the shift keys
                    if currentKey == 8: #delete key
                        print "exited"
                        pygame.mixer.music.stop()
                        pygame.display.quit()
                        return False #exits loop


                    if currentKey <= 256: #fixes crash with keys such as windows button
                        if self.is_Int(chr(currentKey)): #if the key pressed is a top row number
                            if self.folderName == "Piano":
                                self.instrumentList[int(chr(currentKey))].set_volume(0.5)
                            else:
                                self.instrumentList[int(chr(currentKey))].set_volume(0.8)
                            self.instrumentList[int(chr(currentKey))].play() #play the corresponding wav file

                        else: #if its another key
                            if chr(currentKey) in self.userSounds: #if the key is binded to a sound
                                self.userSounds[chr(currentKey)].play()#then play that sound
                            else: #otherwise the key is unkown
                                print "unbinded key"

