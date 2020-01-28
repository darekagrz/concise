import yaml
import os


class TestSuiteConfig(object):
    __instance = None
    __raw_dict = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(TestSuiteConfig, cls).__new__(cls, *args, **kwargs)
            cls.load_from_file()
        return cls.__instance

    @staticmethod
    def load_from_file():
        config_path = os.path.join(os.pathsep, os.path.dirname(__file__), "./config.yml")
        override_path = os.path.join(os.pathsep, os.path.dirname(__file__), "./config_override.yml")
        config = yaml.load(open(config_path).read(), Loader=yaml.SafeLoader)

        # check for a local override json file
        if os.path.isfile(override_path):
            override = yaml.load(open(override_path).read(), Loader=yaml.SafeLoader)
            if not(not isinstance(override, dict) or not override.get('override_config')):
                import collections

                def update(d, u):
                    for k, v in u.items():
                        if isinstance(v, collections.Mapping):
                            r = update(d.get(k, {}), v)
                            d[k] = r
                        else:
                            d[k] = u[k]
                    return d

                config = update(config, override)
        TestSuiteConfig.__raw_dict = config
        return config

    def get_config(self):
        return self.__raw_dict

    @property
    def run_type(self):
        return self.__raw_dict.get('run_type', {})

    @property
    def selected_run_type(self):
        return self.__raw_dict[self.run_type]

    @property
    def get_user(self):
        return self.selected_run_type.get('users', {})

    @property
    def browser_type(self):
        value = self.selected_run_type.get('browser_type', None)
        if isinstance(value, str):
            value = value.upper()
        return value

    @property
    def incognito_mode(self):
        value = self.selected_run_type.get('incognito_mode', None)
        if isinstance(value, bool):
            value = bool(value)
        return value

    @property
    def chromedriver_path(self):
        value = self.selected_run_type.get('chromedriver_path', None)
        if value is None:
            value = os.path.join(os.pathsep, os.path.dirname(os.path.realpath(__file__)), '..//externals//chromedriver')
            print('Chromedriver path: ' + value)
        return value

    @property
    def logging(self):
        return self.selected_run_type.get('logging', {})

    @property
    def log_level(self):
        return self.logging.get('log_level', 'INFO')

    @property
    def console(self):
        return self.logging.get('console', False)
