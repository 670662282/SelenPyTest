# coding:utf-8
# !/usr/bin/env python3

from parameterized import parameterized
from pyselenium import unit
from pyselenium.untils.function import capture_except
from time import sleep


def setUpModule():
    print('start UITest!')


class DemoTest(unit.TestCase):
    """This is Test a"""
    @parameterized.expand([
        ('test1', 'selenium'),
        ('test2', 'selenium2')
    ])
    @capture_except
    def test_login(self, fun, search_key):
        """test_login"""
        self.open("https://www.baidu.com")
        self.find_element('#kw')
        # self.find_element_by_css('#aa')
        self.send_values(search_key, css="#kw")
        self.click_element(css="#su")
        # self.click_element(css="#aa")
        # self.assertTitle(search_key)
        self.assertEqual(1, 2)

    def test_subtest(self):
        """test subtest aaa"""
        self.open("https://www.baidu.com")
        for i in range(5):
            with self.subTest(parrern=i):
                self.send_values(i, css="#kw")
                self.click_element(css="#su")

    def except_parse(self, driver):
        print('这里进行错误处理!')


"""
if __name__ == '__main__':
    testRunner = TestRunner(cases="./", casecls_re='*.py', debug=False, report_backup=3)
    testRunner.runner()
    report = testRunner.report_file
"""
