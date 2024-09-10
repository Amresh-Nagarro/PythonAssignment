import csv
import os
from robot.api import logger
from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary
from POCO.context_injection import get_user_context

# Initialize SeleniumLibrary
selenium_lib = SeleniumLibrary()

@keyword("Get Credentials From CSV")
def get_credentials_from_csv(file_path, row_num):
    """Reads credentials from a CSV file given a row number."""
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if row_num < len(rows):
            username, password = rows[row_num]
            return username, password
        else:
            raise IndexError(f"Row {row_num} not found in {file_path}")


@keyword("Login To ParaBank")
def login_to_parabank(username, password):
    """Logs into ParaBank application using provided username and password."""
    logger.info(f"Attempting to log in with username: {username}")

    # Inject context using POCO class
    user_context = get_user_context(username, password)

    # Elements locators
    username_field = 'name=username'
    password_field = 'name=password'
    login_button = 'xpath=//input[@value="Log In"]'

    # Interact with web elements using SeleniumLibrary
    selenium_lib.input_text(username_field, user_context.get_username())
    selenium_lib.input_text(password_field, user_context.get_password())
    selenium_lib.click_button(login_button)

    # Wait for the 'Accounts Overview' page
    selenium_lib.wait_until_page_contains_element('xpath=//a[text()="Accounts Overview"]', timeout=10)

    logger.info("Login successful. Accounts Overview page loaded.")

@keyword("Capture Screenshot")
def capture_screenshot(screenshot_dir, test_name):
    """Captures a screenshot and saves it to the specified directory with the test name."""
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
    selenium_lib.capture_page_screenshot(screenshot_path)
    logger.info(f"Screenshot saved to {screenshot_path}")

@keyword("Validate Title")
def validate_title(expected_title):
    """Validates the title of the current page."""
    actual_title = selenium_lib.get_title()
    if actual_title == expected_title:
        
        logger.info(f"Title validation passed. Found title: {actual_title}")
    else:
        logger.error(f"Title validation failed. Expected: {expected_title}, but found: {actual_title}")
        raise AssertionError(f"Title mismatch: expected {expected_title}, but got {actual_title}")

@keyword("Log Test Information")
def log_test_information(test_name, status, message):
    """Logs test status and information."""
    logger.info(f"Test Name: {test_name}")
    logger.info(f"Test Status: {status}")
    logger.info(f"Test Message: {message}")
    

def input_text(locator, value):
    from SeleniumLibrary import SeleniumLibrary
    SeleniumLibrary().input_text(locator, value)


def click_button(locator):
    from SeleniumLibrary import SeleniumLibrary
    
    SeleniumLibrary().click_button(locator)


def wait_until_page_contains_element(xpath, timeout):
    from SeleniumLibrary import SeleniumLibrary
    SeleniumLibrary().wait_until_page_contains_element(xpath, timeout)
