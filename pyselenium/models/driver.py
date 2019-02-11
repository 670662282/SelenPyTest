
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
    try:
        return BROWSERS[bro.lower()](**kwargs)
    except KeyError as e:
        raise e("Not found %s browser, please use 'chrome'\
                'chrome_headless', 'opera', 'edge', 'ie'." % bro)


if __name__ == "__main__":
    dr = browser('chrome')
    dr.get("http://www.baidu.com")
    dr.quit()
