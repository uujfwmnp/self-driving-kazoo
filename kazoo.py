import time, random, os
import irsdk, pygame, mutagen, m3u8
from pygame import mixer
from irsdk import Flags
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError

playlistLocation = 'C:/path/to/playlist.m3u' # Yeah, you need to convert \ to / for Windows, sorry.
playDuringPractice = True # True to play during Practice, False to not play
playDuringQualify  = False # True to play during Qualifcation, False to not play

test = False # Set to True for test mode, False for live
testFile = 'C:/path/to/flag-status.txt' # Text file for a flag state number: 268451840=caution 268452352=one_lap_to_green 268435456=green

m3u = m3u8.load(playlistLocation)
musicLocation = m3u.segments.uri
ir = irsdk.IRSDK()

def write_id3(song):
    try:
        audio = ID3(song)
    except ID3NoHeaderError: # If there are no ID3 tags, write filename instead
        with open('ID3file.txt', 'w') as file:
            file.write(os.path.basename(song))
    else:
        if any(tags not in audio for tags in ('TIT2','TPE1')): # If Artist or Title tag missing
            #write filename instead
            with open('ID3file.txt', 'w') as file:
                file.write(os.path.basename(song))
        else:
            title  = str(audio['TIT2'])
            artist = str(audio['TPE1'])
            if ('TALB' not in audio): # If the Album ID3 tag is missing
                songTags = title + ' - ' + artist
                #write Title - Artist ID3 tags to file
                with open('ID3file.txt', 'w') as file:
                    file.write(songTags)
            else:
                album  = str(audio['TALB'])
                songTags = title + ' - ' + artist + ' ('+ album +')'
                #write Title - Artist (Album) ID3 tags to file
                with open('ID3file.txt', 'w') as file:
                    file.write(songTags)

def file_prep(song): # Because VLC likes to save playlists in browser-friendly formats, but pygame can't read them.
    stripURI = song.strip('file:///')
    fixSpaces = stripURI.replace('%20',' ')
    return fixSpaces

def play_music(sessionFlag,sessionName):
    song = random.choice(musicLocation) # Choose a random song
    mp3 = MP3(file_prep(song)) # Parse the song headers 
    mixer.init(frequency=mp3.info.sample_rate) # Initialize pygame mixer using the correct frequency/sample rate
    mixer.music.load(file_prep(song)) # Load a random song from the list
    write_id3(song) # Write ID3 tags to a filename for OBS/XSpilit streaming
    print('Mixer Initialized:', mixer.get_init())
    mixer.music.play() # Play!
    print('Status: Playing', song)
    while mixer.music.get_busy():
        pygame.time.delay(100) # This prevents the chosen song from stopping too soon.
        if test == True:
            sessionFlag = ir['SessionFlags'] = int(open(testFile, 'r').read())
            mixer.music.fadeout(5000) # Five second long fadeout, then music stops
        else:
            if (sessionName == 'RACE'):
                sessionFlag = ir['SessionFlags'] # This should hopefully update from live data
            if (sessionFlag & Flags.one_lap_to_green):
                stop_playback()
                break # End the while loop
    time.sleep(0.5)
    if (mixer.get_init() != None) and (mixer.music.get_busy() == False): # This occurs if a song ends while still under caution
        mixer.quit() # Unloads the mixer, required to re-initialize with new sample rates

def stop_playback():
    print('One Lap To Green, Stopping Music')
    mixer.music.fadeout(5000) # Five second long fadeout, then music stops
    time.sleep(6) # This keeps the function from being repeatedly called during the fadeout
    mixer.quit() # Unloads the mixer, required to re-initialize with new sample rates

def flag_status(sessionFlag):
    if (sessionFlag & Flags.one_lap_to_green): # I don't think I need this anymore, since the play_music function handles it all.
        print('Music is stopped')
        time.sleep(10)
    elif (sessionFlag & Flags.caution) or (sessionFlag & Flags.caution_waving): # If the sessionFlag decimal contains the Caution flag in hex, call the function below
        print('Caution Is Waving, Playing Music')
        play_music(sessionFlag,sessionName)
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
            if (sessionName.lower() in ['qualify', 'lone qualify']) and (playDuringQualify == True):
                print('Qualify')
                play_music(sessionFlag,sessionName)
            elif (sessionName.lower() == 'practice') and (playDuringPractice == True):
                print('Practice')
                play_music(sessionFlag,sessionName)
            elif (sessionName.lower() == 'race'):
                print('Race')
                flag_status(sessionFlag)
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
                if (sessionName.lower() in ['qualify', 'lone qualify']) and (playDuringQualify == True):
                    play_music(sessionFlag,sessionName)
                elif (sessionName.lower() == 'practice') and (playDuringPractice == True):
                    play_music(sessionFlag,sessionName)
                elif (sessionName.lower() == 'race'):
                    flag_status(sessionFlag)
                time.sleep(1)
except KeyboardInterrupt:
    print('Ending Program\n')
    if (os.path.exists('ID3file.txt')):
        os.remove('ID3file.txt')    # Cleaning up
    quit()
pass
