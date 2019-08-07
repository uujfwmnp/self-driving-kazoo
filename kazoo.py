import irsdk
import pygame
import time
from pygame import mixer
from irsdk import Flags

pygame.init() # Initialize pygame
mixer.init()  # Initialize pygame mixer
musicLocation = 'F:/iRacing/Local Forecast - Elevator.mp3'

def flagSet(flagType):
    if (sess_flag & flagType): # If the current "SessionFlags" contains the required flag type, return True
        return True

def cautionMusic():
    musicStatus = "" #set this outside
    try:
        while True:
            if (flagSet(Flags.caution_waving) == True):
                print('Caution Is Waving, Playing Music')
                if (musicStatus = Playing): # If the music is already playing...
                    time.sleep(1) # Do nothing
                else:
                    musicStatus = Playing # Set the variable
                    mixer.music.load(musicLocation) # Load the song
                    mixer.music.play(loops=-1) # Play it infinitely
            if (flagSet(Flags.one_lap_to_green) == True):
                print('One Lap To Green, Stopping Music')
                musicStatus = "" # Set the variable back to empty
                mixer.fadeout(5000) # Five second long fadeout, then music stops
            else:
                time.sleep(5) # Wait 5 seconds before checking session flags again
    except KeyboardInterrupt:
        print("Ending Program\n")
        quit()
    pass

cautionMusic()
