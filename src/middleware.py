"""OIDC Authentication Middleware."""

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.authentication import AbstractAuthenticationMiddleware, AuthenticationResult
from src.oidc import OIDCAuthConfig


class OIDCAuthMiddleware(AbstractAuthenticationMiddleware):
    def __init__(self, app, config: OIDCAuthConfig) -> None:
        super().__init__(app)
        self.config = config

    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        # Authenticate request using OIDC
        token = connection.headers.get("Authorization")
        if not token:
            msg = "No token provided"
            raise NotAuthorizedException(msg)

        try:
            # Validate token and get user info
            user_info = await self.config.oauth_client.parse_id_token(token)
            user = await self.config.retrieve_user_handler(user_info, connection)
            return AuthenticationResult(user=user, auth=token)
        except Exception as e:  # noqa: BLE001
            msg = f"Authentication failed: {e}"
            raise NotAuthorizedException(msg) from e
