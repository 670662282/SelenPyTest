import importlib
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from common.error import BrowserNoFoundError
from pyselenium.lib.log import print_color, get_logger
from pyselenium.untils.function import find_alias, import_config_py


def chrome_headless():
    ops = Options()
    ops.add_argument('--headless')
    return webdriver.Chrome(chrome_options=ops)


BROWSERS = {
    'chrome':           webdriver.Chrome,
    'chrome_headless':  chrome_headless,
    'firefox':          webdriver.Firefox,
    'ie':               webdriver.Ie,
    'opera':            webdriver.Opera,
    'edge':             webdriver.Edge,
}


def browser(bro, **kwargs):
    bro = bro.lower()
    fun = BROWSERS.get(bro, False)
    if fun:
        return fun(**kwargs)
    else:
        alias_key = find_alias(bro, BROWSERS)
        if alias_key:
            print_color("input %s alias %s" % (bro, alias_key))

    raise BrowserNoFoundError("Not found '%s' browser, please use 'chrome' ,"
                              "'chrome_headless', 'opera', 'edge', 'ie' browser." % bro)


def get_driver(bro='chrome', disabled_log=False, **kwargs):
    return EventFiringWebDriver(browser(bro, **kwargs), EventListener(disabled_log))


class EventListener(AbstractEventListener):
    """ Listener driver"""
    def __init__(self, disabled_log, timeout=10):
        self.logger = get_logger()
        self.logger.disabled = disabled_log
        try:
            self.element_wait = int(timeout)
        except ValueError:
            raise TypeError('timeout type error!')

    def before_navigate_to(self, url, driver):
        self.logger.debug("Before navigate to %s" % url)

    def after_navigate_to(self, url, driver):
        self.logger.debug("After navigate to %s" % url)

    def before_find(self, by, value, driver):
        # TODO 模糊定位 通过特定相识度算法 当控件发生细微变化 这个控件依旧可以准确定位
        # 引入规则引擎 规则-配置文件方式
        """wait element!"""
        break_flag = False
        if self.element_wait:
            for i in range(self.element_wait*10):
                objs = driver.find_elements(by, value)
                if len(objs) != 0:
                    for obj in objs:
                        if obj.is_displayed:
                            break_flag = True
                            break
                    if break_flag:
                        break
                sleep(0.1)
            else:
                self.logger.warning("element NoSuchElement or Invisible, locs:({}, {})".format(by, value))
                self._exception_parse()

    def after_find(self, by, value, driver):
        self.logger.debug('元素定位: ({}, {})'.format(by, value))

    def before_change_value_of(self, element, driver):
        if driver.switch_to.active_element != element:
            print_color('active_element != current element')
        if self._check_element_status(element):
            self._exception_parse()
        if element.get_attribute('value'):
            self.logger.debug('before_change :value=%s' % element.get_attribute('value') or 'None')

    def after_change_value_of(self, element, driver):
        self._change_js_attr(element, driver)
        if element.get_attribute('value'):
            self.logger.debug('after_change :value=%s' % element.get_attribute('value') or 'None')

    def _get_element_attr(self, element):
        if not isinstance(element, WebElement):
            raise TypeError('{} is not WebElment instance'.format(element))
        return 'element: tag={}, id={}, name={}, class={}, text={}'.format(
                        element.tag_name,
                        element.get_attribute('id') or 'None',
                        element.get_attribute('name') or 'None',
                        element.get_attribute('class') or 'None',
                        element.text or 'None')

    def before_click(self, element, c):
        self._change_js_attr(element, driver)
        element_str = self._get_element_attr(element)

        if element.tag_name in ['checkbox', 'radio']:
            status = 'is selected' if element.lower().is_selected() else 'is not selected'
            self.logger.debug('{} 元素 {} 状态'.format(element_str, status))
        if self._check_element_status(element):
            self._exception_parse(driver)

    def _check_element_status(self, element):
        element_str = self._get_element_attr(element)
        if not element.is_displayed():
            self.logger.warning('%s 元素不可以见' % element_str)
            return False
        if not element.is_enabled():
            self.logger.warning('%s 元素disabled状态' % element_str)
            return False
        return True

    def _exception_parse(self, driver):
        # TODO 截图
        # 非预期窗口弹出处理
        # 控件无法操作(send_，click) 无法定位的时候
        # 进入异常恢复模式，检查各种可能的出现的对话框(从异常场景库中寻找)
        # 确认对话框类型后进行重试 刚才失败的步骤
        # 定位 动态加载异常库
        locs = import_config_py()
        for name, value in locs.items():
            elements = driver.find_elements(*value)
            if len(elements) == 1:
                print_color("定位到{}的元素".format(name))
                elements[0].click()
                break
            if len(elements) > 1:
                print_color("警告：异常弹框定位库定位到{}个元素".format(len(elements)), 'red')
        else:
            self.logger.warning("no found in no_exception_window.py")

    @staticmethod
    def _change_js_attr(element, driver, attr='2px solid red'):
        driver.execute_script('q=document.getElementById("{}");q.style.border=\"{}\";'.
                              format(element.get_attribute('id'), attr))

    def after_click(self, element, driver):
        self.logger.info("<id:{}> element be clicked".format(element.get_attribute('id')))

    def before_quit(self, driver):
        self.logger.debug('页面即将关闭')

    def after_quit(self, driver):
        self.logger.debug('页面已经关闭')

    def on_exception(self, exception, driver):
        pass


if __name__ == "__main__":
    driver = browser('chrome')
    driver.get("http://www.baidu.com")
    from selenium.webdriver.support.color import Color

    print(Color.from_string('#00ff33').rgba)
    print(Color.from_string('rgb(1, 255, 3)').hex)
    print(Color.from_string('blue').rgba)


