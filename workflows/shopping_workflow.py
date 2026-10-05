"""
shopping_workflow.py — Sauce Demo shopping flow orchestration.

Demonstrates:
- Multi-page workflow (inventory → cart → checkout)
- Compound business actions
- Composition of multiple page objects
"""

from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from utils.allure_helper import step
from utils.logger import get_logger
from workflows.base_workflow import BaseWorkflow
from workflows.login_workflow import LoginWorkflow

logger = get_logger(__name__)


class ShoppingWorkflow(BaseWorkflow):
    """
    Orchestrates shopping-related business flows.
    """

    def __init__(self, page: Page, app_config: dict):
        super().__init__(page, app_config)
        self.inventory_page = InventoryPage(page, base_url=self.base_url, timeout_ms=self.timeout_ms)
        self.cart_page = CartPage(page, base_url=self.base_url, timeout_ms=self.timeout_ms)
        self.login_workflow = LoginWorkflow(page, app_config)

    @step("Login and open inventory")
    def login_and_open_inventory(self, role: str = "standard") -> None:
        """Login with a named role and ensure inventory is loaded."""
        creds = self.get_user_credentials(role)
        self.login_workflow.login(creds["username"], creds["password"])

    @step("Add product to cart")
    def add_to_cart(self, product_name: str) -> None:
        """Add a product by name — assumes inventory page is loaded."""
        self.log_step(f"Adding product: {product_name}")
        self.inventory_page.add_product_to_cart(product_name)

    @step("Remove product from cart")
    def remove_from_cart(self, product_name: str) -> None:
        """Remove a product from cart — assumes inventory page is loaded."""
        self.log_step(f"Removing product: {product_name}")
        self.inventory_page.remove_product_from_cart(product_name)

    @step("Open cart page")
    def view_cart(self) -> None:
        """Navigate to the cart page."""
        self.inventory_page.open_cart()
        self.cart_page.wait_for_page_load()

    @step("Add multiple products and view cart")
    def add_products_and_view_cart(self, product_names: list) -> int:
        """
        Add multiple products in sequence and open the cart.
        Returns the final cart count for assertion.
        """
        for name in product_names:
            self.add_to_cart(name)
        self.view_cart()
        return self.cart_page.get_item_count()

    def get_cart_badge_count(self) -> int:
        """Return current cart badge count from inventory page."""
        return self.inventory_page.get_cart_count()
