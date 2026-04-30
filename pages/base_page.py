"""
BasePage — abstract base for all page objects.

Responsibilities (Single Responsibility Principle):
- Hold the shared Playwright `page` reference
- Provide common cookie-consent dismissal used by all pages
- Expose a logger pre-named to the concrete subclass

Page objects NEVER assert — assertions belong in test functions.
"""

from playwright.sync_api import Page, Locator
from utils.logger import get_logger
from utils import config


class BasePage:
    """Base class for all page objects. Do not instantiate directly."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(type(self).__name__)
        self.page.set_default_timeout(config.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Cookie consent — shared across pages, defined once (DRY)
    # ------------------------------------------------------------------

    def dismiss_cookies(self) -> None:
        """Accept the cookie banner if it appears. Silently skips if absent."""
        try:
            btn = self.page.locator("#wt-cli-accept-all-btn")
            if btn.is_visible(timeout=5_000):
                self.logger.info("Dismissing cookie banner.")
                btn.click()
        except Exception:
            self.logger.debug("Cookie banner not found or already dismissed.")

    # ------------------------------------------------------------------
    # Shared locators
    # ------------------------------------------------------------------

    @property
    def nav_bar(self) -> Locator:
        return self.page.locator("nav, #navigation, [class*='nav'], header").first

    @property
    def footer(self) -> Locator:
        return self.page.locator("footer")
