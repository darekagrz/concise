from selenium.webdriver.common.alert import Alert
from webcore.wdcore_driver import WdCoreDriver
import time


class Page(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver=None):
        if driver is None:
            self.driver = WdCoreDriver.get_active_driver()
        else:
            self.driver = driver

    def get_page_title(self):
        return self.driver.title

    def execute_javascript(self, javascript):
        return self.driver.execute_script(javascript)

    def switch_to_window_by_title(self, title):
        current_windows = self.driver.window_handles
        for w in current_windows:
            self.driver.switch_to.window(w)
            if self.get_page_title() == title:
                return True
        return False

    @property
    def alert(self):
        """
        :rtype: Alert
        """
        return self.driver.switch_to.alert

    def accept_alert(self, alert_text='', accept_alert=True):
        time.sleep(3)
        alert = self.alert
        actual_text = alert.text
        if accept_alert == 1:
            alert.accept()
        else:
            alert.dismiss()
        if alert_text == '' or alert_text == actual_text:
            return True
        else:
            return False
