# coding:utf-8
# !/usr/bin/env python3
from .ExtentHTMLTestRunner import HTMLTestRunner
from pyselenium.configs.config import YamlConfig
from pyselenium.models.s_logs import Log
import unittest
import time
import os


class TestRunner:
    def __init__(self, cases="./",
                 case_cls_re='*.py',
                 title="UITestReport",
                 report_backup=0,
                 description="Test case execution:",
                 debug=False):

        self.cases = cases
        self.title = title
        self.debug = debug
        self.description = description
        self.case_cls_re = case_cls_re
        self.logger = Log()
        cf = YamlConfig()
        self.backup = report_backup
        self.email_title = cf.get('MAIL_TITLE')
        self.email_server = cf.get('EMAIL_SERVER')
        self.email_usr = cf.get('EMAIL_USR')
        # self.email_pwd = cf.get('EMAIL_PWD')
        self.email_receiver = cf.get('EMAIL_RECEIVE')
        self._report_file = None

    @property
    def report_file(self):
        return self._report_file

    def handle_reports(self, reports_path, reserve_num=0):
        """
        Sort reports for mtime
        Retain the latest reserve_num reports and return to the latest report.
        reserve_num <= 0 表示不进行删除
        """
        if os.path.isdir(reports_path):
            os.chdir(reports_path)

        reports_path = os.getcwd()
        all_file = os.listdir('.')
        self.logger.info('list : %s', all_file)

        reports = [f for f in all_file if f.strip().endswith('.html')]
        reports.sort(key=lambda f: os.path.getmtime(f))
        new_report = reports.pop()
        self.logger.info("new reports_path:" + new_report)
        del_list = []
        # 前面pop最新的报告 所以这要加1
        if 0 < reserve_num < len(reports) + 1:
            for i in range(reserve_num-1):
                reports.pop()
            for r in reports:
                if os.path.isfile(r):
                    del_list.append(r)
                    os.remove(r)
        self.logger.info('del report : %s', del_list)
        return os.path.join(reports_path, new_report)

    def _get_discover(self):
        return unittest.defaultTestLoader.discover(self.cases, pattern=self.case_cls_re)

    def runner(self):
        self._debug() if self.debug else self._normal()

    def _debug(self):
        unit_runner = unittest.TextTestRunner(verbosity=2)
        unit_runner.run(self._get_discover())

    def _normal(self):
        reports_path = os.path.join(os.getcwd(), 'report')
        if not os.path.isdir(reports_path):
            os.mkdir(reports_path)
        report_name = time.strftime("%Y-%m-%d_%H-%M-%S") + 'UITest.html'
        with open(os.path.join(reports_path, report_name), 'wb') as fp:
            runner = HTMLTestRunner(stream=fp,
                                    title=self.title,
                                    description=self.description,
                                    verbosity=2)
            runner.run(self._get_discover())

        att_list = []
        self._report_file = self.handle_reports(reports_path, self.backup)
        att_list.append(self._report_file)


"""
if __name__ == '__main__':
    casecls_re = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.py') else '*_tl.py'
    print('UIAutotest is start')
    tl_runner = TestRunner(casecls_re)
    tl_runner.debug() if len(sys.argv) > 2 and sys.argv[2] == 'debug' else tl_runner.normal()
    print('UIAutotest is end')
"""
