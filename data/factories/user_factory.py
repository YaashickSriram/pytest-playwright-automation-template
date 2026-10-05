"""
user_factory.py — Sauce Demo user credential factory.

Demonstrates:
- Config-driven credential building (no hardcoded passwords)
- Named scenarios for different test personas
- BaseFactory pattern
"""

from data.factories.base_factory import BaseFactory
from utils.logger import get_logger

logger = get_logger(__name__)


class UserFactory(BaseFactory):
    """
    Produces user credential contracts for Sauce Demo scenarios.
    All credentials come from app_config — never hardcoded.
    """

    def __init__(self, app_config: dict):
        self.users = app_config.get("users", {})

    def build(self, **overrides) -> dict:
        """Return the standard user by default."""
        data = self.standard_user()
        data.update(overrides)
        return data

    def standard_user(self) -> dict:
        """Valid Sauce Demo user — happy path tests."""
        return {
            "username": self.users.get("standard", {}).get("username"),
            "password": self.users.get("standard", {}).get("password"),
            "role": "standard"
        }

    def locked_user(self) -> dict:
        """Locked out user — negative scenario."""
        return {
            "username": self.users.get("locked", {}).get("username"),
            "password": self.users.get("locked", {}).get("password"),
            "role": "locked"
        }

    def problem_user(self) -> dict:
        """Problem user — demonstrates bug-prone UI."""
        return {
            "username": self.users.get("problem", {}).get("username"),
            "password": self.users.get("problem", {}).get("password"),
            "role": "problem"
        }

    def performance_user(self) -> dict:
        """Performance glitch user — slow UI."""
        return {
            "username": self.users.get("performance", {}).get("username"),
            "password": self.users.get("performance", {}).get("password"),
            "role": "performance"
        }

    def invalid_credentials(self) -> dict:
        """Non-existent user — authentication failure."""
        return {
            "username": "invalid_user",
            "password": "wrong_password",
            "role": "invalid"
        }

    def empty_credentials(self) -> dict:
        """Empty credentials — form validation."""
        return {
            "username": "",
            "password": "",
            "role": "empty"
        }
