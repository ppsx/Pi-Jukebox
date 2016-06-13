import ConfigParser


class ConfigFile(object):
    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        self.parser.optionxform = str
        self.parser.read("pi-jukebox.conf")
        # MPD configuration settings
        self.settings = []
        self.settings.append({'section': 'Hardware', 'key': 'display', 'value': 'adafruit2.8', 'first_time': False})
        self.settings.append({'section': 'MPD Settings', 'key': 'host', 'value': 'localhost', 'first_time': False})
        self.settings.append({'section': 'MPD Settings', 'key': 'port', 'value': '6600', 'first_time': False})
        self.settings.append({'section': 'MPD Settings', 'key': 'music directory', 'value': None, 'first_time': True})
        self.initialize()

    def initialize(self):
        for setting in self.settings:
            if self.setting_exists(setting['section'], setting['key']):
                setting['value'] = self.setting_get(setting['section'], setting['key'])
            elif not setting['first_time']:
                self.setting_set(setting['section'], setting['key'], setting['value'])

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

    def section_get(self, section):
        dict1 = {}
        options = self.parser.options(section)
        for option in options:
            dict1[option] = self.parser.getboolean(section, option)
        return dict1

config_file = ConfigFile()
