import unittest
from pyselenium.apis.sele_api import ApiDriver
from pyselenium.lib.log import print_color
from pyselenium.models.driver import get_driver


class TestCase(unittest.TestCase, ApiDriver):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver(is_listening=True)
        # cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def except_parse(self, exception, retry, fn, *args, **kwargs):
        print_color('这里进行错误处理')
        try:
            retry = int(retry)
        except ValueError:
            raise TypeError('retry must int type')

        for i in range(1, retry+1):
            try:
                fn(self, *args, **kwargs)
            except Exception:
                print_color('retry exec function:{} time'.format(i))
                if i == retry:
                    print_color('retry reach max time', 'red')
                    raise exception
            else:
                print_color('retry exec function success', 'yellow')
                break






