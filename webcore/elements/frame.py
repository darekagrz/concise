import logging
from selenium.webdriver.support.wait import WebDriverWait

from webcore.elements.element import Element
from webcore.wdcore_driver import WdCoreDriver
from webcore.wdcore_config import WdCoreConfig

LOGGER = logging.getLogger(__name__)


class FrameElement(Element):
    """Base object class for Frame and Iframe web elements."""

    def __init__(self, locator, by=None, parent=None):
        Element.__init__(self, locator, by=by, parent=parent)
        self.add_all_element_instance_variables_as_children()
        self.is_frame = True

    def perform_find(self, context_element, timeout=None):
        if timeout is None:
            timeout = WdCoreConfig.DEFAULT_TIMEOUT
        driver = WdCoreDriver.get_active_driver()
        frame_reference = WebDriverWait(driver, timeout). \
            until(lambda driver: driver.find_element(self.locate_by, self.locator),
                  message='The Element could not be located. Locator: {0} By: {1}'.format(self.locator, self.locate_by))
        WdCoreDriver.get_active_driver().switch_to.frame(frame_reference)
        return driver
