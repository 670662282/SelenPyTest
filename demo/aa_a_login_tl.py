#coding:utf-8
#!/usr/bin/env python3
import sys
from time import sleep
from parameterized import parameterized
from pyselenium import browser, unit, TestRunner, sele_api
from pyselenium.untils.function import capture_except, get_png


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
        self.find_element_by_css('#kw')
        #self.find_element_by_css('#aa')
        self.send_values(search_key, css="#kw")
        self.click_element(css="#su")
        #self.click_element(css="#aa")
        #self.assertTitle(search_key)
        self.assertEqual(1, 2)

    def testAssertRaises(self):
        """test result"""
        print('test assert')
        #self.assertRaise(ValueError, fun, 1, 2)

    def except_parse(self, driver):
        print('这里进行错误处理!')


"""
if __name__ == '__main__':
    testRunner = TestRunner(cases="./", casecls_re='*.py', debug=False, report_backup=3)
    testRunner.runner()
    report = testRunner.report_file
"""
    #logfile = self.get_weblog()
    #if logfile is not None:
        #att_list.append(logfile)

    #Email(self.email_server, self.email_usr).send(
        #self.email_title, '自动化测试', self.email_receiver, report)
