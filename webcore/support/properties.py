from selenium.webdriver.support.color import Color


class ElementCss(object):

    def __init__(self, color, background_color, opacity, font, border, background_image):

        self.__color = Color.from_string(color)
        self.__background_color = Color.from_string(background_color)
        self.__opacity = opacity
        self.__font = font
        self.__border = border
        self.__background_image = background_image

    @property
    def border(self):
        return self.__border

    @property
    def color(self):
        """:rtype: Color"""
        return self.__color

    @property
    def background_color(self):
        """:rtype: Color"""
        return self.__background_color

    @property
    def opacity(self):
        return self.__opacity

    @property
    def font(self):
        return self.__font

    @property
    def background_image(self):
        return self.__background_image


class ElementLocation(object):

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def y(self):
        return self.__y

    @property
    def x(self):
        return self.__x


class ElementSize(object):

    def __init__(self, height, width):
        self.__height = height
        self.__width = width

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
