import logging
from selenium import webdriver

from webcore.wdcore_config import WdCoreConfig

LOGGER = logging.getLogger(__name__)


class BrowserTypes(object):
    """All currently supported browser types for this package."""
    CHROME = 'CHROME'
    CHROME_HEADLESS = 'CHROME_HEADLESS'
    # IE = 'IE'
    # FIREFOX = 'FIREFOX'


class WdCoreDriver(object):
    """
    TODO - CWDriver DOCSTRING
    """

    # This holds the most currently set instance object of webdriver that was created so that it can be accessed
    # across the package.
    __currently_running_driver = None
    __main_window_handle = None

    def __init__(self, url=None, browser_type=BrowserTypes.CHROME, existing_driver=None,
                 driver_log=None, incognito=False):

        if existing_driver is not None:
            self.__driver = existing_driver

        elif browser_type is None:
            chrome_options = webdriver.ChromeOptions()
            if incognito:
                chrome_options.add_argument("--incognito")
            chrome_options.headless = True
            chrome_options.add_argument("--no-sandbox")
            self.__driver = webdriver.Chrome(
                executable_path=WdCoreConfig.CHROMEDRIVER_PATH,
                options=chrome_options, service_log_path=driver_log)

        elif browser_type.upper() == BrowserTypes.CHROME:
            chrome_options = webdriver.ChromeOptions()
            if incognito:
                chrome_options.add_argument("--incognito")
            self.__driver = webdriver.Chrome(
                executable_path=WdCoreConfig.CHROMEDRIVER_PATH, service_log_path=driver_log,
                options=chrome_options)
        elif browser_type.upper() == BrowserTypes.CHROME_HEADLESS:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--no-sandbox")
            if incognito:
                chrome_options.add_argument("--incognito")
            self.__driver = webdriver.Chrome(
                executable_path=WdCoreConfig.CHROMEDRIVER_PATH, service_log_path=driver_log,
                options=chrome_options)
        # elif browser_type.upper() == BrowserTypes.FIREFOX:
        #     profile = webdriver.FirefoxProfile()
        #     self.__driver = webdriver.Firefox(firefox_profile=profile)
        #
        # elif browser_type.upper() == BrowserTypes.IE:
        #     if driver_log is not None:
        #         self.__driver = webdriver.Ie(log_file=driver_log)
        #     else:
        #         self.__driver = webdriver.Ie()
        #     self.__driver.maximize_window()

        else:
            raise NotImplementedError('No valid browser_type was provided.')

        WdCoreDriver.__currently_running_driver = self.__driver
        WdCoreDriver.__main_window_handle = self.__driver.current_window_handle

        if url is not None:
            self.open_url(url)

    @staticmethod
    def get_active_driver():
        """
        :rtype: webdriver.Remote
        """
        if WdCoreDriver.__currently_running_driver is not None:
            return WdCoreDriver.__currently_running_driver
        else:
            # TODO - Implement a real error here. May need to create unique exceptions for the package.
            LOGGER.info('You attempted to get an active driver when none is running. '
                        'Please be sure to start the driver on setup on in your test first.')
            raise NotImplementedError

    @staticmethod
    def reset_focus():
        WdCoreDriver.__currently_running_driver.switch_to.window(WdCoreDriver.__main_window_handle)

    @property
    def driver(self):
        """
        :rtype: webdriver.Remote
        """
        return self.__driver

    def open_url(self, url):
        self.driver.get(url)
