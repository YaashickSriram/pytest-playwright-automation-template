"""
base_factory.py — Foundation for test data factories.

A factory builds structured data contracts (dicts) that tests consume.
No test should hardcode credentials, invoice numbers, user data, etc.

Rule: Factories produce data. Tests use data. No overlap.
"""

import json
import random
import string
from datetime import datetime
from pathlib import Path

from data import fixtures as _fixtures_pkg
from utils.logger import get_logger

logger = get_logger(__name__)

FIXTURES_ROOT = Path(_fixtures_pkg.__file__).parent if hasattr(_fixtures_pkg, "__file__") else None


class BaseFactory:
    """
    Parent class for all test data factories.
    Subclasses implement build() with their specific data contract.
    """

    def build(self, **overrides) -> dict:
        """
        Must be overridden by subclasses.
        Returns a dict representing one test data scenario.
        """
        raise NotImplementedError(
            "Factory subclasses must implement build().\n"
            "Example: def build(self, **overrides) -> dict: ..."
        )

    def build_batch(self, count: int, **overrides) -> list:
        """
        Build multiple instances of the data contract.

        Args:
            count: Number of instances to generate
            **overrides: Fields to override in every instance
        """
        return [self.build(**overrides) for _ in range(count)]

    def load_fixture(self, fixture_name: str) -> dict:
        """
        Load a static JSON fixture file from data/fixtures/.

        Args:
            fixture_name: Relative path under data/fixtures/
                          e.g. 'users/admin.json'

        Returns:
            Parsed JSON content as a dict
        """
        if FIXTURES_ROOT is None:
            raise FileNotFoundError("Fixtures root not resolved")

        fixture_path = FIXTURES_ROOT / fixture_name
        if not fixture_path.exists():
            raise FileNotFoundError(f"Fixture not found: {fixture_path}")

        with open(fixture_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"Fixture loaded: {fixture_name}")
        return data

    # ── Random Data Generators ────────────────────────────────────

    @staticmethod
    def random_string(length: int = 8) -> str:
        """Generate a random alphanumeric string."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_email(domain: str = "test-domain.com") -> str:
        """Generate a random test email address."""
        prefix = BaseFactory.random_string(6)
        return f"test_{prefix}@{domain}"

    @staticmethod
    def timestamp() -> str:
        """Return current timestamp as a filename-safe string."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
