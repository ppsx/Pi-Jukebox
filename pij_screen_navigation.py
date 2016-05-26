"""
=======================================================
**screen_directory.py**: MPD Directory browsing screen
=======================================================
"""


# from settings import *
# from gui_screens import *
# from gui_widgets import *
from screen_settings import *


__author__ = 'Mark Zwart'


class ScreenNavigation(WidgetContainer):
    def __init__(self, tag_name, screen_rect, button_active):
        self.__button_active = button_active
        WidgetContainer.__init__(self, tag_name, screen_rect, 0, 0, ICO_WIDTH + SPACE, SCREEN_HEIGHT)
        button_top = SPACE
        self.add_component(ButtonIcon('btn_player', self.screen, ICO_PLAYER_FILE_ACTIVE, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_playlist', self.screen, ICO_PLAYLIST, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_library', self.screen, ICO_LIBRARY, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_directory', self.screen, ICO_DIRECTORY, SPACE, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_settings', self.screen, ICO_SETTINGS, SPACE, button_top))
        self.button_active_set(button_active)

    def on_click(self, x, y):
        tag_name = super(ScreenNavigation, self).on_click(x, y)
        return tag_name

    def play_pause(self):
        if self.__button_active == 'btn_player':
            self.components['btn_player'].icon_file_set(ICO_PLAYER_FILE_ACTIVE)
        else:
            self.components['btn_player'].icon_file_set(ICO_PLAYER_FILE)
        self.draw()

    def button_active_set(self, button_active):
        self.__button_active = button_active
        self.components['btn_player'].icon_file_set(ICO_PLAYER_FILE)
        self.components['btn_playlist'].icon_file_set(ICO_PLAYLIST)
        self.components['btn_library'].icon_file_set(ICO_LIBRARY)
        self.components['btn_directory'].icon_file_set(ICO_DIRECTORY)

        if button_active == 'btn_player':
            self.components['btn_player'].icon_file_set(ICO_PLAYER_FILE_ACTIVE)
        elif button_active == 'btn_playlist':
            self.components['btn_playlist'].icon_file_set(ICO_PLAYLIST_ACTIVE)
        elif button_active == 'btn_library':
            self.components['btn_library'].icon_file_set(ICO_LIBRARY_ACTIVE)
        elif button_active == 'btn_directory':
            self.components['btn_directory'].icon_file_set(ICO_DIRECTORY_ACTIVE)

        self.draw()
