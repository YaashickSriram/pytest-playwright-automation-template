"""
base_workflow.py — Foundation for business workflow orchestrators.

A workflow composes multiple page actions into a business-readable sequence.
Workflows know the ORDER of steps. Pages know HOW to interact with the DOM.

Rule: Workflows do not own selectors. They call page objects.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseWorkflow:
    """
    Parent class for all business workflow orchestrators.
    Provides access to app_config, base_url, user credentials,
    and step-level logging.
    """

    def __init__(self, page: Page, app_config: dict):
        self.page = page
        self.app_config = app_config
        self.base_url = app_config.get("base_url", "")
        self.timeout_ms = app_config.get("timeout_ms", 10000)

        # Composition — not inheritance
        self.base_page = BasePage(
            page=page,
            base_url=self.base_url,
            timeout_ms=self.timeout_ms
        )

    def get_user_credentials(self, role: str) -> dict:
        """
        Retrieve credentials for a named role from config.

        Args:
            role: Role name (e.g. 'standard', 'admin', 'approver')

        Returns:
            dict with 'username' and 'password' keys
        """
        users = self.app_config.get("users", {})
        creds = users.get(role)
        if not creds:
            raise ValueError(
                f"Role '{role}' not found in config.\n"
                f"Available roles: {list(users.keys())}\n"
                f"Add the role to config/environments/<env>.yaml"
            )
        return creds

    def log_step(self, message: str) -> None:
        """Log a workflow-level step marker for traceability."""
        logger.info(f"WORKFLOW STEP → {message}")
