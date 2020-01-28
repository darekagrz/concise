from selenium.webdriver.common.by import By
import os


class WdCoreConfig:
    """
    Static class to be used for configuration
    """
    # Default "by" value for finding elements - Other options = [By.CSS_SELECTOR, By.ID, By.XPATH, By.CLASS_NAME, etc]
    DEFAULT_BY = By.NAME

    # Default timeout for finding elements
    DEFAULT_TIMEOUT = 10

    # Option to ignore stale elements when doing element binding
    IGNORE_STALE_ELEMENTS = True

    # Option to have the library verify that an element is visible before it attempts a click
    # This helps to avoid not-clickable errors due to timing / page load)
    CLICK_VISIBILITY_CHECK = True

    # Option to have the library verify that an element is visible before it attempts a click
    # This helps to avoid not-clickable errors due to timing / page load)
    ELEMENT_UNCLICKABLE_ATTEMPTS = 0

    # If the path to chromedriver is not in your environment path, it must be added here
    # Default matches the default used by selenium package
    CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')
