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
=======================================================
**screen_radio.py**: MPD radio management
=======================================================

"""
__author__ = 'Mark Zwart'

import sys
import pygame
from pygame.locals import *
import time
import subprocess
import os
import glob
from gui_widgets import *
from pij_screen_navigation import *
from mpd_client import *
from settings import *
from screen_keyboard import *
from screen_settings import *
from config_file import *


class RadioBrowser(ItemList):
    """ The component that displays internet radio stations

        :param screen_rect: The screen rect where the directory browser is drawn on.
    """

    def __init__(self, surface):
        ItemList.__init__(self, 'list_stations', surface,
                          2 * SPACE + ICO_WIDTH, 2 * SPACE + ICO_HEIGHT,
                          SCREEN_WIDTH - 4 * SPACE - ICO_WIDTH - LIST_WIDTH, SCREEN_HEIGHT - ICO_HEIGHT - 3 * SPACE + 2)
        self.outline_visible = False
        self.item_outline_visible = True
        self.font_color = C_GREY_LIGHTEST
        self.item_active_color = C_YELLOW
        self.set_item_alignment(HOR_LEFT, VERT_MID)
        self.radio_stations = []

    def item_selected_get(self):
        return self.radio_stations[self.item_selected_index]

    def station_active_set(self):
        if mpd.radio_mode_get():
            i = 0
            for station in self.radio_stations:
                if station[1] == mpd.now_playing.file:
                    break
                i += 1
            self.active_item_index = i
            self.draw_items()

    def show_stations(self):
        """ Displays all songs or based on the first letter or partial string match.

            :param search: Search string, default = None
            :param only_start: Boolean indicating whether the search string only matches the first letters,
                               default = True
        """
        self.list = []
        self.radio_stations = config_file.radio_stations_get()
        updated = False
        for item in self.radio_stations:
            self.list.append(item[0])
            updated = True
        if updated:
            self.page_showing_index = 0
            self.draw()


class ScreenRadio(Screen):
    """ The screen where the user can browse and add radio station and add those to playlists.

        :param screen_rect: The display's rect where the radio station browser is drawn on.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)
        self.first_time_showing = True
        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.surface, 'btn_radio'))
        # Radio station buttons
        self.add_component(ButtonIcon('btn_station_add', self.surface, ICO_STATION_ADD, 2 * SPACE + ICO_WIDTH, SPACE))
        # Lists
        self.add_component(RadioBrowser(self.surface))

    def show(self):
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        self.components['list_stations'].show_stations()
        return super(ScreenRadio, self).show()

    def update(self):
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        self.components['list_stations'].station_active_set()

    def station_action(self):
        """ Displays screen for follow-up actions when an item was selected from the library. """
        selected = self.components['list_stations'].item_selected_get()
        select_screen = ScreenSelected(self, selected[0], selected[1])
        select_screen.show()
        self.show()

    def on_click(self, x, y):
        """
        :param x: The horizontal click position.
        :param y: The vertical click position.

        :return: Possibly returns a screen index number to switch to.
        """
        tag_name = super(ScreenRadio, self).on_click(x, y)
        if tag_name == 'btn_player':
            self.return_object = 0
            self.close()
        elif tag_name == 'btn_playlist':
            self.return_object = 1
            self.close()
        elif tag_name == 'btn_library':
            self.return_object = 2
            self.close()
        elif tag_name == 'btn_directory':
            self.return_object = 3
            self.close()
        elif tag_name == 'btn_radio':
            self.return_object = 4
            self.close()
        elif tag_name == 'btn_station_add':
            screen_add = ScreenStation(self)
            screen_add.show()
            self.show()
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self)
            setting_screen.show()
            self.show()
        elif tag_name == 'list_stations':
            self.station_action()


