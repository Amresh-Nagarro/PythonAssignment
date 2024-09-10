import pytest
import allure
from ..pages.home_page import HomePage
from ..pages.cart_page import CartPage
from ..pages.product_page import ProductPage
from ..utils.logger import Logger
from ..utils.screenshot import ScreenshotManager

@pytest.mark.usefixtures("browser")
class TestOrderItems:

    #@pytest.fixture(autouse=True)
    def __init__(self, browser):
        """Setup for each test."""
        self.driver = browser
        self.logger = Logger(name="TestLogger")
        self.screenshot_manager = ScreenshotManager(self.driver)
        self.home_page = HomePage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.product_page = ProductPage(self.driver)

    @allure.title("Order Samsung S24 128 GB and Bajaj Iron Majesty")
    @allure.description("Test to order Samsung S24 128 GB and Bajaj Iron Majesty and verify cart")
    def test_order_items(self):
        """Main test method that calls smaller methods corresponding to feature steps."""
        try:
            # Step 1: Open Flipkart
            self.open_flipkart_home_page()

            # Step 2: Search for Samsung S24 and select the second item
            self.search_and_select_samsung_s24()

            # Step 3: Check availability and add Samsung to the cart
            self.check_availability_and_add_samsung_to_cart()

            # Step 4: Return to the home page
            self.return_to_home_page()

            # Step 5: Search for Bajaj Iron and select the second item
            self.search_and_select_bajaj_iron()

            # Step 6: Check availability and add Bajaj Iron to the cart
            self.check_availability_and_add_bajaj_to_cart()

            # Step 7: Navigate to the cart
            self.navigate_to_cart()

            # Step 8: Verify the cart items and total price
            self.verify_cart_items_and_total_price()

            # Step 9: Remove one item and verify the updated total price
            self.remove_item_and_verify_price()

        except AssertionError as e:
            self.screenshot_manager.capture_screenshot("test_order_items_failure")
            self.logger.log_error(f"Assertion error: {str(e)}")
            raise e

        except Exception as e:
            self.screenshot_manager.capture_screenshot("test_order_items_failure")
            self.logger.log_error(f"Unexpected error: {str(e)}")
            raise e

    # Step 1: Open Flipkart
    def open_flipkart_home_page(self):
        self.home_page.open_flipkart()
        self.logger.log_info("Opened Flipkart home page")
        self.screenshot_manager.capture_screenshot("home_page_opened")

    # Step 2: Search for Samsung S24 128 GB and select the second item
    def search_and_select_samsung_s24(self):
        self.home_page.search_item("Samsung S24 128 GB")
        self.home_page.select_second_item()
        self.logger.log_info("Selected the second item for Samsung S24 128 GB")
        self.screenshot_manager.capture_screenshot("second_item_selected_samsung")

    # Step 3: Check availability and add Samsung to the cart
    def check_availability_and_add_samsung_to_cart(self):
        self.product_page.check_availability("122017")
        self.product_page.add_product_to_cart()
        self.logger.log_info("Checked availability and added Samsung S24 128 GB to cart")
        self.screenshot_manager.capture_screenshot("samsung_added_to_cart")

    # Step 4: Return to the home page
    def return_to_home_page(self):
        self.home_page.return_to_home_page()
        self.logger.log_info("Returned to Flipkart home page")
        self.screenshot_manager.capture_screenshot("returned_to_home_page")

    # Step 5: Search for Bajaj Iron and select the second item
    def search_and_select_bajaj_iron(self):
        self.home_page.search_item("bajaj iron majesty")
        self.home_page.select_second_item()
        self.logger.log_info("Selected the second item for Bajaj Iron Majesty")
        self.screenshot_manager.capture_screenshot("second_item_selected_bajaj")

    # Step 6: Check availability and add Bajaj Iron to the cart
    def check_availability_and_add_bajaj_to_cart(self):
        self.product_page.check_availability("122017")
        self.product_page.add_product_to_cart()
        self.logger.log_info("Checked availability and added Bajaj Iron Majesty to cart")
        self.screenshot_manager.capture_screenshot("bajaj_added_to_cart")

    # Step 7: Navigate to the cart
    def navigate_to_cart(self):
        self.home_page.navigate_to_cart()
        self.logger.log_info("Navigated to the cart")
        self.screenshot_manager.capture_screenshot("navigated_to_cart")

    # Step 8: Verify both items and total price
    def verify_cart_items_and_total_price(self):
        assert self.cart_page.verify_items_in_cart(["Samsung S24 128 GB", "Bajaj Iron Majesty"]), "Items not found in cart"
        assert self.cart_page.verify_total_price(), "Total price is incorrect"
        self.logger.log_info("Verified both items in the cart and the total price")
        self.screenshot_manager.capture_screenshot("items_in_cart_verified")

    # Step 9: Remove one item and verify price update
    def remove_item_and_verify_price(self):
        self.cart_page.remove_item_from_cart("Samsung S24 128 GB")
        assert self.cart_page.verify_total_price("Bajaj Iron Majesty"), "Total price did not update correctly"
        self.logger.log_info("Removed Samsung S24 128 GB from the cart and verified updated total price")
        self.screenshot_manager.capture_screenshot("item_removed_total_price_updated")
