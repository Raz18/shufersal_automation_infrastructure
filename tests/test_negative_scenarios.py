"""
Negative test cases for Shufersal Online.
Tests error handling and edge cases.
"""
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.cart_page import CartPage


@pytest.mark.negative
class TestNegativeScenarios:
    """Test suite for negative/edge case scenarios."""
    
    def test_search_nonexistent_product(self, session_page: Page):
        """
        Test searching for a product that doesn't exist.
        
        Steps:
            1. Navigate to homepage
            2. Search for gibberish/non-existent product
            3. Verify no results or empty results
        
        Expected:
            - System shows no results or returns 0 products
            - No application errors occur
        """
        # Arrange
        home_page = HomePage(session_page)
        search_page = SearchResultsPage(session_page)
        nonexistent_product = "XYZQWERTY99999NOTAREALPRODUCT"
        
        # Act
        home_page.navigate()
        home_page.search_product(nonexistent_product)
        
        # Assert
        product_count = search_page.get_product_count()
        assert product_count == 0, \
            f"Expected no results for non-existent product, but found {product_count} products"

    @pytest.mark.cart
    def test_checkout_disabled_with_empty_cart(self, session_page: Page):
        """
        Test that checkout button is disabled when cart is empty.
        
        Steps:
            1. Navigate to homepage
            2. Open cart sidebar (without adding products)
            3. Verify checkout button is disabled
            4. Verify price shows 0.00
        
        Expected:
            - Checkout button should not be clickable
            - Price should display 0.00
        """
        # Arrange
        home_page = HomePage(session_page)
        cart_page = CartPage(session_page)
        
        # Act
        home_page.navigate()
        cart_page.open_cart_sidebar()
        
        # Assert
        assert cart_page.is_cart_empty(), "Cart should be empty"
        
        is_enabled = cart_page.is_checkout_button_enabled()
        assert not is_enabled, "Checkout button should be disabled when cart is empty"
        
        total_price = cart_page.get_checkout_total_price()
        assert total_price == 0.00, f"Expected price 0.00, but got '{total_price}'"

    @pytest.mark.search
    def test_search_with_special_characters(self, session_page: Page):
        """
        Test searching with special characters and symbols.
        
        Steps:
            1. Navigate to homepage
            2. Search for product using special characters (@#$%^&*)
            3. Verify system handles it gracefully (no crash)
            4. Verify results or no results message
        
        Expected:
            - System should not crash
            - Should return 0 results or handle gracefully
        """
        # Arrange
        home_page = HomePage(session_page)
        search_page = SearchResultsPage(session_page)
        special_chars_query = "@#$%^&*()!~"
        
        # Act
        home_page.navigate()
        home_page.search_product(special_chars_query)
        
        # Assert - system should handle gracefully
        product_count = search_page.get_product_count()
        assert product_count >= 0, "Product count should be non-negative"
        
        

