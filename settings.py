# This file is part of pi-jukebox.
#
# pi-jukebox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pi-jukebox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pi-jukebox. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2015- by Mark Zwart, <mark.zwart@pobox.com>

"""

================================================
**settings.py**: Contains project wide variables
================================================

"""
__author__ = 'Mark Zwart'

import os
import pygame
from pygame.locals import *
from config_file import config_file


VERSION = (1, 1, 0)


#: The display dimensions, change this if you have a bigger touch screen.
#: adafruit 2.8" -> 320x240
#: adafruit 3.5" -> 480x320
#: raspberry 7" -> 800x480
DISPLAY_TYPE = config_file.setting_get('Hardware', 'display')
DISPLAY_RES = config_file.setting_get(DISPLAY_TYPE, 'resolution')
DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = map(int, DISPLAY_RES.split('x'))


if DISPLAY_RES == '800x480':
    FONT_SIZE = 28
    SPACE = 14
    KEY_SPACE = 4
    KEY_HEIGHT = 42
    KEY_WIDTH_STD = 42
    KEY_WIDTH_BIG = 64
    KEY_WIDTH_HUGE = 96
    BUTTON_HEIGHT = 64
    ICO_WIDTH = 96
    ICO_HEIGHT = 64
    ICO_INFO_WIDTH = 48
    SWITCH_WIDTH = 48
    SWITCH_HEIGHT = 48
    LIST_WIDTH = 52
    LIST_INDICATOR_WIDTH = 10
    SLIDER_HEIGHT = 64
elif DISPLAY_RES == '480x320':
    FONT_SIZE = 22
    SPACE = 10
    KEY_SPACE = 4
    KEY_HEIGHT = 42
    KEY_WIDTH_STD = 42
    KEY_WIDTH_BIG = 64
    KEY_WIDTH_HUGE = 96
    BUTTON_HEIGHT = 42
    ICO_WIDTH = 64
    ICO_HEIGHT = 42
    ICO_INFO_WIDTH = 48
    SWITCH_WIDTH = 32
    SWITCH_HEIGHT = 32
    LIST_WIDTH = 42
    LIST_INDICATOR_WIDTH = 6
    SLIDER_HEIGHT = 42
else:   # 320x240
    FONT_SIZE = 16
    SPACE = 4
    KEY_SPACE = 3
    KEY_HEIGHT = 32
    KEY_WIDTH_STD = 28
    KEY_WIDTH_BIG = 48
    KEY_WIDTH_HUGE = 64
    BUTTON_HEIGHT = 32
    ICO_WIDTH = 48
    ICO_HEIGHT = 32
    ICO_INFO_WIDTH = 48
    SWITCH_WIDTH = 32
    SWITCH_HEIGHT = 32
    LIST_WIDTH = 42
    LIST_INDICATOR_WIDTH = 6
    SLIDER_HEIGHT = 20

TITLE_HEIGHT = int(FONT_SIZE * 1.4)
FONT_SPACE = int(FONT_SIZE * 1.2)
BUTTON_TOP = TITLE_HEIGHT

#: Switches between development/debugging on your desktop/laptop versus running on your Raspberry Pi
RUN_ON_RASPBERRY_PI = (os.name != 'nt' and os.uname()[4][:3] == 'arm')

# Setting up touch screen, set if statement to true on Raspberry Pi
if RUN_ON_RASPBERRY_PI:
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'
    os.environ['SDL_FBDEV'] = '/dev/fb1'
    if DISPLAY_TYPE == 'raspberry7':
        os.environ['SDL_MOUSEDEV'] = '/dev/input/mouse1'
        os.environ['SDL_MOUSEDRV'] = 'FT5406'
    else:
        os.environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
        os.environ['SDL_MOUSEDRV'] = 'TSLIB'

# Display settings
pygame.init()  # Pygame initialization

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
ICO_SWITCH_ON = DISPLAY_RES + '/switch-on.png'
ICO_SWITCH_OFF = DISPLAY_RES + '/switch-off.png'

