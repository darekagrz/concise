import pytest
from common.BaseTest import BaseTest
from spotify.fragments.loginpage import LoginPage
from spotify.fragments.mainpage import MainPage
from spotify.fragments.signuppage import SignUpPage
import time


class TestAcceptance(BaseTest):

    @pytest.mark.usefixtures("open_page")
    def test_registration_email_mismatch(self):
        main_page = MainPage()
        signup_page = SignUpPage()
        main_page.wait_for_load()
        main_page.signup()
        signup_page.wait_for_load()
        signup_page.set_email(email_addr='email1@test.local')
        signup_page.set_confirm_email(email_addr='email2@test.local')
        signup_page.password.click()
        self.verify.compare(signup_page.confirm_email_label.text(), self.s.EMAIL_MISMATCH)

    @pytest.mark.usefixtures("open_page")
    def test_incorrect_login(self):
        main_page = MainPage()
        login_page = LoginPage()
        main_page.wait_for_load()
        main_page.login()
        login_page.wait_for_load()
        login_page.login_attempt()
        login_page.wait_for_load()
        self.verify.compare(login_page.alert.text(), self.s.INCORRECT_LOGIN)
