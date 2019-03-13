# coding:utf-8
from pyselenium.lib.log import get_logger
from pyselenium.testrunner.template_minin import TemplateMixin

logger = get_logger()

__author__ = "Wai Yip Tung"
__update__ = "wishchen"
__version__ = "1.1"

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?
from enum import Enum
import datetime
import sys
import unittest
import re
import os
from xml.sax import saxutils
from collections import defaultdict
from enum import Enum


class Result(Enum):
    pass


START_TIME = "Start Time"
DURATION = "Duration"
STATUS_ = "Status"


class ReturnCode:
    SUCCESS = 0
    FAIL = 1
    ERROR = 2


class _TestResult(unittest.TextTestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, stream, descriptions, verbosity):
        super(_TestResult, self).__init__(stream, descriptions, verbosity)
        self.result = []
        self.sub_test_list = []

    def get_test_result(self):
        summary = {
            "success": super().wasSuccessful(),
            "stat": {
                'total': super().testsRun,
                'failures': len(super().failures),
                'errors': len(super().errors),
                'skipped': len(super().skipped),
                'expectedFailures': len(super().expectedFailures),
                'unexpectedSuccesses': len(super().unexpectedSuccesses)
            }
        }
        return summary

    def _result_record(self, test, status, attachment=''):
        data = {
            'name': test.shortDescription(),
            'status': status,
            'attachment': attachment,
            "meta_datas": test.meta_datas,
            "png_path": "",
        }
        self.result.append(data)

    def startTest(self, test):
        super().startTest(test)

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        self._result_record(subtest, 'subtest', self._exc_info_to_string(err, subtest))
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


