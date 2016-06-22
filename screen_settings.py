"""
=======================================
**screen_settings.py**: Settings screen
=======================================
"""
__author__ = 'Mark Zwart'

import socket
from config_file import *
from gui_screens import *
from mpd_client import *
from screen_keyboard import Keyboard


class ScreenSettings(ScreenModal):
    """ Screen for settings or quitting/shutting down

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Settings"))
        self.title_color = C_GREY_LIGHTEST
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE

        label = _("Quit Pi-Jukebox")
        self.add_component(
            ButtonText('btn_quit', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Playback options")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_playback', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("MPD related settings")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_mpd', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("System info")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_system_info', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Back")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_return', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_return'].font_color = C_RED
        self.components['btn_return'].outline_color = C_RED

    def on_click(self, x, y):
        tag_name = super(ScreenSettings, self).on_click(x, y)
        if tag_name == 'btn_playback':
            screen_playback_options = ScreenSettingsPlayback(self.screen)
            screen_playback_options.show()
            self.show()
        elif tag_name == 'btn_quit':
            screen_quit = ScreenSettingsQuit(self.screen)
            screen_quit.show()
            self.show()
        elif tag_name == 'btn_mpd':
            screen_mpd = ScreenSettingsMPD(self.screen)
            screen_mpd.show()
            self.show()
        elif tag_name == 'btn_system_info':
            screen_system_info = ScreenSystemInfo(self.screen)
            screen_system_info.show()
            self.show()
        elif tag_name == 'btn_return':
            self.close()


class ScreenSettingsQuit(ScreenModal):
    """ Screen for quitting pi-jukebox.

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Quit"))
        self.window_x = 70
        self.window_y = 25
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True
        button_left = self.window_x + SPACE
        button_top = self.window_y + TITLE_HEIGHT + SPACE
        button_width = self.window_width - 2 * SPACE

        self.add_component(
            ButtonText('btn_quit', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT, _("Quit")))

        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(ButtonText('btn_shutdown', screen_rect,
                                      button_left, button_top, button_width, BUTTON_HEIGHT, _("Shutdown Pi")))

        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_reboot', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT, _("Reboot Pi")))

        button_top = self.window_height + self.window_y - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_cancel', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT, _("Back")))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_quit':
            mpd.disconnect()
            print(_("Bye!"))
            sys.exit()
        elif tag_name == 'btn_shutdown':
            if RUN_ON_RASPBERRY_PI:
                pygame.display.quit()
                os.system("sudo shutdown -h now")
            else:
                sys.exit()
        elif tag_name == 'btn_reboot':
            if RUN_ON_RASPBERRY_PI:
                pygame.display.quit()
                os.system("sudo shutdown -r now")
            else:
                sys.exit()
        elif tag_name == 'btn_cancel':
            self.close()


