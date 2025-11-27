"""Functional test cases for Shufersal Online."""
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.cart_page import CartPage


@pytest.mark.functional
class TestFunctionality:
    """Test suite for cart functionality."""
    
    @pytest.mark.cart
    def test_add_and_remove_single_item(self, session_page: Page):
        """
        Test adding and removing a single item from cart.
        
        Steps:
            1. Navigate to homepage
            2. Search for a product
            3. Add one product to cart
            4. Verify item exists in cart
            5. Remove the item
            6. Verify cart is empty
        
        Expected:
            - Item is successfully added
            - Item is successfully removed
            - Cart shows as empty after removal
        """
        # Arrange
        home_page = HomePage(session_page)
        search_page = SearchResultsPage(session_page)
        cart_page = CartPage(session_page)
        
        # Add product
        home_page.navigate()
        home_page.search_product("חלב")
        result = search_page.add_products_to_cart(num_products=1, handle_address_modal=False)
        assert result['success'], "Failed to add product to cart"
        
        cart_page.open_cart_sidebar()
        initial_count = cart_page.get_cart_item_count()
        assert initial_count >= 1, "Cart should have at least 1 item"
        
        # Remove item
        cart_page.remove_item_from_cart(index=0)
        
        # Assert cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty after removing all items"

    @pytest.mark.cart
    def test_checkout_button_state_changes(self, session_page: Page):
        """
        Test checkout button state when adding and removing products.
        
        Steps:
            1. Navigate to homepage
            2. Verify checkout disabled on empty cart
            3. Add product to cart
            4. Verify checkout enabled with price > 0
            5. Clear cart
            6. Verify checkout disabled with price = 0.00
        
        Expected:
            - Empty cart: button disabled, price = 0.00
            - With items: button enabled, price > 0
            - After clearing: button disabled, price = 0.00
        """
        # Arrange
        home_page = HomePage(session_page)
        search_page = SearchResultsPage(session_page)
        cart_page = CartPage(session_page)
        
        # Check empty cart
        home_page.navigate()
        cart_page.open_cart_sidebar()
        
        # Assert empty cart state
        assert cart_page.is_cart_empty(), "Cart should be empty"
        
        # Add product
        home_page.search_product("חלב")
        result = search_page.add_products_to_cart(num_products=1, handle_address_modal=False)
        assert result['success'], "Failed to add product to cart"
        
        cart_page.open_cart_sidebar()
        
        # Assert cart with items
        is_enabled_with_items = cart_page.is_checkout_button_enabled()
        assert is_enabled_with_items, "Checkout button should be enabled when cart has items"
        
        total_price = cart_page.get_checkout_total_price()
        assert total_price > 0, f"Expected price > 0, but got {total_price}"
        
        # Clear cart
        cart_page.clear_cart()
        
        # Assert empty cart after clearing
        is_enabled_after = cart_page.is_checkout_button_enabled()
        assert not is_enabled_after, "Checkout button should be disabled after clearing cart"
        
        total_price_after = cart_page.get_checkout_total_price()
        assert total_price_after == 0.00, f"Expected price 0.00, but got {total_price_after}"

    @pytest.mark.cart
    def test_update_product_quantity_in_cart(self, page: Page):
        """
        Test updating product quantity in cart.
        
        Flow:
        1. Navigate to homepage
        2. Search for a product
        3. Add 1 product to cart
        4. Update its quantity to 5
        5. Verify cart shows correct quantity
        6. Clean up: Clear cart
        """
        # Initialize page objects
        home_page = HomePage(page)
        search_results_page = SearchResultsPage(page)
        cart_page = CartPage(page)
        
        # Test data
        search_term = "חלב"
        target_quantity = 5
        
        # Navigate and search
        home_page.navigate()
        home_page.search_product(search_term)
        
        # Add 1 product to cart
        result = search_results_page.add_products_to_cart(
            num_products=1,
            handle_address_modal=False
        )
        
        assert result['success'], "Failed to add product"
        product_name = result['product_names'][0]
        
        # Update quantity
        cart_page.open_cart_sidebar()
        
        update_success = cart_page.update_product_quantity_by_name(product_name, target_quantity)
        assert update_success, f"Failed to update quantity for '{product_name}'"
        
        # Verify quantity
        actual_quantity = cart_page.get_product_quantity_in_cart(product_name)
        assert actual_quantity == target_quantity, \
            f"Expected quantity {target_quantity}, but got {actual_quantity}"
        
        # Clean up
        cart_page.clear_cart()
        assert cart_page.is_cart_empty(), "Cart should be empty after cleanup"
    
    

    @pytest.mark.cart
    def test_get_product_price(self, session_page: Page):
        """
        Test retrieving product price from search results.
        
        Steps:
            1. Navigate to homepage
            2. Search for products
            3. Get price of first product
            4. Verify price is a valid number
        
        Expected:
            - Price is retrieved successfully
            - Price is > 0
        """
        # Arrange
        home_page = HomePage(session_page)
        search_page = SearchResultsPage(session_page)
        
        # Search for products
        home_page.navigate()
        home_page.search_product("חלב")
        
        # Get first product name
        product_names = search_page.get_first_n_product_names(n=1)
        assert len(product_names) > 0, "No products found"
        product_name = product_names[0]
        
        # Get price
        price = search_page.get_product_price_by_name(product_name)
        
        # Assert
        assert price is not None, f"Price not found for product '{product_name}'"
        assert price > 0, f"Expected price > 0, but got {price}"