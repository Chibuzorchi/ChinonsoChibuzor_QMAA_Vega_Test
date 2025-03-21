import pytest
from saucedemo.config.constants import Credentials, Products, URLs
from saucedemo.pages.login_page import LoginPage
from saucedemo.pages.inventory_page import InventoryPage
from saucedemo.pages.cart_page import CartPage
from playwright.sync_api import expect

@pytest.mark.smoke
@pytest.mark.regression
def test_cart_management(page):
    """Test adding multiple items to cart and updating quantities"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add multiple items to cart
    inventory_page = InventoryPage(page)
    test_items = [Products.BACKPACK, Products.BIKE_LIGHT, Products.ONESIE]
    
    for item in test_items:
        inventory_page.add_to_cart(item)
        # Verify cart count increases
        expected_count = test_items.index(item) + 1
        actual_count = inventory_page.get_cart_count()
        assert actual_count == expected_count, f"Cart count should be {expected_count}, but was {actual_count}"
    
    # Open cart and verify items
    inventory_page.open_cart()
    cart_page = CartPage(page)
    actual_count = cart_page.get_cart_count()
    assert actual_count == len(test_items), f"Cart count should be {len(test_items)}, but was {actual_count}"
    
    # Get initial cart total
    initial_total = cart_page.get_cart_total()
    
    # Remove one item
    cart_page.remove_item(Products.BIKE_LIGHT)
    
    # Verify updated cart count
    actual_count = cart_page.get_cart_count()
    expected_count = len(test_items) - 1
    assert actual_count == expected_count, f"Cart count after removal should be {expected_count}, but was {actual_count}"
    
    # Verify new total is less than initial total
    new_total = cart_page.get_cart_total()
    assert new_total < initial_total, f"Cart total should decrease after removing item. Was: ${initial_total}, Now: ${new_total}"

@pytest.mark.negative
def test_remove_nonexistent_item(page):
    """Test attempting to remove an item that doesn't exist in cart"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Go directly to cart page
    cart_page = CartPage(page)
    cart_page.navigate()
    
    # Verify cart is empty
    cart_count = cart_page.get_cart_count()
    assert cart_count == 0, f"Expected empty cart but found {cart_count} items"
    
    # Attempt to remove non-existent item
    with pytest.raises(ValueError, match=f"Item '{Products.BACKPACK}' not found in cart"):
        cart_page.remove_item(Products.BACKPACK)

@pytest.mark.regression
def test_add_duplicate_item(page):
    """Test attempting to add the same item multiple times"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add same item twice
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    initial_count = inventory_page.get_cart_count()
    
    # Verify the button has changed to REMOVE
    assert inventory_page.is_item_in_cart(Products.BACKPACK), "Add to cart button should change to REMOVE after adding item"
    
    final_count = inventory_page.get_cart_count()
    assert final_count == initial_count, f"Cart count should remain {initial_count}, but was {final_count}"

@pytest.mark.smoke
def test_remove_item_from_inventory(page):
    """Test removing item from cart while on inventory page"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add item to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    assert inventory_page.get_cart_count() == 1, "Item should be added to cart"
    
    # Remove item from inventory page
    inventory_page.remove_from_cart(Products.BACKPACK)
    
    # Verify cart is empty
    assert inventory_page.get_cart_count() == 0, "Cart should be empty after removing item"

@pytest.mark.regression
def test_cart_persistence_after_logout(page):
    """Test that cart persists after logout in v1 of SauceDemo"""
    # Login
    login_page = LoginPage(page)
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Add items to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart(Products.BACKPACK)
    inventory_page.add_to_cart(Products.BIKE_LIGHT)
    initial_count = inventory_page.get_cart_count()
    assert initial_count == 2, "Two items should be in cart"
    
    # Logout
    login_page.logout()
    
    # Login again
    login_page.login(Credentials.STANDARD_USER, Credentials.STANDARD_PASSWORD)
    
    # Verify cart items persist 
    final_count = inventory_page.get_cart_count()
    assert final_count == initial_count, f"Cart should persist after logout with {initial_count} items, but found {final_count} items"

@pytest.mark.smoke
@pytest.mark.negative
def test_locked_out_user_cart(page):
    """Test cart functionality with locked out user"""
    login_page = LoginPage(page)
    login_page.login(Credentials.LOCKED_OUT_USER, Credentials.STANDARD_PASSWORD)
    
    # Verify error message
    error_message = login_page.get_error_message()
    assert "Epic sadface: Sorry, this user has been locked out" in error_message
    
    # Verify user remains on login page
    current_url = login_page.get_current_url()
    assert current_url == f"{URLs.BASE_URL}/index.html", "Locked out user should remain on login page"
