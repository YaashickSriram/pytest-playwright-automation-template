"""
base_page.py — Foundation for all Page Objects.

Every page inherits from BasePage and gets:
- 20+ reusable browser interactions with built-in logging
- Standard wait strategies via Waiter
- Allure step decoration on key actions
- Consistent error handling

Rule: No business logic here. Only generic browser interactions.
"""

from playwright.sync_api import Page

from utils.allure_helper import step
from utils.logger import get_logger
from utils.waiter import Waiter

logger = get_logger(__name__)


class BasePage:
    """
    Parent class for all page objects.
    Provides reusable browser interactions, waits, and state queries.
    """

    def __init__(self, page: Page, base_url: str = "", timeout_ms: int = 10000):
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.timeout_ms = timeout_ms
        self.waiter = Waiter(page, default_timeout_ms=timeout_ms)

    # ── Navigation ────────────────────────────────────────────────

    @step("Navigate to URL")
    def navigate(self, path: str = "") -> None:
        """Navigate to a path relative to base_url (or absolute URL)."""
        target = path if path.startswith("http") else f"{self.base_url}{path}"
        logger.info(f"Navigating to: {target}")
        self.page.goto(target, wait_until="domcontentloaded")

    def reload(self) -> None:
        """Reload the current page."""
        logger.info("Reloading page")
        self.page.reload(wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    # ── Interactions ──────────────────────────────────────────────

    def click(self, selector: str, description: str = "") -> None:
        """Click an element after waiting for it to be visible."""
        label = description or selector
        logger.info(f"Clicking: {label}")
        self.wait_for_element(selector)
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str, description: str = "") -> None:
        """Fill an input field with text (fast, programmatic)."""
        label = description or selector
        logger.info(f"Filling '{label}' with: {value}")
        self.wait_for_element(selector)
        self.page.locator(selector).fill(value)

    def type_sequentially(self, selector: str, value: str, delay: int = 50) -> None:
        """
        Type text keystroke-by-keystroke with delay.
        Required for React/Vue inputs that listen to keyboard events.
        """
        logger.info(f"Typing into {selector} (delay={delay}ms per char)")
        self.wait_for_element(selector)
        self.page.locator(selector).click()
        self.page.locator(selector).press_sequentially(value, delay=delay)

    def select_option(self, selector: str, value: str) -> None:
        """Select an option from a dropdown by value."""
        logger.info(f"Selecting '{value}' from {selector}")
        self.wait_for_element(selector)
        self.page.locator(selector).select_option(value)

    def check(self, selector: str) -> None:
        """Check a checkbox or radio button."""
        logger.info(f"Checking: {selector}")
        self.page.locator(selector).check()

    def uncheck(self, selector: str) -> None:
        """Uncheck a checkbox."""
        logger.info(f"Unchecking: {selector}")
        self.page.locator(selector).uncheck()

    def hover(self, selector: str) -> None:
        """Hover over an element."""
        logger.info(f"Hovering over: {selector}")
        self.page.locator(selector).hover()

    def press_key(self, key: str) -> None:
        """Press a keyboard key (e.g. 'Enter', 'Escape', 'Tab')."""
        logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)

    # ── State Queries ─────────────────────────────────────────────

    def is_visible(self, selector: str, timeout_ms: int = 2000) -> bool:
        """Check if an element is visible within the timeout."""
        try:
            return self.page.locator(selector).is_visible(timeout=timeout_ms)
        except Exception:
            return False

    def is_enabled(self, selector: str) -> bool:
        """Check if an element is enabled (interactive)."""
        try:
            return self.page.locator(selector).is_enabled()
        except Exception:
            return False

    def is_checked(self, selector: str) -> bool:
        """Check if a checkbox or radio button is checked."""
        try:
            return self.page.locator(selector).is_checked()
        except Exception:
            return False

    def get_text(self, selector: str) -> str:
        """Return the inner text of an element."""
        return self.page.locator(selector).inner_text()

    def get_value(self, selector: str) -> str:
        """Return the value of an input field."""
        return self.page.locator(selector).input_value()

    def get_attribute(self, selector: str, attribute: str) -> str:
        """Return the value of an HTML attribute."""
        return self.page.locator(selector).get_attribute(attribute)

    def get_all_text_contents(self, selector: str) -> list:
        """Return text content of all matching elements."""
        return self.page.locator(selector).all_text_contents()

    def count_elements(self, selector: str) -> int:
        """Return the count of matching elements."""
        return self.page.locator(selector).count()

    # ── Waits ─────────────────────────────────────────────────────

    def wait_for_element(self, selector: str, timeout_ms: int = None) -> bool:
        """Wait for an element to become visible."""
        return self.waiter.wait_for_element_visible(selector, timeout_ms)

    def wait_for_element_hidden(self, selector: str, timeout_ms: int = None) -> bool:
        """Wait for an element to disappear."""
        return self.waiter.wait_for_element_hidden(selector, timeout_ms)

    def wait_for_url(self, url_fragment: str, timeout_ms: int = None) -> bool:
        """Wait for the URL to contain a fragment."""
        return self.waiter.wait_for_url(url_fragment, timeout_ms)

    def wait_for_network_idle(self, timeout_ms: int = None) -> bool:
        """Wait for network traffic to settle."""
        return self.waiter.wait_for_network_idle(timeout_ms)

    # ── Scroll ────────────────────────────────────────────────────

    def scroll_to_element(self, selector: str) -> None:
        """Scroll an element into view."""
        logger.info(f"Scrolling to: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
