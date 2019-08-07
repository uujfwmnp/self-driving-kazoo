import irsdk
import pygame
import time
from pygame import mixer
from irsdk import Flags

musicLocation = 'Local Forecast - Elevator.mp3'

ir = irsdk.IRSDK()
ir.startup()
# To test: Comment out the above two lines, uncomment the two below
#ir = {}
#sess_flag = ir['SessionFlags'] = 268452352
mixer.init()  # Initialize pygame mixer

def flagSet(flagType):
    if (sess_flag & flagType): # If the current "SessionFlags" contains the required flag type, return True
        return True

def cautionMusic():
    musicStatus = "" #set this outside
    try:
        while True:
            if (flagSet(Flags.caution) == True):
                print('Caution Is Waving, Playing Music')
                if (musicStatus == 'Playing'): # If the music is already playing...
                    time.sleep(1) # Do nothing
                else:
                    musicStatus = 'Playing' # Set the variable
                    mixer.music.load(musicLocation) # Load the song
                    mixer.music.play(loops=-1) # Play it infinitely
                    while mixer.music.get_busy():
                        pygame.time.delay(100)
            if (flagSet(Flags.one_lap_to_green) == True):
                print('One Lap To Green, Stopping Music')
                if (musicStatus == 'Stopped'): # If the music is already playing...
                    time.sleep(1) # Do nothing
                else:
                    musicStatus = 'Stopped' # Set the variable to
                    mixer.fadeout(5000) # Five second long fadeout, then music stops
            else:
                print('Not under caution, sleeping')
                time.sleep(5) # Wait 5 seconds before checking session flags again
    except KeyboardInterrupt:
        print('Ending Program\n')
        quit()
    pass

cautionMusic()
