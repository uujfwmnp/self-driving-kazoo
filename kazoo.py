import irsdk
import pygame
import time, random
from pygame import mixer
from irsdk import Flags

musicLocation = ['foo.wav', 'bar.mp3', 'foobar.m4a']
# Be sure to put the full path to each file, if it's not in the same directory as this script

ir = irsdk.IRSDK()
ir.startup()
# Testing: Comment the above two lines, uncomment the two in the try: section at the bottom below
mixer.init()  # Initialize pygame mixer

def cautionMusic(sessionFlag):
    print('Caution Is Waving, Playing Music')
    mixer.music.load(random.choice(musicLocation)) # Load a random song from the list
    mixer.music.play() # Play!
    while mixer.music.get_busy():
        pygame.time.delay(100) # This prevents the chosen song from stopping too soon.
        sessionFlag = ir['SessionFlags'] # This should hopefully update from live data
        if (sessionFlag & Flags.one_lap_to_green):
            stopPlayback()

def stopPlayback():
    print('One Lap To Green, Stopping Music')
    if (mixer.music.get_busy() == True):
        mixer.music.fadeout(5000) # Five second long fadeout, then music stops
        time.sleep(6) # This keeps the function from being repeatedly called during the fadeout
    else:
        print('Music is stopped')
        time.sleep(10) # This keeps the function from being repeatedly called during the fadeout

def flagStatus(sessionFlag):
    if (sessionFlag & Flags.one_lap_to_green): # I don't think I need this anymore, since the cautionMusic function handles it all.
        stopPlayback()
    elif (sessionFlag & Flags.caution) or (sessionFlag & Flags.caution_waving): # If the sessionFlag decimal contains the Caution flag in hex, call the function below
        cautionMusic(sessionFlag)
    else:
        print('Not under caution, sleeping')
        time.sleep(10) # Wait 5 seconds before checking session flags again

try:
    while True:
#        ir = {}
#        sessionFlag = ir['SessionFlags'] = int(open("!flag.txt", "r").read()) # 268451840=caution 268452352=one_lap_to_green
        sessionFlag = ir['SessionFlags']
        print(sessionFlag)
        flagStatus(sessionFlag)
        time.sleep(1)
except KeyboardInterrupt:
    print("Ending Program\n")
    quit()
pass
