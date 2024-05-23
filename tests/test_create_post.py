from datetime import datetime
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from pages import DashboardPage, CreatePostPage


def test_create_post(login: WebDriver) -> None:
    post_title, post_content, post_author = "Test title", "Test content", "Test author"

    browser: WebDriver = login

    dashboard_page: DashboardPage = DashboardPage(browser)
    dashboard_page.create_new_post()

    create_post_page: CreatePostPage = CreatePostPage(browser)
    create_post_page.create_post(post_title, post_content, post_author)

    now_datetime: datetime = datetime.now()
    month: str = now_datetime.strftime('%b')
    day: str = str(now_datetime.day)
    year: str = str(now_datetime.year)
    hour: str = now_datetime.strftime('%I').lstrip('0')
    minute: str = now_datetime.strftime('%M')
    second: str = now_datetime.strftime('%S')
    period: str = now_datetime.strftime('%p')
    formatted_date: str = f'{month} {day}, {year}, {hour}:{minute}:{second} {period}'

    is_alert_shown, alert_text = create_post_page.is_alert_displayed()
    expected_alert_text: str = "Post was successfully created!"

    assert is_alert_shown, "Notification is not shown"
    assert alert_text == expected_alert_text, \
        f"Wrong alert text, expected: {expected_alert_text}, got: {alert_text}"

    dashboard_page.open_page()
    actual_author, actual_title, actual_date = dashboard_page.get_last_row_data()

    assert actual_author == post_author, \
        f"Wrong author, expected: {post_author}, got: {actual_author}"
    assert actual_title == post_title, \
        f"Wrong author, expected: {post_title}, got: {actual_title}"
    assert actual_date == formatted_date, \
        f"Wrong author, expected: {formatted_date}, got: {actual_date}"


def test_create_post_validation(login: WebDriver) -> None:
    browser: WebDriver = login

    dashboard_page: DashboardPage = DashboardPage(browser)
    dashboard_page.create_new_post()

    create_post_page: CreatePostPage = CreatePostPage(browser)
    create_post_page.create_post("", "", "")
    validations: List[str] = create_post_page.get_create_post_validations()

    assert len(validations) == 3, \
        f"Expected 3 validations, got {len(validations)}: {", ".join(validations)}"

    assert validations[0] == "Title cannot be empty!", \
        f"Incorrect title validation: {validations[0]}"
    assert validations[1] == "Content cannot be empty!", \
        f"Incorrect content validation: {validations[1]}"
    assert validations[2] == "Author cannot be empty!", \
        f"Incorrect author validation: {validations[2]}"
