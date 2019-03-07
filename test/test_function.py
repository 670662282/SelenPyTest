from pyselenium.untils.function import find_alias
from test.base import SUnittest


class TestSApi(SUnittest):

    def test_alias(self):
        args = ['admins', 'ylel', 'ets', 'add', 1232304]
        compare_set = {'admin', 'yellow', 'test', 'add', 123}
        compare_list = ['admin', 'yellow', 'test', 'add', 1234]
        compare_dict = {'admin': '', 'yellow': '', 'test': '', 'add': '', 1: ''}
        compare_str = 'adminz'
        for arg in args:
            find_alias(arg, compare_set)
            find_alias(arg, compare_list)
            find_alias(arg, compare_dict)
            find_alias(arg, compare_str)


