import logging

import time
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement

from webcore.wdcore_config import WdCoreConfig
from webcore.support.properties import ElementCss, ElementLocation, ElementSize
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webcore.wdcore_driver import WdCoreDriver

LOGGER = logging.getLogger(__name__)


class Element(object):

    def __init__(self, locator, by=None, parent=None):
        """This class gets the search text from the specified locator"""

        # The locator for search box where search string is entered

        if by is not None:
            self.locator = locator
            self.locate_by = by
        elif isinstance(locator, str):
            self.locator = locator
            self.locate_by = WdCoreConfig.DEFAULT_BY
        else:
            self.locator = locator[1]
            self.locate_by = locator[0]

        self.__css = None
        self.__location = None
        self.__parent = parent
        self.__is_frame = False
        self.__timeout = WdCoreConfig.DEFAULT_TIMEOUT

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def is_frame(self):
        return self.__is_frame

    @is_frame.setter
    def is_frame(self, value):
        self.__is_frame = value

    def style(self):
        return self.get_element().get_attribute('style')

    def location(self):
        loc = self.get_element().location
        return ElementLocation(x=loc['x'], y=loc['y'])

    def size(self):
        size = self.get_element().size
        return ElementSize(height=size['height'], width=size['width'])

    def css(self, css_property=None):
        if css_property is None:
            if self.__css is None:
                self.__css = self.refresh_css_properties()
            return self.__css
        else:
            return self.get_element().value_of_css_property(css_property)

    def count(self):
        return len(self.get_elements())

    def exists(self, timeout=None):
        try:
            self.get_element(timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_visible(self, timeout=None):
        if self.exists(timeout=timeout):
            return self.get_element().is_displayed()
        else:
            return False

    def attribute(self, attr):
        return self.get_element().get_attribute(attr)

    def perform_find(self, context_element, multiple=False, timeout=None):
        if timeout is None:
            timeout = self.__timeout

        driver = WdCoreDriver.get_active_driver()

        if self.parent is not None and self.locate_by is By.XPATH and self.locator.startswith('/'):
            """
            Prepend the self notation for xpath if the user forgot it. The self xpath notation is required anytime
            a context element parent is used with xpath.
            """
            this_locator = '.' + self.locator
        else:
            this_locator = self.locator

        if multiple:
            return WebDriverWait(driver, timeout). \
                until(lambda driver: context_element.find_elements(self.locate_by, this_locator),
                      message='The Element could not be located. Locator: {0} By: {1}'.
                      format(self.locator, self.locate_by))
        else:
            try:
                el = WebDriverWait(driver, timeout). \
                    until(lambda driver: context_element.find_element(self.locate_by, this_locator),
                          message='The Element could not be located. Locator: {0} By: {1}'.
                          format(self.locator, self.locate_by))
                LOGGER.debug('Element located with id: {0}'.format(el.id))
                return el
            except (StaleElementReferenceException, WebDriverException) as exc:
                if WdCoreConfig.IGNORE_STALE_ELEMENTS \
                        and (isinstance(exc, StaleElementReferenceException)
                             or exc.msg.startswith('unknown error: Error is not a constructor')):
                    return self.get_element()
                else:
                    raise exc

    def get_parent(self):
        if self.parent is not None:
            if isinstance(self.parent, WebElement):
                context_element = self.parent
            else:
                context_element = self.parent.get_element()
        else:
            context_element = WdCoreDriver.get_active_driver()
            WdCoreDriver.reset_focus()
        return context_element

    def get_containing_frame(self):
        if self.parent is None:
            return None
        elif self.parent.is_frame:
            return self.parent
        else:
            return self.parent.get_containing_frame()

    def get_element(self, timeout=None):
        """
        Waits until the specified element is on screen. The returns the WebElement object once it is found.
        Default timeout is 10 seconds to allow for the object to appear.
        :rtype: WebElement
        """
        context_element = self.get_parent()

        return self.perform_find(context_element, timeout=timeout)

    def get_elements(self):
        """
        Waits until the specified elements are on screen. The returns a list of WebElement objects once it is found.
        Default timeout is 10 seconds to allow for the object to appear.
        """
        context_element = self.get_parent()

        return self.perform_find(context_element, multiple=True)

    def wait_for_disappearance(self, timeout=None):
        if timeout is None:
            timeout = self.__timeout

        context_element = self.get_parent()
        driver = WdCoreDriver.get_active_driver()

        if self.parent is not None and self.locate_by is By.XPATH and self.locator.startswith('/'):
            """
            Prepend the self notation for xpath if the user forgot it. The self xpath notation is required anytime
            a context element parent is used with xpath.
            """
            this_locator = '.' + self.locator
        else:
            this_locator = self.locator

        return WebDriverWait(driver, timeout). \
            until_not(lambda driver: context_element.find_element(self.locate_by, this_locator),
                      message='The Element could not be located. Locator: {0} By: {1}'.
                      format(self.locator, self.locate_by))

    def wait_for_enable_disable(self, enabled_state=True, timeout=None):
        if timeout is None:
            timeout = self.__timeout

        driver = WdCoreDriver.get_active_driver()

        if enabled_state:
            state = WebDriverWait(driver, timeout).until(lambda driver: self.get_element().is_enabled())
        else:
            state = WebDriverWait(driver, timeout).until_not(lambda driver: self.get_element().is_enabled())
        return state

    def click(self, x=None, y=None):
        element = self.get_element()
        # element.location_once_scrolled_into_view
        WdCoreDriver.get_active_driver().execute_script('return arguments[0].scrollIntoView(false);', element)
        start_time = time.time()
        while WdCoreConfig.CLICK_VISIBILITY_CHECK and not element.is_displayed():
            if time.time() - start_time > self.__timeout:
                raise TimeoutException(msg="Element with identifier {0} never became visible to click."
                                       .format(self.locator))

        if x is None and y is None:
            click_attempts = 0

            while click_attempts < WdCoreConfig.ELEMENT_UNCLICKABLE_ATTEMPTS:
                try:
                    element.click()
                    break
                except WebDriverException as e:
                    if not ('is not clickable at point' in e.msg) and not ('Unable to get element location' in e.msg):
                        # Raise the exception if it is any other kind of error.
                        raise e
                    else:
                        time.sleep(0.5)
                        click_attempts += 1
            else:
                element.click()

        else:
            ActionChains(WdCoreDriver.get_active_driver()).move_to_element_with_offset(element, x, y).click().perform()

    def double_click(self):
        element = self.get_element()
        ActionChains(WdCoreDriver.get_active_driver()).click(element).click().perform()

    def right_click(self):
        element = self.get_element()
        ActionChains(WdCoreDriver.get_active_driver()).context_click(element).perform()

    def mouse_over(self):
        element = self.get_element()
        ActionChains(WdCoreDriver.get_active_driver()).move_to_element(element).perform()

    def mouse_over_and_click(self):
        element = self.get_element()
        ActionChains(WdCoreDriver.get_active_driver()).click_and_hold(element).release().perform()

    def drag_to(self, destination, offset=None):
        if offset is None:
            offset = (5, 5)
        source = self.get_element()
        if isinstance(destination, tuple):
            ActionChains(WdCoreDriver.get_active_driver()).drag_and_drop_by_offset(source, *destination).perform()
        else:
            target = destination.get_element()
            ActionChains(WdCoreDriver.get_active_driver()).click_and_hold(source)\
                .move_to_element_with_offset(target, *offset).release().perform()

    def drag_and_hold(self, destination):
        source = self.get_element()
        if isinstance(destination, tuple):
            ActionChains(WdCoreDriver.get_active_driver())\
                .click_and_hold(source)\
                .move_by_offset(*destination)\
                .perform()
        else:
            target = destination.get_element()
            ActionChains(WdCoreDriver.get_active_driver()) \
                .click_and_hold(source) \
                .move_to_element(target) \
                .perform()

    def execute_javascript(self, javascript):
        driver = WdCoreDriver.get_active_driver()
        return driver.execute_script('return arguments[0].' + javascript, self.get_element())

    def refresh_css_properties(self):
        element = self.get_element()

        return ElementCss(color=element.value_of_css_property('color'),
                          background_color=element.value_of_css_property('background-color'),
                          opacity=element.value_of_css_property('opacity'),
                          font=element.value_of_css_property('font'),
                          border=element.value_of_css_property('border'),
                          background_image=element.value_of_css_property('background-image'))

    def add_child(self, element):
        element.parent = self

    def add_children(self, *elements):
        for element in elements:
            self.add_child(element)

    def add_all_element_instance_variables_as_children(self):
        items = dir(self)
        for item in items:
            if not item.startswith('_') and item != 'parent':
                value = self.__getattribute__(item)
                if isinstance(value, Element) and value.parent is None:
                    self.add_child(value)

    def element(self, locator, by=None):
        return Element(locator, by, self)
