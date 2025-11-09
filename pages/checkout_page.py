"""
Page object for checkout page.
"""
from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutPage(BasePage):
    """Checkout page object."""
    
    # Login Wall Selectors
    LOGIN_HEADER = "h2.login-page__header:has-text('איזה כיף שבאת :)')"
    LOGIN_FORM = "form#loginForm"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def is_login_wall_displayed(self) -> bool:
        """
        Check if login wall is displayed.
        This is expected as we should NOT complete actual purchase.
        
        Returns:
            True if login/auth wall is blocking checkout
        """
        return self.is_visible(self.LOGIN_HEADER, timeout=5000) or \
               self.is_visible(self.LOGIN_FORM, timeout=5000)
