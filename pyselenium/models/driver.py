from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from common.error import BrowserNoFoundError
from pyselenium.lib.s_logs import Log
from pyselenium.untils.function import find_alias
logger = Log()


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
            logger.print_color("input %s alias %s" % (bro, alias_key))

    raise BrowserNoFoundError("Not found '%s' browser, please use 'chrome' ,"
                              "'chrome_headless', 'opera', 'edge', 'ie' browser." % bro)


def get_driver(bro='chrome', is_listening=False, **kwargs):
    return EventFiringWebDriver(browser(bro, **kwargs),
                                MyListener()) if is_listening else browser(bro)


class MyListener(AbstractEventListener):
    """ Listener driver"""
    def __init__(self, timeout=0):
        self.logger = Log()
        try:
            self.element_wait = int(timeout)
        except ValueError:
            raise TypeError('timeout type error!')

    def before_navigate_to(self, url, driver):
        self.logger.info("Before navigate to %s" % url)

    def after_navigate_to(self, url, driver):
        self.logger.info("After navigate to %s" % url)

    def before_find(self, by, value, driver):
        # TODO Refoact this function
        """wait element!"""
        if self.element_wait:
            for i in range(self.element_wait*10):
                objs = driver.find_elements(by, value)
                if len(objs) != 0:
                    for obj in objs:
                        if obj.is_displayed:
                            break
                        else:
                            sleep(0.1)
                    break
                else:
                    sleep(0.1)
            else:
                raise TimeoutError("element NoSuchElement or Invisible, locs:({}, {})".format(by, value))

    def after_find(self, by, value, driver):
        self.logger.info('元素定位: ({}, {})'.format(by, value))

    def before_change_value_of(self, element, driver):
        self.logger.info('before_change :value=%s' % element.get_attribute('value') or 'None')

    def after_change_value_of(self, element, driver):
        self.logger.info('after_change :value=%s' % element.get_attribute('value') or 'None')

    def _get_element_attr(self, element):
        if not isinstance(element, WebElement):
            raise TypeError('{} is not WebElment instance'.format(element))
        return 'element: tag={}, id={}, name={}, class={}, text={}'.format(
                        element.tag_name,
                        element.get_attribute('id') or 'None',
                        element.get_attribute('name') or 'None',
                        element.get_attribute('class') or 'None',
                        element.text or 'None')

    def before_click(self, element, driver):
        element_str = self._get_element_attr(element)
        tag = element.tag_name
        if not element.is_displayed():
            self.logger.warning('%s 元素不可以见' % element_str)
        if not element.is_enabled():
            self.logger.warning('%s 元素disabled状态' % element_str)
        if tag in ['checkbox', 'radio']:
            status = 'is selected' if element.lower().is_selected() else 'is not selected'
            self.logger.info('{} 元素 {} 状态'.format(element_str, status))

    def after_click(self, element, driver):
        pass
        # self.logger.info(element)

    def before_quit(self, driver):
        self.logger.info('页面即将关闭')

    def after_quit(self, driver):
        self.logger.info('页面已经关闭')

    def on_exception(self, exception, driver):
        pass
        # self.logger.info(exception)


if __name__ == "__main__":
    driver = browser('chrome')
    driver.get("http://www.baidu.com")
    from selenium.webdriver.support.color import Color

    print(Color.from_string('#00ff33').rgba)
    print(Color.from_string('rgb(1, 255, 3)').hex)
    print(Color.from_string('blue').rgba)

    import time

    time.sleep(1)

    # 1.通过js改变页面控件的属性（边框粗细，颜色，线的类型）
    js = 'q=document.getElementById("kw");q.style.border=\"1px solid red\";'
    driver.execute_script(js)
    # 2. js拖动到最底部
    js = "$('.scroll_top').click(function(){$(html.body).animate({scrollTop:'0px'},800)});"
    driver.execute_script(js)
