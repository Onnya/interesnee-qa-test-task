from os import getenv

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from pages import LoginPage


@pytest.fixture
def browser() -> WebDriver:
    driver: WebDriver = webdriver.Chrome()
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