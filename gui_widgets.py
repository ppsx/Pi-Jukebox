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


import io
import zipfile
import math
import sys
from settings import *


reload(sys)
sys.setdefaultencoding('utf8')

# Alignment variables
HOR_LEFT = 0
HOR_MID = 1
HOR_RIGHT = 2
VERT_TOP = 0
VERT_MID = 1
VERT_BOTTOM = 2


class Widget(object):
    """ Widget is the base class of screen widgets and should not be instantiated by itself.

        :param tag_name: Text identifying the widget.
        :param surface: The screen's rectangle where the widget is drawn on.
        :param x: The horizontal starting position of the widget's rectangle.
        :param y: The vertical starting position of the widget's rectangle.
        :param width: The width of the widget's rectangle.
        :param height: The height of the widget's rectangle.
    """

    def __init__(self, tag_name, surface, x, y, width, height):
        self.tag_name = tag_name
        self.visible = True
        self.surface = surface
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.rect = Rect(x, y, width, height)
        self.outline_visible = False
        self.outline_color = BLACK
        self.background_color = BLACK
        self.font = FONT
        self.font_color = C_GREY_LIGHTEST
        self.font_height = self.font.size('Tg')[1]

    def on_click(self, x, y):
        """ The function called when a widget is clicked """
        return self.tag_name

    def set_font(self, font_name, font_size, font_color=C_GREY_LIGHTEST):
        self.font = pygame.font.Font(font_name, font_size)
        self.font_color = font_color

    def position_set(self, x, y, width, height):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.rect = Rect(x, y, width, height)


class Rectangle(Widget):
    """ Drawing a rectangle on screen

        :param tag_name: Text identifying the rectangle.
        :param surface: The screen's rectangle where the rectangle is drawn on.
        :param x: The horizontal starting position of the rectangle's rectangle.
        :param y: The vertical starting position of the rectangle's rectangle.
        :param width: The width of the rectangle's rectangle.
        :param height: The height of the rectangle's rectangle.
    """

    def __init__(self, tag_name, surface, x, y, width, height):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        self.background_color = C_GREY_DARK
        self.font_color = C_BLUE
        self.outline_color = C_BLUE

    def draw(self):
        """ Draws the label. """
        self.surface.fill(self.background_color, self.rect)  # Background
        pygame.display.update(self.rect)


class Slider(Rectangle):
    """ A slider control

        :param tag_name: Text identifying the slider.
        :param surface: The screen's rectangle where the slider is drawn on.
        :param x: The horizontal starting position of the slider's rectangle.
        :param y: The vertical starting position of the slider's rectangle.
        :param width: The width of the slider's rectangle.
        :param height: The height of the slider's rectangle.
    """

    def __init__(self, tag_name, surface, x, y, width, height):
        Rectangle.__init__(self, tag_name, surface, x, y, width, height)
        self.progress_color = C_GREEN
        self.progress_percentage = 0
        self.progress_rect = Rect(x + 1, y + 1, 1, height - 2)
        self.caption_visible = True

    def draw(self, percentage=None):
        if percentage is not None:
            self.progress_percentage_set(percentage)
        self.surface.fill(self.background_color, self.rect)  # Background
        pygame.display.update(self.rect)
        if self.progress_percentage > 0:
            self.surface.fill(self.progress_color, self.progress_rect)  # Progress bar
            pygame.display.update(self.progress_rect)

    def progress_percentage_set(self, percentage):
        """ Sets the slider's percentage 'full'.

            :param percentage: No need to explain. Right?
        """
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100
        if percentage == 0:
            width = 1
        else:
            width = (self.width - 2) * (float(percentage) / 100)
        self.progress_rect = Rect(self.x_pos + 1, self.y_pos + 1, width, self.height - 2)
        self.progress_percentage = percentage
        self.draw()

    def on_click(self, x, y):
        """ Sets the percentage of the slide by clicking.
        """
        new_percentage = int((float(x - self.x_pos) / float(self.width)) * 100)
        self.progress_percentage_set(new_percentage)
        return self.tag_name


