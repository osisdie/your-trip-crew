"""Shared fixtures for E2E tests.

Tests run against a live backend. Set TEST_BASE_URL for your environment:
  - Inside trip-backend container (make test-backend): http://localhost:8000
  - From host with docker-compose (port 8200): http://localhost:8200
  - CI (inside container): http://localhost:8000
"""

import os

import httpx
import pytest

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def client():
    """Synchronous httpx client for the API."""
    with httpx.Client(base_url=BASE_URL, timeout=10) as c:
        yield c


@pytest.fixture(scope="session")
async def async_client():
    """Async httpx client for the API."""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
        yield c
