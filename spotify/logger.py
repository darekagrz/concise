import logging
import os
import datetime

from webcore.wdcore_driver import WdCoreDriver
from spotify.config import TestSuiteConfig


class StaticLogger:
    started = False
    logger = None

    __console_handler = None

    def __init__(self):
        if not StaticLogger.started:
            StaticLogger.start()

    @staticmethod
    def start():

        config = TestSuiteConfig()
        desired_level = logging.getLevelName(config.log_level)   # Put config level here

        log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
        dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        StaticLogger.started = True
        root_logger = logging.getLogger()
        root_logger.setLevel(desired_level)
        log_format = '%(asctime)s [%(levelname)s] %(name)s %(message)s'
        log_handler = logging.FileHandler('{0}/{1}.log'.format(log_dir, dt_now))
        log_formatter = logging.Formatter(log_format)
        log_handler.setFormatter(log_formatter)
        root_logger.addHandler(log_handler)

        StaticLogger.logger = logging.getLogger('hempbombs_tests')

        if config.console:  # Put console flag here
            console_format = '[%(levelname)s] %(name)s %(message)s'
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(console_format)
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)

    @staticmethod
    def take_screenshot(filename=None):
        current_test_info = os.environ.get('PYTEST_CURRENT_TEST').split('::')
        # Getting this info in case we need to add it in the future
        test_class_name = current_test_info[1]
        test_name = current_test_info[2].split(' ')[0]

        if filename is None:
            filename = '{0}-{1}'.format(test_class_name, test_name)

        screen_shots_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'screenshots')

        # Create the filename using the filename and the current timestamp
        current_time = datetime.datetime.now()
        filename = '{filename}_{timestamp}.png'.format(
            filename=filename, timestamp=current_time.strftime('%m-%d-%H%M%S')
        )
        full_file_path = os.path.join(screen_shots_folder, filename)
        WdCoreDriver.get_active_driver().save_screenshot(full_file_path)
