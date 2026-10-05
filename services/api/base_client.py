"""
base_client.py — Generic HTTP client base.

Provides reusable session management, auth header injection,
JSON handling, and automatic Allure attachment of API payloads.

Rule: API-specific clients inherit from this. No business logic here.
"""

import requests
import json

from utils.allure_helper import attach_json, step
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseAPIClient:
    """
    Base HTTP client with session reuse and Allure integration.
    Subclass this for service-specific API clients.
    """

    def __init__(self, base_url: str, timeout: int = 10, headers: dict = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        logger.info(f"API client initialised — base: {self.base_url}")

    # ── Core HTTP Methods ─────────────────────────────────────────

    @step("API GET request")
    def get(self, endpoint: str, params: dict = None, **kwargs) -> requests.Response:
        """Send authenticated GET request."""
        return self._request("GET", endpoint, params=params, **kwargs)

    @step("API POST request")
    def post(self, endpoint: str, json_body: dict = None, **kwargs) -> requests.Response:
        """Send authenticated POST request with JSON body."""
        return self._request("POST", endpoint, json=json_body, **kwargs)

    @step("API PUT request")
    def put(self, endpoint: str, json_body: dict = None, **kwargs) -> requests.Response:
        """Send authenticated PUT request."""
        return self._request("PUT", endpoint, json=json_body, **kwargs)

    @step("API DELETE request")
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Send authenticated DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)

    # ── Internal Request Handler ──────────────────────────────────

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Central request handler. Logs the call, attaches request/response
        to Allure, and returns the raw response.
        """
        url = f"{self.base_url}{endpoint}" if endpoint.startswith("/") else endpoint
        logger.info(f"{method} {url}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            self._attach_response(method, url, response)
            logger.info(f"Response: {response.status_code}")
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def _attach_response(self, method: str, url: str, response: requests.Response) -> None:
        """Attach request/response details to the current Allure step."""
        try:
            body = response.json()
            attach_json(
                f"{method} {url} — {response.status_code}",
                json.dumps(body, indent=2)
            )
        except (ValueError, json.JSONDecodeError):
            # Non-JSON response — skip attachment
            pass

    # ── Auth Helpers ──────────────────────────────────────────────

    def set_bearer_token(self, token: str) -> None:
        """Set Authorization: Bearer <token> on all subsequent requests."""
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.info("Bearer token set on session")

    def set_api_key(self, header_name: str, api_key: str) -> None:
        """Set a custom API key header on all subsequent requests."""
        self.session.headers[header_name] = api_key
        logger.info(f"API key header set: {header_name}")
