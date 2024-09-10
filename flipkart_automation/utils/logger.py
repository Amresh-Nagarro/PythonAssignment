import logging
from logging.handlers import RotatingFileHandler

import allure
import pytest
import os
from datetime import datetime


class Logger:
    """Utility class to manage logging throughout the automation framework."""

    _logger = None
    _formatter = None
    log_file = "automation.log"

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self._create_log_dir()
        self._setup_handlers()

    @staticmethod
    def get_logger():
        """
        Creates and returns a logger instance with a specific configuration.

        :return: Configured logger instance.
        """
        if Logger._logger is None:
            Logger._logger = logging.getLogger(name="automation_framework_logger")
            Logger._logger.setLevel(logging.INFO)
            Logger._create_log_dir()

            log_file_path = os.path.join(Logger._create_log_dir(), Logger.log_file)

            # Define logging format
            Logger._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Add the handler to the logger
            Logger._logger.addHandler(Logger._rotating_file_handler(log_file_path, Logger._formatter))

            Logger._setup_handlers()

        if not Logger._logger.hasHandlers():  # Ensure we don't add multiple handlers to the logger
            Logger._logger.setLevel(logging.INFO)
            return Logger._setup_handlers

        return Logger._logger

    @staticmethod
    def _create_log_dir():
        """Create log directory if it doesn't exist."""
        # Create log directory if it doesn't exist
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    @staticmethod
    def _rotating_file_handler(log_file_path: str, _formatter: logging.Formatter = None):
        # Create rotating file handler to ensure logs don't grow too large
        handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3)
        handler.setLevel(logging.INFO)
        handler.setFormatter(_formatter)

        return handler

    @staticmethod
    def _setup_handlers():
        """Set up console and file handlers for logging."""
        # Console Handler to output or print logs to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(Logger._formatter)

        # File Handler to write logs to a file
        file_handler = logging.FileHandler(Logger._get_log_file_name())
        file_handler.setLevel(logging.INFO)

        # Formatter for the logs
        file_handler.setFormatter(Logger._formatter)

        # Adding the handlers to logger
        Logger._logger.addHandler(console_handler)
        Logger._logger.addHandler(file_handler)

    @staticmethod
    def _get_log_file_name():
        """Generate a log file name with timestamp."""
        # Log file path with timestamp
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename =  f"logs/test_log_{now}.log"
        log_file = os.path.join(Logger._create_log_dir(), filename)
        return log_file

    @allure.step("Logging message: '{message}'")
    def log_info(self, message: str):
        """Log an info level message."""
        self.logger.info(message)

    @staticmethod
    def log_test_step(step_description: str):
        """
        Log each test step and attach it to Allure reports.
        :param step_description: A brief description of the test step being executed.
        """
        logger = Logger.get_logger()
        logger.info(step_description)
        # Attach the step description to the Allure report
        allure.step(step_description)

    @staticmethod
    def log_assertion(message: str, status: bool):
        """
        Log the result of an assertion.
        :param message: Assertion message to log.
        :param status: Boolean indicating pass/fail of the assertion.
        """
        logger = Logger.get_logger()
        if status:
            logger.info(f"Assertion Passed: {message}")
            allure.attach(f"Assertion Passed: {message}", name="Assertion", attachment_type=allure.attachment_type.TEXT)
        else:
            logger.error(f"Assertion Failed: {message}")
            allure.attach(f"Assertion Failed: {message}", name="Assertion", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Logging error message: '{message}'")
    def log_error(self, error_message: str):
        """
        Log any error that occurs during test execution.
        :param error_message: Error description.
        """
        logger = Logger.get_logger()
        logger.error(error_message)
        allure.attach(error_message, name="Error", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Logging warning message: '{message}'")
    def log_warning(self, message: str):
        """Log a warning level message."""
        self.logger.warning(message)

    @allure.step("Capture screenshot for logging: '{screenshot_name}'")
    def log_screenshot(self, screenshot_name: str):
        """
        Log and attach screenshot to the Allure report.
        :param screenshot_name: Name of the screenshot captured.
        """
        screenshot_path = f"screenshots/{screenshot_name}.png"

        logger = Logger.get_logger()
        logger.info(f"Screenshot captured at: {screenshot_path}")

        try:
            if os.path.exists(screenshot_path):
                with open(screenshot_path, 'rb') as image_file:
                    allure.attach(image_file.read(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
            else:
                self.log_warning(f"Screenshot '{screenshot_name}' does not exist.")
        except Exception as e:
            logger.error(f"Failed to attach screenshot to Allure report: {e}")

    # @pytest.hookimpl(tryfirst=True)
    # def pytest_runtest_setup(self, item):
    #     """Pytest hook to log test start."""
    #     self.log_info(f"Starting test: {item.name}")

    # @pytest.hookimpl(tryfirst=True)
    # def pytest_runtest_makereport(self, item, call):
    #     """Pytest hook to log test result."""
    #     if call.when == 'call':
    #         outcome = 'Passed' if call.excinfo is None else 'Failed'
    #         self.log_info(f"Test '{item.name}' - Outcome: {outcome}")
    #
    #     if call.when == 'call' and call.excinfo is not None:
    #         self.log_screenshot(f"{item.name}_failure")
    #         self.log_error(f"Test '{item.name}' failed with exception: {call.excinfo.value}")

    # @pytest.hookimpl(tryfirst=True)
    # def pytest_runtest_teardown(self, item):
    #     """Pytest hook to log test teardown."""
    #     self.log_info(f"Completed test: {item.name}")
