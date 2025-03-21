from .base_page import BasePage
from saucedemo.config.constants import URLs, Credentials
from saucedemo.config.logger import logger
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = "[data-test='error']"
        self.url = URLs.LOGIN
        
    def navigate(self):
        """Navigate to login page"""
        self.page.goto(self.url)
        
    def login(self, username: str, password: str):
        """Login with given credentials"""
        logger.info(f"Logging in with username: {username}")
        self.navigate()
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        # Wait for either error message or successful navigation
        try:
            error = self.page.wait_for_selector(self.error_message, timeout=2000)
            if error:
                return
        except:
            # No error found, wait for navigation
            self.page.wait_for_url(URLs.INVENTORY)
        
    def get_error_message(self) -> str:
        """Get error message text"""
        error_message = self.page.locator(self.error_message).text_content()
        return error_message
        
    def get_current_url(self) -> str:
        """Get the current page URL"""
        return self.page.url 

    def logout(self):
        """Logout the current user"""
        self.click(".bm-burger-button")  
        self.click("#logout_sidebar_link")  
        self.page.wait_for_url(self.url)