"""Fabric SQL endpoint connection and query execution."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator

import pyodbc

from app.auth import build_token_struct
from app.config import settings

SQL_COPT_SS_ACCESS_TOKEN = 1256

DRIVER = "{ODBC Driver 18 for SQL Server}"


@contextmanager
def fabric_connection(access_token: str) -> Generator[pyodbc.Connection, None, None]:
    """Open a pyodbc connection to Fabric SQL using the OBO access token."""
    conn_str = (
        f"Driver={DRIVER};"
        f"Server={settings.fabric_sql_server},1433;"
        f"Database={settings.fabric_sql_database};"
        "Encrypt=Yes;"
        "TrustServerCertificate=No;"
    )
    token_struct = build_token_struct(access_token)
    conn = pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    try:
        yield conn
    finally:
        conn.close()


def execute_query(access_token: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    """Execute a read-only query and return results as list of dicts."""
    with fabric_connection(access_token) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
