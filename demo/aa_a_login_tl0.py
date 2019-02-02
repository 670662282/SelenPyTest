# coding:utf-8
# !/usr/bin/env python3

from pyselenium.models import unit
from pyselenium.untils.listener import MyListener
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium import webdriver
from pyselenium.models.driver import browser


def setUpModule():
    print('start UITest!')


class DemoTest2(unit.TestCase):
    """This is Test a2"""

    @classmethod
    def setUpClass(cls):
        ops = webdriver.ChromeOptions()
        ops.add_argument("--proxy-server=socks5://127.0.0.1:1080")
        cls.driver = EventFiringWebDriver(browser('chrome', chrome_options=ops), MyListener())

    def test_assert_raises(self):
        """test result"""
        print('test assert')
        self.open("http://speadmin.nxgvm.net")
        # self.assertRaise(ValueError, fun, 1, 2)

    def test_assert_raises_2(self):
        """1231231"""
        print('test assert')

        # self.assertRaise(ValueError, fun, 1, 2)

