import pytest
from saucedemo.config.constants import Credentials, Products, URLs, TestData
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.inventory_page import InventoryPage
from saucedemo.pages.cart_page import CartPage
from saucedemo.pages.checkout_page import CheckoutPage
from playwright.sync_api import expect

@pytest.mark.smoke
def test_successful_checkout(page):
    """Test complete checkout process with valid shipping details"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add item to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    
    # Navigate to cart and checkout
    inventory_page.open_cart()
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout()
    
    # Fill shipping details and complete checkout
    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_details(**TestData.SHIPPING)
    checkout_page.continue_checkout()
    checkout_page.finish_checkout()
    
    # Verify confirmation message
    confirmation_message = checkout_page.get_confirmation_message()
    expect(checkout_page.get_confirmation_message()).to_have_text("THANK YOU FOR YOUR ORDER")

@pytest.mark.negative
def test_checkout_missing_first_name(page):
    """Test checkout with missing first name"""
    login_page = LoginPage(page)
    checkout_page = CheckoutPage(page)
    
    # Login and go to checkout
    page.goto(URLs.LOGIN)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    page.goto(URLs.CHECKOUT)
    
    # Try to checkout without first name
    checkout_page.fill_checkout_info("", "Doe", "12345")
    checkout_page.continue_checkout()
    
    # Verify error message
    error = checkout_page.get_error_message()
    assert error and "first name is required" in error.lower(), "Should show first name required error"

@pytest.mark.negative
def test_checkout_missing_last_name(page):
    """Test checkout validation when last name is missing"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add item to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    
    # Navigate to cart and checkout
    inventory_page.open_cart()
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout()
    
    # Fill shipping details with missing last name
    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_details(
        first_name=TestData.SHIPPING['first_name'],
        last_name="",
        postal_code=TestData.SHIPPING['postal_code']
    )
    checkout_page.continue_checkout()
    
    # Verify error message
    error_message = checkout_page.get_error_message()
    assert error_message == "Error: Last Name is required"

@pytest.mark.negative
def test_checkout_missing_postal_code(page):
    """Test checkout validation when postal code is missing"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add item to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    
    # Navigate to cart and checkout
    inventory_page.open_cart()
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout()
    
    # Fill shipping details with missing postal code
    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_details(
        first_name=TestData.SHIPPING['first_name'],
        last_name=TestData.SHIPPING['last_name'],
        postal_code=""
    )
    checkout_page.continue_checkout()
    
    # Verify error message
    error_message = checkout_page.get_error_message()
    assert error_message == "Error: Postal Code is required"

@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.regression
def test_checkout_empty_cart(page):
    """Test checkout with empty cart.
    
    Note: This test documents a security/UX issue in SauceDemo:
    - Current behavior: Checkout process can be completed with empty cart
    - Expected behavior: Should show error or disable checkout
    - Impact: Poor UX, allows meaningless checkout completion
    
    This test will fail to highlight this issue.
    """
    login_page = LoginPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    
    # Login and verify cart is empty
    page.goto(URLs.LOGIN)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    assert cart_page.get_cart_count() == 0, "Cart should be empty"
    
    # Attempt checkout with empty cart
    page.goto(URLs.CHECKOUT)
    
    # Document the security/UX issue
    if page.url == URLs.CHECKOUT_STEP_ONE:
        pytest.fail(
            "Security/UX Issue: Checkout allowed with empty cart\n"
            "Current behavior: Can proceed to checkout\n"
            "Expected: Error message or disabled checkout button"
        )


