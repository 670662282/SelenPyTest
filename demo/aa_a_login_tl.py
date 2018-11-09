#coding:utf-8
#!/usr/bin/env python3
from time import sleep
import unittest, random, sys
sys.path.append('./models')
sys.path.append('./page_obj')

from models import unit, function
from page_obj.loginPage import login
from parameterized import parameterized

class loginTest(unit.MyTest):
    """login test"""

    #user login  test
    def user_login_verify(self, username="", password="", randcode=""):
        login(self.driver).user_login(username, password, randcode)

    @parameterized.expand([
        ('all_empty', '', '', '', "不能为空"),
        ('passwd_randcode_empty', 'admin', '', '', '不能为空'),
        ('username_randcode_empty', '', '123456', '', '不能为空'),
        ('randcode_empty', 'admin', '123456', '', '不能为空'),
        ('username_passwd_error', 'admin', 'a23233', 'D9C0A', '用户名或密码不正确'),
        ('login_and_logout', 'admin', '123456', 'D9C0A', '欢迎登录'),
    ])
    def test_login(self, name, username, password, randcode, assert_text):
        class BaiduPage(PageObject):
            search_key = PageElement(id_='kw')
            search_button = PageElement(id_='su')
                # 定位一组元素
            search_result = PageElements(xpath="//div/h3/a")

            driver = webdriver.Chrome()
            page = BaiduPage(driver)
            page.get("https://www.baidu.com")
            page.search_key.send_keys("selenium")
            page.search_button.click()
            sleep(2)

            for result in page.search_result:
                print(result.text)

    if __name__ == "__main__":
        unittest.main()
