from playwright.sync_api import Page, TimeoutError
from config.logger import logger
from typing import Optional

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = 10000  # 10 seconds
        
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
        
    def wait_for_selector(self, selector: str, timeout: int = None) -> bool:
        """Wait for element to be present"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout or self.default_timeout)
            return True
        except TimeoutError:
            logger.warning(f"Element not found: {selector}")
            return False
            
    def get_text(self, selector: str, timeout: int = None) -> Optional[str]:
        """Get text content with better error handling"""
        try:
            if self.wait_for_selector(selector, timeout):
                element = self.page.locator(selector)
                return element.text_content()
            return None
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {str(e)}")
            return None
            
    def get_element_text_safe(self, selector: str, default: str = "") -> str:
        """Safely get element text with default value"""
        text = self.get_text(selector)
        return text if text is not None else default
        
    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible"""
        return self.page.locator(selector).is_visible() 