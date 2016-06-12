"""

================================================
**settings.py**: Contains project wide variables
================================================

"""

import os
import pygame
from pygame.locals import *

__author__ = 'Mark Zwart'


FONT_SIZE = 20

SPACE = 10

TITLE_HEIGHT = int(FONT_SIZE * 1.4)
FONT_SPACE = TITLE_HEIGHT
BUTTON_TOP = TITLE_HEIGHT

KEY_SPACE = 4
KEY_WIDTH_STD = 42
KEY_WIDTH_BIG = 64
KEY_WIDTH_HUGE = 96
KEY_HEIGHT = 42

BUTTON_HEIGHT = 42

ICO_WIDTH = 64
ICO_HEIGHT = 42
ICO_INFO_WIDTH = 48

SWITCH_WIDTH = 42
SWITCH_HEIGHT = 42

LIST_WIDTH = 42
LIST_INDICATOR_WIDTH = 6

#: Switches between development/debugging on your desktop/laptop versus running on your Raspberry Pi
RUN_ON_RASPBERRY_PI = (os.name != 'nt' and os.uname()[4][:3] == 'arm')

# Setting up touch screen, set if statement to true on Raspberry Pi
if RUN_ON_RASPBERRY_PI:
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'
    os.environ['SDL_FBDEV'] = '/dev/fb1'
    os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
    os.environ['SDL_MOUSEDRV'] = 'TSLIB'

# Display settings
pygame.init() 	# Pygame initialization
#: The display dimensions, change this if you have a bigger touch screen.
DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320
PYGAME_EVENT_DELAY = 25

if RUN_ON_RASPBERRY_PI:  # If started on Raspberry Pi
    display_flags = FULLSCREEN | DOUBLEBUF | ANYFORMAT  # Turn on video acceleration
    #: Points to the display.
    SCREEN = pygame.display.set_mode(DISPLAY_SIZE, display_flags)
    pygame.mouse.set_visible(False)                                 # Hide mouse cursor
else:
    SCREEN = pygame.display.set_mode(DISPLAY_SIZE)

#: The directory where resources like button icons or the font file is stored.
RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
RESOURCES_ZIP = os.path.join(RESOURCES, 'resources.zip')

#: Standard font type
FONT = pygame.font.Font(os.path.join(RESOURCES, 'LiberationSans-Regular.ttf'), FONT_SIZE)


""" Used icons """
# Switch icons
ICO_SWITCH_ON = 'switch-on.png'
ICO_SWITCH_OFF = 'switch-off.png'

# General icons
ICO_PLAYER_FILE = 'main-playing-file.png'
ICO_PLAYER_FILE_ACTIVE = 'main-playing-file-active.png'
ICO_PLAYLIST = 'main-playlist.png'
ICO_PLAYLIST_ACTIVE = 'main-playlist-active.png'
ICO_LIBRARY = 'main-library.png'
ICO_LIBRARY_ACTIVE = 'main-library-active.png'
ICO_DIRECTORY = 'main-directory.png'
ICO_DIRECTORY_ACTIVE = 'main-directory-active.png'
ICO_SETTINGS = 'main-settings.png'

# Player icons
ICO_PLAY = 'controller-play.png'
ICO_PAUSE = 'controller-pause.png'
ICO_STOP = 'controller-stop.png'
ICO_NEXT = 'controller-next.png'
ICO_PREVIOUS = 'controller-previous.png'
ICO_VOLUME = 'controller-volume.png'

# Volume icons
ICO_VOLUME_UP = 'volume-up.png'
ICO_VOLUME_DOWN = 'volume-down.png'
ICO_VOLUME_MUTE = 'volume-mute.png'
ICO_VOLUME_MUTE_ACTIVE = 'volume-mute-active.png'

# Library icons
ICO_SEARCH = 'filter-search.png'
ICO_SEARCH_ARTIST = 'filter-artists.png'
ICO_SEARCH_ARTIST_ACTIVE = 'filter-artists-active.png'
ICO_SEARCH_ALBUM = 'filter-albums.png'
ICO_SEARCH_ALBUM_ACTIVE = 'filter-albums-active.png'
ICO_SEARCH_SONG = 'filter-songs.png'
ICO_SEARCH_SONG_ACTIVE = 'filter-songs-active.png'
ICO_PLAYLISTS = 'filter-playlists.png'
ICO_PLAYLISTS_ACTIVE = 'filter-playlists-active.png'

# Directory icons
ICO_FOLDER_ROOT = 'folder-root.png'
ICO_FOLDER_UP = 'folder-up.png'

# Standard info icons
ICO_INFO = 'icon-info.png'
ICO_WARNING = 'icon-warning.png'
ICO_ERROR = 'icon-error.png'

# default covers
DEFAULT_COVER = 'cover-files.png'
TMP_COVER = os.path.join(RESOURCES, 'tmp_cover.jpg')

# Special keyboard icons
ICO_SHIFT = 'keys-shift.png'
ICO_BACKSPACE = 'keys-backspace.png'
ICO_ENTER = 'keys-enter.png'
ICO_LETTERS = 'keys-letters.png'
ICO_SYMBOLS = 'keys-symbols.png'
