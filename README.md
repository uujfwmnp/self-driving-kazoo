# self-driving-kazoo
Silly little Python file to fill your iPacing caution laps with beautiful music.

### Requirements:
 - Python 3.4 or newer
 - PyYAML 3.11 or newer
 - [Python iRacing SDK](https://github.com/kutu/pyirsdk)
 - [pygame](https://www.pygame.org/)

### To use:
 - Run `pip install pyirsdk` to install the Python iRacing SDK module
 - Run `pip install -U pygame --user` to install the pygame module
 - Edit the "musicLocation" variable (currently on line 7) to point to the songs you want to play. Be sure to include the full path to each song, if they are not located in the same directory as this script.
 - Run the iRacing program
 - Run `python kazoo.py` to start the script
 
 ### Notes:
 - ~~It works, but only under controlled testing conditions.~~ It works for sure with ovals, unsure how it will react on road courses that do not have full course cautions.
 - ~~The code probably needs a rewrite.~~ It did, and it was.
 - ~~It has not been tested live on iRacing yet.~~ Works fine for ovals.
