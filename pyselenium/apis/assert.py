from selenium.webdriver.support.expected_conditions import *


def assert_title(driver, title):
    """An expectation for checking the title of a page.
    title is the expected title, which must be an exact match
    """
    if not title_is(title)(driver):
        raise AssertionError('title no matches `%s`' % str(title))


def assert_title_contains(driver, title):
    """ An expectation for checking that the title contains a case-sensitive
    substring. title is the fragment of title expected
    """
    if not title_contains(title)(driver):
        raise AssertionError('`%s` is not the fragment of title expected' % str(title))


def assert_presence_of_element_located(driver, locator):
    """ An expectation for checking that an element is present on the DOM
    of a page. This does not necessarily mean that the element is visible.
    locator - used to find the element
    """
    if not presence_of_element_located(locator)(driver):
        raise AssertionError('The `%s` of webElement no presence' % str(locator))


def assert_url_contains(driver, url):
    """ An expectation for checking that the current url contains a
    case-sensitive substring.
    url is the fragment of url expected
    """
    if not url_contains(url)(driver):
        raise AssertionError('current url not contains `%s`' % url)


def assert_url_matches(driver, pattern):
    """An expectation for checking the current url.
    pattern is the expected pattern, which must be an exact match
    returns True if the url matches, false otherwise."""
    if not url_matches(pattern)(driver):
        raise AssertionError('current url not exact pattern of ``' % pattern)


def assert_url_to_be(driver, url):
    """An expectation for checking the current url.
    url is the expected url, which must be an exact match
    """
    if not url_to_be(url)(driver):
        raise AssertionError('current url not equals `%s`' % url)


def assert_text_to_be_present_in_element(driver, locator, text_):
    """ An expectation for checking if the given text is present in the
    specified element.
    locator, text
    """
    if not text_to_be_present_in_element(locator, text_)(driver):
        raise AssertionError('`%s` present not in `%s` of element' % (text_, str(locator)))


def assert_text_to_be_present_in_element_value(driver, locator, text_):
    """
    An expectation for checking if the given text is present in the element's
    locator, text
    """
    if not text_to_be_present_in_element_value(locator, text_)(driver):
        raise AssertionError('`%s` present not in `%s` of element' % (text_, str(locator)))


def assert_element_to_be_clickable(driver, locator):
    """ An Expectation for checking an element is visible and enabled such that
    you can click it."""
    if not element_to_be_clickable(locator)(driver):
        raise AssertionError('`%s` of element is not clickable' % str(locator))


def assert_number_of_windows_to_be(driver, num_windows):
    """ An expectation for the number of windows to be a certain value."""
    if not number_of_windows_to_be(num_windows)(driver):
        raise AssertionError('number_of_windows is not equal `%s`' % num_windows)


def assert_new_window_is_opened(driver, current_handles):
    """ An expectation that a new window will be opened and have the number of
    windows handles increase"""
    if not new_window_is_opened(current_handles)(driver):
        raise AssertionError('new_window is not opened')


def assert_alert_is_present(driver):
    """ Expect an alert to be present."""
    if not alert_is_present()(driver):
        raise AssertionError('present is not alert')

