"""Page objects package initialization."""
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.address_modal_page import AddressModal

__all__ = [
    'BasePage',
    'HomePage',
    'SearchResultsPage',
    'CartPage',
    'CheckoutPage',
    'AddressModal',
]
