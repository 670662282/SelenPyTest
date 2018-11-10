#coding:utf-8
#!/usr/bin/env python3
from .ExtentHTMLTestRunner import HTMLTestRunner
from SelenPyTest.pyselenium.models.ssh import Tl_ssh
from SelenPyTest.pyselenium.configs.config import Config
from SelenPyTest.pyselenium.models.logs import Log
from SelenPyTest.pyselenium.models.email import Email
import unittest
import time
import os, sys
import smtplib

class TestRunner:
    def __init__(self, cases="./", casecls_re='*_tl.py', title="UITestReport", description="Test case execution"):
        self.cases = cases
        self.title = title
        self.description = description
        self.casecls_re = casecls_re
        self.logger = Log().get_logger()
        #self.backup = cf.get('RESERVE_REPORTS_NUM')
        #self.email_title = cf.get('MAIL_TITLE')
        #self.email_server = cf.get('EMAIL_SERVER')
        #self.email_usr = cf.get('EMAIL_USR')
        #self.email_pwd = cf.get('EMAIL_PWD')
        #self.email_receiver = cf.get('EMAIL_RECEIVE')

    def handle_reports(self, reports_path, reserve_num=0):
        """
        Sort reports for mtime
        Retain the latest reserve_num reports and return to the latest report.
        reserve_num=0 表示不进行删除
        """
        if reserve_num < 0: reserve_num = 0
        if os.path.isdir(reports_path):
            os.chdir(reports_path)
        reports_path = os.getcwd()
        reports = os.listdir('.')
        self.logger.info('list : %s', reports)
        #排除非html后缀的
        reports_cp = reports[:]
        for r in reports_cp:
            if not r.strip().endswith('.html'):
                reports.remove(r)

        reports.sort(key=lambda f: os.path.getmtime(f))
        new_report = reports.pop()
        self.logger.info("new reports_path:" + new_report)
        del_list = []
        #前面pop最新的报告 所这要加1
        if len(reports) + 1 > reserve_num or reserve_num == 0:
            for i in range(reserve_num-1):
                reports.pop()
            for r in reports:
                if os.path.isfile(r):
                    del_list.append(r)
                    os.remove(r)
        self.logger.info('del report : %s', del_list)
        return os.path.join(reports_path, new_report)


    def _get_discover(self):
        return unittest.defaultTestLoader.discover(self.cases, pattern=self.casecls_re)

    def debug(self):
        unit_runner = unittest.TextTestRunner(verbosity=2)
        unit_runner.run(self._get_discover())

    def normal(self):
        reports_path = os.path.join(os.getcwd(), 'report')
        if not os.path.isdir(reports_path):
            os.mkdir(reports_path)
        report_name = time.strftime("%Y-%m-%d_%H-%M-%S") + 'UITest.html'
        with open(os.path.join(reports_path, report_name), 'wb') as fp:
            runner = HTMLTestRunner(stream=fp,
                                title='UI测试报告',
                                description='用例执行情况：',
                                verbosity=2)
            runner.run(self._get_discover())

        att_list = []
        reportfile = self.handle_reports(reports_path, 3)
        att_list.append(reportfile)
        print(att_list)
        #logfile = self.get_weblog()
        #if logfile is not None:
            #att_list.append(logfile)

        #Email(self.email_server, self.email_usr).send(
        #    self.email_title, reportfile, self.email_receiver, att_list)
        Email('smtp.163.com', 'a670662282@163.com').send(
            '自动化测试邮件', reportfile, 'a670662282@163.com', att_list)

"""
if __name__ == '__main__':
    casecls_re = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.py') else '*_tl.py'
    print('UIAutotest is start')
    tl_runner = TestRunner(casecls_re)
    tl_runner.debug() if len(sys.argv) > 2 and sys.argv[2] == 'debug' else tl_runner.normal()
    print('UIAutotest is end')
"""
