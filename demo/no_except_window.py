from selenium.webdriver.common.by import By

window1_loc = (By.CSS_SELECTOR, 'test', 3)
window2_loc = (By.CSS_SELECTOR, 'test')


def windows(value):
    return value * 2
