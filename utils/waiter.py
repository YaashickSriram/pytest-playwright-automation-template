"""
waiter.py — Condition-based wait strategies.

Never use time.sleep() in the framework.
Always wait for a specific condition — the application decides timing.
"""

from utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT_MS = 10000


class Waiter:
    """
    Encapsulates all explicit wait strategies.
    Each method polls for a specific condition and returns success/failure.
    """

    def __init__(self, page, default_timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page = page
        self.default_timeout_ms = default_timeout_ms

    def wait_for_element_visible(self, selector: str, timeout_ms: int = None) -> bool:
        """Wait for an element to become visible in the DOM."""
        timeout = timeout_ms or self.default_timeout_ms
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"Element not visible after {timeout}ms: {selector} — {e}")
            return False

    def wait_for_element_hidden(self, selector: str, timeout_ms: int = None) -> bool:
        """Wait for an element to disappear from the DOM."""
        timeout = timeout_ms or self.default_timeout_ms
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"Element still visible after {timeout}ms: {selector} — {e}")
            return False

    def wait_for_url(self, url_fragment: str, timeout_ms: int = None) -> bool:
        """Wait for the page URL to contain the given fragment."""
        timeout = timeout_ms or self.default_timeout_ms
        try:
            self.page.wait_for_url(f"**{url_fragment}**", timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"URL did not match '{url_fragment}' after {timeout}ms — {e}")
            return False

    def wait_for_network_idle(self, timeout_ms: int = None) -> bool:
        """Wait until no network requests for 500ms."""
        timeout = timeout_ms or self.default_timeout_ms
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"Network did not reach idle state after {timeout}ms")
            return False

    def wait_for_text(self, selector: str, expected_text: str, timeout_ms: int = None) -> bool:
        """Wait for an element to contain the expected text."""
        timeout = timeout_ms or self.default_timeout_ms
        try:
            self.page.locator(selector).filter(has_text=expected_text).wait_for(
                state="visible", timeout=timeout
            )
            return True
        except Exception as e:
            logger.warning(f"Text '{expected_text}' not found in {selector} after {timeout}ms")
            return False
