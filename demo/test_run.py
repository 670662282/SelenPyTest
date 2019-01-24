from pyselenium import TestRunner


if __name__ == '__main__':
    testRunner = TestRunner(cases="./", case_cls_re='aa_a*.py', debug=False, report_backup=3)
    testRunner.runner()
    report = testRunner.report_file
