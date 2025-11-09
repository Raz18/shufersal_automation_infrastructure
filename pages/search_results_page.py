"""
Page object for Shufersal Online search results page.
"""
from typing import List
from pages.base_page import BasePage
from playwright.sync_api import Page
from pages.address_modal_page import AddressModal


class SearchResultsPage(BasePage):
    """Search results page object."""
    
    # Selectors
    PRODUCT_CONTAINER = "ul.tileContainer.newDesignProductTabsMobile"
    PRODUCT_ITEMS = "li.tileBlock.miglog-prod"
    PRODUCT_NAME = "div.text.description strong"
    PRODUCT_PRICE = "span.price span.number"
    ADD_TO_CART_BUTTON = "button.js-add-to-cart.miglog-btn-add"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.address_modal_helper = AddressModal(page)
    
    def wait_for_results_to_load(self) -> None:
        """Wait for search results to appear on page."""
        # Wait for product container to load
        self.page.wait_for_selector(self.PRODUCT_CONTAINER, timeout=10000)
        # Wait for at least one product item
        self.page.wait_for_selector(self.PRODUCT_ITEMS, timeout=10000)
    
    def get_all_product_items(self):
        """
        Get all product item locators.
        
        Returns:
            Locator for all product items
        """
        self.wait_for_results_to_load()
        return self.page.locator(self.PRODUCT_ITEMS)
    
    def get_first_n_product_names(self, n: int = 3) -> List[str]:
        """
        Get the names of the first N products in search results.
        
        Args:
            n: Number of product names to retrieve (default: 3)
            
        Returns:
            List of product names
        """
        product_names = []
        products = self.get_all_product_items()
        
        # Get count of available products
        count = products.count()
        
        # Iterate through first N products
        for i in range(min(n, count)):
            product = products.nth(i)
            name_element = product.locator(self.PRODUCT_NAME).first
            
            if name_element.is_visible():
                product_name = name_element.inner_text()
                product_names.append(product_name)
        
        return product_names
    
    def get_product_count(self) -> int:
        """
        Get total number of products in search results.
        Handles both normal results and empty search results.
        
        Returns:
            Number of products (0 if no results found)
        """

        
        # Check if product container exists
        try:
            self.page.wait_for_selector(self.PRODUCT_CONTAINER, timeout=10000)
            return self.page.locator(self.PRODUCT_ITEMS).count()
        except Exception:
            # No product container means no results
            return 0
    
    def add_first_product_to_cart(self, handle_address_modal: bool = True) -> bool:
        """
        Add the first product in search results to cart.
        
        Args:
            handle_address_modal: Whether to automatically handle address modal if it appears
        
        Returns:
            True if successfully added, False otherwise
        """
        result = self.add_products_to_cart(num_products=1, handle_address_modal=handle_address_modal)
        return result['success']
    
    def add_products_to_cart(self, num_products: int, handle_address_modal: bool = True) -> dict:
        """
        Add multiple products from search results to cart.
        Stores the exact product names element for later verification.
        
        Args:
            num_products: Number of products to add to cart
            handle_address_modal: Whether to automatically handle address modal if it appears (only for first product)
        
        Returns:
            Dictionary with results:
            {
                'total_available': int,  # Total products in search results
                'requested': int,        # Number of products requested
                'added': int,            # Number of products successfully added
                'success': bool,         # True if all requested products were added
                'product_names': list    # Names of products that were added (from <strong> element)
            }
        """
        result = {
            'total_available': 0,
            'requested': num_products,
            'added': 0,
            'success': False,
            'product_names': []
        }
        
        try:
            # Get total available products
            total_available = self.get_product_count()
            result['total_available'] = total_available
            
            self.logger.info(f"Search results: {total_available} products found, requesting {num_products} to add")
            
            # Validate requested amount
            if num_products <= 0:
                self.logger.warning(f"Invalid number of products: {num_products}. Must be greater than 0.")
                return result
            
            if num_products > total_available:
                self.logger.warning(f"Requested {num_products} products, but only {total_available} available. Will add all {total_available}.")
                num_products = total_available
            
            # Get all product items
            products = self.get_all_product_items()
            
            # Add each product to cart
            for i in range(num_products):
                try:
                    product = products.nth(i)
                    
                    
                    # This is the exact name as displayed in search results
                    name_element = product.locator(self.PRODUCT_NAME).first
                    product_name = name_element.inner_text() if name_element.is_visible() else f"Product {i+1}"
                    
                    # Find and click add to cart button
                    add_button = product.locator(self.ADD_TO_CART_BUTTON).first
                    add_button.click()
                    
                    # Handle address modal only for the first product
                    if i == 0:
                        # If handle_address_modal is True, fill the details
                        # If handle_address_modal is False, just close the modal
                        self.address_modal_helper.handle_address_modal_if_present(fill_details=handle_address_modal)
                    
                    # Store the product name for verification
                    result['added'] += 1
                    result['product_names'].append(product_name)
                    
                    self.logger.info(f"Added product {i+1}/{num_products}: '{product_name}'")
                    
                except Exception as e:
                    self.logger.error(f"Failed to add product {i+1}: {e}")
                    continue
            
            # Set success flag
            result['success'] = (result['added'] == result['requested'])
            
            self.logger.info(f"Cart operation completed: {result['added']}/{result['requested']} products added")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in add_products_to_cart: {e}")
            return result
    
    def verify_product_contains_keyword(self, product_index: int, keyword: str) -> bool:
        """
        Verify that a specific product contains a keyword in its name.
        
        Args:
            product_index: Index of the product (0-based)
            keyword: Keyword to search for
            
        Returns:
            True if product name contains keyword, False otherwise
        """
        products = self.get_all_product_items()
        
        if product_index >= products.count():
            return False
        
        product = products.nth(product_index)
        name_element = product.locator(self.PRODUCT_NAME).first
        product_name = name_element.inner_text()
        
        return keyword in product_name
    
    def get_product_price_by_name(self, product_name: str) -> float:
        """
        Get the price of a product by its name.
        
        Args:
            product_name: Name of the product to find (partial match)
            
        Returns:
            Price as a float, or None if product not found
        """
        try:
            products = self.get_all_product_items()
            
            for i in range(products.count()):
                product = products.nth(i)
                
                # Get product name
                name_element = product.locator(self.PRODUCT_NAME).first
                if name_element.is_visible():
                    current_name = name_element.inner_text()
                    
                    # Check if this is the product we're looking for (case-insensitive partial match)
                    if product_name.lower() in current_name.lower():
                        # Get price
                        price_element = product.locator(self.PRODUCT_PRICE).first
                        if price_element.is_visible():
                            price_text = price_element.inner_text().strip()
                            # Convert to float
                            return float(price_text)
            
            self.logger.warning(f"Product '{product_name}' not found in search results")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting price for product '{product_name}': {e}")
            return None


