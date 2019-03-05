from pyselenium import TestRunner


if __name__ == '__main__':
    testRunner = TestRunner(report_path=None, cases="testcases/normal_test", case_cls_re='test_2.py', report_backup=3)
    testRunner.runner()
    report = testRunner.report_file

