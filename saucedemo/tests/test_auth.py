import pytest
from saucedemo.config.constants import Credentials, URLs
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.components.header import Header
from saucedemo.pages.inventory_page import InventoryPage
from playwright.sync_api import expect

@pytest.mark.smoke
def test_successful_login(page):
    """Test successful login with standard user"""
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    expect(page).to_have_url(URLs.INVENTORY)

@pytest.mark.smoke
@pytest.mark.negative
def test_locked_out_user(page):
    """Test locked out user login attempt"""
    login_page = LoginPage(page)
    page.goto(URLs.LOGIN)
    
    # Try to login with locked out user
    login_page.login(Credentials.LOCKED_OUT_USER, Credentials.LOCKED_OUT_PASSWORD)
    
    # Verify error message
    error_message = login_page.get_error_message()
    assert "locked out" in error_message.lower(), "Expected locked out error message"

@pytest.mark.smoke
def test_problem_user(page):
    """Test problem user can login but may have restricted functionality"""
    login_page = LoginPage(page)
    login_page.login(Credentials.PROBLEM_USER, Credentials.PROBLEM_PASSWORD)
    expect(page).to_have_url(URLs.INVENTORY)

@pytest.mark.negative
def test_invalid_credentials(page):
    """Test login with invalid credentials"""
    login_page = LoginPage(page)
    page.goto(URLs.LOGIN)
    
    # Try to login with invalid credentials
    login_page.login("invalid_user", "invalid_password")
    
    # Verify error message
    error_message = login_page.get_error_message()
    assert "username and password do not match" in error_message.lower()

@pytest.mark.negative
def test_empty_credentials(page):
    """Test login with empty credentials"""
    login_page = LoginPage(page)
    page.goto(URLs.LOGIN)
    
    # Try to login with empty credentials
    login_page.login("", "")
    
    # Verify error message
    error_message = login_page.get_error_message()
    assert "username is required" in error_message.lower()

@pytest.mark.smoke
@pytest.mark.regression
def test_logout_and_session_termination(page):
    """Test logout functionality and session invalidation.
    
    Note: This test documents a security vulnerability in v1 of SauceDemo:
    - Current behavior: Direct access to /inventory.html is possible when logged out
    - Expected behavior: Should redirect to login page or show error
    - Impact: Allows unauthorized access to inventory
    
    This test will need to be updated once the security issue is fixed.
    """
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Verify successful login
    expect(page).to_have_url(URLs.INVENTORY)
    
    # Logout via menu
    header = Header(page)
    header.open_menu()
    header.logout()
    
    # Verify redirection to login page
    expect(page).to_have_url(URLs.LOGIN)
    
    # Document security vulnerability: Direct access to inventory when logged out
    page.goto(URLs.INVENTORY, wait_until="networkidle")
    expect(page).to_have_url(URLs.INVENTORY)

@pytest.mark.regression
def test_session_persistence(page):
    """Test that session persists after page refresh"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Verify successful login
    expect(page).to_have_url(URLs.INVENTORY)
    
    # Refresh page
    page.reload()
    
    # Verify still logged in
    expect(page).to_have_url(URLs.INVENTORY)
    
    # Verify can still interact with inventory
    inventory_page = InventoryPage(page)
    assert inventory_page.get_products_count() > 0
