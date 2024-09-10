import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.logger import Logger
from utils.screenshot import ScreenshotManager

class BrowserManager:
    """Class responsible for initializing and managing browser instances."""

    def __init__(self, browser_name = "chrome"):
        """
        Initializes the browser manager with the specified browser name.
        :param browser_name: The name of the browser to use for testing. Default is Chrome.
        """
        self.browser_name = browser_name.lower()
        self.driver = None
        self.logger = Logger.get_logger()

    @allure.step("Initialize and open the browser")
    def start_browser(self):
        """
        Initializes the browser based on the browser_name attribute.
        Supports Chrome and Firefox. Attaches logs and screenshots.
        :return: WebDriver instance.
        """

        Logger.log_test_step(f"Initializing {self.browser_name} browser")

        try:
            if self.browser_name == 'chrome':
                options = ChromeOptions()
                options.add_argument("--start-maximized")
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            elif self.browser_name == 'firefox':
                options = FirefoxOptions()
                options.add_argument("--start-maximized")
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            else:
                raise ValueError(f"Browser '{self.browser_name}' is not supported.")

            self.driver.implicitly_wait(10)
            Logger.log_test_step(f"{self.browser_name.capitalize()} browser launched successfully.")
            self.capture_screenshot("browser_launched_successfully")
        except Exception as e:
            Logger.log_error(f"Error initializing browser: {e}")
            self.logger.error(f"Failed to start browser '{self.browser_name}': {str(e)}")
            pytest.fail(f"Failed to start browser '{self.browser_name}': {str(e)}")
            raise

    @allure.step("Close the browser")
    def close_browser(self):
        """Close the browser and clean up."""

        Logger.log_test_step("Closing the browser")

        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
                Logger.log_test_step(f"{self.browser_name.capitalize()} browser closed successfully.")
        except Exception as e:
            Logger.log_error(f"Error closing browser: {e}")

            self.capture_screenshot("browser_close_error")
            self.logger.error(f"Failed to close browser: {str(e)}")
            pytest.fail(f"Failed to close browser: {str(e)}")

    @allure.step("Open URL '{url}' in the browser")
    def open_url(self, url: str):
        """Open the specified URL in the browser."""
        try:
            if self.driver:
                self.driver.get(url)
                self.logger.info(f"Opened URL: {url}")
            else:
                raise RuntimeError("Browser is not initialized.")
        except Exception as e:
            self.capture_screenshot("open_url_error")
            self.logger.error(f"Failed to open URL '{url}': {str(e)}")
            pytest.fail(f"Failed to open URL '{url}': {str(e)}")

    @allure.step("Capture screenshot with name '{screenshot_name}'")
    def capture_screenshot(self, screenshot_name: str):
        """
        Captures a screenshot on test failure and attaches it to the log and Allure report.
        :param screenshot_name: The name of the test for which the failure occurred.
        """
        try:
            if self.driver:
                Logger.log_test_step(f"Capturing screenshot for test: {screenshot_name}")
                #screenshot_path = f"screenshots/{screenshot_name}.png"
                screenshot_path = ScreenshotManager.capture_screenshot(self.driver, screenshot_name)
                self.driver.save_screenshot(screenshot_path)
                self.logger.info(f"Screenshot saved as: {screenshot_path}")
                Logger.log_screenshot(screenshot_path)
            else:
                raise RuntimeError("Browser is not initialized.")
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot '{screenshot_name}': {str(e)}")
            pytest.fail(f"Failed to capture screenshot '{screenshot_name}': {str(e)}")
            Logger.log_error(f"Failed to capture screenshot for '{screenshot_name}': {str(e)}")
            ScreenshotManager.capture_screenshot(self.driver, screenshot_name)

# Fixture for browser management
# @pytest.fixture(scope="session")
# def browser_manager(request):
#     """
#     Pytest fixture to initialize and quit browser for each test.
#     Also handles screenshot capture on failure.
#     """
#     browser_name = request.config.getoption("--browser")  # Configurable browser option from pytest.ini
#     manager = BrowserManager(browser_name)
#     driver = manager.start_browser()
#
#     yield driver
#
#     if request.node.rep_call.failed:
#         # Capture screenshot on failure
#         test_name = request.node.name
#         manager.capture_screenshot(test_name)
#
#     manager.close_browser()

# Command line option for browser selection
# def pytest_addoption(parser):
#     parser.addoption("--browser", action="store", default="chrome", help="Browser to use for testing (chrome/firefox)")

# Hook for attaching Allure reports and logging
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item):
#     """
#     Pytest hook to log test results and capture screenshots for failed tests.
#     """
#     outcome = yield
#     report = outcome.get_result()
#
#     # Set a custom attribute to store report info on the test
#     setattr(item, "rep_" + report.when, report)
#
#     if report.when == "call" and report.failed:
#         Logger.log_error(f"Test failed: {item.name}")
#         # Capture screenshot on failure (done in fixture)
#         driver = item.funcargs['browser_manager'][0]
#         ScreenshotManager.capture_screenshot(driver, item.name)