class Slider2(Widget):
    """ A slider control with a different lay-out.

        :param tag_name: Text identifying the slider.
        :param surface: The screen's rectangle where the slider is drawn on.
        :param x: The horizontal starting position of the slider's rectangle.
        :param y: The vertical starting position of the slider's rectangle.
        :param width: The width of the slider's rectangle.
        :param height: The height of the slider's rectangle.
    """

    def __init__(self, tag_name, surface, x, y, width, height):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        self.bottom_color = C_GREY_LIGHT
        self.bottom_rect = (x, y + height, width, 1)
        self.progress_color = C_YELLOW
        self.progress_percentage = 0
        self.progress_rect = Rect(x, y, 1, height)
        self.caption_visible = False

    def draw(self, percentage=None):
        if percentage is not None:
            self.progress_percentage_set(percentage)
        self.surface.fill(self.background_color, self.rect)  # Background
        self.surface.fill(self.bottom_color, self.bottom_rect)
        if self.progress_percentage > 0:
            self.surface.fill(self.progress_color, self.progress_rect)  # Progress bar
        pygame.display.update(self.rect)

    def progress_percentage_set(self, percentage):
        """ Sets the slider's percentage 'full'.

            :param percentage: No need to explain. Right?
        """
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100
        if percentage == 0:
            width = 1
        else:
            width = self.width * (float(percentage) / 100)
        self.progress_rect = Rect(self.x_pos, self.y_pos, width, self.height)
        self.progress_percentage = percentage
        self.draw()

    def on_click(self, x, y):
        """ Sets the percentage of the slide by clicking.
        """
        new_percentage = int((float(x - self.x_pos) / float(self.width)) * 100)
        self.progress_percentage_set(new_percentage)
        return self.tag_name


class Picture(Widget):
    """ Picture on screen

        :param tag_name: Text identifying the picture.
        :param surface: The screen's rectangle where the picture is drawn on.
        :param x: The horizontal starting position of the picture's rectangle.
        :param y: The vertical starting position of the picture's rectangle.
        :param width: The width of the picture's rectangle.
        :param height: The height of the picture's rectangle.
        :param center: If set to True - the picture will be centered in given rectangle
    """

    def __init__(self, tag_name, surface, x, y, width, height, image_file="", center=False, image_data=None):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        self.__center = center
        self.x_mod = 0
        self.y_mod = 0
        self.__image_file = image_file
        self.__image = image_data if image_data else self.get_image(image_file)
        self.prepare_picture()

    @staticmethod
    def get_image(image_file):
        if not image_file:
            return None
        if image_file.startswith(RESOURCES_DIR):
            data = image_file
        else:
            with zipfile.ZipFile(RESOURCES_ZIP) as res:
                img = res.read(image_file)
            data = io.BytesIO(img)
        return pygame.image.load(data)

    def draw(self):
        SCREEN.blit(self.__image, (self.x_pos + self.x_mod, self.y_pos + self.y_mod))
        pygame.display.update(self.rect)

    def on_click(self, x, y):
        return self.tag_name

    def picture_set(self, image_file="", image_data=None):
        """ Sets the filename of the picture. """
        self.__image_file = image_file
        self.__image = image_data if image_data else self.get_image(self.__image_file)
        self.prepare_picture()
        self.draw()

    def prepare_picture(self):
        if not self.__image:
            return
        if not self.__center:
            # original behavior - shrinking and/or stretching the image to fit given width/height
            self.__image = pygame.transform.smoothscale(self.__image, (self.width, self.height))
            return
        factor_w = factor_h = 1.0
        if self.__image.get_width() > self.width:
            factor_w = float(self.width) / self.__image.get_width()
        if self.__image.get_height() > self.height:
            factor_h = float(self.height) / self.__image.get_height()
        factor = min(factor_w, factor_h)
        if factor != 1.0:
            # need to shrink the image
            self.__image = pygame.transform.smoothscale(self.__image, (int(self.__image.get_width() * factor),
                                                                       int(self.__image.get_height() * factor)))
        self.x_mod = int(float(self.width - self.__image.get_width()) / 2)
        self.y_mod = int(float(self.height - self.__image.get_height()) / 2)


