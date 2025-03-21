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
    """Test checkout validation when first name is missing"""
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
    
    # Fill shipping details with missing first name
    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_details(
        first_name="",
        last_name=TestData.SHIPPING['last_name'],
        postal_code=TestData.SHIPPING['postal_code']
    )
    checkout_page.continue_checkout()
    
    # Verify error message
    error_message = checkout_page.get_error_message()
    assert error_message == "Error: First Name is required"

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
    """Test checkout validation when cart is empty.
    
    Note: This test documents a potential security/UX issue in v1 of SauceDemo:
    - Current behavior: Checkout is allowed with empty cart, no validation
    - Expected behavior: Should show error message or disable checkout button
    - Impact: Users can proceed through checkout flow with no items
    
    This test will fail to highlight this issue.
    """
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Go directly to cart page
    inventory_page = InventoryPage(page)
    inventory_page.open_cart()
    
    # Verify cart is empty
    assert inventory_page.get_cart_count() == 0, "Cart should be empty"
    
    # Document the issue: Checkout is possible with empty cart
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout()
    
    # Fill shipping details
    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_details(
        first_name="John",
        last_name="Doe",
        postal_code="12345"
    )
    
    # Can continue checkout despite empty cart
    checkout_page.continue_checkout()
    
    # Can even finish checkout with empty cart
    checkout_page.finish_checkout()
    
    # Test fails here to highlight the issue
    pytest.fail(
        "Security/UX Issue: Checkout allowed with empty cart\n"
        "Current behavior: No validation, full checkout possible\n"
        "Expected: Error message or disabled checkout button"
    )


