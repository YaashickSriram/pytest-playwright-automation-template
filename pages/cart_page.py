"""
cart_page.py — Sauce Demo cart page.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.allure_helper import step
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Page Object for the shopping cart page."""

    # ── Locators ─────────────────────────────────────────────────
    CART_CONTAINER   = "#cart_contents_container"
    CART_ITEMS       = ".cart_item"
    ITEM_NAMES       = ".inventory_item_name"
    CHECKOUT_BUTTON  = "#checkout"
    CONTINUE_SHOPPING = "#continue-shopping"

    def __init__(self, page: Page, base_url: str = "", timeout_ms: int = 10000):
        super().__init__(page, base_url, timeout_ms)

    @step("Wait for cart page")
    def wait_for_page_load(self) -> None:
        self.wait_for_element(self.CART_CONTAINER)
        logger.info("Cart page loaded")

    def is_on_cart_page(self) -> bool:
        return "cart.html" in self.get_current_url()

    def get_item_count(self) -> int:
        return self.count_elements(self.CART_ITEMS)

    def get_item_names(self) -> list:
        return self.get_all_text_contents(self.ITEM_NAMES)

    @step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON, description="Checkout")

    @step("Continue shopping")
    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING, description="Continue shopping")
