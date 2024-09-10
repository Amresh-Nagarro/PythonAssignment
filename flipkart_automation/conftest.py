import allure
import pytest
from utils import BrowserManager, Logger, ScreenshotManager
from pages import BasePage, HomePage, CartPage, ProductPage

# Global variables for WebDriver and Logger
logger = None
screenshot_manager = None

# Fixture for browser management
@pytest.fixture(scope="session")
def browser_manager(request):
    """
    Fixture to manage the browser setup and teardown. The browser name is configured via pytest.ini or
    command-line arguments. This fixture also captures screenshots and logs on test failure.
    """

    Logger.log_test_step("Initializing browser manager fixture")
    browser_name = request.config.getoption("--browser")  # Getting browser option from pytest.ini or command line
    manager = BrowserManager(browser_name)
    driver = manager.start_browser()

    base_page = BasePage(driver)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    yield driver, base_page, home_page, product_page, cart_page

    if request.node.rep_call.failed:
        test_name = request.node.name
        ScreenshotManager.capture_screenshot(driver, test_name)
        Logger.log_error(f"Test failed: {test_name} - Screenshot captured")
        allure.attach.file(ScreenshotManager.capture_screenshot(driver, test_name), name=f"Screenshot on Failure {test_name}", attachment_type=allure.attachment_type.PNG)

    manager.close_browser()

def pytest_addoption(parser):
    """
    Pytest hook to add custom command-line options. Adds support for specifying the browser to be used.
    """
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for testing: chrome or firefox")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook that is executed after each test. It captures the outcome of the test and logs
    the results. It also attaches screenshots to reports if the test fails.
    """
    outcome = yield
    report = outcome.get_result()

    # Setting a custom attribute to store test result info (useful for capturing screenshots on failure)
    setattr(item, "rep_" + report.when, report)

    if report.when == "call" and report.failed:
        Logger.log_error(f"Test failed: {item.name}")
        driver = item.funcargs['browser_manager'][0]
        ScreenshotManager.capture_screenshot(driver, item.name)


@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    """
    Fixture that initializes logging at the start of the session.
    Logs information regarding the test session start and attaches logging output to reports.
    """
    Logger.get_logger()
    Logger.log_test_step("Test session setup complete")
    yield
    Logger.log_test_step("Test session teardown")

# @pytest.fixture(scope="session", autouse=True)
# def setup_allure_environment():
#     """
#     Fixture to configure Allure reporting. Customizes the environment information for Allure reports.
#     """
#     create_environment_file()
#     Logger.log_test_step("Allure environment setup complete")

# Test Assertions: Adding log and allure report attachment
@pytest.fixture
def assert_with_logging():
    """
    Custom assertion function with proper logging and Allure report attachment for any assertion errors.
    """
    def _assertion(condition, message):
        try:
            assert condition, message
            Logger.log_test_step(f"Assertion Passed: {message}")
        except AssertionError:
            Logger.log_error(f"Assertion Failed: {message}")
            allure.attach(body=message, name="Assertion Failure", attachment_type=allure.attachment_type.TEXT)
            raise
    return _assertion

@pytest.fixture(autouse=True)
def setup_and_teardown(request):
    """Pytest fixture to handle setup and teardown for each test."""
    Logger.log_info(f"Starting test: {request.node.name}")
    browser_name = request.config.getoption("--browser")  # Getting browser option from pytest.ini or command line
    manager = BrowserManager(browser_name)
    driver = manager.start_browser()

    # Attach screenshots for failed tests
    yield

    if request.node.rep_call.failed:
        screenshot_name = f"{request.node.name}_failure"
        ScreenshotManager.capture_screenshot(driver, screenshot_name)

    Logger.log_info(f"Completed test: {request.node.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Pytest hook to configure Allure reporting."""
    config.project_metadata = {
        'Project Name': 'Flipkart Automation Framework',
        'Test Cases': 'BDD Tests for item ordering',
        'Version': '1.0',
        'Browser': 'Chrome'
    }

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Pytest hook to handle session finish."""
    metadata = session.config.project_metadata
    print(metadata)

    # Log session end
    Logger.log_info(f"Test session finished with status: {exitstatus}")

    # Attach Allure reports at the end of the session
    allure.attach(
        name="Session End Report",
        body=f"Session finished with status: {exitstatus}",
        attachment_type=allure.attachment_type.TEXT
    )

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Pytest hook to log test start."""
    Logger.log_info(f"Starting test: {item}")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item):
    """Pytest hook to log test teardown."""
    Logger.log_info(f"Completed test: {item}")