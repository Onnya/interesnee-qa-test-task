from os import getenv

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages import LoginPage


@pytest.fixture
def browser() -> WebDriver:
    options: Options = webdriver.ChromeOptions()
    options_str = ["--no-sandbox", "--headless", "--disable-dev-shm-usage",
                   "--remote-debugging-pipe"]
    for option_value in options_str:
        options.add_argument(option_value)
    driver: WebDriver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login(browser: WebDriver) -> WebDriver:
    login_page: LoginPage = LoginPage(browser)
    login_page.open_page()
    email: str = getenv("TEST_EMAIL")
    password: str = getenv("TEST_PASSWORD")
    if email is None or password is None:
        pytest.skip("Please set TEST_EMAIL and TEST_PASSWORD")
    login_page.login(email, password)
    yield browser
