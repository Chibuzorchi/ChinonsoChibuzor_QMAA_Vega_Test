from .base_page import BasePage
from saucedemo.config.logger import logger

class ProductDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.remove_button = "button.btn_secondary"
        self.back_button = "button.inventory_details_back_button"
        self.backpack_image = "#item_4_img_link img"
        self.product_name = ".inventory_details_name"
        self.product_price = ".inventory_details_price"
        self.product_description = ".inventory_details_desc"
        
        
    def remove_from_cart(self):
        """Remove product from cart"""
        logger.info("Removing product from cart")
        self.click(self.remove_button)
        
    def return_to_inventory(self):
        """Return to inventory page"""
        logger.info("Returning to inventory page")
        self.click(self.back_button) 

    def click_backpack_image(self):
        """Click on the backpack image"""
        logger.info("Clicking on backpack image")
        self.click(self.backpack_image)
        
    def get_product_name(self) -> str:
        """Get the product name from details page"""
        return self.page.locator(self.product_name).text_content()
        
    def get_product_price(self) -> str:
        """Get the product price from details page"""
        return self.page.locator(self.product_price).text_content()
        
    def get_product_description(self) -> str:
        """Get the product description from details page"""
        return self.page.locator(self.product_description).text_content()
        
    def back_to_products(self):
        """Click back to products button"""
        logger.info("Navigating back to products")
        self.click(self.back_button)