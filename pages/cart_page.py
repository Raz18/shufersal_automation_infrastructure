"""
Page object for shopping cart sidebar.
The cart is implemented as a sidebar that opens on the same page, not a separate page.
"""
from pages.base_page import BasePage
from playwright.sync_api import Page
import re

class CartPage(BasePage):
    """Shopping cart sidebar page object."""
    
    # Cart Toggle & Badge
    CART_TOGGLE_BUTTON = "button.btnToggle.bouncingArrow[data-target='#main']"
    CART_COUNT_BADGE = "div.img-cart span#cartTotalItems"
    
    # Cart Sidebar Container
    CART_SIDEBAR = "div.innerCart"
    CART_MIDDLE_CONTENT = "section.miglog-cart-middleContent#cartMiddleContent"
    CLOSE_CART_BUTTON = "button.closeCart.btnClose"

    # Cart Items
    CART_ITEM = "article.miglog-prod"
    ITEM_NAME = "h3.miglog-prod-name"
    ITEM_REMOVE_BUTTON = "a[data-miglog-role='cart-item-remover']"
    ITEM_QUANTITY_INPUT = "input.spinContainer.js-qty-selector-input[name='qty']"
    ITEM_QUANTITY_INCREASE_BUTTON = "button.btnTouchspin.bootstrap-touchspin-up"
    ITEM_QUANTITY_DECREASE_BUTTON = "button.btnTouchspin.bootstrap-touchspin-down"
    ITEM_UPDATE_BUTTON = "button.js-update-cart.miglog-btn-update"
    
    # Clear Cart
    CLEAR_CART_CONFIRM = "button:has-text('כן, רוקנו את הסל')"
    
    # Empty Cart State
    EMPTY_CART_MESSAGE = "h3.topTitle:has-text('שנתחיל לקנות?')"
    
    # Checkout
    CHECKOUT_LINK_ENABLED = "a.btnSubmit[data-miglog-role='cart-summary-link']:not(.disabled)"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    # ============================================================================
    # CART SIDEBAR OPERATIONS
    # ============================================================================
    
    def open_cart_sidebar(self) -> None:
        """Open the cart sidebar by clicking the cart toggle button."""
        self.click_element(self.CART_TOGGLE_BUTTON)
        self.page.locator(self.CART_SIDEBAR).wait_for(state="visible", timeout=5000)
    
    def close_cart_sidebar(self) -> None:
        """Close the cart sidebar."""
        if self.is_cart_sidebar_open():
            self.click_element(self.CLOSE_CART_BUTTON)
            self.page.locator(self.CART_SIDEBAR).wait_for(state="hidden", timeout=3000)
    
    def is_cart_sidebar_open(self) -> bool:
        """Check if cart sidebar is currently open."""
        try:
            return self.is_visible(self.CART_MIDDLE_CONTENT, timeout=1000)
        except:
            return False
    
    # ============================================================================
    # CART ITEM OPERATIONS
    # ============================================================================
    
    def get_cart_item_count(self) -> int:
        """Get number of items in cart from the sidebar."""
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        if self.is_visible(self.EMPTY_CART_MESSAGE, timeout=5000):
            return 0
        
        items = self.page.locator(self.CART_ITEM)
        try:
            items.first.wait_for(state="attached", timeout=5000)
            return items.count()
        except:
            return 0
    
    def get_product_quantity_in_cart(self, product_name: str) -> int:
        """
        Get the quantity of a specific product in the cart.
        
        Args:
            product_name: Name of the product to check
            
        Returns:
            Quantity of the product as integer, or 0 if not found
        """
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        item = self._get_cart_item_by_name(product_name)
        if item:
            try:
                quantity_input = item.locator(self.ITEM_QUANTITY_INPUT)
                if quantity_input.count() > 0:
                    quantity_value = quantity_input.input_value()
                    return int(float(quantity_value))
            except:
                pass
        
        return 0
    
    def check_product_quantity_in_cart(self, product_name: str, expected_quantity: int) -> bool:
        """
        Check if a specific product has the expected quantity in the cart.
        
        Args:
            product_name: Name of the product to check
            expected_quantity: Expected quantity of the product

        Returns:
            True if the product has the expected quantity, False otherwise
        """
        actual_quantity = self.get_product_quantity_in_cart(product_name)
        return actual_quantity == expected_quantity
    

    def is_cart_empty(self) -> bool:
        """Check if the empty cart message is displayed."""
        return self.is_visible(self.EMPTY_CART_MESSAGE, timeout=5000)
    
    
    def check_product_in_cart(self, product_name: str) -> bool:
        """
        Verify that a specific product is in the cart by checking the product name element.
        
        Args:
            product_name: Name (or partial name) of the product to verify
        
        Returns:
            True if product name found in cart items, False otherwise
        """
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        if self.is_visible(self.EMPTY_CART_MESSAGE, timeout=2000):
            return False
        
        # Get all cart items
        cart_items = self.page.locator(self.CART_ITEM)
        cart_items.first.wait_for(state="attached", timeout=5000)
        
        # Iterate through cart items and check product names
        for i in range(cart_items.count()):
            item = cart_items.nth(i)
            product_name_element = item.locator(self.ITEM_NAME)
            
            if product_name_element.count() > 0:
                actual_product_name = product_name_element.inner_text().strip()
                # Check if the provided product_name is contained in the actual product name
                if product_name.lower() in actual_product_name.lower():
                    return True
        
        return False
    
    def verify_products_in_cart(self, product_names: list, verbose: bool = True) -> dict:
        """
        Verify multiple products are in the cart efficiently.
        
        Args:
            product_names: List of product names to verify
            verbose: If True, print verification progress (default: True)
        
        Returns:
            Dictionary with verification results:
            {
                'total_checked': int,     # Total products checked
                'found': int,             # Number of products found
                'missing': int,           # Number of products missing
                'success': bool,          # True if all products found
                'found_products': list,   # List of products that were found
                'missing_products': list  # List of products that were missing
            }
        """
        result = {
            'total_checked': len(product_names),
            'found': 0,
            'missing': 0,
            'success': False,
            'found_products': [],
            'missing_products': []
        }
        
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        if verbose:
            self.logger.info(f"Verifying {len(product_names)} products in cart")
        
        # Check if cart is empty
        if self.is_visible(self.EMPTY_CART_MESSAGE, timeout=2000):
            result['missing'] = len(product_names)
            result['missing_products'] = product_names.copy()
            if verbose:
                self.logger.warning("Cart is empty, all products are missing")
            return result
        
        # Fetch all cart item names once (efficient - single DOM query)
        cart_items = self.page.locator(self.CART_ITEM)
        cart_items.first.wait_for(state="attached", timeout=5000)
        
        cart_product_names = []
        for i in range(cart_items.count()):
            item = cart_items.nth(i)
            product_name_element = item.locator(self.ITEM_NAME)
            if product_name_element.count() > 0:
                cart_product_names.append(product_name_element.inner_text().strip().lower())
        
        # Check each product against the fetched cart names
        for product_name in product_names:
            found = any(product_name.lower() in cart_name for cart_name in cart_product_names)
            
            if found:
                result['found'] += 1
                result['found_products'].append(product_name)
            else:
                result['missing'] += 1
                result['missing_products'].append(product_name)
                if verbose:
                    self.logger.warning(f"Product '{product_name}' NOT FOUND in cart")
        
        result['success'] = (result['missing'] == 0)
        
        if verbose:
            if result['success']:
                self.logger.info(f"All {result['found']} products verified successfully")
            else:
                self.logger.warning(f"{result['found']}/{result['total_checked']} products found. Missing: {result['missing_products']}")
        
        return result
    
    def update_product_quantity_by_name(self, product_name: str, quantity: int) -> bool:
        """
        Update the quantity of a product in the cart.
        
        Args:
            product_name: Name of the product to update
            quantity: Desired quantity (must be >= 1)
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            if quantity < 1:
                self.logger.warning(f"Invalid quantity: {quantity}")
                return False
            
            if not self.is_cart_sidebar_open():
                self.open_cart_sidebar()
            
            # Find product in cart
            item = self._get_cart_item_by_name(product_name)
            if not item:
                self.logger.warning(f"Product '{product_name}' not found in cart")
                return False
            
            # Get quantity controls
            quantity_input = item.locator(self.ITEM_QUANTITY_INPUT).first
            increase_button = item.locator(self.ITEM_QUANTITY_INCREASE_BUTTON).first
            decrease_button = item.locator(self.ITEM_QUANTITY_DECREASE_BUTTON).first
            
            # Wait for buttons to be available
            increase_button.wait_for(state="attached", timeout=5000)
            
            # Get current quantity
            current_qty = int(float(quantity_input.input_value()))
            
            # Adjust quantity using +/- buttons
            if quantity > current_qty:
                for _ in range(quantity - current_qty):
                    increase_button.click()
                    self.page.wait_for_timeout(200)
            elif quantity < current_qty:
                for _ in range(current_qty - quantity):
                    decrease_button.click()
                    self.page.wait_for_timeout(200)
            
            # Click update button
            item.locator(self.ITEM_UPDATE_BUTTON).first.click()

            self.logger.info(f"Updated '{product_name}' quantity from {current_qty} to {quantity}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating quantity for '{product_name}': {e}")
            return False
    
    # ============================================================================
    # ITEM REMOVAL OPERATIONS
    # ============================================================================
    
    def _get_cart_item_by_name(self, product_name: str):
        """
        method to find a cart item by product name.
        
        Args:
            product_name: Name of the product to find
            
        Returns:
            Locator for the cart item article, or None if not found
        """
        items = self.page.locator(self.CART_ITEM)
        for i in range(items.count()):
            item = items.nth(i)
            name_element = item.locator(self.ITEM_NAME)
            if name_element.count() > 0 and product_name.lower() in name_element.inner_text().lower():
                return item
        return None
    
    def remove_item_from_cart(self, index: int = 0) -> None:
        """
        Remove an item from cart by index.
        
        Args:
            index: Index of item to remove (0-based)
        """
        items = self.page.locator(self.CART_ITEM)
        initial_count = items.count()
        
        if initial_count > index:
            item = items.nth(index)
            remove_button = item.locator(self.ITEM_REMOVE_BUTTON)
            remove_button.wait_for(state="visible", timeout=5000)
            remove_button.click()
            
            # Wait for item count to decrease
            self.page.wait_for_function(
                f"document.querySelectorAll('{self.CART_ITEM}').length < {initial_count}",
                timeout=7000
            )
    
    def remove_product_by_name(self, product_name: str) -> bool:
        """
        Remove a specific product from cart by name.
        
        Args:
            product_name: Name of the product to remove
        
        Returns:
            True if product was found and removed, False otherwise
        """
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        item_to_remove = self._get_cart_item_by_name(product_name)
        
        if item_to_remove:
            initial_count = self.page.locator(self.CART_ITEM).count()
            remove_button = item_to_remove.locator(self.ITEM_REMOVE_BUTTON)
            remove_button.click()
            
            # Wait for item count to decrease
            self.page.wait_for_function(
                f"document.querySelectorAll('{self.CART_ITEM}').length < {initial_count}",
                timeout=7000
            )
            return True
        
        return False
    
    def clear_cart(self) -> None:
        """Clear all items from the cart using the clear cart button."""
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        # Click the clear cart button
        clear_cart_button = self.page.get_by_role("button", name="ניקוי הסל")
        clear_cart_button.wait_for(state="visible", timeout=5000)
        clear_cart_button.click()
        
        # Wait for confirmation dialog and confirm
        confirm_button = self.page.locator(self.CLEAR_CART_CONFIRM)
        confirm_button.wait_for(state="visible", timeout=3000)
        confirm_button.click()
        
        # Wait for cart to be empty
        self.page.locator(self.EMPTY_CART_MESSAGE).wait_for(state="visible", timeout=5000)
    
    # ============================================================================
    # CHECKOUT OPERATIONS
    # ============================================================================
    
    def is_checkout_button_enabled(self) -> bool:
        """
        Check if the checkout button is enabled (cart has items).
        
        Returns:
            True if button is enabled (clickable), False if disabled
        """
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        try:
            enabled_link = self.page.locator(self.CHECKOUT_LINK_ENABLED)
            return enabled_link.is_visible(timeout=2000)
        except:
            return False
    
    def get_checkout_total_price(self) -> float:
        """
        Get the total price displayed on the checkout button.
        
        Returns:
            Total price as float (e.g., 181.60) or 0.00 if cart is empty
        """
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        try:
            # Use role-based selector for better reliability
            checkout_link = self.page.get_by_role("link", name="לתשלום: שקלים חדשים")
            checkout_link.wait_for(state="visible", timeout=5000)   
            
            # Get full text and extract the numeric value
            full_text = checkout_link.inner_text()
        
            match = re.search(r'(\d+[.,]?\d*)', full_text)
            if match:
                price_value = match.group(1).replace(',', '.')
                return float(price_value)
            
            return 0.00
        except Exception as e:
            return 0.00
    
    def proceed_to_checkout(self) -> None:
        """
        Click proceed to checkout button in the cart sidebar.
        Only works if cart has items (button is enabled).
        """
        if not self.is_cart_sidebar_open():
            self.open_cart_sidebar()
        
        if not self.is_checkout_button_enabled():
            raise Exception("Cannot proceed to checkout: cart is empty or button is disabled")
        
        checkout_link = self.page.locator(self.CHECKOUT_LINK_ENABLED)
        checkout_link.wait_for(state="visible", timeout=5000)
        checkout_link.click()
    
    # ============================================================================
    # HELPER OPERATIONS
    # ============================================================================
    
    def get_cart_badge_count(self) -> str:
        """
        Get the cart badge count as a string.
        
        Returns:
            Badge count as string (e.g., "0", "1", "5")
        """
        try:
            badge_text = self.get_text(self.CART_COUNT_BADGE)
            return badge_text.strip()
        except:
            return "0"