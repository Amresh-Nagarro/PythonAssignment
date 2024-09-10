"""
This is the root package for the Flipkart Automation framework.
The root folder is marked as 'Sources root' to ensure proper absolute imports.
"""

# You can define global imports, constants, or configurations here if required.
# For example, global logging configuration or environment setup can be done here.

# Importing necessary modules to make them available at package-level
from utils.browser_manager import BrowserManager
from utils.screenshot import ScreenshotManager
from utils.logger import Logger
from pages.base_page import BasePage, Product, Cart
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# Constants or environment-specific settings can be defined here
FRAMEWORK_VERSION = "1.0.0"

__all__ = [
    "BasePage",
    "Product",
    "Cart",
    "HomePage",
    "CartPage",
    "ProductPage",
    "BrowserManager",
    "Logger",
    "ScreenshotManager"
]
