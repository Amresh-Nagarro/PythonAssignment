import allure
import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Product
from utils.screenshot import ScreenshotManager
from utils.logger import Logger

class ProductPage(BasePage):
    # Locators for elements on the product page
    availability_pin_code_input = (By.XPATH, "//input[@placeholder='Enter Delivery Pincode']")
    check_availability_button = (By.XPATH, "//span[contains(text(),'Check')]")
    add_to_cart_button = (By.XPATH, "//button[contains(text(),'Add to cart')]")
    product_title_locator = (By.XPATH, "//span[@class='B_NuCI']")  # Title of the product
    price_locator = (By.XPATH, "//div[@class='_30jeq3 _16Jk6d']")  # Price of the product
    PRODUCT_NAME = (By.CSS_SELECTOR, "span.B_NuCI")  # Locator for product name
    PRODUCT_PRICE = (By.CSS_SELECTOR, "div._30jeq3")  # Locator for product price
    PINCODE_INPUT = (By.CSS_SELECTOR, "input._36yFo0")  # Locator for pincode input
    CHECK_AVAILABILITY_BUTTON = (By.CSS_SELECTOR, "span._2P_LDn")  # Locator for check pincode button
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button._2KpZ6l._2U9uOA._3v1-ww")  # Locator for Add to Cart button
    GO_TO_CART_BUTTON = (By.CSS_SELECTOR, "a._3SkBxJ")  # Locator for Go to Cart button

    def __init__(self, driver):
        #super().__init__(poco)
        super().__init__(driver)
        self.screenshot_manager = ScreenshotManager(self.driver)
        self.logger = Logger.get_logger()
        self.product = Product()  # Initialize Product POCO

    @allure.step("Verify product title is '{expected_title}'")
    def verify_product_title(self, expected_title):
        """Verify that the product title matches the expected title."""
        try:
            title_element = self.find_element(*self.product_title_locator, step_name="Get product title")
            actual_title = title_element.text.strip()
            assert actual_title == expected_title, f"Expected title: '{expected_title}', but got: '{actual_title}'"
            self.logger.info(f"Product title verified as '{expected_title}'.")
        except AssertionError as e:
            self.screenshot_manager.capture_screenshot("verify_product_title_error")
            self.logger.error(f"AssertionError: {str(e)}")
            pytest.fail(f"AssertionError: {str(e)}")

    @allure.step("Verify product price is '{expected_price}'")
    def verify_product_price(self, expected_price):
        """Verify that the product price matches the expected price."""
        try:
            price_element = self.find_element(*self.price_locator, step_name="Get product price")
            actual_price = price_element.text.replace('₹', '').replace(',', '').strip()
            assert actual_price == str(expected_price), f"Expected price: ₹{expected_price}, but got: ₹{actual_price}"
            self.logger.info(f"Product price verified as ₹{expected_price}.")
        except AssertionError as e:
            self.screenshot_manager.capture_screenshot("verify_product_price_error")
            self.logger.error(f"AssertionError: {str(e)}")
            pytest.fail(f"AssertionError: {str(e)}")

    @allure.step("Get the product price from the page")
    def get_product_price(self):
        """Retrieve the current product price from the page."""
        price_element = self.find_element(*self.price_locator, step_name="Fetch product price")
        return price_element.text.replace('₹', '').replace(',', '').strip()

    @allure.step("Get the product title from the page")
    def get_product_title(self):
        """Retrieve the current product title from the page."""
        title_element = self.find_element(*self.product_title_locator, step_name="Fetch product title")
        return title_element.text.strip()

    def get_product_name_and_price(self):
        """Fetches the product name and price, logs, and attaches screenshots."""
        product_name = self.get_text(self.PRODUCT_NAME, "Product Name")
        product_price = self.extract_price(self.get_text(self.PRODUCT_PRICE, "Product Price"))

        self.logger.info(f"Product Name: {product_name}")
        self.logger.info(f"Product Price: {product_price}")
        allure.attach(self.screenshot_manager.capture_screenshot("product_details"), name="Product Details", attachment_type=allure.attachment_type.PNG)

        # Save details into Product POCO
        self.product.name = product_name
        self.product.price = product_price

    @allure.step("Check product availability for pincode '{pincode}'")
    def check_availability(self, pincode):
        """Check the product's availability by entering the pincode."""
        self.enter_text(self.PINCODE_INPUT, pincode, "Pincode Input")
        self.click_element(self.CHECK_AVAILABILITY_BUTTON, "Check Availability Button")

        # Capture screenshot after checking availability
        allure.attach(self.screenshot_manager.capture_screenshot(f"availability_{self.product.name}"), name=f"Availability for {self.product.name}", attachment_type=allure.attachment_type.PNG)
        self.logger.info(f"Checked availability for product {self.product.name} with pincode {pincode}")

    @allure.step("Add product to cart")
    def add_product_to_cart(self):
        """Adds the product to the cart and logs the action."""
        self.click_element(self.ADD_TO_CART_BUTTON, "Add to Cart Button")
        allure.attach(self.screenshot_manager.capture_screenshot(f"added_{self.product.name}_to_cart"), name=f"Added {self.product.name} to cart", attachment_type=allure.attachment_type.PNG)

        self.logger.info(f"Product {self.product.name} added to cart with price {self.product.price}")

    def go_to_cart(self):
        """Navigates to the cart."""
        self.click_element(self.GO_TO_CART_BUTTON, "Go to Cart Button")
        allure.attach(self.screenshot_manager.capture_screenshot("go_to_cart"), name="Go to Cart", attachment_type=allure.attachment_type.PNG)

        self.logger.info(f"Navigated to Cart after adding product: {self.product.name}")

    @staticmethod
    def extract_price(price_text):
        """Extracts price from string format (₹12,345) to integer format (12345)."""
        return int(price_text.replace("₹", "").replace(",", ""))