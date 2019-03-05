from selenium.webdriver.common.by import By

window1_loc = (By.CSS_SELECTOR, 'test')
window2_loc = (By.CSS_SELECTOR, 'test')


def windows(value):
    return value * 2
