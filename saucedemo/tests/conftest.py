import pytest
import os
from playwright.sync_api import sync_playwright
from saucedemo.config.settings import get_settings
from saucedemo.config.logger import logger

settings = get_settings()

def pytest_addoption(parser):
    """Add command-line options to pytest"""
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to run tests: chromium, firefox, or webkit"
    )

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Fixture to configure browser launch arguments"""
    return {
        "headless": os.getenv('HEADLESS', 'true').lower() == 'true',
        "args": ['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'],
        "timeout": int(os.getenv('PLAYWRIGHT_TIMEOUT', '30000'))
    }

@pytest.fixture(scope="session")
def browser_type(request):
    """Get the browser type from command line option"""
    return request.config.getoption("--browser-type")

@pytest.fixture(scope="session")
def browser(playwright, browser_type, browser_type_launch_args):
    """Create a browser instance"""
    try:
        browser_instance = getattr(playwright, browser_type)
        browser = browser_instance.launch(**browser_type_launch_args)
        yield browser
        browser.close()
    except Exception as e:
        logger.error(f"Failed to launch browser: {str(e)}")
        raise

@pytest.fixture
def context(browser):
    """Create a new browser context"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()

@pytest.fixture
def page(context):
    """Create a new page for each test"""
    page = context.new_page()
    page.set_default_timeout(30000)  # Set default timeout to 30 seconds
    yield page
    page.close()

def pytest_configure(config):
    """Add custom markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "negative: mark test as negative test") 