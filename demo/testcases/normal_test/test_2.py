# coding:utf-8
# !/usr/bin/env python3
import unittest

from parameterized import parameterized
from pyselenium.models import unittests
from pyselenium.untils.function import capture_except


def setUpModule():
    print('start UITest!')

# ToDo 全局设置error.png
# TODO listener 和capture_except  timeout 共存问题


class DemoTest2(unittests.TestCase):
    """hahahaha"""
    @parameterized.expand([
        ('test1', 'python'),
        ('test2', 'java')
    ])
    @capture_except(png_path=r'reports\images', retry=3)
    def test_login2(self, fun, search_key):
        """test_login_2"""
        self.open("https://www.baidu.com")
        self.find_element('#kw')
        # self.find_element_by_css('#aa')
        self.send_values(search_key, css="#kw")
        self.click_element(css="#su")
        # self.click_element(css="#aa")

        if fun == 'test2':
            self.assertEqual(11, 22)

    @capture_except()
    def test_subtest2(self):
        """test subtest_2"""
        self.open("https://www.baidu.com")
        for i in range(3):
            with self.subTest(msg="sub test第{}次测试".format(i), parrern=i):
                self.send_values(i, css="#kw")
                self.click_element(css="#su")
        self.assertEqual(22, 33)

    @unittest.skip('haha')
    def test_subtest3(self):
        """test subtest aaa"""
        self.open("https://www.baidu.com")
        for i in range(3):
            with self.subTest(parrern=i):
                self.send_values(i, css="#kw")
                self.click_element(css="#su")
