from os import getenv

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class LoginPage:
    base_url: str = getenv('TEST_URL')
    url: str = base_url + "admin/login"
    url_after_login: str = base_url + "admin/dashboard"

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.email_field: (By, str) = (By.ID, "email")
        self.password_field: (By, str) = (By.ID, "password")
        self.login_button: (By, str) = (By.CLASS_NAME, "btn")

    def wait_for_login_page(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located (self.email_field)
        )

    def wait_for_main_page(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.url_to_be(self.url_after_login)
        )

    def open_page(self) -> None:
        self.driver.get(self.url)
        self.wait_for_login_page()

    def login(self, email: str, password: str) -> None:
        self.driver.find_element(*self.email_field).send_keys(email)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        self.wait_for_main_page()