class ScreenSettingsPlayback(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Playback settings"))
        self.title_color = C_GREY_LIGHTEST
        switch_width = SWITCH_WIDTH + int(SPACE * 1.5)
        label_top = TITLE_HEIGHT + SPACE
        switch_top = label_top - int((SWITCH_HEIGHT - FONT_SPACE) / 2)
        switch_left = 2 * SPACE
        switch_space = int((self.window_width - 4 * SPACE) / 3)
        label_length = switch_space - switch_width

        self.add_component(Switch('switch_shuffle', screen_rect, switch_left, switch_top))
        self.add_component(LabelText('lbl_shuffle', screen_rect, switch_left + switch_width, label_top, label_length,
                                     FONT_SPACE, _("Shuffle")))

        switch_left += switch_space
        self.add_component(Switch('switch_repeat', screen_rect, switch_left, switch_top))
        self.add_component(LabelText('lbl_repeat', screen_rect, switch_left + switch_width, label_top, label_length,
                                     FONT_SPACE, _("Repeat")))

        switch_left += switch_space
        self.add_component(Switch('switch_single', screen_rect, switch_left, switch_top))
        self.add_component(LabelText('lbl_single', screen_rect, switch_left + switch_width, label_top, label_length,
                                     FONT_SPACE, _("Single")))

        label_top += int(1.5 * FONT_SPACE)
        switch_top += int(1.5 * FONT_SPACE)

        self.add_component(Switch('switch_consume', screen_rect, 2 * SPACE, switch_top))
        self.add_component(LabelText('lbl_consume', screen_rect, 2 * SPACE + switch_width, label_top,
                                     self.window_width - 2 * SPACE, FONT_SPACE, _("Consume playlist")))

        button_left = self.window_x + SPACE
        button_top = self.window_y + switch_top + 6 * SPACE
        button_width = self.window_width - 2 * SPACE

        self.add_component(ButtonText('btn_rescan', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT,
                                      _("Re-scan library")))

        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(ButtonText('btn_update', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT,
                                      _("Update library")))

        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_return', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT, _("Back")))
        self.components['btn_return'].font_color = C_RED
        self.components['btn_return'].outline_color = C_RED

        self.__initialize()

    def __initialize(self):
        """ Sets the screen controls according to current mpd configuration.
        """
        for key, value in self.components.items():
            if key == 'switch_shuffle':
                value.set_on(mpd.random)
            elif key == 'switch_repeat':
                value.set_on(mpd.repeat)
            elif key == 'switch_single':
                value.set_on(mpd.single)
            elif key == 'switch_consume':
                value.set_on(mpd.consume)

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'switch_shuffle':
            mpd.random_switch()
        elif tag_name == 'switch_repeat':
            mpd.repeat_switch()
        elif tag_name == 'switch_single':
            mpd.single_switch()
        elif tag_name == 'switch_consume':
            mpd.consume_switch()
        elif tag_name == 'btn_rescan':
            mpd.library_rescan()
        elif tag_name == 'btn_update':
            mpd.library_update()
        elif tag_name == 'btn_return':
            self.close()


class ScreenSettingsMPD(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("MPD settings"))
        self.title_color = C_GREY_LIGHTEST
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE

        label = _("Change host: {0}").format(config_file.setting_get('MPD Settings', 'host'))
        self.add_component(
            ButtonText('btn_host', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Change port: {0}").format(config_file.setting_get('MPD Settings', 'port'))
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_port', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Change music directory")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_music_dir', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_back', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, _("Back")))
        self.components['btn_back'].font_color = C_RED
        self.components['btn_back'].outline_color = C_RED

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        setting_label = ""
        setting_value = None
        if tag_name == 'btn_back':
            self.close()
            return
        elif tag_name == 'btn_host':
            setting_label = _("Set mpd host")
            self.keyboard_setting(setting_label, 'MPD Settings', 'host')
            mpd.disconnect()
            mpd.host = config_file.setting_get('MPD Settings', 'host')
            mpd.connect()
        elif tag_name == 'btn_port':
            setting_label = _("Set mpd server port")
            self.keyboard_setting(setting_label, 'MPD Settings', 'port')
            mpd.disconnect()
            mpd.host = int(config_file.setting_get('MPD Settings', 'port'))
            mpd.connect()
        elif tag_name == 'btn_music_dir':
            setting_label = _("Set music directory")
            self.keyboard_setting(setting_label, 'MPD Settings', 'music directory')
            mpd.music_directory = config_file.setting_get('MPD Settings', 'music directory')
        self.update()
        self.show()

    def keyboard_setting(self, caption, section, key, value=""):
        setting_value = config_file.setting_get(section, key, value)
        keyboard = Keyboard(self.screen, caption, setting_value)
        new_value = keyboard.show()  # Get entered search text
        config_file.setting_set(section, key, new_value)

    def update(self):
        label = _("Change host: {0}").format(config_file.setting_get('MPD Settings', 'host'))
        self.components['btn_host'].draw(label)
        label = _("Change port: {0}").format(config_file.setting_get('MPD Settings', 'port'))
        self.components['btn_port'].draw(label)


class ScreenSystemInfo(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("System info"))
        self.title_color = C_GREY_LIGHTEST
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        label_top = FONT_SPACE + SPACE

        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_back', self.screen, button_left, button_top, button_width, BUTTON_HEIGHT, _("Back")))
        self.components['btn_back'].font_color = C_RED
        self.components['btn_back'].outline_color = C_RED

        info = mpd.mpd_client.stats()

        self.add_component(LabelText('lbl_database', self.screen,
                                     button_left, label_top, button_width, FONT_SPACE, _("Music database")))
        self.components['lbl_database'].font_color = C_BLUE

        label_length = int((self.window_width - 2 * SPACE) / 3)
        label_left = button_left

        label_top += FONT_SPACE
        artist_count = _("Artists:  ") + "{:,}".format(int(info['artists']))
        self.add_component(
            LabelText('lbl_artist_count', self.screen, label_left, label_top, label_length, FONT_SPACE, artist_count))

        album_count = _("Albums:  ") + "{:,}".format(int(info['albums']))
        label_left += label_length
        self.add_component(
            LabelText('lbl_album_count', self.screen, label_left, label_top, label_length, FONT_SPACE, album_count))

        song_count = _("Songs:  ") + "{:,}".format(int(info['songs']))
        label_left += label_length
        self.add_component(
            LabelText('lbl_song_count', self.screen, label_left, label_top, label_length, FONT_SPACE, song_count))

        label_top += FONT_SPACE
        play_time = _("Total time:  ") + self.make_time_string(int(info['db_playtime']))
        self.add_component(LabelText('lbl_play_time', self.screen,
                                     button_left, label_top,
                                     self.window_width - button_left - SPACE, FONT_SPACE, play_time))

        label_top += int(FONT_SPACE * 1.5)
        self.add_component(
            LabelText('lbl_system', self.screen, button_left, label_top, button_width, FONT_SPACE, _("Server")))
        self.components['lbl_system'].font_color = C_BLUE

        label_top += FONT_SPACE
        self.add_component(LabelText('lbl_host_name', self.screen,
                                     button_left, label_top, self.window_width - button_left - SPACE, FONT_SPACE,
                                     _("Host name: {0}").format(socket.gethostname())))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('google.com', 0))
            ip_address = s.getsockname()[0]
            label_top += FONT_SPACE
            self.add_component(LabelText('lbl_ip_address', self.screen,
                                         button_left, label_top, self.window_width - button_left - SPACE, FONT_SPACE,
                                         _("IP address: {0}").format(ip_address)))
        except Exception:
            pass

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_back':
            self.close()
            return

    def make_time_string(self, seconds):
        days = int(seconds / 86400)
        hours = int((seconds - (days * 86400)) / 3600)
        minutes = int((seconds - (days * 86400) - (hours * 3600)) / 60)
        seconds_left = int(round(seconds - (days * 86400) - (hours * 3600) - (minutes * 60), 0))
        time_string = ""
        if days > 0:
            time_string += str(days) + _(" days ")
        if hours > 0:
            time_string += str(hours) + _(" hrs ")
        if minutes > 0:
            time_string += str(minutes) + _(" mins ")
        if seconds_left > 0:
            time_string += str(seconds_left) + _(" secs ")

        return time_string
