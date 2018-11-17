#coding:utf-8
#!/usr/bin/env python3
import sys
from time import sleep
from parameterized import parameterized
from SelenPyTest.pyselenium import browser, unit, TestRunner, sele_api
from SelenPyTest.pyselenium.untils.function import capture_except, get_png

class DemoTest(unit.TestCase):


    @parameterized.expand([
        ('test1', 'selenium'),
        ('test2', 'selenium2')
    ])
    @capture_except
    def test_login(self, fun, search_key):
        self.open("https://www.baidu.com")
        print('不好')
        self.find_element(css="#kw").send_keys(search_key)
        self.click_element(css="#su")
        #self.assertTitle(search_key)
        self.assertEqual(1, 2)

    def except_parse(self):
        #get_png()
        print('这里进行错误处理好么')

if __name__ == '__main__':
    TestRunner().normal()
