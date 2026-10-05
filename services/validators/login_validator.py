"""
login_validator.py — Business-specific validators for login flows.

Demonstrates:
- BaseValidator inheritance
- Business-named assertion methods
- Structured error reporting
"""

from services.validators.base_validator import BaseValidator
from utils.allure_helper import attach_text
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginValidator(BaseValidator):
    """
    Structured assertions for login-related business rules.
    """

    def assert_logged_in(self, login_workflow, description: str = "") -> None:
        """Assert the user is logged in and on the inventory page."""
        label = description or "User must be on inventory page after login"
        on_inventory = login_workflow.is_on_inventory_page()
        attach_text(
            "Login State Check",
            f"On inventory page : {on_inventory}\n"
            f"Current URL       : {login_workflow.page.url}"
        )
        self.assert_true(on_inventory, label)

    def assert_login_failed(self, login_workflow, description: str = "") -> None:
        """Assert login failed — user still on login page."""
        label = description or "Login must fail — user remains on login page"
        on_login = login_workflow.is_on_login_page()
        attach_text(
            "Login Failure Check",
            f"Still on login : {on_login}\n"
            f"Current URL    : {login_workflow.page.url}"
        )
        self.assert_true(on_login, label)

    def assert_error_message_contains(
        self, login_workflow, expected_text: str, description: str = ""
    ) -> None:
        """Assert error banner contains expected text."""
        error_text = login_workflow.login_page.get_error_text()
        label = description or f"Error message must contain: '{expected_text}'"
        attach_text(
            "Error Message Check",
            f"Expected contains : {expected_text}\n"
            f"Actual error      : {error_text}"
        )
        self.assert_contains(error_text, expected_text, label)
