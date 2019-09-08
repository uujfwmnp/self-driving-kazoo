import time, random, os
import irsdk, pygame, mutagen, m3u8
from pygame import mixer
from irsdk import Flags
from mutagen.mp3 import MP3

test = True # Set to True for test mode, False for live
playlistLocation = 'C:/path/to/playlist.m3u' # Yeah, you need to convert \ to / for Windows, sorry.

m3u = m3u8.load(playlistLocation)
musicLocation = m3u.segments.uri

def cautionMusic(sessionFlag):
    print('Caution Is Waving, Playing Music')
    song = random.choice(musicLocation) # Choose a random song
    mp3 = MP3(song) # Parse the song headers 
    mixer.init(frequency=mp3.info.sample_rate) # Initialize pygame mixer using the correct frequency/sample rate
    mixer.music.load(song) # Load a random song from the list
    mixer.music.play() # Play!
    while mixer.music.get_busy():
        pygame.time.delay(100) # This prevents the chosen song from stopping too soon.
        sessionFlag = ir['SessionFlags'] # This should hopefully update from live data
        if (sessionFlag & Flags.one_lap_to_green):
            stopPlayback()
    mixer.quit() # Unload the mixer

def stopPlayback():
    print('One Lap To Green, Stopping Music')
    if (mixer.music.get_busy() == True):
        mixer.music.fadeout(5000) # Five second long fadeout, then music stops
        time.sleep(6) # This keeps the function from being repeatedly called during the fadeout
        mixer.quit() # Unload the mixer
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

if test == True:
    print('\n -------------------------------------------------------------')
    print('| Test mode enabled. Please press control-c to stop playback. |')
    print(' -------------------------------------------------------------\n')

try:
    while True:
        if test == True:
            ir = {}
            sessionFlag = ir['SessionFlags'] = 268451840 # 268451840=caution 268452352=one_lap_to_green
            flagStatus(sessionFlag)
            time.sleep(1)
        else:
            ir = irsdk.IRSDK()
            ir.startup()
            if (ir.startup()) == False:
                print("Game Ain't Running!")
                exit()
            else:
                sessionFlag = ir['SessionFlags']
                print(sessionFlag)
                flagStatus(sessionFlag)
                time.sleep(1)
except KeyboardInterrupt:
    print("Ending Program\n")
    quit()
pass
