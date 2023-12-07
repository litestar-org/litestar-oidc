"""OIDC Configuration."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from litestar.middleware.base import DefineMiddleware
from litestar.openapi.spec import Components, SecurityRequirement
from litestar.security.base import AbstractSecurityConfig
from src.middleware import OIDCAuthMiddleware

if TYPE_CHECKING:
    from authlib.integrations.httpx_client import OAuth2Client


class OIDCAuthConfig(AbstractSecurityConfig):
    """OIDC Authentication class."""

    def __init__(self, oauth_client: OAuth2Client, retrieve_user: Callable[..., Any]) -> None:
        self.oauth_client = oauth_client
        self.retrieve_user = retrieve_user

    @property
    def openapi_components(self) -> Components:
        # Implement OIDC specific OpenAPI components
        return Components(...)

    @property
    def security_requirement(self) -> SecurityRequirement:
        # Implement OIDC specific security requirements
        return SecurityRequirement(...)

    @property
    def middleware(self) -> DefineMiddleware:
        # Implement middleware to handle OIDC authentication
        return DefineMiddleware(OIDCAuthMiddleware, config=self)

    async def retrieve_user_handler(self, token_info: dict, connection: Any) -> Any:
        # Retrieve user information from OIDC token
        return await self.retrieve_user(token_info)
