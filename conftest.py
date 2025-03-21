import os
import pytest
import allure
from playwright.sync_api import sync_playwright
from saucedemo.config.logger import logger
from saucedemo.config.settings import get_settings

settings = get_settings()

@pytest.fixture(scope="session")
def playwright():
    """Create a Playwright instance"""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright):
    """Create a browser instance"""
    browser = playwright.chromium.launch(
        headless=os.getenv('HEADLESS', 'false').lower() == 'true',
        args=['--disable-gpu']
    )
    yield browser
    browser.close()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot capture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="function")
def context(browser):
    """Create a browser context"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context, request):
    """Create a new page for each test with screenshot capture on failure"""
    page = context.new_page()
    
    # Add listeners for console logs
    page.on("console", lambda msg: logger.info(f"Browser console: {msg.text}"))
    
    yield page
    
    # Capture screenshot on test failure
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(
            screenshot_dir,
            f"{request.node.name}.png"
        )
        page.screenshot(path=screenshot_path)
        allure.attach.file(
            screenshot_path,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    
    page.close()