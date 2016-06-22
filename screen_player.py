"""
=======================================================
**screen_player.py**: Playback screen.
=======================================================
"""

from pij_screen_navigation import *
from screen_settings import *


class Playlist(ItemList):
    """ Displays playlist information.

        :param screen_rect: The display's rect where the library browser is drawn on.
    """
    def __init__(self, screen_rect):
        ItemList.__init__(self, 'list_playing', screen_rect,
                          ICO_WIDTH + 2 * SPACE, SPACE + 2 * FONT_SPACE + 6,
                          SCREEN_WIDTH - 2 * (ICO_WIDTH + 2 * SPACE), SCREEN_HEIGHT - 2 * SPACE - 2 * FONT_SPACE - 6)
        # TODO: Add proper handling
        # if DISPLAY == 'raspberry7':
        #     ItemList.__init__(self, 'list_playing', screen_rect,
        #         52, 46, 696, 419)
        # elif DISPLAY == 'adafruit3.5':
        #     ItemList.__init__(self, 'list_playing', screen_rect,
        #         52, 46, 216, 189)
        # else:
        #     ItemList.__init__(self, 'list_playing', screen_rect,
        #         52, 46, 216, 189)
        self.item_height = FONT_SPACE
        self.item_active_color = C_YELLOW
        self.outline_color = C_BLUE
        self.font_color = C_GREY_LIGHTEST
        self.outline_visible = False

    def show_playlist(self):
        """ Display the playlist. """
        updated = False
        if self.list != mpd.playlist_current_get():
            self.list = mpd.playlist_current_get()
            updated = True
        if self.active_item_index != mpd.playlist_current_playing_index_get():
            self.active_item_index = mpd.playlist_current_playing_index_get()
            updated = True
        if updated:
            self.draw()


