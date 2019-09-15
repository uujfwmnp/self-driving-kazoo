import time, random, os
import irsdk, pygame, mutagen, m3u8
from pygame import mixer
from irsdk import Flags
from mutagen.mp3 import MP3

playlistLocation = 'C:/path/to/playlist.m3u' # Yeah, you need to convert \ to / for Windows, sorry.
test = False # Set to True for test mode, False for live
testFile = 'C:/path/to/flag-status.txt' # Text file for a flag state number: 268451840=caution 268452352=one_lap_to_green 268435456=green

m3u = m3u8.load(playlistLocation)
musicLocation = m3u.segments.uri

def FilePrep(song): # Because VLC likes to save playlists in browser-friendly formats, but pygame can't read them.
    stripURI = song.strip('file:///')
    fixSpaces = stripURI.replace('%20',' ')
    return fixSpaces

def cautionMusic(sessionFlag):
    print('Caution Is Waving, Playing Music')
    song = random.choice(musicLocation) # Choose a random song
    mp3 = MP3(FilePrep(song)) # Parse the song headers 
    mixer.init(frequency=mp3.info.sample_rate) # Initialize pygame mixer using the correct frequency/sample rate
    mixer.music.load(FilePrep(song)) # Load a random song from the list
    mixer.music.play() # Play!
    while mixer.music.get_busy():
        pygame.time.delay(100) # This prevents the chosen song from stopping too soon.
        if (test == True):
            sessionFlag = ir['SessionFlags'] = int(open(testFile, 'r').read())
        else:
            sessionFlag = ir['SessionFlags'] # This should hopefully update from live data
        if (sessionFlag & Flags.one_lap_to_green):
            stopPlayback()
            break # End the while loop
    time.sleep(0.5)
    if (mixer.get_init() != None) and (mixer.music.get_busy() == False): # This occurs if a song ends while still under caution
        mixer.quit() # Unloads the mixer, required to re-initialize with new sample rates

def stopPlayback():
    print('One Lap To Green, Stopping Music')
    mixer.music.fadeout(5000) # Five second long fadeout, then music stops
    time.sleep(6) # This keeps the function from being repeatedly called during the fadeout
    mixer.quit() # Unloads the mixer, required to re-initialize with new sample rates

def flagStatus(sessionFlag):
    if (sessionFlag & Flags.one_lap_to_green): # I don't think I need this anymore, since the cautionMusic function handles it all.
        print('Music is stopped')
        time.sleep(10)
    elif (sessionFlag & Flags.caution) or (sessionFlag & Flags.caution_waving): # If the sessionFlag decimal contains the Caution flag in hex, call the function below
        cautionMusic(sessionFlag)
    else:
        print('Not under caution, sleeping')
        time.sleep(10) # Wait 10 seconds before checking session flags again

if (test == True):
    print('\n -------------------------------------------------------------')
    print('| Test mode enabled. Please press control-c to stop playback. |')
    print(' -------------------------------------------------------------\n')

try:
    while True:
        if (test == True):
            ir = {}
            sessionFlag = ir['SessionFlags'] = int(open(testFile, 'r').read())
            flagStatus(sessionFlag)
            time.sleep(1)
        else:
            ir = irsdk.IRSDK()
            ir.startup()
            if (ir.startup()) == False:
                print('iRacing is not running or not fully loaded, sleeping 15 seconds. . . ')
                time.sleep(15)
            else:
                sessionFlag = ir['SessionFlags']
                #print(sessionFlag)
                flagStatus(sessionFlag)
                time.sleep(1)
except KeyboardInterrupt:
    print('Ending Program\n')
    quit()
pass
