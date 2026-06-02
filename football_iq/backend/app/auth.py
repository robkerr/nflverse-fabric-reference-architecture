"""Entra ID token validation and OBO exchange for Fabric SQL access."""

from __future__ import annotations

import struct
from typing import Any

import msal
from fastapi import Depends, HTTPException, Request

from app.config import settings

FABRIC_SQL_SCOPE = "https://database.windows.net/.default"

_confidential_app: msal.ConfidentialClientApplication | None = None


def get_msal_app() -> msal.ConfidentialClientApplication:
    global _confidential_app
    if _confidential_app is None:
        _confidential_app = msal.ConfidentialClientApplication(
            client_id=settings.azure_client_id,
            client_credential=settings.azure_client_secret,
            authority=f"https://login.microsoftonline.com/{settings.azure_tenant_id}",
        )
    return _confidential_app


def extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return auth_header[7:]


def get_fabric_token_obo(request: Request) -> str:
    """Exchange the user's access token for a Fabric SQL-scoped token via OBO."""
    user_token = extract_bearer_token(request)
    app = get_msal_app()

    result = app.acquire_token_on_behalf_of(
        user_assertion=user_token,
        scopes=[FABRIC_SQL_SCOPE],
    )

    if "access_token" not in result:
        error = result.get("error_description", result.get("error", "Unknown OBO error"))
        raise HTTPException(status_code=401, detail=f"OBO token exchange failed: {error}")

    return result["access_token"]


def build_token_struct(access_token: str) -> bytes:
    """Build the SQL Server access token struct for pyodbc attrs_before."""
    token_bytes = access_token.encode("UTF-16-LE")
    return struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