class LabelText(Widget):
    """ LabelText is used to write text that needs to fit in a pre-defined rectangle.

        :param tag_name: Text identifying the label.
        :param surface: The screen's rectangle where the label is drawn on.
        :param x: The horizontal starting position of the label's rectangle.
        :param y: The vertical starting position of the label's rectangle.
        :param width: The width of the label's rectangle.
        :param height: The height of the label's rectangle.
        :param text: The text to be displayed in the label, default= ""
    """

    def __init__(self, tag_name, surface, x, y, width, height, text=""):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        try:
            self.caption = text.decode('utf-8')
        except UnicodeError:
            self.caption = ""
        self.alignment_horizontal = HOR_LEFT
        self.alignment_vertical = VERT_MID
        self.indent_horizontal = 0
        self.indent_vertical = 0
        self.outline_show = False
        self.outline_color = C_BLUE
        self.background_alpha = 255

    def transparent_set(self, value):
        """ Turns background transparent or opaque. """
        if value:
            self.background_alpha = 0
        else:
            self.background_alpha = 255

    def set_alignment(self, horizontal, vertical, hor_indent=0, vert_indent=0):
        """ Sets the label's horizontal and vertical alignment within the defined
            rectangle and/or the text horizontal/vertical indent.

            :param horizontal: Horizontal alignment
            :param vertical: Vertical alignment
            :param hor_indent: Horizontal alignment indentation
            :param vert_indent: Vertical alignment indentation
        """
        self.alignment_horizontal = horizontal
        self.alignment_vertical = vertical
        self.indent_horizontal = hor_indent
        self.indent_vertical = vert_indent

    def text_set(self, text):
        if self.caption != text.decode('utf-8'):
            self.caption = text.decode('utf-8')
            self.draw()

    def draw(self):
        """ Draws the label.

            :return: Text that couldn't be fitted inside the label's rectangle,
        """
        self.caption = self.caption.decode('utf-8')
        # Draw background
        background = pygame.Surface((self.width, self.height))
        background.set_alpha(self.background_alpha)
        background.fill(self.background_color)
        SCREEN.blit(background, (self.x_pos, self.y_pos))
        # Draw outline
        if self.outline_show:
            pygame.draw.rect(self.surface, self.outline_color, self.rect, 1)
        # Determining caption width and height
        i = 1
        # Determine maximum width of line
        while self.font.size(self.caption[:i])[0] < self.rect.width and i < len(self.caption):
            i += 1
        caption_width = self.font.size(self.caption[:i])[0]
        caption_height = self.font.size(self.caption[:i])[1]

        # Horizontal alignment
        if self.alignment_horizontal == HOR_MID:
            x = self.rect.centerx + self.indent_horizontal - caption_width / 2
        elif self.alignment_horizontal == HOR_RIGHT:
            x = self.rect.right - self.indent_horizontal - caption_width
        else:   # default alignment: HOR_LEFT
            x = self.rect.left + self.indent_horizontal

        # Vertical alignment
        if self.alignment_vertical == VERT_MID:
            y = self.rect.centery + self.indent_vertical - caption_height / 2
        elif self.alignment_vertical == VERT_BOTTOM:
            y = self.rect.bottom - self.indent_vertical - caption_height
        else:   # default alignment: VERT_TOP
            y = self.rect.top + self.indent_vertical

        # Draw Caption
        image = FONT.render(self.caption[:i], True, self.font_color)
        self.surface.blit(image, (x, y))
        pygame.display.update(self.rect)

        return self.caption[i:]


