import pygame
from time import sleep


# Initialize the mixer
pygame.mixer.init()
# Load two sounds
"""
for i in range (11):
    snd1 = pygame.mixer.Sound('piano/'+str(i)+'.wav')
    snd1.play()
    sleep(0.1)
"""
pygame.mixer.music.load('Drum_loops/2.wav')
pygame.mixer.music.play(-1)
for i in range (11):
    snd1 = pygame.mixer.Sound('piano/'+str(i)+'.wav')
    snd1.play()
    sleep(1.3)
    snd1.play()
    sleep(1.3)
sleep (10)
pygame.mixer.music.stop()
# Play the sounds; these will play simultaneously
#use pygame for audio mixing