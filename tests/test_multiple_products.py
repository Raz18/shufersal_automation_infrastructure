import pytest
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@pytest.mark.e2e
class TestMultipleProductsToCart:
    """
    Test Suite: Adding Multiple Products to Cart
    
    This test demonstrates the ability to add a custom number of products
    from search results to the cart in one operation.
    """
    
    def test_add_multiple_products_from_search(self, page):
        """
        Test adding multiple products from search results to cart.
        
        Flow:
        1. Navigate to homepage
        2. Search for a product category
        3. Display number of available products
        4. Add specified number of products to cart
        5. Verify cart contains all added products
        6. Clean up: Clear cart
        """
        # Initialize page objects
        home_page = HomePage(page)
        search_results_page = SearchResultsPage(page)
        cart_page = CartPage(page)
        
        # Test data
        search_term = "חלב"  # Hebrew for "Milk"
        num_products_to_add = 5
        
        # Navigate and search
        home_page.navigate()
        home_page.search_product(search_term)
        
        # Add multiple products to cart
        result = search_results_page.add_products_to_cart(
            num_products=num_products_to_add,
            handle_address_modal=False
        )
        
        # Verify the operation results
        assert result['success'], \
            f"Failed to add all requested products. Added {result['added']}/{result['requested']}"
        
        # Verify cart contains all products
        cart_page.open_cart_sidebar()
        
        # Verify cart item count matches added products
        cart_item_count = cart_page.get_cart_item_count()
        assert cart_item_count == result['added'], \
            f"Expected {result['added']} items in cart, but got {cart_item_count}"
        
        # Verify each product is in the cart
        verification_result = cart_page.verify_products_in_cart(
            product_names=result['product_names'],
            verbose=False
        )
        
        # Assert all products were found
        assert verification_result['success'], \
            f"Not all products found in cart. Missing: {verification_result['missing_products']}"
        
        # Verify cart total is greater than 0
        total_price = cart_page.get_checkout_total_price()
        assert total_price > 0.0, f"Expected price > 0, but got {total_price}"
        
        # Clean up
        cart_page.clear_cart()
        
        final_cart_count = cart_page.get_cart_item_count()
        assert final_cart_count == 0, f"Expected empty cart, but got {final_cart_count} items"
    
   
    