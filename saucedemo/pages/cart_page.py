from .base_page import BasePage
from saucedemo.config.logger import logger
from saucedemo.config.constants import URLs
from playwright.sync_api import Page

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_button = "a.checkout_button"
        self.cart_badge = ".shopping_cart_badge"
        self.remove_button = lambda item: f"//div[text()='{item}']/ancestor::div[@class='cart_item']//button[text()='REMOVE']"
        self.cart_items = ".cart_item"
        self.item_price = ".inventory_item_price"
        self.url = URLs.CART
        
    def navigate(self):
        """Navigate to cart page"""
        self.page.goto(self.url)
        
    def proceed_to_checkout(self):
        """Click the checkout button"""
        logger.info("Proceeding to checkout")
        # Document the security issue: Checkout is possible with empty cart
        # This should be fixed in future versions
        if self.get_cart_count() == 0:
            logger.warning("Security/UX Issue: Proceeding to checkout with empty cart")
        self.click(self.checkout_button)
        # Wait for navigation to checkout page
        self.page.wait_for_url(URLs.CHECKOUT_STEP_ONE)
        
    def get_cart_count(self) -> int:
        """Get number of items in cart with better error handling"""
        badge_text = self.get_element_text_safe(".shopping_cart_badge", "0")
        try:
            return int(badge_text)
        except ValueError:
            logger.warning(f"Invalid cart count value: {badge_text}")
            return 0
            
    def remove_item(self, item_name: str):
        """Remove an item from the cart"""
        logger.info(f"Removing {item_name} from cart")
        remove_button = self.page.locator(self.remove_button(item_name))
        if remove_button.count() == 0:
            raise ValueError(f"Item '{item_name}' not found in cart")
        
        # Get current cart count
        initial_count = self.get_cart_count()
        
        # Click remove and wait for cart count to update
        remove_button.click()
        self.page.wait_for_function(
            f"count => document.querySelector('.shopping_cart_badge')?.textContent === '{initial_count - 1}'"
        )
        
    def get_cart_total(self) -> float:
        """Calculate total price of items in cart"""
        prices = self.page.locator(self.item_price).all()
        total = sum(float(price.text_content().replace('$', '')) for price in prices)
        logger.info(f"Cart total: ${total}")
        return total
        
    def is_checkout_enabled(self) -> bool:
        """Check if checkout button is enabled"""
        checkout_button = self.page.locator(self.checkout_button)
        return checkout_button.is_enabled() if checkout_button.count() > 0 else False
