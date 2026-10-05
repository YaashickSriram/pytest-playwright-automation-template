"""
login_page.py — Sauce Demo login page object.

Reference implementation demonstrating:
- BasePage inheritance
- Selector ownership (all selectors live here)
- @step decoration for Allure
- Separation of actions from assertions
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.allure_helper import step
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object for the Sauce Demo login page.
    All CSS selectors for this page live here and only here.
    """

    # ── Locators ─────────────────────────────────────────────────
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"
    ERROR_MESSAGE  = "[data-test='error']"
    LOGO           = ".login_logo"

    def __init__(self, page: Page, base_url: str = "", timeout_ms: int = 10000):
        super().__init__(page, base_url, timeout_ms)

    # ── Page State ───────────────────────────────────────────────

    @step("Wait for login page to be ready")
    def wait_for_page_load(self) -> None:
        """Wait for the login form to be fully rendered."""
        self.wait_for_element(self.LOGO)
        self.wait_for_element(self.USERNAME_INPUT)
        logger.info("Login page is ready")

    # ── Actions ──────────────────────────────────────────────────

    @step("Enter username")
    def enter_username(self, username: str) -> None:
        self.fill(self.USERNAME_INPUT, username, description="Username")

    @step("Enter password")
    def enter_password(self, password: str) -> None:
        self.fill(self.PASSWORD_INPUT, password, description="Password")

    @step("Click LOGIN button")
    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON, description="LOGIN button")

    # ── State Queries ─────────────────────────────────────────────

    def is_error_visible(self) -> bool:
        """Return True if error banner is displayed."""
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_text(self) -> str:
        """Return the error message text (empty if no error)."""
        if self.is_error_visible():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_still_on_login_page(self) -> bool:
        """Return True if the login form is still visible."""
        return self.is_visible(self.LOGO)
