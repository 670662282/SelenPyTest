from selenium.webdriver.support.events import AbstractEventListener
from pyselenium.lib.s_logs import Log
from selenium.webdriver.remote.webelement import WebElement
from time import sleep


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
