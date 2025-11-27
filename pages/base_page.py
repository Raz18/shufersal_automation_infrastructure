"""
Base page class with common functionality for all page objects.
"""
from playwright.sync_api import Page, TimeoutError
from utils.helpers import setup_logger


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = setup_logger(__name__)
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL."""
        self.page.goto(url)
    
    def wait_for_load_state(self, state: str = "load") -> None:
        """Wait for page to reach a specific load state."""
        self.page.wait_for_load_state(state)
    
    def click_element(self, selector: str) -> None:
        """Click an element with waiting."""
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str) -> None:
        """Fill an input field."""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.locator(selector).inner_text()
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible."""
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            return True
        except TimeoutError:
            return False
    
    def wait_for_element(self, selector: str, timeout: int = 30000) -> None:
        """Wait for element to be visible."""
        self.page.wait_for_selector(selector, timeout=timeout, state="visible")
    
    def take_screenshot(self, name: str) -> None:
        """Take a screenshot."""
        self.page.screenshot(path=f"screenshots/{name}.png")
