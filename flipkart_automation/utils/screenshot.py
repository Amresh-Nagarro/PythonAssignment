import os
import pytest
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime
from utils.logger import Logger

class ScreenshotManager:
    """Utility class for capturing and managing screenshots."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._create_screenshot_dir()

    @staticmethod
    def _create_screenshot_dir():
        """Create the screenshots directory if it doesn't exist."""
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        return screenshots_dir

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self):
        """Pytest hook to clear the screenshots directory before each test."""
        self._clear_screenshot_dir()

    @staticmethod
    def _clear_screenshot_dir():
        """Clear all files in the screenshots directory."""
        screenshots_dir = ScreenshotManager._create_screenshot_dir()
        for file_name in os.listdir(screenshots_dir):
            file_path = os.path.join(screenshots_dir, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                Logger.get_logger().error(f"Error while clearing '{file_path}': {str(e)}")

    def capture_screenshot(self, test_name: str):
        """Capture a screenshot and save it with the provided name."""
        try:
            if self.driver:
                # Get the timestamp for unique screenshot naming
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Create a proper screenshot name with the test name and timestamp
                screenshot_name = f"{test_name}_{timestamp}.png"

                # Define the path where the screenshot will be stored
                screenshots_dir = ScreenshotManager._create_screenshot_dir()
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)

                # Capture the screenshot
                self.driver.save_screenshot(screenshot_path)

                # Attach screenshot to Allure report
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(image_file.read(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)

                # Log the success
                Logger.get_logger().info(f"Screenshot saved at {screenshot_path}")
                print(f"Screenshot saved as: {screenshot_path}")

                return screenshot_path
            else:
                raise RuntimeError("WebDriver is not initialized.")
        except Exception as e:
            print(f"Failed to capture screenshot '{test_name}': {str(e)}")
            pytest.fail(f"Failed to capture screenshot '{test_name}': {str(e)}")
            print(f"Failed to attach screenshot '{test_name}' to Allure report: {str(e)}")
            Logger.get_logger().error(f"Failed to capture screenshot: {e}")
            return ""

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_makereport(self, item, call):
        """Pytest hook to capture screenshots on test failure."""
        if call.when == 'call' and call.excinfo is not None:
            screenshot_name = f"{item.name}_failure"
            self.capture_screenshot(screenshot_name)
