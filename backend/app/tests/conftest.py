"""Shared fixtures for E2E tests.

Tests run against the live backend inside Docker (http://trip-backend:8000).
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
