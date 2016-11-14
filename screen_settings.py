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

    def __init__(self, screen):
        ScreenModal.__init__(self, screen, _("Settings"))
        self.title_color = C_GREY_LIGHTEST
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE

        label = _("Quit Pi-Jukebox")
        self.add_component(
            ButtonText('btn_quit', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Playback options")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_playback', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("MPD related settings")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_mpd', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("System info")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_system_info', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Back")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_return', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_return'].font_color = C_RED
        self.components['btn_return'].outline_color = C_RED

    def on_click(self, x, y):
        tag_name = super(ScreenSettings, self).on_click(x, y)
        if tag_name == 'btn_playback':
            screen_playback_options = ScreenSettingsPlayback(self)
            screen_playback_options.show()
            self.show()
        elif tag_name == 'btn_quit':
            screen_quit = ScreenSettingsQuit(self)
            screen_quit.show()
            self.show()
        elif tag_name == 'btn_mpd':
            screen_mpd = ScreenSettingsMPD(self)
            screen_mpd.show()
            self.show()
        elif tag_name == 'btn_system_info':
            screen_system_info = ScreenSystemInfo(self)
            screen_system_info.show()
            self.show()
        elif tag_name == 'btn_return':
            self.close()


class ScreenSettingsQuit(ScreenModal):
    """ Screen for quitting pi-jukebox.

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen):
        ScreenModal.__init__(self, screen, _("Quit"))
        self.window_x = 70
        self.window_y = 25
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * SPACE

        label = _("Quit")
        button_top = self.window_y + TITLE_HEIGHT + SPACE
        self.add_component(
            ButtonText('btn_quit', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Shutdown Pi")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_shutdown', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Reboot Pi")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_reboot', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Back")
        button_top = self.window_height + self.window_y - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_cancel', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_quit':
            mpd.disconnect()
            print (_("Thanks for using pi-jukebox!\nBye!"))
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

    def __init__(self, screen):
        ScreenModal.__init__(self, screen, _("Playback settings"))
        self.title_color = C_GREY_LIGHTEST
        switch_width = SWITCH_WIDTH + int(SPACE * 1.5)
        label_top = TITLE_HEIGHT + SPACE
        switch_top = label_top - int((SWITCH_HEIGHT - FONT_SPACE) / 2)
        switch_left = 2 * SPACE
        switch_space = int((self.window_width - 4 * SPACE) / 3)
        label_length = switch_space - switch_width

        label = _("Shuffle")
        self.add_component(LabelText('lbl_shuffle', self.surface, switch_left + switch_width, label_top, label_length,
                                     FONT_SPACE, label))
        self.add_component(Switch('switch_shuffle', self.surface, switch_left, switch_top))

        label = _("Repeat")
        switch_left += switch_space
        self.add_component(LabelText('lbl_repeat', self.surface, switch_left + switch_width, label_top, label_length,
                                     FONT_SPACE, label))
        self.add_component(Switch('switch_repeat', self.surface, switch_left, switch_top))

        label = _("Single")
        switch_left += switch_space
        self.add_component(LabelText('lbl_single', self.surface, switch_left + switch_width, label_top, label_length,
                                     FONT_SPACE, label))
        self.add_component(Switch('switch_single', self.surface, switch_left, switch_top))

        label = _("Consume playlist")
        label_top += int(1.5 * FONT_SPACE)
        switch_top += int(1.5 * FONT_SPACE)
        self.add_component(LabelText('lbl_consume', self.surface, 2 * SPACE + switch_width, label_top,
                                     self.window_width - 2 * SPACE, FONT_SPACE, label))
        self.add_component(Switch('switch_consume', self.surface, 2 * SPACE, switch_top))

        label = _("Re-scan library")
        button_left = self.window_x + SPACE
        button_top = self.window_y + switch_top + 6 * SPACE
        button_width = self.window_width - 2 * SPACE
        self.add_component(ButtonText('btn_rescan', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT,
                                      label))

        label = _("Update library")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(ButtonText('btn_update', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT,
                                      label))

        label = _("Back")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_return', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
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
        self.host_new = config_file.setting_get('MPD Settings', 'host')
        self.port_new = config_file.setting_get('MPD Settings', 'port')
        self.dir_new = config_file.setting_get('MPD Settings', 'music directory')

        ScreenModal.__init__(self, screen_rect, _("MPD settings"))
        self.title_color = C_GREY_LIGHTEST
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        button_top = TITLE_HEIGHT + SPACE

        label = _("Change host: {0}").format(self.host_new)
        self.add_component(
            ButtonText('btn_host', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Change port: {0}").format(self.port_new)
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_port', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Change music directory")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_music_dir', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))

        label = _("Cancel")
        # FIXME: Check and correct button position
        button_top = self.window_height - 2 * SPACE - 2 * BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_cancel', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_cancel'].font_color = C_RED
        self.components['btn_cancel'].outline_color = C_RED

        label = _("Check and save")
        button_top += SPACE + BUTTON_HEIGHT
        self.add_component(
                ButtonText('btn_save', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_save'].font_color = C_GREEN
        self.components['btn_save'].outline_color = C_GREEN

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        setting_label = ""
        setting_value = None
        if tag_name == 'btn_save':
            if self.save_settings():
                self.close()
                return
        elif tag_name == 'btn_cancel':
            self.close()
            return
        elif tag_name == 'btn_host':
            setting_label = _("Set mpd host")
            self.host_new = self.keyboard_setting(setting_label, self.host_new)
            self.per_setting_check('host')
        elif tag_name == 'btn_port':
            setting_label = _("Set mpd server port")
            self.port_new = self.keyboard_setting(setting_label, self.port_new)
            self.per_setting_check('port')
        elif tag_name == 'btn_music_dir':
            setting_label = _("Set music directory")
            self.dir_new = self.keyboard_setting(setting_label, self.dir_new)
            self.per_setting_check('music directory')
        self.update()
        self.show()

    def keyboard_setting(self, caption, value=""):
        keyboard = Keyboard(self, caption)
        keyboard.text = value
        new_value = keyboard.show()  # Get entered search text
        return new_value

    def update(self):
        label = _("Change host: {0}").format(self.host_new)
        self.components['btn_host'].draw(label)
        # TODO: str(self.port_new) instead of self.port_new ???
        label = _("Change port: {0}").format(self.port_new)
        self.components['btn_port'].draw(label)

    def per_setting_check(self, setting_type):
        if setting_type == 'host' or setting_type == 'port':
            mpd.disconnect()
            host_old = mpd.host
            port_old = mpd.port
            mpd.host = self.host_new
            mpd.port = self.port_new
            if not mpd.connect():
                error_text = "Couldn't connect to the mpd server " + mpd.host + " on port " + str(mpd.port) + "!" \
                                                                                                              "Is the MPD server running? Try the command 'sudo service mpd start' on the CLI."
                msg_show = ScreenMessage(self.surface, "Wrong host or port!", error_text, 'warning')
                msg_show.show()
                mpd.host = host_old
                mpd.port = port_old
                mpd.connect()
                return False
            else:
                mpd.host = host_old
                mpd.port = port_old
                return True
        if setting_type == 'music directory':
            if not os.path.isdir(self.dir_new):
                error_text = "The music directory you specified " + self.dir_new + " does not exist!"
                msg_show = ScreenMessage(self.surface, "Invalid directory", error_text, 'error')
                msg_show.show()
                return False
            else:
                return True

    def save_settings(self):
        if self.per_setting_check('host') and self.per_setting_check('music directory'):
            config_file.setting_set('MPD Settings', 'host', self.host_new)
            config_file.setting_set('MPD Settings', 'port', self.port_new)
            config_file.setting_set('MPD Settings', 'music directory', self.dir_new)
            mpd.host = self.host_new
            mpd.port = self.port_new
            mpd.music_directory = self.dir_new

class ScreenSystemInfo(ScreenModal):
    """ Screen for settings playback options

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("System info"))
        self.title_color = C_GREY_LIGHTEST
        info = mpd.mpd_client.stats()
        button_left = self.window_x + SPACE
        button_width = self.window_width - 2 * button_left
        label_top = FONT_SPACE + SPACE

        label = _("Back")
        button_top = self.window_height - SPACE - BUTTON_HEIGHT
        self.add_component(
            ButtonText('btn_back', self.surface, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_back'].font_color = C_RED
        self.components['btn_back'].outline_color = C_RED

        label = _("Music database")
        self.add_component(LabelText('lbl_database', self.surface,
                                     button_left, label_top, button_width, FONT_SPACE, label))
        self.components['lbl_database'].font_color = C_BLUE

        label_length = int((self.window_width - 2 * SPACE) / 3)
        label_left = button_left

        label_top += FONT_SPACE
        artist_count = _("Artists:  ") + "{:,}".format(int(info['artists']))
        self.add_component(
            LabelText('lbl_artist_count', self.surface, label_left, label_top, label_length, FONT_SPACE, artist_count))

        album_count = _("Albums:  ") + "{:,}".format(int(info['albums']))
        label_left += label_length
        self.add_component(
            LabelText('lbl_album_count', self.surface, label_left, label_top, label_length, FONT_SPACE, album_count))

        song_count = _("Songs:  ") + "{:,}".format(int(info['songs']))
        label_left += label_length
        self.add_component(
            LabelText('lbl_song_count', self.surface, label_left, label_top, label_length, FONT_SPACE, song_count))

        label_top += FONT_SPACE
        play_time = _("Total time:  ") + self.make_time_string(int(info['db_playtime']))
        self.add_component(LabelText('lbl_play_time', self.surface,
                                     button_left, label_top,
                                     self.window_width - button_left - SPACE, FONT_SPACE, play_time))

        label = _("Server")
        label_top += int(FONT_SPACE * 1.5)
        self.add_component(
            LabelText('lbl_system', self.surface, button_left, label_top, button_width, FONT_SPACE, label))
        self.components['lbl_system'].font_color = C_BLUE

        label = _("Host name: {0}").format(socket.gethostname())
        label_top += FONT_SPACE
        self.add_component(LabelText('lbl_host_name', self.surface, button_left, label_top,
                                     self.window_width - button_left - SPACE, FONT_SPACE, label))
        try:
            label = _("IP address: {0}").format(ip_address)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('google.com', 0))
            ip_address = s.getsockname()[0]
            label_top += FONT_SPACE
            self.add_component(LabelText('lbl_ip_address', self.surface, button_left, label_top,
                                         self.window_width - button_left - SPACE, FONT_SPACE, label))
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
