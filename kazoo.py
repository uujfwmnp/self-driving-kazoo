import time, random, os
import irsdk, pygame, mutagen, m3u8
from pygame import mixer
from irsdk import Flags
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis

test = True # Set to True for test mode, False for live
playlistLocation = 'C:/path/to/playlist.m3u' # Yeah, you need to convert \ to / for Windows, sorry.

m3u = m3u8.load(playlistLocation)
musicLocation = m3u.segments.uri

def SampleRate(ext,song): # To return a sample rate/frequency based on the file extension
    if (ext == '.mp3'):
        mp3 = MP3(song)
        rate = mp3.info.sample_rate
    elif (ext == '.mp4' or ext == '.m4a'): #m4a/mp4 is currently not supported by pygame
        mp4 = MP4(song)
        rate = mp4.info.sample_rate
    elif (ext == '.ogg'):
        ogg = OggVorbis(song)
        rate = ogg.info.sample_rate
    return rate

def cautionMusic(sessionFlag):
    print('Caution Is Waving, Playing Music')
    song = random.choice(musicLocation) # Choose a random song
    name, ext = os.path.splitext(song) # Split the extension from the song title
    mixer.init(frequency=SampleRate(ext,song)) # Initialize pygame mixer using the SampleRate function
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
