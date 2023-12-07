"""OIDC Client."""
from __future__ import annotations

from urllib.parse import urlencode

import httpx


class OIDCClient:
    def __init__(self, discovery_url, client_id, client_secret, redirect_uri) -> None:
        self.discovery_url = discovery_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.provider_config = {}

    async def discover(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.discovery_url)
            self.provider_config = response.json()

    def build_auth_request(self, scope="openid", response_type="code", state=None, nonce=None):
        params = {
            "response_type": response_type,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": state,
            "nonce": nonce,
        }
        return f"{self.provider_config['authorization_endpoint']}?{urlencode(params)}"

    async def fetch_token(self, code):
        token_endpoint = self.provider_config.get("token_endpoint")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(token_endpoint, data=data)
            return response.json()

    async def get_userinfo(self, access_token):
        userinfo_endpoint = self.provider_config.get("userinfo_endpoint")
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(userinfo_endpoint, headers=headers)
            return response.json()
