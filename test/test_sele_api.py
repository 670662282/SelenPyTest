from .base import SUnittest
from pyselenium.webdriver.sele_api import ApiDriver
from common.error import LocationTypeError


class TestSApi(SUnittest):

    def test_get_locs(self):
        self.assertTupleEqual(ApiDriver._get_locs('#kw'), ('css selector', '#kw'))
        self.assertTupleEqual(ApiDriver._get_locs(xpath='#kw'), ('xpaths', '#kw'))
        self.assertRaises(LocationTypeError, ApiDriver._get_locs, test='#kw')



