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


from gui_screens import *
from pij_screen_navigation import ScreenNavigation
from screen_settings import ScreenSettings
from screen_keyboard import Keyboard
from mpd_client import mpd
from settings import *
from gettext import gettext as _


class LetterBrowser(ItemList):
    """ The graphical control for selecting artists/albums/songs starting with a letter.

        :param surface: The screen rect where the library browser is drawn on.
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
        # self.background_color = C_GREY_DARK


class LibraryBrowser(ItemList):
    """ The component that displays mpd library entries.

        :param surface: The screen rect where the library browser is drawn on.
    """
    def __init__(self, surface):
        ItemList.__init__(self, 'list_library', surface,
                          2 * SPACE + ICO_WIDTH, 2 * SPACE + ICO_HEIGHT,
                          SCREEN_WIDTH - ICO_WIDTH - LIST_WIDTH - 4 * SPACE, SCREEN_HEIGHT - ICO_HEIGHT - 3 * SPACE + 2)
        self.outline_visible = False
        self.item_outline_visible = True
        self.font_color = C_GREY_LIGHTEST
        self.set_item_alignment(HOR_LEFT, VERT_MID)

    def show_artists(self, search=None, only_start=True):
        """ Displays all artists or based on the first letter or partial string match.

            :param search: Search string, default = None
            :param only_start: Boolean indicating whether the search string only matches the first letters,
                               default = True
        """
        updated = False
        if self.list != mpd.artists_get(search, only_start):
            self.list = mpd.artists_get(search, only_start)
            updated = True
        if updated:
            self.page_showing_index = 0
            self.draw()

    def show_albums(self, search=None, only_start=True):
        """ Displays all albums or based on the first letter or partial string match.

            :param search: Search string, default = None
            :param only_start: Boolean indicating whether the search string only matches the first letters,
                               default = True
        """
        updated = False
        if self.list != mpd.albums_get(search, only_start):
            self.list = mpd.albums_get(search, only_start)
            updated = True
        if updated:
            self.page_showing_index = 0
            self.draw()

    def show_songs(self, search=None, only_start=True):
        """ Displays all songs or based on the first letter or partial string match.

            :param search: Search string, default = None
            :param only_start: Boolean indicating whether the search string only matches the first letters,
                               default = True
        """
        updated = False
        if self.list != mpd.songs_get(search, only_start):
            self.list = mpd.songs_get(search, only_start)
            updated = True
        if updated:
            self.page_showing_index = 0
            self.draw()

    def show_playlists(self, first_letter=None):
        """ Displays all playlists or based on the first letter.

            :param first_letter: Search string, default = None
        """
        updated = False
        if self.list != mpd.playlists_get(first_letter):
            self.list = mpd.playlists_get(first_letter)
            updated = True
        if updated:
            self.page_showing_index = 0
            self.draw()

    def first_letters_in_result_get(self):
        """ Get's the symbols that are first letters of the items in the result list.

            :return: List of letters
        """
        output_set = set()
        for elem in self.list:
            first_letter = elem[:1].upper()
            output_set.add(first_letter)
        letter_list = list(output_set)
        # Sorting, making sure letters are put before numbers
        letter_list.sort(key=lambda item: ([str, int].index(type(item)), item))
        return letter_list


class ScreenLibrary(Screen):
    """ The screen where the user can browse in the MPD database and playlist_add items to playlists.

        :param screen_rect: The display's rect wehere the library browser is drawn on.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)
        self.first_time_showing = True

        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.surface, 'btn_library'))

        # Library buttons
        button_left = ICO_WIDTH + 2 * SPACE
        self.add_component(ButtonIcon('btn_artists', self.surface, ICO_FILTER_ARTISTS, button_left, SPACE))
        button_left += ICO_WIDTH + SPACE
        self.add_component(ButtonIcon('btn_albums', self.surface, ICO_FILTER_ALBUMS, button_left, SPACE))
        button_left += ICO_WIDTH + SPACE
        self.add_component(ButtonIcon('btn_songs', self.surface, ICO_FILTER_SONGS, button_left, SPACE))
        button_left += ICO_WIDTH + SPACE
        self.add_component(ButtonIcon('btn_playlists', self.surface, ICO_FILTER_PLAYLISTS, button_left, SPACE))
        button_left += ICO_WIDTH + SPACE
        self.add_component(ButtonIcon('btn_search', self.surface, ICO_FILTER_SEARCH, button_left, SPACE))

        # Lists
        self.add_component(LibraryBrowser(self.surface))
        self.add_component(LetterBrowser(self.surface))

        self.currently_showing = 'artists'

    def show(self):
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        if self.first_time_showing:
            self.set_currently_showing('artists')
            self.components['list_library'].show_artists()
            self.letter_list_update()
            self.first_time_showing = False
        return super(ScreenLibrary, self).show()

    def update(self):
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())

    def set_currently_showing(self, type_showing):
        """ Switch icons to active dependent on which kind of searching is active.

            :param type_showing: The type of search results showing [artists, albums, songs, playlists].
        """
        self.currently_showing = type_showing
        if type_showing == 'artists':
            self.components['btn_artists'].set_image_file(ICO_FILTER_ARTISTS_ACTIVE)
            self.components['btn_albums'].set_image_file(ICO_FILTER_ALBUMS)
            self.components['btn_songs'].set_image_file(ICO_FILTER_SONGS)
            self.components['btn_playlists'].set_image_file(ICO_FILTER_PLAYLISTS)
        elif type_showing == 'albums':
            self.components['btn_artists'].set_image_file(ICO_FILTER_ARTISTS)
            self.components['btn_albums'].set_image_file(ICO_FILTER_ALBUMS_ACTIVE)
            self.components['btn_songs'].set_image_file(ICO_FILTER_SONGS)
            self.components['btn_playlists'].set_image_file(ICO_FILTER_PLAYLISTS)
        elif type_showing == 'songs':
            self.components['btn_artists'].set_image_file(ICO_FILTER_ARTISTS)
            self.components['btn_albums'].set_image_file(ICO_FILTER_ALBUMS)
            self.components['btn_songs'].set_image_file(ICO_FILTER_SONGS_ACTIVE)
            self.components['btn_playlists'].set_image_file(ICO_FILTER_PLAYLISTS)
        elif type_showing == 'playlists':
            self.components['btn_artists'].set_image_file(ICO_FILTER_ARTISTS)
            self.components['btn_albums'].set_image_file(ICO_FILTER_ALBUMS)
            self.components['btn_songs'].set_image_file(ICO_FILTER_SONGS)
            self.components['btn_playlists'].set_image_file(ICO_FILTER_PLAYLISTS_ACTIVE)

    def letter_list_update(self):
        self.components['list_letters'].list = self.components['list_library'].first_letters_in_result_get()
        self.components['list_letters'].draw()

    def find_first_letter(self):
        """ Adjust current search type according to the letter clicked in the letter list. """
        letter = self.components['list_letters'].item_selected_get()
        if self.currently_showing == 'artists':
            self.components['list_library'].show_artists(letter)
        elif self.currently_showing == 'albums':
            self.components['list_library'].show_albums(letter)
        elif self.currently_showing == 'songs':
            self.components['list_library'].show_songs(letter)
        elif self.currently_showing == 'playlists':
            self.components['list_library'].show_playlists(letter)
        self.letter_list_update()

    def find_text(self):
        """ Find results according to part of the text.
            Launching a keyboard so that the user can specify the search string.
        """
        screen_search = ScreenSearch(self)  # The search screen
        screen_search.show()
        search_text = screen_search.search_text  # The text the user searches for
        search_type = screen_search.search_type  # The type of tag the user searches for (artist, album, song)
        if search_type == 'artist':
            self.components['list_library'].show_artists(search_text, False)
            self.set_currently_showing('artists')
        elif search_type == 'album':
            self.components['list_library'].show_albums(search_text, False)
            self.set_currently_showing('albums')
        elif search_type == 'song':
            self.components['list_library'].show_songs(search_text, False)
            self.set_currently_showing('songs')
        self.letter_list_update()
        self.show()

    def playlist_action(self):
        """ Displays screen for follow-up actions when an item was selected from the library. """
        selected = self.components['list_library'].item_selected_get()
        if selected:
            select_screen = ScreenSelected(self, self.currently_showing, selected)
            select_screen.show()
            if isinstance(select_screen.return_object, list):
                self.components['list_library'].list = select_screen.return_object
                self.components['list_library'].draw()
                self.set_currently_showing(select_screen.return_type)
        self.letter_list_update()
        self.show()

    def on_click(self, x, y):
        """ Handles click event. """
        tag_name = super(ScreenLibrary, self).on_click(x, y)
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
        elif tag_name == 'btn_artists':
            self.set_currently_showing('artists')
            self.components['list_library'].show_artists()
            self.letter_list_update()
        elif tag_name == 'btn_albums':
            self.set_currently_showing('albums')
            self.components['list_library'].show_albums()
            self.letter_list_update()
        elif tag_name == 'btn_songs':
            self.set_currently_showing('songs')
            self.components['list_library'].show_songs()
            self.letter_list_update()
        elif tag_name == 'btn_playlists':
            self.set_currently_showing('playlists')
            self.components['list_library'].show_playlists()
            self.letter_list_update()
        elif tag_name == 'btn_search':
            self.find_text()
        elif tag_name == 'list_letters':
            self.find_first_letter()
        elif tag_name == 'list_library':
            self.playlist_action()


