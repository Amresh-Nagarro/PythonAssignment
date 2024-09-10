# pages/__init__.py

# Import all the relevant page objects and utility classes

from .base_page import BasePage, Product, Cart  # Importing BasePage and POCO classes from base_page
from .home_page import HomePage  # Importing HomePage class
from .cart_page import CartPage  # Importing CartPage class
from .product_page import ProductPage  # Importing ProductPage class

__all__ = [
    "BasePage",
    "Product",
    "Cart",
    "HomePage",
    "CartPage",
    "ProductPage"
]

