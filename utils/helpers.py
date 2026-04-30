"""
Stateless helper utilities shared across tests.

Keep this module free of Playwright state — pure functions only.
If a helper needs a `page`, it belongs in a page object instead.
"""

import re
from playwright.sync_api import Page, Locator
from utils.logger import get_logger
from utils import config

logger = get_logger(__name__)


def wait_for_network_idle(page: Page, timeout: int | None = None) -> None:
    """Wait for network to be idle (no requests for 500ms)."""
    wait_ms = timeout if timeout is not None else config.NETWORK_IDLE_TIMEOUT
    try:
        page.wait_for_load_state("networkidle", timeout=wait_ms)
    except Exception:
        logger.warning("Network did not reach idle within %dms — continuing.", wait_ms)


def assert_jobs_list_not_empty(jobs: list, department: str) -> None:
    """
    Assert that at least one job exists for the given department.

    Edge case handler: if the list is empty, the test fails with a clear,
    descriptive message rather than silently passing.
    """
    assert len(jobs) > 0, (
        f"Expected at least one open position for '{department}', "
        f"but the job list was empty. "
        f"This may indicate no current openings or a page/selector change."
    )


def normalize_whitespace(text: str) -> str:
    """Collapse all whitespace sequences to a single space and strip edges."""
    return re.sub(r"\s+", " ", text).strip()
