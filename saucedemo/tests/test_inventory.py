import pytest
from playwright.sync_api import expect
from saucedemo.config.constants import Credentials, URLs, Products
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.inventory_page import InventoryPage
from saucedemo.pages.product_details_page import ProductDetailsPage

@pytest.mark.smoke
@pytest.mark.regression
def test_sort_products_by_price(page):
    """Test sorting products by price low to high"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Sort and verify products
    inventory_page = InventoryPage(page)
    inventory_page.sort_products("Price (low to high)")
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices), "Products are not sorted by price correctly"

@pytest.mark.smoke
def test_cart_management(page):
    """Test adding and removing items from cart via product details"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Manage cart items
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    inventory_page.add_to_cart(Products.ONESIE)
    
    # Remove item through product details
    inventory_page.open_product_details(Products.BACKPACK)
    product_details = ProductDetailsPage(page)
    product_details.remove_from_cart()
 
    # Verify cart count
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

@pytest.mark.smoke
@pytest.mark.regression
def test_product_details(page):
    """Test product details page functionality"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Open product details
    inventory_page = InventoryPage(page)
    inventory_page.open_product_details(Products.BACKPACK)
    
    # Verify product details page
    product_details = ProductDetailsPage(page)
    assert product_details.get_product_name() == Products.BACKPACK, "Wrong product name displayed"
    assert float(product_details.get_product_price().replace("$", "")) > 0, "Invalid product price"
    assert len(product_details.get_product_description()) > 0, "Missing product description"
    
    # Test back to products button
    product_details.back_to_products()
    expect(page).to_have_url(URLs.INVENTORY)

@pytest.mark.negative
def test_problem_user_inventory(page):
    """Test inventory page with problem user - known to have image loading issues"""
    # Login as problem user
    login_page = LoginPage(page)
    login_page.login(Credentials.PROBLEM_USER, Credentials.STANDARD_PASSWORD)
    
    # Verify inventory page loads
    expect(page).to_have_url(URLs.INVENTORY)
    
    # Document known issues with problem user
    inventory_page = InventoryPage(page)
    product_count = inventory_page.get_products_count()
    assert product_count > 0, "No products displayed for problem user"
    
    # Known issue: All product images are the same for problem user
    # This test documents the issue rather than failing
    unique_images = inventory_page.get_unique_product_image_urls()
    if len(unique_images) == 1:
        logger.warning(
            "Known Issue: Problem user sees identical images for all products\n"
            f"Image URL: {unique_images[0]}"
        )

@pytest.mark.smoke
@pytest.mark.negative
def test_direct_inventory_access(page):
    """Test direct access to inventory URL when not logged in.
    
    Note: This test documents a potential security issue in v1 of SauceDemo:
    - Current behavior: Direct access to inventory.html is possible when logged out
    - Expected behavior: Should redirect to login page
    - Impact: Allows unauthorized users to view product inventory
    
    This test will fail to highlight this issue.
    """
    # Attempt direct access to inventory page
    page.goto(URLs.INVENTORY, wait_until="networkidle")
    
    # Document the security issue
    if page.url == URLs.INVENTORY:
        pytest.fail(
            "Security Issue: Direct access to inventory allowed when logged out\n"
            "Current behavior: Page loads normally\n"
            "Expected: Redirect to login page"
        )
