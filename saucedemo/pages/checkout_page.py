from .base_page import BasePage
from saucedemo.config.logger import logger
from saucedemo.config.constants import URLs
from playwright.sync_api import Page

class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = "input[data-test='firstName']"
        self.last_name_input = "input[data-test='lastName']"
        self.postal_code_input = "input[data-test='postalCode']"
        self.continue_button = "input.cart_button"
        self.finish_button = "a.cart_button"
        self.confirmation_message = "h2.complete-header"
        self.error_message = "h3[data-test='error']"
        
    def fill_shipping_details(self, first_name: str, last_name: str, postal_code: str):
        """Fill in shipping information"""
        logger.info(f"Filling shipping details for {first_name} {last_name}")
        self.fill(self.first_name_input, first_name)
        self.fill(self.last_name_input, last_name)
        self.fill(self.postal_code_input, postal_code)
        
    def continue_checkout(self):
        """Click continue button"""
        logger.info("Continuing checkout process")
        self.click(self.continue_button)
        # Only wait for navigation if there's no error
        if not self.get_error_message():
            self.page.wait_for_url(URLs.CHECKOUT_STEP_TWO)
        
    def finish_checkout(self):
        """Click finish button"""
        logger.info("Finishing checkout process")
        self.click(self.finish_button)
        self.page.wait_for_url(URLs.CHECKOUT_COMPLETE)
        
    def get_confirmation_message(self):
        return self.page.locator(".complete-header") 
        
    def get_error_message(self) -> str:
        """Get the error message text"""
        return self.get_text(self.error_message)
