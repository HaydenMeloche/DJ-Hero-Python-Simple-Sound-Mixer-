import winsound, sys, os
from time import sleep

print os.getcwd()

for i in range(5):
    for i in range (2):
        winsound.PlaySound(os.getcwd()+'\snapFast.wav',winsound.SND_FILENAME)
        winsound.PlaySound(os.getcwd()+'\clap.wav',winsound.SND_FILENAME)

    sleep(0.5)

#use pygame for audio mixing