from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidElementStateException

from pyselenium.lib.s_logs import Log
from pyselenium.untils import function
from common.error import LocationTypeError
from selenium.webdriver.common.by import By

LOCATORS = {
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_': By.CLASS_NAME,
}
logger = Log()


class ApiDriver:
    TIMEOUT = 10

    def open(self, url):
        self.driver.get(url)

    @property
    def alert_text(self):
        """
        Get warning box prompt information.
        """
        self.driver.switch_to.alert.text

    @property
    def title(self):
        """
        Get window title.
        """
        return self.driver.title

    @property
    def url(self):
        """
        Get the URL address of the current page.
        """
        return self.driver.current_url

    @function.wait(TIMEOUT)
    def waits_for(self, fn, *args):
        return fn(*args)

    @function.change_wait(5)
    def change_implicitly_wait_5s(self, fn, *args):
        return fn(*args)

    def set_wait(self, secs):
        self.driver.implicitly_wait(secs)

    @staticmethod
    def _get_locs(*args, **kwargs):
        if len(args) == 1 or len(kwargs) == 1:
            if args and not kwargs:
                return LOCATORS['css'], args[0]
            if kwargs and not args:
                k, v = kwargs.popitem()
                try:
                    return LOCATORS[k], v
                except KeyError:
                    raise LocationTypeError("Please use a locator：'id_' 'name' 'class_' \
                            'css' 'xpath' 'link_text' 'partial_link_text'.")

        raise ValueError("locator error, only one")

    def find_element(self, *args, **kwargs):
        return self._find_element(*self._get_locs(*args, **kwargs))

    def find_elements(self, *args, **kwargs):
        return self._find_elements(*self._get_locs(*args, **kwargs))

    @function.wait(TIMEOUT)
    def _find_element(self, *location):
        return self.driver.find_element(*location)

    @function.wait(TIMEOUT)
    def _find_elements(self, *location):
        return self.driver.find_elements(*location)

    def F5(self):
        self.driver.refresh()

    def script(self, script):
        self.driver.execute_script(script)

    def click_element(self, *args, **kwargs):
        self.find_element(*args, **kwargs).click()

    def send_values(self, value, *args, **kwargs):
        obj = self.find_element(*args, **kwargs)
        try:
            obj.clear()
        except InvalidElementStateException:
            pass
        obj.send_keys(value)

    def get_text(self, *args, **kwargs):
        return self.find_element(*args, **kwargs).text

    def get_attr(self, attr, *args, **kwargs):
        return self.find_element(*args, **kwargs).get_attribute(attr)

    def get_display(self, *args, **kwargs):
        return self.find_element(*args, **kwargs).is_displayed()

    def wait_element_invisibility(self, *args, **kwargs):
        WebDriverWait(self.driver, self.TIMEOUT).until_not(
            EC.visibility_of_element_located(*self._get_locs(*args, **kwargs)))

    def wait_element_visibility(self, *args, **kwargs):
        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.visibility_of_element_located(*self._get_locs(*args, **kwargs)))

    @function.change_wait(time=1)
    def wait_element_drap(self, fn, *args, **kwargs):
        start_time = time()
        while True:
            try:
                fn(*args, **kwargs)
                sleep(0.5)
                if time() - start_time > self.TIMEOUT:
                    logger.error('drap fail')
                    return False
            except (WebDriverException, NoSuchElementException, AssertionError):
                logger.info('drap success %{}'.format(time() - start_time))
                return True


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
                if select_num < 1:
                    raise ValueError('选择的数不能小于1')
                if i == select_num:
                    break
            action.click(element)
            select_ele_text_list.append(element.text)
            i += 1

        action.key_up(Keys.CONTROL)
        action.perform()
        return select_ele_text_list
