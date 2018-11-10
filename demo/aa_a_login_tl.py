#coding:utf-8
#!/usr/bin/env python3
import sys
from time import sleep
from parameterized import parameterized
from SelenPyTest.pyselenium import browser, unit, TestRunner, sele_api

class DemoTest(unit.TestCase):

    @parameterized.expand([
        ('test1', 'selenium'),
        ('test2', 'selenium2')
    ])
    def test_login(self, funname, search_key):
        self.open("https://www.baidu.com")
        self.find_element(css="#kw").send_keys(search_key)
        self.click_element(css="#su")
        #self.assertTitle(search_key)

if __name__ == '__main__':
    TestRunner().normal()
