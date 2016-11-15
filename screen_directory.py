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
**screen_directory.py**: MPD Directory browsing screen
=======================================================

"""
__author__ = 'Mark Zwart'

from gui_screens import *
from pij_screen_navigation import ScreenNavigation
from screen_settings import ScreenSettings
from mpd_client import mpd
from settings import *


class LetterBrowser(ItemList):
    """ The graphical control for selecting artists/albums/songs starting with a letter.

        :param screen_rect: The screen rect where the library browser is drawn on.
    """

    def __init__(self, surface):
        ItemList.__init__(self, 'list_letters', surface,
                          SCREEN_WIDTH - SPACE - LIST_WIDTH, 2 * SPACE + ICO_HEIGHT,
                          LIST_WIDTH, SCREEN_HEIGHT - ICO_HEIGHT - 3 * SPACE + 2)
        self.item_outline_visible = True
        self.outline_visible = False
        self.font_color = C_GREY_LIGHTEST
        self.set_item_alignment(HOR_MID, VERT_MID)
        self.list = []
        # self.list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"\
        # , "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" \
        #                , "0", "1", "2", "3", "4", "5", "7", "8", "9"]


class DirectoryBrowser(ItemList):
    """ The component that displays mpd directory entries.

        :param screen_rect: The screen rect where the directory browser is drawn on.
    """

    def __init__(self, surface):
        ItemList.__init__(self, 'list_directory', surface,
                          2 * SPACE + ICO_WIDTH, 2 * SPACE + ICO_HEIGHT,
                          SCREEN_WIDTH - ICO_WIDTH - LIST_WIDTH - 4 * SPACE, SCREEN_HEIGHT - ICO_HEIGHT - 3 * SPACE)
        self.outline_visible = False
        self.item_outline_visible = True
        self.font_color = C_GREY_LIGHTEST
        self.set_item_alignment(HOR_LEFT, VERT_MID)
        self.directory_current = "/"
        self.directory_content = []

    def item_selected_get(self):
        return self.directory_content[self.item_selected_index]

    def show_directory(self, path="", first_letter=None):
        """ Displays all songs or based on the first letter or partial string match.

            :param search: Search string, default = None
            :param only_start: Boolean indicating whether the search string only matches the first letters,
                               default = True
        """
        self.list = []
        if first_letter is None:
            self.directory_current = path
        self.directory_content = mpd.directory_list(self.directory_current)
        if first_letter:
            self.directory_content = [(elem_type, elem_name) for elem_type, elem_name in self.directory_content \
                                      if os.path.basename(elem_name).startswith(first_letter)]
        updated = False
        for item in self.directory_content:
            index = item[1].rfind("/")
            if index == -1:
                self.list.append(item[1])
            else:
                self.list.append(item[1][index + 1:])
            updated = True
        if updated:
            self.page_showing_index = 0
            self.first_letters_in_result_get()
            self.draw()

    def show_directory_up(self):
        index = self.directory_current.rfind("/")
        if index == -1:
            self.show_directory("")
        else:
            directory_up = self.directory_current[:index]
            self.show_directory(directory_up)

    def first_letters_in_result_get(self):
        """ Get's the symbols that are first letters of the items in the result list.

            :return: List of letters
        """
        output_set = set()
        for elem in self.list:
            first_letter = elem[:1].upper()
            output_set.add(first_letter)
        letter_list = list(output_set)
        letter_list.sort(key=lambda item: (
            [str, int].index(type(item)), item))  # Sorting, making sure letters are put before numbers
        return letter_list


class ScreenDirectory(Screen):
    """ The screen where the user can browse in the MPD database and playlist_add items to playlists.

        :param screen_rect: The display's rect where the library browser is drawn on.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)
        self.first_time_showing = True
        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.surface, 'btn_directory'))
        # Directory buttons
        button_left = ICO_WIDTH + 2 * SPACE
        self.add_component(ButtonIcon('btn_root', self.surface, ICO_FOLDER_ROOT, button_left, SPACE))
        button_left += ICO_WIDTH + SPACE
        self.add_component(ButtonIcon('btn_up', self.surface, ICO_FOLDER_UP, button_left, SPACE))
        # Lists
        self.add_component(DirectoryBrowser(self.surface))
        self.add_component(LetterBrowser(self.surface))

    def show(self):
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        if self.first_time_showing:
            self.components['list_directory'].show_directory()
            self.letter_list_update()
            self.first_time_showing = False
        return super(ScreenDirectory, self).show()

    def update(self):
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())

    def letter_list_update(self):
        self.components['list_letters'].list = self.components['list_directory'].first_letters_in_result_get()
        self.components['list_letters'].draw()

    def find_first_letter(self):
        """ Adjust current search type according to the letter clicked in the letter list. """
        letter = self.components['list_letters'].item_selected_get()
        self.components['list_directory'].show_directory(first_letter=letter)
        self.letter_list_update()

    def on_click(self, x, y):
        """ Handles click event. """
        tag_name = super(ScreenDirectory, self).on_click(x, y)
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
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self)
            setting_screen.show()
            self.show()
        elif tag_name == 'list_letters':
            self.find_first_letter()
        elif tag_name == 'list_directory':
            self.list_item_action()
        elif tag_name == 'btn_root':
            self.components['list_directory'].show_directory("")
            self.letter_list_update()
        elif tag_name == 'btn_up':
            self.components['list_directory'].show_directory_up()
            self.letter_list_update()

    def list_item_action(self):
        """ Displays screen for follow-up actions when an item was selected from the library. """
        selected = self.components['list_directory'].item_selected_get()
        cur_dir = self.components['list_directory'].directory_current
        select_screen = ScreenSelected(self, cur_dir, selected[0], selected[1])
        select_screen.show()
        if isinstance(select_screen.return_object, list):
            self.components['list_directory'].show_directory(select_screen.selected_name)
        self.letter_list_update()
        self.show()


