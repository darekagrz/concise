import pytest
from webcore.wdcore_config import WdCoreConfig
from selenium.webdriver.common.by import By

from spotify.config import TestSuiteConfig
from spotify.logger import StaticLogger
from webcore.wdcore_driver import WdCoreDriver

suite_config = TestSuiteConfig()

WdCoreConfig.DEFAULT_BY = By.CSS_SELECTOR
WdCoreConfig.DEFAULT_TIMEOUT = 20
WdCoreConfig.CHROMEDRIVER_PATH = suite_config.chromedriver_path
WdCoreConfig.CLICK_VISIBILITY_CHECK = True
WdCoreConfig.ELEMENT_UNCLICKABLE_ATTEMPTS = 40


# <editor-fold desc="TearDown">
@pytest.fixture(scope="class", autouse=True)
def teardown_steps(request):
    def final():
        # Add teardown here
        WdCoreDriver.get_active_driver().quit()

    request.addfinalizer(final)
# </editor-fold>


@pytest.fixture(scope="class")
def open_page_class():
    WdCoreDriver(suite_config.selected_run_type['site']['url'], browser_type=suite_config.browser_type,
                 incognito= suite_config.incognito_mode)
    WdCoreDriver.get_active_driver().maximize_window()


@pytest.fixture(scope="function")
def open_page():
    WdCoreDriver(suite_config.selected_run_type['site']['url'], browser_type=suite_config.browser_type,
                 incognito= suite_config.incognito_mode)
    WdCoreDriver.get_active_driver().maximize_window()


@pytest.fixture(scope="session", autouse=True)
def start_log():
    """
    A fixture to startup the webdriver and navigate to the test site
    before every test.
    """
    StaticLogger.start()


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    # execute all other hooks to obtain the report object
    rep = __multicall__.execute()

    # we only look at actual failing test calls, not setup/teardown

    if (rep.when == "call" or rep.when == "setup") and rep.failed:
        StaticLogger.take_screenshot(rep.nodeid[rep.nodeid.rfind("::")+2:])

    return rep
