import pytest
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@pytest.mark.e2e
@pytest.mark.smoke
class TestEndToEndPurchaseFlow:
    """
    End-to-End Test Suite: Complete Purchase Flow
    
    This test validates the complete user journey from product search to checkout,
    without actually completing a real purchase (stops at login wall).
    
    NOTE: Address and delivery slot handling uses mock/test data via environment variables.
    In a production test environment, this would be handled via:
    - test accounts with saved addresses
    - Test backend API to mock address validation using already prepared json responses from a test sql db
    - Dedicated test environment with known delivery slots
    """
    
    def test_search_add_to_cart_verify_and_checkout(self, page):
        """
        Test complete user flow: Search → Add to Cart → Verify → Checkout → Login Wall
        
        High-Level Flow:
        1. Navigate to homepage
        2. Search for a product (e.g., "Milk")
        3. Verify first 3 results are relevant
        4. Add first product to cart (handles address/delivery slot popup automatically)
        5. Verify cart contains correct product and quantity
        6. Proceed to checkout
        7. Assert login wall appears (test stops here - no real purchase)
        8. Clean up: Remove item from cart
        """
        # Initialize page objects
        home_page = HomePage(page)
        search_results_page = SearchResultsPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        # Test data
        search_term = "חלב" 
        
        # Navigate and search
        home_page.navigate()
        home_page.search_product(search_term)
        
        # Verify first 3 results are relevant
        first_three_products = search_results_page.get_first_n_product_names(3)
        
        assert len(first_three_products) >= 3, \
            f"Expected at least 3 search results, but got {len(first_three_products)}"
        
        for index, product_name in enumerate(first_three_products, start=1):
            assert search_term in product_name, \
                f"Product {index} '{product_name}' does not contain '{search_term}'"
        
        # Add first product to cart
        result = search_results_page.add_products_to_cart(num_products=1, handle_address_modal=False)
        assert result['success'], "Failed to add product to cart"
        
        added_product_name = result['product_names'][0]
        
        # Verify cart contains correct product and quantity
        cart_page.open_cart_sidebar()
        
        # Verify cart has at least 1 item
        cart_item_count = cart_page.get_cart_item_count()
        assert cart_item_count >= 1, f"Expected at least 1 item in cart, but got {cart_item_count}"
        
        # Verify product quantity
        product_quantity = cart_page.get_product_quantity_in_cart(search_term)
        assert product_quantity > 0, f"Expected product quantity > 0, but got {product_quantity}"
        
        # Verify total price is greater than 0
        total_price = cart_page.get_checkout_total_price()
        assert total_price > 0.0, f"Expected price > 0, but got {total_price}"
        
        # Verify the product is in cart
        is_product_in_cart = cart_page.check_product_in_cart(added_product_name)
        assert is_product_in_cart, f"Product '{added_product_name}' not found in cart"

        # Verify checkout button is enabled
        is_checkout_enabled = cart_page.is_checkout_button_enabled()
        assert is_checkout_enabled, "Checkout button should be enabled when cart has items"
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Verify login wall is displayed
        is_login_wall_displayed = checkout_page.is_login_wall_displayed()
        assert is_login_wall_displayed, "Expected login wall to be displayed before checkout"
        
        # Clean up
        page.go_back()
        cart_page.open_cart_sidebar()
        cart_page.clear_cart()
        
        final_cart_count = cart_page.get_cart_item_count()
        assert final_cart_count == 0, f"Expected empty cart, but got {final_cart_count} items"
     

