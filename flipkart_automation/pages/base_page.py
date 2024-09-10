import allure
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from utils.screenshot import ScreenshotManager
from utils.logger import Logger


# POCO Class to handle browser details
class POCO:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver


class BasePage:
    actual_text = None
    actual_title = None

    def __init__(self, poco: POCO):
        self.timeout = None
        self.driver = poco.driver
        self.wait = WebDriverWait(self.driver, 10)
        self.screenshot_manager = ScreenshotManager(self.driver)

    @staticmethod
    def setup_logger():
        """Sets up logging to file and console."""
        Logger.log_test_step("Navigating to the product page")

    def find_element(self, by, value, step_name="find_element"):
        """Finds element with proper logging, allure reporting, and screenshot capture."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                ec.presence_of_element_located((by, value))
            )
            Logger.log_info(f"Element found: {value}")
            self.screenshot_manager.capture_screenshot(step_name)
            return element
        except TimeoutException as e:
            Logger.log_error(f"Timeout: Element not found: {value}: {str(e)}")
            self.screenshot_manager.capture_screenshot(step_name)
            allure.attach(f"Timeout: Element not found: {value}", name=step_name,
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"TimeoutException: Could not find element: {value}")

    def click_element(self, by, value, step_name="click_element"):
        """Clicks an element and logs action, with allure and screenshot capture."""
        try:
            element = self.find_element(by, value, step_name)
            element.click()
            Logger.log_info(f"Clicked element: {value}")
            self.screenshot_manager.capture_screenshot(step_name)
        except Exception as e:
            Logger.log_error(f"Error clicking element {value}: {str(e)}")
            self.screenshot_manager.capture_screenshot(step_name)
            pytest.fail(f"Error in clicking element: {value}")

    def send_keys(self, by, value, text, step_name="send_keys"):
        """Send keys to an input field with logging, allure, and screenshot capture."""
        try:
            element = self.find_element(by, value, step_name)
            element.clear()
            element.send_keys(text)
            Logger.log_info(f"Sent keys '{text}' to element: {value}")
            self.screenshot_manager.capture_screenshot(step_name)
        except Exception as e:
            Logger.log_error(f"Error sending keys to element {value}: {str(e)}")
            self.screenshot_manager.capture_screenshot(step_name)
            pytest.fail(f"Error in sending keys to element: {value}")

    def verify_element_text(self, by, value, expected_text, step_name="verify_element_text"):
        """Verify that an element contains the expected text, with logging, allure, and screenshot capture."""
        try:
            element = self.find_element(by, value, step_name)
            BasePage.actual_text = element.text
            assert BasePage.actual_text == expected_text, f"Expected text: {expected_text}, but got: {BasePage.actual_text}"
            Logger.log_info(f"Verified element text: {expected_text}")
            self.screenshot_manager.capture_screenshot(step_name)
        except AssertionError as e:
            Logger.log_error(f"AssertionError in verifying text for {value}: {str(e)}")
            self.screenshot_manager.capture_screenshot(step_name)
            allure.attach(f"Text Assertion failed for {value}. Expected: {expected_text}, Found: {BasePage.actual_text}",
                          name=step_name, attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"AssertionError: {str(e)}")

    def wait_for_element_to_be_clickable(self, by, value, step_name="wait_for_element_to_be_clickable"):
        """Wait for element to be clickable before performing any action."""
        try:
            WebDriverWait(self.driver, self.timeout).until(ec.element_to_be_clickable((by, value)))
            Logger.log_info(f"Element is clickable: {value}")
            self.screenshot_manager.capture_screenshot(step_name)
        except TimeoutException as e:
            Logger.log_error(f"Timeout: Element not clickable: {value}: {str(e)}")
            self.screenshot_manager.capture_screenshot(step_name)
            allure.attach(f"Timeout: Element not clickable: {value}", name=step_name,
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"TimeoutException: Element not clickable: {value}")

    def verify_page_title(self, expected_title, step_name="verify_page_title"):
        """Verifies the page title with logging, allure report, and screenshot capture."""
        try:
            BasePage.actual_title = self.driver.title
            assert BasePage.actual_title == expected_title, f"Expected title: {expected_title}, but got: {BasePage.actual_title}"
            Logger.log_info(f"Page title verified: {expected_title}")
            self.screenshot_manager.capture_screenshot(step_name)
        except AssertionError as e:
            Logger.log_error(f"Page title mismatch: Expected {expected_title}, Found {BasePage.actual_title}")
            self.screenshot_manager.capture_screenshot(step_name)
            allure.attach(f"Page title mismatch. Expected: {expected_title}, Found: {BasePage.actual_title}", name=step_name,
                          attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"AssertionError: {str(e)}")

    def navigate_to_url(self, url, step_name="navigate_to_url"):
        """Navigates to a specific URL with proper logging, allure, and screenshot capture."""
        try:
            self.driver.get(url)
            Logger.log_info(f"Navigated to URL: {url}")
            self.screenshot_manager.capture_screenshot(step_name)
        except Exception as e:
            Logger.log_error(f"Failed to navigate to URL: {url} - {str(e)}")
            self.screenshot_manager.capture_screenshot(step_name)
            pytest.fail(f"Error navigating to URL: {url}")

    def wait_for_element(self, locator):
        """Wait for element to be present."""
        try:
            element = self.wait.until(ec.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.screenshot_manager.capture_screenshot("element_not_found")
            logging.error(f"Element not found: {locator}")
            pytest.fail(f"Timeout while waiting for element: {locator}")

    def wait_for_clickable(self, locator):
        """Wait for element to be clickable."""
        try:
            element = self.wait.until(ec.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            self.screenshot_manager.capture_screenshot("element_not_clickable")
            logging.error(f"Element not clickable: {locator}")
            pytest.fail(f"Timeout while waiting for clickable element: {locator}")

    def click(self, locator, element_name):
        """Click an element."""
        element = self.wait_for_clickable(locator)
        try:
            element.click()
            logging.info(f"Clicked on {element_name}")
            allure.attach(self.screenshot_manager.capture_screenshot(element_name), name=element_name,
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logging.error(f"Error clicking on {element_name}: {e}")
            self.screenshot_manager.capture_screenshot(f"click_error_{element_name}")
            pytest.fail(f"Failed to click on {element_name}")

    def enter_text(self, locator, text, element_name):
        """Enter text into an input field."""
        element = self.wait_for_element(locator)
        try:
            element.clear()
            element.send_keys(text)
            logging.info(f"Entered text '{text}' into {element_name}")
            allure.attach(self.screenshot_manager.capture_screenshot(element_name), name=element_name,
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logging.error(f"Error entering text into {element_name}: {e}")
            self.screenshot_manager.capture_screenshot(f"text_entry_error_{element_name}")
            pytest.fail(f"Failed to enter text in {element_name}")

    def get_text(self, locator, element_name):
        """Get the text of an element."""
        element = self.wait_for_element(locator)
        try:
            text = element.text
            logging.info(f"Retrieved text from {element_name}: {text}")
            allure.attach(self.screenshot_manager.capture_screenshot(element_name), name=element_name,
                          attachment_type=allure.attachment_type.PNG)
            return text
        except Exception as e:
            logging.error(f"Error getting text from {element_name}: {e}")
            self.screenshot_manager.capture_screenshot(f"get_text_error_{element_name}")
            pytest.fail(f"Failed to retrieve text from {element_name}")

    def verify_title(self, expected_title):
        """Verify the page title."""
        try:
            assert expected_title in self.driver.title, f"Expected title '{expected_title}' not found in '{self.driver.title}'"
            logging.info(f"Page title verified: {expected_title}")
            allure.attach(self.screenshot_manager.capture_screenshot("page_title_verified"), name="page_title",
                          attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logging.error(f"Title verification failed: {e}")
            self.screenshot_manager.capture_screenshot("title_verification_failed")
            pytest.fail(f"Title verification failed: {expected_title}")


class Product:
    """POCO class to represent a product."""

    def __init__(self, name="", price=0, availability=False):
        self.name = name
        self.price = price
        self.availability = availability

    def __str__(self):
        return f"Product(name={self.name}, price={self.price}, availability={self.availability})"


class CartItem(Product):
    """POCO class to represent an item in the cart, extends Product."""

    def __init__(self, name="", price=0, availability=False, quantity=1):
        super().__init__(name, price, availability)
        self.quantity = quantity

    def __str__(self):
        return f"CartItem(name={self.name}, price={self.price}, availability={self.availability}, quantity={self.quantity})"


class Cart:
    """POCO class to represent the cart."""

    def __init__(self):
        self.items = []

    def add_item(self, cart_item):
        self.items.append(cart_item)

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.items)

    def __str__(self):
        return f"Cart(items={[str(item) for item in self.items]})"