class HTMLTestRunner(TemplateMixin):
    """A TestRunner for use with the Python unit testing framework. It
    generates a HTML reports to show the result at a glance.

    The simplest way to use this is to invoke its main method. E.g.
        import unittest
        import HTMLTestRunner

    For more customization options, instantiates a HTMLTestRunner object.
    HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

        # output to a file
        fp = file('my_report.html', 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
                    stream=fp,
                    title='My unit test',
                    description='This demonstrates the reports output by HTMLTestRunner.'
                    )

        # run the test
        runner.run(my_test_suite)
    """
    def __init__(self, report_file, verbosity=1, title=None, description=None):
        self.report_file = report_file
        self.image_path = os.path.join(os.path.dirname(report_file), 'images')
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        self.verbosity = verbosity
        self.title = self.DEFAULT_TITLE if title is None else title
        self.description = self.DEFAULT_DESCRIPTION if description is None else description
        self.startTime = datetime.datetime.now()
        self.stopTime = None

    def run(self, test):
        """ Run the given test case or test suite. """
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generate_report(result)
        print('\nTime Elapsed: %s' % (self.stopTime-self.startTime), file=sys.stderr)
        return result

    @staticmethod
    def sort_result(result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))

        return [(cls, rmap[cls]) for cls in classes]

    def get_report_attributes(self, result):
        """
        Return reports attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        status = []
        if result.success_count:
            status.append('Pass %s' % result.success_count)
        if result.failure_count:
            status.append('Failure %s' % result.failure_count)
        if result.error_count:
            status.append('Error %s' % result.error_count)

        status = ' '.join(status) if status else 'None'
        return [
            (START_TIME, str(self.startTime)[:19]),
            (DURATION, str(self.stopTime - self.startTime)),
            (STATUS_, status),
        ]

    def generate_report(self, result):
        report_attrs = self.get_report_attributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        reports = self._generate_report(result)
        ending = self._generate_ending()
        dashboard_view = self._generate_dashboard_view(report_attrs, result)
        script_js = self._generate_script(result)

        output = self.HTML_TMPL.format(
            title=saxutils.escape(self.title),
            #generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            reports=reports,
            ending=ending,
            dashboard_view=dashboard_view,
            script_js=script_js,
        )
        with open(file=self.report_file, mode='wb') as stream:
            stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        head_dict = defaultdict(str)
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL.format(
                    name=saxutils.escape(name),
                    value=saxutils.escape(value),
                )
            a_lines.append(line)
            head_dict[name] = value

        # 取出来Start Time、Duration、Status
        return self.NAV.format(
            title=saxutils.escape(self.title),
            start_time=head_dict.get(START_TIME, 'None'),
            duration=head_dict.get(DURATION, 'None'),
            status=head_dict.get(STATUS_, 'None'),
            # 需要实现
            description=saxutils.escape(self.description),
        )

    def _generate_script(self, result):
        return self.SCRIPT_JS % dict(
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
        )

    def _generate_dashboard_view(self, report_attrs, result):
        a_lines = []
        head_dict = defaultdict(str)

        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name=saxutils.escape(name),
                    value=saxutils.escape(value),
                )
            a_lines.append(line)
            head_dict[name] = value

        return self.DASHBOARD_VIEW.format(
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            start_time=head_dict.get(START_TIME, 'None'),
            duration=head_dict.get(DURATION, 'None'),
        )

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error), n
        #   TestCase object, t
        #   Test output (byte string), o
        #   stack trace, e
        # )
    def _generate_report(self, result):
        # TODO Refactor this function
        rows = []
        row1s = []
        section_name = []
        category_tbody = []
        category_active = []
        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            # subtotal for a class
            np = nf = ne = 0
            for code, obj, out, trace in cls_results:
                if code == ReturnCode.SUCCESS:
                    np += 1
                elif code == ReturnCode.FAIL:
                    nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.strip('\n') or "None"
            desc = doc and '%s' % name or name

            # section中suite name
            s_name = self.SECTION_SUIT_NAME % dict(
                name=desc,
            )
            section_name.append(s_name)

            test_collection_ul_list = []
            for tid, (code, obj, out, trace) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, code, obj, out, trace, test_collection_ul_list)

            test_collection_li_id = desc + '_' + str(cid+1)
            if ne > 0:
                status = bdd = self.STATUS[ReturnCode.ERROR]
            elif nf > 0:
                status = bdd = self.STATUS[ReturnCode.FAIL]
            else:
                bdd = 'true'
                status = self.STATUS[ReturnCode.SUCCESS]
            row1 = self.TEST_COLLECTION.format(
                test_collection_li_id=test_collection_li_id,
                status=status,
                bdd=bdd,
                # node_level=nodeLevel,
                desc=desc,
                doc=doc,
                count=np+nf+ne,
                Pass=np,
                fail=nf,
                error=ne,
                test_collection_ul_list=''.join(test_collection_ul_list),
                # 没有这块
                cid='c%s' % (cid+1),
            )
            row1s.append(row1)
            body = self.CATEGORY_TBODY % dict(
                name=name,
                desc=desc,
                start_time=self.startTime,
                cid=cid,
                status=status,
            )
            category_tbody.append(body)

            c_active = self.CATEGORY_ACTIVE % dict(
                desc=desc,
                Pass=np,
                fail=nf,
                error=ne,
            )
            category_active.append(c_active)

        control_section = self.CONTROL_SECTION % dict(
            suite_name=''.join(section_name)
        )
        view_charts = self.VIEW_CHARTS % dict(
            pass_count=str(result.success_count),
            fail_count=str(result.failure_count),
            error_count=str(result.error_count),
        )
        subview_left = self.SUBVIEW_LEFT % dict(
            test_collection=''.join(row1s),
        )
        category_view = self.CATEGORY_VIEW % dict(
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            category_tbody=category_tbody,
            category_active=category_active,
        )

        report = self.TEST_VIEW % dict(
            control_section=control_section,
            view_charts=view_charts,
            # test_list=''.join(rows),
            test_list=subview_left,
            count=str(result.success_count+result.failure_count+result.error_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            category_view=category_view,
        )
        return report

    def _generate_report_test(self, rows, cid, tid, code, obj, out, trace, test_collection_ul_list):
        # TODO parameters is greater than 7 authorized
        has_output = bool(out or trace)
        if not has_output:
            return
        # e.g. 'pt1.1', 'ft1.1', etc
        tid = (code == ReturnCode.SUCCESS and 'p' or 'f') + 't%s.%s' % (cid+1, tid+1)
        name = obj.id().split('.')[-1]
        doc = obj.shortDescription() or 'None'
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.TBODY or self.REPORT_TEST_NO_OUTPUT_TMPL

        uo = out
        ue = trace

        ss_reg = re.compile(r'screenshot_.+?png')
        ss = ss_reg.findall(uo)

        images = []

        for ima in ss:
            image = self.REPORT_IMAGE % dict(
                screenshot_id=ima.split(".")[0],
                screenshot=saxutils.escape(os.path.join(self.image_path, ima))
            )
            images.append(image)

        images = ''.join(images)

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=cid,
            output=saxutils.escape(uo+ue),
        )

        t_body = self.TBODY % dict(
            script=script,
            images=images,
        )
        node_level = desc + '_' + str(tid) + '_' + str(cid + 1)
        status = self.STATUS[code]
        tcll = self.TEST_COLLECTION_UL_LIST.format(
            node_level=node_level,
            status=status,
            desc=name,
            doc=doc,
            t_body=t_body,
        )
        test_collection_ul_list.append(tcll)
        # caseid = self.REPORT_TEST_OUTPUT_CASEID % dict(
        #    case_id=saxutils.escape(uo+ue)
        # )
        row = tmpl % dict(
            tid=tid,
            Class=(code == ReturnCode.SUCCESS and 'hiddenRow' or 'none'),
            style=code == ReturnCode.ERROR and 'errorCase' or (code == ReturnCode.FAIL and 'failCase' or 'none'),
            desc=desc,
            script=script,
            images=images,
            # caseid = caseid[caseid.find("case"):(int(caseid.find("case"))+9)],
            status=status,
        )
        rows.append(row)

    def _generate_ending(self):
        return self.ENDING_TMPL


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """
    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=1)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
