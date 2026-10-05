"""
login_workflow.py — Sauce Demo login workflow orchestration.

Demonstrates:
- Composition over inheritance (workflow holds page objects)
- Business-level methods (login, logout) that tests call
- Multi-step actions compressed into single calls
"""

from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.allure_helper import step
from utils.logger import get_logger
from workflows.base_workflow import BaseWorkflow

logger = get_logger(__name__)


class LoginWorkflow(BaseWorkflow):
    """
    Orchestrates login and session-related business flows.
    """

    def __init__(self, page: Page, app_config: dict):
        super().__init__(page, app_config)
        self.login_page = LoginPage(page, base_url=self.base_url, timeout_ms=self.timeout_ms)
        self.inventory_page = InventoryPage(page, base_url=self.base_url, timeout_ms=self.timeout_ms)

    @step("Navigate to login page")
    def navigate_to_login(self) -> None:
        """Navigate to the login page and wait for it to be ready."""
        self.log_step("Navigating to login page")
        self.base_page.navigate("/")
        self.login_page.wait_for_page_load()

    @step("Submit login credentials")
    def submit_credentials(self, username: str, password: str) -> None:
        """Enter credentials and click LOGIN."""
        self.log_step(f"Submitting credentials for: {username}")
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()

    @step("Perform full login and land on inventory")
    def login(self, username: str, password: str) -> None:
        """
        Complete login flow — navigate, submit, wait for inventory.
        Use this for happy-path tests.
        """
        self.navigate_to_login()
        self.submit_credentials(username, password)
        self.inventory_page.wait_for_page_load()
        logger.info(f"Login successful for user: {username}")

    @step("Log out from current session")
    def logout(self) -> None:
        """Log out from the application."""
        self.inventory_page.logout()
        self.login_page.wait_for_page_load()
        logger.info("Logged out successfully")

    def is_on_inventory_page(self) -> bool:
        """Return True if currently on the inventory (post-login) page."""
        return self.inventory_page.is_on_inventory_page()

    def is_on_login_page(self) -> bool:
        """Return True if currently on the login page."""
        return self.login_page.is_still_on_login_page()
