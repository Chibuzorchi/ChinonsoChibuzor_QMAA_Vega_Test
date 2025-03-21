import pytest
import os
from playwright.sync_api import sync_playwright
from saucedemo.config.settings import get_settings
from saucedemo.config.logger import logger

settings = get_settings()

def pytest_addoption(parser):
    parser.addoption("--browser", 
                    action="store",
                    default="chromium",
                    help="Browser to run tests: chromium, firefox, or webkit")

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Fixture to configure browser launch arguments"""
    return {
        "headless": os.getenv('HEADLESS', 'true').lower() == 'true',
        "args": ['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'],
        "timeout": 30000,
    }

@pytest.fixture(scope="session")
def browser(playwright):
    """Create a browser instance"""
    try:
        browser_name = os.getenv('BROWSER', 'chromium').lower()
        browser_type = getattr(playwright, browser_name)
        
        browser = browser_type.launch(**browser_type_launch_args())
        yield browser
        browser.close()
    except Exception as e:
        logger.error(f"Failed to launch browser: {str(e)}")
        raise

@pytest.fixture
def page(browser):
    """Create a new page for each test"""
    page = browser.new_page()
    yield page
    page.close() 