class Memo(Widget):
    """ LabelText is used to write text that needs to fit in a pre-defined rectangle.

        :param tag_name: Text identifying the memo field.
        :param screen_rect: The screen's rectangle where the memo field is drawn on.
        :param x: The horizontal starting position of the memo field's rectangle.
        :param y: The vertical starting position of the memo field's rectangle.
        :param width: The width of the memo field's rectangle.
        :param height: The height of the memo field's rectangle.
        :param text: The text to be displayed in the memo, default= ""
    """

    def __init__(self, tag_name, surface, x, y, width, height, text=""):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        self.__caption = text.decode('utf-8')
        self.__caption_lines = []
        self.alignment_horizontal = HOR_LEFT
        self.indent_horizontal = 0
        self.outline_show = False
        self.outline_color = C_BLUE
        self.background_alpha = 255

    def draw(self, text=None):
        if text is not None:
            self.__caption = text.decode('utf-8')
        # Draw background
        background = pygame.Surface((self.width, self.height))
        background.set_alpha(self.background_alpha)
        background.fill(self.background_color)
        SCREEN.blit(background, (self.x_pos, self.y_pos))
        # Draw outline
        if self.outline_show:
            pygame.draw.rect(self.surface, self.outline_color, self.rect, 1)
        # Draw text lines
        self.__wrap_caption()
        line_height = self.font.size("jP")[1]
        max_lines = self.height / (line_height + 2)
        line_no = 0
        for line in self.__caption_lines:
            image = FONT.render(line, True, self.font_color)
            self.surface.blit(image, (self.x_pos, self.y_pos + (line_no * line_height)))
            line_no += 1
            if line_no > max_lines:
                break
        pygame.display.update(self.rect)

    def transparent_set(self, value):
        """ Turns background transparent or opaque. """
        if value is True:
            self.background_alpha = 0
        else:
            self.background_alpha = 255

    def set_alignment(self, horizontal, hor_indent=0):
        """ Sets the horizontal alignment of the lines. """
        self.alignment_horizontal = horizontal
        self.indent_horizontal = hor_indent

    def __truncate_line(self):
        split_text = self.__caption
        label_width = self.font.size(self.__caption)[0]
        cut = 0
        a = 0
        done = True
        while label_width > self.width:
            a += 1
            n = self.__caption.rsplit(None, a)[0]
            if split_text == n:
                cut += 1
                split_text = n[:-cut]
            else:
                split_text = n
            label_width = self.font.size(split_text)[0]
            done = False
        return done, split_text

    def __wrap_caption(self):
        done = False
        self.caption_lines = []
        while not done:
            done, split_text = self.__truncate_line()
            self.__caption_lines.append(split_text.strip())
            self.__caption = self.__caption[len(split_text):]
            pass


class ButtonIcon(Widget):
    """ ButtonIcon class is a button that only displays an icon.

        :param tag_name: Text identifying the widget,
        :param screen_rect: The screen's rectangle where the button should be drawn,
        :param x: The horizontal position of the button,
        :param y: The vertical position of the button,

        :ivar caption: The button's caption,
        :ivar image_file: The button's icon image file name,
    """

    def __init__(self, tag_name, surface, image, x, y):
        self.image_file = image
        self.__icon = self.get_image(self.image_file)
        Widget.__init__(self, tag_name, surface, x, y, self.__icon.get_width(), self.__icon.get_height())
        self.caption = ""

    @staticmethod
    def get_image(image_file):
        with zipfile.ZipFile(RESOURCES_ZIP) as res:
            img = res.read(image_file)
        bytes_io = io.BytesIO(img)
        return pygame.image.load(bytes_io)

    def draw(self, icon_file=None):
        """ Draws the button """
        if icon_file is not None:
            self.image_file = icon_file
            self.__icon = self.get_image(self.image_file)
        self.rect = self.surface.blit(self.__icon, (self.x_pos, self.y_pos))
        pygame.display.update(self.rect)

    def icon_file_set(self, icon_file):
        self.image_file = icon_file
        self.__icon = self.get_image(self.image_file)

    def set_image_file(self, file_name):
        """ Sets the buttons icon.

            :param file_name: Points to the icon's file name.
        """
        self.image_file = file_name
        self.__icon = self.get_image(self.image_file)
        self.width = self.__icon.get_width()
        self.height = self.__icon.get_height()
        self.draw()


