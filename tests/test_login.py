from selenium.webdriver.remote.webdriver import WebDriver

from pages import LoginPage


def test_login(login: WebDriver) -> None:
    assert login.current_url == LoginPage.url_after_login, \
        f"Expected {LoginPage.url_after_login}, got {login.current_url}"
