"""
Sauce Demo — Shopping Flow Test Suite
======================================
Reference implementation demonstrating:
- Multi-page workflow orchestration
- Compound business actions
- State assertions across pages
- Parametrized testing
"""

import pytest
import allure

from data.factories.product_factory import ProductFactory
from services.validators.base_validator import BaseValidator
from utils.logger import get_logger
from workflows.shopping_workflow import ShoppingWorkflow

logger = get_logger(__name__)


# ── Module Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def shopping_workflow(page, app_config):
    workflow = ShoppingWorkflow(page=page, app_config=app_config)
    # Pre-login as standard user — most shopping tests need an authenticated state
    workflow.login_and_open_inventory(role="standard")
    return workflow


@pytest.fixture(scope="module")
def product_factory():
    return ProductFactory()


@pytest.fixture(scope="module")
def validator():
    return BaseValidator()


# ══════════════════════════════════════════════════════════════════════════════
# Shopping Tests
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.shopping
@allure.feature("Shopping Cart")
@allure.story("Add Single Product")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_single_product_to_cart(shopping_workflow, product_factory, validator):
    """Adding one product updates the cart badge count to 1."""
    data = product_factory.single_product()
    product = data["products"][0]

    shopping_workflow.add_to_cart(product)
    cart_count = shopping_workflow.get_cart_badge_count()

    validator.assert_equal(
        actual=cart_count,
        expected=1,
        description=f"Cart badge must show 1 after adding '{product}'"
    )


@pytest.mark.critical
@pytest.mark.shopping
@allure.feature("Shopping Cart")
@allure.story("Add Multiple Products")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_multiple_products_to_cart(shopping_workflow, product_factory, validator):
    """Adding multiple products increments the cart badge correctly."""
    data = product_factory.multiple_products()
    product_count = len(data["products"])

    cart_count = shopping_workflow.add_products_and_view_cart(data["products"])

    validator.assert_equal(
        actual=cart_count,
        expected=product_count,
        description=f"Cart must contain exactly {product_count} items"
    )


@pytest.mark.regression
@pytest.mark.shopping
@allure.feature("Shopping Cart")
@allure.story("Remove Product")
@allure.severity(allure.severity_level.NORMAL)
def test_remove_product_from_cart(shopping_workflow, product_factory, validator):
    """Removing a product decrements the cart badge."""
    data = product_factory.multiple_products()
    products = data["products"]

    for p in products:
        shopping_workflow.add_to_cart(p)

    validator.assert_equal(
        actual=shopping_workflow.get_cart_badge_count(),
        expected=len(products),
        description="All products added initially"
    )

    shopping_workflow.remove_from_cart(products[0])

    validator.assert_equal(
        actual=shopping_workflow.get_cart_badge_count(),
        expected=len(products) - 1,
        description=f"Cart must show {len(products) - 1} after removal"
    )


@pytest.mark.regression
@pytest.mark.shopping
@allure.feature("Shopping Cart")
@allure.story("Cart Contents")
@allure.severity(allure.severity_level.NORMAL)
def test_cart_contains_added_products(shopping_workflow, product_factory, validator):
    """Products added appear on the cart page with correct names."""
    data = product_factory.multiple_products()

    shopping_workflow.add_products_and_view_cart(data["products"])
    cart_items = shopping_workflow.cart_page.get_item_names()

    for expected_product in data["products"]:
        validator.assert_in(
            member=expected_product,
            collection=cart_items,
            description=f"'{expected_product}' must appear in cart"
        )


@pytest.mark.regression
@pytest.mark.shopping
@allure.feature("Shopping Cart")
@allure.story("Add All Products")
@allure.severity(allure.severity_level.MINOR)
def test_add_all_catalog_products(shopping_workflow, product_factory, validator):
    """Adding every product in the catalog — stress scenario."""
    data = product_factory.all_products()

    cart_count = shopping_workflow.add_products_and_view_cart(data["products"])

    validator.assert_equal(
        actual=cart_count,
        expected=len(data["products"]),
        description="All catalog products must appear in cart"
    )


@pytest.mark.regression
@pytest.mark.shopping
@allure.feature("Shopping Cart")
@allure.story("Parametrized — Individual Products")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("product_name", ProductFactory.CATALOG)
def test_each_product_can_be_added(shopping_workflow, validator, product_name):
    """
    Parametrized: every product in the catalog can be individually added.
    One failure here points directly to the problematic product.
    """
    shopping_workflow.add_to_cart(product_name)
    validator.assert_equal(
        actual=shopping_workflow.get_cart_badge_count(),
        expected=1,
        description=f"'{product_name}' must add successfully"
    )
