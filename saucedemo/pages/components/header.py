from saucedemo.pages.base_page import BasePage
from saucedemo.config.logger import logger

class Header(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.menu_button = ".bm-burger-button"
        self.logout_link = "#logout_sidebar_link"
        
    def open_menu(self):
        """Open the side menu"""
        logger.info("Opening side menu")
        self.click(self.menu_button)
        
    def logout(self):
        """Click the logout link"""
        logger.info("Clicking logout")
        self.click(self.logout_link)
