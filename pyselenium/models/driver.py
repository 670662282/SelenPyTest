
from pyselenium.data.selenium_dict import BROWSERS


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
