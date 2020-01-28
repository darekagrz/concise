from selenium.webdriver.common.by import By

from webcore.elements.container import ContainerElement
from webcore.elements.display import DisplayElement


class MainPage(ContainerElement):

    def __init__(self):
        self.signup_link = DisplayElement("a[data-ga-action='sign-up']", by=By.CSS_SELECTOR)
        self.login_link = DisplayElement("a[href='https://www.spotify.com/pl/account/overview/']", by=By.CSS_SELECTOR)

        ContainerElement.__init__(self, locator='body.page-homepage', by=By.CSS_SELECTOR)

    def wait_for_load(self):
        self.signup_link.exists(timeout=3)
        self.signup_link.is_visible(timeout=1)

    def login(self):
        self.login_link.click()

    def signup(self):
        self.signup_link.click()
