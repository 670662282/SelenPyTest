#coding:utf-8
import unittest
from SelenPyTest.pyselenium.models.driver import browser
from SelenPyTest.pyselenium.models.logs import Log
from SelenPyTest.pyselenium.webdriver.sele_api import ApiDriver

class TestCase(unittest.TestCase, ApiDriver):

    @classmethod
    def setUpClass(cls):
        cls.driver = browser('chrome')
        #cls.driver.maximize_window()
        cls.logger = Log().get_logger()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def except_parse(self, function, e):
        self.logger.exception(e)
        displayfield = function()
        self.logger.error(displayfield)
        if displayfield in ERROR_LIST:
            self.fail(displayfield)
        else:
            self.fail(ACCIDET_POPBOX + displayfield)
