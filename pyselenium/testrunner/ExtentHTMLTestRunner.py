# coding:utf-8
from pprint import pprint
from time import time

from pyselenium.lib.log import get_logger, print_color
from enum import Enum

import unittest
import os
from collections import OrderedDict
from enum import Enum

logger = get_logger()


class Result(Enum):
    SUCCESS = 0
    FAIL = 1
    ERROR = 2


class _TestResult(unittest.TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super(_TestResult, self).__init__(stream, descriptions, verbosity)
        self.result = []
        self.sub_test_list = []
        self.start_time = time()

    @property
    def test_result(self):
        result = OrderedDict({
            "success": self.wasSuccessful(),
            "stat": {
                'total': self.testsRun,
                'total_time': time() - self.start_time,
                'failures': len(self.failures),
                'errors': len(self.errors),
                'skipped': len(self.skipped),
                'expectedFailures': len(self.expectedFailures),
                'unexpectedSuccesses': len(self.unexpectedSuccesses)
            },
            "result": self.result,
        })
        return result

    def _result_record(self, test, status, attachment=''):
        data = OrderedDict({
            'name': test.shortDescription(),
            'status': status,
            'attachment': attachment,
            "meta_datas": 'null',
            "except_data": test.except_data,
        })
        self.result.append(data)

    def startTest(self, test):
        super().startTest(test)

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        # self._result_record(subtest, 'subtest', self._exc_info_to_string(err, test))
        # print("")

    def addSuccess(self, test):
        super().addSuccess(test)
        self._result_record(test, 'success')
        logger.debug(test.except_data)
        print("")

    def addError(self, test, err):
        super().addError(test, err)
        self._result_record(test, 'error')
        print("")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._result_record(test, 'failure', self._exc_info_to_string(err, test))
        logger.debug(test.except_data)
        print("")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._result_record(test, 'skipped', reason)
        print("")

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self._result_record(test, 'ExpectedFailure', self._exc_info_to_string(err, test))
        print("")

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self._result_record(test, 'UnexpectedSuccess')
        print("")


class HTMLTestRunner:
    """A TestRunner for use with the Python unit testing framework. It
    generates a HTML reports to show the result at a glance.
    """
    def __init__(self, report_file, verbosity=2, title=None, description=None):
        self.report_file = report_file
        self.image_path = os.path.join(os.path.dirname(report_file), 'images')
        self.verbosity = verbosity
        self.title = title
        self.description = description
        self.runner = unittest.TextTestRunner(verbosity=verbosity, resultclass=_TestResult)

    def run(self, test):
        """ Run the given test case or test suite. """
        result = self.runner.run(test)
        pprint(result.test_result['result'])

