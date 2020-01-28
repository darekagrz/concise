from selenium.webdriver.support.select import Select

import logging

from webcore.elements.element import Element


LOGGER = logging.getLogger(__name__)


class InputElement(Element):
    """Base object class for INPUT web elements."""

    def set(self, value):
        self.value(value)

    def get(self):
        return self.value()

    def value(self, value=None):
        """Gets the value of the specified object"""
        if value is None:
            return self.get_element().get_attribute("value")
        else:
            """Sets the value to the value supplied"""
            self.clear()
            self.get_element().send_keys(value)

    def clear(self):
        self.get_element().clear()


class CheckboxElement(InputElement):

    def value(self, value=None):
        if value is None:
            return self.get_element().is_selected()
        else:
            current_value = self.get_element().is_selected()
            if current_value is not value:
                self.get_element().click()


class RadioElement(InputElement):

    def value(self, value=None):
        if value is None:
            return self.get_element().is_selected()
        else:
            current_value = self.get_element().is_selected()
            if current_value is not value:
                self.get_element().click()


class SelectElement(Element):

    def get_element(self):
        """:rtype: Select"""
        element = super(SelectElement, self).get_element()
        return Select(element)

    def set(self, value):
        self.text(value)

    def get(self):
        return self.text()

    def text(self, text=None):
        """Gets the text of the specified object"""
        if text is None:
            return self.get_element().first_selected_option.get_attribute('text')
        else:
            self.get_element().select_by_visible_text(text)

    def value(self, value=None):
        if value is None:
            return self.get_element().first_selected_option.get_attribute('value')
        else:
            self.get_element().select_by_value(str(value))
