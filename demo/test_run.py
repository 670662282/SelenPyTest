from pyselenium import browser, unit, TestRunner, sele_api
from pyselenium.untils.function import capture_except, get_png


if __name__ == '__main__':
    testRunner = TestRunner(cases="./", casecls_re='aa_a*.py', debug=False, report_backup=3)
    testRunner.runner()
    report = testRunner.report_file
