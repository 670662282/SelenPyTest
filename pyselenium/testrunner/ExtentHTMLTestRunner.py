# coding:utf-8
from pprint import pprint
from time import time

from pyselenium.lib.log import get_logger
import datetime
import unittest
import os
from enum import Enum
from jinja2 import Template, escape

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
        result = {
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
        }
        return result

    def _result_record(self, test, status, attachment=''):
        data = {
            'name': test.shortDescription(),
            'status': status,
            'attachment': attachment,
            "meta_datas": 'datas',
            "png_path": "",
            "retry_time": "",
            "retry_result": "",
        }
        self.result.append(data)

    def startTest(self, test):
        super().startTest(test)

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        # self._result_record(subtest, 'subtest', self._exc_info_to_string(err, test))
        print("")

    def addSuccess(self, test):
        super().addSuccess(test)
        self._result_record(test, 'success')
        print("")

    def addError(self, test, err):
        super().addError(test, err)
        self._result_record(test, 'error')
        print("")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._result_record(test, 'failure', self._exc_info_to_string(err, test))
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
    def __init__(self, report_file, verbosity=2, title=None, description=None, report_template=None):
        self.report_file = report_file
        self.image_path = os.path.join(os.path.dirname(report_file), 'images')
        self.verbosity = verbosity
        self.title = title
        self.description = description
        self.report_template = report_template
        self.runner = unittest.TextTestRunner(verbosity=verbosity, resultclass=_TestResult)
        self.result = None

    def run(self, test):
        """ Run the given test case or test suite. """
        self.result = self.runner.run(test)

    def html_report(self):

        if self.report_template is None:
            self.report_template = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "test_report.html"
            )
            logger.debug("use default html report template")
        else:
            logger.info("use html report template: {}".format(self.report_template))

        with open(self.report_template, 'r', encoding='utf-8') as f_template:
            template_content = f_template.read()
            with open(self.report_file, 'w', encoding='utf-8') as f_report:
                rendered_content = Template(
                    template_content,
                    extensions=["jinja2.ext.loopcontrols"]
                ).render(self.result.test_result)
                f_report.write(rendered_content)

        # pprint(result.test_result)


