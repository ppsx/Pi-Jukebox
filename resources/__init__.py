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


import zipfile
from os import path
from config_file import config_file


DISPLAY_TYPE = config_file.setting_get('Hardware', 'display')
DISPLAY_RES = config_file.setting_get(DISPLAY_TYPE, 'resolution')
FONT_SIZE = int(config_file.setting_get(DISPLAY_TYPE, 'font size'))

#: The directory where resources like button icons or the font file is stored.
RESOURCES_DIR = path.dirname(__file__)
RESOURCES_ZIP = path.join(RESOURCES_DIR, 'resources.zip')

# icons handling (from zip file)
with zipfile.ZipFile(RESOURCES_ZIP) as z:
    # get list of all icons from zip file for specific resolution (full path)
    _all_files = filter(lambda x: x.startswith(DISPLAY_RES) and x.endswith('.png'), z.namelist())

    # transformation function: filename -> variable name ('800x480/cover-files.png' -> 'ICO_COVER_FILES'
    # be careful while adding/replacing files in zip: filenames really DO matter!
    def create_variable_name(pth):
        return 'ICO_' + path.basename(path.splitext(pth)[0]).replace('-', '_').upper()

    # update global scope (unfortunately...) with newly created variables
    map(lambda x: globals().update({ create_variable_name(x): x }), _all_files)
