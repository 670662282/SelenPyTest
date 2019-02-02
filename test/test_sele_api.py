from pyselenium.configs.cfread import ReaderFactory
from .base import SUnittest
from pyselenium.webdriver.sele_api import ApiDriver
from common.error import LocationTypeError
from collections import OrderedDict
import os


class TestSApi(SUnittest):

    def test_get_locs(self):
        self.assertTupleEqual(ApiDriver._get_locs('#kw'), ('css selector', '#kw'))
        self.assertTupleEqual(ApiDriver._get_locs(xpath='#kw'), ('xpath', '#kw'))
        self.assertRaises(LocationTypeError, ApiDriver._get_locs, test='#kw')

    def test_cfread_yaml(self):
        file_path = 'test.yaml'
        ya = ReaderFactory.reader(file_path)
        info = OrderedDict({
            'URL': "http://10.10.120.3",
            'log': {
                'backup': 3,
                'level': "DEBUG",
                "output": 2
            },
            'RESERVE_REPORTS_NUM': 3,
            "EMAIL_SERVER": "smtp.163.com",
            "EMAIL_USR": '',
            "EMAIL_RECEIVE": '',
            "MAIL_TITLE": 'UI自动化测试报告',
            "IMP_TIME": 20,
            "TIME_OUT": 30,
        })
        ya.data = info
        self.assertDictEqual(info, ya.data[0])
        if os.path.isfile(file_path):
            os.remove(file_path)
