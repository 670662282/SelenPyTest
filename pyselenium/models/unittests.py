import unittest

from pyselenium.apis.sele_api import ApiDriver
from pyselenium.lib.log import print_color
from pyselenium.models.driver import get_driver


class TestCase(unittest.TestCase, ApiDriver):
    # must 定义不然会出现 RecursionError: maximum recursion depth exceeded
    ApiDriver.png_path = '.'
    except_data = {
        "image_path": "",
        "max_retry": 0,
        "retry_result": {},
    }

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        # cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def init_except_data(self):
        self.except_data = {
            "image_path": "",
            "max_retry": 0,
            "retry_result": {},
        }

    def set_image_path(self, image_path):
        self.except_data["image_path"] = image_path

    def except_parse(self, exception, retry, fn, *args, **kwargs):
        try:
            retry = int(retry)
        except ValueError:
            raise TypeError('retry type error')
        if retry < 0:
            raise ValueError('retry must be greater than or equal 0')

        self.except_data["max_retry"] = retry
        for i in range(1, retry+1):

            try:
                fn(self, *args, **kwargs)
            except Exception:
                print_color('retry exec function:{} time'.format(i))
                if i == retry:
                    print_color('retry reach max time', 'red')
                    self.except_data["retry_result"] = {
                        "result": "fail",
                        "retry_time": retry,
                    }
                    raise exception
            else:
                print_color('retry exec function success', 'yellow')
                self.except_data["retry_result"] = {
                    "result": "success",
                    "retry_time": i,
                }
                break






