"""

================================================
**settings.py**: Contains project wide variables
================================================

"""
__author__ = 'Mark Zwart'

import os
import sys, pygame
from pygame.locals import *
import time


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
KEY_SIZE_STD = '%dx%d' % (KEY_WIDTH_STD, KEY_HEIGHT)
KEY_SIZE_BIG = '%dx%d' % (KEY_WIDTH_BIG, KEY_HEIGHT)

BUTTON_HEIGHT = 42

#ICO_SIZE = '48x32'
ICO_WIDTH = 64
ICO_HEIGHT = 42
ICO_SIZE = '%dx%d' % (ICO_WIDTH, ICO_HEIGHT)
ICO_INFO_WIDTH = 48

SWITCH_WIDTH = 42
SWITCH_HEIGHT = 42
SWITCH_SIZE = '%dx%d' % (SWITCH_WIDTH, SWITCH_HEIGHT)

LIST_WIDTH = 42
LIST_INDICATOR_WIDTH = 6

#: Switches between development/debugging on your desktop/laptop versus running on your Raspberry Pi
RUN_ON_RASPBERRY_PI = os.uname()[4][:3] == 'arm'

# Setting up touch screen, set if statement to true on Raspberry Pi
if RUN_ON_RASPBERRY_PI:
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
RESOURCES = os.path.dirname(__file__) + '/resources/'

#: Standard font type
FONT = pygame.font.Font(RESOURCES + 'LiberationSans-Regular.ttf', FONT_SIZE)

""" Color definitions """
BLUE = 0, 148, 255
CREAM = 206, 206, 206
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
# Scheme aqua (currently not in use)
AQUA_TEAL = 18, 151, 147
AQUA_CHARCOAL = 80, 80, 80
AQUA_YELLOW = 255, 245, 195
AQUA_BLUE = 155, 215, 213
AQUA_PINK = 255, 114, 96
# Scheme FIFTIES
FIFTIES_CHARCOAL = 124, 120, 106
FIFTIES_TEAL = 141, 205, 193
FIFTIES_GREEN = 211, 227, 151
FIFTIES_YELLOW = 255, 245, 195
FIFTIES_ORANGE = 235, 110, 68

""" Mouse related variables """
GESTURE_MOVE_MIN = 50  # Minimum movement in pixels to call it a move
GESTURE_CLICK_MAX = 15  # Maximum movement in pixels to call it a click
GESTURE_PRESS_MIN = 500  # Minimum time to call a click a long press
# Gesture enumeration
GESTURE_NONE = -1
GESTURE_CLICK = 0
GESTURE_SWIPE_LEFT = 1
GESTURE_SWIPE_RIGHT = 2
GESTURE_SWIPE_UP = 3
GESTURE_SWIPE_DOWN = 4
GESTURE_LONG_PRESS = 5
GESTURE_DRAG_VERTICAL = 6
GESTURE_DRAG_HORIZONTAL = 7

""" Used icons """
# Switch icons
ICO_SWITCH_ON = RESOURCES + 'switch-on.png'
ICO_SWITCH_OFF = RESOURCES + 'switch-off.png'

# General icons
ICO_PLAYER_FILE = RESOURCES + 'main-playing-file.png'
ICO_PLAYER_FILE_ACTIVE = RESOURCES + 'main-playing-file-active.png'
ICO_PLAYER_RADIO = RESOURCES + 'main-playing-radio.png'
ICO_PLAYER_RADIO_ACTIVE = RESOURCES + 'main-playing-radio-active.png'
ICO_PLAYLIST = RESOURCES + 'main-playlist.png'
ICO_PLAYLIST_ACTIVE = RESOURCES + 'main-playlist-active.png'
ICO_LIBRARY = RESOURCES + 'main-library.png'
ICO_LIBRARY_ACTIVE = RESOURCES + 'main-library-active.png'
ICO_DIRECTORY = RESOURCES + 'main-directory.png'
ICO_DIRECTORY_ACTIVE = RESOURCES + 'main-directory-active.png'
ICO_RADIO = RESOURCES + 'main-radio.png'
ICO_RADIO_ACTIVE = RESOURCES + 'main-radio-active.png'
ICO_SETTINGS = RESOURCES + 'main-settings.png'

# Player icons
ICO_PLAY = RESOURCES + 'controller-play.png'
ICO_PAUSE = RESOURCES + 'controller-pause.png'
ICO_STOP = RESOURCES + 'controller-stop.png'
ICO_NEXT = RESOURCES + 'controller-next.png'
ICO_PREVIOUS = RESOURCES + 'controller-previous.png'
ICO_VOLUME = RESOURCES + 'controller-volume.png'

# Volume icons
ICO_VOLUME_UP = RESOURCES + 'volume-up.png'
ICO_VOLUME_DOWN = RESOURCES + 'volume-down.png'
ICO_VOLUME_MUTE = RESOURCES + 'volume-mute.png'
ICO_VOLUME_MUTE_ACTIVE = RESOURCES + 'volume-mute-active.png'

# Library icons
ICO_SEARCH = RESOURCES + 'filter-search.png'
ICO_SEARCH_ARTIST = RESOURCES + 'filter-artists.png'
ICO_SEARCH_ARTIST_ACTIVE = RESOURCES + 'filter-artists-active.png'
ICO_SEARCH_ALBUM = RESOURCES + 'filter-albums.png'
ICO_SEARCH_ALBUM_ACTIVE = RESOURCES + 'filter-albums-active.png'
ICO_SEARCH_SONG = RESOURCES + 'filter-songs.png'
ICO_SEARCH_SONG_ACTIVE = RESOURCES + 'filter-songs-active.png'
ICO_PLAYLISTS = RESOURCES + 'filter-playlists.png'
ICO_PLAYLISTS_ACTIVE = RESOURCES + 'filter-playlists-active.png'

# Directory icons
ICO_FOLDER_ROOT = RESOURCES + 'folder-root.png'
ICO_FOLDER_UP = RESOURCES + 'folder-up.png'

# Radio icons
ICO_STATION_ADD = RESOURCES + 'station-add.png'

# Special keyboard icons
ICO_SHIFT = RESOURCES + 'shift_%s.png' % KEY_SIZE_STD
ICO_BACKSPACE = RESOURCES + 'backspace_%s.png' % KEY_SIZE_STD
ICO_ENTER = RESOURCES + 'enter_%s.png' % KEY_SIZE_BIG
ICO_LETTERS = RESOURCES + 'letters_%s.png' % KEY_SIZE_BIG
ICO_SYMBOLS = RESOURCES + 'symbols_%s.png' % KEY_SIZE_BIG

# Standard info icons
ICO_INFO = RESOURCES + 'icon_info.png'
ICO_WARNING = RESOURCES + 'icon_warning.png'
ICO_ERROR = RESOURCES + 'icon_warning.png'

# default covers
DEFAULT_COVER = RESOURCES + 'cover-files.png'
COVER_ART_RADIO = RESOURCES + 'cover-radio.png'