class ButtonText(LabelText):
    """ ButtonText class is a button with text that uses two images for button rendering.

        :param tag_name: Text identifying the widget,
        :param surface: The screen's rectangle where the button should be drawn,
        :param x: The horizontal position of the button,
        :param y: The vertical position of the button,
        :param width: The label's rectangle width,
        :param text: default "", The label's caption,

        :ivar transparent: Whether the label's background is transparent, default = False,
        :ivar font_color: The text font color,
        :ivar alignment_horizontal: The button's text horizontal alignment, default = :py:const:HOR_MID.
        :ivar alignment_vertical: The button's text vertical alignment, default = :py:const:VERT_MID,
    """

    def __init__(self, tag_name, surface, x, y, width, height, text=""):
        LabelText.__init__(self, tag_name, surface, x, y, width, height, text)
        self.transparent_set(True)
        self.button_rect = (x + 1, y + 1, width - 2, height - 2)
        self.button_color = C_GREY_DARK
        self.__background_left = None
        self.__background_middle = None
        self.__background_right = None
        self.transparent = True
        self.font_color = C_BLUE
        self.alignment_vertical = VERT_MID
        self.alignment_horizontal = HOR_MID
        self.outline_show = True
        self.outline_color = C_BLUE

    def draw(self, text=None):
        self.surface.fill(self.button_color, self.button_rect)  # Background
        if text is not None:
            self.caption = text
        super(ButtonText, self).draw()
        pygame.display.update(self.rect)


class Switch(Widget):
    """ An on/off control for settings

        :param tag_name: Text identifying the widget,
        :param surface: The screen's rectangle where the button should be drawn,
        :param x: The horizontal position of the button,
        :param y: The vertical position of the button,
    """

    def __init__(self, tag_name, surface, x, y):
        self.__icon_on = self.get_image(ICO_SWITCH_ON)
        self.__icon_off = self.get_image(ICO_SWITCH_OFF)
        self.width = self.__icon_on.get_width()
        self.height = self.__icon_on.get_height()
        Widget.__init__(self, tag_name, surface, x, y, self.width, self.height)
        self.__is_on = False

    @staticmethod
    def get_image(image_file):
        with zipfile.ZipFile(RESOURCES_ZIP) as res:
            img = res.read(image_file)
        bytes_io = io.BytesIO(img)
        return pygame.image.load(bytes_io)

    def set_on(self, boolean):
        """ Turns the control status to on or off.

            :param boolean: Boolean determining whether the control is in the 'on' state.
        """
        self.__is_on = boolean
        self.draw()

    def get_on(self):
        """ Retrieved the on status of the control.

            :return: Boolean indicating whether control has 'on' status
        """
        return self.__is_on

    def on_click(self, x, y):
        self.surface.fill(self.background_color, self.rect)
        self.__is_on = not self.__is_on
        self.draw()
        return self.tag_name

    def draw(self):
        if self.__is_on:
            rect = self.surface.blit(self.__icon_on, (self.x_pos, self.y_pos))
        else:
            rect = self.surface.blit(self.__icon_off, (self.x_pos, self.y_pos))
        pygame.display.update(rect)


