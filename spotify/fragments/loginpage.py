from selenium.webdriver.common.by import By
from webcore.elements.container import ContainerElement
from webcore.elements.display import DisplayElement
from webcore.elements.input import InputElement, CheckboxElement


class LoginPage(ContainerElement):

    def __init__(self):

        self.email_username = InputElement('login-username', by=By.ID)
        self.password = InputElement('login-password', by=By.ID)
        self.remember_me_checkbox = CheckboxElement('login-remember', by=By.ID)
        self.login_btn = DisplayElement('login-button', by=By.ID)
        self.alert = DisplayElement('p.alert', by=By.CSS_SELECTOR)

        ContainerElement.__init__(self, locator='div.login', by=By.CSS_SELECTOR)

    def wait_for_load(self):
        self.email_username.exists(timeout=3)
        self.email_username.is_visible(timeout=1)

    def set_email_username(self, email_addr: str = 'test@dummy.local'):
        self.email_username.set(email_addr)

    def set_password(self, pwd: str = 'foopassword'):
        self.password.set(pwd)

    def login_attempt(self,user_or_email: str = 'test@dummy.local', password: str = 'fu1dfuuu', remember: bool = False):
        if self.remember_me_checkbox.get() is not remember:
            self.remember_me_checkbox.element('following-sibling::span', By.XPATH).click()
        self.set_email_username(user_or_email)
        self.set_password(password)
        self.login_btn.click()

