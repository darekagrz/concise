import logging

from webcore.elements.element import Element

LOGGER = logging.getLogger(__name__)


class DisplayElement(Element):
    """Base object class for most non-INPUT web elements."""

    def get(self):
        return self.text()

    def get_all(self):
        els = self.get_elements()
        return [el.text for el in els]

    def text(self):
        """
        Gets the text property of the specified web element.

        text provides the text of the element and any sub-elements that have text.
        It removes whitespace including tabs, but not linebreaks.
        """
        return self.get_element().text

    def textcontent(self):
        """
        Gets the textContent property of the specified web element.

        textContent provides the text of the element and any sub-elements that have text.
        It does NOT remove whitespace.
        """
        return self.get_element().get_attribute("textContent")

    def innerhtml(self):
        """
        Gets the innerHTML property of the specified web element.

        innerHTML provides the full html contained inside of the element.
        Any element text that is included does NOT remove whitespace.
        """
        return self.get_element().get_attribute("innerHTML")

    def innertext(self):
        """
        Gets the innerText property of the specified web element.

        innerText provides the text of the element and any sub-elements that have text.
        It REMOVES whitespace but not tabs or linebreaks.
        """
        return self.get_element().get_attribute("innerText")
