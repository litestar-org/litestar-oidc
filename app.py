from __future__ import annotations

from src.client import OIDCClient
from src.oidc import OIDCAuthConfig

from litestar import Litestar

oidc_client = OIDCClient(
    discovery_url="http://localhost:4004/auth/oidc",
    client_id="client-id",
    client_secret="cl-secret",
    redirect_uri="http://localhost:3000/callback",
)


async def retrieve_user(token_info) -> dict:
    user_id = token_info.get("sub")

    return {
        "id": user_id,
        "name": token_info.get("name"),
        "email": token_info.get("email"),
    }


oidc_auth_config = OIDCAuthConfig(oauth_client=oauth_client_that_doesnt_exist, retrieve_user=retrieve_user)

app = Litestar(middleware=[oidc_auth_config.middleware])
