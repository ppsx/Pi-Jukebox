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


from gui_widgets import *


class ScreenNavigation(WidgetContainer):
    def __init__(self, tag_name, surface, button_active):
        WidgetContainer.__init__(self, tag_name, surface, 0, 0, ICO_WIDTH + SPACE, SCREEN_HEIGHT)
        self.__radio_mode = False
        self.__button_active = button_active
        button_top = SPACE
        self.add_component(ButtonIcon('btn_player', self.surface, ICO_MAIN_PLAYING_FILE_ACTIVE, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_playlist', self.surface, ICO_MAIN_PLAYLIST, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_library', self.surface, ICO_MAIN_LIBRARY, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_directory', self.surface, ICO_MAIN_DIRECTORY, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_radio', self.surface, ICO_MAIN_RADIO, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_settings', self.surface, ICO_MAIN_SETTINGS, SPACE, button_top))
        self.button_active_set(button_active)

    def on_click(self, x, y):
        tag_name = super(ScreenNavigation, self).on_click(x, y)
        return tag_name

    def radio_mode_set(self, radio_mode_bool):
        self.__radio_mode = radio_mode_bool
        if radio_mode_bool:
            if self.__button_active == 'btn_player':
                self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_RADIO_ACTIVE)
            else:
                self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_RADIO)
        else:
            if self.__button_active == 'btn_player':
                self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_FILE_ACTIVE)
            else:
                self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_FILE)
        self.draw()

    def button_active_set(self, button_active):
        self.__button_active = button_active
        if self.__radio_mode:
            self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_RADIO)
        else:
            self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_FILE)
        self.components['btn_playlist'].icon_file_set(ICO_MAIN_PLAYLIST)
        self.components['btn_library'].icon_file_set(ICO_MAIN_LIBRARY)
        self.components['btn_directory'].icon_file_set(ICO_MAIN_DIRECTORY)
        self.components['btn_radio'].icon_file_set(ICO_MAIN_RADIO)

        if button_active == 'btn_player':
            if self.__radio_mode:
                self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_RADIO_ACTIVE)
            else:
                self.components['btn_player'].icon_file_set(ICO_MAIN_PLAYING_FILE_ACTIVE)
        elif button_active == 'btn_playlist':
            self.components['btn_playlist'].icon_file_set(ICO_MAIN_PLAYLIST_ACTIVE)
        elif button_active == 'btn_library':
            self.components['btn_library'].icon_file_set(ICO_MAIN_LIBRARY_ACTIVE)
        elif button_active == 'btn_directory':
            self.components['btn_directory'].icon_file_set(ICO_MAIN_DIRECTORY_ACTIVE)
        elif button_active == 'btn_radio':
            self.components['btn_radio'].icon_file_set(ICO_MAIN_RADIO_ACTIVE)

        self.draw()
