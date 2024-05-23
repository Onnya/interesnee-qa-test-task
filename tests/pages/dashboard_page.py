from os import getenv
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement


class DashboardPage:
    base_url: str = getenv('TEST_URL')
    url: str = base_url + "admin/dashboard"

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.create_post_link: (By, str) = (By.LINK_TEXT, "Create post")
        self.table: (By, str) = (By.CSS_SELECTOR, "table")

    def wait_for_dashboard_page(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(self.create_post_link)
        )

    def wait_for_dashboard_table(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(self.table)
        )

    def open_page(self) -> None:
        self.driver.get(self.url)
        self.wait_for_dashboard_table()

    def create_new_post(self) -> None:
        self.wait_for_dashboard_page()
        self.driver.find_element(*self.create_post_link).click()

    def get_last_row_data(self) -> List[str]:
        table: WebElement = self.driver.find_element(*self.table)
        data: List[WebElement] = (table.find_elements(By.TAG_NAME, "tr")[-1]
                                  .find_elements(By.TAG_NAME, "td"))
        return list(map(lambda x: x.text, data))[1:4]
