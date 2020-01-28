from common.utils.verification import Verification


class BaseAction(object):

    def __init__(self):
        super(BaseAction, self).__init__()
        self.test = True
        self.verify = Verification()
