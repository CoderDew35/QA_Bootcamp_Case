"""
conftest.py — pytest fixtures for the entire test suite.

This file is auto-discovered by pytest. All page-object fixtures and
browser lifecycle management live here.

Design decisions:
- `browser_context` handles tracing start/stop once — DRY, no duplication.
- Screenshot-on-failure hook is defined here, not in each test.
- Page objects are injected as fixtures so tests declare their dependencies
  explicitly (Dependency Inversion from SOLID).
"""

import os
import pytest

from pathlib import Path
from playwright.sync_api import Page, BrowserContext, Browser
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.jobs_page import JobsPage
from utils import config
from utils.logger import get_logger

logger = get_logger("conftest")

REPORTS_DIR = Path("reports")
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR = REPORTS_DIR / "traces"


# ---------------------------------------------------------------------------
# Session-scoped dirs — created once per run
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def ensure_report_dirs() -> None:
    """Create output directories once before any test runs."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    TRACES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Browser context with tracing
# ---------------------------------------------------------------------------

@pytest.fixture()
def context_with_tracing(context: BrowserContext):
    """
    Wrap the default pytest-playwright `context` fixture to enable tracing.

    Tracing is stopped and the zip saved only on failure (YAGNI — no trace
    files generated for passing tests).
    """
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    # Tracing is stopped inside the makereport hook below; nothing to do here.


# ---------------------------------------------------------------------------
# Page object fixtures — each test declares only what it needs
# ---------------------------------------------------------------------------

@pytest.fixture()
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture()
def careers_page(page: Page) -> CareersPage:
    return CareersPage(page)


@pytest.fixture()
def jobs_page(page: Page) -> JobsPage:
    return JobsPage(page)


# ---------------------------------------------------------------------------
# Screenshot on failure — single hook, no duplication across test files
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            test_name = item.name.replace("/", "_").replace("\\", "_")
            screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info("Failure screenshot saved: %s", screenshot_path)
            except Exception as exc:
                logger.warning("Could not capture screenshot: %s", exc)

            # Save trace for failed test
            context = page.context
            trace_path = TRACES_DIR / f"{test_name}.zip"
            try:
                context.tracing.stop(path=str(trace_path))
                logger.info("Trace saved: %s", trace_path)
            except Exception:
                # Tracing was not started for this context (e.g., using default pytest-playwright
                # context without context_with_tracing fixture) — safe to ignore.
                logger.debug("Tracing not active for this context; skipping trace save.")
        else:
            logger.debug("No `page` fixture found for test '%s'; skipping screenshot.", item.name)
