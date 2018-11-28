from time import sleep, time
import re, functools
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import  TimeoutException,\
                                        NoSuchElementException,\
                                        StaleElementReferenceException,\
                                        WebDriverException,\
                                        ElementNotVisibleException,\
                                        InvalidElementStateException
from selenium.webdriver.support.select import Select
from SelenPyTest.pyselenium.models.logs import Log
from SelenPyTest.pyselenium.data.selenium_dict import LOCATORS
from SelenPyTest.pyselenium.untils import function

class ApiDriver:

    def open(self, url):
        self.driver.get(url)

    @property
    def get_driver(self):
        return self.driver

    @function.wait(5)
    def waits_for(self, fn, *args):
        return fn(*args)

    @function.changewait(5)
    def changewait_for_5s(self, fn, *args):
        return fn(*args)

    def set_wait(self, secs):
        self.driver.implicitly_wait(secs)

    def _get_locs(self, *args, **kwargs):
        print(len(args))
        if len(args) == 1 or len(kwargs) == 1:
            if args and not kwargs:
                return (LOCATORS['css'], args[0])
            if kwargs and not args:
                k, v = kwargs.popitem()
                try:
                    return (LOCATORS[k], v)
                except KeyError:
                    raise KeyError("Please use a locator：'id_' 'name' 'class_' \
                            'css' 'xpath' 'link_text' 'partial_link_text'.")

        raise ValueError("locator error, only one")


    def find_element(self, *args, **kwargs):
        return self._find_element(*self._get_locs(*args, **kwargs))
    def find_elements(self, *args, **kwargs):
        return self._find_elements(*self._get_locs(*args, **kwargs))
    def find_element_by_css(self, loc):
        return self.driver.find_element_by_css_selector(loc)

    @function.wait(5)
    def _find_element(self, *location):
        return self.driver.find_element(*location)

    @function.wait(5)
    def _find_elements(self, *location):
        return self.driver.find_elements(*location)

    def F5(self):
        self.driver.refresh()

    def script(self, script):
        self.driver.execute_script(script)

    def click_button(self, name):
        self.click_element(*self.by_text_loc(name))

    def by_text_loc(self, str):
        loc = '//span[text()="{}"]/../../..'.format(str)
        self.logger.info(loc)
        return (By.XPATH, loc)

    def click_element(self, *args, **kwargs):
        self.find_element(*args, **kwargs).click()

    def send_values(self, str, *args, **kwargs):
        obj = self.find_element(*args, **kwargs)
        try:
            obj.clear()
        except InvalidElementStateException as e:
            pass
        obj.send_keys(str)

    def get_text(self, *args, **kwargs):
        return self.find_element(*args, **kwargs).text
    def get_attr(self, attr, *args, **kwargs):
        return self.find_element(*args, **kwargs).get_attribute(attr)
    def get_display(self, *args, **kwargs):
        return self.find_element(*args, **kwargs).is_displayed()

    def wait_element_invisibility(self, *args, **kwargs):
        WebDriverWait(self.driver, self.timeout).until_not(
            EC.visibility_of_element_located(*self._get_locs(*args, **kwargs)))

    def wait_element_visibility(self, *args, **kwargs):
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(*self._get_locs(*args, **kwargs)))

    #需要优化
    @function.changewait(time=1)
    def wait_for_drap(self, fn, *para):
        start_time = time()
        while True:
            try:
                fn(*para)
                sleep(1)
                if time() - start_time > self.timeout:
                    self.logger.error('drap fail')
                    return False
                self.logger.info('fun:{}, wait..'.format(fn))
            except ( WebDriverException, NoSuchElementException ) as e:
                self.logger.info('drap success')
                return True

    """
    changeable select item
    parameter: select_obj      --select element object
    parameter: choice_value    --select choice which  ep: 0, 1, 2, 3
    return false or choice.text
    """
    def select_changeable_item(self, select_obj, which):
        choice_info = None
        try:
            select_obj.click()
            you_choice = self.get_obj_list()[which]
            choice_info = you_choice.text
            self.logger.info('you choice is {}'.format(choice_info))
            # wait Element change
            sleep(0.5)
            you_choice.click()
        except IndexError as e:
            self.logger.error('index is null')
            raise
        except StaleElementReferenceException as e:
            # only choice oright pool result in  StaleElementReference
            self.logger.info('Select StaleElement')
            self.get_obj_list()[which].click()

        return choice_info



    """
    const select item
    parameter: select_obj      --select element object
    parameter: choice_value    --select choice value
    parameter: const_list      --select item (choosable)
    if const_list is None ,    list of value is text what select
    content element obj_list
    """
    def select_const_item(self, select_obj, choice_value, const_list=None):
        select_obj.click()
        #get elements list  as value
        obj_list = self.get_obj_list()
        #get const_list  as key
        if const_list is None:
            const_list = [ x.text for x in obj_list ]

        my_dict = dict(zip(const_list, obj_list))
        try:
            self.logger.info('you choice :{}'.format(choice_value))
            my_dict[str(choice_value)].click()
        except KeyError as e:
            self.logger.exception(e)
            print("key must ", const_list)
            select_obj.click()
            raise e

    @function.changewait(time=1)
    def capture_error_closed(self):
        function.get_png(self.driver, '_error.png')

    """
    SHIFT多选操作
        start_element
        end_element
    """
    def shift_muitl_selected(self, start_element, end_element):
        action = ActionChains(self.driver)
        action.click(start_element)
        action.key_down(Keys.SHIFT)
        action.click(end_element)
        action.key_up(Keys.SHIFT)
        action.perform()

    def ctrl_muitl_selected(self, element_list, select_num=None):
        select_ele_text_list = []
        action = ActionChains(self.driver)
        action.key_down(Keys.CONTROL)
        i = 0
        for element in element_list:
            if select_num is not None:
                if select_num < 1:  raise ValueError('选择的数不能小于1')
                if i == select_num: break
            action.click(element)
            select_ele_text_list.append(element.text)
            i += 1

        action.key_up(Keys.CONTROL)
        action.perform()
        return select_ele_text_list
