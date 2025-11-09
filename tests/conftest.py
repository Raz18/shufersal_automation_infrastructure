"""
Pytest configuration and fixtures for Shufersal Online automation tests.
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from utils.settings import Settings


@pytest.fixture(scope="session")
def playwright_instance():
    """Create a Playwright instance for the entire test session."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    """
    Launch browser instance for the test session.
    Using Chromium for stability and compatibility.
    Browser settings are loaded from Settings class.
    """
    browser = playwright_instance.chromium.launch(
        headless=Settings.HEADLESS,
        slow_mo=Settings.SLOW_MO,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Create a new browser context for each test to ensure isolation."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="he-IL",  # Hebrew locale for Shufersal
        timezone_id="Asia/Jerusalem",
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a new page for each test."""
    page = context.new_page()
    page.set_default_timeout(Settings.BROWSER_TIMEOUT)
    yield page
    page.close()


@pytest.fixture(scope="session")
def session_context(browser: Browser) -> BrowserContext:
    """Create a browser context for the entire test session (for session-based tests)."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="he-IL",  # Hebrew locale for Shufersal
        timezone_id="Asia/Jerusalem",
    )
    yield context
    context.close()


@pytest.fixture(scope="session")
def session_page(session_context: BrowserContext) -> Page:
    """Create a page for the entire test session (for session-based tests)."""
    page = session_context.new_page()
    page.set_default_timeout(Settings.BROWSER_TIMEOUT)
    yield page
    page.close()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "negative: mark test as negative test case")
    config.addinivalue_line("markers", "cart: mark test related to shopping cart")
    config.addinivalue_line("markers", "search: mark test related to search functionality")
    config.addinivalue_line("markers", "checkout: mark test related to checkout process")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end")
    config.addinivalue_line("markers", "functional: mark test as session-based functional test")
