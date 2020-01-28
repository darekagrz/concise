import inspect
import time

from spotify.logger import StaticLogger


class GlobalRunVariables(object):
    pass


class Verification(object):

    __timeout = 20  # Add configuration option

    def function(self, func, expected_result=True, **kwargs):
        """
        Expects a func that takes a timeout and returns a boolean of success
        Does not throw an assert error if the func test fails
        """
        loop_wait = .5
        timeout = self.__timeout
        params = dict()
        fail_message = ''
        for key, val in kwargs.items():
            if str(key) == 'timeout':
                timeout = int(val)
            elif str(key) == 'loop_wait':
                loop_wait = int(val)
            elif str(key) == 'fail_message':
                fail_message = val
            else:
                params[key] = val

        found = not expected_result
        start_time = time.time()

        while not found and (time.time() - start_time <= timeout):
            if len(params) > 0:
                found = func(**params)
            else:
                found = func()

            if not found:
                time.sleep(loop_wait)

        assert found, fail_message

    def compare(self, actual, expected, fail_message=None):
        """
        Uses verify to perform a straight comparison. Actual can take a function
        signature or string value.
        This function will also format the fail message.
        :param expected: A string, int, float, boolean, or iterable to serve as
                         the expected value.
        :param actual: If this is a instance method, pass this in as a signature
                       (ie, no parenthesis).
        :param fail_message: Message to send to console on failure
        :return:
        """
        if inspect.ismethod(actual):
            self.function(lambda: actual() == expected,
                          fail_message=self.create_formatted_fail_message(expected,
                                                                          actual(),
                                                                          fail_message))
        else:
            assert actual == expected, self.create_formatted_fail_message(expected,
                                                                          actual,
                                                                          fail_message)

    def different(self, actual, expected, fail_message="Expected value to be different, but they are not"):
        """
        Uses verify to make sure provided arguments are different. Actual can take a function
        signature or string value.
        This function will also format the fail message.
        :param expected: A string, int, float, boolean, or iterable to serve as
                         the expected value.
        :param actual: If this is a instance method, pass this in as a signature
                       (ie, no parenthesis).
        :param fail_message: Message to send to console on failure
        :return:
        """
        if inspect.ismethod(actual):
            self.function(lambda: actual() != expected,
                          fail_message=self.create_formatted_fail_message(expected,
                                                                          actual(),
                                                                          fail_message))
        else:
            assert actual != expected, self.create_formatted_fail_message(expected,
                                                                          actual,
                                                                          fail_message)

    def contains(self, actual, expected, fail_message=None):
        """
        Uses verify to the expected is contained within the actual value. Actual can take a
             function signature, string value, or iterable.
             This function will also format the fail message.
        :param expected: A string, int, float, boolean, or iterable to serve as
                         the expected value.
        :param actual: If this is a instance method, pass this in as a signature
                       (ie, no parenthesis).
        :param fail_message: Message to send to console on failure
        :return:
        """
        if inspect.ismethod(actual):
            self.function(lambda: expected in actual(),
                          fail_message=self.create_formatted_fail_message(expected,
                                                                          actual(),
                                                                          fail_message))
        else:
            assert expected in actual, self.create_formatted_fail_message(expected,
                                                                          actual,
                                                                          fail_message)

    @staticmethod
    def create_formatted_fail_message(expected, actual, error_message=None):
        if error_message is None:
            error_message = 'The actual value does not match the expected value.'
        message = "{0}\nExpected: '{1}'\nActual: '{2}'".format(error_message, expected, actual)
        StaticLogger.logger.error(message)
        return message
