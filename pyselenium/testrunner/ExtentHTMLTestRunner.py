# coding:utf-8
from copy import copy
from pprint import pprint
from time import time, sleep

from pyselenium.lib.log import get_logger
from enum import Enum
import datetime
import unittest
import os
import platform
from collections import defaultdict
from enum import Enum
from jinja2 import Template, escape
from __init__ import __version__
logger = get_logger()


class Result(Enum):
    SUCCESS = 0
    FAIL = 1
    ERROR = 2


class _TestResult(unittest.TextTestResult):
    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the
    formatted traceback of the error that occurred.
    """

    def __init__(self, stream, descriptions, verbosity):
        super(_TestResult, self).__init__(stream, descriptions, verbosity)
        self.result = []
        self.sub_test_list = []
        self.start_time = time()
        self.successes = 0
        self.start_at = None

    @property
    def test_result(self):
        result = {
            "platform": {
                "SelePyTest_version": __version__,
                "python_version": "{} {}".format(platform.python_implementation(), platform.python_version()),
                "platform_os": platform.platform()
            },
            "stat": {
                'total': self.testsRun,
                'total_time': time() - self.start_time,
                'now_time': str(datetime.datetime.now()),
                'successes': self.successes,
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
        if self.wasSuccessful():
            self.successes += 1
        data = {
            'name': test.shortDescription(),
            'duration': self.duration,
            'test_suite_docs': test.__doc__ and test.__doc__.splitlines()[0] or "",
            'status': status,
            'success': self.wasSuccessful(),
            'attachment': attachment,
            "except_data": test.except_data,

        }
        self.result.append(data)

    @property
    def duration(self):
        """Duration time of a single test case

        :return: duration time
        """
        return time() - self.start_at

    def printErrors(self):
        """Called by TestRunner after test run"""
        pass

    def startTestRun(self):
        """Called once before any tests are executed.

        See startTest for a method called before each test.
        """
        self.start_at = time()

    def startTest(self, test):
        """Called when the given test is about to be run"""
        super().startTest(test)

    def stopTestRun(self):
        """Called once after all tests are executed.

        See stopTest for a method called after each test.
        """

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
        self.report_template = report_template
        self.image_path = os.path.join(os.path.dirname(report_file), 'images')
        self.verbosity = verbosity
        self.title = title
        self.description = description
        self.runner = unittest.TextTestRunner(verbosity=verbosity, resultclass=_TestResult)
        self.result = None

    def run(self, test):
        """ Run the given test case or test suite. """
        self.result = self.runner.run(test)
        sleep(2)
        pprint(self.result.test_result)

    def html_report(self):

        if self.report_template is None:
            self.report_template = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "test_report.html"
            )
            logger.debug("use default html report template")
        else:
            logger.info("use html report template: {}".format(self.report_template))
        summary = copy(self.result.test_result)
        with open(self.report_template, 'r', encoding='utf-8') as f_template:
            template_content = f_template.read()
            with open(self.report_file, 'w', encoding='utf-8') as f_report:
                rendered_content = Template(
                    template_content,
                    extensions=["jinja2.ext.loopcontrols"]
                ).render(summary)
                f_report.write(rendered_content)

        # pprint(result.test_result)


