# coding:utf-8
# !/usr/bin/env python3

from pyselenium import unit


def setUpModule():
    print('start UITest!')


class DemoTest2(unit.TestCase):
    """This is Test a2"""
    def test_subtest(self):
        """test subtest aaa"""
        self.open("https://www.baidu.com")
        for i in range(5):
            with self.subTest(parrern=i):
                self.send_values(i, css="#kw")
                self.click_element(css="#su")

    def test_assert_raises_2(self):
        """1231231"""
        print('test assert')

        # self.assertRaise(ValueError, fun, 1, 2)

