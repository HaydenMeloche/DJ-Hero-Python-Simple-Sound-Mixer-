import pygame
from time import sleep
from pygame.locals import *

pygame.init()

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