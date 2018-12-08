#coding:utf-8
#!/usr/bin/env python3
import sys
from time import sleep
from parameterized import parameterized
from SelenPyTest.pyselenium import browser, unit, TestRunner, sele_api
from SelenPyTest.pyselenium.untils.function import capture_except, get_png


def setUpModule():
    print('start UITest!')

def tearDownModule():
    print('end UITest!')

class DemoTest(unit.TestCase):
    """
    This is Test a
    """
    @parameterized.expand([
        ('test1', 'selenium'),
        ('test2', 'selenium2')
    ])
    @capture_except
    def test_login(self, fun, search_key):
        """
        test_login
        """
        self.open("https://www.baidu.com")
        self.find_element_by_css('#kw')
        #self.find_element_by_css('#aa')
        self.send_values(search_key, css="#kw")
        self.click_element(css="#su")
        #self.click_element(css="#aa")
        #self.assertTitle(search_key)
        self.assertEqual(1, 2)

    def testAssertRaises(self):
        """
        test result
        """
        print('cheng')
        #self.assertRaise(ValueError, fun, 1, 2)
    """
    def test_subtest(self):
        for i in range(5):
            with self.subTest(parrern=i):
                self.send_values(i, css="#kw")
                self.click_element(css="#su")
                self.assertEqual(1, 2)
    """
    def except_parse(self, driver):
        print('这里进行错误处理!')

if __name__ == '__main__':
    testRunner = TestRunner(cases="./", casecls_re='*.py', debug=False)
    testRunner.runner()
    report = testRunner.report_file

    #logfile = self.get_weblog()
    #if logfile is not None:
        #att_list.append(logfile)

    #Email(self.email_server, self.email_usr).send(
        #self.email_title, '自动化测试', self.email_receiver, report)
