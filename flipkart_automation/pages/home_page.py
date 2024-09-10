import allure
import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Product, Cart
from utils.screenshot import ScreenshotManager
from utils.logger import Logger


class HomePage(BasePage):
    # Locators for elements on the Flipkart page
    search_box = (By.NAME, "q")  # Search box element
    search_button = (By.XPATH, "//button[@type='submit']")  # Search button
    second_item = (By.XPATH, "(//div[@class='_1AtVbE'])[3]")  # Second item in the list (adjust based on ads/structure)
    pin_code_input = (By.XPATH, "//input[@placeholder='Enter Delivery Pincode']")
    check_availability_button = (By.XPATH, "//span[contains(text(),'Check')]")
    add_to_cart_button = (By.XPATH, "//button[contains(text(),'Add to cart')]")
    home_page_icon = (By.XPATH, "//img[@alt='Flipkart']")
    cart_icon = (By.XPATH, "//a[@href='/viewcart?otracker=Cart_Icon_Click']")
    SEARCH_BAR = (By.NAME, "q")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div._1AtVbE")
    HOME_LOGO = (By.CLASS_NAME, "_2xm1JU")

    def __init__(self, driver):
        #super().__init__(poco)
        super().__init__(driver)
        self.screenshot_manager = ScreenshotManager(self.driver)
        self.logger = Logger.get_logger()
        self.cart = Cart()  # Cart object to store cart items


    @allure.step("Add item to cart")
    def add_item_to_cart(self):
        """Add the selected item to the cart."""
        self.click_element(By.XPATH, "//button[contains(text(),'Add to cart')]", step_name="Add item to cart")
        self.logger.info("Item added to the cart.")

    @allure.step("Navigate to cart")
    def navigate_to_cart(self):
        """Navigate to the cart."""
        self.click_element(By.XPATH, "//a[@href='/viewcart?otracker=Cart_Icon_Click']", step_name="Navigate to cart")
        self.logger.info("Navigated to cart.")

    @allure.step("Verify item presence in cart")
    def verify_items_in_cart(self, item_names):
        """Verify if the specified items are in the cart."""
        for item in item_names:
            try:
                item_locator = (By.XPATH, f"//a[contains(text(),'{item}')]")
                element = self.find_element(*item_locator, step_name=f"Verify item '{item}' in cart")
                assert element is not None, f"Item '{item}' not found in the cart."
                self.logger.info(f"Verified item '{item}' is in the cart.")
            except AssertionError as e:
                self.logger.error(f"AssertionError: {str(e)}")
                pytest.fail(f"AssertionError: {str(e)}")

    @allure.step("Verify total price")
    def verify_total_price(self, expected_total):
        """Verify that the total price is correct."""
        try:
            total_price_element = self.find_element(By.XPATH, "//span[contains(@class, '_2-ut7f _1WpvJ7')]",
                                                    step_name="Get total price")
            actual_total = total_price_element.text.replace('₹', '').replace(',', '').strip()
            assert actual_total == str(expected_total), f"Expected total: ₹{expected_total}, but got: ₹{actual_total}"
            self.logger.info(f"Verified total price is ₹{expected_total}.")
        except AssertionError as e:
            self.logger.error(f"AssertionError: {str(e)}")
            pytest.fail(f"AssertionError: {str(e)}")

    def open_flipkart(self):
        """Open Flipkart homepage."""
        self.driver.get("https://www.flipkart.com")
        self.logger.info("Opened Flipkart homepage")
        allure.attach(self.screenshot_manager.capture_screenshot("flipkart_homepage"), name="flipkart_homepage",
                      attachment_type=allure.attachment_type.PNG)

    @allure.step("Search for a product '{product_name}'")
    def search_item(self, search_term):
        """Search for an item in the search bar."""
        self.enter_text(self.SEARCH_BAR, search_term, "Search Bar")
        self.logger.info(f"Searched for '{search_term}'")
        allure.attach(self.screenshot_manager.capture_screenshot(f"searched_{search_term}"),
                      name=f"Searched_{search_term}", attachment_type=allure.attachment_type.PNG)

    @allure.step("Select second item from search results")
    def select_second_item(self):
        """Select the second item from search results."""
        results = self.wait_for_element(self.SEARCH_RESULTS)
        second_item = results[1]  # Assuming second item is at index 1
        product_name = second_item.text.split("\n")[0]
        second_item.click()
        self.logger.info(f"Selected the second item: {product_name}")
        allure.attach(self.screenshot_manager.capture_screenshot(f"selected_{product_name}"),
                      name=f"selected_{product_name}", attachment_type=allure.attachment_type.PNG)
        return product_name

    @allure.step("Check item availability for pincode '{pincode}'")
    def check_item_availability(self, pincode, product_name):
        """Check the availability of the selected item by entering a pin code."""
        pincode_field = (By.CSS_SELECTOR, "input[placeholder='Enter Delivery Pincode']")
        check_pincode_btn = (By.CSS_SELECTOR, "span[tabindex='0']")

        self.enter_text(pincode_field, pincode, "Pincode Field")
        self.click(check_pincode_btn, "Check Pincode Button")

        #availability_msg = "In Stock"  # an element shows "In Stock" message
        self.logger.info(f"Checked availability of {product_name} with pincode {pincode}")
        allure.attach(self.screenshot_manager.capture_screenshot(f"availability_{product_name}"),
                      name=f"availability_{product_name}", attachment_type=allure.attachment_type.PNG)

        return Product(name=product_name, availability=True)  # the item is available

    def add_to_cart(self, product):
        """Add the selected item to the cart."""
        add_to_cart_btn = (By.CSS_SELECTOR, "button._2KpZ6l._2U9uOA._3v1-ww")

        self.click(add_to_cart_btn, "Add to Cart Button")
        self.cart.add_item(product)
        self.logger.info(f"Added {product.name} to the cart")
        allure.attach(self.screenshot_manager.capture_screenshot(f"added_{product.name}_to_cart"),
                      name=f"added_{product.name}_to_cart", attachment_type=allure.attachment_type.PNG)

    @allure.step("Return to home page")
    def return_to_home_page(self):
        """Navigate back to the home page."""
        self.click(self.HOME_LOGO, "Home Logo")
        self.logger.info("Returned to Flipkart homepage")
        allure.attach(self.screenshot_manager.capture_screenshot("flipkart_homepage_return"),
                      name="flipkart_homepage_return", attachment_type=allure.attachment_type.PNG)

    def verify_cart_items(self):
        """Verify that all items are present in the cart."""
        total_items = len(self.cart.items)
        assert total_items > 0, "Cart is empty!"
        self.logger.info(f"Verified that there are {total_items} items in the cart")
        allure.attach(self.screenshot_manager.capture_screenshot("cart_items_verified"), name="cart_items_verified",
                      attachment_type=allure.attachment_type.PNG)

        # Also verify the total price calculation
        total_price = self.cart.calculate_total_price()
        self.logger.info(f"Total price of items in the cart: {total_price}")
        allure.attach(self.screenshot_manager.capture_screenshot("total_price_verified"), name="total_price_verified",
                      attachment_type=allure.attachment_type.PNG)

    @allure.step("Remove item from cart")
    def remove_item_from_cart(self, product_name):
        """Remove an item from the cart by name."""
        try:
            remove_item_btn = (By.CSS_SELECTOR, "div._3dsJAO")
            self.click(remove_item_btn, f"Remove {product_name}")
            self.cart.remove_item(product_name)
            self.logger.info(f"Removed {product_name} from the cart")
            allure.attach(self.screenshot_manager.capture_screenshot(f"removed_{product_name}"),
                      name=f"removed_{product_name}", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            self.logger.error(f"Error removing item '{product_name}' from cart: {str(e)}")
            pytest.fail(f"Error removing item '{product_name}' from cart: {str(e)}")
            allure.attach(self.screenshot_manager.capture_screenshot(f"error_removing_{product_name}"),
                      name=f"error_removing_{product_name}", attachment_type=allure.attachment_type.PNG)
