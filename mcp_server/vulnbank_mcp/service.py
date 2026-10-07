import os

import httpx
from dotenv import load_dotenv


load_dotenv()


class VulnBankService:

    def __init__(self):
        self.base_url = os.getenv(
            "VULNBANK_BASE_URL",
            "http://localhost:5000"
        )

        self.api_key = os.getenv(
            "VULNBANK_MCP_API_KEY"
        )

        self.client = httpx.Client(
            base_url=self.base_url,
            follow_redirects=True,
            timeout=10
        )

        self.authenticated = False

    def authenticate(self, api_key: str) -> dict:

        if not self.api_key:
            return {
                "authenticated": False,
                "error": (
                    "Server has no "
                    "VULNBANK_MCP_API_KEY configured."
                )
            }

        if api_key == self.api_key:
            self.authenticated = True

            return {
                "authenticated": True
            }

        return {
            "authenticated": False,
            "error": "Invalid API key."
        }

    def require_auth(self):

        if not self.authenticated:
            raise PermissionError(
                "Not authenticated. "
                "Call authenticate(api_key=...) first."
            )

    def login(
        self,
        username: str,
        password: str
    ) -> dict:

        self.require_auth()

        response = self.client.post(
            "/login",
            data={
                "username": username,
                "password": password
            }
        )

        logged_in = "login" not in response.url.path

        return {
            "status_code": response.status_code,
            "logged_in": logged_in,
            "body": response.text[:1000]
        }

    def get_dashboard(self) -> dict:

        self.require_auth()

        response = self.client.get("/dashboard")

        return {
            "status_code": response.status_code,
            "body": response.text[:3000]
        }

    def get_account(
        self,
        account_id: int
    ) -> dict:

        self.require_auth()

        response = self.client.get(
            f"/account/{account_id}"
        )

        return {
            "status_code": response.status_code,
            "body": response.text[:3000]
        }

    def transfer_funds(
        self,
        to_account: int,
        amount: float
    ) -> dict:

        self.require_auth()

        response = self.client.post(
            "/transfer",
            data={
                "to_account": to_account,
                "amount": amount
            }
        )

        return {
            "status_code": response.status_code,
            "body": response.text[:1000]
        }

    def get_admin_panel(self) -> dict:

        self.require_auth()

        response = self.client.get("/admin")

        return {
            "status_code": response.status_code,
            "body": response.text[:3000]
        }