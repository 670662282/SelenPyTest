# coding:utf-8
# !/usr/bin/env python3

from parameterized import parameterized

from pyselenium.apis.sele_api import ApiDriver
from pyselenium.models import unittests
from pyselenium.untils.function import capture_except


def setUpModule():
    print('start UITest!')

# TODO listener 和wait装饰器  timeout 共存问题


class DemoTest(unittests.TestCase):
    ApiDriver.png_path = 'reports'
    """This is Test a"""
    @parameterized.expand([
        ('test1', 'selenium'),
        ('test2', 'selenium2')
    ])
    @capture_except(png_path=r'reports\images', retry=2)
    def test_login(self, fun, search_key):
        """test_login"""
        self.open("https://www.baidu.com")
        self.find_element('#kw')
        # self.find_element_by_css('#aa')
        self.send_values(search_key, css="#kw")
        self.click_element(css="#su")
        # self.click_element(css="#aa")

        if fun == 'test2':
            self.assertEqual(1, 2)

    @capture_except()
    def test_subtest(self):
        """test subtest aaa"""
        self.open("https://www.baidu.com")
        for i in range(5):
            with self.subTest(parrern=i):
                self.send_values(i, css="#kw")
                self.click_element(css="#su")
        self.assertEqual(2, 3)


