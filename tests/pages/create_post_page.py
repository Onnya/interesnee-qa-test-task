from os import getenv
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class CreatePostPage:
    base_url: str = getenv('TEST_URL')
    url: str = base_url + "admin/create"

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.title_field: (By, str) = (By.ID, "title")
        self.content_field: (By, str) = (By.CLASS_NAME, "ql-editor")
        self.author_field: (By, str) = (By.ID, "author")
        self.create_post_button: (By, str) = (By.CLASS_NAME, "btn")
        self.created_alert: (By, str) = (By.CLASS_NAME, "alert-success")

    def wait_for_create_post__page(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(self.content_field)
        )

    def create_post(self, title: str, content: str, author: str) -> None:
        self.wait_for_create_post__page()
        self.driver.find_element(*self.title_field).send_keys(title)
        content_field: WebElement = self.driver.find_element(*self.content_field)
        for char in content:
            self.driver.execute_script(
                """
                var element = arguments[0];
                var char = arguments[1];
                var event = new KeyboardEvent('keydown', {'key': char});
                element.dispatchEvent(event);
                element.textContent += char;
                """,
                content_field, char
            )
        self.driver.find_element(*self.author_field).send_keys(author)
        self.driver.find_element(*self.create_post_button).click()

    def is_alert_displayed(self) -> (bool, str):
        try:
            WebDriverWait(self.driver, 5).until(
                ec.visibility_of_element_located(self.created_alert)
            )
            alert_text: str = (self.driver.find_element(*self.created_alert)
                               .find_element(By.CSS_SELECTOR, "p")).text
            return True, alert_text
        except NoSuchElementException:
            return False, ""

    def get_create_post_validations(self) -> List[str]:
        return list(map(lambda x:
                        x.find_element(By.TAG_NAME, "small").text,
                        self.driver.find_elements(By.CLASS_NAME, "validation")))
