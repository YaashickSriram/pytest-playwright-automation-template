"""
product_factory.py — Sauce Demo product data factory.

Demonstrates:
- Static product catalog as factory data
- Named scenarios for test combinations
"""

from data.factories.base_factory import BaseFactory
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductFactory(BaseFactory):
    """
    Produces product name contracts for shopping scenarios.
    Product names match Sauce Demo's exact catalog.
    """

    # Sauce Demo product catalog (exact names as they appear in the UI)
    CATALOG = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]

    def build(self, **overrides) -> dict:
        """Return the backpack as default product scenario."""
        data = {
            "product_name": "Sauce Labs Backpack",
            "quantity": 1
        }
        data.update(overrides)
        return data

    def single_product(self) -> dict:
        """One product scenario."""
        return {"products": ["Sauce Labs Backpack"]}

    def multiple_products(self) -> dict:
        """Multiple product scenario — 3 items."""
        return {
            "products": [
                "Sauce Labs Backpack",
                "Sauce Labs Bike Light",
                "Sauce Labs Fleece Jacket"
            ]
        }

    def all_products(self) -> dict:
        """Add every product in the catalog."""
        return {"products": list(self.CATALOG)}

    def expensive_product(self) -> dict:
        """Highest priced single product."""
        return {"products": ["Sauce Labs Fleece Jacket"]}
