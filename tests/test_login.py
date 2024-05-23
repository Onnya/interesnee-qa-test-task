from selenium.webdriver.remote.webdriver import WebDriver

from pages import LoginPage


def test_login(login: WebDriver):
    assert login.current_url == LoginPage.url_after_login
