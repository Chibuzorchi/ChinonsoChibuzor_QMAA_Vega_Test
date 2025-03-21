import pytest
import allure
from playwright.sync_api import sync_playwright
from saucedemo.config.logger import logger
from saucedemo.config.settings import get_settings

settings = get_settings()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot capture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Configure browser launch arguments"""
    return {
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLOWMO,
    }

@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context"""
    return {
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True,
        "timeout": settings.TIMEOUT,
    }

@pytest.fixture(scope="function")
def page(request, browser):
    """Create a new page for each test with screenshot capture on failure"""
    page = browser.new_page()
    
    # Add listeners for console logs
    page.on("console", lambda msg: logger.info(f"Browser console: {msg.text}"))
    
    yield page
    
    # Capture screenshot on test failure
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        allure.attach(
            page.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    
    page.close()