from enum import Enum
from .settings import get_settings

settings = get_settings()

class SortOptions(Enum):
    PRICE_LOW_TO_HIGH = "Price (low to high)"
    PRICE_HIGH_TO_LOW = "Price (high to low)"
    NAME_A_TO_Z = "Name (A to Z)"
    NAME_Z_TO_A = "Name (Z to A)"

class Products:
    BACKPACK = "Sauce Labs Backpack"
    BIKE_LIGHT = "Sauce Labs Bike Light"
    BOLT_SHIRT = "Sauce Labs Bolt T-Shirt"
    FLEECE_JACKET = "Sauce Labs Fleece Jacket"
    ONESIE = "Sauce Labs Onesie"
    TEST_SHIRT = "Test.allTheThings() T-Shirt (Red)"

class TestData:
    SHIPPING = {
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "12345"
    }

class URLs:
    BASE_URL = settings.BASE_URL
    LOGIN = f"{BASE_URL}/index.html"
    INVENTORY = f"{BASE_URL}/inventory.html"
    CART = f"{BASE_URL}/cart.html"
    CHECKOUT_STEP_ONE = f"{BASE_URL}/checkout-step-one.html"
    CHECKOUT_STEP_TWO = f"{BASE_URL}/checkout-step-two.html"
    CHECKOUT_COMPLETE = f"{BASE_URL}/checkout-complete.html"
    CHECKOUT = f"{BASE_URL}/checkout-step-one.html"

class Credentials:
    STANDARD_USER = settings.STANDARD_USER
    STANDARD_PASSWORD = settings.STANDARD_PASSWORD
    LOCKED_OUT_USER = settings.LOCKED_OUT_USER
    LOCKED_OUT_PASSWORD = settings.LOCKED_OUT_PASSWORD
    PROBLEM_USER = settings.PROBLEM_USER
    PROBLEM_PASSWORD = settings.PROBLEM_PASSWORD