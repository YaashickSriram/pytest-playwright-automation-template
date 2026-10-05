"""
Sauce Demo — Login Authentication Test Suite
=============================================
Reference implementation demonstrating:
- Full framework stack: fixtures, workflows, validators, factories
- Allure feature/story/severity annotations
- Positive, negative, and edge case scenarios
- Clean separation: test = business intent only
"""

import pytest
import allure

from data.factories.user_factory import UserFactory
from services.validators.login_validator import LoginValidator
from utils.logger import get_logger
from workflows.login_workflow import LoginWorkflow

logger = get_logger(__name__)


# ── Module Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def login_workflow(page, app_config):
    return LoginWorkflow(page=page, app_config=app_config)


@pytest.fixture(scope="module")
def user_factory(app_config):
    return UserFactory(app_config=app_config)


@pytest.fixture(scope="module")
def validator():
    return LoginValidator()


# ══════════════════════════════════════════════════════════════════════════════
# Login Tests
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
@allure.feature("Login Authentication")
@allure.story("Happy Path — Standard User")
@allure.severity(allure.severity_level.CRITICAL)
def test_standard_user_can_login(login_workflow, user_factory, validator):
    """
    Standard user logs in with valid credentials.
    System must land on the inventory page.
    """
    user = user_factory.standard_user()
    login_workflow.login(user["username"], user["password"])
    validator.assert_logged_in(login_workflow)


@pytest.mark.critical
@pytest.mark.login
@allure.feature("Login Authentication")
@allure.story("Account Locked")
@allure.severity(allure.severity_level.CRITICAL)
def test_locked_user_cannot_login(login_workflow, user_factory, validator):
    """
    Locked user attempts to log in.
    System must show error and keep user on login page.
    """
    user = user_factory.locked_user()
    login_workflow.navigate_to_login()
    login_workflow.submit_credentials(user["username"], user["password"])

    validator.assert_login_failed(login_workflow)
    validator.assert_error_message_contains(
        login_workflow,
        "locked out"
    )


@pytest.mark.regression
@pytest.mark.login
@allure.feature("Login Authentication")
@allure.story("Invalid Credentials")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_credentials_rejected(login_workflow, user_factory, validator):
    """Invalid username and password combination must be rejected."""
    user = user_factory.invalid_credentials()
    login_workflow.navigate_to_login()
    login_workflow.submit_credentials(user["username"], user["password"])

    validator.assert_login_failed(login_workflow)
    validator.assert_error_message_contains(
        login_workflow,
        "do not match"
    )


@pytest.mark.regression
@pytest.mark.login
@allure.feature("Login Authentication")
@allure.story("Empty Credentials — Validation")
@allure.severity(allure.severity_level.NORMAL)
def test_empty_credentials_shows_error(login_workflow, user_factory, validator):
    """Submitting empty credentials must show a required-field error."""
    user = user_factory.empty_credentials()
    login_workflow.navigate_to_login()
    login_workflow.submit_credentials(user["username"], user["password"])

    validator.assert_login_failed(login_workflow)
    validator.assert_error_message_contains(
        login_workflow,
        "Username is required"
    )


@pytest.mark.regression
@pytest.mark.login
@allure.feature("Login Authentication")
@allure.story("Session — Logout")
@allure.severity(allure.severity_level.NORMAL)
def test_user_can_logout(login_workflow, user_factory, validator):
    """
    After successful login, user can log out and returns to login page.
    """
    user = user_factory.standard_user()
    login_workflow.login(user["username"], user["password"])
    validator.assert_logged_in(login_workflow)

    login_workflow.logout()
    validator.assert_login_failed(
        login_workflow,
        "After logout, user must be returned to login page"
    )
