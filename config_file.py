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


import ConfigParser


class ConfigFile(object):

    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        self.parser.optionxform = str
        self.parser.read("pi-jukebox.conf")
        # MPD configuration settings
        self.settings = []
        self.radio_stations = []
        self.settings.append({'section': 'MPD Settings', 'key': 'host', 'value': 'localhost', 'first_time': False})
        self.settings.append({'section': 'MPD Settings', 'key': 'port', 'value': '6600', 'first_time': False})
        self.settings.append({'section': 'MPD Settings', 'key': 'music directory', 'value': None, 'first_time': True})
        self.settings.append({'section': 'Miscellaneous', 'key': 'blank period', 'value': '300', 'first_time': False})
        self.settings.append({'section': 'Hardware', 'key': 'display', 'value': 'adafruit2.8', 'first_time': False})
        self.settings.append({'section': 'adafruit2.8', 'key': 'resolution', 'value': '320x240', 'first_time': False})
        self.settings.append({'section': 'adafruit2.8', 'key': 'font size', 'value': '16', 'first_time': False})
        self.settings.append({'section': 'adafruit3.5', 'key': 'resolution', 'value': '480x320', 'first_time': False})
        self.settings.append({'section': 'adafruit3.5', 'key': 'font size', 'value': '20', 'first_time': False})
        self.settings.append({'section': 'raspberry7', 'key': 'resolution', 'value': '800x480', 'first_time': False})
        self.settings.append({'section': 'raspberry7', 'key': 'font size', 'value': '28', 'first_time': False})
        self.settings.append({'section': 'Radio stations', 'key': 'Radio Swiss Jazz',
                              'value': 'http://stream.srg-ssr.ch/m/rsj/mp3_128', 'first_time': False})
        self.initialize()

    def initialize(self):
        for setting in self.settings:
            if self.setting_exists(setting['section'], setting['key']):
                setting['value'] = self.setting_get(setting['section'], setting['key'])
            elif not setting['first_time']:
                self.setting_set(setting['section'], setting['key'], setting['value'])
            if setting['section'] == 'Radio stations':
                self.radio_stations.append((setting['key'], setting['value']))

    def setting_get(self, section, key, default=None):
        if self.setting_exists(section, key):
            return self.parser.get(section, key)
        else:
            return default

    def setting_set(self, section, key, value):
        """ Write a setting to the configuration file

            :param section: Config section
            :param key: Key
            :param value: Value

        """
        cfg_file = open("pi-jukebox.conf", 'w')
        try:
            self.parser.add_section(section)
        except ConfigParser.DuplicateSectionError:
            pass
        self.parser.set(section, key, value)
        self.parser.write(cfg_file)
        cfg_file.close()

    def setting_remove(self, section, key):
        """ Remove a setting to the configuration file
        """
        cfg_file = open("pi-jukebox.conf", 'w')
        try:
            self.parser.remove_option(section, key)
        except ConfigParser.NoSectionError:
            pass
        self.parser.write(cfg_file)
        cfg_file.close()

    def section_exists(self, section):
        return self.parser.has_section(section)

    def setting_exists(self, section, key):
        return self.parser.has_option(section, key)

    def radio_station_set(self, name, url):
        """ Edits or creates radio station entry """
        self.setting_set('Radio stations', name, url)

    def radio_stations_get(self):
        """ Get's radio stations from the configuration file and returns them in a list """
        self.radio_stations = []
        stations = self.parser.options('Radio stations')
        for name in stations:
            url = self.setting_get('Radio stations', name)
            self.radio_stations.append((name, url))
        return self.radio_stations

config_file = ConfigFile()
