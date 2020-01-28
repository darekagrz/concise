import pytest

from common.Constants import Strings
from common.utils.verification import Verification


class BaseTest(object):

    @classmethod
    @pytest.fixture(scope='function', autouse=True)
    def setup(cls):
        cls.test = True
        cls.verify = Verification()
        cls.s = Strings()
