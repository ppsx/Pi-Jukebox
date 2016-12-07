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


import os
import importlib
import pygame
from pygame.locals import *
from def_colors import *
from def_gestures import *
from resources import *


VERSION = (1, 1, 0)


# dynamically import all visual settings depending on configured screen resolution
# load proper file and update global scope with all variables; the same as for 'from xxx import *'
g = importlib.import_module('{}.r{}'.format(__name__, DISPLAY_RES))
map(lambda x: globals().update({x: g.__dict__[x]}), filter(lambda y: not y.startswith('_'), dir(g)))

DISPLAY_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = map(int, DISPLAY_RES.split('x'))

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

#: Standard font type (needs to be created after pygame.init())
FONT = pygame.font.Font(os.path.join(RESOURCES_DIR, 'LiberationSans-Regular.ttf'), FONT_SIZE)

PYGAME_EVENT_DELAY = 25

if RUN_ON_RASPBERRY_PI:  # If started on Raspberry Pi
    display_flags = FULLSCREEN | DOUBLEBUF | ANYFORMAT  # Turn on video acceleration
    #: Points to the display.
    SCREEN = pygame.display.set_mode(DISPLAY_SIZE, display_flags)
    pygame.mouse.set_visible(False)                                 # Hide mouse cursor
else:
    SCREEN = pygame.display.set_mode(DISPLAY_SIZE)
