"""
Page object for Shufersal Online homepage.
"""
from pages.base_page import BasePage
from playwright.sync_api import Page, TimeoutError


class HomePage(BasePage):
    """Shufersal Online homepage page object."""
    
    # Selectors - based on actual site inspection
    SEARCH_INPUT = "input[placeholder='חיפוש פריט, קטגוריה או מותג..']"
    SEARCH_BUTTON = "button:has-text('לתוצאות חיפוש')"
    LOGO = "a:has-text('שופרסל אונליין')"
    CART_ICON = "button:has-text('הסל שלי')"
    CART_LEFT_BAR_TOGGLE = "button.btnToggle.bouncingArrow[data-target='#main']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.shufersal.co.il/online/he"
    
    def navigate(self) -> None:
        """Navigate to Shufersal Online homepage."""
        self.navigate_to(self.url)
        # Wait for key elements to be visible
        self.wait_for_element(self.SEARCH_INPUT, timeout=10000)
        # Dismiss any promotional popups that may appear on first visit
        self._dismiss_popups()
    
    def search_product(self, product_name: str) -> None:
        """
        Search for a product.
        
        Args:
            product_name: Name of the product to search for
        """
        # Wait for search input to be available
        self.wait_for_element(self.SEARCH_INPUT)
        
        # Fill search input
        self.fill_input(self.SEARCH_INPUT, product_name)
        
        # Click search or press Enter
        self.page.keyboard.press("Enter")
    
    def is_homepage_loaded(self) -> bool:
        """Verify homepage is loaded."""
        return self.is_visible(self.LOGO) and self.is_visible(self.SEARCH_INPUT)
    
    def go_to_cart(self) -> None:
        """Navigate to shopping cart (opens cart sidebar)."""
        self.click_element(self.CART_LEFT_BAR_TOGGLE)
        # Wait for cart sidebar to appear
        self.page.locator("complementary").wait_for(state="visible", timeout=5000)

    def _dismiss_popups(self) -> None:
        """Dismiss any promotional popups that appear on first visit."""
        try:
            # Look for Close button in promotional popup
            close_button = self.page.locator("status button:has-text('Close')")
            if close_button.is_visible(timeout=2000):
                close_button.click()
                self.logger.info("Dismissed promotional popup")
        except TimeoutError:
            pass  # No popup to dismiss
