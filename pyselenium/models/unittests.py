import unittest
from pyselenium.apis.sele_api import ApiDriver
from pyselenium.lib.s_logs import Log
from pyselenium.models.driver import get_driver


class TestCase(unittest.TestCase, ApiDriver):

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        # cls.driver.maximize_window()
        cls.logger = Log()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def except_parse(self, driver):
        print('这里进行错误处理')


