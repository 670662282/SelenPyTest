# coding:utf-8
# !/usr/bin/env python3
from .ExtentHTMLTestRunner import HTMLTestRunner
from pyselenium.lib.log import print_color, get_logger
import unittest
import time
import os


class TestRunner:
    def __init__(self,
                 report_path=None,
                 cases="./",
                 case_cls_re='*.py',
                 title="UITestReport",
                 report_backup=0,
                 description="Test case execution:",
                 ):

        self.report_path = report_path
        self.cases = cases
        self.title = title
        self.description = description
        self.case_cls_re = case_cls_re
        self.backup = report_backup
        self.logger = get_logger()
        self._report_file = None

        if report_path and not os.path.exists(self.report_path):
                os.makedirs(self.report_path)

    @property
    def report_file(self):
        return self._report_file

    def handle_reports(self, reports_path, reserve_num=0):
        """
        Sort reports for mtime
        Retain the latest reserve_num reports and return to the latest reports.
        reserve_num <= 0 表示不进行删除
        """
        if os.path.isdir(reports_path):
            os.chdir(reports_path)

        reports_path = os.getcwd()
        all_file = os.listdir('.')
        self.logger.info('list : %s' % all_file)

        reports = [f for f in all_file if f.strip().endswith('.html')]
        reports.sort(key=lambda f: os.path.getmtime(f))
        new_report = reports.pop()
        print_color("new reports_path:" + new_report)
        del_list = []
        # 前面pop最新的报告 所以这要加1
        if 0 < reserve_num < len(reports) + 1:
            for i in range(reserve_num-1):
                reports.pop()
            for r in reports:
                if os.path.isfile(r):
                    del_list.append(r)
                    os.remove(r)
        self.logger.info('del reports : %s' % del_list)
        return os.path.join(reports_path, new_report)

    def _get_discover(self):
        return unittest.defaultTestLoader.discover(self.cases, pattern=self.case_cls_re)

    def runner(self):
        self._normal() if self.report_path else self._no_html()

    def _no_html(self):
        unittest.TextTestRunner(verbosity=2).run(self._get_discover())

    def _normal(self):
        runner = HTMLTestRunner(
            report_file=os.path.join(
                self.report_path, time.strftime("%Y-%m-%d_%H-%M-%S") + 'UITest.html'),
            title=self.title,
            description=self.description,
            verbosity=2)
        runner.run(self._get_discover())

        # self._report_file = self.handle_reports(self.report_path, self.backup)