class ScreenPlaylist(Screen):
    """ The screen containing everything to control playback.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)

        self.font_color = C_GREY_LIGHTEST

        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.screen, 'btn_playlist'))

        # Player specific buttons
        button_top = SPACE
        button_left = SCREEN_WIDTH - ICO_WIDTH - SPACE
        self.add_component(ButtonIcon('btn_play', self.screen, ICO_PLAY, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_stop', self.screen, ICO_STOP, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_prev', self.screen, ICO_PREVIOUS, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_next', self.screen, ICO_NEXT, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_volume', self.screen, ICO_VOLUME, button_left, button_top))

        # Player specific labels
        label_left = ICO_WIDTH + 2 * SPACE
        label_width = SCREEN_WIDTH - 2 * (ICO_WIDTH + 2 * SPACE)
        self.add_component(LabelText('lbl_track_artist', self.screen, label_left, SPACE, label_width, FONT_SPACE))
        self.add_component(
            LabelText('lbl_track_title', self.screen, label_left, SPACE + FONT_SPACE, label_width, FONT_SPACE))

        # Splits labels from playlist
        self.add_component(Rectangle('rct_split', self.screen, label_left, SPACE + 2 * FONT_SPACE + 4, label_width, 1))

        # Playlist
        self.add_component(Playlist(self.screen))
        self.components['list_playing'].active_item_index = mpd.playlist_current_playing_index_get()

        # time (current/total)
        self.add_component(LabelText('lbl_time_total', self.screen,
                                     SCREEN_WIDTH - ICO_WIDTH - SPACE, SCREEN_HEIGHT - FONT_SIZE - SPACE,
                                     ICO_WIDTH, FONT_SIZE))
        self.components['lbl_time_total'].set_alignment(HOR_MID, VERT_MID)

        self.add_component(LabelText('lbl_time_current', self.screen,
                                     SCREEN_WIDTH - ICO_WIDTH - SPACE, SCREEN_HEIGHT - 2 * FONT_SIZE - SPACE,
                                     ICO_WIDTH, FONT_SIZE))
        self.components['lbl_time_current'].set_alignment(HOR_MID, VERT_MID)

    def show(self):
        """ Displays the screen. """
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        now_playing = mpd.now_playing
        self.components['lbl_time_current'].text_set(now_playing.time_current)
        self.components['lbl_time_total'].text_set(now_playing.time_total)
        if mpd.player_control_get() == 'play':
            self.components['btn_play'].set_image_file(ICO_PAUSE)
        else:
            self.components['btn_play'].set_image_file(ICO_PLAY)
        self.components['btn_play'].draw()
        self.components['lbl_track_title'].text_set(now_playing.title)
        self.components['lbl_track_artist'].text_set(now_playing.artist)
        super(ScreenPlaylist, self).show()  # Draw screen
        self.components['list_playing'].show_playlist()
        self.components['list_playing'].show_item_active()  # Makes sure currently playing playlist item is on screen

    def update(self):
        now_playing = mpd.now_playing
        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        while True:
            try:
                event = mpd.events.popleft()
                if event == 'playing_index':
                    self.components['list_playing'].show_playlist()
                elif event == 'time_elapsed' or event == 'playing_time_total':
                    self.components['lbl_time_current'].text_set(now_playing.time_current)
                    self.components['lbl_time_total'].text_set(now_playing.time_total)
                elif event == 'playing_file':
                    self.components['lbl_track_title'].text_set(now_playing.title)
                    self.components['lbl_track_artist'].text_set(now_playing.artist)
                elif event == 'state':
                    state = mpd.player_control_get()
                    if self.components['btn_play'].image_file != ICO_PAUSE and state == 'play':
                        self.components['btn_play'].draw(ICO_PAUSE)
                    elif self.components['btn_play'].image_file == ICO_PAUSE and state != 'play':
                        self.components['btn_play'].draw(ICO_PLAY)
            except IndexError:
                break

    def on_click(self, x, y):
        """
        :param x: The horizontal click position.
        :param y: The vertical click position.

        :return: Possibly returns a screen index number to switch to.
        """
        tag_name = super(ScreenPlaylist, self).on_click(x, y)
        if tag_name == 'btn_player':
            return 0
        elif tag_name == 'btn_playlist':
            return 1
        elif tag_name == 'btn_library':
            return 2
        elif tag_name == 'btn_directory':
            return 3
        elif tag_name == 'btn_radio':
            return 4
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self.screen)
            setting_screen.show()
            self.show()
        elif tag_name == 'btn_play':
            if mpd.player_control_get() == 'play':
                mpd.player_control_set('pause')
                self.components['btn_play'].set_image_file(ICO_PLAY)
            else:
                mpd.player_control_set('play')
                self.components['btn_play'].set_image_file(ICO_PAUSE)
            self.components['btn_play'].draw()
        elif tag_name == 'btn_stop':
            self.components['btn_play'].set_image_file(ICO_PLAY)
            mpd.player_control_set('stop')
        elif tag_name == 'btn_prev':
            mpd.player_control_set('previous')
        elif tag_name == 'btn_next':
            mpd.player_control_set('next')
        elif tag_name == 'btn_volume':
            screen_volume = ScreenVolume(self.screen)
            screen_volume.show()
            self.show()
        elif tag_name == 'list_playing':
            selected_index = self.components['list_playing'].item_selected_index
            if selected_index >= 0:
                mpd.play_playlist_item(selected_index + 1)
                self.components['list_playing'].active_item_index = selected_index
                self.components['list_playing'].draw()


class ScreenPlaying(Screen):
    """ Screen cover art

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """
    def __init__(self, screen_rect):
        Screen.__init__(self, screen_rect)

        # Screen navigation buttons
        self.add_component(ScreenNavigation('screen_nav', self.screen, 'btn_player'))

        # Player specific buttons
        button_top = SPACE
        button_left = SCREEN_WIDTH - ICO_WIDTH - SPACE
        self.add_component(ButtonIcon('btn_play', self.screen, ICO_PLAY, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_stop', self.screen, ICO_STOP, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_prev', self.screen, ICO_PREVIOUS, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_next', self.screen, ICO_NEXT, button_left, button_top))
        button_top += ICO_HEIGHT + SPACE
        self.add_component(ButtonIcon('btn_volume', self.screen, ICO_VOLUME, button_left, button_top))

        # Player specific labels
        label_left = ICO_WIDTH + 2 * SPACE
        label_width = SCREEN_WIDTH - 2 * (ICO_WIDTH + 2 * SPACE)
        self.add_component(
            LabelText('lbl_track_artist', self.screen, label_left, SPACE, label_width, FONT_SIZE))
        self.components['lbl_track_artist'].set_alignment(HOR_MID, VERT_MID)
        self.add_component(
            LabelText('lbl_track_album', self.screen, label_left, SPACE + FONT_SIZE, label_width, FONT_SIZE))
        self.components['lbl_track_album'].set_alignment(HOR_MID, VERT_MID)

        # Cover art
        self.add_component(Picture('pic_cover_art', self.screen,
                                   label_left, 2 * SPACE + 2 * FONT_SIZE,
                                   label_width, SCREEN_HEIGHT - LIST_INDICATOR_WIDTH - 3 * FONT_SIZE - 5 * SPACE,
                                   image_data=mpd.get_cover_art(), center=True))

        self.add_component(Slider2('slide_time', self.screen,
                                   label_left, SCREEN_HEIGHT - LIST_INDICATOR_WIDTH - FONT_SIZE - 2 * SPACE,
                                   label_width, LIST_INDICATOR_WIDTH))

        self.add_component(LabelText('lbl_track_title', self.screen,
                                     label_left, SCREEN_HEIGHT - FONT_SIZE - SPACE,
                                     label_width, FONT_SIZE))
        self.components['lbl_track_title'].set_alignment(HOR_MID, VERT_MID)

        # time (current/total)
        self.add_component(LabelText('lbl_time_total', self.screen,
                                     SCREEN_WIDTH - ICO_WIDTH - SPACE, SCREEN_HEIGHT - FONT_SIZE - SPACE,
                                     ICO_WIDTH, FONT_SIZE))
        self.components['lbl_time_total'].set_alignment(HOR_MID, VERT_MID)

        self.add_component(LabelText('lbl_time_current', self.screen,
                                     SCREEN_WIDTH - ICO_WIDTH - SPACE, SCREEN_HEIGHT - 2 * FONT_SIZE - SPACE,
                                     ICO_WIDTH, FONT_SIZE))
        self.components['lbl_time_current'].set_alignment(HOR_MID, VERT_MID)


    def show(self):
        """ Displays the screen. """

        self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
        self.components['lbl_time_current'].text_set(mpd.now_playing.time_current)
        self.components['lbl_time_total'].text_set(mpd.now_playing.time_total)
        if mpd.player_control_get() == 'play':
            self.components['btn_play'].set_image_file(ICO_PAUSE)
        else:
            self.components['btn_play'].set_image_file(ICO_PLAY)
        self.components['btn_play'].draw()
        self.components['lbl_track_title'].text_set(mpd.now_playing.title)
        self.components['lbl_track_artist'].text_set(mpd.now_playing.artist)
        self.components['lbl_track_album'].text_set(mpd.now_playing.album)
        self.components['pic_cover_art'].picture_set(image_data=mpd.get_cover_art())
        super(ScreenPlaying, self).show()  # Draw screen

    def update(self):
        while True:
            try:
                event = mpd.events.popleft()
                self.components['screen_nav'].radio_mode_set(mpd.radio_mode_get())
                playing = mpd.now_playing
                if event == 'time_elapsed':
                    self.components['lbl_time_current'].text_set(playing.time_current)
                    self.components['slide_time'].draw(playing.time_percentage)
                elif event == 'playing_file':
                    self.components['lbl_track_title'].text_set(playing.title)
                    self.components['lbl_track_artist'].text_set(playing.artist)
                    self.components['pic_cover_art'].picture_set(image_data=mpd.get_cover_art())
                    self.components['lbl_track_album'].text_set(playing.album)
                    self.components['lbl_time_total'].text_set(playing.time_total)
                elif event == 'state':
                    if self.components['btn_play'].image_file != ICO_PAUSE and mpd.player_control_get() == 'play':
                        self.components['btn_play'].draw(ICO_PAUSE)
                    elif self.components['btn_play'].image_file == ICO_PAUSE and mpd.player_control_get() != 'play':
                        self.components['btn_play'].draw(ICO_PLAY)
            except IndexError:
                break

    def on_click(self, x, y):
        tag_name = super(ScreenPlaying, self).on_click(x, y)
        if tag_name == 'btn_player':
            return 0
        elif tag_name == 'btn_playlist':
            return 1
        elif tag_name == 'btn_library':
            return 2
        elif tag_name == 'btn_directory':
            return 3
        elif tag_name == 'btn_radio':
            return 4
        elif tag_name == 'btn_settings':
            setting_screen = ScreenSettings(self.screen)
            setting_screen.show()
            self.show()
        elif tag_name == 'btn_play':
            if mpd.player_control_get() == 'play':
                mpd.player_control_set('pause')
                self.components['btn_play'].set_image_file(ICO_PLAY)
            else:
                mpd.player_control_set('play')
                self.components['btn_play'].set_image_file(ICO_PAUSE)
            self.components['btn_play'].draw()
        elif tag_name == 'btn_stop':
            self.components['btn_play'].set_image_file(ICO_PLAY)
            mpd.player_control_set('stop')
        elif tag_name == 'btn_prev':
            mpd.player_control_set('previous')
        elif tag_name == 'btn_next':
            mpd.player_control_set('next')
        elif tag_name == 'btn_volume':
            screen_volume = ScreenVolume(self.screen)
            screen_volume.show()
            self.show()


class ScreenVolume(ScreenModal):
    """ Screen setting volume

        :param screen_rect: The display's rectangle where the screen is drawn on.
    """

    def __init__(self, screen_rect):
        ScreenModal.__init__(self, screen_rect, _("Volume"))
        self.window_x = 15
        self.window_y = 52
        self.window_width -= 2 * self.window_x
        self.window_height -= 2 * self.window_y
        self.outline_shown = True
        self.title_color = C_BLUE
        self.outline_color = C_BLUE

        button_top = self.window_y + BUTTON_TOP + SPACE
        button_left = self.window_x + SPACE + 1

        self.add_component(ButtonIcon('btn_mute', screen_rect, ICO_VOLUME_MUTE, self.window_x + 5, button_top))
        self.components['btn_mute'].x_pos = self.window_x + self.window_width / 2 - \
            self.components['btn_mute'].width / 2

        self.add_component(ButtonIcon('btn_volume_down', screen_rect, ICO_VOLUME_DOWN, button_left, button_top))

        self.add_component(ButtonIcon('btn_volume_up', screen_rect, ICO_VOLUME_UP,
                                      self.window_x + self.window_width - ICO_WIDTH - SPACE, button_top))

        button_top += ICO_HEIGHT + 2 * SPACE
        self.add_component(
            Slider('slide_volume', screen_rect, button_left, button_top, self.window_width - 2 * SPACE, BUTTON_HEIGHT))
        self.components['slide_volume'].progress_percentage_set(mpd.volume)

        label = _("Back")
        button_top = self.window_height + self.window_y - SPACE - BUTTON_HEIGHT
        button_width = self.window_width - 2 * SPACE
        self.add_component(
            ButtonText('btn_back', screen_rect, button_left, button_top, button_width, BUTTON_HEIGHT, label))
        self.components['btn_back'].font_color = C_RED
        self.components['btn_back'].outline_color = C_RED

    def on_click(self, x, y):
        tag_name = super(ScreenModal, self).on_click(x, y)
        if tag_name == 'btn_mute':
            mpd.volume_mute_switch()
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'btn_volume_down':
            mpd.volume_set_relative(-10)
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'btn_volume_up':
            mpd.volume_set_relative(10)
            self.components['slide_volume'].progress_percentage_set(mpd.volume)
        elif tag_name == 'slide_volume':
            mpd.volume_set(self.components['slide_volume'].progress_percentage)
        elif tag_name == 'btn_back':
            self.close()
        if mpd.volume == 0 or mpd.volume_mute_get():
            self.components['btn_mute'].set_image_file(ICO_VOLUME_MUTE_ACTIVE)
        else:
            self.components['btn_mute'].set_image_file(ICO_VOLUME_MUTE)
        self.components['btn_mute'].draw()