class ScreenSelected(ScreenModal):
    """ Screen for selecting playback actions with a selected radio station.

        :param screen_rect: The directory's rect where the library browser is drawn on.
        :param station_name: The name of the selected radio station.
        :param station_URL: The URL of the selected radio station.
    """

    def __init__(self, screen, station_name, station_URL):
        ScreenModal.__init__(self, screen, station_name)
        self.station_name = station_name
        self.station_URL = station_URL
        self.title_color = C_BLUE
        self.initialize()
        self.return_type = ""

    def initialize(self):
        """ Set-up screen controls. """
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE

        label = _("Tune in")
        self.add_component(
            ButtonText('btn_tune_in', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_tune_in'].font_color = C_GREEN
        self.components['btn_tune_in'].outline_color = C_GREEN

        label = _("Edit")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_edit', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Remove")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_remove', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Cancel")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_cancel', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

    def on_click(self, x, y):
        """ Action that should be performed on a click. """
        tag_name = super(ScreenModal, self).on_click(x, y)
        play = False
        clear_playlist = False
        if tag_name == 'btn_edit':
            screen_edit = ScreenStation(self, self.station_name)
            screen_edit.show()
            self.close()
        elif tag_name == 'btn_remove':
            screen_yes_no = ScreenYesNo(self, _("Remove {0}").format(self.station_name),
                _("Are you sure you want to remove {0}?").format(self.station_name))
            if screen_yes_no.show() == 'yes':
                config_file.setting_remove('Radio stations', self.station_name)
            self.close()
        if tag_name == 'btn_tune_in':
            mpd.radio_station_start(self.station_URL)
        self.close()


class ScreenStation(ScreenModal):
    """ Screen for selecting playback actions with a selected radio station.

        :param screen_rect: The directory's rect where the library browser is drawn on.
        :param station_name: The name of the selected radio station.
        :param station_URL: The URL of the selected radio station.
    """
    def __init__(self, screen_rect, station_name=""):
        ScreenModal.__init__(self, screen_rect, station_name)
        self.title_color = C_BLUE
        self.window_x = 20
        self.window_y = 60
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True
        self.station_name = station_name
        btn_name_label = ""
        btn_URL_label = ""
        if station_name == "":
            ScreenModal.__init__(self, screen_rect, _("Add a radio station"))
            self.station_URL = ""
            btn_name_label = _("Set station name")
            btn_URL_label = _("Set station URL")
        else:
            ScreenModal.__init__(self, screen_rect, _("Edit radio station"))
            self.station_URL = config_file.setting_get('Radio stations', self.station_name)
            btn_name_label = _("Change name {0}").format(self.station_name)
            btn_URL_label = _("Change station URL")

        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE
        self.add_component(
            ButtonText('btn_name', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, btn_name_label))
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_URL', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, btn_URL_label))

        label = _("Cancel")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_cancel', self.surface, button_left, button_top, KEY_WIDTH_HUGE, BUTTON_HEIGHT, label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

        label = _("Ok")
        self.add_component(ButtonText('btn_ok', self.surface,
                                      self.window_x + self.window_width - KEY_WIDTH_HUGE - SPACE, button_top,
                                      KEY_WIDTH_HUGE, BUTTON_HEIGHT, label))
        self.components['btn_ok'].font_color = C_GREEN
        self.components['btn_ok'].outline_color = C_GREEN

    def update(self):
        """ Set-up screen controls. """
        if self.station_name == "":
            self.components['btn_name'].draw(_("Set station name"))
        else:
            self.components['btn_name'].draw(_("Change name {0}").format(self.station_name))
        if self.station_URL == "":
            self.components['btn_URL'].draw(_("Set station URL"))
        else:
            self.components['btn_URL'].draw(_("Change station URL"))
        self.show()

    def on_click(self, x, y):
        """ Action that should be performed on a click. """
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_name':
            keyboard = Keyboard(self.surface, _("Set station name"), self.station_name)
            self.station_name = keyboard.show()
            self.update()
            self.show()
        elif tag_name == 'btn_URL':
            keyboard = Keyboard(self.surface, _("Set station URL"), self.station_URL)
            keyboard.title_color = C_BLUE
            self.station_URL = keyboard.show()
            self.update()
            self.show()
        elif tag_name == 'btn_cancel':
            self.close()
        elif tag_name == 'btn_ok':
            if self.station_name != "" and self.station_URL != "":
                config_file.setting_set('Radio stations', self.station_name, self.station_URL)
            self.close()
