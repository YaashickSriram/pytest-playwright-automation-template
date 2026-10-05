"""
inventory_page.py — Sauce Demo inventory (products) page.

Demonstrates:
- List-based locators
- Dynamic selectors derived from product name
- Count queries for business assertions
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.allure_helper import step
from utils.logger import get_logger

logger = get_logger(__name__)


class InventoryPage(BasePage):
    """
    Page Object for Sauce Demo inventory/products page.
    """

    # ── Locators ─────────────────────────────────────────────────
    PAGE_TITLE          = ".title"
    INVENTORY_CONTAINER = "#inventory_container"
    PRODUCT_ITEMS       = ".inventory_item"
    PRODUCT_NAMES       = ".inventory_item_name"
    CART_BADGE          = ".shopping_cart_badge"
    CART_LINK           = ".shopping_cart_link"
    SORT_DROPDOWN       = "[data-test='product-sort-container']"
    MENU_BUTTON         = "#react-burger-menu-btn"
    LOGOUT_LINK         = "#logout_sidebar_link"

    def __init__(self, page: Page, base_url: str = "", timeout_ms: int = 10000):
        super().__init__(page, base_url, timeout_ms)

    # ── Page State ───────────────────────────────────────────────

    @step("Wait for inventory page")
    def wait_for_page_load(self) -> None:
        """Wait for inventory container to load."""
        self.wait_for_element(self.INVENTORY_CONTAINER)
        logger.info("Inventory page loaded")

    def is_on_inventory_page(self) -> bool:
        """Return True if on the inventory page."""
        return "inventory.html" in self.get_current_url()

    # ── Actions ──────────────────────────────────────────────────

    @step("Add product to cart")
    def add_product_to_cart(self, product_name: str) -> None:
        """
        Add a product to cart by its visible name.
        Dynamically derives the Add to Cart button selector.
        """
        # Sauce Demo button ID pattern: add-to-cart-<kebab-case-name>
        kebab = product_name.lower().replace(" ", "-").replace(".", "")
        selector = f"[data-test='add-to-cart-{kebab}']"
        logger.info(f"Adding '{product_name}' to cart")
        self.click(selector, description=f"Add '{product_name}' to cart")

    @step("Remove product from cart")
    def remove_product_from_cart(self, product_name: str) -> None:
        """Remove a product from cart by its visible name."""
        kebab = product_name.lower().replace(" ", "-").replace(".", "")
        selector = f"[data-test='remove-{kebab}']"
        logger.info(f"Removing '{product_name}' from cart")
        self.click(selector, description=f"Remove '{product_name}' from cart")

    @step("Open shopping cart")
    def open_cart(self) -> None:
        self.click(self.CART_LINK, description="Shopping cart")

    @step("Sort products")
    def sort_by(self, option_value: str) -> None:
        """
        Sort products. Valid values:
          az — Name A to Z
          za — Name Z to A
          lohi — Price low to high
          hilo — Price high to low
        """
        self.select_option(self.SORT_DROPDOWN, option_value)

    @step("Log out")
    def logout(self) -> None:
        self.click(self.MENU_BUTTON, description="Menu")
        self.wait_for_element(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK, description="Logout link")

    # ── State Queries ─────────────────────────────────────────────

    def get_product_count(self) -> int:
        """Return the number of products visible."""
        return self.count_elements(self.PRODUCT_ITEMS)

    def get_cart_count(self) -> int:
        """Return the number of items in the cart (from the badge)."""
        if not self.is_visible(self.CART_BADGE, timeout_ms=1000):
            return 0
        try:
            return int(self.get_text(self.CART_BADGE))
        except (ValueError, TypeError):
            return 0

    def get_all_product_names(self) -> list:
        """Return all product names on the page."""
        return self.get_all_text_contents(self.PRODUCT_NAMES)
