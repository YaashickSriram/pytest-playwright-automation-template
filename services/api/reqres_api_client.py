"""
reqres_api_client.py — Public API client example.

Uses ReqRes.in — a public dummy REST API for testing.
Demonstrates:
- BaseAPIClient inheritance
- Service-specific endpoint methods
- API key header injection
- Clear separation from base HTTP mechanics

Docs: https://reqres.in/
"""

from services.api.base_client import BaseAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class ReqResAPIClient(BaseAPIClient):
    """
    Client for the ReqRes.in public demo API.
    Inherits HTTP mechanics from BaseAPIClient.
    """

    def __init__(self, config: dict):
        """
        Args:
            config: api section from environment YAML
        """
        super().__init__(
            base_url=config["base_url"],
            timeout=config.get("timeout_seconds", 10)
        )
        api_key = config.get("api_key")
        if api_key:
            self.set_api_key("x-api-key", api_key)

    # ── Users Endpoints ───────────────────────────────────────────

    def list_users(self, page: int = 1) -> dict:
        """GET /users?page=N — list paginated users."""
        response = self.get("/users", params={"page": page})
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id: int) -> dict:
        """GET /users/{id} — get a single user."""
        response = self.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, name: str, job: str) -> dict:
        """POST /users — create a user."""
        response = self.post("/users", json_body={"name": name, "job": job})
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: int, name: str, job: str) -> dict:
        """PUT /users/{id} — update a user."""
        response = self.put(f"/users/{user_id}", json_body={"name": name, "job": job})
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: int) -> int:
        """DELETE /users/{id} — delete a user. Returns status code."""
        response = self.delete(f"/users/{user_id}")
        return response.status_code