class ItemList(Widget):
    """ List of text items that can be clicked.

        :param tag_name: Text identifying the list.
        :param surface: The screen's rectangle where the list is drawn on.
        :param x: The horizontal starting position of the list's rectangle.
        :param y: The vertical starting position of the list's rectangle.
        :param width: The width of the list's rectangle.
        :param height: The height of the list's rectangle.

        :ivar list: List containing items for ItemList.
        :ivar outline_visible: Indicates whether the outline of the list is visible, default = True.

        :ivar item_height: The height of one list item, default = 25.
        :ivar item_indent: The indent for the text of a list item, default = 2.
        :ivar item_alignment_horizontal: Horizontal alignment of an item's text, default = :py:const:HOR_LEFT.
        :ivar item_alignment_vertical: Vertical alignment of an item's text, default = :py:const:VERT_MID.
        :ivar item_outline_visible: Boolean for displaying the rectangle of an item, default = False.

        :ivar active_item_index: The index of the currently active list item. It differs from selected in that it is set
                                 by the program and not by the user, default = -1.
        :ivar item_active_color: The active list item for color, default = :py:const:BLUE.
        :ivar item_active_background_color: The active list item background color, default = :py:const:WHITE.
        :ivar item_selected_index: The index of the selected list item, default = -1.
        :ivar item_selected_color: The font color of a selected item, default = :py:const:BLUE.
        :ivar item_selected_background_color: The selected list item background color, default = :py:const:WHITE.
    """

    def __init__(self, tag_name, surface, x, y, width, height):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        self.list = []
        self.outline_visible = True

        self.item_height = FONT_SPACE
        self.item_indent = SPACE
        self.item_alignment_horizontal = HOR_LEFT
        self.item_alignment_vertical = VERT_MID
        self.item_outline_visible = False

        self.active_item_index = -1
        self.item_active_color = BLUE
        self.item_active_background_color = WHITE

        self.item_selected_index = -1
        self.item_selected_color = BLUE
        self.item_selected_background_color = WHITE

        self.items_per_page = (self.height - 2 * self.item_indent) / self.item_height  # Maximum number
        self.page_showing_index = 0  # Index of page currently showing

    def set_item_alignment(self, horizontal, vertical):
        """ Sets the alignment of the text of an item within the item's rectangle. """
        self.item_alignment_horizontal = horizontal
        self.item_alignment_vertical = vertical

    def draw(self):
        """ Draws the item list on screen. """
        self.surface.fill(self.background_color, self.rect)
        if self.outline_visible:
            pygame.draw.rect(self.surface, self.outline_color, self.rect, 1)
        pygame.display.update(self.rect)
        self.draw_items()
        self.draw_page_indicator()
        pygame.display.flip()

    def draw_page_indicator(self):
        """ Draws a 'progress' indicator on the list. """
        if self.pages_count() > 1:
            indicator_width = LIST_INDICATOR_WIDTH
            indicator_height = self.height / self.pages_count()
            indicator_x = self.x_pos + self.width - indicator_width
            indicator_y = self.y_pos + self.page_showing_index * indicator_height
            indicator = Rect(indicator_x, indicator_y, indicator_width, indicator_height)
            pygame.draw.rect(self.surface, C_YELLOW, indicator)

    def draw_items(self):
        """ Draws the list items. """
        # Do not draw items when there are none
        if self.list is None:
            return
        # Populate the ItemList with items
        item_nr = 0
        item_start = self.page_showing_index * self.items_per_page
        while item_nr + item_start < len(self.list) and item_nr < self.items_per_page:
            item_text = self.list[item_nr + item_start]  # Get item text from list
            item_x_pos = self.x_pos + self.item_indent                                     # x position of item
            item_width = self.width - 2 * self.item_indent - SPACE - LIST_INDICATOR_WIDTH  # Maximum item width
            item_y_pos = self.y_pos + self.item_indent + (self.item_height * item_nr)      # y position of item
            list_item = LabelText('lbl_item_' + str(item_nr), self.surface, item_x_pos, item_y_pos, item_width,
                                  self.item_height, item_text)  # Create label
            list_item.font_color = self.font_color
            list_item.outline_visible = self.item_outline_visible
            if item_nr + item_start == self.active_item_index:  # Give active item designated colour
                list_item.font_color = self.item_active_color
            list_item.set_alignment(self.item_alignment_horizontal, self.item_alignment_vertical)
            list_item.draw()  # Draw item on screen
            item_nr += 1

    def clicked_item(self, x_pos, y_pos):
        """ Determines which item, if any, was clicked.

            :param x_pos: The click's horizontal position
            :param y_pos: The click's vertical position

            :return: The index of the selected list item
        """
        x_pos = x_pos - self.x_pos
        y_pos = y_pos - self.y_pos
        if x_pos < 0 or x_pos > self.width or y_pos < 0:  # Check whether the click was outside the control
            self.item_selected_index = -1
            return None
        # Check whether no item was clicked
        if y_pos > self.height or (
                self.page_showing_index * self.items_per_page + (y_pos + 2)) / self.item_height >= len(self.list):
            self.item_selected_index = -1
            return None
        self.item_selected_index = (self.page_showing_index * self.items_per_page + (y_pos + 2) / self.item_height)
        return self.item_selected_index

    def pages_count(self):
        """ :return: The number of pages filled with list items. """
        items_count = len(self.list)
        page_count = int(math.ceil(items_count / self.items_per_page) + 1)
        return page_count

    def item_active_get(self):
        """ :return: active item text """
        return self.list[self.active_item_index]

    def item_active_index_set(self, index):
        if 0 <= index < len(list):
            self.active_item_index = index
            self.draw()

    def item_selected_get(self):
        """ :return: selected item's text """
        return self.list[self.item_selected_index] if 0 <= self.item_selected_index < len(self.list) else None

    def on_click(self, x_pos, y_pos):
        """ Relays click action to a list item.
        :param x_pos: The horizontal click position.
        :param y_pos: The vertical click position.

        :return: return the ListItem's tag_name.
        """
        self.clicked_item(x_pos, y_pos)
        return self.tag_name

    def show_next_items(self):
        """ Shows next page of items. """
        if self.page_showing_index * self.items_per_page + self.items_per_page < len(self.list):
            self.page_showing_index += 1
            self.draw()

    def show_prev_items(self):
        """ Shows previous page of items. """
        if self.page_showing_index * self.items_per_page > 0:
            self.page_showing_index -= 1
            self.draw()
        else:
            self.page_showing_index = 0

    def show_item_active(self):
        page_no = 0
        while self.active_item_index > (page_no + 1) * self.items_per_page:
            page_no += 1
        self.page_showing_index = page_no
        self.draw()


