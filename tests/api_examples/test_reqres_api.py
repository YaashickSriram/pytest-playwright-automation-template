"""
ReqRes.in Public API — Test Suite
==================================
Reference implementation demonstrating:
- API client inheritance from BaseAPIClient
- No browser required — pure HTTP tests
- Config-driven endpoint and auth setup
- Allure integration for API tests

API: https://reqres.in/
"""

import pytest
import allure

from services.api.reqres_api_client import ReqResAPIClient
from services.validators.base_validator import BaseValidator
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Module Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def api_client(app_config):
    api_config = app_config.get("api", {})
    return ReqResAPIClient(config=api_config)


@pytest.fixture(scope="module")
def validator():
    return BaseValidator()


# ══════════════════════════════════════════════════════════════════════════════
# API Tests
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.api
@allure.feature("Users API")
@allure.story("List Users — Happy Path")
@allure.severity(allure.severity_level.CRITICAL)
def test_list_users_returns_data(api_client, validator):
    """GET /users?page=1 returns a paginated list of users."""
    result = api_client.list_users(page=1)

    validator.assert_not_empty(result.get("data"), "User list must not be empty")
    validator.assert_true(
        condition=len(result["data"]) > 0,
        description="At least one user must be returned"
    )


@pytest.mark.critical
@pytest.mark.api
@allure.feature("Users API")
@allure.story("Get Single User")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_user_by_id(api_client, validator):
    """GET /users/2 returns the user with id=2."""
    result = api_client.get_user(user_id=2)
    user = result.get("data", {})

    validator.assert_equal(
        actual=user.get("id"),
        expected=2,
        description="User id must match requested value"
    )
    validator.assert_not_empty(user.get("email"), "User must have an email")


@pytest.mark.regression
@pytest.mark.api
@allure.feature("Users API")
@allure.story("Create User")
@allure.severity(allure.severity_level.NORMAL)
def test_create_user(api_client, validator):
    """POST /users creates a new user and returns id + createdAt."""
    result = api_client.create_user(name="Framework Demo", job="QA Engineer")

    validator.assert_not_empty(result.get("id"), "Response must include generated id")
    validator.assert_equal(
        actual=result.get("name"),
        expected="Framework Demo",
        description="Returned name must match input"
    )


@pytest.mark.regression
@pytest.mark.api
@allure.feature("Users API")
@allure.story("Update User")
@allure.severity(allure.severity_level.NORMAL)
def test_update_user(api_client, validator):
    """PUT /users/2 updates and returns updatedAt timestamp."""
    result = api_client.update_user(user_id=2, name="Updated Name", job="Senior QA")

    validator.assert_not_empty(result.get("updatedAt"), "Response must include updatedAt")
    validator.assert_equal(
        actual=result.get("job"),
        expected="Senior QA",
        description="Returned job must match input"
    )


@pytest.mark.regression
@pytest.mark.api
@allure.feature("Users API")
@allure.story("Delete User")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_user(api_client, validator):
    """DELETE /users/2 returns 204 No Content."""
    status = api_client.delete_user(user_id=2)
    validator.assert_equal(
        actual=status,
        expected=204,
        description="DELETE must return 204 No Content"
    )
