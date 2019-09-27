import time, random, os
import irsdk, pygame, mutagen, m3u8
from pygame import mixer
from irsdk import Flags
from mutagen.mp3 import MP3

playlistLocation = 'C:/path/to/playlist.m3u' # Yeah, you need to convert \ to / for Windows, sorry.
playDuringPractice = True # True to play during Practice, False to not play
playDuringQualify  = False # True to play during Qualifcation, False to not play

test = False # Set to True for test mode, False for live
testFile = 'C:/path/to/flag-status.txt' # Text file for a flag state number: 268451840=caution 268452352=one_lap_to_green 268435456=green

m3u = m3u8.load(playlistLocation)
musicLocation = m3u.segments.uri
ir = irsdk.IRSDK()

def FilePrep(song): # Because VLC likes to save playlists in browser-friendly formats, but pygame can't read them.
    stripURI = song.strip('file:///')
    fixSpaces = stripURI.replace('%20',' ')
    return fixSpaces

def playMusic(sessionFlag,sessionName):
    song = random.choice(musicLocation) # Choose a random song
    mp3 = MP3(FilePrep(song)) # Parse the song headers 
    mixer.init(frequency=mp3.info.sample_rate) # Initialize pygame mixer using the correct frequency/sample rate
    mixer.music.load(FilePrep(song)) # Load a random song from the list
    print('Mixer Initialized:', mixer.get_init())
    mixer.music.play() # Play!
    print('Status: Playing', song)
    while mixer.music.get_busy():
        pygame.time.delay(100) # This prevents the chosen song from stopping too soon.
        if test == True:
            sessionFlag = ir['SessionFlags'] = int(open(testFile, 'r').read())
        else:
            if (sessionName == 'RACE'):
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
    if (sessionFlag & Flags.one_lap_to_green): # I don't think I need this anymore, since the playMusic function handles it all.
        print('Music is stopped')
        time.sleep(10)
    elif (sessionFlag & Flags.caution) or (sessionFlag & Flags.caution_waving): # If the sessionFlag decimal contains the Caution flag in hex, call the function below
        playMusic(sessionFlag,sessionName)
    else:
        print('Not under caution, sleeping')
        time.sleep(10) # Wait 10 seconds before checking session flags again

if (test == True):
    print('\n -------------------------------------------------------------')
    print('| Test mode enabled. Please press control-c to stop playback. |')
    print(' -------------------------------------------------------------\n')

try:
    while True:
        if (test == True): # If test mode is enabled
            ir = {}
            sessionFlag = ir['SessionFlags'] = int(open(testFile, 'r').read())
            sessionName = 'practice' #We don't need sessionNum set since we can do it directly here
            #print(sessionFlag)
            if (sessionName in ['QUALIFY', 'LONE QUALIFY', 'qualify', 'lone qualify']) and (playDuringQualify == True):
                print('Qualify')
                playMusic(sessionFlag,sessionName)
            elif (sessionName in ['PRACTICE', 'practice']) and (playDuringPractice == True):
                print('Practice')
                playMusic(sessionFlag,sessionName)
            elif (sessionName in ['RACE', 'race']):
                print('Race')
                flagStatus(sessionFlag)
            time.sleep(1)
        else:
            ir.startup()
            if (ir.startup()) == False: # This can occur if the sim is not running or fully loaded
                print('iRacing is not running or not fully loaded, sleeping 15 seconds. . . ')
                time.sleep(15)
            else:
                sessionFlag = ir['SessionFlags']
                sessionNum = ir['SessionNum']
                sessionName = ir['SessionInfo']['Sessions'][sessionNum]['SessionName']
                #print(sessionFlag)
                if (sessionName in ['QUALIFY', 'LONE QUALIFY', 'qualify', 'lone qualify']) and (playDuringQualify == True):
                    playMusic(sessionFlag,sessionName)
                elif (sessionName in ['PRACTICE', 'practice']) and (playDuringPractice == True):
                    playMusic(sessionFlag,sessionName)
                elif (sessionName in ['RACE', 'race']):
                    flagStatus(sessionFlag)
                time.sleep(1)
except KeyboardInterrupt:
    print('Ending Program\n')
    quit()
pass
