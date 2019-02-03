from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from common.error import BrowserNoFoundError
from pyselenium.lib.s_logs import Log
from pyselenium.untils.function import find_alias

logger = Log()


def chrome_headless():
    ops = Options()
    ops.add_argument('--headless')
    return webdriver.Chrome(chrome_options=ops)


BROWSERS = {
    'chrome':           webdriver.Chrome,
    'chrome_headless':  chrome_headless,
    'firefox':          webdriver.Firefox,
    'ie':               webdriver.Ie,
    'opera':            webdriver.Opera,
    'edge':             webdriver.Edge,
}


def browser(bro, **kwargs):
    bro = bro.lower()
    fun = BROWSERS.get(bro, False)
    if fun:
        return fun(**kwargs)
    else:
        alias_key = find_alias(bro, BROWSERS)
        if alias_key:
            logger.print_color("input %s alias %s" % (bro, alias_key))

    raise BrowserNoFoundError("Not found '%s' browser, please use 'chrome' ,"
                              "'chrome_headless', 'opera', 'edge', 'ie' browser." % bro)


if __name__ == "__main__":
    dr = browser('chrom')
    dr.get("http://www.baidu.com")
    dr.quit()
