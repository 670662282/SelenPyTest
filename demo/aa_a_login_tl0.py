#coding:utf-8
#!/usr/bin/env python3
import sys
from time import sleep
from parameterized import parameterized
from SelenPyTest.pyselenium import browser, unit, TestRunner, sele_api
from SelenPyTest.pyselenium.untils.function import capture_except, get_png


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


    def testAssertRaises2(self):
        """1231231"""
        print('test assert')

        #self.assertRaise(ValueError, fun, 1, 2)



    #Email(self.email_server, self.email_usr).send(
        #self.email_title, '自动化测试', self.email_receiver, report)
