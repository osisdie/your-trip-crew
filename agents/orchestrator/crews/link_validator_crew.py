"""Link Validator Crew — validates URLs in itinerary content (code-only, no LLM)."""

import asyncio
import logging
import os
import re

import httpx

logger = logging.getLogger(__name__)

_URL_RE = re.compile(r'https?://[^\s\)\]"\'<>]+')

# Derive concurrency limit from runtime resources.
# In free-threading (PEP 703) builds, threads aren't GIL-bound so we can
# afford higher I/O concurrency.  For standard CPython the limit stays
# conservative to avoid socket / file-descriptor exhaustion.
_MAX_CONCURRENCY = min(os.cpu_count() or 4, 16) * 2


async def validate_links_async(content: str) -> str:
    """Validate all URLs in content and remove dead links.

    Uses a shared httpx.AsyncClient (connection pooling) and a semaphore
    to cap concurrency based on available runtime resources.
    """
    urls = list(set(_URL_RE.findall(content)))
    if not urls:
        return content

    sem = asyncio.Semaphore(_MAX_CONCURRENCY)

    async def _check(client: httpx.AsyncClient, url: str) -> tuple[str, bool]:
        async with sem:
            try:
                resp = await client.head(url)
                return url, resp.status_code < 400
            except Exception:
                return url, False

    async with httpx.AsyncClient(
        timeout=5.0,
        follow_redirects=True,
        limits=httpx.Limits(
            max_connections=_MAX_CONCURRENCY,
            max_keepalive_connections=_MAX_CONCURRENCY // 2,
        ),
    ) as client:
        results = await asyncio.gather(*[_check(client, u) for u in urls])

    dead_urls = {url for url, ok in results if not ok}

    if not dead_urls:
        logger.info("All %d URLs valid", len(urls))
        return content

    logger.info("Found %d dead URLs out of %d", len(dead_urls), len(urls))
    for url in dead_urls:
        content = re.sub(rf"\n\[?\d*\]?:?\s*{re.escape(url)}[^\n]*", "", content)
        content = re.sub(rf"\[([^\]]+)\]\({re.escape(url)}\)", r"\1", content)

    return content.strip()


def validate_links(content: str) -> str:
    """Synchronous wrapper for use in CrewAI Flow steps."""
    return asyncio.run(validate_links_async(content))