class ScreenSearch(ScreenModal):
    """ Screen used further searching based on an item selected from the library

        :param screen: The display's rect where the library browser is drawn on.

        :ivar search_type: Searching for... [artist, album, song].
        :ivar search_text: Partial text which should be searched for
    """

    def __init__(self, screen):
        ScreenModal.__init__(self, screen, _("Search library for..."), C_BLUE)
        self.font_color = C_GREY_DARK
        self.search_type = ""
        self.search_text = ""
        self.initialize()

    def initialize(self):
        """ Set-up screen controls. """
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left

        label = _("Artists")
        button_top = TITLE_HEIGHT + SPACE
        self.add_component(
            ButtonText('btn_artists', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Albums")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_albums', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Songs")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_songs', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Cancel")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_cancel', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

    def on_click(self, x, y):
        """ Action that should be performed on a click. """
        tag_name = super(ScreenModal, self).on_click(x, y)
        search_label = tag_name
        if tag_name == 'btn_cancel':
            self.close()
            return
        elif tag_name == 'btn_artists':
            self.search_type = 'artist'
            search_label = _("Search artists")
        elif tag_name == 'btn_albums':
            self.search_type = 'album'
            search_label = _("Search albums")
        elif tag_name == 'btn_songs':
            self.search_type = 'song'
            search_label = _("Search songs")
        # Open on-screen keyboard for entering search string
        keyboard = Keyboard(self, search_label)
        self.search_text = keyboard.show()  # Get entered search text
        self.close()


class ScreenSelected(ScreenModal):
    """ Screen for selecting playback actions with an item selected from the library.

        :param screen: The display's rect where the library browser is drawn on.
        :param selected_type: The selected library item [artists, albums, songs].
        :param selected_title: The title of the selected library item.
    """

    def __init__(self, screen, selected_type, selected_title):
        ScreenModal.__init__(self, screen, selected_title, C_BLUE)
        self.type = selected_type
        self.selected = selected_title
        self.font_color = C_GREY_DARK
        self.initialize()
        self.return_type = ""

    def initialize(self):
        """ Set-up screen controls. """
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left

        label = _("Add to playlist")
        button_top = TITLE_HEIGHT + SPACE
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

        if self.type == 'artists':
            label = _("Albums of ...")
            # label = _("Albums of {0}").format(self.title)
            button_top += SPACE + BUTTON_HEIGHT
            button_width_2 = int((button_width - SPACE) / 2)
            self.add_component(
                    ButtonText('btn_artist_get_albums', self.surface, button_left, button_top,
                               button_width_2, BUTTON_HEIGHT, label))

            label = _("Songs of ...")
            # button_top += SPACE + BUTTON_HEIGHT
            self.add_component(
                    ButtonText('btn_artist_get_songs', self.surface, button_left + button_width_2 + SPACE,
                               button_top, button_width_2, BUTTON_HEIGHT, label))
        elif self.type == 'albums':
            label = _("Songs of ...")
            button_top += SPACE + BUTTON_HEIGHT
            self.add_component(
                    ButtonText('btn_album_get_songs', self.surface, button_left, button_top,
                               button_width, BUTTON_HEIGHT, label))

        # TODO: Should the Cancel button be removed?
        label = _("Cancel")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText("btn_cancel", self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

    def on_click(self, x, y):
        """ Action that should be performed on a click. """
        play = False
        clear_playlist = False
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_add_play':
            play = True
        elif tag_name == 'btn_replace':
            play = True
            clear_playlist = True
        if tag_name == 'btn_add' or tag_name == 'btn_add_play' or tag_name == 'btn_replace':
            if self.type == 'artists':
                mpd.playlist_add_artist(self.selected, play, clear_playlist)
            elif self.type == 'albums':
                mpd.playlist_add_album(self.selected, play, clear_playlist)
            elif self.type == 'songs':
                mpd.playlist_add_song(self.selected, play, clear_playlist)
            elif self.type == 'playlists':
                mpd.playlist_add_playlist(self.selected, play, clear_playlist)
            self.return_object = None
        elif tag_name == 'btn_artist_get_albums':
            self.return_object = mpd.artist_albums_get(self.selected)
            self.return_type = 'albums'
            self.close()
        elif tag_name == 'btn_artist_get_songs':
            self.return_object = mpd.artist_songs_get(self.selected)
            self.return_type = 'songs'
            self.close()
        elif tag_name == 'btn_album_get_songs':
            self.return_object = mpd.album_songs_get(self.selected)
            self.return_type = 'songs'
            self.close()
        self.close()
