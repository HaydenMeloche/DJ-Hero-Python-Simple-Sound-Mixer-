from array import array
from struct import pack

import pyaudio
import wave
import pygame
from pygame.locals import *
import os

#--------------------------------------------------------------------------------

class soundSample (object):

    def __init__(self, threshold,chunkSize,rate,letter):
        self.threshold = threshold #used to determine when the user is talking or not
        self.chunkSize= chunkSize #used
        self.letter = letter #used for exporting and which key the loop will be later binded to
        self.rate = rate #used for recording then after speeding or slowing down when exporting
        self.originalRate = rate #the original rate recorded, used for restoring the rate of the audio

        self.Format = pyaudio.paInt16
        self.recordedAudio = array("h")
        self.sampleWidth = 2 #used to initialize sample width which be recieved after the recording
        self.rateRelative = 0 #how high or low the rate is relative to the starting position

    def is_silent(self,snd_data): #see if the sound is less then the threshold and is silent
        return max(snd_data) < self.threshold

    def normalize(self,snd_data):
        maxVal = 16384
        times = float(maxVal)/max(abs(i) for i in snd_data)

        normalizedAudio = array('h')
        for i in snd_data:
            normalizedAudio.append(int(i*times))
        return normalizedAudio

    def trim(self,snd_data): #removes empty audio at the end of the sample
        soundsList = array.tolist(snd_data) #creates a list from the recorded audio array
        trimmedSound = array('h')
        for i in range (len(soundsList)-70000): #for the length of the recorded audio minus the last second
            trimmedSound.append(soundsList[i]) #add from the list to the new trimmed array
        return trimmedSound # return the trimmed audio

    def speedOrSlow (self,amount): #takes in an amount that will be used to speed up or slow down a sample
        self.rate = self.rate + amount #modifies audio rate with the passed amount
        if amount < 0: #if the rate has been lowered
            if self.rate < 0: #if the rate is below 0 and invalid
                self.rate = 20000*2 #then default the rate to 20000*2
            else: #if the modified rate is valid
                self.rateRelative -= 1

        else:
            self.rateRelative += 1

    def restoreRate (self): #restore the audio rate back to the original
        self.rate = self.originalRate
        self.rateRelative = 0


    def record(self): #record function

        p = pyaudio.PyAudio()
        stream = p.open(format=self.Format, channels=1, rate=self.rate,
            input=True, output=True,
            frames_per_buffer=self.chunkSize)

        audio = array('h') #the array to hold all the audio data
        print "Waiting............."

        while True: #Loops until silence is broken
            snd_data = array('h', stream.read(self.chunkSize))

            if not (self.is_silent(snd_data)): #if the audio isn't silent
                audio.extend(snd_data) #add the audio
                break #break the silent loop

        print "Started" #Let the games begin

        num_silent = 0 #used to track how long the user has been silent for

        while True: #Infinitely loops until the user stops making noise
            snd_data = array('h', stream.read(self.chunkSize))
            audio.extend(snd_data) #Saves noise which is later exported

            silent = self.is_silent(snd_data) #boolean if the recorded is silent or not

            if silent:
                num_silent += 1
                print num_silent

            else:
                num_silent = 0  #resets silence counter to zero
                print "talking" #output user it talking

            if num_silent > 100: #last number is how long continued silence before programs
                break #break the recording loop

        self.sampleWidth = p.get_sample_size(self.Format) #get the sample width
        stream.stop_stream()
        stream.close()
        p.terminate()

        audio = self.normalize(audio) #normalize the audio
        audio = self.trim(audio) #Removes Silence at the end

        self.sampleWidth = p.get_sample_size(self.Format) #sets the sample width of the recording
        self.recordedAudio = audio #sets the recorded audio in array form to the object

    def export (self): #export the recorded audio
        data = self.recordedAudio #the recorded audio in array form
        data = pack('<' + ('h'*len(data)), *data) #prepares the audio for exporting into a wav file

        wf = wave.open("userSamples/"+self.letter+".wav", 'wb') #creates a wave file based on the letter of the object
        wf.setnchannels(1)
        wf.setsampwidth(self.sampleWidth)
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()

        #beta testing array to text file

        textFile = open(os.getcwd()+"/keyConfig/"+self.letter+".txt",'w') #open a text file based on the letter of the object

        for i in self.recordedAudio: #for every item in the array
            textFile.write("%s\n" % i) #write the number to the text file

        textFile.close() #close the text file

    def play (self): #play the sound associated with the current letter
        curSound = pygame.mixer.Sound("userSamples/"+self.letter+'.wav')
        curSound.play()
