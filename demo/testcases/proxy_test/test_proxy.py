# coding:utf-8
# !/usr/bin/env python3

from pyselenium.models import unittests
from selenium import webdriver
from pyselenium.models.driver import get_driver


def setUpModule():
    print('start UITest!')


class DemoTest2(unittests.TestCase):
    """This is Test a2"""

    @classmethod
    def setUpClass(cls):
        ops = webdriver.ChromeOptions()
        ops.add_argument("--proxy-server=socks5://127.0.0.1:1080")
        cls.driver = get_driver('chrome', chrome_options=ops)

    def test_assert_raises(self):
        """test result"""
        print('test assert')
        self.open("http://speadmin.nxgvm.net")
        # self.assertRaise(ValueError, fun, 1, 2)

    def test_assert_raises_2(self):
        """1231231"""
        print('test assert')

        # self.assertRaise(ValueError, fun, 1, 2)

