from selenium.webdriver.common.by import By

from webcore.elements.container import ContainerElement
from webcore.elements.display import DisplayElement
from webcore.elements.input import InputElement


class SignUpPage(ContainerElement):

    def __init__(self):
        self.email = InputElement('register-email', by=By.ID)
        self.confirm_email = InputElement('register-confirm-email', by=By.ID)
        self.password = InputElement('register-password', by=By.ID)

        '''*** Labels *** '''
        self.confirm_email_label = DisplayElement(".has-error[for='register-confirm-email']", by=By.CSS_SELECTOR)

        ContainerElement.__init__(self, locator='body.page-signup', by=By.CSS_SELECTOR)

    def wait_for_load(self):
        self.email.exists(timeout=3)
        self.email.is_visible(timeout=1)

    def set_email(self, email_addr: str = 'test@dummy.local'):
        self.email.set(email_addr)

    def set_confirm_email(self, email_addr: str = 'test@dummy.local'):
        self.confirm_email.set(email_addr)