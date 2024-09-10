import allure
import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Product, Cart
from utils.screenshot import ScreenshotManager
from utils.logger import Logger

class CartPage(BasePage):
    # Locators for elements in the cart page
    total_price_locator = (By.XPATH, "//span[contains(@class, '_2-ut7f _1WpvJ7')]")  # Locator for total price
    item_name_locator = "//a[contains(text(),'{item_name}')]"  # XPath for finding item by name
    remove_button_locator = "//a[contains(text(),'{item_name}')]/../../following-sibling::div//button[contains(text(),'Remove')]"
    CART_ITEM = (By.CSS_SELECTOR, "div._1AtVbE")  # Generic locator for cart items
    ITEM_NAME = (By.CSS_SELECTOR, "a._2Kn22P")    # Locator for item names in the cart
    ITEM_PRICE = (By.CSS_SELECTOR, "span._1vC4OE")  # Locator for item price
    REMOVE_BUTTON = (By.XPATH, "//div[text()='Remove']")  # Locator for remove button
    CONFIRM_REMOVE = (By.XPATH, "//div[text()='Remove Item']")  # Confirmation button for removing item
    TOTAL_PRICE = (By.CSS_SELECTOR, "span._1dqRvU")  # Locator for total price in the cart

    def __init__(self, driver):
        #super().__init__(poco)
        super().__init__(driver)
        self.screenshot_manager = ScreenshotManager(self.driver)
        self.logger = Logger.get_logger()
        self.cart = Cart()  # Cart object to store and manipulate cart items

    @allure.step("Verify that item '{item_name}' is present in the cart")
    def verify_item_in_cart(self, item_name):
        """Verify if a specific item is present in the cart."""
        try:
            item_locator = (By.XPATH, self.item_name_locator.format(item_name=item_name))
            element = self.find_element(*item_locator, step_name=f"Check if item '{item_name}' is in cart")
            assert element is not None, f"Item '{item_name}' is not present in the cart."
            self.logger.info(f"Verified that item '{item_name}' is in the cart.")
        except AssertionError as e:
            self.screenshot_manager.capture_screenshot(f"verify_item_in_cart_error_{item_name}")
            self.logger.error(f"AssertionError: {str(e)}")
            pytest.fail(f"AssertionError: {str(e)}")

    @allure.step("Remove item '{item_name}' from the cart")
    def remove_item_from_cart(self, item_name):
        """Remove a specific item from the cart."""
        try:
            remove_button = (By.XPATH, self.remove_button_locator.format(item_name=item_name))
            self.click_element(*remove_button, step_name=f"Click 'Remove' for item '{item_name}'")
            self.logger.info(f"Item '{item_name}' has been removed from the cart.")
        except Exception as e:
            self.screenshot_manager.capture_screenshot(f"remove_item_error_{item_name}")
            self.logger.error(f"Failed to remove item '{item_name}' from the cart: {str(e)}")
            pytest.fail(f"Failed to remove item '{item_name}' from the cart: {str(e)}")

    @allure.step("Verify that item '{item_name}' is not present in the cart after removal")
    def verify_item_removed(self, item_name):
        """Verify that an item has been successfully removed from the cart."""
        try:
            item_locator = (By.XPATH, self.item_name_locator.format(item_name=item_name))
            element = self.find_element(*item_locator, step_name=f"Check if item '{item_name}' is still in cart")
            assert element is None, f"Item '{item_name}' is still present in the cart after removal."
            self.logger.info(f"Verified that item '{item_name}' has been removed from the cart.")
        except AssertionError as e:
            self.screenshot_manager.capture_screenshot(f"verify_item_removed_error_{item_name}")
            self.logger.error(f"AssertionError: {str(e)}")
            pytest.fail(f"AssertionError: {str(e)}")

    @allure.step("Get the total price from the cart")
    def get_total_price(self):
        """Retrieve the current total price from the cart."""
        total_price_element = self.find_element(*self.total_price_locator, step_name="Fetch total price from cart")
        return total_price_element.text.replace('₹', '').replace(',', '').strip()

    def get_cart_items(self):
        """Retrieve and verify all items present in the cart."""
        items = self.find_element(self.CART_ITEM, "Cart Items")
        cart_items = []

        for item in items:
            product_name = item.find_element(*self.ITEM_NAME).text
            product_price = self.extract_price(item.find_element(*self.ITEM_PRICE).text)
            cart_items.append(Product(name=product_name, price=product_price, availability=True))
            self.logger.info(f"Found item in cart: {product_name} with price {product_price}")
            allure.attach(self.screenshot_manager.capture_screenshot(f"cart_item_{product_name}"), name=f"Cart item - {product_name}", attachment_type=allure.attachment_type.PNG)

        assert len(cart_items) > 0, "Cart is empty!"
        self.cart.items = cart_items
        return cart_items

    def verify_items_in_cart(self, expected_items):
        """Verify that the expected items are present in the cart."""
        cart_items = self.get_cart_items()
        for expected_item in expected_items:
            assert any(item.name == expected_item.name for item in cart_items), f"{expected_item.name} not found in the cart"
            self.logger.info(f"Verified that {expected_item.name} is present in the cart")
            allure.attach(self.screenshot_manager.capture_screenshot(f"verify_{expected_item.name}_in_cart"), name=f"Verified {expected_item.name} in cart", attachment_type=allure.attachment_type.PNG)

    def remove_item(self, product_name):
        """Remove an item from the cart."""
        cart_items = self.find_element(self.CART_ITEM, "Cart Items")
        for item in cart_items:
            name = item.find_element(*self.ITEM_NAME).text
            if name == product_name:
                self.click_element(item.find_element(*self.REMOVE_BUTTON), f"Remove {product_name}")
                self.logger.info(f"Clicked Remove button for {product_name}")
                allure.attach(self.screenshot_manager.capture_screenshot(f"remove_{product_name}_clicked"), name=f"Remove {product_name} clicked", attachment_type=allure.attachment_type.PNG)
                self.click_element(self.CONFIRM_REMOVE, "Confirm Remove")
                self.logger.info(f"Confirmed removal of {product_name}")
                allure.attach(self.screenshot_manager.capture_screenshot(f"removed_{product_name}_confirmation"), name=f"Removed {product_name} confirmation", attachment_type=allure.attachment_type.PNG)
                self.cart.remove_item(product_name)
                break

    @allure.step("Verify total price of items in the cart")
    def verify_total_price(self):
        """Verify the total price of items in the cart."""
        total_price_element = self.find_element(self.TOTAL_PRICE, "Total Price")
        displayed_total_price = self.extract_price(total_price_element.text)
        calculated_total_price = self.cart.calculate_total_price()

        assert displayed_total_price == calculated_total_price, f"Total price mismatch: expected {calculated_total_price}, but got {displayed_total_price}"
        self.logger.info(f"Verified total price: {calculated_total_price}")
        allure.attach(self.screenshot_manager.capture_screenshot("total_price_verified"), name="Total price verified", attachment_type=allure.attachment_type.PNG)

    @staticmethod
    def extract_price(price_text):
        """Extracts and converts price from string (₹12,345) to integer (12345)."""
        return int(price_text.replace("₹", "").replace(",", ""))