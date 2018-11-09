#coding:utf-8
from selenium import webdriver
from .driver import browser
import os, sys
import unittest
from .logs import Log
from .config import Config



class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        timeout = Config().get('IMP_TIME')
        self.driver = browser()
        #self.driver.maximize_window()
        self.driver.implicitly_wait(timeout if timeout else 15)
        self.logger = Log().get_logger()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def except_parse(self, function, e):
        self.logger.exception(e)
        displayfield = function()
        self.logger.error(displayfield)
        if displayfield in ERROR_LIST:
            self.fail(displayfield)
        else:
            self.fail(ACCIDET_POPBOX + displayfield)

    if __name__ == "__main__":
        unittest.main()