class ScreenSelected(ScreenModal):
    """ Screen for selecting playback actions with an item selected from the directory.

        :param screen_rect: The directory's rect where the library browser is drawn on.
        :param directory: The directory who's content iss currently being listed.
        :param selected_type: The selected directory item ['file', 'directory'].
        :param selected_item: The name of the selected directory item.
    """

    def __init__(self, screen, directory, selected_type, selected_item):
        ScreenModal.__init__(self, screen, selected_item, C_BLUE)
        self.directory_current = directory
        self.selected_type = selected_type
        self.selected_name = selected_item
        self.font_color = C_GREY_DARK
        self.initialize()
        self.return_type = ""

    def initialize(self):
        """ Set-up screen controls. """
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE

        if self.selected_type == 'directory':
            # label = _("Browse directory {0}").format(self.selected_name)  # name removed because of its potential length
            label = _("Browse directory")
            self.add_component(
                ButtonText('btn_browse', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
            button_top += SPACE + BUTTON_HEIGHT

        label = _("Add to playlist")
        self.add_component(
            ButtonText('btn_add', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_add'].font_color = C_GREEN
        self.components['btn_add'].outline_color = C_GREEN

        label = _("Add to playlist and play")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_add_play', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_add_play'].font_color = C_GREEN
        self.components['btn_add_play'].outline_color = C_GREEN

        label = _("Replace playlist and play")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_replace', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_replace'].font_color = C_GREEN
        self.components['btn_replace'].outline_color = C_GREEN

        label = _("Cancel")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(ButtonText('btn_cancel', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT,
                                      label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

    def on_click(self, x, y):
        """ Action that should be performed on a click. """
        tag_name = super(ScreenModal, self).on_click(x, y)
        play = False
        clear_playlist = False

        if tag_name == 'btn_browse':
            self.return_object = mpd.directory_list(self.selected_name)
        elif tag_name == 'btn_add_play':
            play = True
        elif tag_name == 'btn_replace':
            play = True
            clear_playlist = True
        if tag_name == 'btn_add' or tag_name == 'btn_add_play' or tag_name == 'btn_replace':
            if self.selected_type == 'directory':
                mpd.playlist_add_directory(self.selected_name, play, clear_playlist)
            elif self.selected_type == 'file':
                mpd.playlist_add_file(self.selected_name, play, clear_playlist)
            self.return_object = None
        self.close()