class WidgetContainer(Widget):
    """ Basic screen used for displaying widgets. This type of screen should be used for the entire program.

        :param surface: The screen's rectangle where the screen is drawn on

        :ivar components: Dictionary holding the screen's widgets with a tag_name as key and the widget as value
    """

    def __init__(self, tag_name, surface, x, y, width, height):
        Widget.__init__(self, tag_name, surface, x, y, width, height)
        self.components = {}  # Interface dictionary

    def add_component(self, widget):
        """ Adds components to component list, thus ensuring a component is found on a mouse event.

            :param widget: The widget that should be added to the dictionary.
        """
        self.components[widget.tag_name] = widget

    def draw(self):
        """ Displays the screen. """
        self.surface.fill(self.background_color, self.rect)  # Background
        for key, value in self.components.items():
            if value.visible:
                value.draw()
        pygame.display.update(self.rect)

    def on_click(self, x, y):
        """ Determines which component was clicked and fires it's click function in turn.

            :param x: The horizontal click position.
            :param y: The vertical click position.

            :return: The tag_name of the clicked component.
        """
        for key, value in self.components.items():
            if isinstance(value, ButtonIcon) or isinstance(value, ButtonText) or \
                    isinstance(value, Switch) or isinstance(value, Slider) and value.visible or \
                    isinstance(value, Picture):
                if value.x_pos <= x <= value.x_pos + value.width and value.y_pos <= y <= value.y_pos + value.height:
                    value.on_click(x, y)
                    return key
            if isinstance(value, ItemList) and value.visible:
                if value.x_pos <= x <= value.x_pos + value.width and value.y_pos <= y <= value.y_pos + value.height:
                    value.clicked_item(x, y)
                    return key

    def on_swipe(self, x, y, swipe_type):
        """ Relays swipe to ItemList components for next(up)/previous(down) swipes for ItemLists.

            :param x: The horizontal start position of the swipe move.
            :param y: The vertical start position of the swipe move.
            :param swipe_type: The type of swipe movement done.
        """
        for key, value in self.components.items():
            if isinstance(value, ItemList):
                if value.x_pos <= x <= value.x_pos + value.width and value.y_pos <= y <= value.y_pos + value.height:
                    if swipe_type == GESTURE_SWIPE_UP:
                        value.show_next_items()
                    if swipe_type == GESTURE_SWIPE_DOWN:
                        value.show_prev_items()
