import unittest
from pyselenium.models.driver import browser
from pyselenium.models.logs import Log
from pyselenium.webdriver.sele_api import ApiDriver
from pyselenium.untils.listener import MyListener
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium import webdriver


class TestCase(unittest.TestCase, ApiDriver):

    @classmethod
    def setUpClass(cls):
        ops = webdriver.ChromeOptions()
        cls.driver = EventFiringWebDriver(browser('chrome'), MyListener())
        # cls.driver.maximize_window()
        cls.logger = Log().get_logger()


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def except_parse(self, driver):
        print('这里进行错误处理')


