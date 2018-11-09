#coding:utf-8
#!/usr/bin/env python3
#from HTMLTestRunner import HTMLTestRunner
#from HTML_test_runner import HTMLTestRunner
from htmlrunner.ExtentHTMLTestRunner import HTMLTestRunner
import unittest
import time
import os, sys
import smtplib
sys.path.append('./case/models')
from case.models import myssh
from case.models.config import Config, BASE_PATH, REPORT_PATH, TL_WEBLOG_PATH, IMAGE_PATH, CASE_PATH
from case.models.logs import Log
from case.models.email import Email

class TL_TestRunner:
    def __init__(self, casecls_re='*_tl.py'):
        cf = Config()
        self.casecls_re = casecls_re
        self.backup = cf.get('RESERVE_REPORTS_NUM')
        self.email_title = cf.get('MAIL_TITLE')
        self.email_server = cf.get('EMAIL_SERVER')
        self.email_usr = cf.get('EMAIL_USR')
        self.email_pwd = cf.get('EMAIL_PWD')
        self.email_receiver = cf.get('EMAIL_RECEIVE')
        self.tl_log_path = cf.get('TL_LOG')
        self.tl_ip = cf.get('URL').split('//')[1]
        self.tl_pwd = '1'
        self.logger = Log().get_logger()

    #获取测试页面的web日志 通过sftp下载
    def get_weblog(self):
        ssh = myssh.Tl_ssh(self.tl_ip, self.tl_pwd)
        ssh.connect()
        ssh.set_transport()
        log_name = ssh.exec_cmd('date +"%Y-%m-%d"').strip('\n') + '.log'
        local_logfile = os.path.join(TL_WEBLOG_PATH, log_name)
        try:
            ssh.down(os.path.join(self.tl_log_path, log_name), local_logfile)
        except FileNotFoundError:
            self.logger.info('soory no find {}'.format(log_name))
            return None
        finally:
            ssh.close()

        return local_logfile



    def handle_reports(self, reports_path, reserve_num=0):
        """
        Sort reports for mtime
        Retain the latest reserve_num reports and return to the latest report.
        reserve_num=0 表示不进行删除
        """
        if reserve_num < 0:
            reserve_num = 0
        os.chdir(reports_path)
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
        return unittest.defaultTestLoader.discover(CASE_PATH, pattern=self.casecls_re)

    def debug(self):
        unit_runner = unittest.TextTestRunner(verbosity=2)
        unit_runner.run(self._get_discover())

    def normal(self):
        report_name = time.strftime("%Y-%m-%d_%H_%M") + 'result.html'
        with open(os.path.join(REPORT_PATH, report_name), 'wb') as fp:
            runner = HTMLTestRunner(stream=fp,
                                title='UI测试报告',
                                description='用例执行情况：',
                                verbosity=2)
            runner.run(self._get_discover())

        att_list = []
        reportfile = self.handle_reports(REPORT_PATH, self.backup)
        att_list.append(reportfile)
        logfile = self.get_weblog()
        if logfile is not None:
            att_list.append(logfile)

        Email(self.email_server, self.email_usr).send(
            self.email_title, reportfile, self.email_receiver, att_list)



if __name__ == '__main__':
    casecls_re = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.py') else '*_tl.py'
    print('UIAutotest is start')
    tl_runner = TL_TestRunner(casecls_re)
    tl_runner.debug() if len(sys.argv) > 2 and sys.argv[2] == 'debug' else tl_runner.normal()
    print('UIAutotest is end')