# General icons
ICO_PLAYER_FILE = DISPLAY_RES + '/main-playing-file.png'
ICO_PLAYER_FILE_ACTIVE = DISPLAY_RES + '/main-playing-file-active.png'
ICO_PLAYER_RADIO = DISPLAY_RES + '/main-playing-radio.png'
ICO_PLAYER_RADIO_ACTIVE = DISPLAY_RES + '/main-playing-radio-active.png'
ICO_PLAYLIST = DISPLAY_RES + '/main-playlist.png'
ICO_PLAYLIST_ACTIVE = DISPLAY_RES + '/main-playlist-active.png'
ICO_LIBRARY = DISPLAY_RES + '/main-library.png'
ICO_LIBRARY_ACTIVE = DISPLAY_RES + '/main-library-active.png'
ICO_DIRECTORY = DISPLAY_RES + '/main-directory.png'
ICO_DIRECTORY_ACTIVE = DISPLAY_RES + '/main-directory-active.png'
ICO_RADIO = DISPLAY_RES + '/main-radio.png'
ICO_RADIO_ACTIVE = DISPLAY_RES + '/main-radio-active.png'
ICO_SETTINGS = DISPLAY_RES + '/main-settings.png'

# Player icons
ICO_PLAY = DISPLAY_RES + '/controller-play.png'
ICO_PAUSE = DISPLAY_RES + '/controller-pause.png'
ICO_STOP = DISPLAY_RES + '/controller-stop.png'
ICO_NEXT = DISPLAY_RES + '/controller-next.png'
ICO_PREVIOUS = DISPLAY_RES + '/controller-previous.png'
ICO_VOLUME = DISPLAY_RES + '/controller-volume.png'

# Volume icons
ICO_VOLUME_UP = DISPLAY_RES + '/volume-up.png'
ICO_VOLUME_DOWN = DISPLAY_RES + '/volume-down.png'
ICO_VOLUME_MUTE = DISPLAY_RES + '/volume-mute.png'
ICO_VOLUME_MUTE_ACTIVE = DISPLAY_RES + '/volume-mute-active.png'

# Library icons
ICO_SEARCH = DISPLAY_RES + '/filter-search.png'
ICO_SEARCH_ARTIST = DISPLAY_RES + '/filter-artists.png'
ICO_SEARCH_ARTIST_ACTIVE = DISPLAY_RES + '/filter-artists-active.png'
ICO_SEARCH_ALBUM = DISPLAY_RES + '/filter-albums.png'
ICO_SEARCH_ALBUM_ACTIVE = DISPLAY_RES + '/filter-albums-active.png'
ICO_SEARCH_SONG = DISPLAY_RES + '/filter-songs.png'
ICO_SEARCH_SONG_ACTIVE = DISPLAY_RES + '/filter-songs-active.png'
ICO_PLAYLISTS = DISPLAY_RES + '/filter-playlists.png'
ICO_PLAYLISTS_ACTIVE = DISPLAY_RES + '/filter-playlists-active.png'

# Directory icons
ICO_FOLDER_ROOT = DISPLAY_RES + '/folder-root.png'
ICO_FOLDER_UP = DISPLAY_RES + '/folder-up.png'

# Standard info icons
ICO_INFO = DISPLAY_RES + '/icon-info.png'
ICO_WARNING = DISPLAY_RES + '/icon-warning.png'
ICO_ERROR = DISPLAY_RES + '/icon-error.png'

# Radio icons
ICO_STATION_ADD = DISPLAY_RES + '/station-add.png'

# default covers
DEFAULT_COVER = DISPLAY_RES + '/cover-files.png'
COVER_ART_RADIO = DISPLAY_RES + '/cover-radio.png'

# Special keyboard icons
ICO_SHIFT = DISPLAY_RES + '/keys-shift.png'
ICO_BACKSPACE = DISPLAY_RES + '/keys-backspace.png'
ICO_ENTER = DISPLAY_RES + '/keys-enter.png'
ICO_LETTERS = DISPLAY_RES + '/keys-letters.png'
ICO_SYMBOLS = DISPLAY_RES + '/keys-symbols.png'
