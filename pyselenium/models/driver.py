
from SelenPyTest.pyselenium.data.selenium_dict import BROWSERS

def browser(bro):
    try:
        return BROWSERS[bro.lower()]()
    except KeyError as e:
        raise e("Not found %s browser, please use 'chrome'\
                'chrome_headless', 'opera', 'edge', 'ie'." % bro)

if __name__ == "__main__":
    dr = browser()
    dr.get("http://www.baidu.com")
    dr.quit()
