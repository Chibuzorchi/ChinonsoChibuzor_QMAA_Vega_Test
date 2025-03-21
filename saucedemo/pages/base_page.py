from playwright.sync_api import Page
from config.logger import logger
from typing import Optional

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
    def navigate_to(self, url: str):
        """Navigate to the specified URL"""
        logger.info(f"Navigating to {url}")
        self.page.goto(url)
        
    def click(self, selector: str, timeout: int = 5000):
        """Click an element with logging and error handling"""
        try:
            logger.info(f"Clicking element: {selector}")
            self.page.click(selector, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {str(e)}")
            raise
        
    def fill(self, selector: str, value: str, timeout: int = 5000):
        """Fill a form field with logging and error handling"""
        try:
            logger.info(f"Filling {selector} with value: {value}")
            self.page.fill(selector, value, timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to fill {selector}: {str(e)}")
            raise
        
    def get_text(self, selector: str, timeout: int = 5000) -> Optional[str]:
        """Get text content with logging and error handling"""
        try:
            element = self.page.locator(selector)
            return element.text_content(timeout=timeout)
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {str(e)}")
            return None
        
    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible"""
        return self.page.locator(selector).is_visible() 