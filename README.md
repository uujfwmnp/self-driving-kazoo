# self-driving-kazoo
Silly little Python file to fill your iPacing caution laps with beautiful music.

### Requirements:
 - Python 3.4 or newer
 - PyYAML 3.11 or newer
 - [m3u8](https://github.com/globocom/m3u8) 0.3.12 or newer
 - [mutagen](https://github.com/quodlibet/mutagen) 1.42.0 or newer
 - [Python iRacing SDK](https://github.com/kutu/pyirsdk)
 - [pygame](https://www.pygame.org/) 1.9.6 or newer

### To use:
 - Run `pip install pyirsdk` to install the Python iRacing SDK module
 - Run `pip install m3u8` to install the m3u8 parser module
 - Run `pip install mutagen` to install the mutagen id3 parser module
 - Run `pip install -U pygame --user` to install the pygame module
 - Edit the "musicLocation" variable to point to your m3u/m3u8 playlist, be sure to include the full path to the file.
 - Run the iRacing program
 - Run `python kazoo.py` to start the script
 - Press Control-C to stop the script, or just close the terminal window I suppose.
 
 ### Test Mode:
 - If you find yourself wanting to run the script without being ingame, edit the "test" variable from `False` to `True`. This can be useful for people wanting to set audio levels or test other things prior to live use in game.
 
 ### Notes:
 - ~~It works, but only under controlled testing conditions.~~ It works for sure with ovals, unsure how it will react on road courses that do not have full course cautions.
 - ~~The code probably needs a rewrite.~~ It did, and it was.
 - ~~It has not been tested live on iRacing yet.~~ Works fine for ovals.
 - Make sure your playlist has the absolute path to each music file, or it will not play (and will probably crash the script).
