from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

LOCATORS = {
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_': By.CLASS_NAME,
}

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
