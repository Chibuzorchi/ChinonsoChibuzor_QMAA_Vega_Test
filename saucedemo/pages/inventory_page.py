from .base_page import BasePage
from saucedemo.config.logger import logger
from playwright.sync_api import Page
from saucedemo.config.constants import URLs

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sort_dropdown = ".product_sort_container"
        self.product_prices = ".inventory_item_price"
        self.cart_badge = ".shopping_cart_badge"
        self.url = URLs.INVENTORY
        self.inventory_items = ".inventory_item"
        self.product_images = ".inventory_item img"
        self.add_to_cart_button = lambda item: f"//div[text()='{item}']/ancestor::div[@class='inventory_item']//button[text()='ADD TO CART']"
        self.remove_button = lambda item: f"//div[text()='{item}']/ancestor::div[@class='inventory_item']//button[text()='REMOVE']"
        
    def navigate(self):
        """Navigate to inventory page"""
        self.page.goto(self.url)
        
    def sort_products(self, option: str):
        """Sort products using the dropdown"""
        logger.info(f"Sorting products by: {option}")
        value_map = {
            "Price (low to high)": "lohi",
            "Price (high to low)": "hilo",
            "Name (A to Z)": "az",
            "Name (Z to A)": "za"
        }
        self.page.select_option(self.sort_dropdown, value_map[option])
        
    def get_product_prices(self) -> list[float]:
        """Get list of product prices"""
        prices = self.page.locator(self.product_prices).all()
        return [float(price.text_content().replace('$', '')) for price in prices]
        
    def add_to_cart(self, item_name: str):
        """Add an item to cart by its name"""
        logger.info(f"Adding product to cart: {item_name}")
        self.click(self.add_to_cart_button(item_name))
        
    def open_product_details(self, product_name: str):
        """Click on product image to open details"""
        logger.info(f"Opening details for product: {product_name}")
        self.page.locator(f".inventory_item:has-text('{product_name}') img").click()
        
    def get_cart_count(self) -> int:
        """Get the number of items in cart"""
        cart_badge = self.page.locator(self.cart_badge)
        if cart_badge.count() > 0:
            return int(cart_badge.text_content())
        return 0
        
    def open_cart(self):
        """Open the shopping cart"""
        logger.info("Opening shopping cart")
        self.page.click(".shopping_cart_link")
        # Wait for navigation to cart page
        self.page.wait_for_url(URLs.CART)
        
    def remove_from_cart(self, item_name: str):
        """Remove an item from cart while on inventory page"""
        logger.info(f"Removing product from cart: {item_name}")
        self.click(self.remove_button(item_name))
        
    def is_item_in_cart(self, item_name: str) -> bool:
        """Check if item is in cart by verifying REMOVE button exists"""
        remove_button = self.page.locator(self.remove_button(item_name))
        return remove_button.count() > 0
        
    def get_products_count(self) -> int:
        """Get the total number of products displayed on the page"""
        return self.page.locator(self.inventory_items).count()
        
    def get_unique_product_image_urls(self) -> list[str]:
        """Get list of unique product image URLs to check for image loading issues"""
        logger.info("Getting unique product image URLs")
        images = self.page.locator(self.product_images).all()
        urls = [img.get_attribute('src') for img in images]
        return list(set(urls))