"""
base_validator.py — Structured assertion engine.

Every assertion logs ✓ PASS or ✗ FAIL with expected vs actual values
and attaches evidence to the Allure report before raising.

Rule: Tests should use these methods instead of raw assert statements.
"""

from utils.allure_helper import attach_text
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseValidator:
    """
    Structured assertion base class.
    Each method logs the comparison and attaches evidence to Allure.
    """

    # ── Equality Assertions ───────────────────────────────────────

    def assert_equal(self, actual, expected, description: str = "") -> None:
        """Assert actual == expected."""
        label = description or f"Expected {expected} but got {actual}"
        attach_text(
            "Equality Check",
            f"Expected : {expected}\n"
            f"Actual   : {actual}"
        )
        if actual == expected:
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label} — got {actual}, expected {expected}")
            raise AssertionError(f"{label} — got {actual}, expected {expected}")

    def assert_not_equal(self, actual, expected, description: str = "") -> None:
        """Assert actual != expected."""
        label = description or f"Values must differ but both are {actual}"
        attach_text(
            "Inequality Check",
            f"Value A : {actual}\n"
            f"Value B : {expected}"
        )
        if actual != expected:
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label}")
            raise AssertionError(label)

    # ── Boolean Assertions ────────────────────────────────────────

    def assert_true(self, condition: bool, description: str = "") -> None:
        """Assert condition is True."""
        label = description or "Condition must be true"
        if condition:
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label} — condition evaluated to False")
            raise AssertionError(f"{label} — condition evaluated to False")

    def assert_false(self, condition: bool, description: str = "") -> None:
        """Assert condition is False."""
        label = description or "Condition must be false"
        if not condition:
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label} — condition evaluated to True")
            raise AssertionError(f"{label} — condition evaluated to True")

    # ── String Assertions ─────────────────────────────────────────

    def assert_contains(self, haystack: str, needle: str, description: str = "") -> None:
        """Assert needle is a substring of haystack."""
        label = description or f"'{haystack}' must contain '{needle}'"
        attach_text(
            "Contains Check",
            f"Haystack : {haystack}\n"
            f"Needle   : {needle}"
        )
        if needle in str(haystack):
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label}")
            raise AssertionError(label)

    def assert_not_contains(self, haystack: str, needle: str, description: str = "") -> None:
        """Assert needle is NOT a substring of haystack."""
        label = description or f"'{haystack}' must not contain '{needle}'"
        if needle not in str(haystack):
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label}")
            raise AssertionError(label)

    # ── Collection Assertions ─────────────────────────────────────

    def assert_not_empty(self, value, description: str = "") -> None:
        """Assert value is not None and not empty."""
        label = description or "Value must not be empty"
        if value:
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label} — got: {value}")
            raise AssertionError(f"{label} — got: {value}")

    def assert_in(self, member, collection, description: str = "") -> None:
        """Assert member is in collection."""
        label = description or f"'{member}' must be in collection"
        attach_text(
            "Membership Check",
            f"Member     : {member}\n"
            f"Collection : {collection}"
        )
        if member in collection:
            logger.info(f"✓ PASS — {label}")
        else:
            logger.error(f"✗ FAIL — {label}")
            raise AssertionError(label)

    def assert_count(self, collection, expected_count: int, description: str = "") -> None:
        """Assert collection has exactly the expected number of items."""
        actual = len(collection)
        label = description or f"Collection must have {expected_count} items"
        if actual == expected_count:
            logger.info(f"✓ PASS — {label} (actual: {actual})")
        else:
            logger.error(f"✗ FAIL — {label} — got {actual}")
            raise AssertionError(f"{label} — got {actual}, expected {expected_count}")
