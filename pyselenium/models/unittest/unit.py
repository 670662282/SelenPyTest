#coding:utf-8
import unittest
from SelenPyTest.pyselenium.models.driver import browser
from SelenPyTest.pyselenium.models.logs import Log
from SelenPyTest.pyselenium.webdriver.sele_api import ApiDriver
from SelenPyTest.pyselenium.untils.listener import MyListener
from selenium.webdriver.support.events import EventFiringWebDriver



class TestCase(unittest.TestCase, ApiDriver):

    @classmethod
    def setUpClass(cls):
        #cls.driver = browser('chrome')
        cls.driver = EventFiringWebDriver(browser('chrome'), MyListener())
        #cls.driver.maximize_window()
        cls.logger = Log().get_logger()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def except_parse(self, driver):
        print('这里进行错误处理')
